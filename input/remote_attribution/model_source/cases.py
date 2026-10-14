"""Reader for the exported real-cell cases (realcell_baselines_20261008).  numpy (+ scipy / anndata if present) only.

Layout (written by code/export_cases.py; format described in cases/README.md):

    cases/<panel>/READY                     panel finished and verified (JSON summary)
    cases/<panel>/index.json                one entry per case: case_id, group, budget, draw, file sha256s
    cases/<panel>/<case_id>.npz             expression (CSR), cells, support labels, genes
    cases/<panel>/<case_id>.json            case metadata, provenance and the equality checks that passed
    cases_labels/<panel>/<case_id>.npz      QUERY LABELS (scoring only; never pass them to a method)

Panels: pbmc, kidney, zebra (processed values only), zebra_counts (reconstructed counts).

Typical use in a method track::

    import sys; sys.path.insert(0, "<campaign>/code"); import cases
    for entry in cases.list_cases("pbmc"):
        case = cases.load_case("pbmc", entry["case_id"])
        Xs, ys = case.support_X(), case.support_labels          # fit on these only
        Xq = case.query_X()                                      # predict these, in this row order
        ...
    # scoring (separate step):
    obs_ids, labels = cases.load_query_labels("pbmc", case_id)  # same order as case.query_obs_ids

Rows: support cells first (in the benchmark's order), then query cells (in the benchmark's order).
Columns: genes in the source dataset's order with their real identifiers (``var_symbol``, ``var_ensembl``).
``var_benchmark_column[j]`` is the column of gene j in the benchmark's (gene-permuted) input, i.e.
``X[:, argsort(var_benchmark_column)]`` is the benchmark's column order.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases"
LABELS = ROOT / "cases_labels"
PANELS = ("pbmc", "kidney", "zebra", "zebra_counts")

ARRAY_KEYS = ("X_data", "X_indices", "X_indptr", "X_shape", "obs_id", "split", "support_label", "donor", "study",
              "n_counts", "var_symbol", "var_ensembl", "var_ensembl_source", "var_benchmark_column")


def sha256_file(path, chunk=8 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def ready(panel: str) -> bool:
    return (CASES / panel / "READY").exists()


def list_cases(panel: str | None = None, *, require_ready: bool = True) -> list[dict]:
    """Index entries (case_id, panel, group, group_kind, support_budget, draw, feature_panel, files ...)."""
    out = []
    for p in ([panel] if panel else PANELS):
        if require_ready and not ready(p):
            raise FileNotFoundError(f"panel {p} is not READY ({CASES / p / 'READY'} missing)")
        index = CASES / p / "index.json"
        if index.exists():
            out += json.loads(index.read_text())["cases"]
    return out


class Case:
    """One exported case.  ``X`` is a CSR matrix (scipy) if scipy is importable, else the raw CSR arrays."""

    def __init__(self, panel: str, case_id: str, *, verify: bool = True):
        self.panel, self.case_id = panel, case_id
        npz, meta = CASES / panel / f"{case_id}.npz", CASES / panel / f"{case_id}.json"
        self.meta = json.loads(meta.read_text())
        if verify and sha256_file(npz) != self.meta["files"]["npz_sha256"]:
            raise ValueError(f"{npz} does not match the sha256 recorded in {meta}")
        with np.load(npz, allow_pickle=False) as d:
            a = {k: d[k] for k in ARRAY_KEYS}
        self._csr = (a["X_data"], a["X_indices"], a["X_indptr"], tuple(int(v) for v in a["X_shape"]))
        self.obs_ids = a["obs_id"]
        self.split = a["split"]
        self.support_mask = self.split == "support"
        self.query_mask = self.split == "query"
        if not (self.support_mask.sum() + self.query_mask.sum() == len(self.split)):
            raise ValueError("split column holds values other than support/query")
        if not (np.all(np.flatnonzero(self.support_mask) < np.flatnonzero(self.query_mask).min())):
            raise ValueError("support rows are not first")
        self.support_labels = a["support_label"][self.support_mask].astype(np.int64)
        if np.any(a["support_label"][self.query_mask] != -1):
            raise ValueError("query rows carry labels in the case file")
        self.donors, self.studies, self.n_counts = a["donor"], a["study"], a["n_counts"]
        self.var_symbol, self.var_ensembl = a["var_symbol"], a["var_ensembl"]
        self.var_ensembl_source, self.var_benchmark_column = a["var_ensembl_source"], a["var_benchmark_column"]
        self.class_names = list(self.meta["class_names"])
        self.class_ids = list(self.meta["class_ids"])
        self.value_type = self.meta["value_type"]          # raw_counts | reconstructed_counts | log1p_cp10k_supplied
        self.species = self.meta["species"]

    # ---------------------------------------------------------------- matrices
    @property
    def X(self):
        try:
            from scipy import sparse
        except ImportError:  # pragma: no cover
            return self._csr
        data, indices, indptr, shape = self._csr
        return sparse.csr_matrix((data, indices, indptr), shape=shape)

    def support_X(self):
        return self.X[np.flatnonzero(self.support_mask)]

    def query_X(self):
        return self.X[np.flatnonzero(self.query_mask)]

    @property
    def support_obs_ids(self):
        return self.obs_ids[self.support_mask]

    @property
    def query_obs_ids(self):
        return self.obs_ids[self.query_mask]

    def benchmark_order(self) -> np.ndarray:
        """Column order that reproduces the benchmark's (gene-permuted) input: X[:, benchmark_order()]."""
        return np.argsort(self.var_benchmark_column, kind="stable")

    def to_anndata(self):
        """AnnData with obs (obs_id, split, support_label [-1 for query], donor, study, n_counts) and var
        (gene_symbol index made unique, ensembl_id, ...).  Query labels are NOT included."""
        import anndata as ad
        import pandas as pd
        obs = pd.DataFrame(dict(split=self.split, donor=self.donors, study=self.studies, n_counts=self.n_counts),
                           index=pd.Index(self.obs_ids, name="obs_id"))
        lab = np.full(len(self.split), -1, dtype=np.int64)
        lab[self.support_mask] = self.support_labels
        obs["support_label"] = lab
        names = np.full(len(self.split), "", dtype=object)
        names[self.support_mask] = [self.class_names[i] for i in self.support_labels]
        obs["support_label_name"] = names
        var = pd.DataFrame(dict(gene_symbol=self.var_symbol, ensembl_id=self.var_ensembl,
                                ensembl_id_source=self.var_ensembl_source,
                                benchmark_column=self.var_benchmark_column))
        var.index = pd.Index(_make_unique(self.var_symbol.tolist()), name="gene")
        adata = ad.AnnData(X=self.X, obs=obs, var=var)
        adata.uns["case"] = json.dumps({k: v for k, v in self.meta.items() if k in (
            "case_id", "panel", "group", "group_kind", "support_budget", "draw", "draw_kind", "feature_panel",
            "species", "value_type", "class_names", "class_ids")})
        return adata


def _make_unique(names: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}-{seen[n]}")
        else:
            seen[n] = 0
            out.append(n)
    return out


def load_case(panel: str, case_id: str, *, verify: bool = True) -> Case:
    return Case(panel, case_id, verify=verify)


def load_query_labels(panel: str, case_id: str) -> tuple[np.ndarray, np.ndarray]:
    """(query obs ids, integer query labels) for SCORING only; same order as Case.query_obs_ids."""
    with np.load(LABELS / panel / f"{case_id}.npz", allow_pickle=False) as d:
        return d["query_obs_id"], d["query_label"].astype(np.int64)


def balanced_accuracy(labels, predictions, n_classes: int) -> float:
    """Cell-level balanced accuracy as the benchmark computes it (evaluation_metrics.classification_metrics_from_logits):
    mean recall over ALL n_classes; every class must occur in ``labels`` (fraction, 0-1).  Kidney pt_sex is scored
    at donor level in the benchmark, which this helper does not do."""
    labels, predictions = np.asarray(labels), np.asarray(predictions)
    recalls = []
    for c in range(n_classes):
        if not np.any(labels == c):
            raise ValueError(f"query cohort has no class {c}")
        recalls.append(float(np.mean(predictions[labels == c] == c)))
    return float(np.mean(recalls))
