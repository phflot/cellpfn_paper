"""Direct aligned class-inducing CellPFN classifier.

This model retains the K-summary support router, same-gene relation network,
program cross-attention, and Transformer used by :class:`AlignedClassInducingPFN`.
Unlike that residual model, its output is produced only by a learned direct
classification head.  No empirical-Bayes score, retrieval logit, analytic
probability, confidence gate, residual bound, or fixed-logit addition appears
on the output path.

Two observation modes share the complete latent backbone.  Count inputs use
the incumbent count-aware feature surfaces.  Processed inputs are expected to
already contain log1p-CP10K expression and use feature stems that never apply a
second library-size normalization or logarithm.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from dataclasses import fields as dataclass_fields
from typing import Literal

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.checkpoint import checkpoint

from hashprompt.episodes import DenseEpisodeBatch
from hashprompt.models.aligned_class_inducing_pfn import (
    MAX_CLASS_SUMMARIES,
    AlignedClassInducingPFN,
    SupportSummaryMode,
)
from hashprompt.models.aligned_prototype_pfn import (
    AlignedOperatorMode,
    AlignedPrototypeResidualPFN,
    AlignedPrototypeSupportState,
)
from hashprompt.models.embedding import PromptForwardOutput
from hashprompt.models.gene_gene_operator import (
    GENE_GENE_OPERATOR_SPECS,
    GeneGeneOperator,
    LCSQueryContext,
    PooledWhitenV2Context,
    build_lcs_extra_stem,
    build_lcs_pair_head,
    fit_lcs_support,
    fit_pooled_whiten_v2_support,
    lcs_gene_channels,
    lcs_query_context,
    pooled_whiten_v2_gene_channels,
    pooled_whiten_v2_query_context,
    validate_gene_gene_operator,
)
from hashprompt.models.program_pfn import _balanced_accuracy

ObservationMode = Literal["count", "processed"]
COUNT_SUPPORT_INPUT_DIM = 10
PROCESSED_SUPPORT_INPUT_DIM = 9
PROCESSED_RELATION_INPUT_DIM = 22


@dataclass(frozen=True)
class _DirectBaseSupportState(AlignedPrototypeSupportState):
    observation_mode: ObservationMode


@dataclass(frozen=True)
class AlignedClassInducingDirectSupportState:
    """Support cache bound to the observation stem used to construct it."""

    base: _DirectBaseSupportState
    support_row_embeddings: torch.Tensor
    learned_summary_weights: torch.Tensor
    learned_summary_active: torch.Tensor

    @property
    def class_ids(self) -> torch.Tensor:
        return self.base.class_ids

    @property
    def observation_mode(self) -> ObservationMode:
        return self.base.observation_mode


class _ObservationStemEncoder(nn.Module):
    """Two input projections followed by one shared nonlinear encoder."""

    def __init__(
        self,
        count_stem: nn.Linear,
        processed_input_dim: int,
        shared: nn.Sequential,
    ) -> None:
        super().__init__()
        self.count_stem = count_stem
        self.processed_stem = nn.Linear(
            int(processed_input_dim),
            int(count_stem.out_features),
        )
        self.shared = shared
        # Optional zero-initialized gene-gene stem (``pooled_whiten_v1``/``lcs_v1``/
        # ``pooled_whiten_v2``).  It is only
        # registered as a module when enabled, so flag-off state_dict keys are
        # unchanged.  Per-chunk channels are handed over by the enclosing
        # (checkpointed) relation closure through ``pending_extra``.
        self.extra_stem = None
        self.pending_extra: torch.Tensor | None = None

    def forward(
        self,
        features: torch.Tensor,
        *,
        observation_mode: ObservationMode = "count",
    ) -> torch.Tensor:
        mode = _validate_observation_mode(observation_mode)
        expected = (
            int(self.count_stem.in_features)
            if mode == "count"
            else int(self.processed_stem.in_features)
        )
        if int(features.size(-1)) != expected:
            raise RuntimeError(
                f"{mode} feature stem expected {expected} channels; "
                f"received {int(features.size(-1))}"
            )
        stem = self.count_stem if mode == "count" else self.processed_stem
        hidden = stem(features)
        extra = self.pending_extra
        if extra is not None:
            if self.extra_stem is None:
                raise RuntimeError("gene-gene channels supplied without an extra stem")
            # extra: [pairs, genes, channels] broadcast over the summary axis.
            hidden = hidden + self.extra_stem(extra).unsqueeze(1).to(hidden.dtype)
        return self.shared(hidden)


def _validate_observation_mode(value: object) -> ObservationMode:
    if value not in {"count", "processed"}:
        raise ValueError("observation_mode must be 'count' or 'processed'")
    return value  # type: ignore[return-value]


class AlignedClassInducingDirectPFN(AlignedClassInducingPFN):
    """Matched-capacity CellPFN with direct, unbounded classification logits."""

    def __init__(
        self,
        *,
        num_active_class_summaries: int = 4,
        support_router_layers: int = 3,
        gene_gene_operator: GeneGeneOperator = "none",
        **kwargs: object,
    ) -> None:
        gene_gene_operator = validate_gene_gene_operator(gene_gene_operator)
        if bool(kwargs.get("counterfactual_deranged_anchor", False)):
            raise ValueError("direct CellPFN does not support auxiliary anchor losses")
        # These residual-only knobs must not change the direct model.  Supplying
        # them is tolerated so shared experiment configuration remains loadable.
        kwargs.pop("residual_bound", None)
        kwargs.pop("eb_equivalent_cells", None)
        kwargs.pop("eb_dispersion", None)
        kwargs.pop("counterfactual_deranged_anchor", None)
        super().__init__(
            num_active_class_summaries=num_active_class_summaries,
            support_router_layers=support_router_layers,
            counterfactual_deranged_anchor=False,
            **kwargs,
        )

        old_support_encoder = self.support_gene_mlp
        del self.support_gene_mlp
        self.support_gene_mlp = _ObservationStemEncoder(
            old_support_encoder[0],
            PROCESSED_SUPPORT_INPUT_DIM,
            nn.Sequential(*list(old_support_encoder.children())[1:]),
        )

        old_relation_encoder = self.relation_mlp
        del self.relation_mlp
        self.relation_mlp = _ObservationStemEncoder(
            old_relation_encoder[0],
            PROCESSED_RELATION_INPUT_DIM,
            nn.Sequential(*list(old_relation_encoder.children())[1:]),
        )

        # Remove every learned component of the residual/analytic fusion path.
        del self.residual_scorer
        del self.base_confidence_gate
        self.observation_mode_tokens = nn.Parameter(
            torch.randn(2, self.model_dim) / math.sqrt(float(self.model_dim))
        )
        self.direct_scorer = nn.Sequential(
            nn.Linear(2 * self.model_dim, self.model_dim),
            nn.GELU(),
            nn.Linear(self.model_dim, 1),
        )
        # Registered last so every pre-existing parameter keeps its seeded
        # initialization; both learned LCS outputs start at exactly zero.
        self.gene_gene_operator: GeneGeneOperator = gene_gene_operator
        if gene_gene_operator != "none":
            spec = GENE_GENE_OPERATOR_SPECS[gene_gene_operator]
            self.relation_mlp.extra_stem = build_lcs_extra_stem(
                int(self.relation_mlp.count_stem.out_features),
                len(spec.gene_channels),
            )
            self.lcs_pair_head = build_lcs_pair_head(
                self.model_dim, len(spec.pair_scalars)
            )

    def gene_gene_parameter_names(self) -> tuple[str, ...]:
        """Names of parameters added by the gene-gene operator (empty if off)."""

        if self.gene_gene_operator == "none":
            return ()
        return tuple(
            name
            for name, _ in self.named_parameters()
            if name.startswith(("relation_mlp.extra_stem.", "lcs_pair_head."))
        )

    def load_pre_extension_state_dict(
        self,
        state_dict: dict[str, torch.Tensor],
    ) -> tuple[str, ...]:
        """Load a flag-off state; only gene-gene parameters may stay at init."""

        missing, unexpected = self.load_state_dict(state_dict, strict=False)
        expected = set(self.gene_gene_parameter_names())
        if unexpected or set(missing) != expected:
            raise RuntimeError(
                "pre-extension state must match every non-gene-gene parameter: "
                f"missing={sorted(missing)} unexpected={sorted(unexpected)}"
            )
        return tuple(sorted(missing))

    def _lcs_pearson(
        self,
        values: torch.Tensor,
        depths: torch.Tensor | None,
        mean: torch.Tensor,
        std: torch.Tensor,
        observation_mode: ObservationMode,
    ) -> torch.Tensor:
        with torch.autocast(device_type=values.device.type, enabled=False):
            if observation_mode == "count":
                if depths is None:
                    raise RuntimeError("count LCS view requires depths")
                expression, _ = self._log_view(values.float(), depths.unsqueeze(1))
            else:
                expression = values.float()
            return (
                (expression - mean.unsqueeze(0)) / std.unsqueeze(0)
            ).clamp(-8.0, 8.0)

    def _lcs_context(
        self,
        base_state: _DirectBaseSupportState,
        query: torch.Tensor,
        query_depths: torch.Tensor,
        *,
        observation_mode: ObservationMode,
        operator_mode: AlignedOperatorMode,
    ) -> LCSQueryContext | PooledWhitenV2Context:
        """Fixed (parameter-free, gradient-free) LCS statistics of one episode."""

        if operator_mode == "gene_deranged":
            support_values = base_state.deranged_support_x
            mean = base_state.deranged_global_log_mean
            std = base_state.deranged_global_log_std
        else:
            support_values = base_state.support_x
            mean = base_state.global_log_mean
            std = base_state.global_log_std
        with torch.no_grad():
            support_pearson = self._lcs_pearson(
                support_values,
                base_state.support_depths if observation_mode == "count" else None,
                mean,
                std,
                observation_mode,
            )
            query_pearson = self._lcs_pearson(
                query,
                query_depths if observation_mode == "count" else None,
                mean,
                std,
                observation_mode,
            )
            if self.gene_gene_operator == "pooled_whiten_v2":
                return pooled_whiten_v2_query_context(
                    fit_pooled_whiten_v2_support(
                        support_pearson,
                        base_state.support_y_local,
                        int(base_state.class_ids.numel()),
                    ),
                    query_pearson,
                )
            fit = fit_lcs_support(
                support_pearson,
                base_state.support_y_local,
                int(base_state.class_ids.numel()),
                max_class_rank=GENE_GENE_OPERATOR_SPECS[
                    self.gene_gene_operator
                ].max_class_rank,
            )
            return lcs_query_context(fit, query_pearson)

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
        lcs: LCSQueryContext | PooledWhitenV2Context | None = None,
    ) -> torch.Tensor:
        if lcs is None:
            return super()._reduce_pair_relations(
                state,
                query_x,
                query_depths,
                query_row_detection,
                pair_indices,
                prototype_weights,
                operator_mode=operator_mode,
            )
        gene_count = int(query_x.size(1))
        total_sum = None
        total_square = None
        total_max = None
        total_lse = None
        relation_mlp = self.relation_mlp
        # Fixed channels for the whole pair chunk ([pairs, genes, 4], a few MB);
        # per-gene values do not depend on gene-chunk borders.
        selected = GENE_GENE_OPERATOR_SPECS[self.gene_gene_operator].gene_channels
        if isinstance(lcs, PooledWhitenV2Context):
            channels = pooled_whiten_v2_gene_channels(
                lcs, pair_indices, start=0, stop=gene_count
            )
        else:
            channels = lcs_gene_channels(lcs, pair_indices, start=0, stop=gene_count)
        channels = channels[..., list(selected)]
        for start in range(0, gene_count, self.gene_chunk_size):
            stop = min(gene_count, start + self.gene_chunk_size)

            def reductions(
                anchor: torch.Tensor,
                *,
                chunk_start: int = start,
                chunk_stop: int = stop,
            ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
                del anchor
                # Recomputed identically under activation checkpointing: the
                # channels are a deterministic function of the fixed context.
                relation_mlp.pending_extra = channels[:, chunk_start:chunk_stop]
                try:
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
                finally:
                    relation_mlp.pending_extra = None

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
    def _tag_base_state(
        state: AlignedPrototypeSupportState,
        observation_mode: ObservationMode,
    ) -> _DirectBaseSupportState:
        payload = {
            field.name: getattr(state, field.name)
            for field in dataclass_fields(AlignedPrototypeSupportState)
        }
        return _DirectBaseSupportState(
            **payload,
            observation_mode=observation_mode,
        )

    def _fit_processed_base(
        self,
        support_x: torch.Tensor,
        support_y: torch.Tensor,
        class_ids: torch.Tensor | None,
    ) -> _DirectBaseSupportState:
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
            # `values` is already log1p-CP10K.  It is intentionally never sent
            # through `_log_view`, `expm1`, or another depth normalization.
            values = support_x.float()
            labels = support_y.to(device=values.device, dtype=torch.long)
            classes = (
                torch.unique(labels, sorted=True)
                if class_ids is None
                else class_ids.to(device=values.device, dtype=torch.long)
            )
            if int(classes.numel()) < 2:
                raise ValueError("direct CellPFN requires at least two classes")
            local = self._localize_labels(labels, classes)
            class_counts = torch.bincount(local, minlength=int(classes.numel()))
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

            detection = (values > 0).float()
            global_mean = values.mean(dim=0)
            global_std = values.std(dim=0, unbiased=False).clamp_min(self.eps)
            global_detection = detection.mean(dim=0)
            standardized = (
                (values - global_mean.unsqueeze(0)) / global_std.unsqueeze(0)
            ).clamp(-8.0, 8.0)
            class_mean: list[torch.Tensor] = []
            class_std: list[torch.Tensor] = []
            class_detection: list[torch.Tensor] = []
            for class_index in range(int(classes.numel())):
                mask = local == class_index
                class_values = values[mask]
                class_mean.append(class_values.mean(dim=0))
                class_std.append(class_values.std(dim=0, unbiased=False))
                class_detection.append(detection[mask].mean(dim=0))

            relative_derangement, derangement_groups, group_counts = (
                self._relative_derangement(
                    global_mean,
                    global_std,
                    global_detection,
                )
            )
            deranged_values = values.index_select(1, relative_derangement).clone()
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
            deranged_detection = (deranged_values > 0).float()
            deranged_global_mean = deranged_values.mean(dim=0)
            deranged_global_std = deranged_values.std(
                dim=0,
                unbiased=False,
            ).clamp_min(self.eps)
            deranged_global_detection = deranged_detection.mean(dim=0)
            deranged_class_mean: list[torch.Tensor] = []
            deranged_class_std: list[torch.Tensor] = []
            deranged_class_detection: list[torch.Tensor] = []
            for class_index in range(int(classes.numel())):
                mask = local == class_index
                class_values = deranged_values[mask]
                deranged_class_mean.append(class_values.mean(dim=0))
                deranged_class_std.append(class_values.std(dim=0, unbiased=False))
                deranged_class_detection.append(deranged_detection[mask].mean(dim=0))

            # `support_depths` is a structural sentinel required by the shared
            # support-state container.  The processed stems never consume it.
            unused_depth_sentinel = values.new_zeros(int(values.size(0)))
            return _DirectBaseSupportState(
                class_ids=classes,
                support_y_local=local,
                support_x=values,
                class_member_indices=member_indices,
                class_member_mask=member_mask,
                class_support_counts=class_counts.to(dtype=torch.float32),
                support_depths=unused_depth_sentinel,
                support_detection=detection.mean(dim=1),
                global_log_mean=global_mean,
                global_log_std=global_std,
                global_detection=global_detection,
                class_log_mean=torch.stack(class_mean),
                class_log_std=torch.stack(class_std),
                class_detection=torch.stack(class_detection),
                deranged_support_x=deranged_values,
                deranged_global_log_mean=deranged_global_mean,
                deranged_global_log_std=deranged_global_std,
                deranged_global_detection=deranged_global_detection,
                deranged_class_log_mean=torch.stack(deranged_class_mean),
                deranged_class_log_std=torch.stack(deranged_class_std),
                deranged_class_detection=torch.stack(deranged_class_detection),
                eb_log_probabilities=None,
                support_raw_norms=values.square().sum(dim=1).sqrt().clamp_min(self.eps),
                support_pearson_norms=standardized.square()
                .sum(dim=1)
                .sqrt()
                .clamp_min(self.eps),
                relative_derangement=relative_derangement,
                derangement_aligned_gene_fraction=(derangement_aligned_gene_fraction),
                observation_mode="processed",
            )

    def _support_row_embeddings(
        self,
        state: _DirectBaseSupportState,
    ) -> torch.Tensor:
        values = state.support_x
        gene_count = int(values.size(1))
        local = state.support_y_local
        mode = state.observation_mode
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
                if mode == "count":
                    row_expression, row_composition = self._log_view(
                        row_values,
                        state.support_depths[:, None],
                    )
                else:
                    row_expression = row_values
                    row_composition = None
                row_detection = (row_values > 0).float()
                global_mean = state.global_log_mean[chunk_start:chunk_stop]
                global_std = state.global_log_std[chunk_start:chunk_stop]
                global_detection = state.global_detection[chunk_start:chunk_stop]
                row_pearson = (
                    (row_expression - global_mean.unsqueeze(0))
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
                common = (
                    row_expression / 10.0,
                    row_pearson / 4.0,
                    row_detection,
                )
                if mode == "count":
                    if row_composition is None:
                        raise RuntimeError("count support composition is missing")
                    features = torch.stack(
                        (
                            *common,
                            torch.sqrt(
                                row_composition * float(max(gene_count, 1)) + self.eps
                            ),
                            global_mean.unsqueeze(0).expand_as(row_expression) / 10.0,
                            global_std.unsqueeze(0).expand_as(row_expression) / 10.0,
                            global_detection.unsqueeze(0).expand_as(row_expression),
                            class_mean / 10.0,
                            class_std / 10.0,
                            class_detection,
                        ),
                        dim=-1,
                    )
                else:
                    features = torch.stack(
                        (
                            *common,
                            global_mean.unsqueeze(0).expand_as(row_expression) / 10.0,
                            global_std.unsqueeze(0).expand_as(row_expression) / 10.0,
                            global_detection.unsqueeze(0).expand_as(row_expression),
                            class_mean / 10.0,
                            class_std / 10.0,
                            class_detection,
                        ),
                        dim=-1,
                    )
                encoded = self.support_gene_mlp(
                    features,
                    observation_mode=mode,
                )
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
        if any(
            value is None for value in (total_sum, total_square, total_max, total_lse)
        ):
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

    def fit_support(
        self,
        support_x: torch.Tensor,
        support_y: torch.Tensor,
        class_ids: torch.Tensor | None = None,
        *,
        observation_mode: ObservationMode,
    ) -> AlignedClassInducingDirectSupportState:
        mode = _validate_observation_mode(observation_mode)
        if mode == "count":
            base = AlignedPrototypeResidualPFN.fit_support(
                self,
                support_x,
                support_y,
                class_ids,
                count_eligible=False,
            )
            tagged_base = self._tag_base_state(base, mode)
        else:
            tagged_base = self._fit_processed_base(
                support_x,
                support_y,
                class_ids,
            )
        row_embeddings = self._support_row_embeddings(tagged_base)
        weights, active = self._learned_summary_weights(
            tagged_base,
            row_embeddings,
        )
        return AlignedClassInducingDirectSupportState(
            base=tagged_base,
            support_row_embeddings=row_embeddings,
            learned_summary_weights=weights,
            learned_summary_active=active,
        )

    def _deterministic_summary_weights(
        self,
        state: AlignedPrototypeSupportState,
        summary_count: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        mode = getattr(state, "observation_mode", "count")
        if mode == "count":
            return super()._deterministic_summary_weights(state, summary_count)
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
        key = state.support_x.mean(dim=1) / 10.0 + (
            math.sqrt(2.0) * state.support_detection
        )
        for class_index in range(class_count):
            count = int(state.class_support_counts[class_index].item())
            members = state.class_member_indices[class_index, :count]
            order = torch.argsort(key.index_select(0, members), stable=True)
            slots = min(int(summary_count), count)
            active[class_index, :slots] = True
            for rank in range(count):
                slot = rank % slots
                weights[class_index, slot, int(order[rank].item())] = 1.0
            normalizer = weights[class_index, :slots].sum(dim=-1, keepdim=True)
            weights[class_index, :slots] /= normalizer.clamp_min(1.0)
        return weights, active

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
        mode = getattr(state, "observation_mode", None)
        if mode == "count":
            return AlignedPrototypeResidualPFN._relation_chunk_reductions(
                self,
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
        if mode != "processed":
            raise TypeError("direct relation state is missing its observation mode")
        return self._processed_relation_chunk_reductions(
            state,
            query_x,
            query_row_detection,
            pair_indices,
            prototype_weights,
            start=start,
            stop=stop,
            operator_mode=operator_mode,
        )

    def _processed_relation_chunk_reductions(
        self,
        state: AlignedPrototypeSupportState,
        query_x: torch.Tensor,
        query_row_detection: torch.Tensor,
        pair_indices: torch.Tensor,
        prototype_weights: torch.Tensor,
        *,
        start: int,
        stop: int,
        operator_mode: AlignedOperatorMode,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        class_count = int(state.class_ids.numel())
        query_indices = torch.div(pair_indices, class_count, rounding_mode="floor")
        class_indices = torch.remainder(pair_indices, class_count)
        gene_indices = torch.arange(start, stop, device=query_x.device)
        if operator_mode == "gene_deranged":
            support_source = state.deranged_support_x
            global_mean = state.deranged_global_log_mean
            global_std = state.deranged_global_log_std
            global_detection = state.deranged_global_detection
            class_mean = state.deranged_class_log_mean
            class_std = state.deranged_class_log_std
            class_detection = state.deranged_class_detection
        else:
            support_source = state.support_x
            global_mean = state.global_log_mean
            global_std = state.global_log_std
            global_detection = state.global_detection
            class_mean = state.class_log_mean
            class_std = state.class_log_std
            class_detection = state.class_detection

        members = state.class_member_indices.index_select(0, class_indices)
        pair_count, maximum_members = members.shape
        summary_count = int(prototype_weights.size(1))
        member_values = support_source.index_select(
            0,
            members.reshape(-1),
        )[:, gene_indices].reshape(
            pair_count,
            maximum_members,
            stop - start,
        )
        support_detection = (member_values > 0).float()
        support_pearson = (
            (member_values - global_mean[gene_indices].view(1, 1, -1))
            / global_std[gene_indices].view(1, 1, -1)
        ).clamp(-8.0, 8.0)
        support_views = torch.stack(
            (
                member_values / 10.0,
                support_pearson / 4.0,
                support_detection,
            ),
            dim=-1,
        )
        prototypes = torch.einsum(
            "pmb,pbgv->pmgv",
            prototype_weights,
            support_views,
        )

        query_values = query_x.index_select(0, query_indices)[:, gene_indices].float()
        query_detection = (query_values > 0).float()
        query_pearson = (
            (query_values - global_mean[gene_indices].unsqueeze(0))
            / global_std[gene_indices].unsqueeze(0)
        ).clamp(-8.0, 8.0)
        query_views = torch.stack(
            (
                query_values / 10.0,
                query_pearson / 4.0,
                query_detection,
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
                    global_mean[gene_indices] / 10.0,
                    global_std[gene_indices] / 10.0,
                    global_detection[gene_indices],
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
                class_mean.index_select(0, class_indices)[:, gene_indices] / 10.0,
                class_std.index_select(0, class_indices)[:, gene_indices] / 10.0,
                class_detection.index_select(0, class_indices)[:, gene_indices],
            ),
            dim=-1,
        )[:, None].expand(-1, summary_count, -1, -1)
        pair_query_detection = query_row_detection.index_select(0, query_indices)
        query_auxiliary = pair_query_detection[:, None, None, None].expand(
            -1,
            summary_count,
            stop - start,
            1,
        )
        member_detection = state.support_detection.index_select(
            0,
            members.reshape(-1),
        ).reshape(pair_count, maximum_members)
        prototype_detection = torch.einsum(
            "pmb,pb->pm",
            prototype_weights,
            member_detection,
        )
        prototype_auxiliary = prototype_detection[:, :, None, None].expand(
            -1,
            -1,
            stop - start,
            1,
        )
        support_scale = (
            torch.log1p(state.class_support_counts.index_select(0, class_indices))
            / math.log(101.0)
        )[:, None, None, None].expand(
            -1,
            summary_count,
            stop - start,
            1,
        )
        per_gene_alignment = 0.5 * (
            query_expanded[..., 0] * prototypes[..., 0]
            + query_expanded[..., 1] * prototypes[..., 1]
        )
        features = torch.cat(
            (
                relation_views,
                global_features,
                class_features,
                query_auxiliary,
                prototype_auxiliary,
                support_scale,
                per_gene_alignment.unsqueeze(-1),
            ),
            dim=-1,
        )
        if int(features.size(-1)) != PROCESSED_RELATION_INPUT_DIM:
            raise RuntimeError("processed relation feature surface changed")
        relation = self.relation_mlp(
            features,
            observation_mode="processed",
        )
        with torch.autocast(device_type=relation.device.type, enabled=False):
            values = relation.float()
            return (
                values.sum(dim=2),
                values.square().sum(dim=2),
                torch.amax(values, dim=2),
                torch.logsumexp(values, dim=2),
            )

    def score_inductive(
        self,
        state: AlignedClassInducingDirectSupportState,
        query_x: torch.Tensor,
        *,
        observation_mode: ObservationMode,
        return_debug: bool = False,
        summary_mode_override: SupportSummaryMode = "learned",
        operator_mode_override: AlignedOperatorMode | None = None,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        mode = _validate_observation_mode(observation_mode)
        if not isinstance(state, AlignedClassInducingDirectSupportState):
            raise TypeError("state must be an AlignedClassInducingDirectSupportState")
        if state.observation_mode != mode:
            raise ValueError(
                "observation mode mismatch: support was fitted as "
                f"{state.observation_mode!r}, query was supplied as {mode!r}"
            )
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
        summary_weights, summary_active = self._select_summary_weights(
            state,
            summary_mode_override,
        )
        query_count = int(query.size(0))
        class_count = int(base_state.class_ids.numel())
        pair_count = query_count * class_count
        summary_count = int(summary_weights.size(1))
        flattened_weights = (
            summary_weights.unsqueeze(0)
            .expand(
                query_count,
                -1,
                -1,
                -1,
            )
            .reshape(pair_count, summary_count, int(summary_weights.size(-1)))
        )
        flattened_active = (
            summary_active.unsqueeze(0)
            .expand(
                query_count,
                -1,
                -1,
            )
            .reshape(pair_count, summary_count)
        )
        query_depths = (
            query.sum(dim=1).clamp_min(1.0)
            if mode == "count"
            else query.new_zeros(query_count)
        )
        query_detection = (query > 0).float().mean(dim=1)
        lcs = (
            None
            if self.gene_gene_operator == "none"
            else self._lcs_context(
                base_state,
                query,
                query_depths,
                observation_mode=mode,
                operator_mode=operator_mode,
            )
        )
        lcs_head_chunks: list[torch.Tensor] = []
        direct_chunks: list[torch.Tensor] = []
        token_chunks: list[torch.Tensor] = []
        program_chunks: list[torch.Tensor] = []
        mode_token_chunks: list[torch.Tensor] = []
        reduced_chunks: list[torch.Tensor] = []
        mode_index = 0 if mode == "count" else 1

        for start in range(0, pair_count, self.pair_chunk_size):
            stop = min(pair_count, start + self.pair_chunk_size)
            pair_indices = torch.arange(start, stop, device=query.device)
            if lcs is None:
                reduced = self._reduce_pair_relations(
                    base_state,
                    query,
                    query_depths,
                    query_detection,
                    pair_indices,
                    flattened_weights[start:stop],
                    operator_mode=operator_mode,
                )
            else:
                reduced = self._reduce_pair_relations(
                    base_state,
                    query,
                    query_depths,
                    query_detection,
                    pair_indices,
                    flattened_weights[start:stop],
                    operator_mode=operator_mode,
                    lcs=lcs,
                )
            summary_tokens = self.reduction_projection(reduced)
            summary_tokens = summary_tokens + self.class_summary_roles.unsqueeze(0)
            program_seed = self.program_queries.unsqueeze(0).expand(
                stop - start,
                -1,
                -1,
            )
            attended, _ = self.prototype_cross_attention(
                program_seed,
                summary_tokens,
                summary_tokens,
                key_padding_mask=~flattened_active[start:stop],
                need_weights=False,
            )
            programs = self.prototype_cross_norm(program_seed + attended)
            mode_seed = self.observation_mode_tokens[mode_index].view(1, 1, -1)
            mode_seed = mode_seed.expand(stop - start, -1, -1)
            transformed = self.program_transformer(
                torch.cat((mode_seed, programs), dim=1)
            )
            transformed_mode = transformed[:, :1]
            transformed_programs = transformed[:, 1:]
            pooled = torch.cat(
                (
                    transformed_programs.mean(dim=1),
                    torch.amax(transformed_programs, dim=1),
                ),
                dim=-1,
            )
            with torch.autocast(device_type=query.device.type, enabled=False):
                if lcs is None:
                    direct_chunks.append(
                        self.direct_scorer(pooled.float()).squeeze(-1)
                    )
                else:
                    pair_gate = lcs.pair_gate[start:stop].unsqueeze(1)
                    scalar_columns = list(
                        GENE_GENE_OPERATOR_SPECS[self.gene_gene_operator].pair_scalars
                    )
                    lcs_head = pair_gate * self.lcs_pair_head(
                        lcs.pair_scalars[start:stop][:, scalar_columns]
                    )
                    lcs_head_chunks.append(lcs_head)
                    direct_chunks.append(
                        self.direct_scorer(pooled.float() + lcs_head).squeeze(-1)
                    )
            token_chunks.append(summary_tokens)
            program_chunks.append(transformed_programs)
            mode_token_chunks.append(transformed_mode)
            reduced_chunks.append(reduced)

        logits = torch.cat(direct_chunks).reshape(query_count, class_count)
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
        transformed_mode_tokens = torch.cat(mode_token_chunks).reshape(
            query_count,
            class_count,
            1,
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
        entropy = (
            -(active_weight * active_weight.clamp_min(self.eps).log()).sum()
            / active_count
        )
        centered_slots = reduced.float() - reduced.float().mean(dim=2, keepdim=True)
        debug: dict[str, torch.Tensor] = {
            "direct_logits": logits,
            "summary_weights": summary_weights,
            "summary_active_mask": summary_active,
            "support_row_embeddings": state.support_row_embeddings,
            "prototype_tokens": summary_tokens,
            "query_programs": programs,
            "transformed_observation_mode_tokens": transformed_mode_tokens,
            "query_context": programs.mean(dim=(1, 2)),
            "class_context": self.class_summary_roles.mean(
                dim=0,
                keepdim=True,
            ).expand(class_count, -1),
            "prototype_weight_entropy": entropy,
            "prototype_effective_support": (
                active_weight.square().sum(dim=-1).clamp_min(self.eps).reciprocal()
                * summary_active
            ).sum()
            / active_count,
            "barycenter_relation_diversity": centered_slots.square().mean().sqrt(),
            "derangement_aligned_gene_fraction": (
                base_state.derangement_aligned_gene_fraction
            ),
            "observation_mode_index": torch.tensor(
                mode_index,
                device=query.device,
                dtype=torch.long,
            ),
            "operator_mode": torch.tensor(
                {"aligned": 0, "gene_deranged": 1, "uniform_only": 2}[operator_mode],
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
        if lcs is not None:
            debug.update(
                {
                    "lcs_pair_scalars": lcs.pair_scalars.reshape(
                        query_count, class_count, -1
                    ),
                    "lcs_gate": lcs.fit.class_gate,
                    "lcs_class_rank": lcs.fit.class_rank,
                    "lcs_pooled_rank": lcs.fit.pooled_rank,
                    "lcs_head_abs_mean": torch.cat(lcs_head_chunks).abs().mean(),
                }
            )
        return logits, debug if return_debug else {}

    def forward_episode(
        self,
        episode: DenseEpisodeBatch,
        *,
        observation_mode: ObservationMode,
    ) -> PromptForwardOutput:
        if episode.query_y is None:
            raise ValueError("training episodes require query labels")
        mode = _validate_observation_mode(observation_mode)
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
        state = self.fit_support(
            support_x,
            support_y,
            class_ids,
            observation_mode=mode,
        )
        logits, debug = self.score_inductive(
            state,
            query_x,
            observation_mode=mode,
            return_debug=True,
        )
        with torch.autocast(device_type=device.type, enabled=False):
            loss = F.cross_entropy(logits.float(), query_y)
        predictions = logits.argmax(dim=1)
        histogram = torch.bincount(
            predictions,
            minlength=int(class_ids.numel()),
        ).float()
        return PromptForwardOutput(
            z_q=debug["query_context"],
            y_q=query_y,
            protos=debug["class_context"],
            classes=state.class_ids,
            logits=logits,
            proto_loss=loss,
            aux_losses={},
            aux_metrics={
                "train_query_balanced_accuracy": _balanced_accuracy(
                    query_y,
                    predictions,
                    int(class_ids.numel()),
                ),
                "train_query_max_pred_share": float(
                    (histogram.max() / histogram.sum().clamp_min(1.0)).item()
                ),
                "direct_logit_abs_mean": float(logits.abs().mean().detach()),
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
                "observation_mode_index": float(
                    debug["observation_mode_index"].detach()
                ),
                **(
                    {}
                    if self.gene_gene_operator == "none"
                    else {
                        "lcs_head_abs_mean": float(
                            debug["lcs_head_abs_mean"].detach()
                        ),
                        "lcs_gate_mean": float(debug["lcs_gate"].mean().detach()),
                        "lcs_pooled_rank": float(debug["lcs_pooled_rank"].detach()),
                    }
                ),
            },
            debug_tensors={
                "direct_logits": logits.detach(),
                "class_histogram": histogram.detach(),
                "observation_mode_index": debug["observation_mode_index"].detach(),
            },
        )

    def forward(
        self,
        episode: DenseEpisodeBatch,
        *,
        observation_mode: ObservationMode,
    ) -> PromptForwardOutput:
        return self.forward_episode(episode, observation_mode=observation_mode)


__all__ = [
    "COUNT_SUPPORT_INPUT_DIM",
    "PROCESSED_RELATION_INPUT_DIM",
    "PROCESSED_SUPPORT_INPUT_DIM",
    "AlignedClassInducingDirectPFN",
    "AlignedClassInducingDirectSupportState",
    "ObservationMode",
]
