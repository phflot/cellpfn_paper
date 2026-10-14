"""Aggregate run_case.py / dsloo.py results into tables (CSV + markdown snippets) and per-class ranking CSVs.

No expression values are written: only attributions, knockout effects (logit units), ranks and gene names.
"""
import csv, glob, gzip, json, os, sys
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr, pearsonr

OUT = "/share/runs/2026/30-03-phflot-hashprompt/hashprompt_improvement_loop/gene_importance_20261008"
RES, TAB = f"{OUT}/results", f"{OUT}/tables"
os.makedirs(f"{TAB}/rankings", exist_ok=True)
CASE_ORDER = ["pbmc_l1_b10_s0", "pbmc_l1_b10_s1", "pbmc_l1_b100_s0", "zebra_dev_b10_s0", "kidney_core9_A_F0_count",
              "kidney_core9_A_F0_processed"]
METHOD_LABEL = {"gxi_margin": "grad x input", "gxi_trunk_margin": "grad x input, operator as shipped (no grad)",
                "ig16_margin": "IG m=16", "ig64_margin": "IG m=64", "op_ko_margin": "operator readout (KO form)",
                "op_mid_margin": "operator readout (midpoint form)", "dsloo_margin": "DS-LOO (linearised)",
                "dsloo_corr_margin": "DS-LOO + depth/detection correction",
                "dsloo_sq_margin": "DS-LOO support+query (router, depths, operator D/U fixed)"}
MARKERS = {
    "B": ["MS4A1", "CD79A"], "CD4 T": ["CD3E", "IL7R"], "CD8 T": ["CD3E", "CD8A"], "NK": ["NKG7", "GNLY"],
    "Mono": ["CD14", "LYZ", "FCGR3A"], "DC": ["FCER1A", "CLEC10A", "LILRA4"], "other": ["PPBP"],
    "other T": ["CD3E"],
    "epithelial cell of proximal tubule": ["LRP2", "CUBN"],
    "kidney loop of Henle cortical thick ascending limb epithelial cell": ["UMOD", "SLC12A1"],
    "kidney capillary endothelial cell": ["EMCN", "PECAM1"], "renal principal cell": ["AQP2"],
    "renal alpha-intercalated cell": ["SLC4A1"], "T cell": ["CD3E"], "natural killer cell": ["NKG7"],
    "mononuclear phagocyte": ["CD68"],
    # Zebra (human cortex): canonical markers chosen here (not given in the task)
    "Glia": ["GFAP", "AQP4", "SLC1A2", "OLIG2", "PLP1", "MBP"], "Immune cell": ["CX3CR1", "P2RY12", "C1QA", "PTPRC"],
    "Neural": ["SNAP25", "SYT1", "RBFOX3", "GAD1", "SLC17A7"], "Vascular cell": ["CLDN5", "FLT1", "PECAM1", "PDGFRB"],
}
SHORT = {"epithelial cell of proximal tubule": "PT", "kidney loop of Henle cortical thick ascending limb epithelial cell": "TAL",
         "kidney loop of Henle descending limb epithelial cell": "DTL", "mononuclear phagocyte": "MNP",
         "kidney capillary endothelial cell": "capillary EC", "natural killer cell": "NK", "renal principal cell": "PC",
         "renal alpha-intercalated cell": "alpha-IC"}


def short(c):
    return SHORT.get(c, c)


def sp(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5 or np.std(a[ok]) == 0 or np.std(b[ok]) == 0:
        return np.nan
    return spearmanr(a[ok], b[ok]).statistic


def load(case, arm):
    p = f"{RES}/{case}__{arm}.npz"
    if not os.path.exists(p):
        return None
    z = dict(np.load(p))
    z["json"] = json.load(open(f"{RES}/{case}__{arm}.json"))
    dp = f"{RES}/{case}__{arm}__dsloo.npz"
    if os.path.exists(dp):
        d = np.load(dp)
        z["dsloo"] = dict(d)
        z["dsloo_json"] = json.load(open(f"{RES}/{case}__{arm}__dsloo.json"))
        z["class__dsloo_margin"] = d["class__dsloo_margin"]
        cl = np.zeros_like(d["class__dsloo_margin"])
        for c in range(cl.shape[0]):
            ix = np.flatnonzero(z["cls"] == c)
            if len(ix):
                cl[c] = d["dl_logit"][ix].mean(0)
        z["class__dsloo_logit"] = cl
    cp = f"{RES}/{case}__{arm}__dsloo_corr.npz"
    if os.path.exists(cp):
        d2 = np.load(cp)
        z["dsloo_corr"] = dict(d2)
        z["dsloo_corr_json"] = json.load(open(f"{RES}/{case}__{arm}__dsloo_corr.json"))
        z["class__dsloo_corr_margin"] = d2["class__dsloo_corr_margin"]
    sqp = f"{RES}/{case}__{arm}__dsloo_sq.npz"
    if os.path.exists(sqp):
        d3 = np.load(sqp)
        z["dsloo_sq"] = dict(d3)
        z["dsloo_sq_json"] = json.load(open(f"{RES}/{case}__{arm}__dsloo_sq.json"))
        z["class__dsloo_sq_margin"] = d3["class__dsloo_sq_margin"]
    dp2 = f"{RES}/{case}__{arm}__dsloo_del.npz"
    if os.path.exists(dp2):
        for k_, v_ in np.load(dp2).items():
            if k_.startswith(("del__", "group__")):
                z[k_] = v_
    ep = f"{RES}/{case}__{arm}__dsloo_extra.npz"
    if os.path.exists(ep):
        z["dsloo_extra"] = dict(np.load(ep))
    return z


def md_table(rows, cols, path=None, floatfmt="{:.2f}"):
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out = []
        for c in cols:
            v = r.get(c, "")
            out.append(floatfmt.format(v) if isinstance(v, (float, np.floating)) and np.isfinite(v) else
                       ("–" if isinstance(v, (float, np.floating)) else str(v)))
        lines.append("| " + " | ".join(out) + " |")
    s = "\n".join(lines) + "\n"
    if path:
        open(path, "w").write(s)
    return s


def write_csv(path, rows):
    if not rows:
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)


data = {(c, a): load(c, a) for c in CASE_ORDER for a in ("G", "C")}
data = {k: v for k, v in data.items() if v is not None}
print("loaded", sorted(data))

faith_rows, faith_class_rows, del_rows, group_rows, time_rows, ig_rows, ds_rows = [], [], [], [], [], [], []
marker_rows, top10_rows = [], []
for (case, arm), z in data.items():
    names = list(z["class_names"])
    K = len(names)
    sym = z["symbols"]
    cls, m0 = z["cls"], z["margin0"]
    methods = [m for m in METHOD_LABEL if f"class__{m}" in z]
    # ---------------- rankings CSV (top 200 + bottom 50 per method/target/class)
    rk = []
    for key in sorted(k for k in z if isinstance(k, str) and k.startswith("class__")):
        mname = key[len("class__"):]
        cs = z[key]
        for c in range(K):
            if not np.any(cls == c):
                continue
            o = np.argsort(-cs[c])
            for r_, g in enumerate(o[:200]):
                rk.append(dict(case=case, arm=arm, method=mname, cls=names[c], rank=r_ + 1, gene=sym[g],
                               score=f"{cs[c, g]:.6g}"))
            for r_, g in enumerate(o[::-1][:50]):
                rk.append(dict(case=case, arm=arm, method=mname, cls=names[c], rank=-(r_ + 1), gene=sym[g],
                               score=f"{cs[c, g]:.6g}"))
    with gzip.open(f"{TAB}/rankings/{case}__{arm}.csv.gz", "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["case", "arm", "method", "cls", "rank", "gene", "score"])
        w.writeheader(); w.writerows(rk)
    # ---------------- faithfulness vs exact knockouts
    per_m = defaultdict(lambda: defaultdict(list))
    for c in range(K):
        if f"ko_genes__{c}" not in z:
            continue
        genes = z[f"ko_genes__{c}"]
        Eq = z[f"ko_q_margin__{c}"]          # [genes, cells]
        Esq = z[f"ko_sq_margin__{c}"]
        eq, esq = Eq.mean(1), np.nanmean(Esq, 1) if np.isfinite(Esq).any() else np.full(len(genes), np.nan)
        cells_c = np.flatnonzero(cls == c)
        ko_best = np.sort(eq)[::-1][:20].mean()
        for m in methods:
            a = z[f"class__{m}"][c, genes]
            if m == "dsloo_margin":
                ca_ = z["dsloo"]["dl_margin"][cells_c][:, genes]
            elif m == "dsloo_corr_margin":
                ca_ = z["dsloo_corr"]["dl_margin"][cells_c][:, genes]
            elif m == "dsloo_sq_margin":
                ca_ = z["dsloo_sq"]["dl_margin"][cells_c][:, genes]
            else:
                ca_ = z.get(f"cellattr__{m}__{c}")
            cell_rho = [sp(ca_[i], Eq[:, i]) for i in range(Eq.shape[1])] if ca_ is not None else []
            cell_rho_sq = [sp(ca_[i], Esq[:, i]) for i in range(Esq.shape[1])] if ca_ is not None else []
            top = np.argsort(-z[f"class__{m}"][c])[:20]
            inset = np.isin(genes, top)
            r = dict(case=case, arm=arm, method=m, cls=names[c], n_genes=len(genes), n_cells=Eq.shape[1],
                     rho_class_q=sp(a, eq), rho_class_sq=sp(a, esq),
                     rho_cell_q_median=float(np.nanmedian(cell_rho)) if len(cell_rho) else np.nan,
                     rho_cell_sq_median=float(np.nanmedian(cell_rho_sq)) if len(cell_rho_sq) else np.nan,
                     top20_mean_ko_q=float(eq[inset].mean()) if inset.any() else np.nan,
                     top20_in_set=int(inset.sum()), ko_best20_mean_q=float(ko_best))
            faith_class_rows.append(r)
            for k_ in ("rho_class_q", "rho_class_sq", "rho_cell_q_median", "rho_cell_sq_median", "top20_mean_ko_q"):
                per_m[m][k_].append(r[k_])
            per_m[m]["frac_best"].append(r["top20_mean_ko_q"] / ko_best if ko_best > 0 else np.nan)
        # random / low reference effects
        tags = z[f"ko_tags__{c}"]
        rnd = np.array(["random_expressed" in t for t in tags])
        per_m["_ref"]["random_mean_ko_q"].append(eq[rnd].mean() if rnd.any() else np.nan)
        for low in ("low:ig64_margin", "low:op_ko_margin"):
            lw = np.array([low in t for t in tags])
            per_m["_ref"][f"{low}_mean_ko_q"].append(eq[lw].mean() if lw.any() else np.nan)
        per_m["_ref"]["ko_best20_mean_q"].append(ko_best)
        per_m["_ref"]["abs_ko_median_q"].append(np.median(np.abs(Eq)))
        per_m["_ref"]["sq_minus_q_median_abs"].append(np.nanmedian(np.abs(Esq - Eq)))
    ref = {k: float(np.nanmean(v)) for k, v in per_m["_ref"].items()}
    for m in methods:
        faith_rows.append(dict(case=case, arm=arm, method=m, label=METHOD_LABEL[m],
                               rho_class_q=float(np.nanmedian(per_m[m]["rho_class_q"])),
                               rho_class_sq=float(np.nanmedian(per_m[m]["rho_class_sq"])),
                               rho_cell_q=float(np.nanmedian(per_m[m]["rho_cell_q_median"])),
                               rho_cell_sq=float(np.nanmedian(per_m[m]["rho_cell_sq_median"])),
                               top20_mean_ko_q=float(np.nanmean(per_m[m]["top20_mean_ko_q"])),
                               frac_of_ko_best20=float(np.nanmean(per_m[m]["frac_best"])),
                               random20_mean_ko_q=ref.get("random_mean_ko_q", np.nan),
                               low_ig64_mean_ko_q=ref.get("low:ig64_margin_mean_ko_q", np.nan),
                               low_opko_mean_ko_q=ref.get("low:op_ko_margin_mean_ko_q", np.nan),
                               median_base_margin=float(np.median(m0)),
                               noise_floor=z["json"]["diag"].get("ko_noise_floor_margin_maxabs", np.nan)))
    # ---------------- deletion curves
    kgrid = list(z["kgrid"])
    dk = defaultdict(list)
    for key in [k for k in z if isinstance(k, str) and k.startswith("del__")]:
        _, c, oname = key.split("__", 2)
        c = int(c)
        v = z[key]  # [k, cells]
        base = m0[cls == c][None, :]
        oname_g = oname.rsplit("_", 1)[0] if "random_expressed" in oname else oname
        dk[oname_g].append((v, (v > base)))
    for oname, lst in sorted(dk.items()):
        drop = np.concatenate([v for v, _ in lst], 1)
        flip = np.concatenate([f for _, f in lst], 1)
        r = dict(case=case, arm=arm, ordering=oname)
        for kk in (1, 5, 10, 20, 50):
            if kk in kgrid:
                i = kgrid.index(kk)
                r[f"drop@{kk}"] = float(drop[i].mean())
        r["flip@10"] = float(flip[kgrid.index(10)].mean())
        r["flip@50"] = float(flip[kgrid.index(50)].mean())
        r["auc_drop_k1_50"] = float(np.trapezoid(drop.mean(1), kgrid) / (kgrid[-1] - kgrid[0]))
        r["median_base_margin"] = float(np.median(m0))
        del_rows.append(r)
    # ---------------- group knockouts (support + query, top-50)
    gk = defaultdict(list)
    for key in [k for k in z if isinstance(k, str) and k.startswith("group__")]:
        _, c, sname = key.split("__", 2)
        c = int(c)
        sname_g = "random_expressed" if "random_expressed" in sname else sname
        gk[sname_g].append((z[key], z[key] > m0[cls == c]))
    for sname, lst in sorted(gk.items()):
        dr = np.concatenate([v for v, _ in lst]); fl = np.concatenate([f for _, f in lst])
        group_rows.append(dict(case=case, arm=arm, set=sname, mean_drop_top50_sq=float(dr.mean()),
                               flip_top50_sq=float(fl.mean())))
    # ---------------- timing
    t = z["json"]["timing"]
    G = t["G"]
    row = dict(case=case, arm=arm, G=G, Q=t["Q"], K=t["K"], cells=t["n_cells"],
               gxi_s=t.get("gxi"), ig16_s=t.get("ig16"), ig64_s=t.get("ig64"),
               op_readout_s=t.get("operator_readout"),
               dsloo_s=z.get("dsloo_json", {}).get("seconds_all_genes"),
               dsloo_corr_s=z.get("dsloo_corr_json", {}).get("seconds"),
               dsloo_sq_s=z.get("dsloo_sq_json", {}).get("seconds"),
               naive_ko_full_forward_s=t["naive_single_ko_full_forward_seconds"],
               naive_ko_all_genes_q_h=t["naive_exact_ko_all_genes_query_only_hours"],
               naive_ko_all_genes_sq_h=t["naive_exact_ko_all_genes_support_query_hours"],
               restricted_ko_all_genes_q_h=t["ko_query_only_seconds_per_gene_class"] * K * G / 3600,
               peak_gib=t["peak_gpu_gib"])
    time_rows.append(row)
    # ---------------- IG diagnostics
    dg = z["json"]["diag"]
    igr = dict(case=case, arm=arm, **{k: dg[k] for k in dg})
    if "class__ig64_margin" in z:
        ov, rh = [], []
        for c in range(K):
            if not np.any(cls == c):
                continue
            a16, a64 = z["class__ig16_margin"][c], z["class__ig64_margin"][c]
            t16, t64 = set(np.argsort(-a16)[:20]), set(np.argsort(-a64)[:20])
            ov.append(len(t16 & t64) / 20)
            u_ = np.union1d(np.argsort(-a64)[:200], np.argsort(a64)[:50])
            rh.append(sp(a16[u_], a64[u_]))
        igr["ig16_ig64_top20_overlap"] = float(np.mean(ov))
        igr["ig16_ig64_rho_top250"] = float(np.mean(rh))
    ig_rows.append(igr)
    # ---------------- DS-LOO vs exact knockouts
    if "dsloo" in z:
        dsl = z["dsloo"]
        rr = defaultdict(list)
        for c in range(K):
            if f"ko_genes__{c}" not in z:
                continue
            genes = z[f"ko_genes__{c}"]
            Eq = z[f"ko_q_margin__{c}"]
            cells_c = np.flatnonzero(cls == c)
            lin = dsl["dl_margin"][cells_c][:, genes].T   # [genes, cells]
            rep = dsl[f"replay_margin__{c}"].T if f"replay_margin__{c}" in dsl else None
            ex = z.get("dsloo_extra", {})
            if f"genes__{c}" in ex and len(ex[f"genes__{c}"]):
                lin_all = np.concatenate((lin, dsl["dl_margin"][cells_c][:, ex[f"genes__{c}"]].T))
                E_all = np.concatenate((Eq, ex[f"ko_q_margin__{c}"]))
                rr["n_extra_genes"].append(len(ex[f"genes__{c}"]))
            else:
                lin_all, E_all = lin, Eq
            rr["pearson_lin_vs_exact_incl_dsloo_top"].append(pearsonr(lin_all.ravel(), E_all.ravel()).statistic)
            rr["rho_class_lin_incl_dsloo_top"].append(sp(lin_all.mean(1), E_all.mean(1)))
            rr["rho_cell_lin_incl_dsloo_top"].append(np.nanmedian([sp(lin_all[:, i], E_all[:, i]) for i in range(E_all.shape[1])]))
            if "dsloo_corr" in z:
                cor = z["dsloo_corr"]["dl_margin"][cells_c][:, genes].T
                rr["rel_err_corr"].append(np.linalg.norm(cor.ravel() - Eq.ravel()) / np.linalg.norm(Eq.ravel()))
                rr["pearson_corr_vs_exact"].append(pearsonr(cor.ravel(), Eq.ravel()).statistic)
                rr["rho_cell_corr"].append(np.nanmedian([sp(cor[:, i], Eq[:, i]) for i in range(Eq.shape[1])]))
            x, y_ = lin.ravel(), Eq.ravel()
            rr["pearson_lin_vs_exact"].append(pearsonr(x, y_).statistic)
            rr["spearman_lin_vs_exact"].append(sp(x, y_))
            rr["rel_err_lin"].append(np.linalg.norm(x - y_) / np.linalg.norm(y_))
            rr["rho_class_lin"].append(sp(lin.mean(1), Eq.mean(1)))
            if rep is not None:
                rr["rel_err_replay_vs_exact"].append(np.linalg.norm(rep.ravel() - y_) / np.linalg.norm(y_))
                rr["rel_err_lin_vs_replay"].append(np.linalg.norm(x - rep.ravel()) / np.linalg.norm(rep.ravel()))
            gx = z.get(f"cellattr__gxi_margin__{c}")
            if gx is not None:
                rr["rel_err_gxi"].append(np.linalg.norm(gx.T.ravel() - y_) / np.linalg.norm(y_))
                rr["pearson_gxi_vs_exact"].append(pearsonr(gx.T.ravel(), y_).statistic)
            ig = z.get(f"cellattr__ig64_margin__{c}", z.get(f"cellattr__ig16_margin__{c}"))
            if ig is not None:
                rr["rel_err_ig"].append(np.linalg.norm(ig.T.ravel() - y_) / np.linalg.norm(y_))
                rr["pearson_ig_vs_exact"].append(pearsonr(ig.T.ravel(), y_).statistic)
        ds_rows.append(dict(case=case, arm=arm, **{k: float(np.nanmedian(v)) for k, v in rr.items()},
                            seconds=z["dsloo_json"]["seconds_all_genes"],
                            corr_seconds=z.get("dsloo_corr_json", {}).get("seconds", np.nan),
                            R_check=z["dsloo_json"]["checks"]["max_abs_R_vs_model"],
                            logit_check=z["dsloo_json"]["checks"]["max_abs_logit_vs_model"]))
    # ---------------- sanity: top-10 and marker ranks
    show = [m for m in ("dsloo_corr_margin", "ig64_margin", "ig16_margin", "dsloo_margin", "op_ko_margin", "gxi_margin",
                        "ig64_logit", "ig16_logit", "dsloo_logit", "gxi_logit") if f"class__{m}" in z]
    for a_, b_ in (("ig64_margin", "ig16_margin"), ("ig64_logit", "ig16_logit")):
        if a_ in show and b_ in show:
            show.remove(b_)
    for c in range(K):
        if not np.any(cls == c):
            continue
        for m in [m_ for m_ in show if m_.endswith("_margin")]:
            o = np.argsort(-z[f"class__{m}"][c])
            top10_rows.append(dict(case=case, arm=arm, cls=short(names[c]), method=m,
                                   top10=", ".join(sym[o[:10]])))
        for mk in MARKERS.get(names[c], []):
            hit = np.flatnonzero(sym == mk)
            r = dict(case=case, arm=arm, cls=short(names[c]), marker=mk)
            for m in show:
                if len(hit) == 0:
                    r[m] = "not in panel"
                else:
                    o = np.argsort(-z[f"class__{m}"][c])
                    r[m] = int(np.flatnonzero(o == hit[0])[0]) + 1
            marker_rows.append(r)

sq_rows = []
for (case, arm), z in data.items():
    if "dsloo_sq" not in z:
        continue
    rr = defaultdict(list)
    for c in range(len(z["class_names"])):
        if f"ko_genes__{c}" not in z:
            continue
        g, m_ = z[f"ko_genes__{c}"], z[f"ko_sqmask__{c}"]
        E = z[f"ko_sq_margin__{c}"][m_]
        ix = np.flatnonzero(z["cls"] == c)
        A = z["dsloo_sq"]["dl_margin"][ix][:, g[m_]].T
        Aq = (z["dsloo_corr"] if "dsloo_corr" in z else z["dsloo"])["dl_margin"][ix][:, g[m_]].T
        rr["pearson_sq"].append(pearsonr(A.ravel(), E.ravel()).statistic)
        rr["rel_err_sq"].append(np.linalg.norm(A - E) / np.linalg.norm(E))
        rr["rho_class_sq"].append(sp(A.mean(1), E.mean(1)))
        rr["rho_cell_sq"].append(np.nanmedian([sp(A[:, i], E[:, i]) for i in range(E.shape[1])]))
        rr["rho_class_sq_by_query_dsloo"].append(sp(Aq.mean(1), E.mean(1)))
        rr["n_genes"].append(len(E))
    sq_rows.append(dict(case=case, arm=arm, **{k: float(np.nanmedian(v)) for k, v in rr.items()},
                        seconds=z["dsloo_sq_json"]["seconds"]))
write_csv(f"{TAB}/dsloo_sq_vs_exact.csv", sq_rows)
write_csv(f"{TAB}/faithfulness_summary.csv", faith_rows)
write_csv(f"{TAB}/faithfulness_per_class.csv", faith_class_rows)
write_csv(f"{TAB}/deletion_curves.csv", del_rows)
write_csv(f"{TAB}/group_knockout_top50.csv", group_rows)
write_csv(f"{TAB}/timing.csv", time_rows)
write_csv(f"{TAB}/ig_diagnostics.csv", ig_rows)
write_csv(f"{TAB}/dsloo_vs_exact.csv", ds_rows)
write_csv(f"{TAB}/marker_ranks.csv", marker_rows)
write_csv(f"{TAB}/top10_per_class.csv", top10_rows)

# full-delete-curve CSV (mean over classes and cells per k) for plotting
curve = []
for (case, arm), z in data.items():
    kgrid = list(z["kgrid"])
    acc = defaultdict(list)
    for key in [k for k in z if isinstance(k, str) and k.startswith("del__")]:
        _, c, oname = key.split("__", 2)
        og = oname.rsplit("_", 1)[0] if "random_expressed" in oname else oname
        acc[og].append(z[key])
    for og, lst in acc.items():
        mean = np.concatenate(lst, 1).mean(1)
        for kk, v in zip(kgrid, mean):
            curve.append(dict(case=case, arm=arm, ordering=og, k=kk, mean_margin_drop=float(v)))
write_csv(f"{TAB}/deletion_curves_long.csv", curve)

# stability: PBMC draws and G vs C
stab = []
def top20(z, m, c):
    return set(np.argsort(-z[f"class__{m}"][c])[:20])
for m in ("dsloo_corr_margin", "dsloo_margin", "ig16_margin", "op_ko_margin", "gxi_margin"):
    for arm in ("G", "C"):
        pairs = [("pbmc_l1_b10_s0", "pbmc_l1_b10_s1"), ("pbmc_l1_b10_s0", "pbmc_l1_b100_s0")]
        for a, b in pairs:
            if (a, arm) in data and (b, arm) in data and f"class__{m}" in data[(a, arm)] and f"class__{m}" in data[(b, arm)]:
                za, zb = data[(a, arm)], data[(b, arm)]
                assert list(za["symbols"]) == list(zb["symbols"])
                ov = [len(top20(za, m, c) & top20(zb, m, c)) / 20 for c in range(len(za["class_names"]))
                      if np.any(za["cls"] == c) and np.any(zb["cls"] == c)]
                stab.append(dict(kind="draw", method=m, arm=arm, a=a, b=b, top20_overlap=float(np.mean(ov))))
    for case in CASE_ORDER:
        if (case, "G") in data and (case, "C") in data and f"class__{m}" in data[(case, "G")] and f"class__{m}" in data[(case, "C")]:
            zg, zc = data[(case, "G")], data[(case, "C")]
            ov = [len(top20(zg, m, c) & top20(zc, m, c)) / 20 for c in range(len(zg["class_names"]))
                  if np.any(zg["cls"] == c) and np.any(zc["cls"] == c)]
            stab.append(dict(kind="G_vs_C", method=m, arm="G/C", a=case, b=case, top20_overlap=float(np.mean(ov))))
write_csv(f"{TAB}/stability.csv", stab)
print("faith rows", len(faith_rows), "del", len(del_rows), "timing", len(time_rows), "ds", len(ds_rows))
