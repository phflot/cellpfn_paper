"""Gene attributions for one case x arm, plus exact-knockout faithfulness and timing (GPU 2, fp32).

usage: run_case.py <case_key> <arm G|C> [--cap 48] [--seed 0]

Coordinates.  Attributions are taken in u = log1p-CP10k coordinates: count mode at the cell's FIXED depth
(x = expm1(u) d / 1e4 and the model's depth input held at d; the architecture report shows raw-count gradient x input
is meaningless because count mode is scale-invariant), processed mode u = x.  Baseline: zero expression (u = 0).

Targets.  For each selected query cell (correctly predicted, capped per class): the fp32 predicted class c and runner-up
j.  l_c ("logit") and l_c - l_j ("margin").  Logit l[q,k] depends only on pair (q,k) (+ the operator's per-query class
centring), so every target needs 2 (query, class) pairs; one backward gives both gradients via per-pair query copies.

Methods (per cell x gene; class ranking = mean over the class's selected cells):
  gxi        u * dl/du at u (differentiable operator for G1v2')
  gxi_trunk  same with the operator as shipped (no_grad; G only) -> how much the operator path adds
  ig16/ig64  integrated gradients, straight path alpha*u, midpoint rule with m = 16 / 64
  op_ko      closed-form operator (LDA) readout: exact change of M_qj - M_qc when z_qg -> z(0)   [margin-type]
  op_mid     closed-form operator readout beta_g (2 z_qg - mu_cg - mu_jg) (sums to M_qj - M_qc)  [margin-type]
             (for C1v2' the same quantities are a data-only LDA surrogate: C has no operator)
Faithfulness (exact, eval mode, fp32, model's own count depth):
  single-gene knockouts (value -> 0) in query cells only, and separately in support + query (support refit),
  on gene set = top-20 of each method U 20 random expressed genes U bottom-20 (ig64, op_ko);
  deletion curves (query only): remove the top-k genes of the class ranking (and of each cell's own ranking),
  k in KGRID, vs random expressed genes; group knockout of the top-50 in support + query.
Outputs: results/<case>__<arm>.npz (+ .json summary), rankings CSVs are written by aggregate.py.
"""
import argparse, json, os, sys, time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cellpfn_attr as ca  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("case")
ap.add_argument("arm")
ap.add_argument("--cap", type=int, default=48)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--row-chunk", type=int, default=256)
ap.add_argument("--ko-chunk", type=int, default=512)
ap.add_argument("--skip-ig64", action="store_true")
args = ap.parse_args()

KGRID = [1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50]
TOPN, NRAND, NLOW, SQN = 20, 20, 20, 10
RESULT = ca.OUT / "results" / f"{args.case}__{args.arm}"
dev = ca.gpu_setup()
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.manual_seed(args.seed)
rng = np.random.default_rng(args.seed)
T = ca.Timer()
log = lambda *a: print(time.strftime("%H:%M:%S"), *a, flush=True)

model, info = ca.load_model(args.arm, dev)
data = ca.case_inputs(args.case)
stored, _, _, stored_path = ca.stored_logits(args.case, args.arm)
K, G, mode = len(data.class_names), data.support.shape[1], data.mode
xs = torch.as_tensor(data.support, device=dev)
ys = torch.as_tensor(data.support_labels, device=dev)
xq_all = torch.as_tensor(data.query, device=dev)
is_g = model.gene_gene_operator != "none"
log("loaded", info["label"], args.case, mode, "Q", len(data.query), "G", G, "K", K)

# ------------------------------------------------------------------ support fit (+ operator fit for the readout)
with torch.no_grad():  # not inference_mode: the support state is reused inside autograd graphs
    with T("fit_support"):
        fitted = ca.fit_support(model, xs, ys, K, mode)
    base = fitted.state.base
    zs = model._lcs_pearson(base.support_x, base.support_depths if mode == "count" else None,
                            base.global_log_mean, base.global_log_std, mode)
    from hashprompt.models import gene_gene_operator as ggo
    lda_fit = fitted.fit if is_g else ggo.fit_pooled_whiten_v2_support(zs, base.support_y_local, K)

# ------------------------------------------------------------------ cell selection (correct under stored bf16 AND fp32)
y = data.query_labels
cand = np.flatnonzero(stored.argmax(1) == y)
sel = []
for c in range(K):
    idx = cand[y[cand] == c]
    if len(idx) > args.cap:
        idx = np.sort(rng.choice(idx, args.cap, replace=False))
    sel.extend(idx.tolist())
sel = np.asarray(sorted(sel))
with torch.inference_mode():
    with T("baseline_logits_selected"):
        lg_sel = ca.full_logits(model, fitted, xq_all[torch.as_tensor(sel, device=dev)], 64).cpu().numpy()
keep = lg_sel.argmax(1) == y[sel]
sel, lg_sel = sel[keep], lg_sel[keep]
n = len(sel)
cls = y[sel]
order2 = np.argsort(-lg_sel, 1)
pred, run = order2[:, 0], order2[:, 1]
assert np.array_equal(pred, cls)
margin0 = lg_sel[np.arange(n), pred] - lg_sel[np.arange(n), run]
log("selected cells", n, "per class", np.bincount(cls, minlength=K).tolist(), "dropped (fp32 flip)", int((~keep).sum()))

xq = xq_all[torch.as_tensor(sel, device=dev)].contiguous()
u, d = ca.to_u(xq, mode)
pred_t = torch.as_tensor(pred, device=dev)
run_t = torch.as_tensor(run, device=dev)
expressed = (xq > 0)

# ------------------------------------------------------------------ gradient passes
rows_u = torch.cat((u, u))
rows_d = None if d is None else torch.cat((d, d))
rows_cls = torch.cat((pred_t, run_t))


def grad_pass(alpha: float, diff_op: bool):
    """d l / d u at alpha*u for every selected cell, for its predicted (rows :n) and runner-up (rows n:) class."""
    model.train()
    R = int(rows_u.size(0))
    grads = torch.empty_like(rows_u)
    logits = torch.empty(R, device=dev)
    for s in range(0, R, args.row_chunk):
        e = min(R, s + args.row_chunk)
        leaf = (alpha * rows_u[s:e]).detach().requires_grad_(True)
        dd = None if rows_d is None else rows_d[s:e]
        with torch.enable_grad():
            x = ca.from_u(leaf, dd, mode)
            lg = ca.score_pairs(model, fitted, x, torch.arange(e - s, device=dev), rows_cls[s:e], depths=dd,
                                differentiable_operator=diff_op)
            g, = torch.autograd.grad(lg.sum(), leaf)
        grads[s:e] = g
        logits[s:e] = lg.detach()
    model.eval()
    return grads[:n], grads[n:], logits[:n], logits[n:]


attr = {}
passes = {}
with T("gxi"):
    gp, gr, lp1, lr1 = grad_pass(1.0, diff_op=is_g)
attr["gxi_logit"] = u * gp
attr["gxi_margin"] = u * (gp - gr)
passes["gxi"] = 1
endpoint = (lp1 - lr1).cpu().numpy()
log("gxi done", round(T.t["gxi"], 1), "s; fp32-train endpoint margin vs eval margin max|diff|",
    float(np.abs(endpoint - margin0).max()))
if is_g:
    with T("gxi_trunk"):
        gp2, gr2, _, _ = grad_pass(1.0, diff_op=False)
    attr["gxi_trunk_logit"] = u * gp2
    attr["gxi_trunk_margin"] = u * (gp2 - gr2)
    passes["gxi_trunk"] = 1
    del gp2, gr2
    log("gxi_trunk done", round(T.t["gxi_trunk"], 1))

# baseline (u = 0, fixed depth) logits for IG completeness
model.eval()
with torch.inference_mode():
    zero_rows = ca.from_u(torch.zeros_like(rows_u), rows_d, mode)
    l0 = []
    for s in range(0, int(rows_u.size(0)), args.row_chunk):
        e = min(int(rows_u.size(0)), s + args.row_chunk)
        l0.append(ca.score_pairs(model, fitted, zero_rows[s:e], torch.arange(e - s, device=dev), rows_cls[s:e],
                                 depths=None if rows_d is None else rows_d[s:e]))
    l0 = torch.cat(l0)
l0p, l0r = l0[:n].cpu().numpy(), l0[n:].cpu().numpy()

for m in ([16] if args.skip_ig64 else [16, 64]):
    sp = torch.zeros_like(u)
    sr = torch.zeros_like(u)
    with T(f"ig{m}"):
        for k in range(m):
            a = (k + 0.5) / m
            gp_, gr_, _, _ = grad_pass(a, diff_op=is_g)
            sp += gp_
            sr += gr_
    attr[f"ig{m}_logit"] = u * sp / m
    attr[f"ig{m}_margin"] = u * (sp - sr) / m
    passes[f"ig{m}"] = m
    log(f"ig{m} done", round(T.t[f"ig{m}"], 1), "s")
del sp, sr, gp, gr

# ------------------------------------------------------------------ operator closed-form readout
with torch.inference_mode(), T("operator_readout"):
    fit_holder = ca.Fitted(state=fitted.state, fit=lda_fit, mode=mode, K=K)
    zq = model._lcs_pearson(xq, d if mode == "count" else None, base.global_log_mean, base.global_log_std, mode)
    z0 = model._lcs_pearson(torch.zeros(1, G, device=dev), torch.ones(1, device=dev) if mode == "count" else None,
                            base.global_log_mean, base.global_log_std, mode)[0]
    mid, ko, contrast = ca.operator_readout(fit_holder, zq, pred_t, run_t, z0)
attr["op_mid_margin"] = mid
attr["op_ko_margin"] = ko
log("operator readout", round(T.t["operator_readout"], 2), "s")

# IG completeness and convergence (margin and logit)
lm1 = margin0
diag = {}
for m in ([16] if args.skip_ig64 else [16, 64]):
    s_m = attr[f"ig{m}_margin"].sum(1).cpu().numpy()
    s_l = attr[f"ig{m}_logit"].sum(1).cpu().numpy()
    tgt_m = endpoint - (l0p - l0r)
    tgt_l = lp1.cpu().numpy() - l0p
    diag[f"ig{m}_completeness_margin_median_relgap"] = float(np.median(np.abs(s_m - tgt_m) / np.maximum(np.abs(tgt_m), 1e-6)))
    diag[f"ig{m}_completeness_logit_median_relgap"] = float(np.median(np.abs(s_l - tgt_l) / np.maximum(np.abs(tgt_l), 1e-6)))
if not args.skip_ig64:
    a16, a64 = attr["ig16_margin"], attr["ig64_margin"]
    diag["ig16_vs_ig64_median_rel_l2"] = float(((a16 - a64).norm(dim=1) / a64.norm(dim=1).clamp_min(1e-12)).median())
if is_g:
    diag["gxi_trunk_vs_gxi_median_rel_l2"] = float(((attr["gxi_trunk_margin"] - attr["gxi_margin"]).norm(dim=1)
                                                    / attr["gxi_margin"].norm(dim=1).clamp_min(1e-12)).median())
log("diagnostics", json.dumps(diag))

# ------------------------------------------------------------------ class rankings
methods = [k for k in attr]
class_scores = {}
cells_of = {c: np.flatnonzero(cls == c) for c in range(K)}
for mname, a in attr.items():
    cs = torch.zeros(K, G, device=dev)
    for c, ix in cells_of.items():
        if len(ix):
            cs[c] = a[torch.as_tensor(ix, device=dev)].mean(0)
    class_scores[mname] = cs.cpu().numpy()

# ------------------------------------------------------------------ exact knockouts
def margins(X: torch.Tensor, prd: torch.Tensor, rn: torch.Tensor, fit_obj=None):
    """Exact fp32 eval logits l_pred, l_run for rows X (model's own count depth)."""
    fo = fitted if fit_obj is None else fit_obj
    out_p, out_r = [], []
    with torch.inference_mode():
        for s in range(0, int(X.size(0)), args.ko_chunk):
            Xb = X[s:s + args.ko_chunk]
            r = int(Xb.size(0))
            ar = torch.arange(r, device=dev)
            lg = ca.score_pairs(model, fo, Xb, torch.cat((ar, ar)),
                                torch.cat((prd[s:s + r], rn[s:s + r])))
            out_p.append(lg[:r]); out_r.append(lg[r:])
    return torch.cat(out_p), torch.cat(out_r)


# noise floor: baseline margins via the knockout path, two batch layouts
with T("noise_floor"):
    bp, br = margins(xq, pred_t, run_t)
    perm = torch.randperm(n, device=dev)
    bp2, br2 = margins(xq[perm], pred_t[perm], run_t[perm])
    inv = torch.empty_like(perm); inv[perm] = torch.arange(n, device=dev)
    base_margin = (bp - br)
    base_logit = bp
    noise = float(((bp2 - br2)[inv] - base_margin).abs().max())
diag["ko_noise_floor_margin_maxabs"] = noise
diag["eval_margin_vs_selected_baseline_maxabs"] = float(np.abs(base_margin.cpu().numpy() - margin0).max())
log("noise floor", noise)

primary = ["gxi_margin", "ig16_margin", "op_ko_margin", "op_mid_margin"] + \
          ([] if args.skip_ig64 else ["ig64_margin"]) + (["gxi_trunk_margin"] if is_g else [])
low_from = ["op_ko_margin"] + ([] if args.skip_ig64 else ["ig64_margin"])
ko_sets = {}
for c, ix in cells_of.items():
    if len(ix) < 3:
        continue
    genes, tags = [], {}
    def add(g_list, tag):
        for g in g_list:
            g = int(g)
            if g not in tags:
                genes.append(g); tags[g] = []
            tags[g].append(tag)
    for mname in primary:
        add(np.argsort(-class_scores[mname][c])[:TOPN], f"top:{mname}")
    for mname in low_from:
        add(np.argsort(class_scores[mname][c])[:NLOW], f"low:{mname}")
    expr_c = np.flatnonzero(expressed[torch.as_tensor(ix, device=dev)].any(0).cpu().numpy())
    pool = np.setdiff1d(expr_c, np.asarray(genes))
    rand = rng.choice(pool, min(NRAND, len(pool)), replace=False)
    add(rand, "random_expressed")
    # support+query subset (one support refit per gene): top-SQN of each method, bottom-SQN, SQN random
    sq = set()
    for mname in primary:
        sq.update(int(g) for g in np.argsort(-class_scores[mname][c])[:SQN])
    for mname in low_from:
        sq.update(int(g) for g in np.argsort(class_scores[mname][c])[:SQN])
    sq.update(int(g) for g in rand[:SQN])
    ko_sets[c] = (np.asarray(genes), tags, np.asarray([g in sq for g in genes]))
log("knockout gene sets", {c: (len(v[0]), int(v[2].sum())) for c, v in ko_sets.items()})

ko_q, ko_sq = {}, {}
with T("ko_query_only"):
    for c, (genes, _, _) in ko_sets.items():
        ix = torch.as_tensor(cells_of[c], device=dev)
        Xc = xq[ix]
        nc = int(ix.numel())
        res_m = np.zeros((len(genes), nc), np.float32)
        res_l = np.zeros((len(genes), nc), np.float32)
        gb = max(1, args.ko_chunk * 4 // nc)
        for s in range(0, len(genes), gb):
            gg = torch.as_tensor(genes[s:s + gb], device=dev)
            X = Xc.repeat(len(gg), 1)
            X[torch.arange(X.size(0), device=dev), gg.repeat_interleave(nc)] = 0.0
            lp, lr = margins(X, pred_t[ix].repeat(len(gg)), run_t[ix].repeat(len(gg)))
            res_m[s:s + len(gg)] = (base_margin[ix].repeat(len(gg)) - (lp - lr)).reshape(len(gg), nc).cpu().numpy()
            res_l[s:s + len(gg)] = (base_logit[ix].repeat(len(gg)) - lp).reshape(len(gg), nc).cpu().numpy()
        ko_q[c] = (res_m, res_l)
n_ko_q = sum(len(v[0]) for v in ko_sets.values())
log("query-only knockouts", n_ko_q, "genes x class;", round(T.t["ko_query_only"], 1), "s")

# support + query knockouts: one support refit per gene (shared across classes)
union = sorted({int(g) for genes, _, sqm in ko_sets.values() for g in genes[sqm]})
where = {g: [(c, int(np.flatnonzero(genes == g)[0])) for c, (genes, _, sqm) in ko_sets.items()
             if g in set(genes[sqm].tolist())] for g in union}
for c, (genes, _, _) in ko_sets.items():
    ko_sq[c] = np.full((len(genes), len(cells_of[c])), np.nan, np.float32)
t_fit = 0.0
with T("ko_support_query"):
    for g in union:
        xs2 = xs.clone(); xs2[:, g] = 0.0
        torch.cuda.synchronize(); t0 = time.perf_counter()
        with torch.inference_mode():
            f2 = ca.fit_support(model, xs2, ys, K, mode)
        torch.cuda.synchronize(); t_fit += time.perf_counter() - t0
        cl = [c for c, _ in where[g]]
        ixs = [torch.as_tensor(cells_of[c], device=dev) for c in cl]
        ix = torch.cat(ixs)
        X = xq[ix].clone(); X[:, g] = 0.0
        lp, lr = margins(X, pred_t[ix], run_t[ix], f2)
        dm = (base_margin[ix] - (lp - lr)).cpu().numpy()
        o = 0
        for (c, row), ixc in zip(where[g], ixs):
            k_ = int(ixc.numel())
            ko_sq[c][row] = dm[o:o + k_]
            o += k_
log("support+query knockouts", len(union), "genes;", round(T.t["ko_support_query"], 1), "s (fits", round(t_fit, 1), "s)")

# ------------------------------------------------------------------ deletion curves (query only)
best_ig = "ig16_margin" if args.skip_ig64 else "ig64_margin"
del_orders = ["gxi_margin", best_ig, "op_ko_margin", "op_mid_margin"]
del_res = {}  # (c, ordering) -> [len(KGRID), nc] margin drop
KMAX = max(KGRID)
with T("deletion"):
    for c, ix_np in cells_of.items():
        if len(ix_np) < 3:
            continue
        ix = torch.as_tensor(ix_np, device=dev)
        nc = len(ix_np)
        Xc = xq[ix]
        ex = expressed[ix]
        expr_c = np.flatnonzero(ex.any(0).cpu().numpy())
        orderings = {}
        for mname in del_orders:
            top = torch.as_tensor(np.argsort(-class_scores[mname][c])[:KMAX].copy(), device=dev)
            orderings[f"class:{mname}"] = top.unsqueeze(0).expand(nc, -1)
        for mname in ["gxi_margin", best_ig, "op_ko_margin"]:
            orderings[f"cell:{mname}"] = torch.argsort(attr[mname][ix], dim=1, descending=True)[:, :KMAX]
        for r_ in range(2):
            top = torch.as_tensor(rng.permutation(expr_c)[:KMAX].copy(), device=dev)
            orderings[f"class:random_expressed_{r_}"] = top.unsqueeze(0).expand(nc, -1)
            # per cell: random order of the cell's own expressed genes (random keys, unexpressed last)
            keys = torch.rand(ex.shape, device=dev, generator=torch.Generator(device=dev).manual_seed(1000 * c + r_))
            keys = torch.where(ex, keys, keys - 2.0)
            orderings[f"cell:random_expressed_{r_}"] = torch.argsort(keys, dim=1, descending=True)[:, :KMAX]
        for oname, top in orderings.items():
            X = Xc.repeat(len(KGRID), 1)
            for ki, k in enumerate(KGRID):
                X[ki * nc:(ki + 1) * nc].scatter_(1, top[:, :k], 0.0)
            lp, lr = margins(X, pred_t[ix].repeat(len(KGRID)), run_t[ix].repeat(len(KGRID)))
            del_res[(c, oname)] = (base_margin[ix].repeat(len(KGRID)) - (lp - lr)).reshape(len(KGRID), nc).cpu().numpy()
log("deletion curves", len(del_res), round(T.t["deletion"], 1), "s")

# group knockout of the class top-50 in support + query (refit) vs random expressed 50
group = {}
with T("group_ko_support_query"):
    for c, ix_np in cells_of.items():
        if len(ix_np) < 3:
            continue
        ix = torch.as_tensor(ix_np, device=dev)
        expr_c = np.flatnonzero(expressed[ix].any(0).cpu().numpy())
        sets = {m_: np.argsort(-class_scores[m_][c])[:50] for m_ in del_orders}
        for r_ in range(2):
            sets[f"random_expressed_{r_}"] = rng.choice(expr_c, min(50, len(expr_c)), replace=False)
        for sname, gl in sets.items():
            gt = torch.as_tensor(np.asarray(gl, dtype=np.int64), device=dev)
            xs2 = xs.clone(); xs2[:, gt] = 0.0
            with torch.inference_mode():
                f2 = ca.fit_support(model, xs2, ys, K, mode)
            X = xq[ix].clone(); X[:, gt] = 0.0
            lp, lr = margins(X, pred_t[ix], run_t[ix], f2)
            group[(c, sname)] = (base_margin[ix] - (lp - lr)).cpu().numpy()
log("group knockouts", len(group), round(T.t["group_ko_support_query"], 1), "s")

# ------------------------------------------------------------------ timing of naive exact knockout
with T("naive_single_ko_full_forward"):
    tq = xq_all if len(data.query) <= 1024 else xq_all[:512]
    with torch.inference_mode():
        X = tq.clone(); X[:, int(union[0])] = 0.0
        _ = ca.full_logits(model, fitted, X, 64)
naive_scale = len(data.query) / int(tq.size(0))
naive_q = T.t["naive_single_ko_full_forward"] * naive_scale
with T("naive_single_ko_support_refit"):
    with torch.inference_mode():
        xs2 = xs.clone(); xs2[:, int(union[0])] = 0.0
        _ = ca.fit_support(model, xs2, ys, K, mode)
timing = dict(T.t)
timing.update(
    n_cells=n, G=G, K=K, Q=len(data.query), N=len(data.support), passes=passes,
    naive_single_ko_full_forward_seconds=naive_q,
    naive_single_ko_full_forward_scaled_from=int(tq.size(0)),
    naive_exact_ko_all_genes_query_only_hours=naive_q * G / 3600.0,
    naive_exact_ko_all_genes_support_query_hours=(naive_q + T.t["naive_single_ko_support_refit"]) * G / 3600.0,
    ko_query_only_seconds_per_gene_class=T.t["ko_query_only"] / max(n_ko_q, 1),
    ko_restricted_all_genes_query_only_hours=T.t["ko_query_only"] / max(n_ko_q, 1) * K * G / 3600.0,
    ko_support_query_genes=len(union), ko_support_query_fit_seconds=t_fit,
    ko_support_query_seconds_per_gene=T.t["ko_support_query"] / max(len(union), 1),
    peak_gpu_gib=torch.cuda.max_memory_allocated() / 2**30,
    torch=torch.__version__, cuda=torch.version.cuda, gpu=torch.cuda.get_device_name(dev),
    cuda_visible_devices=os.environ.get("CUDA_VISIBLE_DEVICES"))
log("timing", json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in timing.items()}))

# ------------------------------------------------------------------ save
RESULT.parent.mkdir(parents=True, exist_ok=True)
save = dict(sel=sel, cls=cls, pred=pred, run=run, margin0=margin0, logits_sel=lg_sel, symbols=data.symbols,
            class_names=np.asarray(data.class_names), kgrid=np.asarray(KGRID), l0p=l0p, l0r=l0r)
for mname, cs in class_scores.items():
    save[f"class__{mname}"] = cs
for c, (genes, tags, sqm) in ko_sets.items():
    save[f"ko_genes__{c}"] = genes
    save[f"ko_sqmask__{c}"] = sqm
    save[f"ko_tags__{c}"] = np.asarray([";".join(tags[int(g)]) for g in genes])
    save[f"ko_q_margin__{c}"] = ko_q[c][0]
    save[f"ko_q_logit__{c}"] = ko_q[c][1]
    save[f"ko_sq_margin__{c}"] = ko_sq[c]
    ix = torch.as_tensor(cells_of[c], device=dev)
    gt = torch.as_tensor(genes, device=dev)
    for mname, a in attr.items():
        save[f"cellattr__{mname}__{c}"] = a[ix][:, gt].cpu().numpy()  # per-cell attribution on the KO gene set
for (c, oname), v in del_res.items():
    save[f"del__{c}__{oname}"] = v
for (c, sname), v in group.items():
    save[f"group__{c}__{sname}"] = v
np.savez_compressed(str(RESULT) + ".npz", **save)
# per-cell attribution maps (float16) for reuse, cache only
np.savez_compressed(ca.OUT / "cache" / f"cellattr_{args.case}__{args.arm}.npz",
                    **{m_: a.half().cpu().numpy() for m_, a in attr.items()})
json.dump(dict(case=args.case, arm=args.arm, info=info, stored=stored_path, diag=diag, timing=timing,
               cells_per_class=np.bincount(cls, minlength=K).tolist(), class_names=data.class_names, mode=mode),
          open(str(RESULT) + ".json", "w"), indent=1, default=str)
log("saved", RESULT)
