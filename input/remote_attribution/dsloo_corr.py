"""First-order correction of DS-LOO for the two row-level couplings it holds fixed: the query depth (count mode:
removing x_g lowers d by x_g, which shifts every gene's log1p-CP10k value and the log-depth feature) and the detected
fraction (-1/G when an expressed gene is removed).  One backward per (cell, pred/runner pair) with d and the detected
fraction as leaves (differentiable operator for G1v2'):
    Delta l_g (base - KO)  +=  dl/dd * x_g  +  dl/dqdet * 1[x_g > 0] / G
usage: dsloo_corr.py <case> <arm>  -> results/<case>__<arm>__dsloo_corr.npz (corrected margins, class scores, timing)
"""
import json, os, sys, time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cellpfn_attr as ca  # noqa: E402

case, arm = sys.argv[1], sys.argv[2]
dev = ca.gpu_setup()
torch.backends.cuda.matmul.allow_tf32 = False
RES = ca.OUT / "results" / f"{case}__{arm}"
res = np.load(str(RES) + ".npz")
dsl = np.load(str(RES) + "__dsloo.npz")
model, info = ca.load_model(arm, dev)
data = ca.case_inputs(case)
K, G, mode = len(data.class_names), data.support.shape[1], data.mode
xs = torch.as_tensor(data.support, device=dev)
ys = torch.as_tensor(data.support_labels, device=dev)
with torch.no_grad():
    fitted = ca.fit_support(model, xs, ys, K, mode)
sel, cls, pred, run = res["sel"], res["cls"], res["pred"], res["run"]
n = len(sel)
xq = torch.as_tensor(data.query[sel], device=dev)
rows = torch.cat((xq, xq))
rcls = torch.cat((torch.as_tensor(pred, device=dev), torch.as_tensor(run, device=dev)))
torch.cuda.synchronize(); t0 = time.perf_counter()
model.train()
gd = torch.zeros(2 * n, device=dev); gq = torch.zeros(2 * n, device=dev)
for s in range(0, 2 * n, 256):
    e = min(2 * n, s + 256)
    X = rows[s:e]
    d = (X.sum(1).clamp_min(1.0) if mode == "count" else X.new_zeros(e - s)).detach().requires_grad_(mode == "count")
    q = (X > 0).float().mean(1).detach().requires_grad_(True)
    with torch.enable_grad():
        lg = ca.score_pairs(model, fitted, X, torch.arange(e - s, device=dev), rcls[s:e], depths=d, qdet=q,
                            differentiable_operator=model.gene_gene_operator != "none")
        leaves = [d, q] if mode == "count" else [q]
        gr = torch.autograd.grad(lg.sum(), leaves)
    if mode == "count":
        gd[s:e], gq[s:e] = gr[0], gr[1]
    else:
        gq[s:e] = gr[0]
model.eval()
with torch.no_grad():
    x = xq
    det = (x > 0).float() / G
    # base - KO = -(Delta l) with Delta d = -x_g, Delta qdet = -1[x_g>0]/G  ->  + dl/dd * x_g + dl/dqdet * det
    corr_p = gd[:n, None] * x + gq[:n, None] * det
    corr_r = gd[n:, None] * x + gq[n:, None] * det
    corr = (corr_p - corr_r).cpu().numpy()
torch.cuda.synchronize(); secs = time.perf_counter() - t0
dl = dsl["dl_margin"] + corr
cs = np.zeros((K, G), np.float32)
for c in range(K):
    ix = np.flatnonzero(cls == c)
    if len(ix):
        cs[c] = dl[ix].mean(0)
np.savez_compressed(str(RES) + "__dsloo_corr.npz", dl_margin=dl.astype(np.float32), class__dsloo_corr_margin=cs)
json.dump(dict(case=case, arm=arm, seconds=secs, median_abs_dl_dd=float(gd.abs().median()),
               median_abs_dl_dqdet=float(gq.abs().median())), open(str(RES) + "__dsloo_corr.json", "w"), indent=1)
print(case, arm, f"correction pass {secs:.1f} s", flush=True)
