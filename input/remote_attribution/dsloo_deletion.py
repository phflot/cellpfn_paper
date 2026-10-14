"""Deletion curves (query only) and support+query group knockout (top-50) for the DS-LOO orderings, with exactly the
protocol of run_case.py (same cells, KGRID, fp32 eval, model's own depth; class ranking and each cell's own ranking).
usage: dsloo_deletion.py <case> <arm>  -> results/<case>__<arm>__dsloo_del.npz
"""
import os, sys
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cellpfn_attr as ca  # noqa: E402

case, arm = sys.argv[1], sys.argv[2]
dev = ca.gpu_setup()
torch.backends.cuda.matmul.allow_tf32 = False
RES = ca.OUT / "results" / f"{case}__{arm}"
res = np.load(str(RES) + ".npz")
src = str(RES) + ("__dsloo_corr.npz" if os.path.exists(str(RES) + "__dsloo_corr.npz") else "__dsloo.npz")
dsl = np.load(src)
key = "class__dsloo_corr_margin" if "class__dsloo_corr_margin" in dsl.files else "class__dsloo_margin"
model, info = ca.load_model(arm, dev)
data = ca.case_inputs(case)
K, mode = len(data.class_names), data.mode
xs = torch.as_tensor(data.support, device=dev)
ys = torch.as_tensor(data.support_labels, device=dev)
with torch.no_grad():
    fitted = ca.fit_support(model, xs, ys, K, mode)
sel, cls, pred, run, KGRID = res["sel"], res["cls"], res["pred"], res["run"], list(res["kgrid"])
xq = torch.as_tensor(data.query[sel], device=dev)
pred_t, run_t = torch.as_tensor(pred, device=dev), torch.as_tensor(run, device=dev)
dlm = torch.as_tensor(dsl["dl_margin"], device=dev)


def margins(X, prd, rn, fo=None, chunk=512):
    fo = fitted if fo is None else fo
    out = []
    with torch.inference_mode():
        for s in range(0, int(X.size(0)), chunk):
            Xb = X[s:s + chunk]; r = int(Xb.size(0)); ar = torch.arange(r, device=dev)
            lg = ca.score_pairs(model, fo, Xb, torch.cat((ar, ar)), torch.cat((prd[s:s + r], rn[s:s + r])))
            out.append(lg[:r] - lg[r:])
    return torch.cat(out)


base = margins(xq, pred_t, run_t)
save = {"source": np.asarray(os.path.basename(src) + ":" + key)}
for c in range(K):
    ix_np = np.flatnonzero(cls == c)
    if len(ix_np) < 3:
        continue
    ix = torch.as_tensor(ix_np, device=dev)
    nc = len(ix_np)
    Xc = xq[ix]
    orders = {"class:dsloo": torch.as_tensor(np.argsort(-dsl[key][c])[:max(KGRID)].copy(), device=dev)
              .unsqueeze(0).expand(nc, -1),
              "cell:dsloo": torch.argsort(dlm[ix], dim=1, descending=True)[:, :max(KGRID)]}
    for oname, top in orders.items():
        X = Xc.repeat(len(KGRID), 1)
        for ki, k in enumerate(KGRID):
            X[ki * nc:(ki + 1) * nc].scatter_(1, top[:, :k], 0.0)
        m = margins(X, pred_t[ix].repeat(len(KGRID)), run_t[ix].repeat(len(KGRID)))
        save[f"del__{c}__{oname}"] = (base[ix].repeat(len(KGRID)) - m).reshape(len(KGRID), nc).cpu().numpy()
    gt = torch.as_tensor(np.argsort(-dsl[key][c])[:50].copy(), device=dev)
    xs2 = xs.clone(); xs2[:, gt] = 0.0
    with torch.no_grad():
        f2 = ca.fit_support(model, xs2, ys, K, mode)
    X = Xc.clone(); X[:, gt] = 0.0
    save[f"group__{c}__dsloo"] = (base[ix] - margins(X, pred_t[ix], run_t[ix], f2)).cpu().numpy()
np.savez_compressed(str(RES) + "__dsloo_del.npz", **save)
print(case, arm, "dsloo deletion done", flush=True)
