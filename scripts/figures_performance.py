#!/usr/bin/env python3
"""Build the biological benchmark, transfer, feature and cost figures from frozen CSVs.

No remote dependencies and no inferred uncertainty. All selections are exported
next to the graphics. Source IDs remain raw in CSV/JSON; manuscript labels name
scientific configurations rather than development versions.
"""
from pathlib import Path
import json
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
from figures_common import (ROOT,DATA,COLORS,TEAL,BLUE,PURPLE,GRAY,PANELS,PANEL_NAMES,
                            MODEL_NAMES,read,select,numeric,panel_label,write_source,save_figure)

BUDGETS=['1','10','100']; DRAWS=['0','1','2']
SHORT={'pbmc_l1':'PBMC coarse','pbmc_l2':'PBMC fine','zebra_dev':'Cortex development','zebra_ood':'Cortex held studies'}
MODELS=[('cellpfn_g1v2p','CellPFN','all'),('tabicl_v2','TabICLv2','hvg2000'),('c2b40k','TabICLv2 + prior','hvg2000'),('kumo_small','Kumo small','hvg2000'),('k2b_s40k','Kumo small + prior','hvg2000'),('kumo_large','Kumo large','hvg2000'),('k2b_l40k','Kumo large + prior','hvg2000'),('tabpfn35','TabPFN-3.5','hvg2000'),('geneformer_lr','Geneformer + LR','own_input'),('scgpt_lr','scGPT + LR','own_input'),('woodbury32_lda','Low-rank LDA','all'),('celltypist','CellTypist','all'),('singler','SingleR','all'),('scanvi_inductive','scANVI inductive','hvg2000'),('scanvi_transductive','scANVI transductive','hvg2000'),('logreg','Logistic regression','hvg2000')]
CORE=[MODELS[i] for i in [0,1,5,8,9,10]]
MARKERS=['o','s','^','D','v','X']
EXPOSURE=read('fig2__exposure_marks')
CMAP=LinearSegmentedColormap.from_list('soft_accuracy',['#FFFFFF','#DAE9E7','#89B8B2'])
DIV=LinearSegmentedColormap.from_list('signed_change',['#B66245','#FFFFFF','#258A83'])

def metadata(letter,claim,source,filters,n,unit,aggregation,uncertainty='None',availability='Complete selected rows'):
 return dict(letter=letter,claim=claim,source=source,filters=filters,n=n,unit=unit,aggregation=aggregation,uncertainty=uncertainty,availability=availability)

def src(fid,letter,stem,frame):
 out=frame.copy();out.insert(0,'export_file',stem+'.csv');write_source(fid,letter,out);return out

def bench(model,view,panels=PANELS):
 stem='fig4__cases' if model in [m[0] for m in MODELS[10:]] else 'fig2__cases'
 d=select(read(stem),model_id=model,gene_view=view,panel=panels,support_per_class=BUDGETS,draw=DRAWS,metric='balanced_accuracy',status='ok')
 if 'input_mode' in d:
  assert not d.duplicated(['panel','support_per_class','draw']).any(),(model,d.input_mode.unique())
 assert not d.duplicated(['panel','support_per_class','draw']).any(),model
 return stem,d

def mark(model,panel):
 family={'geneformer_lr':'geneformer','scgpt_lr':'scgpt'}.get(model)
 if not family:return ''
 d=select(EXPOSURE,family=family,panel=panel)
 return d.iloc[0]['mark'] if len(d)==1 else ''

def heat(ax,values,rows,cols,*,marks=None,signed=False,precision=1,bold=False,fontsize=6):
 a=np.asarray(values,float)
 im=ax.imshow(a,aspect='auto',interpolation='nearest',cmap=DIV if signed else CMAP,
              norm=TwoSlopeNorm(0,vmin=-max(1,np.nanmax(np.abs(a))),vmax=max(1,np.nanmax(np.abs(a)))) if signed else None,
              vmin=None if signed else 0,vmax=None if signed else 100)
 ax.set_xticks(range(len(cols)),cols);ax.set_yticks(range(len(rows)),rows)
 ax.tick_params(length=0,pad=3)
 ax.set_xticks(np.arange(-.5,len(cols),1),minor=True);ax.set_yticks(np.arange(-.5,len(rows),1),minor=True)
 ax.grid(which='minor',color='white',lw=.7);ax.tick_params(which='minor',length=0)
 for spine in ax.spines.values():spine.set_visible(False)
 for i in range(a.shape[0]):
  for j in range(a.shape[1]):
   if np.isnan(a[i,j]):ax.text(j,i,'—',ha='center',va='center',color='#7F7F7F',fontsize=fontsize);continue
   flag=marks[i][j] if marks is not None else ''
   display=Decimal(format(a[i,j],'.12f')).quantize(Decimal(1).scaleb(-precision),rounding=ROUND_HALF_UP)
   if display==0:display=abs(display)
   text=(f'{display:+.{precision}f}' if signed else f'{display:.{precision}f}')+flag
   weight='normal'
   if bold:
    overall=np.nanmax(a[:,j]); unflagged=[a[k,j] for k in range(a.shape[0]) if not (marks[k][j] if marks is not None else '') and np.isfinite(a[k,j])]
    rounded=lambda z:Decimal(format(z,'.12f')).quantize(Decimal(1).scaleb(-precision),rounding=ROUND_HALF_UP)
    if rounded(a[i,j])==rounded(overall) or (not flag and unflagged and rounded(a[i,j])==rounded(max(unflagged))):weight='bold'
   ax.text(j,i,text,ha='center',va='center',fontsize=fontsize,color='#666666' if flag else '#172D32',fontweight=weight)
 return im

def finish(fig,fid,title,claim,panels,sources,extra=None):
 save_figure(fig,fid,title=title,claim=claim,panels=panels,sources=sources,extra=extra)


def figure2():
 fid='figure2'; panels=[]
 fig=plt.figure(figsize=(180/25.4,175/25.4))
 fig.text(.07,.982,'Biological performance and transfer of the cellular prior',fontsize=9,fontweight='bold',va='top')
 gs=fig.add_gridspec(3,4,left=.08,right=.98,bottom=.12,top=.86,height_ratios=[1,.76,1.05],hspace=.83,wspace=.38)
 source=[]
 for pi,p in enumerate(PANELS):
  ax=fig.add_subplot(gs[0,pi]); selected=[]
  for mi,(m,label,view) in enumerate(CORE):
   stem,d=bench(m,view,[p]);source.append(stem);selected.append(d.assign(export_file=stem+'.csv'))
   means=[];xx=[]
   for bi,b in enumerate(BUDGETS):
    r=select(d,support_per_class=b);v=numeric(r)
    if len(v)==0:continue
    assert len(v)==3
    ax.scatter(np.full(3,bi)+np.array([-.04,0,.04]),v,s=6,color=COLORS[m],alpha=.5,linewidths=0,zorder=2)
    means.append(v.mean());xx.append(bi)
   ax.plot(xx,means,marker=MARKERS[mi],ms=3,lw=1.15 if m=='cellpfn_g1v2p' else .8,color=COLORS[m],label=label,zorder=4 if m=='cellpfn_g1v2p' else 3)
  exposure_text='; '.join(label.split(' + ')[0]+mark(m,p) for m,label,_ in CORE if mark(m,p))
  if exposure_text:ax.text(.025,.04,exposure_text,transform=ax.transAxes,fontsize=6,color='#777777',ha='left',va='bottom')
  write_source(fid,chr(97+pi),pd.concat(selected,ignore_index=True))
  ax.set_xticks(range(3),BUDGETS);ax.set_ylim(0,102);ax.set_xlim(-.15,2.2);ax.set_yticks([0,25,50,75,100]);ax.grid(axis='y',color='#EEEEEE',lw=.5)
  ax.set_xlabel('Supports per class')
  if pi==0:ax.set_ylabel('Balanced accuracy (%)')
  else:ax.set_yticklabels([])
  panel_label(ax,chr(97+pi),SHORT[p].replace('Cortex ','Cortex\n'))
  panels.append(metadata(chr(97+pi),'Support-dependent biological classification','fig2__cases / fig4__cases',dict(panel=p,models=[m[0] for m in CORE],views={m:v for m,_,v in CORE},metric='balanced_accuracy',draw=DRAWS,status='ok'),len(pd.concat(selected)),'support draw','Mean within panel, budget and model','Three raw support draws; no confidence interval','LDA one-shot unavailable; flags follow exposure audit'))
 handles=[Line2D([0],[0],color=COLORS[m],marker=MARKERS[i],ms=3,lw=1,label=l) for i,(m,l,_) in enumerate(CORE)]
 fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.52,.957),ncol=6,frameon=False,columnspacing=1.1,handletextpad=.4,handlelength=1.5,fontsize=6)
 ax=fig.add_subplot(gs[1,:]);models=['c2b40k','k2b_s40k','k2b_l40k']
 d=select(read('fig3__paired'),model_id=models,gene_view='hvg2000',panel=PANELS,support_per_class=BUDGETS,draw=DRAWS,metric='balanced_accuracy')
 assert len(d)==108
 vals=[[numeric(select(d,model_id=m,panel=p,support_per_class=b),'delta').mean() for p in PANELS for b in BUDGETS] for m in models]
 im=heat(ax,vals,['TabICLv2','Kumo small','Kumo large'],BUDGETS*4,signed=True,fontsize=7)
 for k,p in enumerate(PANELS):
  ax.text((k*3+1)/12+.5/12,1.08,SHORT[p],transform=ax.transAxes,ha='center',fontsize=7)
  if k:ax.axvline(k*3-.5,color='#777777',lw=.7)
 ax.set_xlabel('Supports per class');ax.annotate('e',xy=(0,1),xycoords='axes fraction',xytext=(-13,30),textcoords='offset points',fontsize=8,fontweight='bold',ha='left',va='bottom',annotation_clip=False);ax.set_title('Adapted − released balanced accuracy (percentage points)',loc='left',pad=29)
 src(fid,'e','fig3__paired',d);source.append('fig3__paired')
 panels.append(metadata('e','Cellular adaptation improves several conditions but can harm fine PBMC','fig3__paired',dict(model_id=models,gene_view='hvg2000',metric='balanced_accuracy',draw=DRAWS),108,'paired support draw','Mean matched-run delta over three draws per cell','No inferential interval; exact signed values shown'))
 ax=fig.add_subplot(gs[2,:2]);d=select(read('fig3__trajectory'),gene_view='hvg2000',finetune_arm=['c2b','k2b_s','k2b_l','p1_s43','p1_s44','p1_g'],scoring_run=['c2b_root','k2b_root','p1_root'])
 for arm,label,c,marker,style in [('c2b','TabICLv2',BLUE,'s','-'),('k2b_s','Kumo small',COLORS['kumo_small'],'o','-'),('k2b_l','Kumo large',PURPLE,'^','-'),('p1_s43','Kumo small, stream 2',COLORS['kumo_small'],'o',':'),('p1_s44','Kumo small, stream 3',COLORS['kumo_small'],'o','--'),('p1_g','Kumo small, generic',GRAY,'X','--')]:
  r=select(d,finetune_arm=arm).copy();r['sort']=numeric(r,'tasks_seen');r=r.sort_values('sort')
  ax.plot(numeric(r,'tasks_seen')/1000,numeric(r,'mean_delta_BA_8_low_support_cells'),color=c,marker=marker,ms=3,ls=style,lw=1,label=label)
 ax.axhline(0,color='#999999',lw=.6);ax.set_xticks([5,10,20,40]);ax.set_xlabel('Additional main-stream tasks (thousands)');ax.set_ylabel('Low-support change (pp)');ax.set_ylim(-6.5,7.5);handles,labels=ax.get_legend_handles_labels();ax.legend([handles[i] for i in [0,1,2,5]],['TabICLv2','Kumo small (3 task streams)','Kumo large','Kumo small, generic'],frameon=False,fontsize=6,loc='lower left',ncol=1,handlelength=1.5,borderaxespad=.2,labelspacing=.22)
 panel_label(ax,'f','Adaptation trajectory and generic control');src(fid,'f','fig3__trajectory',d);source.append('fig3__trajectory')
 panels.append(metadata('f','Cellular and generic task streams produce different changes','fig3__trajectory',dict(gene_view='hvg2000',finetune_arm=['c2b','k2b_s','k2b_l','p1_s43','p1_s44','p1_g'],scoring_run=['c2b_root','k2b_root','p1_root']),len(d),'checkpoint on one training seed','Equal mean of eight low-support panel–budget conditions, each over three support draws','Separate lines show task-stream repeats, not model-seed uncertainty','Generic control has unmatched row/column exposure; cellular curves exclude 25% additional replay count'))
 ax=fig.add_subplot(gs[2,2:]);d=select(read('fig3__generic_tables_cases'),model_id=['tabicl_v2','c2b40k'],metric='balanced_accuracy',status='ok')
 assert len(d)==120
 for i,(m,label,c) in enumerate([('tabicl_v2','Released',BLUE),('c2b40k','Adapted',TEAL)]):
  vals=[]
  for j,b in enumerate(['B1','B10','full']):
   r=select(d,model_id=m,support_budget=b);assert len(r)==20
   vals.append(numeric(r).mean())
   per=r.assign(score=numeric(r)).groupby('dataset').score.mean()
   ax.scatter(np.full(4,j)+(i-.5)*.12,per,s=9,color=c,alpha=.4)
  ax.plot(range(3),vals,color=c,marker='s' if i==0 else 'o',ms=4,label=label)
 ax.set_xticks(range(3),['1/class','10/class','Full split']);ax.set_ylim(40,102);ax.set_ylabel('Balanced accuracy (%)');ax.set_xlabel('Generic-table support budget');ax.legend(frameon=False,loc='lower right');panel_label(ax,'g','Generic-task retention')
 src(fid,'g','fig3__generic_tables_cases',d);source.append('fig3__generic_tables_cases')
 panels.append(metadata('g','Generic-task retention is incomplete','fig3__generic_tables_cases',dict(model_id=['tabicl_v2','c2b40k'],metric='balanced_accuracy',status='ok'),120,'dataset/split','Large symbols: equal mean of four datasets and five splits; small dots: dataset means','Dataset dots are heterogeneity, not confidence intervals'))
 fig.text(.08,.02,'CellPFN: 12.33M parameters · 384k scheduled episodes · 276,828 loss-bearing episodes\nAdaptation: 40k cellular + 10k replay tasks; released pretraining is additional. * / (*) mark query-source exposure evidence.',fontsize=6,color='#444444')
 finish(fig,fid,'Biological performance and cellular-prior transfer','The cellular prior supports compact inference and transfers to pretrained tabular models, with condition-specific tradeoffs.',panels,sorted(set(source))+['fig1__lineage','fig3__arms','fig2__exposure_marks'])


def supp2():
 fid='supp_figure2';panels=[];sources=[]
 fig=plt.figure(figsize=(180/25.4,190/25.4));fig.text(.06,.985,'Complete benchmark and finer annotation tasks',fontsize=9,fontweight='bold',va='top')
 ax=fig.add_axes([.25,.59,.72,.34]);vals=[];flags=[];selected=[]
 for m,label,view in MODELS:
  stem,d=bench(m,view);sources.append(stem);selected.append(d.assign(export_file=stem+'.csv'));vals.append([]);flags.append([])
  for p in PANELS:
   for b in BUDGETS:
    r=select(d,panel=p,support_per_class=b);assert len(r) in [0,3],(m,p,b,len(r))
    vals[-1].append(numeric(r).mean() if len(r) else np.nan);flags[-1].append(mark(m,p))
 heat(ax,vals,[l for _,l,_ in MODELS],BUDGETS*4,marks=flags,bold=True,fontsize=6)
 for k,p in enumerate(PANELS):
  ax.text((k*3+1.5)/12,1.03,SHORT[p].replace('Cortex ','Cortex\n'),transform=ax.transAxes,ha='center',fontsize=6)
  if k:ax.axvline(k*3-.5,color='#888888',lw=.7)
 ax.set_xlabel('Supports per class');panel_label(ax,'a')
 write_source(fid,'a',pd.concat(selected,ignore_index=True));panels.append(metadata('a','Full declared core comparator set','fig2__cases / fig4__cases',dict(models=[m[0] for m in MODELS],views={m:v for m,_,v in MODELS},panel=PANELS,draw=DRAWS,metric='balanced_accuracy',status='ok'),len(pd.concat(selected)),'support draw','Mean over three draws; bold best overall and best unflagged per condition, ties at displayed precision','No confidence intervals','Missing scores are dashes; gray starred values are exposure flagged; transductive scANVI uses query expression'))
 ax=fig.add_axes([.25,.16,.28,.31]);d=select(read('supp_prior_ablation__hard_tier_cellpfn_values'),model_id='cellpfn_g1v2p',checkpoint_update='96000',gene_view='hvg8192',scope_kind='task',metric=['H_b1_ba','H_b10_ba','H_b100_ba'],status='ok',readout_status='final')
 tasks=[('pbmc.l2.sib.CD4T','CD4 T, level 2 (4)'),('pbmc.l2.sib.T','T, level 2 (9)'),('pbmc.l3.sib.CD4T','CD4 T, level 3 (9)'),('pbmc.l3.sib.CD8T','CD8 T, level 3 (7)'),('pbmc.l3.sib.B','B, level 3 (6)'),('pbmc.l3.sib.NK','NK, level 3 (6)'),('pbmc.l3.sib.T','T, level 3 (17)'),('pbmc.l3.full','All PBMC, level 3 (35)'),('zebra.ct2.full.dev','Cortex finer types (7)'),('zebra.ct2.sib.Neural.ood','Held-study neural (3)')]
 vals=[]
 for task,_ in tasks:
  row=[]
  for b in BUDGETS:
   r=select(d,scope_value=task,metric='H_b'+b+'_ba');assert len(r)==1
   row.append(float(r.iloc[0].value))
  vals.append(row)
 heat(ax,vals,[l for _,l in tasks],BUDGETS,fontsize=6);ax.axhline(7.5,color='#888888',lw=.8);ax.set_xlabel('Supports per class');panel_label(ax,'b','Finer tasks: CellPFN, up to 8,192 HVGs')
 src(fid,'b','supp_prior_ablation__hard_tier_cellpfn_values',d);sources.append('supp_prior_ablation__hard_tier_cellpfn_values');panels.append(metadata('b','Finer biological label tasks are available but exploratory','supp_prior_ablation__hard_tier_cellpfn_values',dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',gene_view='hvg8192',scope_kind='task',status='ok',readout_status='final'),len(d),'task summary','Supplied mean balanced accuracy; class counts in parentheses','10/10/5 support-draw means; no draw-level data or intervals in this checkpoint summary','Eight PBMC tasks and two cortex tasks defined post hoc; differing labels prevent an isolated difficulty comparison'))
 ax=fig.add_axes([.69,.28,.28,.19]);d=read('fig4__cases');kp=['kidney_core5_a','kidney_core5_b','kidney_core9_a','kidney_core9_b'];picked=[];values=[];marks=[]
 km=[('cellpfn_g1v2p','CellPFN, counts','all','count'),('cellpfn_g1v2p','CellPFN, processed','all','processed'),('tabicl_v2','TabICLv2','hvg2000','processed'),('kumo_large','Kumo large','hvg2000','processed'),('geneformer_lr','Geneformer + LR','own_input','own'),('scgpt_lr','scGPT + LR','own_input','own'),('woodbury32_lda','Low-rank LDA','all','processed')]
 for m,label,view,mode in km:
  r=select(d,model_id=m,panel=kp,gene_view=view,input_mode=mode,support_per_class='100',metric='balanced_accuracy',status='ok',level='cell')
  assert not r.duplicated(['panel','draw']).any();picked.append(r);values.append([]);marks.append([])
  for p in kp:
   q=select(r,panel=p);values[-1].append(numeric(q).mean() if len(q) else np.nan);marks[-1].append('*' if m=='geneformer_lr' else '')
 heat(ax,values,[l for _,l,_,_ in km],['5/A','5/B','9/A','9/B'],marks=marks,bold=True,fontsize=6);ax.set_xlabel('Classes / feature panel');panel_label(ax,'c','Kidney, 100 supports/class')
 src(fid,'c','fig4__cases',pd.concat(picked,ignore_index=True));sources.append('fig4__cases');panels.append(metadata('c','Kidney cell-type evaluation extends the contextual benchmark','fig4__cases',dict(panel=kp,support_per_class='100',metric='balanced_accuracy',level='cell',models=km),len(pd.concat(picked)),'donor-held-out fold','Mean over available folds, separately for feature panels A/B','No inferred intervals; complete folds in source data','Count and processed CellPFN input modes both shown; Geneformer query-source exposure flagged'))
 ax=fig.add_axes([.62,.095,.35,.12]);ax.axis('off');panel_label(ax,'d','Exposure and comparison boundaries')
 ax.text(0,.92,'* PBMC: likely query-cell exposure for\n   Geneformer and scGPT.\n* Held cortex: Geneformer source studies\n   cover 92.6% of query cells.\n(*) Development cortex: possible\n   Geneformer overlap, at most 22.3%.\n   Exact-cell and target-label matches unverified.',fontsize=6.2,va='top',linespacing=1.28,transform=ax.transAxes)
 src(fid,'d','fig2__exposure_marks',EXPOSURE);sources.append('fig2__exposure_marks');panels.append(metadata('d','Pretraining exposure is evidence-qualified','fig2__exposure_marks',{},len(EXPOSURE),'source-study audit','No numerical score adjustment','Not applicable','Unflagged results do not certify no exposure'))
 fig.text(.06,.035,'Values: balanced accuracy (%). Gray * / (*) values: query-source exposure; bold: best overall and best unflagged, including ties.\nFiner tasks are post hoc and do not constitute independent cohorts. TabPFN-3.5: non-commercial research use only.',fontsize=6,color='#444444')
 finish(fig,fid,'Complete biological benchmark and finer annotation','Performance is heterogeneous across methods, annotation resolutions and cohorts.',panels,sorted(set(sources)))


def supp3():
 fid='supp_figure3';panels=[];sources=[]
 fig=plt.figure(figsize=(180/25.4,190/25.4));fig.text(.06,.985,'Gene coverage and preprocessing sensitivity',fontsize=9,fontweight='bold',va='top')
 gs=fig.add_gridspec(3,2,left=.18,right=.98,bottom=.10,top=.91,hspace=.85,wspace=.72,height_ratios=[1.05,1.4,1])
 ax=fig.add_subplot(gs[0,0]);d=select(read('fig2__cases'),model_id='cellpfn_g1v2p',panel=PANELS,support_per_class=BUDGETS,draw=DRAWS,gene_view=['hvg2000','hvg8192','all'],metric='balanced_accuracy',status='ok')
 lab=[];means=[];lo=[];hi=[]
 for p in PANELS:
  for b in BUDGETS:
   r=select(d,panel=p,support_per_class=b,gene_view='hvg8192');v=numeric(r,'n_genes');lab.append(SHORT[p].replace('Cortex ','Cx ')+' / '+b);means.append(v.mean());lo.append(v.min());hi.append(v.max())
 y=np.arange(12);ax.hlines(y,lo,hi,color=TEAL,lw=2);ax.scatter(means,y,s=13,color=TEAL);ax.axvline(8192,color=GRAY,ls='--',lw=.7);ax.set_yticks(y,lab,fontsize=6);ax.invert_yaxis();ax.set_xlim(0,9000);ax.set_xticks([0,4000,8192],['0','4,000','8,192']);ax.set_xlabel('Realized genes (mean and range)');panel_label(ax,'a','Requested 8,192 HVGs')
 src(fid,'a','fig2__cases',d);sources.append('fig2__cases');panels.append(metadata('a','HVG labels denote caps, with reduced realized width at low support','fig2__cases',dict(model_id='cellpfn_g1v2p',gene_view=['hvg2000','hvg8192','all'],metric='balanced_accuracy',draw=DRAWS),len(d),'support draw','8,192-HVG means and min/max over three draws; all/2k widths preserved in source data','Descriptive ranges, not CIs'))
 ax=fig.add_subplot(gs[0,1]);d=select(read('fig2__cells'),model_id='cellpfn_g1v2p',panel=PANELS,support_per_class=BUDGETS,gene_view='all',metric='balanced_accuracy',draw_set='draws_0_19');ordered=pd.concat([select(d,panel=p,support_per_class=b) for p in PANELS for b in BUDGETS]);assert len(ordered)==12
 mid=numeric(ordered,'delta_vs_hvg2000_mean');low=numeric(ordered,'delta_vs_hvg2000_ci95_low');high=numeric(ordered,'delta_vs_hvg2000_ci95_high');ax.errorbar(mid,y,xerr=[mid-low,high-mid],fmt='o',ms=3,color=TEAL,lw=.8,capsize=1);ax.axvline(0,color=GRAY,lw=.6);ax.set_yticks(y,lab,fontsize=6);ax.invert_yaxis();ax.set_xlabel('Balanced-accuracy change (pp)');panel_label(ax,'b','All genes − 2k HVGs, 20 draws');src(fid,'b','fig2__cells',ordered);sources.append('fig2__cells');panels.append(metadata('b','Full-gene effects vary across settings','fig2__cells',dict(model_id='cellpfn_g1v2p',gene_view='all',metric='balanced_accuracy',draw_set='draws_0_19'),12,'paired support draw','Exported mean all-minus-HVG difference','Exported paired 95% t intervals over 20 draws; not training/donor uncertainty'))
 ax=fig.add_subplot(gs[1,0]);views=['rand2000','hvg2000','rand8192','hvg8192','all'];names=['Random 2,000','2k HVGs','Random 8,192','8,192 HVGs','All genes'];d=select(read('fig2__cells'),model_id='cellpfn_g1v2p',panel=PANELS,support_per_class=BUDGETS,gene_view=views,metric='balanced_accuracy',draw_set='draws_0_19')
 for i,v in enumerate(views):
  r=select(d,gene_view=v);assert len(r)==12;vv=numeric(r,'mean');ax.scatter(vv,np.full(12,i)+np.linspace(-.17,.17,12),s=7,c='#9CBDBA',alpha=.7);ax.scatter([vv.mean()],[i],s=28,c=TEAL,marker='D',zorder=3)
 ax.set_yticks(range(5),names);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Balanced accuracy (%)');panel_label(ax,'c','Random and HVG controls');src(fid,'c','fig2__cells',d);panels.append(metadata('c','Random-gene controls contextualize gene selection','fig2__cells',dict(model_id='cellpfn_g1v2p',gene_view=views,draw_set='draws_0_19',metric='balanced_accuracy'),60,'panel–support combination','Small dots: 20-draw means for 12 conditions; diamond: equally weighted condition mean','Condition heterogeneity only; no CI over conditions'))
 ax=fig.add_subplot(gs[1,1]);d=read('supp_stored_zeros__study_gene_availability');r=d.assign(sort=numeric(d,'genes_not_measured_pct')).sort_values('sort');ax.barh(range(len(r)),numeric(r,'genes_not_measured_pct'),color='#91BDB7');ax.set_yticks(range(len(r)),r.study,fontsize=6);ax.set_xlabel('Genes unmeasured in study (%)');panel_label(ax,'d','Stored-zero gene coverage');src(fid,'d','supp_stored_zeros__study_gene_availability',d);sources.append('supp_stored_zeros__study_gene_availability');panels.append(metadata('d','Missing assays are encoded as zeros in the merged cortex matrix','supp_stored_zeros__study_gene_availability',{},len(d),'study','Percentage of 21,158 panel genes unmeasured per study','Descriptive; no uncertainty','Includes support, query and separate sex-case study roles; see source data'))
 ax=fig.add_subplot(gs[2,0]);d=read('supp_stored_zeros__facts');picked=[];vals=[];labels=[]
 for p in ['zebra_dev','zebra_ood']:
  for b in BUDGETS:
   prefix=f'tierD.{p}.b{b}.b_raw_minus_a';r=select(d,key=[prefix,prefix+'_ci_low',prefix+'_ci_high']);assert len(r)==3;picked.append(r);v={x.key:float(x.value) for x in r.itertuples()};vals.append((v[prefix],v[prefix+'_ci_low'],v[prefix+'_ci_high']));labels.append(('Development' if p=='zebra_dev' else 'Held studies')+' / '+b)
 arr=np.array(vals);ax.errorbar(arr[:,0],range(6),xerr=[arr[:,0]-arr[:,1],arr[:,2]-arr[:,0]],fmt='o',ms=3,color=TEAL,capsize=2,lw=.8);ax.axvline(0,color=GRAY,lw=.7);ax.set_yticks(range(6),labels,fontsize=6);ax.invert_yaxis();ax.set_xlabel('Balanced-accuracy change (pp)');panel_label(ax,'e','Remove genes unmeasured in any study');src(fid,'e','supp_stored_zeros__facts',pd.concat(picked));sources.append('supp_stored_zeros__facts');panels.append(metadata('e','Removing stored-zero genes changes performance','supp_stored_zeros__facts',dict(key='tierD.{panel}.b{budget}.b_raw_minus_a and ci_low/ci_high'),18,'paired support draw','Exported difference after removing unmeasured genes; retained values unchanged','Paired 95% t intervals over 10 draws','No renormalization; separate from reconstructed-count experiment'))
 ax=fig.add_subplot(gs[2,1]);d=select(read('supp_stored_zeros__cases'),model_id='cellpfn_g1v2p',panel=['zebra_dev','zebra_ood','zebra_counts_dev','zebra_counts_ood'],support_per_class=BUDGETS,draw=DRAWS,gene_view='all',metric='balanced_accuracy',status='ok');d=d[((d.panel.str.contains('counts')) & (d.input_mode=='count')) | ((~d.panel.str.contains('counts')) & (d.input_mode=='processed'))]
 assert len(d)==36
 for pi,p in enumerate(['zebra_dev','zebra_ood']):
  for mode,label,style in [('processed','processed','-'),('count','counts','--')]:
   pp=p if mode=='processed' else p.replace('zebra_','zebra_counts_');r=select(d,panel=pp);means=[numeric(select(r,support_per_class=b)).mean() for b in BUDGETS];ax.plot(range(3),means,color=TEAL if pi==0 else PURPLE,ls=style,marker='o' if mode=='processed' else 's',ms=3,label=('Dev., ' if pi==0 else 'Held, ')+label)
 ax.set_xticks(range(3),BUDGETS);ax.set_ylim(0,102);ax.set_xlabel('Supports per class');ax.set_ylabel('Balanced accuracy (%)');ax.legend(frameon=False,fontsize=6,loc='lower right');panel_label(ax,'f','Processed versus reconstructed counts');src(fid,'f','supp_stored_zeros__cases',d);sources.append('supp_stored_zeros__cases');panels.append(metadata('f','Count reconstruction changes multiple inputs simultaneously','supp_stored_zeros__cases',dict(model_id='cellpfn_g1v2p',gene_view='all',metric='balanced_accuracy',draw=DRAWS,input_mode='count for counts panels; processed otherwise'),36,'support draw','Mean over three draws per panel/budget','No confidence interval','21,158 processed versus 12,325 count genes; some support identities differ'))
 fig.text(.06,.025,'The same CellPFN checkpoint is used throughout. Supports/class are shown after “/”.\nIntervals in b and e condition on the checkpoint and fixed query cells. Count reconstruction is not an isolated normalization test.',fontsize=6,color='#444444')
 finish(fig,fid,'Gene coverage and preprocessing sensitivity','Gene coverage and missing-assay encoding affect performance and qualify scaling comparisons.',panels,sorted(set(sources)))


def supp9():
 fid='supp_figure9';panels=[];sources=[]
 fig=plt.figure(figsize=(180/25.4,180/25.4));fig.text(.06,.985,'Recorded computational costs and timing boundaries',fontsize=9,fontweight='bold',va='top')
 gs=fig.add_gridspec(2,2,left=.19,right=.98,bottom=.14,top=.91,hspace=.75,wspace=.8)
 ax=fig.add_subplot(gs[0,0]);d=select(read('fig3__finetune_cost'),finetune_arm=['c2b','k2b_s','k2b_l'])
 for arm,label,c in [('c2b','TabICLv2',BLUE),('k2b_s','Kumo small',COLORS['kumo_small']),('k2b_l','Kumo large',PURPLE)]:
  r=select(d,finetune_arm=arm).copy();r['sort']=numeric(r,'tasks_seen');r=r.sort_values('sort');ax.plot(numeric(r,'tasks_seen')/1000,numeric(r,'gpu_hours_compute_cumulative'),color=c,marker='o',ms=3,label=label)
 ax.set_xlim(0,42);ax.set_ylim(0,6);ax.set_xticks([0,10,20,40]);ax.set_xlabel('Additional cellular tasks (thousands)');ax.set_ylabel('Cumulative optimizer compute (h)');ax.legend(frameon=False,loc='upper left',fontsize=6);panel_label(ax,'a','Measured adaptation compute')
 ax.text(0,-.27,'GPU-lock wait at 40k: 0 / 3.54 / 10.17 h\n(TabICLv2 / Kumo small / Kumo large)',transform=ax.transAxes,fontsize=6,va='top');src(fid,'a','fig3__finetune_cost',d);sources.append('fig3__finetune_cost');panels.append(metadata('a','Additional adaptation has recorded optimizer costs','fig3__finetune_cost',dict(finetune_arm=['c2b','k2b_s','k2b_l']),len(d),'training update','Cumulative measured per-update compute on one H100 80 GB','One training seed; no uncertainty','Excludes vendor pretraining, evaluation, startup and checkpoint IO; waiting separate; +25% replay beyond plotted cellular tasks'))
 cases=['pbmc_l1_b10_s0','pbmc_l1_b10_s1','pbmc_l1_b100_s0','zebra_dev_b10_s0','kidney_core9_A_F0_count','kidney_core9_A_F0_processed'];labels=['PBMC, 10, draw 0','PBMC, 10, draw 1','PBMC, 100','Cortex dev., 10','Kidney, counts','Kidney, processed']
 routes=read('fig5__cost_by_route');d=select(routes,model_id='cellpfn_g1v2p',case_id=cases,route=['dsloo_plus_correction','ig64'],status='measured')
 ax=fig.add_subplot(gs[0,1])
 for ri,(route,label,c,m) in enumerate([('dsloo_plus_correction','DS-LOO + correction',TEAL,'o'),('ig64','IG64',PURPLE,'s')]):
  for i,case in enumerate(cases):
   r=select(d,case_id=case,route=route,timing_context='run_case_and_first_run');assert len(r)==1
   ax.scatter(numeric(r,'seconds')/60,[i+(ri-.5)*.2],c=c,marker=m,s=20,label=label if i==0 else None)
   r=select(d,case_id=case,route=route,timing_context='load_matched')
   if len(r):ax.scatter(numeric(r,'seconds')/60,[i+(ri-.5)*.2],facecolors='none',edgecolors=c,marker='o',s=25,label='DS-LOO, retimed' if i==2 else None)
 ax.set_yticks(range(6),labels,fontsize=6);ax.invert_yaxis();ax.set_xlim(0,7);ax.set_xlabel('Recorded elapsed time (min)');ax.legend(frameon=False,fontsize=6,loc='center right',bbox_to_anchor=(1,.39));panel_label(ax,'b','Measured attribution routes');src(fid,'b','fig5__cost_by_route',d);sources.append('fig5__cost_by_route');panels.append(metadata('b','Measured attribution timing depends on route and GPU load','fig5__cost_by_route',dict(model_id='cellpfn_g1v2p',route=['dsloo_plus_correction','ig64'],status='measured'),len(d),'timed case','Seconds converted to minutes; original and available retimed DS-LOO shown','No error bars; reruns are not independent model replicates','Shared GPU; explained cells and scope in source data; IG64 was not load-matched to every rerun'))
 ax=fig.add_subplot(gs[1,0]);d=select(routes,model_id='cellpfn_g1v2p',case_id=cases,route='exact_ko_all_genes_explained_cells',status='inferred')
 for ctx,c,marker,label in [('run_case_and_first_run',GRAY,'s','Original timing'),('load_matched',TEAL,'o','Load-matched timing')]:
  for i,case in enumerate(cases):
   r=select(d,case_id=case,timing_context=ctx)
   if len(r):ax.scatter(numeric(r,'seconds')/3600,[i],color=c,marker=marker,s=20,label=label if (i==0 and ctx=='run_case_and_first_run') or (i==2 and ctx=='load_matched') else None)
 ax.set_yticks(range(6),labels,fontsize=6);ax.invert_yaxis();ax.set_xlim(0,65);ax.set_xlabel('Extrapolated exact-deletion time (h)');ax.legend(frameon=False,fontsize=6,loc='lower right');panel_label(ax,'c','Inferred all-gene exact deletion');src(fid,'c','fig5__cost_by_route',d);panels.append(metadata('c','Full all-gene exact deletion cost is extrapolated','fig5__cost_by_route',dict(model_id='cellpfn_g1v2p',route='exact_ko_all_genes_explained_cells',status='inferred'),len(d),'case timing extrapolation','Single-gene timing scaled across all genes; seconds to hours','No confidence interval','Full all-gene exact runs were not measured; original and load-matched timing contexts differ'))
 ax=fig.add_subplot(gs[1,1]);d=select(read('fig5__cost_kumo_estimated'),model_id=['kumo_small','kumo_large'],kumo_task=['pbmc_l1','pbmc_l2','zebra_dev','zebra_ood'],kumo_panel=['pbmc','zebra'],gene_view='hvg2000',route='A_library_as_is',status='estimated');tasks=['pbmc_l1','pbmc_l2','zebra_dev','zebra_ood']
 assert len(d)==8
 for i,(m,label,c,marker) in enumerate([('kumo_small','Kumo small',COLORS['kumo_small'],'o'),('kumo_large','Kumo large',PURPLE,'s')]):
  for j,p in enumerate(tasks):
   r=select(d,model_id=m,kumo_task=p);assert len(r)==1;ax.scatter(numeric(r,'hours'),[j+(i-.5)*.18],color=c,marker=marker,s=22,label=label if j==0 else None)
 ax.set_yticks(range(4),[SHORT[p] for p in tasks],fontsize=6);ax.invert_yaxis();ax.set_xlim(left=0);ax.set_xlabel('Estimated library-loop deletion time (h)');ax.legend(frameon=False,fontsize=6,loc='upper right');panel_label(ax,'d','Estimated Kumo, 2k HVGs');src(fid,'d','fig5__cost_kumo_estimated',d);sources.append('fig5__cost_kumo_estimated');panels.append(metadata('d','Kumo knockout costs are modelled estimates','fig5__cost_kumo_estimated',dict(model_id=['kumo_small','kumo_large'],kumo_task=tasks,kumo_panel=['pbmc','zebra'],gene_view='hvg2000',route='A_library_as_is',status='estimated'),8,'case-family timing estimate','Recorded forward median multiplied by library-loop forward count','No confidence interval','No full deletion implementation timed; differs from CellPFN in query counts, gene coverage, precision and GPU conditions'))
 fig.text(.06,.04,'Measured (a,b), extrapolated (c), and estimated (d) quantities are shown separately. Timings are descriptive, not controlled speedups.\nAttribution: fp32 CellPFN; Kumo estimates: fp16, different cell/gene scopes. No numerical simulator-throughput claim is made.',fontsize=6,color='#444444')
 finish(fig,fid,'Recorded computational costs','Existing logs quantify selected computation while their scope prevents universal speed claims.',panels,sorted(set(sources)),extra={'timing_claim_status':'Provisional; shared-GPU and scope differences retained'})

if __name__=='__main__':
 figure2();supp2();supp3();supp9()
