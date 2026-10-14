"""Query-conditioned same-gene cellular PFN.

The model applies a shared nonlinear relation on the task-local gene axis.
The incumbent order forms fixed, query-local support barycenters first; the
row-first order applies the relation to individual support rows and aggregates
the resulting relation features. Genes are reduced only after that relation.
Queries remain independent, genes have no positions or identities, and the
learned score is a bounded residual over a fixed empirical-Bayes count expert.

This is intentionally a standalone model rather than a ProgramPFN subclass.
The earlier ProgramPFN families compress each cell before comparing labelled
support with a query; this model tests the distinct ordering

    fixed query-local support barycenters
      -> same-gene nonlinear relation
      -> permutation-invariant gene reduction.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

from hashprompt.episodes import DenseEpisodeBatch
from hashprompt.models.embedding import PromptForwardOutput
from hashprompt.models.program_pfn import _balanced_accuracy

AlignedOperatorMode = Literal["aligned", "gene_deranged", "uniform_only"]
AlignedRelationOrder = Literal["barycenter_first", "row_first"]

PROTOTYPE_MODE_COUNT = 4
RELATION_INPUT_DIM = 28


@dataclass(frozen=True)
class AlignedPrototypeSupportState:
    class_ids: torch.Tensor
    support_y_local: torch.Tensor
    support_x: torch.Tensor
    class_member_indices: torch.Tensor
    class_member_mask: torch.Tensor
    class_support_counts: torch.Tensor
    support_depths: torch.Tensor
    support_detection: torch.Tensor
    global_log_mean: torch.Tensor
    global_log_std: torch.Tensor
    global_detection: torch.Tensor
    class_log_mean: torch.Tensor
    class_log_std: torch.Tensor
    class_detection: torch.Tensor
    deranged_support_x: torch.Tensor
    deranged_global_log_mean: torch.Tensor
    deranged_global_log_std: torch.Tensor
    deranged_global_detection: torch.Tensor
    deranged_class_log_mean: torch.Tensor
    deranged_class_log_std: torch.Tensor
    deranged_class_detection: torch.Tensor
    eb_log_probabilities: torch.Tensor | None
    support_raw_norms: torch.Tensor
    support_pearson_norms: torch.Tensor
    relative_derangement: torch.Tensor
    derangement_aligned_gene_fraction: torch.Tensor


def _row_zscore(values: torch.Tensor, eps: float) -> torch.Tensor:
    centered = values - values.mean(dim=1, keepdim=True)
    scale = centered.square().mean(dim=1, keepdim=True).sqrt().clamp_min(eps)
    return centered / scale


class AlignedPrototypeResidualPFN(nn.Module):
    """Fixed local barycenters plus a learned same-gene EB residual."""

    def __init__(
        self,
        *,
        relation_dim: int = 224,
        relation_hidden_dim: int = 448,
        model_dim: int = 448,
        num_program_tokens: int = 8,
        num_heads: int = 8,
        program_layers: int = 2,
        ff_multiplier: int = 4,
        dropout: float = 0.0,
        residual_bound: float = 2.0,
        eb_equivalent_cells: float = 4.0,
        eb_dispersion: float = 0.1,
        pair_chunk_size: int = 8,
        gene_chunk_size: int = 1024,
        member_chunk_size: int = 4,
        checkpoint_relation_chunks: bool = True,
        operator_mode: AlignedOperatorMode = "aligned",
        relation_order: AlignedRelationOrder = "barycenter_first",
        counterfactual_deranged_anchor: bool = False,
        eps: float = 1.0e-6,
    ) -> None:
        super().__init__()
        if relation_dim < 8 or relation_hidden_dim < 8:
            raise ValueError("relation dimensions must be at least eight")
        if model_dim < 8 or model_dim % num_heads != 0:
            raise ValueError("model_dim must be positive and divisible by num_heads")
        if num_program_tokens < 2:
            raise ValueError("num_program_tokens must be at least two")
        if program_layers < 1:
            raise ValueError("program_layers must be positive")
        if pair_chunk_size < 1 or gene_chunk_size < 1 or member_chunk_size < 1:
            raise ValueError("pair, gene, and member chunk sizes must be positive")
        if operator_mode not in {"aligned", "gene_deranged", "uniform_only"}:
            raise ValueError("unknown aligned prototype operator mode")
        if relation_order not in {"barycenter_first", "row_first"}:
            raise ValueError("unknown aligned prototype relation order")
        if not math.isfinite(float(residual_bound)) or residual_bound <= 0.0:
            raise ValueError("residual_bound must be finite and positive")
        if not math.isfinite(float(eb_equivalent_cells)) or eb_equivalent_cells <= 0:
            raise ValueError("EB equivalent cells must be finite and positive")
        if not math.isfinite(float(eb_dispersion)) or eb_dispersion < 0.0:
            raise ValueError("EB dispersion must be finite and nonnegative")
        if type(checkpoint_relation_chunks) is not bool:
            raise TypeError("checkpoint_relation_chunks must be a boolean")
        if type(counterfactual_deranged_anchor) is not bool:
            raise TypeError("counterfactual_deranged_anchor must be a boolean")
        if counterfactual_deranged_anchor and operator_mode != "aligned":
            raise ValueError(
                "counterfactual deranged anchoring requires aligned operator mode"
            )

        self.relation_dim = int(relation_dim)
        self.model_dim = int(model_dim)
        self.num_program_tokens = int(num_program_tokens)
        self.residual_bound = float(residual_bound)
        self.eb_equivalent_cells = float(eb_equivalent_cells)
        self.eb_dispersion = float(eb_dispersion)
        self.pair_chunk_size = int(pair_chunk_size)
        self.gene_chunk_size = int(gene_chunk_size)
        self.member_chunk_size = int(member_chunk_size)
        self.checkpoint_relation_chunks = bool(checkpoint_relation_chunks)
        self.operator_mode: AlignedOperatorMode = operator_mode
        self.relation_order: AlignedRelationOrder = relation_order
        self.counterfactual_deranged_anchor = bool(counterfactual_deranged_anchor)
        self.eps = float(eps)

        self.relation_mlp = nn.Sequential(
            nn.Linear(RELATION_INPUT_DIM, int(relation_hidden_dim)),
            nn.GELU(),
            nn.Linear(int(relation_hidden_dim), int(relation_dim)),
            nn.LayerNorm(int(relation_dim)),
        )
        self.reduction_projection = nn.Sequential(
            nn.Linear(4 * int(relation_dim), int(model_dim)),
            nn.GELU(),
            nn.LayerNorm(int(model_dim)),
        )
        self.prototype_roles = nn.Parameter(
            torch.randn(PROTOTYPE_MODE_COUNT, int(model_dim))
            / math.sqrt(float(model_dim))
        )
        # The generic trainer explicitly checks that this parameter receives
        # gradients. It is the query set for the four fixed prototype tokens.
        self.program_queries = nn.Parameter(
            torch.randn(int(num_program_tokens), int(model_dim))
            / math.sqrt(float(model_dim))
        )
        self.prototype_cross_attention = nn.MultiheadAttention(
            embed_dim=int(model_dim),
            num_heads=int(num_heads),
            dropout=float(dropout),
            batch_first=True,
        )
        self.prototype_cross_norm = nn.LayerNorm(int(model_dim))
        layer = nn.TransformerEncoderLayer(
            d_model=int(model_dim),
            nhead=int(num_heads),
            dim_feedforward=int(ff_multiplier) * int(model_dim),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.program_transformer = nn.TransformerEncoder(
            layer,
            num_layers=int(program_layers),
            enable_nested_tensor=False,
        )
        self.residual_scorer = nn.Sequential(
            nn.Linear(2 * int(model_dim) + 1, int(model_dim)),
            nn.GELU(),
            nn.Linear(int(model_dim), 1),
        )
        nn.init.zeros_(self.residual_scorer[-1].weight)
        nn.init.zeros_(self.residual_scorer[-1].bias)

    @staticmethod
    def _localize_labels(
        labels: torch.Tensor,
        class_ids: torch.Tensor,
        *,
        require_all_classes: bool = True,
    ) -> torch.Tensor:
        matches = labels.unsqueeze(1) == class_ids.unsqueeze(0)
        if not torch.all(matches.sum(dim=1) == 1):
            raise ValueError("every label must occur exactly once in class_ids")
        local = matches.to(dtype=torch.long).argmax(dim=1)
        if require_all_classes and torch.any(
            torch.bincount(local, minlength=int(class_ids.numel())) == 0
        ):
            raise ValueError("every class requires at least one support row")
        return local

    @staticmethod
    def _log_view(
        values: torch.Tensor,
        depths: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        nonnegative = values.clamp_min(0.0)
        composition = nonnegative / depths.clamp_min(1.0)
        return torch.log1p(10_000.0 * composition), composition

    def _fit_eb_log_probabilities(
        self,
        support_x: torch.Tensor,
        support_y_local: torch.Tensor,
        num_classes: int,
    ) -> torch.Tensor:
        counts = support_x.float()
        class_counts = torch.zeros(
            (int(num_classes), int(counts.size(1))),
            device=counts.device,
            dtype=torch.float32,
        )
        class_counts.index_add_(0, support_y_local, counts)
        class_depths = class_counts.sum(dim=1)
        global_counts = class_counts.sum(dim=0)
        global_probability = (global_counts + 0.5) / (
            global_counts.sum() + 0.5 * float(counts.size(1))
        )
        median_depth = torch.quantile(
            counts.sum(dim=1),
            0.5,
            interpolation="midpoint",
        ).clamp_min(1.0)
        tau = self.eb_equivalent_cells * median_depth
        probabilities = (class_counts + tau * global_probability.unsqueeze(0)) / (
            class_depths.unsqueeze(1) + tau
        )
        probabilities = probabilities.clamp_min(1.0e-30)
        probabilities = probabilities / probabilities.sum(dim=1, keepdim=True)
        return probabilities.log()

    def _relative_derangement(
        self,
        global_log_mean: torch.Tensor,
        global_log_std: torch.Tensor,
        global_detection: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        gene_count = int(global_log_mean.numel())
        identity = torch.arange(gene_count, device=global_log_mean.device)
        if gene_count < 2:
            return (
                identity,
                torch.zeros_like(identity),
                torch.ones(1, device=identity.device, dtype=torch.long),
            )
        # The ordering uses only task-local exchangeable statistics. Under a
        # joint gene permutation the key follows the genes, unlike a fixed
        # positional roll.
        key = (
            global_log_mean.double()
            + math.sqrt(2.0) * global_log_std.double()
            + math.pi * global_detection.double()
        )
        order = torch.argsort(key, stable=True)
        sorted_key = key.index_select(0, order)
        _, sorted_groups, group_counts = torch.unique_consecutive(
            sorted_key,
            return_inverse=True,
            return_counts=True,
        )
        groups = torch.empty_like(sorted_groups)
        groups[order] = sorted_groups
        tied = group_counts.index_select(0, sorted_groups) > 1
        unique_order = order[~tied]
        source = identity.clone()
        if int(unique_order.numel()) >= 2:
            source[unique_order] = torch.roll(unique_order, shifts=-1)
        return source, groups, group_counts

    def fit_support(
        self,
        support_x: torch.Tensor,
        support_y: torch.Tensor,
        class_ids: torch.Tensor | None = None,
        *,
        count_eligible: bool = True,
    ) -> AlignedPrototypeSupportState:
        if type(count_eligible) is not bool:
            raise TypeError("count_eligible must be a boolean")
        if support_x.ndim != 2 or support_y.ndim != 1:
            raise ValueError(
                "support tensors must have shapes [rows, genes] and [rows]"
            )
        if int(support_x.size(0)) != int(support_y.numel()):
            raise ValueError("support rows and labels are misaligned")
        if int(support_x.size(0)) < 2 or int(support_x.size(1)) < 1:
            raise ValueError("support requires at least two rows and one gene")
        if not torch.isfinite(support_x).all() or torch.any(support_x < 0):
            raise ValueError("support values must be finite and nonnegative")
        with torch.autocast(device_type=support_x.device.type, enabled=False):
            values = support_x.float()
            labels = support_y.to(device=values.device, dtype=torch.long)
            if class_ids is None:
                classes = torch.unique(labels, sorted=True)
            else:
                classes = class_ids.to(device=values.device, dtype=torch.long)
            if int(classes.numel()) < 2:
                raise ValueError("aligned prototype PFN requires at least two classes")
            local = self._localize_labels(labels, classes)
            class_counts = torch.bincount(
                local,
                minlength=int(classes.numel()),
            )
            maximum = int(class_counts.max().item())
            member_indices = torch.zeros(
                (int(classes.numel()), maximum),
                device=values.device,
                dtype=torch.long,
            )
            member_mask = torch.zeros_like(member_indices, dtype=torch.bool)
            for class_index in range(int(classes.numel())):
                members = torch.nonzero(
                    local == class_index,
                    as_tuple=False,
                ).flatten()
                member_indices[class_index, : int(members.numel())] = members
                member_mask[class_index, : int(members.numel())] = True

            depths = values.sum(dim=1, keepdim=True).clamp_min(1.0)
            detection = (values > 0).float()
            log_view, _ = self._log_view(values, depths)
            global_log_mean = log_view.mean(dim=0)
            global_log_std = log_view.std(
                dim=0,
                unbiased=False,
            ).clamp_min(self.eps)
            global_detection = detection.mean(dim=0)
            pearson = (
                (log_view - global_log_mean.unsqueeze(0)) / global_log_std.unsqueeze(0)
            ).clamp(-8.0, 8.0)
            class_log_mean = []
            class_log_std = []
            class_detection = []
            for class_index in range(int(classes.numel())):
                mask = local == class_index
                class_log = log_view[mask]
                class_log_mean.append(class_log.mean(dim=0))
                class_log_std.append(class_log.std(dim=0, unbiased=False))
                class_detection.append(detection[mask].mean(dim=0))

            relative_derangement, derangement_groups, group_counts = (
                self._relative_derangement(
                    global_log_mean,
                    global_log_std,
                    global_detection,
                )
            )
            deranged_values = values.index_select(
                1,
                relative_derangement,
            ).clone()
            per_gene_group_counts = group_counts.index_select(
                0,
                derangement_groups,
            )
            tied_genes = per_gene_group_counts > 1
            if bool(tied_genes.any()):
                group_sums = values.new_zeros(
                    int(values.size(0)),
                    int(group_counts.numel()),
                )
                group_sums.index_add_(1, derangement_groups, values)
                leave_one_out = (
                    group_sums.index_select(1, derangement_groups) - values
                ) / (per_gene_group_counts.to(dtype=values.dtype) - 1.0).clamp_min(1.0)
                deranged_values[:, tied_genes] = leave_one_out[:, tied_genes]
            derangement_aligned_gene_fraction = (
                (deranged_values == values).all(dim=0).float().mean()
            )
            deranged_log_view, _ = self._log_view(deranged_values, depths)
            deranged_detection = (deranged_values > 0).float()
            deranged_global_log_mean = deranged_log_view.mean(dim=0)
            deranged_global_log_std = deranged_log_view.std(
                dim=0,
                unbiased=False,
            ).clamp_min(self.eps)
            deranged_global_detection = deranged_detection.mean(dim=0)
            deranged_class_log_mean = []
            deranged_class_log_std = []
            deranged_class_detection = []
            for class_index in range(int(classes.numel())):
                mask = local == class_index
                class_log = deranged_log_view[mask]
                deranged_class_log_mean.append(class_log.mean(dim=0))
                deranged_class_log_std.append(class_log.std(dim=0, unbiased=False))
                deranged_class_detection.append(deranged_detection[mask].mean(dim=0))

            return AlignedPrototypeSupportState(
                class_ids=classes,
                support_y_local=local,
                support_x=values,
                class_member_indices=member_indices,
                class_member_mask=member_mask,
                class_support_counts=class_counts.to(dtype=torch.float32),
                support_depths=depths[:, 0],
                support_detection=detection.mean(dim=1),
                global_log_mean=global_log_mean,
                global_log_std=global_log_std,
                global_detection=global_detection,
                class_log_mean=torch.stack(class_log_mean),
                class_log_std=torch.stack(class_log_std),
                class_detection=torch.stack(class_detection),
                deranged_support_x=deranged_values,
                deranged_global_log_mean=deranged_global_log_mean,
                deranged_global_log_std=deranged_global_log_std,
                deranged_global_detection=deranged_global_detection,
                deranged_class_log_mean=torch.stack(
                    deranged_class_log_mean,
                ),
                deranged_class_log_std=torch.stack(
                    deranged_class_log_std,
                ),
                deranged_class_detection=torch.stack(
                    deranged_class_detection,
                ),
                eb_log_probabilities=(
                    self._fit_eb_log_probabilities(
                        values,
                        local,
                        int(classes.numel()),
                    )
                    if count_eligible
                    else None
                ),
                support_raw_norms=log_view.square()
                .sum(dim=1)
                .sqrt()
                .clamp_min(self.eps),
                support_pearson_norms=pearson.square()
                .sum(dim=1)
                .sqrt()
                .clamp_min(self.eps),
                relative_derangement=relative_derangement,
                derangement_aligned_gene_fraction=(derangement_aligned_gene_fraction),
            )

    def _score_fixed_eb(
        self,
        query_x: torch.Tensor,
        log_probabilities: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        query = query_x.float()
        probabilities = log_probabilities.exp()
        phi = self.eb_dispersion
        pieces: list[torch.Tensor] = []
        for start in range(0, int(query.size(0)), 16):
            values = query[start : start + 16]
            if phi == 0.0:
                pieces.append(values @ log_probabilities.transpose(0, 1))
                continue
            depths = values.sum(dim=1)
            means = depths[:, None, None] * probabilities[None, :, :]
            curvature = torch.log1p(phi * means)
            pieces.append(
                torch.sum(
                    values[:, None, :] * log_probabilities[None, :, :]
                    - (values[:, None, :] + 1.0 / phi) * curvature,
                    dim=2,
                )
            )
        raw = torch.cat(pieces, dim=0)
        raw = raw - raw.mean(dim=1, keepdim=True)
        return _row_zscore(raw, self.eps), raw

    def _query_support_similarities(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        query_count = int(query_x.size(0))
        support_count = int(state.support_x.size(0))
        raw_dot = query_x.new_zeros(
            (query_count, support_count),
            dtype=torch.float32,
        )
        pearson_dot = torch.zeros_like(raw_dot)
        query_raw_square = query_x.new_zeros(query_count, dtype=torch.float32)
        query_pearson_square = torch.zeros_like(query_raw_square)
        query_depths = query_x.float().sum(dim=1, keepdim=True).clamp_min(1.0)
        gene_count = int(query_x.size(1))
        for start in range(0, gene_count, self.gene_chunk_size):
            stop = min(gene_count, start + self.gene_chunk_size)
            support_values = state.support_x[:, start:stop]
            query_values = query_x[:, start:stop].float()
            support_log, _ = self._log_view(
                support_values,
                state.support_depths[:, None],
            )
            query_log, _ = self._log_view(query_values, query_depths)
            mean = state.global_log_mean[start:stop]
            std = state.global_log_std[start:stop]
            support_pearson = (
                (support_log - mean.unsqueeze(0)) / std.unsqueeze(0)
            ).clamp(-8.0, 8.0)
            query_pearson = ((query_log - mean.unsqueeze(0)) / std.unsqueeze(0)).clamp(
                -8.0, 8.0
            )
            raw_dot.add_(query_log @ support_log.transpose(0, 1))
            pearson_dot.add_(query_pearson @ support_pearson.transpose(0, 1))
            query_raw_square.add_(query_log.square().sum(dim=1))
            query_pearson_square.add_(query_pearson.square().sum(dim=1))
        raw_denominator = query_raw_square.sqrt().clamp_min(self.eps).unsqueeze(
            1
        ) * state.support_raw_norms.unsqueeze(0)
        pearson_denominator = query_pearson_square.sqrt().clamp_min(self.eps).unsqueeze(
            1
        ) * state.support_pearson_norms.unsqueeze(0)
        return raw_dot / raw_denominator, pearson_dot / pearson_denominator

    @staticmethod
    def _masked_standardize(
        values: torch.Tensor,
        mask: torch.Tensor,
        eps: float,
    ) -> torch.Tensor:
        weights = mask.to(dtype=values.dtype)
        count = weights.sum(dim=-1, keepdim=True).clamp_min(1.0)
        mean = (values * weights).sum(dim=-1, keepdim=True) / count
        variance = ((values - mean).square() * weights).sum(
            dim=-1, keepdim=True
        ) / count
        standardized = (values - mean) / variance.sqrt().clamp_min(eps)
        return torch.where(mask, standardized, torch.zeros_like(standardized))

    @staticmethod
    def _masked_softmax(values: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        masked = values.masked_fill(~mask, -torch.inf)
        result = torch.softmax(masked, dim=-1)
        return torch.where(mask, result, torch.zeros_like(result))

    def _prototype_weights(
        self,
        state: AlignedPrototypeSupportState,
        raw_similarity: torch.Tensor,
        pearson_similarity: torch.Tensor,
        *,
        operator_mode: AlignedOperatorMode,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        indices = state.class_member_indices
        mask = state.class_member_mask.unsqueeze(0).expand(
            int(raw_similarity.size(0)),
            -1,
            -1,
        )
        raw = raw_similarity[:, indices]
        pearson = pearson_similarity[:, indices]
        raw_z = self._masked_standardize(raw, mask, self.eps)
        pearson_z = self._masked_standardize(pearson, mask, self.eps)
        uniform = mask.to(dtype=raw.dtype)
        uniform = uniform / uniform.sum(dim=-1, keepdim=True).clamp_min(1.0)
        raw_weights = self._masked_softmax(raw_z, mask)
        pearson_weights = self._masked_softmax(pearson_z, mask)
        mixed_weights = self._masked_softmax(0.5 * (raw_z + pearson_z), mask)
        if operator_mode == "uniform_only":
            raw_weights = uniform
            pearson_weights = uniform
            mixed_weights = uniform
        weights = torch.stack(
            (uniform, raw_weights, pearson_weights, mixed_weights),
            dim=2,
        )

        mixed_similarity = 0.5 * (raw + pearson)
        retrieval = torch.logsumexp(
            mixed_similarity.masked_fill(~mask, -torch.inf),
            dim=-1,
        ) - torch.log(mask.sum(dim=-1).to(dtype=mixed_similarity.dtype).clamp_min(1.0))
        return weights, _row_zscore(retrieval, self.eps)

    def _relation_chunk_reductions(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
        query_depths: torch.Tensor,
        query_row_detection: torch.Tensor,
        pair_indices: torch.Tensor,
        prototype_weights: torch.Tensor,
        *,
        start: int,
        stop: int,
        operator_mode: AlignedOperatorMode,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        if self.relation_order == "row_first":
            return self._row_first_relation_chunk_reductions(
                state,
                query_x,
                query_depths,
                query_row_detection,
                pair_indices,
                prototype_weights,
                start=start,
                stop=stop,
                operator_mode=operator_mode,
            )
        class_count = int(state.class_ids.numel())
        query_indices = torch.div(
            pair_indices,
            class_count,
            rounding_mode="floor",
        )
        class_indices = torch.remainder(pair_indices, class_count)
        target_gene_indices = torch.arange(
            start,
            stop,
            device=query_x.device,
        )
        if operator_mode == "gene_deranged":
            support_source = state.deranged_support_x
            global_log_mean = state.deranged_global_log_mean
            global_log_std = state.deranged_global_log_std
            global_detection = state.deranged_global_detection
            class_log_mean = state.deranged_class_log_mean
            class_log_std = state.deranged_class_log_std
            class_detection = state.deranged_class_detection
        else:
            support_source = state.support_x
            global_log_mean = state.global_log_mean
            global_log_std = state.global_log_std
            global_detection = state.global_detection
            class_log_mean = state.class_log_mean
            class_log_std = state.class_log_std
            class_detection = state.class_detection
        members = state.class_member_indices.index_select(0, class_indices)
        pair_count, maximum_members = members.shape
        summary_count = int(prototype_weights.size(1))
        if summary_count < 1:
            raise ValueError("prototype_weights must contain at least one summary")
        member_values = support_source.index_select(
            0,
            members.reshape(-1),
        )[:, target_gene_indices].reshape(
            pair_count,
            maximum_members,
            stop - start,
        )
        member_depths = state.support_depths.index_select(
            0,
            members.reshape(-1),
        ).reshape(pair_count, maximum_members, 1)
        support_log, support_composition = self._log_view(
            member_values,
            member_depths,
        )
        support_detection = (member_values > 0).float()
        support_pearson = (
            (support_log - global_log_mean[target_gene_indices].view(1, 1, -1))
            / global_log_std[target_gene_indices].view(1, 1, -1)
        ).clamp(-8.0, 8.0)
        gene_count = max(int(state.support_x.size(1)), 1)
        support_views = torch.stack(
            (
                support_log / 10.0,
                support_pearson / 4.0,
                support_detection,
                torch.sqrt(support_composition * float(gene_count) + self.eps),
            ),
            dim=-1,
        )
        prototypes = torch.einsum(
            "pmb,pbgv->pmgv",
            prototype_weights,
            support_views,
        )

        query_values = query_x.index_select(0, query_indices)[
            :, target_gene_indices
        ].float()
        pair_query_depths = query_depths.index_select(
            0,
            query_indices,
        ).unsqueeze(1)
        query_log, query_composition = self._log_view(
            query_values,
            pair_query_depths,
        )
        query_detection = (query_values > 0).float()
        query_pearson = (
            (query_log - global_log_mean[target_gene_indices].unsqueeze(0))
            / global_log_std[target_gene_indices].unsqueeze(0)
        ).clamp(-8.0, 8.0)
        query_views = torch.stack(
            (
                query_log / 10.0,
                query_pearson / 4.0,
                query_detection,
                torch.sqrt(query_composition * float(gene_count) + self.eps),
            ),
            dim=-1,
        )
        query_expanded = query_views[:, None, :, :].expand(
            -1,
            summary_count,
            -1,
            -1,
        )
        relation_views = torch.cat(
            (
                query_expanded,
                prototypes,
                query_expanded * prototypes,
                torch.abs(query_expanded - prototypes),
            ),
            dim=-1,
        )

        global_features = (
            torch.stack(
                (
                    global_log_mean[target_gene_indices] / 10.0,
                    global_log_std[target_gene_indices] / 10.0,
                    global_detection[target_gene_indices],
                ),
                dim=-1,
            )
            .view(1, 1, stop - start, 3)
            .expand(
                pair_count,
                summary_count,
                -1,
                -1,
            )
        )
        class_features = torch.stack(
            (
                class_log_mean.index_select(0, class_indices)[:, target_gene_indices]
                / 10.0,
                class_log_std.index_select(0, class_indices)[:, target_gene_indices]
                / 10.0,
                class_detection.index_select(0, class_indices)[:, target_gene_indices],
            ),
            dim=-1,
        )[:, None].expand(-1, summary_count, -1, -1)
        query_log_depth = torch.log1p(pair_query_depths[:, 0]) / 12.0
        pair_query_detection = query_row_detection.index_select(0, query_indices)
        query_auxiliary = torch.stack(
            (query_log_depth, pair_query_detection),
            dim=-1,
        )[:, None, None, :].expand(
            -1,
            summary_count,
            stop - start,
            -1,
        )
        member_log_depth = (
            torch.log1p(state.support_depths.index_select(0, members.reshape(-1)))
            / 12.0
        ).reshape(pair_count, maximum_members)
        member_detection = state.support_detection.index_select(
            0,
            members.reshape(-1),
        ).reshape(pair_count, maximum_members)
        prototype_log_depth = torch.einsum(
            "pmb,pb->pm",
            prototype_weights,
            member_log_depth,
        )
        prototype_detection = torch.einsum(
            "pmb,pb->pm",
            prototype_weights,
            member_detection,
        )
        prototype_auxiliary = torch.stack(
            (prototype_log_depth, prototype_detection),
            dim=-1,
        )[:, :, None, :].expand(-1, -1, stop - start, -1)
        support_scale = (
            torch.log1p(state.class_support_counts.index_select(0, class_indices))
            / math.log(101.0)
        )[:, None, None, None].expand(
            -1,
            summary_count,
            stop - start,
            1,
        )

        # A universally valid fixed analytic channel: per-gene contribution to
        # the raw/Pearson retrieval relation. Unlike a per-gene NB term, this
        # remains defined for the processed-expression Zebra stress track.
        retrieval_contribution = 0.5 * (
            query_expanded[..., 0] * prototypes[..., 0]
            + query_expanded[..., 1] * prototypes[..., 1]
        )
        # The raw/Pearson views are already support-standardized and scaled.
        # Keep this product on that fixed scale rather than normalizing inside
        # a gene chunk, which would make the operator depend on chunk borders.
        retrieval_contribution = retrieval_contribution.unsqueeze(-1)
        features = torch.cat(
            (
                relation_views,
                global_features,
                class_features,
                query_auxiliary,
                prototype_auxiliary,
                support_scale,
                retrieval_contribution,
            ),
            dim=-1,
        )
        if int(features.size(-1)) != RELATION_INPUT_DIM:
            raise RuntimeError("aligned relation feature surface changed")
        relation = self.relation_mlp(features)
        with torch.autocast(device_type=relation.device.type, enabled=False):
            values = relation.float()
            return (
                values.sum(dim=2),
                values.square().sum(dim=2),
                torch.amax(values, dim=2),
                torch.logsumexp(values, dim=2),
            )

    def _row_first_relation_chunk_reductions(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
        query_depths: torch.Tensor,
        query_row_detection: torch.Tensor,
        pair_indices: torch.Tensor,
        prototype_weights: torch.Tensor,
        *,
        start: int,
        stop: int,
        operator_mode: AlignedOperatorMode,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Apply the relation per support row before fixed class aggregation."""

        class_count = int(state.class_ids.numel())
        query_indices = torch.div(
            pair_indices,
            class_count,
            rounding_mode="floor",
        )
        class_indices = torch.remainder(pair_indices, class_count)
        target_gene_indices = torch.arange(
            start,
            stop,
            device=query_x.device,
        )
        if operator_mode == "gene_deranged":
            support_source = state.deranged_support_x
            global_log_mean = state.deranged_global_log_mean
            global_log_std = state.deranged_global_log_std
            global_detection = state.deranged_global_detection
            class_log_mean = state.deranged_class_log_mean
            class_log_std = state.deranged_class_log_std
            class_detection = state.deranged_class_detection
        else:
            support_source = state.support_x
            global_log_mean = state.global_log_mean
            global_log_std = state.global_log_std
            global_detection = state.global_detection
            class_log_mean = state.class_log_mean
            class_log_std = state.class_log_std
            class_detection = state.class_detection

        members = state.class_member_indices.index_select(0, class_indices)
        member_mask = state.class_member_mask.index_select(0, class_indices)
        pair_count, maximum_members = members.shape
        gene_width = stop - start
        gene_count = max(int(state.support_x.size(1)), 1)

        query_values = query_x.index_select(0, query_indices)[
            :, target_gene_indices
        ].float()
        pair_query_depths = query_depths.index_select(
            0,
            query_indices,
        ).unsqueeze(1)
        query_log, query_composition = self._log_view(
            query_values,
            pair_query_depths,
        )
        query_detection = (query_values > 0).float()
        query_pearson = (
            (query_log - global_log_mean[target_gene_indices].unsqueeze(0))
            / global_log_std[target_gene_indices].unsqueeze(0)
        ).clamp(-8.0, 8.0)
        query_views = torch.stack(
            (
                query_log / 10.0,
                query_pearson / 4.0,
                query_detection,
                torch.sqrt(query_composition * float(gene_count) + self.eps),
            ),
            dim=-1,
        )

        global_features = torch.stack(
            (
                global_log_mean[target_gene_indices] / 10.0,
                global_log_std[target_gene_indices] / 10.0,
                global_detection[target_gene_indices],
            ),
            dim=-1,
        ).view(1, 1, gene_width, 3)
        class_features = torch.stack(
            (
                class_log_mean.index_select(0, class_indices)[
                    :, target_gene_indices
                ]
                / 10.0,
                class_log_std.index_select(0, class_indices)[
                    :, target_gene_indices
                ]
                / 10.0,
                class_detection.index_select(0, class_indices)[
                    :, target_gene_indices
                ],
            ),
            dim=-1,
        )[:, None]
        query_log_depth = torch.log1p(pair_query_depths[:, 0]) / 12.0
        pair_query_detection = query_row_detection.index_select(0, query_indices)
        query_auxiliary = torch.stack(
            (query_log_depth, pair_query_detection),
            dim=-1,
        )[:, None, None, :]
        support_scale = (
            torch.log1p(state.class_support_counts.index_select(0, class_indices))
            / math.log(101.0)
        )[:, None, None, None]

        aggregated_relation: torch.Tensor | None = None
        for member_start in range(0, maximum_members, self.member_chunk_size):
            member_stop = min(
                maximum_members,
                member_start + self.member_chunk_size,
            )
            chunk_members = members[:, member_start:member_stop]
            chunk_mask = member_mask[:, member_start:member_stop]
            chunk_width = member_stop - member_start
            flattened_members = chunk_members.reshape(-1)
            member_values = support_source.index_select(
                0,
                flattened_members,
            )[:, target_gene_indices].reshape(
                pair_count,
                chunk_width,
                gene_width,
            )
            member_depths = state.support_depths.index_select(
                0,
                flattened_members,
            ).reshape(pair_count, chunk_width, 1)
            support_log, support_composition = self._log_view(
                member_values,
                member_depths,
            )
            support_detection = (member_values > 0).float()
            support_pearson = (
                (
                    support_log
                    - global_log_mean[target_gene_indices].view(1, 1, -1)
                )
                / global_log_std[target_gene_indices].view(1, 1, -1)
            ).clamp(-8.0, 8.0)
            support_views = torch.stack(
                (
                    support_log / 10.0,
                    support_pearson / 4.0,
                    support_detection,
                    torch.sqrt(
                        support_composition * float(gene_count) + self.eps
                    ),
                ),
                dim=-1,
            )
            query_expanded = query_views[:, None].expand(
                -1,
                chunk_width,
                -1,
                -1,
            )
            relation_views = torch.cat(
                (
                    query_expanded,
                    support_views,
                    query_expanded * support_views,
                    torch.abs(query_expanded - support_views),
                ),
                dim=-1,
            )
            member_log_depth = (
                torch.log1p(
                    state.support_depths.index_select(0, flattened_members)
                )
                / 12.0
            ).reshape(pair_count, chunk_width)
            member_detection = state.support_detection.index_select(
                0,
                flattened_members,
            ).reshape(pair_count, chunk_width)
            member_auxiliary = torch.stack(
                (member_log_depth, member_detection),
                dim=-1,
            )[:, :, None, :].expand(-1, -1, gene_width, -1)
            retrieval_contribution = 0.5 * (
                query_expanded[..., 0] * support_views[..., 0]
                + query_expanded[..., 1] * support_views[..., 1]
            )
            features = torch.cat(
                (
                    relation_views,
                    global_features.expand(
                        pair_count,
                        chunk_width,
                        -1,
                        -1,
                    ),
                    class_features.expand(-1, chunk_width, -1, -1),
                    query_auxiliary.expand(-1, chunk_width, gene_width, -1),
                    member_auxiliary,
                    support_scale.expand(-1, chunk_width, gene_width, -1),
                    retrieval_contribution.unsqueeze(-1),
                ),
                dim=-1,
            )
            if int(features.size(-1)) != RELATION_INPUT_DIM:
                raise RuntimeError("aligned row relation feature surface changed")
            relation = self.relation_mlp(features)
            weights = prototype_weights[
                :,
                :,
                member_start:member_stop,
            ]
            weights = weights * chunk_mask[:, None, :].to(dtype=weights.dtype)
            with torch.autocast(device_type=relation.device.type, enabled=False):
                weighted_relation = torch.einsum(
                    "pmb,pbgr->pmgr",
                    weights.float(),
                    relation.float(),
                )
            aggregated_relation = (
                weighted_relation
                if aggregated_relation is None
                else aggregated_relation + weighted_relation
            )

        if aggregated_relation is None:
            raise RuntimeError("row-first relation received no support members")
        with torch.autocast(
            device_type=aggregated_relation.device.type,
            enabled=False,
        ):
            values = aggregated_relation.float()
            return (
                values.sum(dim=2),
                values.square().sum(dim=2),
                torch.amax(values, dim=2),
                torch.logsumexp(values, dim=2),
            )

    def _reduce_pair_relations(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
        query_depths: torch.Tensor,
        query_row_detection: torch.Tensor,
        pair_indices: torch.Tensor,
        prototype_weights: torch.Tensor,
        *,
        operator_mode: AlignedOperatorMode,
    ) -> torch.Tensor:
        gene_count = int(query_x.size(1))
        total_sum = None
        total_square = None
        total_max = None
        total_lse = None
        for start in range(0, gene_count, self.gene_chunk_size):
            stop = min(gene_count, start + self.gene_chunk_size)

            def reductions(
                anchor: torch.Tensor,
                *,
                chunk_start: int = start,
                chunk_stop: int = stop,
            ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
                del anchor
                return self._relation_chunk_reductions(
                    state,
                    query_x,
                    query_depths,
                    query_row_detection,
                    pair_indices,
                    prototype_weights,
                    start=chunk_start,
                    stop=chunk_stop,
                    operator_mode=operator_mode,
                )

            if (
                self.checkpoint_relation_chunks
                and self.training
                and torch.is_grad_enabled()
            ):
                chunk_sum, chunk_square, chunk_max, chunk_lse = checkpoint(
                    reductions,
                    self.program_queries,
                    use_reentrant=False,
                    preserve_rng_state=True,
                )
            else:
                chunk_sum, chunk_square, chunk_max, chunk_lse = reductions(
                    self.program_queries
                )
            total_sum = chunk_sum if total_sum is None else total_sum + chunk_sum
            total_square = (
                chunk_square if total_square is None else total_square + chunk_square
            )
            total_max = (
                chunk_max if total_max is None else torch.maximum(total_max, chunk_max)
            )
            total_lse = (
                chunk_lse
                if total_lse is None
                else torch.logaddexp(total_lse, chunk_lse)
            )
        if (
            total_sum is None
            or total_square is None
            or total_max is None
            or total_lse is None
        ):
            raise RuntimeError("gene reduction received no genes")
        return torch.cat(
            (
                total_sum / float(gene_count),
                torch.sqrt(total_square / float(gene_count) + self.eps),
                total_max,
                total_lse - math.log(float(gene_count)),
            ),
            dim=-1,
        )

    @staticmethod
    def _representation_diagnostics(
        reduced: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        matrix = reduced.float().reshape(-1, int(reduced.size(-1)))
        channel_std = matrix.std(dim=0, unbiased=False)
        centered = matrix - matrix.mean(dim=0, keepdim=True)
        # A diagonal-covariance participation proxy is cheap enough to record
        # on every synthetic task. Full SVD diagnostics belong in bounded
        # evaluation, not the training hot path.
        eigenvalues = centered.square().mean(dim=0).clamp_min(0.0)
        participation = (
            eigenvalues.sum().square() / eigenvalues.square().sum().clamp_min(1.0e-12)
        )
        return {
            "relation_channel_std_mean": channel_std.mean(),
            "relation_channel_std_min": channel_std.min(),
            "relation_participation_ratio": participation,
        }

    def score_inductive(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
        *,
        return_debug: bool = False,
        operator_mode_override: AlignedOperatorMode | None = None,
        fixed_base_logits: torch.Tensor | None = None,
        count_eligible: bool = True,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        if type(count_eligible) is not bool:
            raise TypeError("count_eligible must be a boolean")
        if query_x.ndim != 2 or int(query_x.size(0)) < 1:
            raise ValueError("query_x must have shape [nonempty rows, genes]")
        if int(query_x.size(1)) != int(state.support_x.size(1)):
            raise ValueError("support and query gene counts differ")
        if not torch.isfinite(query_x).all() or torch.any(query_x < 0):
            raise ValueError("query values must be finite and nonnegative")
        operator_mode = (
            self.operator_mode
            if operator_mode_override is None
            else operator_mode_override
        )
        if operator_mode not in {"aligned", "gene_deranged", "uniform_only"}:
            raise ValueError("unknown aligned prototype operator mode override")

        with torch.autocast(device_type=query_x.device.type, enabled=False):
            query = query_x.float()
            internal_raw_eb: torch.Tensor | None = None
            if fixed_base_logits is None:
                if not count_eligible or state.eb_log_probabilities is None:
                    raise ValueError(
                        "noncount scoring requires explicit fixed_base_logits"
                    )
                fixed_base, internal_raw_eb = self._score_fixed_eb(
                    query,
                    state.eb_log_probabilities,
                )
            else:
                fixed_base = fixed_base_logits.to(
                    device=query.device,
                    dtype=torch.float32,
                )
                expected_shape = (
                    int(query.size(0)),
                    int(state.class_ids.numel()),
                )
                if tuple(fixed_base.shape) != expected_shape:
                    raise ValueError("fixed_base_logits has the wrong shape")
                if not torch.isfinite(fixed_base).all():
                    raise ValueError("fixed_base_logits must be finite")
            with torch.no_grad():
                raw_similarity, pearson_similarity = self._query_support_similarities(
                    state, query
                )
                prototype_weights, fixed_retrieval = self._prototype_weights(
                    state,
                    raw_similarity,
                    pearson_similarity,
                    operator_mode=operator_mode,
                )
                member_mask = state.class_member_mask.unsqueeze(0).expand(
                    int(query.size(0)),
                    -1,
                    -1,
                )
                uniform = member_mask.to(dtype=raw_similarity.dtype)
                uniform = uniform / uniform.sum(
                    dim=-1,
                    keepdim=True,
                ).clamp_min(1.0)
                raw_class = (
                    raw_similarity[:, state.class_member_indices] * uniform
                ).sum(dim=-1)
                pearson_class = (
                    pearson_similarity[:, state.class_member_indices] * uniform
                ).sum(dim=-1)
                fixed_raw = _row_zscore(raw_class, self.eps)
                fixed_pearson = _row_zscore(pearson_class, self.eps)
                fixed_raw_pearson = 0.5 * (fixed_raw + fixed_pearson)

        query_count = int(query.size(0))
        class_count = int(state.class_ids.numel())
        pair_count = query_count * class_count
        query_depths = query.sum(dim=1).clamp_min(1.0)
        query_row_detection = (query > 0).float().mean(dim=1)
        learned_chunks: list[torch.Tensor] = []
        prototype_token_chunks: list[torch.Tensor] = []
        program_chunks: list[torch.Tensor] = []
        reduced_chunks: list[torch.Tensor] = []
        flattened_weights = prototype_weights.reshape(
            pair_count,
            PROTOTYPE_MODE_COUNT,
            int(prototype_weights.size(-1)),
        )
        flattened_retrieval = fixed_retrieval.reshape(pair_count, 1)
        for start in range(0, pair_count, self.pair_chunk_size):
            stop = min(pair_count, start + self.pair_chunk_size)
            pair_indices = torch.arange(start, stop, device=query.device)
            reduced = self._reduce_pair_relations(
                state,
                query,
                query_depths,
                query_row_detection,
                pair_indices,
                flattened_weights[start:stop],
                operator_mode=operator_mode,
            )
            prototype_tokens = self.reduction_projection(reduced)
            prototype_tokens = prototype_tokens + self.prototype_roles.unsqueeze(0)
            program_seed = self.program_queries.unsqueeze(0).expand(
                stop - start,
                -1,
                -1,
            )
            attended, _ = self.prototype_cross_attention(
                program_seed,
                prototype_tokens,
                prototype_tokens,
                need_weights=False,
            )
            programs = self.prototype_cross_norm(program_seed + attended)
            programs = self.program_transformer(programs)
            pooled = torch.cat(
                (
                    programs.mean(dim=1),
                    torch.amax(programs, dim=1),
                ),
                dim=-1,
            )
            head_features = torch.cat(
                (
                    pooled.float(),
                    flattened_retrieval[start:stop],
                ),
                dim=-1,
            )
            with torch.autocast(device_type=query.device.type, enabled=False):
                learned_chunks.append(
                    self.residual_scorer(head_features.float()).squeeze(-1)
                )
            prototype_token_chunks.append(prototype_tokens)
            program_chunks.append(programs)
            reduced_chunks.append(reduced)

        unbounded = torch.cat(learned_chunks).reshape(query_count, class_count)
        centered = unbounded - unbounded.mean(dim=1, keepdim=True)
        learned = self.residual_bound * torch.tanh(centered / self.residual_bound)
        logits = fixed_base + learned
        prototype_tokens = torch.cat(prototype_token_chunks).reshape(
            query_count,
            class_count,
            PROTOTYPE_MODE_COUNT,
            self.model_dim,
        )
        programs = torch.cat(program_chunks).reshape(
            query_count,
            class_count,
            self.num_program_tokens,
            self.model_dim,
        )
        reduced = torch.cat(reduced_chunks).reshape(
            query_count,
            class_count,
            PROTOTYPE_MODE_COUNT,
            4 * self.relation_dim,
        )
        relation_diagnostics = self._representation_diagnostics(reduced.detach())
        with torch.no_grad():
            nonuniform_weights = prototype_weights[:, :, 1:].float()
            prototype_weight_entropy = (
                -(nonuniform_weights * nonuniform_weights.clamp_min(self.eps).log())
                .sum(dim=-1)
                .mean()
            )
            prototype_effective_support = (
                nonuniform_weights.square().sum(dim=-1).clamp_min(self.eps).reciprocal()
            ).mean()
            centered_barycenters = reduced.float() - reduced.float().mean(
                dim=2,
                keepdim=True,
            )
            barycenter_relation_diversity = centered_barycenters.square().mean().sqrt()
        query_context = programs.mean(dim=(1, 2))
        class_context = self.prototype_roles.mean(dim=0, keepdim=True).expand(
            class_count,
            -1,
        )
        debug = {
            "fixed_base_logits": fixed_base,
            "raw_logits": fixed_base,
            "raw_control_logits": fixed_base,
            "learned_logits": learned,
            "learned_logits_unbounded": unbounded,
            "learned_logits_centered": centered,
            "fixed_retrieval_logits": fixed_retrieval,
            "fixed_raw_prototype_logits": fixed_raw,
            "fixed_pearson_prototype_logits": fixed_pearson,
            "fixed_raw_pearson_logits": fixed_raw_pearson,
            "prototype_weights": prototype_weights,
            "prototype_tokens": prototype_tokens,
            "query_programs": programs,
            "query_context": query_context,
            "class_context": class_context,
            "prototype_weight_entropy": prototype_weight_entropy,
            "prototype_effective_support": prototype_effective_support,
            "barycenter_relation_diversity": barycenter_relation_diversity,
            "derangement_aligned_gene_fraction": (
                state.derangement_aligned_gene_fraction
            ),
            "operator_mode": torch.tensor(
                {"aligned": 0, "gene_deranged": 1, "uniform_only": 2}[operator_mode],
                device=query.device,
            ),
            "relation_order": torch.tensor(
                {"barycenter_first": 0, "row_first": 1}[self.relation_order],
                device=query.device,
            ),
            "maximum_relation_block_elements": torch.tensor(
                self.pair_chunk_size
                * (
                    PROTOTYPE_MODE_COUNT
                    if self.relation_order == "barycenter_first"
                    else max(PROTOTYPE_MODE_COUNT, self.member_chunk_size)
                )
                * self.gene_chunk_size
                * self.relation_dim,
                device=query.device,
                dtype=torch.long,
            ),
            **relation_diagnostics,
        }
        if count_eligible:
            debug["fixed_eb_logits"] = fixed_base
        if internal_raw_eb is not None:
            debug["raw_eb_logits"] = internal_raw_eb
        return logits, debug if return_debug else {}

    def forward_episode(self, episode: DenseEpisodeBatch) -> PromptForwardOutput:
        if episode.query_y is None:
            raise ValueError("training episodes require query labels")
        device = next(self.parameters()).device
        support_x = episode.support_x.to(device=device, dtype=torch.float32)
        support_y = episode.support_y.to(device=device, dtype=torch.long)
        query_x = episode.query_x.to(device=device, dtype=torch.float32)
        query_y_public = episode.query_y.to(device=device, dtype=torch.long)
        class_ids = episode.class_ids.to(device=device, dtype=torch.long)
        query_y = self._localize_labels(
            query_y_public,
            class_ids,
            require_all_classes=False,
        )
        state = self.fit_support(support_x, support_y, class_ids)
        logits, debug = self.score_inductive(
            state,
            query_x,
            return_debug=True,
        )
        with torch.autocast(device_type=device.type, enabled=False):
            loss = F.cross_entropy(logits.float(), query_y)
        aux_losses: dict[str, torch.Tensor] = {}
        counterfactual_metrics: dict[str, float] = {}
        counterfactual_debug_tensors: dict[str, torch.Tensor] = {}
        if (
            self.counterfactual_deranged_anchor
            and self.training
            and torch.is_grad_enabled()
        ):
            counterfactual_logits, counterfactual_debug = self.score_inductive(
                state,
                query_x,
                return_debug=True,
                operator_mode_override="gene_deranged",
            )
            if not torch.equal(
                debug["fixed_eb_logits"],
                counterfactual_debug["fixed_eb_logits"],
            ):
                raise RuntimeError(
                    "aligned and deranged counterfactual EB logits differ"
                )
            with torch.autocast(device_type=device.type, enabled=False):
                fixed_log_probabilities = F.log_softmax(
                    debug["fixed_eb_logits"].detach().float(),
                    dim=-1,
                )
                counterfactual_log_probabilities = F.log_softmax(
                    counterfactual_logits.float(),
                    dim=-1,
                )
                per_query_kl = (
                    fixed_log_probabilities.exp()
                    * (fixed_log_probabilities - counterfactual_log_probabilities)
                ).sum(dim=-1)
                counterfactual_kl = per_query_kl.clamp_min(0.0).mean()
            if not torch.isfinite(counterfactual_kl):
                raise FloatingPointError(
                    "counterfactual deranged EB anchor is non-finite"
                )
            counterfactual_learned = counterfactual_debug["learned_logits"]
            aux_losses["counterfactual_deranged_eb_anchor_kl"] = counterfactual_kl
            counterfactual_metrics.update(
                {
                    "counterfactual_deranged_eb_anchor_kl": float(
                        counterfactual_kl.detach()
                    ),
                    "counterfactual_deranged_learned_logit_abs_mean": float(
                        counterfactual_learned.abs().mean().detach()
                    ),
                    "counterfactual_deranged_residual_saturation_fraction": (
                        float(
                            (counterfactual_learned.abs() >= 0.95 * self.residual_bound)
                            .float()
                            .mean()
                            .detach()
                        )
                    ),
                }
            )
            counterfactual_debug_tensors.update(
                {
                    "counterfactual_deranged_fixed_eb_logits": (
                        counterfactual_debug["fixed_eb_logits"].detach()
                    ),
                    "counterfactual_deranged_learned_logits": (
                        counterfactual_learned.detach()
                    ),
                }
            )
        predictions = logits.argmax(dim=1)
        histogram = torch.bincount(
            predictions,
            minlength=int(class_ids.numel()),
        ).float()
        learned = debug["learned_logits"]
        return PromptForwardOutput(
            z_q=debug["query_context"],
            y_q=query_y,
            protos=debug["class_context"],
            classes=state.class_ids,
            logits=logits,
            proto_loss=loss,
            aux_losses=aux_losses,
            aux_metrics={
                "train_query_balanced_accuracy": _balanced_accuracy(
                    query_y,
                    predictions,
                    int(class_ids.numel()),
                ),
                "train_query_max_pred_share": float(
                    (histogram.max() / histogram.sum().clamp_min(1.0)).item()
                ),
                "raw_logit_abs_mean": float(
                    debug["fixed_eb_logits"].abs().mean().detach()
                ),
                "learned_logit_abs_mean": float(learned.abs().mean().detach()),
                "fixed_retrieval_logit_abs_mean": float(
                    debug["fixed_retrieval_logits"].abs().mean().detach()
                ),
                "residual_saturation_fraction": float(
                    (learned.abs() >= 0.95 * self.residual_bound)
                    .float()
                    .mean()
                    .detach()
                ),
                "relation_channel_std_mean": float(
                    debug["relation_channel_std_mean"].detach()
                ),
                "relation_channel_std_min": float(
                    debug["relation_channel_std_min"].detach()
                ),
                "relation_participation_ratio": float(
                    debug["relation_participation_ratio"].detach()
                ),
                "prototype_weight_entropy": float(
                    debug["prototype_weight_entropy"].detach()
                ),
                "prototype_effective_support": float(
                    debug["prototype_effective_support"].detach()
                ),
                "barycenter_relation_diversity": float(
                    debug["barycenter_relation_diversity"].detach()
                ),
                "derangement_aligned_gene_fraction": float(
                    debug["derangement_aligned_gene_fraction"].detach()
                ),
                **counterfactual_metrics,
            },
            debug_tensors={
                "fixed_eb_logits": debug["fixed_eb_logits"].detach(),
                "learned_logits": learned.detach(),
                "fixed_retrieval_logits": (debug["fixed_retrieval_logits"].detach()),
                "class_histogram": histogram.detach(),
                **counterfactual_debug_tensors,
            },
        )

    def forward(self, episode: DenseEpisodeBatch) -> PromptForwardOutput:
        return self.forward_episode(episode)


__all__ = [
    "AlignedOperatorMode",
    "AlignedRelationOrder",
    "AlignedPrototypeResidualPFN",
    "AlignedPrototypeSupportState",
]
