"""Small gene-attribution tool for direct CellPFN (G1v2' / C1v2' @ 96000).  Prototype, 2026-10-08.

Everything here imports project code READ-ONLY (hashprompt_eval_learnable @ 494b44e, whose model files hash to the
checkpoint's recorded model_source_sha256 / model_dependency_sha256s) and writes nothing outside
gene_importance_20261008/.

Pieces
------
* load_model(arm)            checkpoint -> AlignedClassInducingDirectPFN exactly as the evaluator builds it
                             (kwargs + strict state dict, .eval().requires_grad_(False)), with sha256 pins and a
                             check that the imported model sources are the ones the checkpoint was trained with.
* case_inputs(spec)          exported real-gene case -> the benchmark's input matrices (benchmark column order),
                             gene symbols in that order, query labels, stored logits of the v2-column evaluation.
* evaluator_logits(...)      the evaluator's own _score_direct (bf16 autocast, inference_mode, query batch 32/64).
* score_pairs(...)           a line-by-line re-implementation of score_inductive restricted to chosen
                             (query row, class) pairs, with (a) optional fixed query depth (count mode),
                             (b) a cached operator support fit and (c) an optional differentiable operator
                             query side.  Logit l[q, c] depends only on query q and class c (plus the operator's
                             per-query class centring, which is computed for every class), so a margin needs 2 pairs.
* operator_readout(...)      closed-form pooled_whiten_v2 contrasts (LDA form), per cell and gene.
"""
from __future__ import annotations

import dataclasses
import hashlib
import math
import os
import sys
import time
import types
from pathlib import Path

import numpy as np
import torch

BASE = Path("/share/runs/2026/30-03-phflot-hashprompt")
LOOP = BASE / "hashprompt_improvement_loop"
EVAL_REPO = BASE / "hashprompt_eval_learnable"
OUT = LOOP / "gene_importance_20261008"
for p in (str(EVAL_REPO / "src"), str(EVAL_REPO), str(LOOP / "realcell_baselines_20261008" / "code")):
    if p not in sys.path:
        sys.path.insert(0, p)

import cases as realcases  # noqa: E402
from hashprompt.models import gene_gene_operator as ggo  # noqa: E402
from hashprompt.models.aligned_class_inducing_direct_pfn import AlignedClassInducingDirectPFN  # noqa: E402

TRAIN = LOOP / "gene_gene_r12k_v22_20261001" / "training"
CHECKPOINTS = {
    "G": (TRAIN / "G1v2p/checkpoints/checkpoint_96000.pt",
          "aa5490d5a5d4020c87eba05297d80a31c901bcbeba6ba49b4b4857acb84f9f02", "G1v2p_096000"),
    "C": (TRAIN / "C1v2p/checkpoints/checkpoint_96000.pt", None, "C1v2p_096000"),  # sha pinned at load (cee5126d...)
}
C_SHA_PREFIX = "cee5126d"
PRED = LOOP / "gene_gene_r12k_eval_v2col_20261002" / "practical"

# case key -> spec.  'pred' / 'key' locate the stored v2-column logits; qbs = evaluator query batch size.
CASES = {
    "pbmc_l1_b10_s0": dict(panel="pbmc", case_id="celltype.l1_b10_s0", mode="count",
                           pred="pbmc/results/{arm}/celltype.l1_b10_s0/predictions.npz", key="logits__{arm}", qbs=32),
    "pbmc_l1_b10_s1": dict(panel="pbmc", case_id="celltype.l1_b10_s1", mode="count",
                           pred="pbmc/results/{arm}/celltype.l1_b10_s1/predictions.npz", key="logits__{arm}", qbs=32),
    "pbmc_l1_b100_s0": dict(panel="pbmc", case_id="celltype.l1_b100_s0", mode="count",
                            pred="pbmc/results/{arm}/celltype.l1_b100_s0/predictions.npz", key="logits__{arm}", qbs=32),
    "zebra_dev_b10_s0": dict(panel="zebra", case_id="zebra_closed_development_b10_s0_p0", mode="processed",
                             pred="zebra/{arm}/zebra_cell_type/zebra_closed_development_b10_s0_p0/predictions.npz",
                             key="logits", qbs=32),
    "kidney_core9_A_F0_count": dict(panel="kidney", case_id="kidney_core9_cell_type_F0_b100__support_hvg4096",
                                    mode="count",
                                    pred="kidney/{arm}/kidney/kidney_core9_cell_type_F0_b100/predictions.npz",
                                    key="logits__support_hvg4096__count", qbs=32),
    "kidney_core9_A_F0_processed": dict(panel="kidney", case_id="kidney_core9_cell_type_F0_b100__support_hvg4096",
                                        mode="processed",
                                        pred="kidney/{arm}/kidney/kidney_core9_cell_type_F0_b100/predictions.npz",
                                        key="logits__support_hvg4096__processed", qbs=32),
}


def sha256_file(path, chunk=8 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


# --------------------------------------------------------------------------------------------- model loading
def load_model(arm: str, device: torch.device):
    path, pinned, label = CHECKPOINTS[arm]
    sha = sha256_file(path)
    if pinned is not None and sha != pinned:
        raise ValueError(f"{arm}: checkpoint sha256 {sha} != pinned {pinned}")
    if arm == "C" and not sha.startswith(C_SHA_PREFIX):
        raise ValueError(f"C: checkpoint sha256 {sha} does not start with {C_SHA_PREFIX}")
    payload = torch.load(path, map_location="cpu", weights_only=True)
    # The imported model sources must be the ones the checkpoint records (training identity).
    models_dir = EVAL_REPO / "src/hashprompt/models"
    src = {"aligned_class_inducing_direct_pfn": sha256_file(models_dir / "aligned_class_inducing_direct_pfn.py")}
    if payload["model_source_sha256"] != src["aligned_class_inducing_direct_pfn"]:
        raise ValueError("model source differs from the checkpoint's model_source_sha256")
    deps = dict(payload.get("model_dependency_sha256s", {}))
    for name, want in deps.items():
        f = models_dir / f"{name}.py"
        if f.exists() and sha256_file(f) != want:
            raise ValueError(f"dependency {name} differs from the checkpoint")
    model = AlignedClassInducingDirectPFN(**dict(payload["model_kwargs"]))
    model.load_state_dict(payload["model_state_dict"], strict=True)
    model.to(device).eval().requires_grad_(False)
    info = dict(arm=arm, label=label, checkpoint=str(path), sha256=sha, gene_gene_operator=model.gene_gene_operator,
                parameter_count=sum(p.numel() for p in model.parameters()),
                model_source_sha256=payload["model_source_sha256"], dependencies_checked=sorted(deps))
    return model, info


# --------------------------------------------------------------------------------------------- case inputs
@dataclasses.dataclass
class CaseData:
    key: str
    spec: dict
    support: np.ndarray        # [N, G] float32, benchmark column order, as fed to the model
    support_labels: np.ndarray
    query: np.ndarray          # [Q, G] float32
    query_labels: np.ndarray
    query_obs: np.ndarray
    symbols: np.ndarray        # [G] gene symbols in benchmark column order
    class_names: list
    mode: str


def case_inputs(key: str) -> CaseData:
    spec = CASES[key]
    c = realcases.load_case(spec["panel"], spec["case_id"])
    order = c.benchmark_order()
    xs = c.support_X()[:, order].toarray()
    xq = c.query_X()[:, order].toarray()
    if spec["panel"] == "kidney" and spec["mode"] == "processed":
        # run_cellxgene_kidney.full_library_cp10k_log1p: float64 log1p(counts * (1e4 / max(full library, 1))) -> f32
        lib = np.asarray(c.n_counts, dtype=np.float64)
        ls, lq = lib[c.support_mask][:, None], lib[c.query_mask][:, None]
        xs = np.asarray(np.log1p(xs.astype(np.float64) * (10_000.0 / np.maximum(ls, 1.0))), dtype=np.float32)
        xq = np.asarray(np.log1p(xq.astype(np.float64) * (10_000.0 / np.maximum(lq, 1.0))), dtype=np.float32)
    xs = np.ascontiguousarray(xs, dtype=np.float32)
    xq = np.ascontiguousarray(xq, dtype=np.float32)
    obs, y = realcases.load_query_labels(spec["panel"], spec["case_id"])
    if not np.array_equal(obs, c.query_obs_ids):
        raise ValueError("label file query order differs from the case")
    return CaseData(key=key, spec=spec, support=xs, support_labels=c.support_labels.astype(np.int64), query=xq,
                    query_labels=y, query_obs=np.asarray(obs), symbols=np.asarray(c.var_symbol)[order],
                    class_names=list(c.class_names), mode=spec["mode"])


def stored_logits(key: str, arm: str):
    spec = CASES[key]
    label = CHECKPOINTS[arm][2]
    z = np.load(PRED / spec["pred"].format(arm=label))
    return (z[spec["key"].format(arm=label)].astype(np.float32), z["labels"], z["obs_ids"],
            str(PRED / spec["pred"].format(arm=label)))


# --------------------------------------------------------------------------------------------- evaluator path
def evaluator_logits(model, device, data: CaseData) -> np.ndarray:
    """The evaluator's own scoring function, imported read-only (bf16 autocast, inference_mode)."""
    from experiments import run_direct_cellpfn_evaluation as direct
    loaded = types.SimpleNamespace(model=model, device=device)
    classes = np.arange(len(data.class_names), dtype=np.int64)
    return direct._score_direct(loaded, data.support, data.support_labels, classes, data.query,
                                observation_mode=data.mode, query_batch_size=data.spec["qbs"])


# --------------------------------------------------------------------------------------------- support fit
@dataclasses.dataclass
class Fitted:
    state: object
    fit: object | None        # PooledWhitenV2Fit (G only)
    mode: str
    K: int


def fit_support(model, support: torch.Tensor, labels: torch.Tensor, K: int, mode: str) -> Fitted:
    classes = torch.arange(K, device=support.device)
    with torch.no_grad():
        state = model.fit_support(support, labels, classes, observation_mode=mode)
        fit = None
        if model.gene_gene_operator == "pooled_whiten_v2":
            base = state.base
            zs = model._lcs_pearson(base.support_x, base.support_depths if mode == "count" else None,
                                    base.global_log_mean, base.global_log_std, mode)
            fit = ggo.fit_pooled_whiten_v2_support(zs, base.support_y_local, int(base.class_ids.numel()))
    return Fitted(state=state, fit=fit, mode=mode, K=K)


def operator_context(model, fitted: Fitted, query: torch.Tensor, depths: torch.Tensor, differentiable: bool):
    """pooled_whiten_v2 query context from a cached support fit.  differentiable=False is bit-identical to the
    model's own _lcs_context (same fit, same function); differentiable=True keeps the query-side autograd graph
    (same fp64 operations in the same order as ggo.pooled_whiten_v2_query_context)."""
    base = fitted.state.base
    mode = fitted.mode
    zq32 = model._lcs_pearson(query, depths if mode == "count" else None, base.global_log_mean,
                              base.global_log_std, mode)
    fit = fitted.fit
    ref = ggo.pooled_whiten_v2_query_context(fit, zq32.detach())
    if not differentiable:
        return ref
    with torch.autocast(device_type=query.device.type, enabled=False):
        zq = zq32.to(torch.float64)
        scale = fit.inverse_scale.unsqueeze(0)
        sq, sm = zq * scale, fit.class_mean * scale
        diag = sq.square().sum(1).unsqueeze(1) - 2.0 * (sq @ sm.transpose(0, 1)) + sm.square().sum(1).unsqueeze(0)
        coord = (sq @ fit.pooled_loadings).unsqueeze(1) - (sm @ fit.pooled_loadings).unsqueeze(0)
        shrink = fit.pooled_lambda / (1.0 + fit.pooled_lambda)
        M = (diag - (coord.square() * shrink).sum(2)).clamp_min(0.0)
        gate = fit.class_gate.to(torch.float64)
        fitted_mask = (gate > 0.0).to(torch.float64).unsqueeze(0)
        centre = (M * fitted_mask).sum(1, keepdim=True) / fitted_mask.sum().clamp_min(1.0)
        centred = (M - centre) / (2.0 * fit.variable_gene_count.clamp_min(1.0)).sqrt()
        comp = torch.asinh(centred)
        gt = gate.sum()
        gt = torch.where(gt > 0.0, gt, torch.ones_like(gt))
        stat = comp - (comp * gate.unsqueeze(0)).sum(1, keepdim=True) / gt
        pg = gate.unsqueeze(0).expand_as(M)
        rf = fit.pooled_rank.to(torch.float64) / float(ggo.PW2_MAX_POOLED_RANK)
        scalars = torch.stack((pg * stat, pg * rf, pg), -1)
        P = int(coord.shape[0]) * int(coord.shape[1])
        return dataclasses.replace(ref, query_pearson=zq32, coordinate_difference=coord.reshape(P, -1),
                                   pair_scalars=scalars.reshape(P, -1).float())


# --------------------------------------------------------------------------------------------- pair scoring
def score_pairs(model, fitted: Fitted, query: torch.Tensor, pair_rows: torch.Tensor, pair_classes: torch.Tensor, *,
                depths: torch.Tensor | None = None, differentiable_operator: bool = False,
                operator_off: bool = False, return_reduced: bool = False, pair_chunk: int | None = None,
                qdet: torch.Tensor | None = None):
    """score_inductive (ACID:1009-1171) restricted to pairs (pair_rows[i], pair_classes[i]).

    query: [R, G] model-input values (counts in count mode, log1p-CP10k in processed mode).
    depths: optional fixed per-row depths (count mode); default = the model's own query.sum(1).clamp_min(1).
    Returns logits [len(pairs)] (and the pooled relation statistics R [pairs, S, 896] if return_reduced).
    """
    state = fitted.state
    base = state.base
    mode = fitted.mode
    K = fitted.K
    with torch.autocast(device_type=query.device.type, enabled=False):
        query = query.float()
    weights, active = model._select_summary_weights(state, "learned")
    R = int(query.size(0))
    if mode == "count":
        qd = query.sum(dim=1).clamp_min(1.0) if depths is None else depths
    else:
        qd = query.new_zeros(R)
    if qdet is None:  # optional override (a leaf for the DS-LOO detected-fraction correction); default as the model
        qdet = (query > 0).float().mean(dim=1)
    lcs = None
    if model.gene_gene_operator != "none":
        lcs = operator_context(model, fitted, query, qd, differentiable_operator)
    pair_index = pair_rows * K + pair_classes
    mode_index = 0 if mode == "count" else 1
    chunk = model.pair_chunk_size if pair_chunk is None else int(pair_chunk)
    out, reduced_out = [], []
    for start in range(0, int(pair_index.numel()), chunk):
        pidx = pair_index[start:start + chunk]
        cls = pair_classes[start:start + chunk]
        w = weights.index_select(0, cls)
        act = active.index_select(0, cls)
        if lcs is None:
            reduced = model._reduce_pair_relations(base, query, qd, qdet, pidx, w, operator_mode=model.operator_mode)
        else:
            if operator_off:
                reduced = _reduce_operator_off(model, base, query, qd, qdet, pidx, w, lcs)
            else:
                reduced = model._reduce_pair_relations(base, query, qd, qdet, pidx, w,
                                                       operator_mode=model.operator_mode, lcs=lcs)
        logit = head(model, reduced, act, mode_index, lcs, pidx, operator_off=operator_off)
        out.append(logit)
        if return_reduced:
            reduced_out.append(reduced)
    logits = torch.cat(out)
    if return_reduced:
        return logits, torch.cat(reduced_out)
    return logits


def _reduce_operator_off(model, base, query, qd, qdet, pidx, w, lcs):
    """Trunk with the operator's per-gene channel zeroed (extra_stem output 0) -- like the operator_off control."""
    stem = model.relation_mlp.extra_stem
    saved = stem.forward
    stem.forward = lambda x: torch.zeros(*x.shape[:-1], stem.out_features, device=x.device, dtype=x.dtype)
    try:
        return model._reduce_pair_relations(base, query, qd, qdet, pidx, w, operator_mode=model.operator_mode, lcs=lcs)
    finally:
        stem.forward = saved


def head(model, reduced, active, mode_index, lcs, pidx, operator_off=False):
    n = int(reduced.size(0))
    summary_tokens = model.reduction_projection(reduced) + model.class_summary_roles.unsqueeze(0)
    seed = model.program_queries.unsqueeze(0).expand(n, -1, -1)
    attended, _ = model.prototype_cross_attention(seed, summary_tokens, summary_tokens,
                                                  key_padding_mask=~active, need_weights=False)
    programs = model.prototype_cross_norm(seed + attended)
    mode_seed = model.observation_mode_tokens[mode_index].view(1, 1, -1).expand(n, -1, -1)
    transformed = model.program_transformer(torch.cat((mode_seed, programs), dim=1))
    tp = transformed[:, 1:]
    pooled = torch.cat((tp.mean(dim=1), torch.amax(tp, dim=1)), dim=-1)
    with torch.autocast(device_type=reduced.device.type, enabled=False):
        if lcs is None:
            return model.direct_scorer(pooled.float()).squeeze(-1)
        gate = lcs.pair_gate[pidx].unsqueeze(1)
        cols = list(ggo.GENE_GENE_OPERATOR_SPECS[model.gene_gene_operator].pair_scalars)
        lh = gate * model.lcs_pair_head(lcs.pair_scalars[pidx][:, cols])
        if operator_off:
            lh = torch.zeros_like(lh)
        return model.direct_scorer(pooled.float() + lh).squeeze(-1)


def all_pairs(Q: int, K: int, device):
    rows = torch.arange(Q, device=device).repeat_interleave(K)
    cls = torch.arange(K, device=device).repeat(Q)
    return rows, cls


def full_logits(model, fitted, query: torch.Tensor, batch: int, **kw) -> torch.Tensor:
    """All-pair logits [Q, K] in query batches (same batching as the evaluator)."""
    K = fitted.K
    out = []
    for s in range(0, int(query.size(0)), batch):
        q = query[s:s + batch]
        r, c = all_pairs(int(q.size(0)), K, q.device)
        out.append(score_pairs(model, fitted, q, r, c, **kw).reshape(-1, K))
    return torch.cat(out)


# --------------------------------------------------------------------------------------------- coordinates
def to_u(query: torch.Tensor, mode: str):
    """Attribution coordinates: u = log1p(1e4 x / d) with d the cell's depth (count) or u = x (processed)."""
    if mode == "count":
        d = query.sum(1).clamp_min(1.0)
        return torch.log1p(1.0e4 * query / d.unsqueeze(1)), d
    return query.clone(), None


def from_u(u: torch.Tensor, d: torch.Tensor | None, mode: str):
    if mode == "count":
        return torch.expm1(u) * (d.unsqueeze(1) / 1.0e4)
    return u


# --------------------------------------------------------------------------------------------- operator readout
def operator_readout(fitted: Fitted, z_query: torch.Tensor, c_idx: torch.Tensor, j_idx: torch.Tensor,
                     z_zero: torch.Tensor):
    """Closed-form pooled_whiten_v2 (LDA) contrasts for cells q with classes c (predicted) vs j (runner-up).

    beta = Sigma^-1 (mu_c - mu_j) (Woodbury, fp64), per gene
      mid_g = beta_g (2 z_qg - mu_cg - mu_jg)      sums exactly to M_qj - M_qc
      ko_g  = 2 beta_g (z_qg - z0_g)               exact change of M_qj - M_qc when z_qg -> z0_g (zero expression)
    Returns (mid, ko, contrast) as float32 tensors."""
    fit = fitted.fit
    inv = fit.inverse_scale
    U, lam = fit.pooled_loadings, fit.pooled_lambda
    shrink = lam / (1.0 + lam)
    mu = fit.class_mean
    dm = (mu.index_select(0, c_idx) - mu.index_select(0, j_idx)) * inv           # [n, G]
    beta = inv * (dm - (dm @ U) * shrink @ U.T)                                    # [n, G]
    z = z_query.to(torch.float64)
    mid = beta * (2.0 * z - mu.index_select(0, c_idx) - mu.index_select(0, j_idx))
    ko = 2.0 * beta * (z - z_zero.to(torch.float64).unsqueeze(0))
    return mid.float(), ko.float(), mid.sum(1)


def gpu_setup(cap_gib: float = 30.0):
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "2", "this prototype may only use GPU 2"
    assert os.environ.get("CUDA_DEVICE_ORDER") == "PCI_BUS_ID"
    dev = torch.device("cuda:0")
    torch.cuda.set_device(dev)
    total = torch.cuda.get_device_properties(dev).total_memory
    torch.cuda.set_per_process_memory_fraction(min(1.0, cap_gib * (1 << 30) / total), dev)
    return dev


class Timer:
    def __init__(self):
        self.t = {}

    def __call__(self, name):
        timer = self

        class _T:
            def __enter__(self_):
                torch.cuda.synchronize()
                self_.s = time.perf_counter()

            def __exit__(self_, *a):
                torch.cuda.synchronize()
                timer.t[name] = timer.t.get(name, 0.0) + time.perf_counter() - self_.s
        return _T()
