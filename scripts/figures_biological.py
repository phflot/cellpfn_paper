#!/usr/bin/env python3
"""Expanded RNA maps and marker overlays for Supplementary Figure S7.

Only consumes verified figure derivatives; performs no embedding, modelling,
expression transformation or cell sampling. One numbered figure has two assets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, TwoSlopeNorm, to_hex, to_rgb
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, ScalarFormatter
from figures_common import ROOT, FIGURES, SOURCE, TEAL, BLUE, PURPLE, GRAY, write_source, save_figure
from figures_explanation import CLASS_COLORS

BIO=FIGURES/'biological_data'
EXPECTED={'pbmc_main':(320,191),'cortex_main':(7769,96),'pbmc_fine':(800,0),'cortex_held':(7163,0)}
FINE_LABELS=['B intermediate','B memory','B naive','CD14 Mono','CD16 Mono',
             'CD4 Naive','CD4 TCM','CD4 TEM','CD8 Naive','CD8 TCM','CD8 TEM',
             'MAIT','NK','NK Proliferating','NK_CD56bright','Platelet','Treg','cDC2','gdT','pDC']
# Use stable explicit fine-class colours while preserving shared coarse cortex colours.
FINE_COLORS={label:to_hex(plt.get_cmap('tab20')(i)) for i,label in enumerate(FINE_LABELS)}


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_case(name):
 path=BIO/f'{name}.csv';meta_path=BIO/f'{name}.json'
 if not path.exists() or not meta_path.exists():raise FileNotFoundError(f'Verified biological derivative missing: {path}')
 info=json.loads(meta_path.read_text());assert sha(path)==info['output_sha256'],path
 d=pd.read_csv(path,dtype={'obs_id':str,'true_label':str,'predicted_label':str,'donor':str,'study':str})
 assert d.obs_id.is_unique and d.obs_id.notna().all()
 assert np.isfinite(d[['umap1','umap2']].to_numpy(float)).all()
 for col in ['correct','explained']:
  if d[col].dtype!=bool:d[col]=d[col].astype(str).str.lower().map({'true':True,'false':False,'1':True,'0':False})
  assert d[col].notna().all()
 assert (d.correct==(d.true_label==d.predicted_label)).all()
 assert len(d)==info['query_cells']==EXPECTED[name][0],(name,len(d))
 assert int(d.explained.sum())==info['explained_cells']==EXPECTED[name][1]
 assert d.loc[d.explained,'correct'].all()
 bacc=d.groupby('true_label',observed=True).correct.mean().mean()*100
 assert abs(bacc-info['balanced_accuracy_pct'])<1e-8
 assert info['visualization_only'] and info['parameters']['seed']==42
 return d,info


def coords(ax,d):
 x=d.umap1.to_numpy();y=d.umap2.to_numpy()
 xr=max(np.ptp(x),1e-6);yr=max(np.ptp(y),1e-6)
 ax.set_xlim(x.min()-.06*xr,x.max()+.06*xr);ax.set_ylim(y.min()-.06*yr,y.max()+.06*yr)
 ax.set_aspect('equal',adjustable='box');ax.set_xticks([]);ax.set_yticks([])
 for spine in ax.spines.values():spine.set_visible(False)


def tag(ax,letter,title):
 ax.set_title(title,fontsize=7,loc='left',pad=5)
 ax.annotate(letter,(0,1),xycoords='axes fraction',xytext=(-12,5),textcoords='offset points',fontweight='bold',fontsize=8,ha='left',va='bottom',annotation_clip=False)


def category(ax,d,col,palette):
 assert d[col].notna().all(),col
 # A fixed permutation avoids a class-ordered draw stack without dropping cells.
 order=np.random.default_rng(42).permutation(len(d));q=d.iloc[order]
 colors=[palette[x] for x in q[col]]
 ax.scatter(q.umap1,q.umap2,s=5 if len(d)<1000 else .65,c=colors,linewidths=0,rasterized=True)
 coords(ax,d)


def errors(ax,d):
 q=d[d.correct];e=d[~d.correct]
 ax.scatter(q.umap1,q.umap2,s=5 if len(d)<1000 else .6,color='#D5D9DB',linewidths=0,rasterized=True)
 ax.scatter(e.umap1,e.umap2,s=9 if len(d)<1000 else 2.2,color='#B44742',linewidths=0,rasterized=True)
 coords(ax,d)
 ax.text(.01,-.065,f'{len(e):,} / {len(d):,} errors',transform=ax.transAxes,fontsize=6,color='#444444',ha='left',va='bottom',clip_on=False)


def handles(palette):
 return [Line2D([],[],marker='o',linestyle='none',markerfacecolor=c,markeredgewidth=0,markersize=3.4,label=k) for k,c in palette.items()]


def panel_source(letter,d,fields):
 return write_source('supp_figure7',letter,d[list(dict.fromkeys(['obs_id','umap1','umap2']+fields))])


def meta(letter,claim,case,variable,d,info,*,extra=None):
 out=dict(letter=letter,claim=claim,sources=[str(BIO/f'{case}.csv'),str(BIO/f'{case}.json')],
          filters={'case':case,'variable':variable,'population':'all query cells'},n=len(d),unit='query cell',
          aggregation='none',uncertainty='none; descriptive map',exclusions='No cell sampling or omission',
          coordinate_system='RNA-derived UMAP of exact support/query union; same coordinates reused within case',
          visualization_parameters=info['parameters'],checkpoint_sha256=info['checkpoint_sha256'])
 if extra:out.update(extra)
 return out


def save_asset(fig,fid,title,claim,panels,sources,source_csv,extra):
 save_figure(fig,fid,title=title,claim=claim,panels=panels,sources=sources,extra=extra)
 # Both continuation assets share the source-data folder for the numbered figure.
 path=FIGURES/f'{fid}.json';m=json.loads(path.read_text())
 m['panel_source_data']={p:sha(ROOT/p) for p in source_csv}
 path.write_text(json.dumps(m,indent=2)+'\n')
 print(f'Linked {len(source_csv)} shared S7 panel-source files for {fid}')


def maps():
 names=['pbmc_fine','cortex_held','pbmc_main','cortex_main']
 data={name:load_case(name) for name in names}
 fig=plt.figure(figsize=(180/25.4,180/25.4))
 fig.text(.055,.982,'Biological context across annotation and cohort shifts',fontsize=9,fontweight='bold',va='top')
 panels=[];source_csv=[];sources=[]
 lefts=[.055,.375,.695];width=.265
 for case,bottom,letters,title in [('pbmc_fine',.655,'abc','Fine PBMC · 10 supports/class · 800 query cells'),
                                   ('cortex_held',.355,'def','Held-study cortex · 10 supports/class · 7,163 query cells')]:
  d,info=data[case];palette=FINE_COLORS if case=='pbmc_fine' else {k:CLASS_COLORS[k] for k in ['Glia','Immune cell','Neural','Vascular cell']}
  assert set(d.true_label.unique())<=set(palette) and set(d.predicted_label.unique())<=set(palette)
  fig.text(.055,bottom+.272,title,fontsize=7.5,fontweight='bold',va='bottom')
  for col,(variable,label) in enumerate([('true_label','Reference labels'),('predicted_label','CellPFN predictions'),('correct','Prediction errors')]):
   ax=fig.add_axes([lefts[col],bottom,width,.235])
   if variable=='correct':errors(ax,d)
   else:category(ax,d,variable,palette)
   tag(ax,letters[col],label)
   source_csv.append(panel_source(letters[col],d,[variable,'true_label','predicted_label','correct']))
   panels.append(meta(letters[col],'Reference and predicted labels share one RNA-derived geometry',case,variable,d,info,extra={'class_palette':palette,'draw_order':'fixed seed-42 permutation for categorical maps; correct background then errors'}))
  if case=='cortex_held':
   fig.legend(handles=handles(palette),loc='upper left',bbox_to_anchor=(.05,bottom-.012),ncol=4,frameon=False,fontsize=6,handlelength=.7,handletextpad=.3,columnspacing=1.5)
 for i,(case,var,letter,title) in enumerate([('pbmc_main','donor','g','PBMC coarse: donor'),('cortex_main','study','h','Development cortex: study')]):
  d,info=data[case];labs=sorted(d[var].dropna().unique());assert len(labs)==4
  palette={lab:c for lab,c in zip(labs,[BLUE,TEAL,PURPLE,'#CC6E3B'])}
  ax=fig.add_axes([lefts[i],.075,width,.205]);category(ax,d,var,palette)
  ax.set_title(title,visible=False)  # Preserve descriptive geometry metadata.
  fig.text(lefts[i]-.025,.293,letter,fontsize=8,fontweight='bold',va='bottom')
  fig.text(lefts[i],.293,title,fontsize=7,va='bottom')
  fig.legend(handles=handles(palette),loc='upper left',bbox_to_anchor=(lefts[i]-.007,.061),ncol=2,frameon=False,fontsize=6,handlelength=.7,handletextpad=.3,columnspacing=.8)
  source_csv.append(panel_source(letter,d,[var,'true_label','predicted_label','correct']))
  panels.append(meta(letter,'Biological maps retain donor/study context without integration',case,var,d,info,extra={'category_palette':palette,'draw_order':'fixed seed-42 permutation'}))
 # Stable categorical legend occupies its own area, outside the data panels.
 legend_ax=fig.add_axes([.695,.015,.285,.27]);legend_ax.axis('off')
 legend_ax.text(0,1,'Fine PBMC classes',fontsize=7,fontweight='bold',va='top')
 legend_ax.legend(handles=handles(FINE_COLORS),loc='upper left',bbox_to_anchor=(-.04,.92),ncol=2,frameon=False,fontsize=6,handlelength=.55,handletextpad=.25,columnspacing=.45,labelspacing=.52,borderaxespad=0)
 for name in names:sources.extend([BIO/f'{name}.csv',BIO/f'{name}.json'])
 save_asset(fig,'supp_figure7_maps','Expanded biological maps','Reference labels, errors and study context can be examined on shared RNA coordinates without dropping query cells.',panels,sources,source_csv,{'numbered_figure':'S7','continuation_asset':'page 1 of 2','fine_class_palette':FINE_COLORS,'coarse_class_palette':CLASS_COLORS})


def markers():
 data={name:load_case(name) for name in ['pbmc_main','cortex_main']}
 fig=plt.figure(figsize=(180/25.4,150/25.4))
 fig.text(.055,.985,'Expression and signed deletion attribution in the same cells',fontsize=9,fontweight='bold',va='top')
 panels=[];source_csv=[];sources=[]
 xleft=[.055,.29,.525,.76];width=.205
 for row,(case,genes,letters,title) in enumerate([
     ('pbmc_main',['IL7R','NKG7'],'ijkl','PBMC coarse · 100 supports/class · 191 / 320 queries explained'),
     ('cortex_main',['PLP1','CLDN5'],'mnop','Development cortex · 10 supports/class · 96 / 7,769 queries explained')]):
  d,info=data[case];bottom=.62 if row==0 else .21
  fig.text(.055,bottom+.29,title,fontsize=7.5,fontweight='bold',va='bottom')
  for gi,gene in enumerate(genes):
   for kind in ['expression','attribution']:
    ci=gi*2+(kind=='attribution');letter=letters[ci];col=kind+'_'+gene
    assert col in d
    ax=fig.add_axes([xleft[ci],bottom,width,.245]);values=pd.to_numeric(d[col],errors='raise')
    if kind=='expression':
     assert values.notna().all() and np.isfinite(values).all() and (values>=0).all()
     order=np.random.default_rng(42).permutation(len(d));q=d.iloc[order]
     im=ax.scatter(q.umap1,q.umap2,c=values.iloc[order],cmap='YlGnBu',norm=Normalize(vmin=0,vmax=float(values.max())),s=6 if len(d)<1000 else .8,linewidths=0,rasterized=True)
     scale_label='log1p CP10k' if case=='pbmc_main' else 'Processed expression'
     ticks=[0,float(values.max())];extra={'color_scale':[0,float(values.max())],'transformation':'No additional transformation; supplied display expression'}
    else:
     assert values.notna().equals(d.explained)
     assert np.isfinite(values[d.explained]).all()
     # Gray includes every query. All explained cells, including exact zeros, are overlaid.
     ax.scatter(d.umap1,d.umap2,color='#DDDFE1',s=6 if len(d)<1000 else .8,linewidths=0,rasterized=True)
     q=d[d.explained];v=values[d.explained];limit=float(np.max(np.abs(v)));assert limit>0
     im=ax.scatter(q.umap1,q.umap2,c=v,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit),s=10 if len(d)<1000 else 6,edgecolors='#333333',linewidths=.12,rasterized=True)
     scale_label='Signed margin change';ticks=[-limit,0,limit]
     extra={'color_scale':[-limit,limit],'explained_cells':int(d.explained.sum()),'missing_values':'NaN = not explained; gray background; not interpreted as zero','target':'Corrected DS-LOO query-only predicted-versus-fixed-runner-up margin; positive supports the predicted class','point_sizes':'Explained-cell marks enlarged for visibility; size does not encode effect'}
    coords(ax,d);tag(ax,letter,f'{gene}: '+('expression' if kind=='expression' else 'attribution'))
    cax=fig.add_axes([xleft[ci]+.012,bottom-.027,width-.024,.012]);cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=ticks)
    cb.ax.tick_params(labelsize=6,length=2,pad=2);cb.ax.set_xticklabels([format(x,'.2g') for x in ticks]);cb.set_label(scale_label,fontsize=6,labelpad=1)
    source_csv.append(panel_source(letter,d,['true_label','predicted_label','correct','explained',col]))
    panels.append(meta(letter,'Marker expression and signed deletion effects are distinct quantities',case,col,d,info,extra=extra))
  sources.extend([BIO/f'{case}.csv',BIO/f'{case}.json'])
 fig.text(.055,.075,'All query cells are retained. Gray attribution backgrounds mark cells without explanations; outlined points mark explained cells.\nColor limits span observed values (symmetric around zero for attribution), independently per gene. RNA geometry is fixed within a case.\nPositive attribution supports the predicted class over its fixed runner-up; expression direction and causality are not inferred.',fontsize=6,color='#444444',va='top',linespacing=1.35)
 save_asset(fig,'supp_figure7_markers','Expression and signed attribution overlays','Known marker expression and query-specific deletion effects can be inspected on a common RNA map with explicit explanation coverage.',panels,sources,source_csv,{'numbered_figure':'S7','continuation_asset':'page 2 of 2','color_scale_policy':'Full observed limits; no clipping or quantile scaling; separate per gene and quantity'})


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--markers-only',action='store_true');args=parser.parse_args()
 if not args.markers_only:maps()
 markers()
