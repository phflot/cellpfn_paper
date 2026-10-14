"""Aligned same-gene PFN with support-derived multimodal class summaries.

The incumbent aligned PFN forms four query-conditioned analytic barycenters.
This family instead learns a small, query-independent set of support summaries
per class, applies the proven same-gene query--summary relation, and predicts a
bounded correction over an explicitly supplied analytic base.  Support routing
is linear in the number of support rows and never uses query rows or labels.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import torch
import torch.nn as nn
from torch.utils.checkpoint import checkpoint

from hashprompt.models.aligned_prototype_pfn import (
    AlignedOperatorMode,
    AlignedPrototypeResidualPFN,
    AlignedPrototypeSupportState,
    _row_zscore,
)


MAX_CLASS_SUMMARIES = 8
SupportSummaryMode = Literal[
    "learned",
    "uniform_one",
    "deterministic_two",
    "deterministic_four",
    "deterministic_eight",
]


@dataclass(frozen=True)
class AlignedClassInducingSupportState:
    base: AlignedPrototypeSupportState
    support_row_embeddings: torch.Tensor
    learned_summary_weights: torch.Tensor
    learned_summary_active: torch.Tensor

    @property
    def class_ids(self) -> torch.Tensor:
        return self.base.class_ids


class _ResidualRouterBlock(nn.Module):
    def __init__(self, model_dim: int, ff_multiplier: int = 4) -> None:
        super().__init__()
        hidden = int(ff_multiplier) * int(model_dim)
        self.norm = nn.LayerNorm(int(model_dim))
        self.ff = nn.Sequential(
            nn.Linear(int(model_dim), hidden),
            nn.GELU(),
            nn.Linear(hidden, int(model_dim)),
        )

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return values + self.ff(self.norm(values))


class AlignedClassInducingPFN(AlignedPrototypeResidualPFN):
    """Multiple support-derived class summaries plus aligned query relations."""

    def __init__(
        self,
        *,
        num_active_class_summaries: int = 4,
        support_router_layers: int = 3,
        **kwargs: object,
    ) -> None:
        if int(num_active_class_summaries) not in {2, 4, 8}:
            raise ValueError("num_active_class_summaries must be 2, 4, or 8")
        if int(support_router_layers) < 1:
            raise ValueError("support_router_layers must be positive")
        if str(kwargs.get("relation_order", "barycenter_first")) != (
            "barycenter_first"
        ):
            raise ValueError("aligned class induction uses barycenter-first relations")
        super().__init__(**kwargs)
        self.num_active_class_summaries = int(num_active_class_summaries)
        self.support_router_layers = int(support_router_layers)
        del self.prototype_roles

        self.class_summary_roles = nn.Parameter(
            torch.randn(MAX_CLASS_SUMMARIES, self.model_dim)
            / math.sqrt(float(self.model_dim))
        )
        self.class_summary_queries = nn.Parameter(
            torch.randn(MAX_CLASS_SUMMARIES, self.model_dim)
            / math.sqrt(float(self.model_dim))
        )
        support_gene_dim = min(64, max(32, self.relation_dim))
        self.support_gene_mlp = nn.Sequential(
            nn.Linear(10, support_gene_dim),
            nn.GELU(),
            nn.Linear(support_gene_dim, support_gene_dim),
            nn.LayerNorm(support_gene_dim),
        )
        self.support_row_projection = nn.Sequential(
            nn.Linear(4 * support_gene_dim, self.model_dim),
            nn.GELU(),
            nn.LayerNorm(self.model_dim),
        )
        self.support_router_blocks = nn.ModuleList(
            _ResidualRouterBlock(self.model_dim)
            for _ in range(self.support_router_layers)
        )
        self.summary_query_projection = nn.Linear(self.model_dim, self.model_dim)
        self.summary_key_projection = nn.Linear(self.model_dim, self.model_dim)
        gate_hidden = max(32, self.model_dim // 2)
        self.base_confidence_gate = nn.Sequential(
            nn.Linear(6, gate_hidden),
            nn.GELU(),
            nn.Linear(gate_hidden, 1),
        )

    def _support_row_embeddings(
        self,
        state: AlignedPrototypeSupportState,
    ) -> torch.Tensor:
        values = state.support_x
        gene_count = int(values.size(1))
        local = state.support_y_local
        total_sum: torch.Tensor | None = None
        total_square: torch.Tensor | None = None
        total_max: torch.Tensor | None = None
        total_lse: torch.Tensor | None = None

        for start in range(0, gene_count, self.gene_chunk_size):
            stop = min(gene_count, start + self.gene_chunk_size)

            def reductions(
                anchor: torch.Tensor,
                *,
                chunk_start: int = start,
                chunk_stop: int = stop,
            ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
                del anchor
                row_values = values[:, chunk_start:chunk_stop]
                row_log, row_composition = self._log_view(
                    row_values,
                    state.support_depths[:, None],
                )
                row_detection = (row_values > 0).float()
                global_mean = state.global_log_mean[chunk_start:chunk_stop]
                global_std = state.global_log_std[chunk_start:chunk_stop]
                global_detection = state.global_detection[chunk_start:chunk_stop]
                row_pearson = (
                    (row_log - global_mean.unsqueeze(0))
                    / global_std.unsqueeze(0)
                ).clamp(-8.0, 8.0)
                class_mean = state.class_log_mean.index_select(0, local)[
                    :, chunk_start:chunk_stop
                ]
                class_std = state.class_log_std.index_select(0, local)[
                    :, chunk_start:chunk_stop
                ]
                class_detection = state.class_detection.index_select(0, local)[
                    :, chunk_start:chunk_stop
                ]
                features = torch.stack(
                    (
                        row_log / 10.0,
                        row_pearson / 4.0,
                        row_detection,
                        torch.sqrt(
                            row_composition * float(max(gene_count, 1)) + self.eps
                        ),
                        global_mean.unsqueeze(0).expand_as(row_log) / 10.0,
                        global_std.unsqueeze(0).expand_as(row_log) / 10.0,
                        global_detection.unsqueeze(0).expand_as(row_log),
                        class_mean / 10.0,
                        class_std / 10.0,
                        class_detection,
                    ),
                    dim=-1,
                )
                encoded = self.support_gene_mlp(features)
                with torch.autocast(device_type=encoded.device.type, enabled=False):
                    encoded32 = encoded.float()
                    return (
                        encoded32.sum(dim=1),
                        encoded32.square().sum(dim=1),
                        torch.amax(encoded32, dim=1),
                        torch.logsumexp(encoded32, dim=1),
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
                chunk_square
                if total_square is None
                else total_square + chunk_square
            )
            total_max = (
                chunk_max if total_max is None else torch.maximum(total_max, chunk_max)
            )
            total_lse = (
                chunk_lse
                if total_lse is None
                else torch.logaddexp(total_lse, chunk_lse)
            )
        if any(value is None for value in (total_sum, total_square, total_max, total_lse)):
            raise RuntimeError("support-row encoder received no genes")
        pooled = torch.cat(
            (
                total_sum / float(gene_count),
                torch.sqrt(total_square / float(gene_count) + self.eps),
                total_max,
                total_lse - math.log(float(gene_count)),
            ),
            dim=-1,
        )
        embedded = self.support_row_projection(pooled)
        for block in self.support_router_blocks:
            embedded = block(embedded)
        return embedded

    def _learned_summary_weights(
        self,
        state: AlignedPrototypeSupportState,
        row_embeddings: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        indices = state.class_member_indices
        member_mask = state.class_member_mask
        packed = row_embeddings.index_select(0, indices.reshape(-1)).reshape(
            int(indices.size(0)),
            int(indices.size(1)),
            self.model_dim,
        )
        mask_float = member_mask.to(dtype=packed.dtype).unsqueeze(-1)
        class_mean = (packed * mask_float).sum(dim=1) / mask_float.sum(
            dim=1
        ).clamp_min(1.0)
        queries = class_mean[:, None, :] + self.class_summary_queries.unsqueeze(0)
        query = self.summary_query_projection(queries)
        key = self.summary_key_projection(packed)
        logits = torch.einsum("ckd,cmd->ckm", query, key) / math.sqrt(
            float(self.model_dim)
        )
        weights = self._masked_softmax(
            logits,
            member_mask[:, None, :].expand(-1, MAX_CLASS_SUMMARIES, -1),
        )
        slot_indices = torch.arange(MAX_CLASS_SUMMARIES, device=weights.device)
        active_counts = torch.minimum(
            state.class_support_counts.to(dtype=torch.long),
            torch.full_like(
                state.class_support_counts.to(dtype=torch.long),
                self.num_active_class_summaries,
            ),
        )
        active = slot_indices.unsqueeze(0) < active_counts.unsqueeze(1)
        weights = weights * active.unsqueeze(-1).to(dtype=weights.dtype)
        return weights, active

    def fit_support(
        self,
        support_x: torch.Tensor,
        support_y: torch.Tensor,
        class_ids: torch.Tensor | None = None,
        *,
        count_eligible: bool = True,
    ) -> AlignedClassInducingSupportState:
        base = super().fit_support(
            support_x,
            support_y,
            class_ids,
            count_eligible=count_eligible,
        )
        row_embeddings = self._support_row_embeddings(base)
        weights, active = self._learned_summary_weights(base, row_embeddings)
        return AlignedClassInducingSupportState(
            base=base,
            support_row_embeddings=row_embeddings,
            learned_summary_weights=weights,
            learned_summary_active=active,
        )

    def _deterministic_summary_weights(
        self,
        state: AlignedPrototypeSupportState,
        summary_count: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if int(summary_count) not in {1, 2, 4, 8}:
            raise ValueError("deterministic summary count must be 1, 2, 4, or 8")
        class_count, maximum = state.class_member_indices.shape
        weights = state.support_x.new_zeros(
            (class_count, MAX_CLASS_SUMMARIES, maximum),
            dtype=torch.float32,
        )
        active = torch.zeros(
            (class_count, MAX_CLASS_SUMMARIES),
            device=state.support_x.device,
            dtype=torch.bool,
        )
        log_depth = torch.log1p(state.support_depths) / 12.0
        key = log_depth + math.sqrt(2.0) * state.support_detection
        for class_index in range(class_count):
            count = int(state.class_support_counts[class_index].item())
            members = state.class_member_indices[class_index, :count]
            order = torch.argsort(key.index_select(0, members), stable=True)
            slots = min(int(summary_count), count)
            active[class_index, :slots] = True
            for rank in range(count):
                slot = rank % slots
                weights[class_index, slot, int(order[rank].item())] = 1.0
            normalizer = weights[class_index, :slots].sum(
                dim=-1,
                keepdim=True,
            )
            weights[class_index, :slots] /= normalizer.clamp_min(1.0)
        return weights, active

    def _select_summary_weights(
        self,
        state: AlignedClassInducingSupportState,
        mode: SupportSummaryMode,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if mode == "learned":
            return state.learned_summary_weights, state.learned_summary_active
        counts = {
            "uniform_one": 1,
            "deterministic_two": 2,
            "deterministic_four": 4,
            "deterministic_eight": 8,
        }
        if mode not in counts:
            raise ValueError("unknown support summary mode")
        return self._deterministic_summary_weights(state.base, counts[mode])

    def score_inductive(
        self,
        state: AlignedClassInducingSupportState,
        query_x: torch.Tensor,
        *,
        return_debug: bool = False,
        operator_mode_override: AlignedOperatorMode | None = None,
        fixed_base_logits: torch.Tensor | None = None,
        count_eligible: bool = True,
        summary_mode_override: SupportSummaryMode = "learned",
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        base_state = state.base
        if query_x.ndim != 2 or int(query_x.size(0)) < 1:
            raise ValueError("query_x must have shape [nonempty rows, genes]")
        if int(query_x.size(1)) != int(base_state.support_x.size(1)):
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
                if not count_eligible or base_state.eb_log_probabilities is None:
                    raise ValueError(
                        "noncount scoring requires explicit fixed_base_logits"
                    )
                fixed_base, internal_raw_eb = self._score_fixed_eb(
                    query,
                    base_state.eb_log_probabilities,
                )
            else:
                fixed_base = fixed_base_logits.to(
                    device=query.device,
                    dtype=torch.float32,
                )
                expected = (
                    int(query.size(0)),
                    int(base_state.class_ids.numel()),
                )
                if tuple(fixed_base.shape) != expected or not torch.isfinite(
                    fixed_base
                ).all():
                    raise ValueError("fixed_base_logits is malformed")
            with torch.no_grad():
                raw_similarity, pearson_similarity = self._query_support_similarities(
                    base_state,
                    query,
                )
                _, fixed_retrieval = self._prototype_weights(
                    base_state,
                    raw_similarity,
                    pearson_similarity,
                    operator_mode=operator_mode,
                )
                member_mask = base_state.class_member_mask.unsqueeze(0).expand(
                    int(query.size(0)), -1, -1
                )
                uniform = member_mask.to(dtype=query.dtype)
                uniform = uniform / uniform.sum(dim=-1, keepdim=True).clamp_min(1.0)
                fixed_raw = _row_zscore(
                    (raw_similarity[:, base_state.class_member_indices] * uniform).sum(
                        dim=-1
                    ),
                    self.eps,
                )
                fixed_pearson = _row_zscore(
                    (
                        pearson_similarity[:, base_state.class_member_indices]
                        * uniform
                    ).sum(dim=-1),
                    self.eps,
                )

        summary_weights, summary_active = self._select_summary_weights(
            state,
            summary_mode_override,
        )
        query_count = int(query.size(0))
        class_count = int(base_state.class_ids.numel())
        pair_count = query_count * class_count
        summary_count = int(summary_weights.size(1))
        flattened_weights = summary_weights.unsqueeze(0).expand(
            query_count, -1, -1, -1
        ).reshape(pair_count, summary_count, int(summary_weights.size(-1)))
        flattened_active = summary_active.unsqueeze(0).expand(
            query_count, -1, -1
        ).reshape(pair_count, summary_count)
        query_depths = query.sum(dim=1).clamp_min(1.0)
        query_detection = (query > 0).float().mean(dim=1)
        base_probabilities = torch.softmax(fixed_base.float(), dim=1)
        learned_chunks: list[torch.Tensor] = []
        gate_chunks: list[torch.Tensor] = []
        token_chunks: list[torch.Tensor] = []
        program_chunks: list[torch.Tensor] = []
        reduced_chunks: list[torch.Tensor] = []
        flattened_retrieval = fixed_retrieval.reshape(pair_count, 1)

        for start in range(0, pair_count, self.pair_chunk_size):
            stop = min(pair_count, start + self.pair_chunk_size)
            pair_indices = torch.arange(start, stop, device=query.device)
            query_indices = torch.div(
                pair_indices, class_count, rounding_mode="floor"
            )
            class_indices = torch.remainder(pair_indices, class_count)
            reduced = self._reduce_pair_relations(
                base_state,
                query,
                query_depths,
                query_detection,
                pair_indices,
                flattened_weights[start:stop],
                operator_mode=operator_mode,
            )
            summary_tokens = self.reduction_projection(reduced)
            summary_tokens = summary_tokens + self.class_summary_roles.unsqueeze(0)
            program_seed = self.program_queries.unsqueeze(0).expand(
                stop - start, -1, -1
            )
            attended, _ = self.prototype_cross_attention(
                program_seed,
                summary_tokens,
                summary_tokens,
                key_padding_mask=~flattened_active[start:stop],
                need_weights=False,
            )
            programs = self.prototype_cross_norm(program_seed + attended)
            programs = self.program_transformer(programs)
            pooled = torch.cat(
                (programs.mean(dim=1), torch.amax(programs, dim=1)),
                dim=-1,
            )
            head = torch.cat(
                (pooled.float(), flattened_retrieval[start:stop]),
                dim=-1,
            )
            raw_learned = self.residual_scorer(head).squeeze(-1)
            support_scale = (
                torch.log1p(
                    base_state.class_support_counts.index_select(0, class_indices)
                )
                / math.log(101.0)
            )
            gate_features = torch.stack(
                (
                    fixed_base.reshape(-1).index_select(0, pair_indices),
                    base_probabilities.reshape(-1).index_select(0, pair_indices),
                    flattened_retrieval[start:stop, 0],
                    support_scale,
                    torch.log1p(query_depths.index_select(0, query_indices)) / 12.0,
                    query_detection.index_select(0, query_indices),
                ),
                dim=-1,
            )
            gate = torch.sigmoid(self.base_confidence_gate(gate_features).squeeze(-1))
            learned_chunks.append(raw_learned * (2.0 * gate))
            gate_chunks.append(gate)
            token_chunks.append(summary_tokens)
            program_chunks.append(programs)
            reduced_chunks.append(reduced)

        unbounded = torch.cat(learned_chunks).reshape(query_count, class_count)
        centered = unbounded - unbounded.mean(dim=1, keepdim=True)
        learned = self.residual_bound * torch.tanh(centered / self.residual_bound)
        logits = fixed_base + learned
        summary_tokens = torch.cat(token_chunks).reshape(
            query_count,
            class_count,
            summary_count,
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
            summary_count,
            4 * self.relation_dim,
        )
        relation_diagnostics = self._representation_diagnostics(reduced.detach())
        active_weight = summary_weights * summary_active.unsqueeze(-1)
        active_count = summary_active.sum().clamp_min(1)
        entropy = -(
            active_weight
            * active_weight.clamp_min(self.eps).log()
        ).sum() / active_count
        centered_slots = reduced.float() - reduced.float().mean(dim=2, keepdim=True)
        debug: dict[str, torch.Tensor] = {
            "fixed_base_logits": fixed_base,
            "raw_logits": fixed_base,
            "raw_control_logits": fixed_base,
            "learned_logits": learned,
            "standalone_neural_logits": learned,
            "learned_logits_unbounded": unbounded,
            "learned_logits_centered": centered,
            "fixed_retrieval_logits": fixed_retrieval,
            "fixed_raw_prototype_logits": fixed_raw,
            "fixed_pearson_prototype_logits": fixed_pearson,
            "fixed_raw_pearson_logits": 0.5 * (fixed_raw + fixed_pearson),
            "prototype_weights": summary_weights.unsqueeze(0).expand(
                query_count, -1, -1, -1
            ),
            "summary_weights": summary_weights,
            "summary_active_mask": summary_active,
            "support_row_embeddings": state.support_row_embeddings,
            "prototype_tokens": summary_tokens,
            "query_programs": programs,
            "query_context": programs.mean(dim=(1, 2)),
            "class_context": self.class_summary_roles.mean(dim=0, keepdim=True).expand(
                class_count, -1
            ),
            "prototype_weight_entropy": entropy,
            "prototype_effective_support": (
                active_weight.square().sum(dim=-1).clamp_min(self.eps).reciprocal()
                * summary_active
            ).sum() / active_count,
            "barycenter_relation_diversity": centered_slots.square().mean().sqrt(),
            "summary_gate_mean": torch.cat(gate_chunks).mean(),
            "derangement_aligned_gene_fraction": (
                base_state.derangement_aligned_gene_fraction
            ),
            "operator_mode": torch.tensor(
                {"aligned": 0, "gene_deranged": 1, "uniform_only": 2}[
                    operator_mode
                ],
                device=query.device,
            ),
            "relation_order": torch.tensor(0, device=query.device),
            "maximum_relation_block_elements": torch.tensor(
                self.pair_chunk_size
                * summary_count
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


__all__ = [
    "AlignedClassInducingPFN",
    "AlignedClassInducingSupportState",
    "MAX_CLASS_SUMMARIES",
    "SupportSummaryMode",
]
