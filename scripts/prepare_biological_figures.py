#!/usr/bin/env python3
"""Derive figure-only RNA coordinates and gene overlays from frozen Rift cases.

Run on Rift in the recorded analysis environment. Existing inputs are read-only;
all derivatives go to --output. This performs no model training or inference.
"""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

parser=argparse.ArgumentParser()
parser.add_argument('--root',default='/share/runs/2026/30-03-phflot-hashprompt')
parser.add_argument('--output',required=True)
parser.add_argument('--cases',nargs='*',default=['pbmc_main','cortex_main','pbmc_fine','cortex_held'])
args=parser.parse_args()
R=Path(args.root);L=R/'hashprompt_improvement_loop';OUT=Path(args.output)
assert OUT.resolve().is_relative_to((R/'cellpfn_paper_figures').resolve())
OUT.mkdir(parents=True,exist_ok=True)
os.environ['NUMBA_CACHE_DIR']=str(OUT/'numba_cache')
os.environ['NUMBA_NUM_THREADS']='1'
sys.dont_write_bytecode=True
sys.path.insert(0,str(L/'gene_importance_20261008/code'))
import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
from scipy import sparse
from scipy.special import softmax
from sklearn.metrics import balanced_accuracy_score
import cellpfn_attr as ca

SPECS={
 'pbmc_main':dict(key='pbmc_l1_b100_s0',panel='pbmc',case='celltype.l1_b100_s0',mode='count',markers=['IL7R','NKG7']),
 'cortex_main':dict(key='zebra_dev_b10_s0',panel='zebra',case='zebra_closed_development_b10_s0_p0',mode='processed',markers=['PLP1','CLDN5']),
 'pbmc_fine':dict(key='pbmc_l2_b10_s0',panel='pbmc',case='celltype.l2_b10_s0',mode='count',markers=[]),
 'cortex_held':dict(key='zebra_ood_b10_s0',panel='zebra',case='zebra_closed_ood_development_b10_s0_p0',mode='processed',markers=[]),
}
GENES=['CD79A','MAL','CD8B','FCER1A','SERPINA1','KLRF1','GNG11','GZMK','MS4A1','IL7R','CD8A','CLEC10A','CD14','GNLY','NKG7','PPBP','CD3E','LILRA4','LYZ']

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(8<<20),b''):h.update(chunk)
 return h.hexdigest()

for name in args.cases:
 spec=SPECS[name];key=spec['key'];started=time.monotonic()
 print('START',name,flush=True)
 if key not in ca.CASES:
  pred=(f'pbmc/results/{{arm}}/{spec["case"]}/predictions.npz' if spec['panel']=='pbmc' else f'zebra/{{arm}}/zebra_cell_type/{spec["case"]}/predictions.npz')
  ca.CASES[key]=dict(panel=spec['panel'],case_id=spec['case'],mode=spec['mode'],pred=pred,key='logits__{arm}' if spec['panel']=='pbmc' else 'logits',qbs=32)
 case_json=L/'realcell_baselines_20261008/cases'/spec['panel']/(spec['case']+'.json')
 if not case_json.exists():
  print('MISSING_CASE',case_json,flush=True);continue
 meta=json.loads(case_json.read_text());sources={str(case_json):sha(case_json)}
 for keyfile,hashkey in [('npz','npz_sha256'),('query_labels','query_labels_sha256')]:
  path=Path(meta['files'][keyfile]);digest=sha(path)
  assert digest==meta['files'][hashkey],(path,digest,meta['files'][hashkey])
  sources[str(path)]=digest
 data=ca.case_inputs(key);logits,y,obs,pred_path=ca.stored_logits(key,'G')
 sources[pred_path]=sha(pred_path)
 assert np.array_equal(y,data.query_labels)
 assert np.array_equal(obs,data.query_obs)
 assert len(set(obs.tolist()))==len(obs)
 raw=ca.realcases.load_case(spec['panel'],spec['case'])
 assert np.array_equal(raw.query_obs_ids,obs)
 expected_nq=meta['n_query'];assert len(obs)==expected_nq
 pred=logits.argmax(1);probs=softmax(logits,axis=1)
 df=pd.DataFrame({'obs_id':obs,'true_label':np.asarray(data.class_names)[y],
                  'predicted_label':np.asarray(data.class_names)[pred],
                  'correct':pred==y,'confidence':probs.max(1),
                  'entropy':-(probs*np.log(np.maximum(probs,1e-12))).sum(1),
                  'explained':False})
 with np.load(meta['files']['npz'],allow_pickle=False) as z:
  qmask=z['split']=='query'
  for col in ['donor','study']:
   df[col]=z[col][qmask]
 # Expression figures use log-normalized counts; preserve the processed cortex view.
 X=np.vstack([data.support,data.query]).astype(np.float32)
 if data.mode=='count':
  X*=10000./np.maximum(X.sum(1,keepdims=True),1)
  np.log1p(X,out=X)
 assert np.isfinite(X).all() and X.min()>=0
 ns=len(data.support)
 attr_path=L/'gene_importance_20261008/results'/(spec['key']+'__G.npz')
 corr_path=L/'gene_importance_20261008/results'/(spec['key']+'__G__dsloo_corr.npz')
 if attr_path.exists() and corr_path.exists():
  z=np.load(attr_path,allow_pickle=False);corr=np.load(corr_path,allow_pickle=False)
  sel=z['sel'];assert np.array_equal(z['symbols'],data.symbols)
  assert np.array_equal(z['class_names'],np.asarray(data.class_names))
  assert np.array_equal(z['cls'],y[sel]) and np.all(pred[sel]==y[sel])
  np.testing.assert_allclose(corr['class__dsloo_corr_margin'],np.vstack([corr['dl_margin'][z['cls']==c].mean(0) for c in range(len(data.class_names))]),rtol=2e-5,atol=2e-6)
  df.loc[sel,'explained']=True
  for gene in spec['markers']:
   ix=np.flatnonzero(data.symbols==gene);assert len(ix)==1,(gene,ix)
   df['expression_'+gene]=X[ns:,ix[0]]
   df['attribution_'+gene]=np.nan
   df.loc[sel,'attribution_'+gene]=corr['dl_margin'][:,ix[0]]
  if name=='pbmc_main':
   rows=[]
   for c,label in enumerate(data.class_names):
    support=X[:ns][data.support_labels==c]
    for gene in GENES:
     ix=np.flatnonzero(data.symbols==gene);assert len(ix)==1,(gene,ix)
     j=int(ix[0]);rows.append(dict(class_label=label,gene=gene,mean_log_expression=float(support[:,j].mean()),detected_fraction=float((support[:,j]>0).mean()),dsloo_corr_margin=float(corr['class__dsloo_corr_margin'][c,j])))
   pd.DataFrame(rows).to_csv(OUT/'pbmc_gene_matrix.csv',index=False)
  sources[str(attr_path)]=sha(attr_path);sources[str(corr_path)]=sha(corr_path)
  z.close();corr.close()
 # All fitting below is visualization only and does not affect stored classifier outputs.
 av=ad.AnnData(X)
 sc.pp.highly_variable_genes(av,flavor='seurat',n_top_genes=min(2000,X.shape[1]),inplace=True)
 mask=av.var.highly_variable.to_numpy();mask &= np.asarray(av.X.var(0)>0)
 hvgs=np.flatnonzero(mask)
 av=av[:,hvgs].copy();del X
 sc.pp.scale(av,max_value=10)
 npc=min(50,av.n_obs-1,av.n_vars-1)
 sc.tl.pca(av,n_comps=npc,svd_solver='arpack',random_state=42)
 sc.pp.neighbors(av,n_neighbors=15,n_pcs=npc,use_rep='X_pca',metric='euclidean',random_state=42)
 sc.tl.umap(av,min_dist=.3,random_state=42)
 coords=np.asarray(av.obsm['X_umap']);assert np.isfinite(coords).all()
 df.insert(1,'umap1',coords[ns:,0]);df.insert(2,'umap2',coords[ns:,1])
 df.to_csv(OUT/(name+'.csv'),index=False)
 pd.DataFrame({'gene':data.symbols[hvgs],'benchmark_column':hvgs}).to_csv(OUT/(name+'_visual_genes.csv'),index=False)
 info={'case':spec,'checkpoint_sha256':ca.CHECKPOINTS['G'][1],
       'source_hashes':sources,'preparation_script_sha256':sha(__file__),'query_cells':len(df),'support_cells':ns,'explained_cells':int(df.explained.sum()),
       'balanced_accuracy_pct':100*balanced_accuracy_score(y,pred),'visualization_only':True,
       'parameters':{'hvg_flavor':'seurat','requested_hvgs':2000,'realized_hvgs':len(hvgs),'scale_clip':10,'pca_components':npc,'neighbors':15,'umap_min_dist':.3,'metric':'euclidean','seed':42,'fitting_population':'exact support/query union, without labels'},
       'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'pandas':pd.__version__,'scanpy':sc.__version__,'anndata':ad.__version__},
       'output_sha256':sha(OUT/(name+'.csv')),'seconds':time.monotonic()-started}
 (OUT/(name+'.json')).write_text(json.dumps(info,indent=2)+'\n')
 print('DONE',name,{k:info[k] for k in ['query_cells','support_cells','explained_cells','balanced_accuracy_pct','seconds']},flush=True)
 del av,data,df,raw;gc.collect()
