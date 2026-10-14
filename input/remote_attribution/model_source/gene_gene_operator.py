"""Gene-gene interaction operator for the direct CellPFN ("LCS", ``lcs_v1``).

The direct CellPFN sees genes only through exchangeable per-gene statistics;
it has no second-moment path and therefore ties on tasks whose classes differ
only in gene-gene co-expression (for example the four-pattern XOR task).  The
low-rank support-fitted class-subspace (LCS) operator adds that path without
introducing any gene identity:

* every quantity is computed in the model's existing Pearson view
  ``clamp((log_view - global_log_mean) / global_log_std, -8, 8)``;
* per class ``c`` with ``n_c >= 2`` support rows, a dual PCA of the
  class-centred rows (``n_c x n_c`` Gram matrix, fp64 eigendecomposition)
  yields ``m_c = min(n_c - 1, 8)`` orthonormal gene loadings;
* a pooled within-class residual covariance
  ``Sigma = D + U Lambda U^T`` (rank <= 32, Woodbury inverse) whitens
  query-minus-class-mean differences.

Per (query, class) pair and per gene it emits four channels (class-subspace
residual, class-subspace reconstruction, pooled-whitened difference, class
loading energy of that gene) and per pair six scalars (residual energy,
subspace energy, subspace Mahalanobis, whitened Mahalanobis, rank fraction,
gate).  Every output is multiplied by a support-size gate that is exactly zero
for a class with a single support row, so B1 predictions never depend on the
operator.  All operations are inner products over the gene axis or
elementwise per gene, so the operator is gene-anonymous and equivariant under
gene, support-row, and class-label permutations.  It is a fixed, parameter-free
statistic of the episode; learned consumption happens in the direct model.

``pooled_whiten_v2`` (review 2026-09-30, F03/F28/F29) keeps the v1 interface
(one per-gene channel, three pair scalars, the same zero-initialized stem and
head, the same exact B1 gate) but uses the estimator that the G1/G2 gates
validated (``gates/gate_rules.py`` ``_pooled``/``_pooled_lowrank``/
``woodbury_lda``): ``D`` is the full pooled within-class per-gene variance
plus a floor of 1% of its mean over support-variable genes; the low-rank part
is fitted on D-standardised residuals with ``lambda = max(ev - 1, 0)`` and
rank ``<= min(32, floor(dof / 2))``.  The ``floor(dof / 2)`` cap
(:data:`PW2_RANK_CAP_DOF_DIVISOR`) is a deliberate deviation from the validated
``woodbury_lda`` m=32 rule (review F03 fix text); it binds only when
``dof < 64`` (for example K2 B10), and ``dof_rank_divisor=None`` restores the
pure m=32 rule.  Support-silent genes (identical in every support row) are
masked out of every v2 output, and its Mahalanobis pair scalar is
class-centred, chi^2-scaled, asinh-compressed and centred again over classes
(gate-weighted), so its per-query level is identically zero and cannot track
how many support-silent genes (or how much depth) a query has.  ``pooled_whiten_v1``
and ``lcs_v1`` are unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import torch
from torch import nn

GeneGeneOperator = Literal["none", "pooled_whiten_v1", "lcs_v1", "pooled_whiten_v2"]
GENE_GENE_OPERATORS: tuple[str, ...] = (
    "none",
    "pooled_whiten_v1",
    "lcs_v1",
    "pooled_whiten_v2",
)
LCS_GENE_CHANNELS = 4
LCS_PAIR_SCALARS = 6
# Column 6 of the full scalar surface (pooled rank fraction) is used only by
# the pooled-whitening operator; lcs_v1 keeps its six declared scalars.
_FULL_PAIR_SCALARS = 7


@dataclass(frozen=True)
class GeneGeneOperatorSpec:
    """Which LCS surfaces an operator consumes.

    ``pooled_whiten_v1`` (primary, LDA-like): the pooled rank<=32 whitened
    query-minus-class-mean per gene, plus whitened Mahalanobis, pooled rank
    fraction and gate per pair; no per-class subspaces are fitted.
    ``lcs_v1``: pooled whitening plus the per-class rank<=8 subspace
    channels (residual, reconstruction, loading energy) and scalars.
    ``pooled_whiten_v2``: indices refer to its own surfaces
    (:func:`pooled_whiten_v2_gene_channels`, :data:`PW2_PAIR_SCALAR_NAMES`):
    the symmetric-whitened difference per gene, and the class-centred
    chi^2-scaled Mahalanobis, pooled rank fraction and gate per pair.
    """

    gene_channels: tuple[int, ...]
    pair_scalars: tuple[int, ...]
    max_class_rank: int


GENE_GENE_OPERATOR_SPECS: dict[str, GeneGeneOperatorSpec] = {
    "pooled_whiten_v1": GeneGeneOperatorSpec(
        gene_channels=(2,), pair_scalars=(3, 6, 5), max_class_rank=0
    ),
    "lcs_v1": GeneGeneOperatorSpec(
        gene_channels=(0, 1, 2, 3),
        pair_scalars=(0, 1, 2, 3, 4, 5),
        max_class_rank=8,
    ),
    "pooled_whiten_v2": GeneGeneOperatorSpec(
        gene_channels=(0,), pair_scalars=(0, 1, 2), max_class_rank=0
    ),
}
LCS_MAX_CLASS_RANK = 8
LCS_MAX_POOLED_RANK = 32
LCS_GATE_PSEUDO_ROWS = 4.0
LCS_WHITENING_PRIOR_DOF = 4.0
LCS_PEARSON_CLAMP = 8.0
LCS_CHANNEL_SCALE = 4.0
_RELATIVE_EIGEN_TOLERANCE = 1.0e-9
_ABSOLUTE_EIGEN_TOLERANCE = 1.0e-10


def validate_gene_gene_operator(value: object) -> GeneGeneOperator:
    if value not in GENE_GENE_OPERATORS:
        raise ValueError(
            f"gene_gene_operator must be one of {GENE_GENE_OPERATORS}; got {value!r}"
        )
    return value  # type: ignore[return-value]


def lcs_support_gate(counts: torch.Tensor) -> torch.Tensor:
    """``(n - 1) / (n - 1 + 4)`` for ``n >= 2`` and exactly zero for ``n <= 1``."""

    counts = counts.to(dtype=torch.float64)
    excess = (counts - 1.0).clamp_min(0.0)
    return torch.where(
        counts >= 2.0,
        excess / (excess + LCS_GATE_PSEUDO_ROWS),
        torch.zeros_like(counts),
    )


@dataclass(frozen=True)
class LCSSupportFit:
    """Support-only LCS factors (fp32 storage, fp64 construction)."""

    class_mean: torch.Tensor  # [K, G]
    class_loadings: torch.Tensor  # [K, G, R]; masked columns are zero
    class_direction_variance: torch.Tensor  # [K, R]
    class_residual_variance: torch.Tensor  # [K] per-gene residual variance
    class_rank: torch.Tensor  # [K] retained class rank
    class_gate: torch.Tensor  # [K]
    loading_energy_feature: torch.Tensor  # [K, G] log1p(normalized energy)
    pooled_loadings: torch.Tensor  # [G, P]
    pooled_diagonal: torch.Tensor  # [G] D of Sigma = D + U Lambda U^T
    pooled_capacitance_inverse: torch.Tensor  # [P, P] (Lambda^-1 + U^T D^-1 U)^-1
    pooled_rank: torch.Tensor  # scalar retained pooled rank


@dataclass(frozen=True)
class LCSQueryContext:
    """Per-(query, class) LCS state; pair index is ``query * K + class``."""

    fit: LCSSupportFit
    query_pearson: torch.Tensor  # [Q, G] fp32
    class_count: int
    subspace_coordinates: torch.Tensor  # [Q*K, R] U_c^T (z_q - mu_c)
    whitening_coefficients: torch.Tensor  # [Q*K, P] M^-1 U^T D^-1 (z_q - mu_c)
    pair_scalars: torch.Tensor  # [Q*K, 7] gated (see GeneGeneOperatorSpec)
    pair_gate: torch.Tensor  # [Q*K]


def _eigen_keep(evals: torch.Tensor, count: int) -> torch.Tensor:
    top = evals[:count]
    scale = evals.clamp_min(0.0).max() if int(evals.numel()) else evals.new_zeros(())
    tolerance = scale * _RELATIVE_EIGEN_TOLERANCE + _ABSOLUTE_EIGEN_TOLERANCE
    return top > tolerance


def fit_lcs_support(
    support_pearson: torch.Tensor,
    support_labels: torch.Tensor,
    class_count: int,
    *,
    max_class_rank: int = LCS_MAX_CLASS_RANK,
    max_pooled_rank: int = LCS_MAX_POOLED_RANK,
) -> LCSSupportFit:
    """Fit class subspaces and pooled whitening from Pearson-view support rows."""

    if support_pearson.ndim != 2 or support_labels.ndim != 1:
        raise ValueError("LCS support must have shapes [rows, genes] and [rows]")
    rows, genes = (int(value) for value in support_pearson.shape)
    if rows != int(support_labels.numel()) or genes < 1:
        raise ValueError("LCS support rows and labels are misaligned")
    device = support_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        z = support_pearson.detach().to(dtype=torch.float64)
        labels = support_labels.to(device=device, dtype=torch.long)
        counts = torch.bincount(labels, minlength=int(class_count)).to(torch.float64)
        mean = z.new_zeros((int(class_count), genes))
        mean.index_add_(0, labels, z)
        mean = mean / counts.clamp_min(1.0).unsqueeze(1)
        centered = z - mean.index_select(0, labels)

        loadings = z.new_zeros((int(class_count), genes, int(max_class_rank)))
        direction_variance = z.new_zeros((int(class_count), int(max_class_rank)))
        residual_variance = z.new_zeros(int(class_count))
        class_rank = z.new_zeros(int(class_count))
        for class_index in range(int(class_count) if int(max_class_rank) > 0 else 0):
            members = torch.nonzero(labels == class_index, as_tuple=False).flatten()
            n = int(members.numel())
            if n < 2:
                continue
            block = centered.index_select(0, members)
            gram = block @ block.transpose(0, 1)
            evals, evecs = torch.linalg.eigh(gram)
            evals = evals.flip(0)
            evecs = evecs.flip(1)
            rank = min(n - 1, int(max_class_rank))
            keep = _eigen_keep(evals, rank)
            top = evals[:rank].clamp_min(_ABSOLUTE_EIGEN_TOLERANCE)
            vectors = (block.transpose(0, 1) @ evecs[:, :rank]) / top.sqrt()
            vectors = vectors * keep.to(dtype=vectors.dtype)
            loadings[class_index, :, :rank] = vectors
            kept_evals = evals[:rank].clamp_min(0.0) * keep.to(dtype=evals.dtype)
            direction_variance[class_index, :rank] = kept_evals / float(n)
            total = evals.clamp_min(0.0).sum()
            residual_variance[class_index] = (total - kept_evals.sum()).clamp_min(
                0.0
            ) / float(n * genes)
            class_rank[class_index] = keep.sum().to(dtype=torch.float64)

        gate = lcs_support_gate(counts)
        weighted = (loadings.square() * direction_variance.unsqueeze(1)).sum(dim=2)
        normalizer = direction_variance.sum(dim=1, keepdim=True)
        energy = torch.where(
            normalizer > 0.0,
            float(genes) * weighted / normalizer.clamp_min(1.0e-300),
            torch.zeros_like(weighted),
        )
        energy_feature = torch.log1p(energy)

        dof = int((counts - 1.0).clamp_min(0.0).sum().item())
        pooled_rank_cap = int(max_pooled_rank)
        pooled_loadings = z.new_zeros((genes, pooled_rank_cap))
        pooled_lambda = z.new_zeros(pooled_rank_cap)
        pooled_keep = torch.zeros(pooled_rank_cap, device=device, dtype=torch.bool)
        if dof >= 1:
            gram = centered @ centered.transpose(0, 1)
            evals, evecs = torch.linalg.eigh(gram)
            evals = evals.flip(0)
            evecs = evecs.flip(1)
            rank = min(pooled_rank_cap, dof, rows)
            keep = _eigen_keep(evals, rank)
            top = evals[:rank].clamp_min(_ABSOLUTE_EIGEN_TOLERANCE)
            vectors = (centered.transpose(0, 1) @ evecs[:, :rank]) / top.sqrt()
            pooled_loadings[:, :rank] = vectors * keep.to(dtype=vectors.dtype)
            pooled_lambda[:rank] = (
                evals[:rank].clamp_min(0.0) * keep.to(dtype=evals.dtype) / float(dof)
            )
            pooled_keep[:rank] = keep
            per_gene = centered.square().sum(dim=0) / float(dof)
            explained = (pooled_loadings.square() * pooled_lambda.unsqueeze(0)).sum(
                dim=1
            )
            residual = (per_gene - explained).clamp_min(0.0)
            diagonal = (float(dof) * residual + LCS_WHITENING_PRIOR_DOF) / (
                float(dof) + LCS_WHITENING_PRIOR_DOF
            )
        else:
            diagonal = z.new_ones(genes)
        inverse_diagonal = diagonal.reciprocal()
        capacitance = pooled_loadings.transpose(0, 1) @ (
            pooled_loadings * inverse_diagonal.unsqueeze(1)
        )
        inverse_lambda = torch.where(
            pooled_keep,
            pooled_lambda.clamp_min(1.0e-300).reciprocal(),
            torch.ones_like(pooled_lambda),
        )
        capacitance = capacitance + torch.diag(inverse_lambda)
        capacitance = 0.5 * (capacitance + capacitance.transpose(0, 1))
        capacitance_inverse = torch.cholesky_inverse(torch.linalg.cholesky(capacitance))
        capacitance_inverse = capacitance_inverse * (
            pooled_keep.unsqueeze(0) & pooled_keep.unsqueeze(1)
        ).to(dtype=capacitance_inverse.dtype)

        return LCSSupportFit(
            class_mean=mean.float(),
            class_loadings=loadings.float(),
            class_direction_variance=direction_variance.float(),
            class_residual_variance=residual_variance.float(),
            class_rank=class_rank.float(),
            class_gate=gate.float(),
            loading_energy_feature=energy_feature.float(),
            pooled_loadings=pooled_loadings.float(),
            pooled_diagonal=diagonal.float(),
            pooled_capacitance_inverse=capacitance_inverse.float(),
            pooled_rank=pooled_keep.sum().float(),
        )


def lcs_query_context(fit: LCSSupportFit, query_pearson: torch.Tensor) -> LCSQueryContext:
    """Per-(query, class) projections and gated pair scalars."""

    if query_pearson.ndim != 2:
        raise ValueError("LCS queries must have shape [rows, genes]")
    genes = int(query_pearson.size(1))
    if genes != int(fit.class_mean.size(1)):
        raise ValueError("LCS support and query gene counts differ")
    device = query_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        zq = query_pearson.detach().to(dtype=torch.float64)
        mean = fit.class_mean.double()
        loadings = fit.class_loadings.double()
        class_count = int(mean.size(0))
        query_count = int(zq.size(0))
        # Subspace coordinates a_qc = U_c^T (z_q - mu_c).
        query_projection = torch.einsum("qg,cgr->qcr", zq, loadings)
        mean_projection = torch.einsum("cg,cgr->cr", mean, loadings)
        coordinates = query_projection - mean_projection.unsqueeze(0)
        query_square = zq.square().sum(dim=1)
        mean_square = mean.square().sum(dim=1)
        cross = zq @ mean.transpose(0, 1)
        difference_square = (
            query_square.unsqueeze(1) - 2.0 * cross + mean_square.unsqueeze(0)
        ).clamp_min(0.0)
        coordinate_square = coordinates.square().sum(dim=2)
        residual_energy = (difference_square - coordinate_square).clamp_min(0.0) / genes
        subspace_energy = coordinate_square / genes
        variance = fit.class_direction_variance.double()
        noise = fit.class_residual_variance.double()
        direction_mask = (variance > 0.0).to(dtype=torch.float64)
        ratio = coordinates.square() / (
            variance.unsqueeze(0) + noise.view(1, -1, 1) + 1.0e-6
        )
        rank = fit.class_rank.double()
        subspace_mahalanobis = (ratio * direction_mask.unsqueeze(0)).sum(
            dim=2
        ) / rank.clamp_min(1.0).unsqueeze(0)

        inverse_diagonal = fit.pooled_diagonal.double().reciprocal()
        pooled = fit.pooled_loadings.double()
        capacitance_inverse = fit.pooled_capacitance_inverse.double()
        weighted_query = zq * inverse_diagonal.unsqueeze(0)
        weighted_mean = mean * inverse_diagonal.unsqueeze(0)
        diagonal_mahalanobis = (
            (zq * weighted_query).sum(dim=1).unsqueeze(1)
            - 2.0 * (zq @ weighted_mean.transpose(0, 1))
            + (mean * weighted_mean).sum(dim=1).unsqueeze(0)
        )
        projected = (weighted_query @ pooled).unsqueeze(1) - (
            weighted_mean @ pooled
        ).unsqueeze(0)
        coefficients = projected @ capacitance_inverse
        whitened_mahalanobis = (
            diagonal_mahalanobis - (projected * coefficients).sum(dim=2)
        ).clamp_min(0.0) / genes

        gate = fit.class_gate.double().unsqueeze(0).expand(query_count, -1)
        rank_fraction = (rank / float(LCS_MAX_CLASS_RANK)).unsqueeze(0).expand(
            query_count, -1
        )
        scalars = torch.stack(
            (
                gate * torch.log1p(residual_energy),
                gate * torch.log1p(subspace_energy),
                gate * torch.log1p(subspace_mahalanobis),
                gate * torch.log1p(whitened_mahalanobis),
                gate * rank_fraction,
                gate,
                gate * (fit.pooled_rank.double() / float(LCS_MAX_POOLED_RANK)),
            ),
            dim=-1,
        )
        pair_count = query_count * class_count
        return LCSQueryContext(
            fit=fit,
            query_pearson=query_pearson.detach().float(),
            class_count=class_count,
            subspace_coordinates=coordinates.reshape(pair_count, -1).float(),
            whitening_coefficients=coefficients.reshape(pair_count, -1).float(),
            pair_scalars=scalars.reshape(pair_count, _FULL_PAIR_SCALARS).float(),
            pair_gate=gate.reshape(pair_count).float(),
        )


def lcs_gene_channels(
    context: LCSQueryContext,
    pair_indices: torch.Tensor,
    *,
    start: int,
    stop: int,
) -> torch.Tensor:
    """Four gated per-gene channels for one (pair chunk, gene chunk): [P, g, 4]."""

    fit = context.fit
    device = context.query_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        class_count = int(context.class_count)
        query_indices = torch.div(pair_indices, class_count, rounding_mode="floor")
        class_indices = torch.remainder(pair_indices, class_count)
        difference = context.query_pearson[:, start:stop].index_select(
            0, query_indices
        ) - fit.class_mean[:, start:stop].index_select(0, class_indices)
        loadings = fit.class_loadings[:, start:stop].index_select(0, class_indices)
        coordinates = context.subspace_coordinates.index_select(0, pair_indices)
        reconstruction = torch.einsum("pgr,pr->pg", loadings, coordinates)
        residual = difference - reconstruction
        correction = (
            context.whitening_coefficients.index_select(0, pair_indices)
            @ fit.pooled_loadings[start:stop].transpose(0, 1)
        )
        whitened = (difference - correction) / fit.pooled_diagonal[
            start:stop
        ].sqrt().unsqueeze(0)
        energy = fit.loading_energy_feature[:, start:stop].index_select(
            0, class_indices
        )
        gate = context.pair_gate.index_select(0, pair_indices).unsqueeze(1)
        bound = LCS_PEARSON_CLAMP
        return torch.stack(
            (
                gate * residual.clamp(-bound, bound) / LCS_CHANNEL_SCALE,
                gate * reconstruction.clamp(-bound, bound) / LCS_CHANNEL_SCALE,
                gate * whitened.clamp(-bound, bound) / LCS_CHANNEL_SCALE,
                gate * energy / LCS_CHANNEL_SCALE,
            ),
            dim=-1,
        )


def build_lcs_pair_head(
    model_dim: int, scalars: int = LCS_PAIR_SCALARS
) -> nn.Sequential:
    """MLP(scalars -> model_dim -> 2 * model_dim) whose output layer starts at zero."""

    head = nn.Sequential(
        nn.Linear(int(scalars), int(model_dim)),
        nn.GELU(),
        nn.Linear(int(model_dim), 2 * int(model_dim)),
    )
    nn.init.zeros_(head[-1].weight)
    nn.init.zeros_(head[-1].bias)
    return head


def build_lcs_extra_stem(stem_width: int, channels: int = LCS_GENE_CHANNELS) -> nn.Linear:
    """Bias-free Linear(channels -> stem width) that starts at exactly zero."""

    extra = nn.Linear(int(channels), int(stem_width), bias=False)
    nn.init.zeros_(extra.weight)
    return extra


# --------------------------------------------------------------------------
# pooled_whiten_v2: the G1/G2 gate-validated pooled low-rank estimator
# --------------------------------------------------------------------------

PW2_MAX_POOLED_RANK = 32
# Rank cap min(PW2_MAX_POOLED_RANK, floor(dof / PW2_RANK_CAP_DOF_DIVISOR)):
# a declared deviation from the gate rule's woodbury_lda m=32 (review F03 fix
# text).  It binds only for dof < 2 * 32; ``dof_rank_divisor=None`` in
# :func:`fit_pooled_whiten_v2_support` gives the pure m=32 gate rule.
PW2_RANK_CAP_DOF_DIVISOR = 2
PW2_VARIANCE_FLOOR = 1.0e-2
PW2_GENE_CHANNELS = 1
PW2_PAIR_SCALARS = 3
PW2_GENE_CHANNEL_NAMES = ("symmetric_whitened_difference",)
PW2_PAIR_SCALAR_NAMES = (
    "centred_chi2_mahalanobis",
    "pooled_rank_fraction",
    "gate",
)


@dataclass(frozen=True)
class PooledWhitenV2Fit:
    """Support-only ``pooled_whiten_v2`` factors (fp64 construction and storage).

    ``Sigma = D^1/2 (I + U diag(lambda) U^T) D^1/2`` on support-variable genes;
    ``U`` has orthonormal columns in D-standardised coordinates.
    """

    class_mean: torch.Tensor  # [K, G]
    variable_genes: torch.Tensor  # [G] bool; False marks a support-silent gene
    pooled_diagonal: torch.Tensor  # [G] D (1 on support-silent genes)
    inverse_scale: torch.Tensor  # [G] D^-1/2 on variable genes, exactly 0 on silent
    pooled_loadings: torch.Tensor  # [G, P] U; zero rows on silent genes
    pooled_lambda: torch.Tensor  # [P] max(ev - 1, 0); zero on dropped columns
    pooled_rank: torch.Tensor  # scalar: retained columns (lambda > 0)
    variable_gene_count: torch.Tensor  # scalar: support-variable genes (chi^2 dof)
    class_gate: torch.Tensor  # [K] exact-zero-at-B1 support gate
    class_rank: torch.Tensor  # [K] zeros: no per-class subspaces are fitted
    dof: int  # sum_c max(n_c - 1, 0)
    rank_cap: int  # min(max_pooled_rank, floor(dof / divisor), rows); no dof term if divisor None


@dataclass(frozen=True)
class PooledWhitenV2Context:
    """Per-(query, class) ``pooled_whiten_v2`` state; pair index is ``query * K + class``."""

    fit: PooledWhitenV2Fit
    query_pearson: torch.Tensor  # [Q, G] fp32
    class_count: int
    coordinate_difference: torch.Tensor  # [Q*K, P] fp64 U^T D^-1/2 (z_q - mu_c)
    mahalanobis: torch.Tensor  # [Q*K] fp64 ungated whitened Mahalanobis M_qc
    centred_statistic: torch.Tensor  # [Q*K] fp64 ungated x_qc = (M_qc - mean_c M_qc) / sqrt(2 r)
    pair_statistic: torch.Tensor  # [Q*K] fp64 ungated asinh(x_qc) - sum_c g_c asinh(x_qc) / sum_c g_c
    pair_scalars: torch.Tensor  # [Q*K, 3] fp32 gated (PW2_PAIR_SCALAR_NAMES)
    pair_gate: torch.Tensor  # [Q*K] fp32


def fit_pooled_whiten_v2_support(
    support_pearson: torch.Tensor,
    support_labels: torch.Tensor,
    class_count: int,
    *,
    max_pooled_rank: int = PW2_MAX_POOLED_RANK,
    variance_floor: float = PW2_VARIANCE_FLOOR,
    dof_rank_divisor: int | None = PW2_RANK_CAP_DOF_DIVISOR,
) -> PooledWhitenV2Fit:
    """Gate-rule pooled low-rank covariance from Pearson-view support rows.

    Ports ``gate_rules._pooled`` / ``_pooled_lowrank``: ``D`` is the pooled
    within-class per-gene variance plus ``variance_floor`` times its mean over
    support-variable genes; the dual PCA (fp64 ``eigh`` of the ``rows x rows``
    Gram) runs on D-standardised residuals, ``lambda = max(ev - 1, 0)`` and the
    rank is capped at ``min(max_pooled_rank, floor(dof / dof_rank_divisor))``.
    The dof cap is the declared deviation from the gate rule's m=32
    (:data:`PW2_RANK_CAP_DOF_DIVISOR`); ``dof_rank_divisor=None`` drops it
    (pure ``woodbury_lda`` m=``max_pooled_rank``).  Using ``dof`` instead of
    ``rows`` as the divisor rescales ``D`` globally and leaves the
    eigenvalues, loadings and every argmin unchanged.  ``max_pooled_rank=0`` is
    the diagonal-only (rank-0) control.
    """

    if support_pearson.ndim != 2 or support_labels.ndim != 1:
        raise ValueError("pooled_whiten_v2 support must have shapes [rows, genes] and [rows]")
    rows, genes = (int(value) for value in support_pearson.shape)
    if rows != int(support_labels.numel()) or genes < 1:
        raise ValueError("pooled_whiten_v2 support rows and labels are misaligned")
    if int(max_pooled_rank) < 0 or not float(variance_floor) > 0.0:
        raise ValueError("pooled_whiten_v2 needs a non-negative rank and a positive floor")
    if dof_rank_divisor is not None and int(dof_rank_divisor) < 1:
        raise ValueError("pooled_whiten_v2 dof_rank_divisor must be None or >= 1")
    device = support_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        z = support_pearson.detach().to(dtype=torch.float64)
        labels = support_labels.to(device=device, dtype=torch.long)
        counts = torch.bincount(labels, minlength=int(class_count)).to(torch.float64)
        mean = z.new_zeros((int(class_count), genes))
        mean.index_add_(0, labels, z)
        mean = mean / counts.clamp_min(1.0).unsqueeze(1)
        # Support-silent genes (identical in every support row) carry no
        # support information; they are removed from D, U and every output.
        variable = z.amax(dim=0) > z.amin(dim=0)
        mask = variable.to(dtype=torch.float64)
        variable_count = mask.sum()
        dof = int((counts - 1.0).clamp_min(0.0).sum().item())
        dof_cap = rows if dof_rank_divisor is None else dof // int(dof_rank_divisor)
        rank_cap = max(0, min(int(max_pooled_rank), dof_cap, rows))
        residual = (z - mean.index_select(0, labels)) * mask.unsqueeze(0)
        if dof >= 1:
            variance = residual.square().sum(dim=0) / float(dof)
            floor = (
                float(variance_floor) * variance.sum() / variable_count.clamp_min(1.0)
            )
            floor = torch.where(
                floor > _ABSOLUTE_EIGEN_TOLERANCE, floor, torch.ones_like(floor)
            )
            diagonal = torch.where(variable, variance + floor, torch.ones_like(variance))
        else:
            diagonal = z.new_ones(genes)
        inverse_scale = diagonal.rsqrt() * mask
        loadings = z.new_zeros((genes, int(max_pooled_rank)))
        spikes = z.new_zeros(int(max_pooled_rank))
        if rank_cap >= 1:
            scaled = residual * inverse_scale.unsqueeze(0)
            gram = (scaled @ scaled.transpose(0, 1)) / float(dof)
            evals, evecs = torch.linalg.eigh(gram)
            evals = evals.flip(0)
            evecs = evecs.flip(1)
            top = evals[:rank_cap]
            spike = (top - 1.0).clamp_min(0.0)
            keep = (spike > 0.0).to(dtype=torch.float64)
            vectors = (scaled.transpose(0, 1) @ evecs[:, :rank_cap]) / (
                top.clamp_min(_ABSOLUTE_EIGEN_TOLERANCE) * float(dof)
            ).sqrt()
            loadings[:, :rank_cap] = vectors * keep.unsqueeze(0)
            spikes[:rank_cap] = spike * keep
        return PooledWhitenV2Fit(
            class_mean=mean,
            variable_genes=variable,
            pooled_diagonal=diagonal,
            inverse_scale=inverse_scale,
            pooled_loadings=loadings,
            pooled_lambda=spikes,
            pooled_rank=(spikes > 0.0).sum().to(dtype=torch.float32),
            variable_gene_count=variable_count,
            class_gate=lcs_support_gate(counts).float(),
            class_rank=torch.zeros(int(class_count), device=device),
            dof=dof,
            rank_cap=rank_cap,
        )


def pooled_whiten_v2_query_context(
    fit: PooledWhitenV2Fit, query_pearson: torch.Tensor
) -> PooledWhitenV2Context:
    """Whitened Mahalanobis per (query, class) and the gated v2 pair scalars.

    ``M_qc = ||D^-1/2 d||^2 - sum_k lambda_k / (1 + lambda_k) (u_k^T D^-1/2 d)^2``
    with ``d = z_q - mu_c`` on support-variable genes (``woodbury_lda``).  With
    ``x_qc = (M_qc - mean_c M_qc) / sqrt(2 r)`` (``r`` the support-variable
    gene count, the chi^2 dof of ``M``; the mean over classes with
    ``n_c >= 2``) the pair statistic is
    ``s_qc = asinh(x_qc) - sum_c g_c asinh(x_qc) / sum_c g_c`` with ``g_c`` the
    support gate.  Centring again after the nonlinearity, with gate weights,
    makes the gated scalar ``g_c s_qc`` sum to zero over classes for every
    query and support-size mix (asinh would otherwise turn a skewed class
    contrast into a level that follows depth); with equal ``n_c`` it is the
    plain mean over fitted classes.  The per-query class order and argmin are
    those of ``M_qc``.
    """

    if query_pearson.ndim != 2:
        raise ValueError("pooled_whiten_v2 queries must have shape [rows, genes]")
    genes = int(query_pearson.size(1))
    if genes != int(fit.class_mean.size(1)):
        raise ValueError("pooled_whiten_v2 support and query gene counts differ")
    device = query_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        zq = query_pearson.detach().to(dtype=torch.float64)
        class_count = int(fit.class_mean.size(0))
        query_count = int(zq.size(0))
        scale = fit.inverse_scale.unsqueeze(0)
        scaled_query = zq * scale
        scaled_mean = fit.class_mean * scale
        diagonal_mahalanobis = (
            scaled_query.square().sum(dim=1).unsqueeze(1)
            - 2.0 * (scaled_query @ scaled_mean.transpose(0, 1))
            + scaled_mean.square().sum(dim=1).unsqueeze(0)
        )
        loadings = fit.pooled_loadings
        coordinates = (scaled_query @ loadings).unsqueeze(1) - (
            scaled_mean @ loadings
        ).unsqueeze(0)
        spikes = fit.pooled_lambda
        shrink = spikes / (1.0 + spikes)
        mahalanobis = (
            diagonal_mahalanobis - (coordinates.square() * shrink).sum(dim=2)
        ).clamp_min(0.0)
        gate = fit.class_gate.to(dtype=torch.float64)
        fitted = (gate > 0.0).to(dtype=torch.float64).unsqueeze(0)
        fitted_count = fitted.sum().clamp_min(1.0)
        centre = (mahalanobis * fitted).sum(dim=1, keepdim=True) / fitted_count
        centred = (mahalanobis - centre) / (
            2.0 * fit.variable_gene_count.clamp_min(1.0)
        ).sqrt()
        # Second centring after asinh, weighted by the support gates, so the
        # gated scalar the head sees sums to zero over classes for every query
        # (plain mean over fitted classes when all n_c are equal).
        compressed = torch.asinh(centred)
        gate_total = gate.sum()
        gate_total = torch.where(gate_total > 0.0, gate_total, torch.ones_like(gate_total))
        level = (compressed * gate.unsqueeze(0)).sum(dim=1, keepdim=True) / gate_total
        statistic = compressed - level
        pair_gate = gate.unsqueeze(0).expand(query_count, -1)
        rank_fraction = fit.pooled_rank.to(dtype=torch.float64) / float(
            PW2_MAX_POOLED_RANK
        )
        scalars = torch.stack(
            (
                pair_gate * statistic,
                pair_gate * rank_fraction,
                pair_gate,
            ),
            dim=-1,
        )
        pair_count = query_count * class_count
        return PooledWhitenV2Context(
            fit=fit,
            query_pearson=query_pearson.detach().float(),
            class_count=class_count,
            coordinate_difference=coordinates.reshape(pair_count, -1),
            mahalanobis=mahalanobis.reshape(pair_count),
            centred_statistic=centred.reshape(pair_count),
            pair_statistic=statistic.reshape(pair_count),
            pair_scalars=scalars.reshape(pair_count, PW2_PAIR_SCALARS).float(),
            pair_gate=pair_gate.reshape(pair_count).float(),
        )


def pooled_whiten_v2_gene_channels(
    context: PooledWhitenV2Context,
    pair_indices: torch.Tensor,
    *,
    start: int,
    stop: int,
) -> torch.Tensor:
    """Gated symmetric-whitened difference for one (pair chunk, gene chunk): [P, g, 1].

    ``w = (I - U diag(1 - (1 + lambda)^-1/2) U^T) D^-1/2 (z_q - mu_c)``, so the
    unclamped ``sum_g w_g^2`` equals ``M_qc``; support-silent genes are exactly 0.
    """

    fit = context.fit
    device = context.query_pearson.device
    with torch.autocast(device_type=device.type, enabled=False):
        class_count = int(context.class_count)
        query_indices = torch.div(pair_indices, class_count, rounding_mode="floor")
        class_indices = torch.remainder(pair_indices, class_count)
        scale = fit.inverse_scale[start:stop].unsqueeze(0)
        difference = (
            context.query_pearson[:, start:stop]
            .to(dtype=torch.float64)
            .index_select(0, query_indices)
            - fit.class_mean[:, start:stop].index_select(0, class_indices)
        ) * scale
        whitening = 1.0 - (1.0 + fit.pooled_lambda).rsqrt()
        coordinates = context.coordinate_difference.index_select(0, pair_indices)
        correction = (coordinates * whitening.unsqueeze(0)) @ fit.pooled_loadings[
            start:stop
        ].transpose(0, 1)
        whitened = difference - correction
        gate = (
            context.pair_gate.index_select(0, pair_indices)
            .to(dtype=torch.float64)
            .unsqueeze(1)
        )
        bound = LCS_PEARSON_CLAMP
        channel = gate * whitened.clamp(-bound, bound) / LCS_CHANNEL_SCALE
        return channel.to(dtype=torch.float32).unsqueeze(-1)


def gene_gene_operator_contract(operator: str) -> dict[str, object] | None:
    """Declared estimator semantics for receipts (``None`` keeps v1 receipts unchanged)."""

    if operator != "pooled_whiten_v2":
        return None
    return {
        "operator": "pooled_whiten_v2",
        "reference": (
            "hashprompt_improvement_loop/realism_v2_20260929/gates/gate_rules.py "
            "_pooled/_pooled_lowrank/woodbury_lda"
        ),
        "view": "support Pearson view clamp((log_view - mean) / std, -8, 8) as v1",
        "support_silent_genes": "identical in every support row; masked from D, U, channel, scalars",
        "diagonal": "pooled within-class variance (SS / dof) + 0.01 * mean over support-variable genes",
        "low_rank": "fp64 dual PCA of D-standardised residuals; lambda = max(ev - 1, 0); "
        "rank <= min(32, floor(dof / 2))",
        "deviation_from_reference": (
            "rank cap floor(dof / 2) is not in gate_rules.woodbury_lda (m=32); it binds only "
            "for dof < 64 (e.g. K2 B10, dof 18 -> rank <= 9); dof_rank_divisor=None restores m=32"
        ),
        "mahalanobis": "||D^-1/2 d||^2 - sum_k lambda_k / (1 + lambda_k) (u_k^T D^-1/2 d)^2",
        "gene_channels": ["gate * clamp((I - U diag(1 - (1 + lambda)^-1/2) U^T) D^-1/2 d, +-8) / 4"],
        "pair_scalars": [
            "gate_c * (asinh(x_qc) - sum_c gate_c asinh(x_qc) / sum_c gate_c), "
            "x_qc = (M_qc - mean_{c: n_c >= 2} M_qc) / sqrt(2 * support-variable genes); "
            "sum over classes of this scalar is 0 per query",
            "gate * pooled_rank / 32",
            "gate",
        ],
        "gate": "(n_c - 1) / (n_c + 3) for n_c >= 2, exactly 0 for n_c <= 1",
        "initialization": "extra_stem and lcs_pair_head output layer zero (as v1)",
    }


__all__ = [
    "GENE_GENE_OPERATORS",
    "GENE_GENE_OPERATOR_SPECS",
    "GeneGeneOperatorSpec",
    "LCS_GENE_CHANNELS",
    "LCS_MAX_CLASS_RANK",
    "LCS_MAX_POOLED_RANK",
    "LCS_PAIR_SCALARS",
    "GeneGeneOperator",
    "LCSQueryContext",
    "LCSSupportFit",
    "build_lcs_extra_stem",
    "build_lcs_pair_head",
    "fit_lcs_support",
    "lcs_gene_channels",
    "lcs_query_context",
    "lcs_support_gate",
    "validate_gene_gene_operator",
    "PW2_GENE_CHANNELS",
    "PW2_GENE_CHANNEL_NAMES",
    "PW2_MAX_POOLED_RANK",
    "PW2_PAIR_SCALARS",
    "PW2_PAIR_SCALAR_NAMES",
    "PW2_RANK_CAP_DOF_DIVISOR",
    "PW2_VARIANCE_FLOOR",
    "PooledWhitenV2Context",
    "PooledWhitenV2Fit",
    "fit_pooled_whiten_v2_support",
    "gene_gene_operator_contract",
    "pooled_whiten_v2_gene_channels",
    "pooled_whiten_v2_query_context",
]
