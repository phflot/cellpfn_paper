"""DeepSets leave-one-gene-out (DS-LOO): every single-gene query-side zero-knockout from ~3 relation passes.

usage: dsloo.py <case_key> <arm G|C>     (needs results/<case>__<arm>.npz from run_case.py: same cells / pairs)

Why it works (ARCHITECTURE.md sections 2-3, 6.3): on the query side the trunk mixes genes only through four pooled
statistics of a per-gene relation vector phi[p, s, g] (224-d): R = [mean_g, rms_g, max_g, lse_g - log G].  Knocking out
gene g (value -> 0) changes only phi[., ., g] (with the query's depth and detected fraction held fixed), the operator's
per-gene channel of g (own-gene term; the rank<=32 cross-gene term is ignored) and the operator's pair scalars (exact
closed form).  So:
  pass A   phi for all genes  -> totals (sum, sum of squares, top-2 + argmax, logsumexp) -> R  (checked vs the model)
  head     one backward through the small per-pair head: dl/dR and dl/d(lcs head output)
  pass B   phi again and phi' (whole query row at 0, row scalars fixed, KO operator channel) for every gene ->
           exact per-gene Delta R (mean, rms, max via top-2, lse) -> Delta l_lin = dl/dR . Delta R  + operator pair term
Outputs Delta margin (= Delta l_pred - Delta l_runner) for EVERY gene and selected cell.  Validation only:
  'exact head replay' for the genes of the class's knockout set: l(R + Delta R_g) through the full head (isolates the
  head linearisation), to be compared with the exact knockouts of run_case.py (true model: depth and detected
  fraction recomputed, operator cross-gene term included).
"""
import json, math, os, sys, time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cellpfn_attr as ca  # noqa: E402
from hashprompt.models import gene_gene_operator as ggo  # noqa: E402

case, arm = sys.argv[1], sys.argv[2]
dev = ca.gpu_setup()
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
T = ca.Timer()
log = lambda *a: print(time.strftime("%H:%M:%S"), *a, flush=True)
RES = ca.OUT / "results" / f"{case}__{arm}"
res = np.load(str(RES) + ".npz")
model, info = ca.load_model(arm, dev)
data = ca.case_inputs(case)
K, G, mode = len(data.class_names), data.support.shape[1], data.mode
is_g = model.gene_gene_operator != "none"
xs = torch.as_tensor(data.support, device=dev)
ys = torch.as_tensor(data.support_labels, device=dev)
with torch.no_grad():
    fitted = ca.fit_support(model, xs, ys, K, mode)
base = fitted.state.base
sel, cls, pred, run = res["sel"], res["cls"], res["pred"], res["run"]
n = len(sel)
xq = torch.as_tensor(data.query[sel], device=dev)
weights, active = model._select_summary_weights(fitted.state, "learned")
S = int(weights.size(1))
mode_index = 0 if mode == "count" else 1
eps = float(model.eps)

# rows: per class c, its cells twice (pred pair, runner pair); pair chunks never mix classes (shared gene sets)
qd_all = xq.sum(1).clamp_min(1.0) if mode == "count" else xq.new_zeros(n)
qdet_all = (xq > 0).float().mean(1)
captured = {}
hook = model.relation_mlp.register_forward_hook(lambda m, i, o: captured.__setitem__("phi", o))


def head_logits(R, act, lh, need_grad=False):
    nP = int(R.size(0))
    tok = model.reduction_projection(R) + model.class_summary_roles.unsqueeze(0)
    seed = model.program_queries.unsqueeze(0).expand(nP, -1, -1)
    att, _ = model.prototype_cross_attention(seed, tok, tok, key_padding_mask=~act, need_weights=False)
    prog = model.prototype_cross_norm(seed + att)
    ms = model.observation_mode_tokens[mode_index].view(1, 1, -1).expand(nP, -1, -1)
    tr = model.program_transformer(torch.cat((ms, prog), 1))[:, 1:]
    pooled = torch.cat((tr.mean(1), torch.amax(tr, 1)), -1)
    inp = pooled.float() + (lh if lh is not None else 0.0)
    return model.direct_scorer(inp).squeeze(-1)


def relation_phi(query, qd, qdet, pidx, w, a, b, channels):
    if channels is not None:
        model.relation_mlp.pending_extra = channels[:, a:b]
    try:
        model._relation_chunk_reductions(base, query, qd, qdet, pidx, w, start=a, stop=b,
                                         operator_mode=model.operator_mode)
    finally:
        model.relation_mlp.pending_extra = None
    return captured.pop("phi").float()  # [P, S, g, 224]


# ---------------------------------------------------------------------------------- operator closed forms
if is_g:
    fit = fitted.fit
    inv, U, lam = fit.inverse_scale, fit.pooled_loadings, fit.pooled_lambda
    Wwh = 1.0 - (1.0 + lam).rsqrt()
    shrink = lam / (1.0 + lam)
    A_gg = 1.0 - (U.square() * Wwh).sum(1)                     # own-gene entry of (I - U W U^T)
    S_gg = inv.square() * (1.0 - (U.square() * shrink).sum(1))  # diag of Sigma^-1
    gate64 = fit.class_gate.double()
    fitted_mask = (gate64 > 0).double()
    rf = fit.pooled_rank.double() / float(ggo.PW2_MAX_POOLED_RANK)
    cols = list(ggo.GENE_GENE_OPERATOR_SPECS[model.gene_gene_operator].pair_scalars)
    z0 = model._lcs_pearson(torch.zeros(1, G, device=dev), torch.ones(1, device=dev) if mode == "count" else None,
                            base.global_log_mean, base.global_log_std, mode)[0].double()


def stat_from_M(M):  # M [..., K] fp64 -> gated pair statistic (ggo.pooled_whiten_v2_query_context)
    centre = (M * fitted_mask).sum(-1, keepdim=True) / fitted_mask.sum().clamp_min(1.0)
    x = (M - centre) / (2.0 * fit.variable_gene_count.clamp_min(1.0)).sqrt()
    comp = torch.asinh(x)
    gt = gate64.sum()
    gt = torch.where(gt > 0, gt, torch.ones_like(gt))
    return comp - (comp * gate64).sum(-1, keepdim=True) / gt


out_lin = np.zeros((n, 2, G), np.float32)   # Delta l (base - KO) linearised, [cell, pred/run, gene]
replay = {}                                   # class -> [cells, 2, nset] exact-head replay (base - KO)
checks = dict(max_abs_R_vs_model=0.0, max_abs_logit_vs_model=0.0, channel_recompute_maxabs=0.0)
GC = model.gene_chunk_size
torch.cuda.synchronize(); t_start = time.perf_counter()
t_replay = 0.0
for c in range(K):
    cell_ix = np.flatnonzero(cls == c)
    if len(cell_ix) == 0:
        continue
    kog = res[f"ko_genes__{c}"] if f"ko_genes__{c}" in res.files else np.zeros(0, np.int64)
    kog_t = torch.as_tensor(kog, device=dev)
    ci = torch.as_tensor(cell_ix, device=dev)
    rows_x = torch.cat((xq[ci], xq[ci]))
    rows_qd, rows_qdet = torch.cat((qd_all[ci], qd_all[ci])), torch.cat((qdet_all[ci], qdet_all[ci]))
    rows_cls = torch.cat((torch.as_tensor(pred[cell_ix], device=dev), torch.as_tensor(run[cell_ix], device=dev)))
    nr = int(rows_x.size(0))
    zero_rows = torch.zeros_like(rows_x)
    with torch.no_grad():
        lcs = ca.operator_context(model, fitted, rows_x, rows_qd, False) if is_g else None
    for s0 in range(0, nr, model.pair_chunk_size):
        s1 = min(nr, s0 + model.pair_chunk_size)
        prow = torch.arange(s0, s1, device=dev)
        pcls = rows_cls[s0:s1]
        pidx = prow * K + pcls
        w = weights.index_select(0, pcls)
        act = active.index_select(0, pcls)
        P = s1 - s0
        with torch.no_grad():
            ch_base = ch_ko = None
            if is_g:
                ch_base = ggo.pooled_whiten_v2_gene_channels(lcs, pidx, start=0, stop=G)  # [P, G, 1]
                zq = lcs.query_pearson.index_select(0, prow).double()                       # [P, G]
                mu = fit.class_mean.index_select(0, pcls)
                t = (zq - mu) * inv
                coords = lcs.coordinate_difference.index_select(0, pidx)
                whit = t - (coords * Wwh) @ U.T
                gate_p = lcs.pair_gate.index_select(0, pidx).double().unsqueeze(1)
                chk = (gate_p * whit.clamp(-8, 8) / 4.0).float().unsqueeze(-1)
                checks["channel_recompute_maxabs"] = max(checks["channel_recompute_maxabs"],
                                                         float((chk - ch_base).abs().max()))
                dt = inv * (z0.unsqueeze(0) - zq)
                ch_ko = (gate_p * (whit + A_gg * dt).clamp(-8, 8) / 4.0).float().unsqueeze(-1)
            # ---- pass A: totals
            tot_sum = tot_sq = tot_lse = None
            top_v = top_i = None
            for a in range(0, G, GC):
                b = min(G, a + GC)
                phi = relation_phi(rows_x, rows_qd, rows_qdet, pidx, w, a, b, ch_base)
                cs, cq = phi.sum(2), phi.square().sum(2)
                cl = torch.logsumexp(phi, 2)
                k2 = min(2, b - a)
                v, i = torch.topk(phi, k2, dim=2)
                i = i + a
                if tot_sum is None:
                    tot_sum, tot_sq, tot_lse, top_v, top_i = cs, cq, cl, v, i
                else:
                    tot_sum, tot_sq = tot_sum + cs, tot_sq + cq
                    tot_lse = torch.logaddexp(tot_lse, cl)
                    allv, alli = torch.cat((top_v, v), 2), torch.cat((top_i, i), 2)
                    vv, jj = torch.topk(allv, 2, dim=2)
                    top_v, top_i = vv, torch.gather(alli, 2, jj)
            R = torch.cat((tot_sum / G, torch.sqrt(tot_sq / G + eps), top_v[:, :, 0], tot_lse - math.log(G)), -1)
            ref = model._reduce_pair_relations(base, rows_x, rows_qd, rows_qdet, pidx, w,
                                               operator_mode=model.operator_mode,
                                               **({"lcs": lcs} if is_g else {}))
            checks["max_abs_R_vs_model"] = max(checks["max_abs_R_vs_model"], float((R - ref).abs().max()))
            lh = None
            if is_g:
                sc = lcs.pair_scalars.index_select(0, pidx)[:, cols]
                lh = lcs.pair_gate.index_select(0, pidx).unsqueeze(1) * model.lcs_pair_head(sc)
        # ---- head backward: dl/dR, dl/d(lh)
        Rl = R.detach().requires_grad_(True)
        lhl = lh.detach().requires_grad_(True) if is_g else None
        with torch.enable_grad():
            l0 = head_logits(Rl, act, lhl)
            grads = torch.autograd.grad(l0.sum(), [Rl] + ([lhl] if is_g else []))
        gR = grads[0]
        glh = grads[1] if is_g else None
        with torch.no_grad():
            lref = ca.score_pairs(model, fitted, rows_x, prow, pcls)
            checks["max_abs_logit_vs_model"] = max(checks["max_abs_logit_vs_model"], float((l0.detach() - lref).abs().max()))
            gm, gr_, gx, gl = gR[..., :224], gR[..., 224:448], gR[..., 448:672], gR[..., 672:]
            rms = torch.sqrt(tot_sq / G + eps)
            dl = torch.zeros(P, G, device=dev)
            nset = int(kog_t.numel())
            dR_set = torch.zeros(P, S, nset, 4 * 224, device=dev) if nset else None
            # ---- pass B
            for a in range(0, G, GC):
                b = min(G, a + GC)
                phi = relation_phi(rows_x, rows_qd, rows_qdet, pidx, w, a, b, ch_base)
                phik = relation_phi(zero_rows, rows_qd, rows_qdet, pidx, w, a, b, ch_ko)
                d_mean = (phik - phi) / G
                d_rms = torch.sqrt(((tot_sq.unsqueeze(2) + phik.square() - phi.square()) / G + eps).clamp_min(0)) - rms.unsqueeze(2)
                gidx = torch.arange(a, b, device=dev).view(1, 1, -1, 1)
                is_top = top_i[:, :, 0:1, :] == gidx
                others = torch.where(is_top, top_v[:, :, 1:2, :], top_v[:, :, 0:1, :])
                d_max = torch.maximum(phik, others) - top_v[:, :, 0:1, :]
                L = tot_lse.unsqueeze(2)
                inside = (1.0 - torch.exp(phi - L) + torch.exp(phik - L)).clamp_min(1e-30)
                d_lse = torch.log(inside)
                dl[:, a:b] = (torch.einsum("psgc,psc->pg", d_mean, gm) + torch.einsum("psgc,psc->pg", d_rms, gr_)
                              + torch.einsum("psgc,psc->pg", d_max, gx) + torch.einsum("psgc,psc->pg", d_lse, gl))
                if nset:
                    m_ = (kog_t >= a) & (kog_t < b)
                    if bool(m_.any()):
                        loc = kog_t[m_] - a
                        dR_set[:, :, m_] = torch.cat((d_mean[:, :, loc], d_rms[:, :, loc], d_max[:, :, loc],
                                                      d_lse[:, :, loc]), -1)
            # ---- operator pair-scalar term (exact closed form per gene, linearised through direct_scorer)
            dlh_set = None
            if is_g:
                zq = lcs.query_pearson.index_select(0, prow).double()
                delta = (z0.unsqueeze(0) - zq) * (inv > 0)                       # [P, G]
                tK = (zq.unsqueeze(1) - fit.class_mean.unsqueeze(0)) * inv          # [P, K, G]
                sinv_d = inv * (tK - ((tK @ U) * shrink) @ U.T)                     # [P, K, G]
                M0 = lcs.mahalanobis.view(-1, K).index_select(0, prow)              # [P, K]
                gate_p = lcs.pair_gate.index_select(0, pidx).unsqueeze(1)
                base_lh = model.lcs_pair_head(sc)
                if nset:
                    dlh_set = torch.zeros(P, nset, base_lh.size(-1), device=dev)
                for a in range(0, G, 4096):
                    b = min(G, a + 4096)
                    Mk = (M0.unsqueeze(2) + 2.0 * delta[:, None, a:b] * sinv_d[:, :, a:b]
                          + delta[:, None, a:b].square() * S_gg[a:b]).clamp_min(0.0)  # [P, K, g]
                    st = stat_from_M(Mk.transpose(1, 2))                                # [P, g, K]
                    st_c = torch.gather(st, 2, pcls.view(-1, 1, 1).expand(-1, b - a, 1)).squeeze(2)
                    gc_ = fit.class_gate.double().index_select(0, pcls).unsqueeze(1)
                    sc_k = torch.stack((gc_ * st_c, (gc_ * rf).expand_as(st_c), gc_.expand_as(st_c)), -1).float()
                    lh_k = gate_p.unsqueeze(1) * model.lcs_pair_head(sc_k)              # [P, g, 896]
                    d_lh = lh_k - (gate_p * base_lh).unsqueeze(1)
                    dl[:, a:b] += torch.einsum("pgc,pc->pg", d_lh, glh)
                    if nset:
                        m_ = (kog_t >= a) & (kog_t < b)
                        if bool(m_.any()):
                            dlh_set[:, m_] = d_lh[:, kog_t[m_] - a]
            # store: dl is (KO - base); report base - KO
            rr = torch.arange(s0, s1)
            for j, r in enumerate(rr.tolist()):
                which = 0 if r < len(cell_ix) else 1
                cidx = cell_ix[r % len(cell_ix)]
                out_lin[cidx, which] = -dl[j].cpu().numpy()
        # ---- validation only: exact head replay for the knockout-set genes
        if nset:
            torch.cuda.synchronize(); tr0 = time.perf_counter()
            with torch.no_grad():
                Rp = (R.unsqueeze(2) + dR_set).permute(0, 2, 1, 3).reshape(P * nset, S, -1)
                actp = act.repeat_interleave(nset, 0)
                lhp = None
                if is_g:
                    lhp = (lh.unsqueeze(1) + dlh_set).reshape(P * nset, -1)
                lk = []
                for q0 in range(0, P * nset, 512):
                    lk.append(head_logits(Rp[q0:q0 + 512], actp[q0:q0 + 512], None if lhp is None else lhp[q0:q0 + 512]))
                lk = torch.cat(lk).view(P, nset)
                l0_ng = head_logits(R, act, lh)  # same (no-grad) attention path as the replays
                drep = (l0_ng.unsqueeze(1) - lk).cpu().numpy()
            if c not in replay:
                replay[c] = np.zeros((len(cell_ix), 2, nset), np.float32)
            for j, r in enumerate(range(s0, s1)):
                which = 0 if r < len(cell_ix) else 1
                replay[c][r % len(cell_ix), which] = drep[j]
            torch.cuda.synchronize(); t_replay += time.perf_counter() - tr0
    log("class", c, "done", len(cell_ix), "cells")
torch.cuda.synchronize()
t_total = time.perf_counter() - t_start - t_replay
hook.remove()
log("checks", json.dumps(checks))
log(f"DS-LOO all {G} genes x {n} cells x 2 pairs: {t_total:.1f} s (+ validation replay {t_replay:.1f} s)")
dl_margin = out_lin[:, 0] - out_lin[:, 1]
save = dict(dl_margin=dl_margin.astype(np.float32), dl_logit=out_lin[:, 0])
for c, v in replay.items():
    save[f"replay_margin__{c}"] = v[:, 0] - v[:, 1]
cs = np.zeros((K, G), np.float32)
for c in range(K):
    ix = np.flatnonzero(cls == c)
    if len(ix):
        cs[c] = dl_margin[ix].mean(0)
save["class__dsloo_margin"] = cs
np.savez_compressed(str(RES) + "__dsloo.npz", **save)
json.dump(dict(case=case, arm=arm, checks=checks, seconds_all_genes=t_total, seconds_validation_replay=t_replay,
               n_cells=n, G=G, K=K, peak_gpu_gib=torch.cuda.max_memory_allocated() / 2**30),
          open(str(RES) + "__dsloo.json", "w"), indent=1)
log("saved")
