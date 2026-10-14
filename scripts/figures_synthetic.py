#!/usr/bin/env python3
"""Generate one fixed-seed illustrative bank on Rift; plot its RNA UMAP locally.

This is an illustration of one prior draw, never a realism or accuracy result.
Generation writes exclusively to the explicitly supplied derivative directory.
"""
from pathlib import Path
import argparse
import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import time


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(8<<20),b''):h.update(block)
    return h.hexdigest()


def generate(outdir):
    root=Path('/share/runs/2026/30-03-phflot-hashprompt')
    hp=root/'hashprompt';sim=root/'pyscintelligentdesign'
    for name,value in [('OMP_NUM_THREADS','4'),('MKL_NUM_THREADS','4'),
                       ('OPENBLAS_NUM_THREADS','4'),('NUMBA_NUM_THREADS','4')]:os.environ[name]=value
    os.environ['CUDA_VISIBLE_DEVICES']=''
    sys.path[:0]=[str(hp/'src'),str(hp),str(sim/'src')]
    import numpy as np
    import pandas as pd
    import torch
    import scanpy as sc
    import anndata as ad
    from scipy import sparse
    import pyScIntelligentDesign
    from hashprompt import foundation_dataset_reuse as reuse
    from hashprompt import foundation_task_stream as fts
    torch.set_num_threads(4)
    assert str(Path(pyScIntelligentDesign.__file__).resolve()).startswith(str(sim/'src'))
    assert str(Path(reuse.__file__).resolve()).startswith(str(hp/'src'))
    revision=lambda p:subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
    assert revision(hp)=='c06f99df609e4931828d8ebdceac27556c88b455'
    assert revision(sim)=='6c4d2d0e52db8f8ede6c662aa2b0c641454d73b9'
    outdir=Path(outdir).resolve()
    expected=root/'cellpfn_paper_figures/synthetic_illustration'
    assert outdir==expected
    outdir.mkdir(parents=True,exist_ok=True)
    result=outdir/'synthetic_illustration.json'
    if result.exists():
        print('Existing complete derivative retained:',result,flush=True)
        return
    config=hp/'conf/foundation_realism_v22_B_usage.yaml'
    identity=fts.foundation_config_identity(config)
    schedule=reuse.build_reuse_schedule(datasets=4,episodes_per_dataset=1,root_start=42,
        task_stream_seed=42,config_identity_sha256=identity['content_sha256'],curriculum_offset=10000)
    spec=next(s for s in schedule.schedule if s.lane=='mean_program')
    assert not spec.early_prior
    assert spec.root==44
    fts._initialize_foundation_worker(str(config),identity['content_sha256'],
        fts.FoundationGenerationConfig(parent_query_per_class=100,train_query_per_class=100,mixed_shapes=True),
        'native_gene_count_v1')
    print('Generating exactly one bank:',spec.root,spec.lane,identity['content_sha256'],flush=True)
    t0=time.perf_counter();bank=reuse.generate_biology_bank(spec)
    assert bank.counts.shape==(8,8,256,8192)
    assert bank.receipt['lane']=='mean_program'
    count_path=outdir/'counts.npy'
    if count_path.exists():raise RuntimeError('Unfinished prior derivative exists; refusing silent overwrite')
    np.save(count_path,bank.counts)
    donor,celltype,cell=np.indices(bank.counts.shape[:3])
    n=donor.size
    print('Generated bank; beginning RNA coordinates for',n,'cells',flush=True)
    obs=pd.DataFrame({'cell_id':[f'synthetic_{i:05d}' for i in range(n)],
        'donor':donor.ravel()+1,'cell_type':celltype.ravel()+1,'cell_within_type_donor':cell.ravel(),
        'study':donor.ravel()%4+1}).set_index('cell_id')
    counts=bank.counts.reshape(n,8192)
    a=ad.AnnData(sparse.csr_matrix(counts,dtype=np.float32),obs=obs)
    a.var_names=[f'anonymous_gene_{i:04d}' for i in range(8192)]
    sc.pp.normalize_total(a,target_sum=10000)
    sc.pp.log1p(a)
    sc.pp.highly_variable_genes(a,flavor='seurat',n_top_genes=2000)
    selected=np.flatnonzero(a.var.highly_variable.to_numpy())
    pd.DataFrame({'anonymous_gene_index':selected,'gene_id':a.var_names[selected]}).to_csv(
        outdir/'synthetic_illustration_genes.csv',index=False)
    b=a[:,a.var.highly_variable].copy()
    sc.pp.pca(b,n_comps=50,svd_solver='arpack',random_state=42)
    sc.pp.neighbors(b,n_neighbors=15,n_pcs=50,metric='euclidean',random_state=42)
    sc.tl.umap(b,min_dist=.3,random_state=42)
    assert np.isfinite(b.obsm['X_umap']).all()
    obs['umap_1']=b.obsm['X_umap'][:,0];obs['umap_2']=b.obsm['X_umap'][:,1]
    obs.reset_index().to_csv(outdir/'synthetic_illustration.csv',index=False)
    metadata={'purpose':'Single fixed-seed illustrative prior draw, not an evaluation or realism statistic',
       'selection':'First mean_program lane in four-bank schedule with root_start=42, seed=42; no bank screening',
       'prior_label':'Cellular prior','root_start':42,'task_stream_seed':42,'bank_root':spec.root,
       'curriculum_offset':10000,'spec':dataclasses.asdict(spec),'config_identity':identity,
       'source_revisions':{'hashprompt':revision(hp),'pyscintelligentdesign':revision(sim)},
       'source_modules':{'reuse':reuse.__file__,'simulator':pyScIntelligentDesign.__file__},
       'receipt':bank.receipt,'counts_shape':list(bank.counts.shape),'counts_dtype':str(bank.counts.dtype),
       'counts_file_sha256':sha(count_path),'n_cells':n,'n_genes':8192,
       'visualization':{'normalization':'log1p(CP10000)','hvg_flavor':'seurat','hvg_requested':2000,
          'hvg_realized':len(selected),'pca_components':50,'pca_solver':'arpack','neighbors':15,
          'metric':'euclidean','min_dist':.3,'random_state':42,'labels_used_in_geometry':False},
       'versions':{'numpy':np.__version__,'torch':torch.__version__,
          'scanpy':__import__('importlib.metadata').metadata.version('scanpy'),
          'anndata':__import__('importlib.metadata').metadata.version('anndata')},
       'cpu_threads_max':4,'cuda_initialized':torch.cuda.is_initialized(),
       'derivative_elapsed_seconds':time.perf_counter()-t0,
       'timing_interpretation':'Illustration execution receipt only; not a controlled simulator throughput benchmark',
       'outputs':{p.name:sha(p) for p in outdir.glob('synthetic_illustration*.csv')}}
    assert not metadata['cuda_initialized']
    result.write_text(json.dumps(metadata,indent=2,default=str)+'\n')
    print('Completed',result,flush=True)


def plot():
    import numpy as np
    import pandas as pd
    from matplotlib.lines import Line2D
    from figures_common import ROOT,FIGURES,plt,save_figure,write_source,panel_label
    folder=FIGURES/'biological_data'
    meta=json.loads((folder/'synthetic_illustration.json').read_text())
    d=pd.read_csv(folder/'synthetic_illustration.csv')
    assert len(d)==16384 and meta['bank_root']==44
    assert d.groupby(['donor','cell_type']).size().eq(256).all()
    colors=['#167C80','#3F69A5','#826199','#BD6C38','#8E8B35','#577449','#A65C79','#65717B']
    fig,axes=plt.subplots(1,2,figsize=(180/25.4,90/25.4))
    fig.subplots_adjust(left=.07,right=.98,bottom=.20,top=.83,wspace=.25)
    fig.text(.035,.965,'One synthetic dataset expresses cell-type and donor structure',fontsize=8,fontweight='bold',va='top')
    fig.text(.035,.91,'Illustrative fixed-seed draw  |  8 donors × 8 cell types × 256 cells  |  Anonymous genes',fontsize=7)
    order=np.random.default_rng(42).permutation(len(d))
    for ax,key,title,letter in zip(axes,['cell_type','donor'],['Simulated cell type','Simulated donor'],['m','n']):
        dd=d.iloc[order]
        ax.scatter(dd.umap_1,dd.umap_2,c=[colors[int(v)-1] for v in dd[key]],s=.9,
                   linewidths=0,rasterized=True)
        ax.set_xlabel('RNA UMAP 1');ax.set_ylabel('RNA UMAP 2');ax.set_xticks([]);ax.set_yticks([])
        ax.set_xlim(d.umap_1.min()-.5,d.umap_1.max()+.5);ax.set_ylim(d.umap_2.min()-.5,d.umap_2.max()+.5)
        panel_label(ax,letter,title)
        handles=[Line2D([],[],marker='o',markersize=3,color=c,lw=0,label=str(i+1)) for i,c in enumerate(colors)]
        ax.legend(handles=handles,ncol=8,loc='upper center',bbox_to_anchor=(.5,-.1),frameon=False,
                  columnspacing=.7,handlelength=.5,handletextpad=.3)
    fid='supp_figure1_illustration';write_source(fid,'m_n',d)
    skill=Path('/home/phflot/.codex/skills/nature-figure/scripts')
    if skill.exists():
        sys.path.insert(0,str(skill))
        from audit_panel_alignment import require_matplotlib_panel_alignment
        require_matplotlib_panel_alignment(fig,json_out=str(FIGURES/f'{fid}.alignment.json'),strict=True)
    save_figure(fig,fid,title='Illustrative synthetic-cell RNA geometry',
        claim='A single predefined cellular-prior draw shows cell-type and donor structure in RNA coordinates.',
        panels=[{'letter':l,'claim':t,'source':'synthetic_illustration.csv','n':'16384 generated cells from one synthetic bank',
            'uncertainty':'Illustrative coordinates; no inferential estimate','color':k,'geometry':'Same unsupervised RNA coordinates in both panels'}
            for l,t,k in zip(['m','n'],['Cell-type structure','Donor structure'],['cell_type','donor'])],
        sources=[folder/'synthetic_illustration.csv',folder/'synthetic_illustration.json',folder/'synthetic_illustration_genes.csv'],
        extra={'selection':meta['selection'],'bank_hash':meta['receipt']['bank_sha256'],
               'visualization':meta['visualization'],'exclusions':'None; every generated cell is displayed.'})
    (ROOT/'sections/legend_supp_figure1_illustration.tex').write_text(
       r'\textbf{Illustrative RNA geometry of one predefined cellular-prior draw.} '
       r'\textbf{m,n}, Identical unsupervised UMAP coordinates coloured by simulated cell type or donor. '
       r'All 16,384 cells comprise eight donors, eight types and 256 cells per combination, with 8,192 anonymous genes. '
       r'The mean-program bank (root 44; seed 42) was selected before generation. '
       r'Log1p counts-per-10,000 and 2k HVGs supplied 50 principal components, 15 Euclidean neighbours and UMAP '
       r'(minimum distance 0.3; seed 42). Labels did not determine geometry. '
       r'This single draw is illustrative, not a realism assessment. Source Data provide coordinates, selected genes and the configuration receipt.'+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--generate',type=Path);a=p.parse_args()
    if a.generate:generate(a.generate)
    else:plot()
