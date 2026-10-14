"""Anonymous count-aware program tokens with support-conditioned inference.

The model has no gene-position, gene-identity, or class-position parameters.
The v2 factorized path preserves each program slot until after leakage-safe
dataset contextualization.  A parameter-matched pooled control repeats the
legacy pooled row over the same slot axis.
"""

from __future__ import annotations

import math
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Literal

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

from hashprompt.episodes import DenseEpisodeBatch
from hashprompt.models.embedding import PromptForwardOutput

ProgramContextMode = Literal["legacy_pooled", "pooled_control", "factorized"]
SupportRowMode = Literal["individual_rows", "repeated_class_mean"]
LearnedHeadMode = Literal["query_class_pair", "support_class_bias"]


@dataclass(frozen=True)
class CountViewStatistics:
    log_mean: torch.Tensor
    log_std: torch.Tensor
    detection_rate: torch.Tensor


@dataclass(frozen=True)
class ProgramPFNSupportState:
    class_ids: torch.Tensor
    support_y_local: torch.Tensor
    support_rows: torch.Tensor
    class_rows: torch.Tensor
    count_statistics: CountViewStatistics
    raw_prototypes: torch.Tensor


@dataclass(frozen=True)
class ProgramViewConsistencyLoss:
    view_loss: torch.Tensor
    decorrelation_loss: torch.Tensor
    support_cosine: torch.Tensor
    query_cosine: torch.Tensor
    student_token_variance: torch.Tensor


def _balanced_accuracy(
    targets: torch.Tensor,
    predictions: torch.Tensor,
    num_classes: int,
) -> float:
    recalls = []
    for class_index in range(int(num_classes)):
        mask = targets == class_index
        if torch.any(mask):
            recalls.append((predictions[mask] == class_index).float().mean())
    return 0.0 if not recalls else float(torch.stack(recalls).mean().item())


class ProgramPFN(nn.Module):
    """Program-token set encoder followed by leakage-safe dataset attention."""

    def __init__(
        self,
        *,
        gene_feature_dim: int = 48,
        model_dim: int = 96,
        num_program_tokens: int = 8,
        num_heads: int = 4,
        cell_self_attention_layers: int = 1,
        dataset_attention_layers: int = 3,
        dataset_ff_multiplier: int = 4,
        dropout: float = 0.0,
        preserve_support_rows: bool = True,
        cell_chunk_size: int = 64,
        activation_checkpoint_cells: bool = False,
        eps: float = 1.0e-6,
        program_context_mode: ProgramContextMode = "legacy_pooled",
        residual_bound: float | None = None,
        support_row_mode: SupportRowMode = "individual_rows",
        learned_head_mode: LearnedHeadMode = "query_class_pair",
    ) -> None:
        super().__init__()
        if model_dim % num_heads != 0:
            raise ValueError("model_dim must be divisible by num_heads.")
        if num_program_tokens < 2:
            raise ValueError("num_program_tokens must be at least two.")
        if cell_chunk_size < 1:
            raise ValueError("cell_chunk_size must be positive.")
        if type(activation_checkpoint_cells) is not bool:
            raise TypeError("activation_checkpoint_cells must be a boolean.")
        if program_context_mode not in {
            "legacy_pooled",
            "pooled_control",
            "factorized",
        }:
            raise ValueError("unknown program_context_mode")
        if residual_bound is not None and (
            not math.isfinite(float(residual_bound)) or float(residual_bound) <= 0.0
        ):
            raise ValueError("residual_bound must be finite and positive")
        if support_row_mode not in {"individual_rows", "repeated_class_mean"}:
            raise ValueError("unknown support_row_mode")
        if not preserve_support_rows and support_row_mode != "individual_rows":
            raise ValueError("repeated_class_mean requires preserve_support_rows=True")
        if learned_head_mode not in {"query_class_pair", "support_class_bias"}:
            raise ValueError("unknown learned_head_mode")
        if learned_head_mode == "support_class_bias" and (
            program_context_mode != "factorized"
            or not preserve_support_rows
            or support_row_mode != "individual_rows"
        ):
            raise ValueError(
                "support_class_bias requires factorized context and "
                "individual support rows"
            )
        self.model_dim = int(model_dim)
        self.num_program_tokens = int(num_program_tokens)
        self.preserve_support_rows = bool(preserve_support_rows)
        self.cell_chunk_size = int(cell_chunk_size)
        self.activation_checkpoint_cells = activation_checkpoint_cells
        self.eps = float(eps)
        self.program_context_mode: ProgramContextMode = program_context_mode
        self.residual_bound = None if residual_bound is None else float(residual_bound)
        self.support_row_mode: SupportRowMode = support_row_mode
        self.learned_head_mode: LearnedHeadMode = learned_head_mode

        self.gene_encoder = nn.Sequential(
            nn.Linear(8, int(gene_feature_dim)),
            nn.GELU(),
            nn.Linear(int(gene_feature_dim), int(model_dim)),
            nn.LayerNorm(int(model_dim)),
        )
        self.program_queries = nn.Parameter(
            torch.randn(int(num_program_tokens), int(model_dim))
            / math.sqrt(float(model_dim))
        )
        self.gene_cross_attention = nn.MultiheadAttention(
            embed_dim=int(model_dim),
            num_heads=int(num_heads),
            dropout=float(dropout),
            batch_first=True,
        )
        self.gene_cross_norm = nn.LayerNorm(int(model_dim))

        cell_layer = nn.TransformerEncoderLayer(
            d_model=int(model_dim),
            nhead=int(num_heads),
            dim_feedforward=int(dataset_ff_multiplier) * int(model_dim),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.cell_transformer = nn.TransformerEncoder(
            cell_layer,
            num_layers=int(cell_self_attention_layers),
            enable_nested_tensor=False,
        )
        self.row_projection = nn.Sequential(
            nn.Linear(2 * int(model_dim), int(model_dim)),
            nn.GELU(),
            nn.LayerNorm(int(model_dim)),
        )
        self.class_projection = nn.Sequential(
            nn.Linear(2 * int(model_dim), int(model_dim)),
            nn.GELU(),
            nn.LayerNorm(int(model_dim)),
        )
        self.early_label_projection = nn.Sequential(
            nn.Linear(int(model_dim), int(model_dim)),
            nn.Tanh(),
        )
        self.support_type = nn.Parameter(torch.zeros(int(model_dim)))
        self.class_type = nn.Parameter(torch.zeros(int(model_dim)))
        self.query_type = nn.Parameter(torch.zeros(int(model_dim)))

        dataset_layer = nn.TransformerEncoderLayer(
            d_model=int(model_dim),
            nhead=int(num_heads),
            dim_feedforward=int(dataset_ff_multiplier) * int(model_dim),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.dataset_transformer = nn.TransformerEncoder(
            dataset_layer,
            num_layers=int(dataset_attention_layers),
            enable_nested_tensor=False,
        )
        self.learned_scorer = nn.Sequential(
            nn.Linear(4 * int(model_dim), int(model_dim)),
            nn.GELU(),
            nn.Linear(int(model_dim), 1),
        )
        nn.init.zeros_(self.learned_scorer[-1].weight)
        nn.init.zeros_(self.learned_scorer[-1].bias)
        self.log_raw_prototype_scale = nn.Parameter(torch.zeros(()))

    @property
    def uses_program_context(self) -> bool:
        return self.program_context_mode != "legacy_pooled"

    def _log_count_view(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        nonnegative = x.clamp_min(0.0)
        depth = nonnegative.sum(dim=1, keepdim=True).clamp_min(1.0)
        composition = nonnegative / depth
        return torch.log1p(10_000.0 * composition), composition

    def _fit_count_statistics(self, support_x: torch.Tensor) -> CountViewStatistics:
        support_log, _ = self._log_count_view(support_x)
        return CountViewStatistics(
            log_mean=support_log.mean(dim=0),
            log_std=support_log.std(dim=0, unbiased=False).clamp_min(self.eps),
            detection_rate=(support_x > 0).to(support_log.dtype).mean(dim=0),
        )

    def _gene_features(
        self,
        x: torch.Tensor,
        statistics: CountViewStatistics,
    ) -> torch.Tensor:
        log_view, composition = self._log_count_view(x)
        detected = (x > 0).to(log_view.dtype)
        gene_count = max(int(x.size(1)), 1)
        sqrt_composition = torch.sqrt(composition * float(gene_count) + self.eps)
        row_log_depth = torch.log1p(x.clamp_min(0.0).sum(dim=1, keepdim=True)) / 12.0
        row_detection = detected.mean(dim=1, keepdim=True)
        row_log_depth = row_log_depth.expand_as(log_view)
        row_detection = row_detection.expand_as(log_view)
        return torch.stack(
            (
                log_view / 10.0,
                detected,
                sqrt_composition,
                statistics.log_mean.unsqueeze(0).expand_as(log_view) / 10.0,
                statistics.log_std.unsqueeze(0).expand_as(log_view) / 10.0,
                statistics.detection_rate.unsqueeze(0).expand_as(log_view),
                row_log_depth,
                row_detection,
            ),
            dim=-1,
        )

    def _pool_programs(self, programs: torch.Tensor) -> torch.Tensor:
        pooled = torch.cat((programs.mean(dim=-2), programs.max(dim=-2).values), dim=-1)
        return self.row_projection(pooled)

    def _encode_cell_chunk(
        self,
        x: torch.Tensor,
        log_mean: torch.Tensor,
        log_std: torch.Tensor,
        detection_rate: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        statistics = CountViewStatistics(
            log_mean=log_mean,
            log_std=log_std,
            detection_rate=detection_rate,
        )
        gene_tokens = self.gene_encoder(self._gene_features(x, statistics))
        queries = self.program_queries.unsqueeze(0).expand(int(x.size(0)), -1, -1)
        attended, _ = self.gene_cross_attention(
            queries, gene_tokens, gene_tokens, need_weights=False
        )
        programs = self.gene_cross_norm(queries + attended)
        programs = self.cell_transformer(programs)
        return self._pool_programs(programs), programs

    def _encode_cells(
        self,
        x: torch.Tensor,
        statistics: CountViewStatistics,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        row_chunks: list[torch.Tensor] = []
        program_chunks: list[torch.Tensor] = []
        for start in range(0, int(x.size(0)), self.cell_chunk_size):
            stop = min(int(x.size(0)), start + self.cell_chunk_size)
            inputs = (
                x[start:stop],
                statistics.log_mean,
                statistics.log_std,
                statistics.detection_rate,
            )
            if (
                self.activation_checkpoint_cells
                and self.training
                and torch.is_grad_enabled()
            ):
                rows, programs = checkpoint(
                    self._encode_cell_chunk,
                    *inputs,
                    use_reentrant=False,
                    preserve_rng_state=True,
                )
            else:
                rows, programs = self._encode_cell_chunk(*inputs)
            row_chunks.append(rows)
            program_chunks.append(programs)
        return torch.cat(row_chunks, dim=0), torch.cat(program_chunks, dim=0)

    def encode_pre_context_program_tokens(
        self,
        support_x: torch.Tensor,
        query_x: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Encode one view using support-only statistics and no dataset context."""

        if support_x.ndim != 2 or query_x.ndim != 2:
            raise ValueError("Program-token inputs must have shape [rows, genes].")
        if int(support_x.size(0)) < 1 or int(query_x.size(0)) < 1:
            raise ValueError("Program-token inputs require support and query rows.")
        if int(support_x.size(1)) != int(query_x.size(1)):
            raise ValueError("Program-token support/query gene counts differ.")
        statistics = self._fit_count_statistics(support_x)
        _, support_programs = self._encode_cells(support_x, statistics)
        _, query_programs = self._encode_cells(query_x, statistics)
        return support_programs, query_programs

    def paired_program_view_consistency_loss(
        self,
        observed_support_x: torch.Tensor,
        observed_query_x: torch.Tensor,
        teacher_support_x: torch.Tensor,
        teacher_query_x: torch.Tensor,
    ) -> ProgramViewConsistencyLoss:
        """Match aligned observed/teacher slots with a detached shared encoder."""

        if (
            observed_support_x.shape != teacher_support_x.shape
            or observed_query_x.shape != teacher_query_x.shape
        ):
            raise ValueError("Observed and teacher program-token views are misaligned.")
        student_support, student_query = self.encode_pre_context_program_tokens(
            observed_support_x,
            observed_query_x,
        )
        with torch.no_grad():
            teacher_support, teacher_query = self.encode_pre_context_program_tokens(
                teacher_support_x,
                teacher_query_x,
            )
        support_cosine = F.cosine_similarity(
            student_support.float(), teacher_support.float(), dim=-1, eps=self.eps
        ).mean()
        query_cosine = F.cosine_similarity(
            student_query.float(), teacher_query.float(), dim=-1, eps=self.eps
        ).mean()
        view_loss = 1.0 - 0.5 * (support_cosine + query_cosine)

        student = torch.cat((student_support, student_query), dim=0).float()
        normalized = F.normalize(student, dim=-1, eps=self.eps)
        similarities = normalized @ normalized.transpose(-1, -2)
        off_diagonal = ~torch.eye(
            self.num_program_tokens,
            dtype=torch.bool,
            device=similarities.device,
        )
        decorrelation_loss = similarities[:, off_diagonal].square().mean()
        token_variance = student.var(dim=1, unbiased=False).mean()
        return ProgramViewConsistencyLoss(
            view_loss=view_loss,
            decorrelation_loss=decorrelation_loss,
            support_cosine=support_cosine,
            query_cosine=query_cosine,
            student_token_variance=token_variance,
        )

    def _localize_labels(
        self,
        support_y: torch.Tensor,
        class_ids: torch.Tensor,
    ) -> torch.Tensor:
        matches = support_y.unsqueeze(1) == class_ids.unsqueeze(0)
        if not torch.all(matches.sum(dim=1) == 1):
            raise ValueError(
                "Every support label must occur exactly once in class_ids."
            )
        return matches.to(dtype=torch.long).argmax(dim=1)

    def _class_rows(
        self,
        support_rows: torch.Tensor,
        support_y_local: torch.Tensor,
        num_classes: int,
    ) -> torch.Tensor:
        rows = []
        for class_index in range(int(num_classes)):
            members = support_rows[support_y_local == class_index]
            if members.numel() == 0:
                raise ValueError("Every class requires at least one support row.")
            rows.append(
                self.class_projection(
                    torch.cat(
                        (
                            members.mean(dim=0),
                            members.var(dim=0, unbiased=False),
                        ),
                        dim=-1,
                    )
                )
            )
        return torch.stack(rows, dim=0)

    def _raw_rows(self, x: torch.Tensor) -> torch.Tensor:
        log_view, _ = self._log_count_view(x)
        return F.normalize(log_view, dim=-1, eps=self.eps)

    @staticmethod
    def _type_offset(parameter: torch.Tensor, values: torch.Tensor) -> torch.Tensor:
        return parameter.view(*([1] * (values.ndim - 1)), -1)

    def _context_rows(self, rows: torch.Tensor, programs: torch.Tensor) -> torch.Tensor:
        if self.program_context_mode == "legacy_pooled":
            return rows
        if self.program_context_mode == "factorized":
            return programs
        # The v2 control destroys slot identity without adding a second active
        # projection path.  Both v2 arms therefore use ``row_projection`` only
        # for the shared post-context mean/max pooling.  This keeps the paired
        # screen focused on distinct versus pooled program context rather than
        # confounding it with projection depth.
        pooled = 0.5 * (programs.mean(dim=-2) + programs.max(dim=-2).values)
        return pooled.unsqueeze(1).expand(-1, self.num_program_tokens, -1)

    def fit_support(
        self,
        support_x: torch.Tensor,
        support_y: torch.Tensor,
        class_ids: torch.Tensor | None = None,
    ) -> ProgramPFNSupportState:
        if support_x.ndim != 2 or support_y.ndim != 1:
            raise ValueError(
                "Support tensors must have shapes [rows, genes] and [rows]."
            )
        if int(support_x.size(0)) != int(support_y.numel()):
            raise ValueError("Support rows and labels are misaligned.")
        support_y = support_y.to(device=support_x.device, dtype=torch.long)
        if class_ids is None:
            class_ids = torch.unique(support_y, sorted=True)
        else:
            class_ids = class_ids.to(device=support_x.device, dtype=torch.long)
        if int(class_ids.numel()) < 2:
            raise ValueError("ProgramPFN requires at least two classes.")
        support_y_local = self._localize_labels(support_y, class_ids)
        statistics = self._fit_count_statistics(support_x)
        support_rows, support_programs = self._encode_cells(support_x, statistics)
        context_support = self._context_rows(support_rows, support_programs)
        class_rows = self._class_rows(
            context_support, support_y_local, int(class_ids.numel())
        )
        dataset_support = context_support
        if self.support_row_mode == "repeated_class_mean":
            means = torch.stack(
                [
                    context_support[support_y_local == class_index].mean(dim=0)
                    for class_index in range(int(class_ids.numel()))
                ],
                dim=0,
            )
            dataset_support = means.index_select(0, support_y_local)
        labelled_support = (
            dataset_support
            + self._type_offset(self.support_type, dataset_support)
            + self.early_label_projection(class_rows).index_select(0, support_y_local)
        )
        class_tokens = class_rows + self._type_offset(self.class_type, class_rows)
        raw_context = (
            torch.autocast(device_type=support_x.device.type, enabled=False)
            if self.uses_program_context
            else nullcontext()
        )
        # The legacy branch intentionally retains its original autocast path.
        with raw_context:
            raw_input = support_x.float() if self.uses_program_context else support_x
            raw_support = self._raw_rows(raw_input)
            raw_prototypes = torch.stack(
                [
                    F.normalize(
                        raw_support[support_y_local == class_index].mean(dim=0),
                        dim=-1,
                        eps=self.eps,
                    )
                    for class_index in range(int(class_ids.numel()))
                ],
                dim=0,
            )
        return ProgramPFNSupportState(
            class_ids=class_ids,
            support_y_local=support_y_local,
            support_rows=labelled_support,
            class_rows=class_tokens,
            count_statistics=statistics,
            raw_prototypes=raw_prototypes,
        )

    def _inductive_attention_mask(
        self,
        base_count: int,
        query_count: int,
        device: torch.device,
    ) -> torch.Tensor:
        total = int(base_count) + int(query_count)
        mask = torch.zeros((total, total), dtype=torch.bool, device=device)
        if query_count == 0:
            return mask
        mask[:base_count, base_count:] = True
        mask[base_count:, base_count:] = True
        query_indices = torch.arange(query_count, device=device)
        mask[base_count + query_indices, base_count + query_indices] = False
        return mask

    def _contextualize(
        self,
        base: torch.Tensor,
        query_tokens: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        mask = self._inductive_attention_mask(
            int(base.size(0)), int(query_tokens.size(0)), base.device
        )
        tokens = torch.cat((base, query_tokens), dim=0)
        if self.program_context_mode == "legacy_pooled":
            contextual = self.dataset_transformer(
                tokens.unsqueeze(0), mask=mask
            ).squeeze(0)
            return contextual, mask
        contextual = self.dataset_transformer(
            tokens.permute(1, 0, 2), mask=mask
        ).permute(1, 0, 2)
        return contextual, mask

    def _context_base(
        self,
        state: ProgramPFNSupportState,
    ) -> tuple[torch.Tensor, int]:
        if self.preserve_support_rows:
            return (
                torch.cat((state.support_rows, state.class_rows), dim=0),
                int(state.support_rows.size(0)),
            )
        return state.class_rows, 0

    def _support_only_class_context(
        self,
        state: ProgramPFNSupportState,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        base, class_start = self._context_base(state)
        empty_queries = base.new_empty((0, *base.shape[1:]))
        contextual, mask = self._contextualize(base, empty_queries)
        class_context = contextual[
            class_start : class_start + int(state.class_ids.numel())
        ]
        context_shape = torch.tensor(
            tuple(contextual.shape), device=contextual.device, dtype=torch.long
        )
        if self.uses_program_context:
            class_context = self._pool_programs(class_context)
        return class_context, mask, context_shape

    def _bounded_residual(
        self, learned_features: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if self.residual_bound is None:
            unbounded = self.learned_scorer(learned_features).squeeze(-1)
            centered = unbounded - unbounded.mean(dim=-1, keepdim=True)
            return unbounded, unbounded, centered
        with torch.autocast(device_type=learned_features.device.type, enabled=False):
            unbounded = self.learned_scorer(learned_features.float()).squeeze(-1)
            centered = unbounded - unbounded.mean(dim=-1, keepdim=True)
            bound = float(self.residual_bound)
            residual = bound * torch.tanh(centered / bound)
        return residual, unbounded, centered

    def score_inductive(
        self,
        state: ProgramPFNSupportState,
        query_x: torch.Tensor,
        *,
        return_debug: bool = False,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        if query_x.ndim != 2:
            raise ValueError("query_x must have shape [rows, genes].")
        if int(query_x.size(1)) != int(state.raw_prototypes.size(1)):
            raise ValueError("Support and query gene counts differ.")
        if self.learned_head_mode == "query_class_pair":
            query_rows, query_programs = self._encode_cells(
                query_x, state.count_statistics
            )
            query_base = self._context_rows(query_rows, query_programs)
            query_tokens = query_base + self._type_offset(
                self.query_type, query_base
            )
            base, class_start = self._context_base(state)
            contextual, mask = self._contextualize(base, query_tokens)
            class_context = contextual[
                class_start : class_start + int(state.class_ids.numel())
            ]
            query_context = contextual[int(base.size(0)) :]
            context_shape = torch.tensor(
                tuple(contextual.shape),
                device=contextual.device,
                dtype=torch.long,
            )
            if self.uses_program_context:
                class_context = self._pool_programs(class_context)
                query_context = self._pool_programs(query_context)

            query_expanded = query_context.unsqueeze(1).expand(
                -1, int(class_context.size(0)), -1
            )
            class_expanded = class_context.unsqueeze(0).expand(
                int(query_context.size(0)), -1, -1
            )
            learned_features = torch.cat(
                (
                    query_expanded,
                    class_expanded,
                    query_expanded * class_expanded,
                    torch.abs(query_expanded - class_expanded),
                ),
                dim=-1,
            )
            learned_logits, unbounded, centered = self._bounded_residual(
                learned_features
            )
        else:
            class_context, mask, context_shape = self._support_only_class_context(
                state
            )
            class_expanded = class_context.unsqueeze(0)
            task_context = class_context.mean(dim=0, keepdim=True)
            task_expanded = task_context.unsqueeze(1).expand(
                1, int(class_context.size(0)), -1
            )
            learned_features = torch.cat(
                (
                    task_expanded,
                    class_expanded,
                    task_expanded * class_expanded,
                    torch.abs(task_expanded - class_expanded),
                ),
                dim=-1,
            )
            bias, bias_unbounded, bias_centered = self._bounded_residual(
                learned_features
            )
            query_count = int(query_x.size(0))
            learned_logits = bias.expand(query_count, -1)
            unbounded = bias_unbounded.expand(query_count, -1)
            centered = bias_centered.expand(query_count, -1)
            # Encode row-local query representations only after the learned
            # class bias is fixed. This preserves structural query independence
            # even when dropout is enabled during training.
            query_rows, query_programs = self._encode_cells(
                query_x, state.count_statistics
            )
            query_context = query_rows
        if self.residual_bound is None and not self.uses_program_context:
            raw_query = self._raw_rows(query_x)
            raw_control_logits = raw_query @ state.raw_prototypes.transpose(0, 1)
            raw_scale = self.log_raw_prototype_scale.exp().clamp(0.1, 100.0)
            raw_logits = raw_control_logits * raw_scale
            logits = raw_logits + learned_logits
        else:
            with torch.autocast(device_type=query_x.device.type, enabled=False):
                raw_query = self._raw_rows(query_x.float())
                raw_control_logits = raw_query @ state.raw_prototypes.float().transpose(
                    0, 1
                )
                raw_scale = self.log_raw_prototype_scale.float().exp().clamp(0.1, 100.0)
                raw_logits = raw_control_logits * raw_scale
                logits = raw_logits + learned_logits.float()
        debug = {
            "raw_logits": raw_logits,
            "raw_control_logits": raw_control_logits,
            "learned_logits": learned_logits,
            "learned_logits_unbounded": unbounded,
            "learned_logits_centered": centered,
            "query_context": query_context,
            "class_context": class_context,
            "query_programs": query_programs,
            "context_input_shape": context_shape,
            "attention_mask": mask,
            "raw_prototype_scale": raw_scale,
        }
        return logits, debug if return_debug else {}

    def forward_episode(self, episode: DenseEpisodeBatch) -> PromptForwardOutput:
        if episode.query_y is None:
            raise ValueError("Training episodes require query labels.")
        device = next(self.parameters()).device
        support_x = episode.support_x.to(device=device, dtype=torch.float32)
        support_y = episode.support_y.to(device=device, dtype=torch.long)
        query_x = episode.query_x.to(device=device, dtype=torch.float32)
        query_y = episode.query_y.to(device=device, dtype=torch.long)
        class_ids = episode.class_ids.to(device=device, dtype=torch.long)
        state = self.fit_support(support_x, support_y, class_ids)
        logits, debug = self.score_inductive(state, query_x, return_debug=True)
        if self.residual_bound is None and not self.uses_program_context:
            loss = F.cross_entropy(logits, query_y)
        else:
            with torch.autocast(device_type=device.type, enabled=False):
                loss = F.cross_entropy(logits.float(), query_y)
        predictions = logits.argmax(dim=1)
        histogram = torch.bincount(
            predictions, minlength=int(class_ids.numel())
        ).float()
        learned = debug["learned_logits"]
        bound = self.residual_bound
        saturation = (
            torch.zeros((), device=learned.device)
            if bound is None
            else (learned.abs() >= 0.95 * float(bound)).float().mean()
        )
        aux_metrics = {
            "train_query_balanced_accuracy": _balanced_accuracy(
                query_y, predictions, int(class_ids.numel())
            ),
            "train_query_max_pred_share": float(
                (histogram.max() / histogram.sum().clamp_min(1.0)).item()
            ),
            "raw_logit_abs_mean": float(debug["raw_logits"].abs().mean().detach()),
            "learned_logit_abs_mean": float(learned.abs().mean().detach()),
        }
        if self.residual_bound is not None:
            aux_metrics.update(
                {
                    "learned_logit_abs_max": float(learned.abs().max().detach()),
                    "residual_saturation_fraction": float(saturation.detach()),
                    "raw_prototype_scale": float(debug["raw_prototype_scale"].detach()),
                }
            )
        debug_tensors = {
            "raw_logits": debug["raw_logits"].detach(),
            "learned_logits": learned.detach(),
            "class_histogram": histogram.detach(),
        }
        if self.residual_bound is not None:
            debug_tensors["learned_logits_unbounded"] = debug[
                "learned_logits_unbounded"
            ].detach()
        return PromptForwardOutput(
            z_q=debug["query_context"],
            y_q=query_y,
            protos=debug["class_context"],
            classes=state.class_ids,
            logits=logits,
            proto_loss=loss,
            aux_losses={},
            aux_metrics=aux_metrics,
            debug_tensors=debug_tensors,
        )

    def forward(self, episode: DenseEpisodeBatch) -> PromptForwardOutput:
        return self.forward_episode(episode)


__all__ = [
    "CountViewStatistics",
    "LearnedHeadMode",
    "ProgramContextMode",
    "ProgramPFN",
    "ProgramPFNSupportState",
    "ProgramViewConsistencyLoss",
    "SupportRowMode",
]
