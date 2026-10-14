#!/usr/bin/env python3
"""Reconcile cached attribution fixtures without rerunning model inference."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy.stats import spearmanr
parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);parser.add_argument('--output',required=True)
a=parser.parse_args();R=Path(a.root);OUT=Path(a.output)
assert OUT.resolve().is_relative_to((R/'cellpfn_paper_figures').resolve())
base=R/'hashprompt_improvement_loop/gene_importance_20261008/results'
cases=['pbmc_l1_b10_s0','pbmc_l1_b10_s1','pbmc_l1_b100_s0','zebra_dev_b10_s0','kidney_core9_A_F0_count','kidney_core9_A_F0_processed']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(8<<20),b''):h.update(block)
 return h.hexdigest()
rows=[];hashes={}
for case in cases:
 for arm in ['G','C']:
  paths=[base/f'{case}__{arm}.npz',base/f'{case}__{arm}__dsloo_corr.npz',base/f'{case}__{arm}.json',base/f'{case}__{arm}__dsloo.json']
  for p in paths:hashes[str(p)]=sha(p)
  info=json.loads(paths[2].read_text());checks=json.loads(paths[3].read_text())['checks']
  z=np.load(paths[0],allow_pickle=False);c=np.load(paths[1],allow_pickle=False);cls=z['cls']
  rho=[];err=[];n_pairs=0
  for j in range(len(z['class_names'])):
   if f'ko_genes__{j}' not in z:continue
   genes=z[f'ko_genes__{j}'];exact=z[f'ko_q_margin__{j}']
   cell_idx=np.flatnonzero(cls==j);fast=c['dl_margin'][cell_idx][:,genes].T
   assert fast.shape==exact.shape
   rho.append(float(np.nanmedian([spearmanr(fast[:,k],exact[:,k]).statistic for k in range(exact.shape[1])])))
   err.append(float(np.linalg.norm(fast.ravel()-exact.ravel())/np.linalg.norm(exact.ravel())))
   n_pairs+=exact.size
  row=dict(case_id=case,model_id='cellpfn_g1v2p' if arm=='G' else 'cellpfn_c1v2p',arm=arm,
           rho_cell_corr=float(np.nanmedian(rho)),rel_err_corr=float(np.nanmedian(err)),
           n_classes=len(rho),n_cells=len(cls),n_original_gene_pairs=n_pairs,
           checkpoint_sha256=info['info']['sha256'],recorded_parity=checks,
           gene_set='original class knockout set; excludes later DS-LOO-extreme extension',
           verification='independent recomputation from stored per-cell arrays; no new checkpoint inference')
  rows.append(row);print(row,flush=True);z.close();c.close()
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({'script_sha256':sha(Path(__file__)),'source_hashes':hashes,'results':rows},indent=2)+'\n')
