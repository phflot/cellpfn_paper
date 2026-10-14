#!/usr/bin/env python3
"""Source-bound simulator, ablation and phenotype supplementary figures.

Python-only rendering. Raw exports are immutable; every displayed selection and
derived value is saved with source provenance. One model seed underlies all
training arms; support/task-stream variation is not model-seed replication.
"""
from pathlib import Path
import argparse
import json
import sys
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from figures_common import (ROOT, FIGURES, TEAL, BLUE, PURPLE, GRAY, PANELS,
                            read, select, numeric, panel_label, write_source,
                            save_figure, plt)

ORANGE = '#BD6C38'
PANEL_SHORT = {'pbmc_l1':'PBMC coarse', 'pbmc_l2':'PBMC fine',
               'zebra_dev':'Cortex dev.', 'zebra_ood':'Cortex held'}


def rec(letter, claim, source, filters, n, uncertainty, **extra):
    return dict(letter=letter, claim=claim, source=source, filters=filters,
                n=n, uncertainty=uncertainty, **extra)


def legend_file(number, title, text):
    (ROOT/'sections'/f'legend_supp_figure{number}.tex').write_text(
        r'\textbf{'+title+'} '+text+'\n')


def finish(fig, fid, **kwargs):
    """Optional installed-skill alignment gate; figure remains portable."""
    skill = Path('/home/phflot/.codex/skills/nature-figure/scripts')
    if skill.exists():
        sys.path.insert(0, str(skill))
        from audit_panel_alignment import require_matplotlib_panel_alignment
        require_matplotlib_panel_alignment(
            fig, json_out=str(FIGURES/f'{fid}.alignment.json'),
            tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=True)
    save_figure(fig, fid, **kwargs)


def build_s1():
    fid='supp_figure1'
    source='fig7__sim_vs_real_summary'
    d=read(source)
    specs=[
      ('A class: strongest marker per pair','Strongest class marker','Absolute log2 fold change',1),
      ('A class: share DE with |LFC|>2','Large class effects','Fraction of genes',1),
      ('A class: separability BA B10, K-matched (real K8, 64 cells; primary)','Task separability: 10 supports','Chance-adjusted accuracy',1),
      ('A class: separability BA B100, K-matched (real K8, 64 cells; primary)','Task separability: 100 supports','Chance-adjusted accuracy',1),
      ('B donor: SD within study, 4x2 design (primary)','Within-study donor variation','SD (log2 expression)',1),
      ('B donor: >=10x on-switches (4x2)','Large donor on-switches','Fraction of genes',1),
      ('B donor: silenced pairs, 4x2 design (primary)','Donor silencing','Fraction of gene–donor pairs',1),
      ('D marginal: NB phi','Count overdispersion','Negative-binomial dispersion',1),
      ('D marginal: zero excess','Excess zeros','Fraction',1),
      ('D marginal: detected-gene fraction','Gene detection','Fraction of genes',1),
      ('E gene-gene: LDA gain B10 (full - diagonal), K-matched (real K8, 64 cells)','Gene–gene signal: 10 supports','Full minus diagonal LDA (pp)',100),
      ('E gene-gene: LDA gain B100 (full - diagonal), K-matched (real K8, 64 cells)','Gene–gene signal: 100 supports','Full minus diagonal LDA (pp)',100),
    ]
    fig,axes=plt.subplots(4,3,figsize=(180/25.4,184/25.4))
    fig.subplots_adjust(left=.135,right=.98,bottom=.065,top=.865,wspace=.55,hspace=1.12)
    fig.text(.04,.98,'Calibration covers several biological effects, with important distributional mismatches',
             va='top',fontsize=8,fontweight='bold')
    fig.text(.04,.95,'Synthetic: median, 25–75% and 5–95%  |  Public reference: median and range',fontsize=7)
    panels=[]; selected=[]
    for idx,(effect,title,unit,factor) in enumerate(specs):
        ax=axes.flat[idx]; letter=chr(97+idx)
        x=select(d,effect=effect,prior_id=['v1_late','v2.2-B'])
        assert len(x)==2,(effect,len(x))
        x=x.copy();x['display_scale']=factor;x['display_panel']=letter
        write_source(fid,letter,x);selected.append(x)
        current=select(x,prior_id='v2.2-B').iloc[0]
        for prior,y,color in [('v1_late',2,GRAY),('v2.2-B',1,TEAL)]:
            r=select(x,prior_id=prior).iloc[0]
            q=np.array([float(r['syn_'+k])*factor for k in ['q05','q25','q50','q75','q95']])
            assert np.all(np.diff(q)>=0)
            ax.plot(q[[0,4]],[y,y],color=color,lw=1)
            ax.plot(q[[1,3]],[y,y],color=color,lw=5,solid_capstyle='butt',alpha=.55)
            ax.scatter(q[2],y,color=color,s=16,zorder=3)
        lo,med,hi=[float(current[k])*factor for k in ['real_min','real_q50','real_max']]
        ax.errorbar(med,0,xerr=[[med-lo],[hi-med]],fmt='D',ms=3.3,color=BLUE,capsize=2)
        ax.set_yticks([0,1,2],['Public ref.','Cellular','Baseline'])
        ax.set_ylim(-.55,2.55);ax.set_xlabel(unit)
        ax.tick_params(axis='y',length=0)
        ax.set_title(title,loc='left',pad=18)
        ax.text(0,1.04,f"Real units: {int(float(current.real_n_units))}; cellular: {current.verdict}",
                transform=ax.transAxes,fontsize=6,va='bottom')
        panel_label(ax,letter)
        panels.append(rec(letter,title,source,dict(effect=effect,prior_id=['v1_late','v2.2-B']),
                          {'real_units':int(float(current.real_n_units)),
                           'synthetic_units':{r.prior_id:int(float(r.syn_n_units)) for r in x.itertuples()},
                           'synthetic_banks':{r.prior_id:int(float(r.syn_n_banks)) for r in x.itertuples()}},
                          'Synthetic median/IQR/5–95%; real median and min–max; not confidence intervals',
                          display_scale=factor,exclusions='All real summaries exclude ROSMAP; fresh synthetic banks, not independent real validation'))
    a=select(d,effect=specs[0][0],prior_id='v2.2-B').iloc[0]
    assert abs(float(a.syn_q50)-6.23)<.02
    finish(fig,fid,title='Simulator calibration and task diversity',
           claim='The cellular prior broadens biological effect coverage but retains excessive separability and noise relative to calibrated public references.',
           panels=panels,sources=[source],extra={'archetype':'quantitative grid',
           'numeric_anchors':{'strongest_marker_cellular_median':float(a.syn_q50)},
           'real_reference':'PBMC, human ZEBRA cortex and kidney; calibration and evaluation datasets overlap',
           'training_exposure':'Cellular prior supplies the final 64000 of 384000 scheduled CellPFN episodes; all cellular adaptation episodes use it.'})
    legend_file(1,'Calibration covers biological effects while retaining distributional mismatches.',
        r'''\textbf{a,b}, Strongest class marker and fraction of differentially expressed genes with absolute log$_2$ fold change above two. \textbf{c,d}, Chance-adjusted nearest-class-mean balanced accuracy on eight-class tasks with ten or 100 supports per class. \textbf{e--g}, Within-study donor variation, tenfold on-switches and silencing. \textbf{h--j}, Count dispersion, excess zeros and detection. \textbf{k,l}, Full minus diagonal LDA accuracy; pp, percentage points. Synthetic circles, thick segments and whiskers show median, interquartile range and fifth--95th percentiles. Public-reference diamonds and whiskers show median and range; none are confidence intervals. Real units number 142 (a,b), eight (c,d,k,l), eleven (e--g) and 79 (h--j). The cellular prior uses 128 fresh banks; class-effect/separability summaries exclude signed-covariance banks, leaving 96. Source Data give exact counts. Real units summarize matched draws whereas synthetic units are individual draws, preventing matched-tail inference. Public references are PBMC, human cortex and kidney; ROSMAP is excluded. These datasets informed calibration and evaluation, so this is not independent real-data validation. Coverage labels retain the exported judgments. CellPFN received this prior in only its final 64,000 of 384,000 scheduled episodes.''')


def build_s4():
    fid='supp_figure4';paired=read('fig6__operator_paired_by_view')
    d=select(paired,metric='balanced_accuracy',gene_view=['all','hvg8192','hvg2000'])
    contrasts=[('cellpfn_g1v2p','cellpfn_c1v2p','Full − none',TEAL,'o'),
               ('cellpfn_d1v2p','cellpfn_c1v2p','Diagonal − none',BLUE,'s'),
               ('cellpfn_g1v2p','cellpfn_d1v2p','Full − diagonal',ORANGE,'^')]
    rows=[(p,str(b)) for p in PANELS for b in [1,10,100]]
    fig=plt.figure(figsize=(180/25.4,182/25.4));gs=fig.add_gridspec(2,3,height_ratios=[1.5,1],
      left=.18,right=.975,top=.89,bottom=.095,hspace=.48,wspace=.38)
    axes=[fig.add_subplot(gs[0,i]) for i in range(3)]
    panels=[]
    fig.text(.035,.978,'Operator effects depend on gene coverage and support size',fontsize=8,fontweight='bold',va='top')
    fig.legend(handles=[Line2D([],[],marker=m,color=c,label=n,lw=1,ms=4) for _,_,n,c,m in contrasts],
               ncol=3,loc='upper center',bbox_to_anchor=(.57,.958),frameon=False)
    for j,(view,title) in enumerate([('all','All genes'),('hvg8192','Up to 8,192 HVGs'),('hvg2000','Up to 2k HVGs')]):
        ax=axes[j];selected=[]
        for k,(a,b,name,color,marker) in enumerate(contrasts):
            x=select(d,gene_view=view,model_a=a,model_b=b)
            assert len(x)==12 and set(x.n_draws)=={'20'}
            selected.append(x)
            for i,(panel,budget) in enumerate(rows):
                r=select(x,panel=panel,support_per_class=budget).iloc[0]
                val,lo,hi=map(float,[r.mean_diff,r.ci95_lo,r.ci95_hi])
                ax.errorbar(val,i+(k-1)*.22,xerr=[[val-lo],[hi-val]],fmt=marker,ms=2.8,
                            color=color,capsize=1.4,lw=.8)
        for y in [2.5,5.5,8.5]:ax.axhline(y,color='.9',lw=.6)
        ax.axvline(0,color=GRAY,lw=.7);ax.set_ylim(11.7,-.7);ax.set_xlim(-5.5,10.5)
        ax.set_xticks([-5,0,5,10]);ax.set_xlabel('Paired change in accuracy (pp)')
        labels=[f'{PANEL_SHORT[p]} · {b}' for p,b in rows]
        ax.set_yticks(range(12),labels if j==0 else [])
        panel_label(ax,chr(97+j),title)
        write_source(fid,chr(97+j),pd.concat(selected))
        panels.append(rec(chr(97+j),'Trained operator contrasts by support budget','fig6__operator_paired_by_view',
                         dict(metric='balanced_accuracy',gene_view=view,contrasts=[(a,b) for a,b,*_ in contrasts]),
                         '20 paired support draws per task/budget; one training seed per arm',
                         'Exported paired 95% t intervals',
                         note='At one support per class the operator gate is zero; differences reflect trained-network differences.'))
    ax=fig.add_subplot(gs[1,:2]);n3=read('fig6__operator_n3_test_wide');write_source(fid,'d',n3)
    for i,r in enumerate(n3.itertuples()):
        v,l,h=map(float,[r.delta_ba,r.delta_lo,r.delta_hi]);c=ORANGE if float(r.delta_ba)<-float(r.theta) else TEAL
        ax.errorbar(v,i,xerr=[[v-l],[h-v]],fmt='o',color=c,ms=4,capsize=3)
        for sign in [-1,1]:ax.plot(sign*float(r.theta),i,marker='|',color='black',ms=13,mew=1)
        ax.text(7.1,i,str(r.interval_coverage).split(' (')[0],fontsize=6,va='center')
    ax.set_yticks(range(3),[f'{PANEL_SHORT[r.panel]} · {r.support_per_class}' for r in n3.itertuples()])
    ax.set_ylim(2.6,-.65);ax.set_xlim(-4.5,9.2);ax.axvline(0,color=GRAY,lw=.6)
    ax.set_xlabel('Full minus none, accuracy (pp)');panel_label(ax,'d','Prespecified criterion: not supported')
    fig.text(.18,.018,'Vertical ticks in d: ± harm/gain threshold; interval coverage shown at right.',fontsize=6)
    panels.append(rec('d','The prespecified operator test failed on coarse PBMC at ten supports','fig6__operator_n3_test_wide',{},
                     'Three frozen support draws; PBMC four query donors; cortex donor bootstrap within study',
                     'Original PBMC donor-enumeration interval ~80%; cortex 95%; not homogenized',
                     numeric_anchors={'harm_delta':-1.5625,'harm_threshold':1.5},verdict='NOT SUPPORTED'))
    ax=fig.add_subplot(gs[1,2]);control=read('fig6__operator_prereg_cases')
    filters=dict(checkpoint_update='96000',model_id=['cellpfn_g1v2p','cellpfn_g1v2p_rank0','cellpfn_g1v2p_opoff'])
    selected=[]
    for i,(panel,budget) in enumerate([('pbmc_l1','100'),('zebra_ood','10')]):
        for k,(model,color,marker,label) in enumerate([('cellpfn_g1v2p',TEAL,'o','Full'),
                      ('cellpfn_g1v2p_rank0',BLUE,'s','Rank 0'),('cellpfn_g1v2p_opoff',GRAY,'^','Off')]):
            x=select(control,**{**filters,'model_id':model},panel=panel,support_per_class=budget,status='ok')
            assert len(x)==3
            selected.append(x);values=numeric(x,'ba_pct');mean=values.mean()
            ax.errorbar(i+(k-1)*.22,mean,yerr=[[mean-values.min()],[values.max()-mean]],
                        fmt=marker,ms=4,color=color,capsize=2,label=label if i==0 else None)
            ax.scatter(np.repeat(i+(k-1)*.22,3),values,s=7,facecolors='none',edgecolors=color,linewidths=.5)
    ax.set_xticks([0,1],['PBMC coarse\n100 supports','Cortex held\n10 supports'])
    ax.set_ylabel('Balanced accuracy (%)');ax.set_ylim(78,96)
    ax.legend(loc='lower left',frameon=False)
    panel_label(ax,'e','Inference-only interventions')
    write_source(fid,'e',pd.concat(selected))
    panels.append(rec('e','Removing an operator at inference differs from training without it',
                         'fig6__operator_prereg_cases',filters,
                         'Three frozen support draws per condition', 'Mean and observed min–max, with all draw values',
                         exclusions='Selected original primary examples; inference interventions are not separately trained diagonal/none arms.'))
    finish(fig,fid,title='Gene–gene operator ablations and prespecified test',
           claim='The trained operator gives context-dependent gains; its prespecified overall support criterion failed.',
           panels=panels,sources=['fig6__operator_paired_by_view','fig6__operator_n3_test_wide','fig6__operator_prereg_cases'])
    legend_file(4,'Operator effects depend on support and gene coverage; the prespecified test was not supported.',
        r'''\textbf{a--c}, Separately trained full, diagonal and no-operator balanced-accuracy contrasts using all genes, up to 8,192 HVGs or up to 2k HVGs. Rows specify panel and supports per class. Points and bars show paired means and 95\% $t$ intervals over twenty support draws, conditional on one training seed per arm and fixed queries. HVG widths are requested caps. At one support, the operator gate is zero; differences reflect trained-network differences. \textbf{d}, Original prespecified test using three frozen draws. Black ticks mark thresholds. Coarse-PBMC ten-support balanced accuracy crossed the $-1.50$-point harm threshold ($-1.5625$ points), triggering the overall failed criterion. PBMC bars use four-donor enumeration with approximately 80\% coverage; held-study cortex uses a 95\% donor bootstrap within study. The later twenty-draw estimates do not overturn that decision. \textbf{e}, Full-model rank-zero and operator-off interventions at inference, showing all three draws, means and ranges. These differ from the separately trained arms in a--c. All checkpoints are at update 96,000; no interval measures training-seed variation. pp, percentage points. Source Data retain the exact contrasts, intervals and control observations.''')


def build_s5():
    fid='supp_figure5';outcomes=read('supp_prior_ablation__outcomes')
    short={'LR':'Task restriction','A5':'Weaker class effects','A6':'No covariance lane',
           'A7':'Donor dominance','A8a':'Gene absence','A8d':'Study detection',
           'A1':'More donors','A3':'Sex mechanisms','A2':'Adult-age prior','A4':'Weak metadata'}
    status={'LR':'Keep','A5':'Drop','A6':'Neutral','A7':'Unresolved','A8a':'Drop (guard)',
            'A8d':'Not testable','A1':'Routing only','A3':'Routing only','A2':'Routing only','A4':'Routing only'}
    fig=plt.figure(figsize=(180/25.4,189/25.4));gs=fig.add_gridspec(3,2,
       height_ratios=[1.3,1,1.15],left=.19,right=.98,bottom=.06,top=.93,hspace=.75,wspace=.75)
    panels=[]
    fig.text(.035,.985,'Task restriction improves proxy accuracy but changes calibration and exposure',
             fontsize=8,fontweight='bold',va='top')
    ax=fig.add_subplot(gs[0,0]);arms=['LR','A5','A6','A7','A8a','A8d'];x=select(outcomes,arm=arms)
    def candidate_axes(ax, arms, xlabel, letter, title):
        dat=select(outcomes,arm=arms)
        for i,arm in enumerate(arms):
            r=select(dat,arm=arm).iloc[0];values=np.array([float(r[k]) for k in ['r42','r43','r44']]);m=float(r['mean'])
            color=TEAL if arm=='LR' else (ORANGE if arm=='A5' else GRAY)
            ax.plot([float(r.band_eff),float(r.band_eff)],[i-.27,i+.27],color='.65',lw=1)
            ax.plot(float(r.keep),i,marker='|',color=BLUE,ms=10,mew=1)
            ax.scatter(values,np.array([-.13,0,.13])+i,s=14,marker='o',facecolors='none',edgecolors=color,zorder=3)
            ax.plot(m,i,'D',ms=3.5,color=color)
        ax.axvline(0,color=GRAY,lw=.7);ax.set_ylim(len(arms)-.5,-.6)
        ax.set_yticks(range(len(arms)),[f'{a}: {short[a]}\n{status[a]}' for a in arms])
        ax.set_xlabel(xlabel);panel_label(ax,letter,title)
        write_source(fid,letter,dat)
        panels.append(rec(letter,title,'supp_prior_ablation__outcomes',{'arm':arms},
                    'Three paired task-stream replicates, one model seed',
                    'Each replicate and mean; effective noise-band and keep thresholds, not confidence intervals',
                    aggregation='Improvement-signed difference against each arm-specific base; endpoints retained separately',
                    source_labels='Frozen outcome labels retained in source; routing only means proxy cannot decide donor/weak-task efficacy'))
    candidate_axes(ax,arms,'Improvement in balanced accuracy (pp)','a','Accuracy endpoints: six candidates')
    ax.set_xlim(-2.1,3.1)
    # Right upper cell subdivides endpoint units rather than mixing AUC and nats.
    inner=gs[0,1].subgridspec(2,1,height_ratios=[3,1],hspace=1.25)
    ax=fig.add_subplot(inner[0,0]);candidate_axes(ax,['A1','A3','A2'],'Improvement in unit AUC','b','Donor endpoints: reported only')
    ax.set_xlim(-.025,.15)
    ax=fig.add_subplot(inner[1,0]);candidate_axes(ax,['A4'],'Reduction in NLL (nats)','c','Weak-task calibration endpoint')
    ax.set_xlim(-.045,.06)
    # Task composition and exact materialized row exposure are separate evidence.
    comp=read('fig6__taskmix_stream_composition');ax=fig.add_subplot(gs[1,0])
    categories=[('metadata_binary','Binary metadata',GRAY),('metadata_categorical','Categorical metadata','#9EA8AE'),
                ('cell_type','Cell type',TEAL),('donor_identity','Donor identity',PURPLE)]
    for i,(model,name) in enumerate([('cellpfn_gs1','Standard'),('cellpfn_gl1','Restricted')]):
        left=0
        for cat,label,color in categories:
            q=select(comp,model_id=model,quantity='families',category=cat)
            n=float(q.iloc[0].value) if len(q) else 0
            if not n:continue
            ax.barh(i,n/160,left=left,color=color,height=.5,label=label if i==0 else None)
            if n/160>10:ax.text(left+n/320,i,f'{n/160:.0f}%',ha='center',va='center',fontsize=6,color='white' if color!= '#9EA8AE' else 'black')
            left+=n/160
        assert abs(left-100)<1e-9
    ax.set_yticks([0,1],['Standard','Restricted']);ax.set_xlim(0,100);ax.set_ylim(1.65,-.65)
    ax.set_xlabel('Share of 16,000 additional tasks (%)')
    ax.legend(loc='upper center',bbox_to_anchor=(.45,-.33),ncol=2,frameon=False,columnspacing=.8)
    panel_label(ax,'d','The task family distribution changes')
    dat=select(comp,quantity='families');write_source(fid,'d',dat)
    panels.append(rec('d','Restricted training removes metadata tasks','fig6__taskmix_stream_composition',{'quantity':'families'},
                     '16000 tasks per arm','Exact task counts; no intervals'))
    ax=fig.add_subplot(gs[1,1]);dat=select(comp,quantity='cells_per_update',category='total')
    assert len(dat)==2
    vals=[]
    for model in ['cellpfn_gs1','cellpfn_gl1']:vals.append(float(select(dat,model_id=model).iloc[0].value))
    ax.bar([0,1],np.array(vals)/1e6,color=[GRAY,TEAL],width=.58)
    for i,v in enumerate(vals):ax.text(i,v/1e6+.25,f'{v/1e6:.3f} M',ha='center',fontsize=7)
    ax.set_xticks([0,1],['Standard','Restricted']);ax.set_ylabel('Cell exposures (millions)');ax.set_ylim(0,12.3)
    panel_label(ax,'e','CellPFN cell exposure is unequal')
    write_source(fid,'e',dat)
    panels.append(rec('e','Equal additional updates do not match materialized cell exposure','fig6__taskmix_stream_composition',
                     {'quantity':'cells_per_update','category':'total'},'4000 updates per arm',
                     'Exact recorded counts; repeated cell exposures, not unique cells',
                     numeric_anchors={'standard':vals[0],'restricted':vals[1],'ratio':vals[1]/vals[0]}))
    paired=read('fig6__taskmix_paired')
    for j,(metric,title,unit) in enumerate([('balanced_accuracy','Accuracy change','Restricted minus standard (pp)'),
                                         ('nll','Log-loss change','Restricted minus standard NLL (nats)')]):
        ax=fig.add_subplot(gs[2,j]);x=select(paired,metric=metric,model_a='cellpfn_gl1',model_b='cellpfn_gs1',gene_view='all')
        assert len(x)==12 and set(x.n_draws)=={'20'}
        for k,(panel,color,marker) in enumerate(zip(PANELS,[TEAL,BLUE,PURPLE,ORANGE],['o','s','^','D'])):
            pp=select(x,panel=panel).copy();pp['budget_num']=numeric(pp,'support_per_class');pp=pp.sort_values('budget_num')
            mean=numeric(pp,'mean_diff').to_numpy();low=numeric(pp,'ci95_lo').to_numpy();hi=numeric(pp,'ci95_hi').to_numpy()
            ax.errorbar(np.arange(3)+(k-1.5)*.13,mean,yerr=[mean-low,hi-mean],fmt=marker,ms=3.5,
                        color=color,capsize=2,label=PANEL_SHORT[panel])
        ax.axhline(0,color=GRAY,lw=.7);ax.set_xticks(range(3),['1','10','100']);ax.set_xlabel('Supports per class');ax.set_ylabel(unit)
        if j==0:ax.legend(loc='upper right',frameon=False,ncol=2,columnspacing=.7,handletextpad=.3)
        panel_label(ax,chr(102+j),title)
        write_source(fid,chr(102+j),x)
        panels.append(rec(chr(102+j),title,'fig6__taskmix_paired',{'metric':metric,'model_a':'cellpfn_gl1','model_b':'cellpfn_gs1','gene_view':'all'},
                         '20 paired support draws per task/budget, one training run per arm',
                         'Exported paired 95% t intervals; no model-seed replication',
                         note='4,000 additional updates; unequal cell exposures and simultaneous task-family/lane changes preclude an isolated causal task-difficulty effect.'))
    assert len(outcomes)==10 and sum(len(p['filters'].get('arm',[])) for p in panels[:3])==10
    finish(fig,fid,title='Prior interventions and task-mixture tradeoffs',
           claim='Task restriction improves proxy low-support accuracy but changes training composition and exposure and incurs calibration tradeoffs.',
           panels=panels,sources=['supp_prior_ablation__outcomes','fig6__taskmix_stream_composition','fig6__taskmix_paired'],
           extra={'numeric_anchors':{'LR_mean':float(select(outcomes,arm='LR').iloc[0]['mean']),
                                    'total_candidates':10},'axes_units':'Accuracy, AUC and NLL are never combined on one numerical axis.'})
    legend_file(5,'Task restriction improves proxy accuracy with calibration and exposure tradeoffs.',
        r'''\textbf{a--c}, All ten prior candidates on the Kumo-small proxy after 10,000 cellular tasks, 625 updates and up to 2k HVGs. Open circles are three paired task-stream replicates from one model seed; diamonds are means. Gray/blue ticks mark the effective noise band/keep threshold. Positive differences favour each candidate against its specified base. Accuracy endpoints differ across candidates; donor AUC and NLL reduction use separate axes. Supplementary Table~\ref{tab:s5} defines bases and endpoints. Routing-only labels are not efficacy decisions; A8d is not testable because proxy headroom is insufficient. \textbf{d,e}, CellPFN continuation over 4,000 updates and 16,000 tasks per arm. Standard training supplied 12,816 metadata, 2,398 cell-type and 786 donor-identity tasks; restriction supplied 12,001 cell-type and 3,999 donor-identity tasks and excluded signed-covariance banks. Cell exposures were 6,386,352 versus 10,671,056 (1.67-fold), including reuse. \textbf{f,g}, Restricted minus standard balanced accuracy and NLL at update 100,000 with all genes: paired means and 95\% $t$ intervals over twenty support draws. Positive NLL change is worse. Task composition, bank acceptance and cell exposure change together; intervals do not cover training-seed variation. pp, percentage points. Source Data retain full frozen decisions and numerical summaries.''')


def raw_splits(ax, d, groups, ylabel, *, chance=None, ylim=None, color=TEAL):
    """Display every repeated support split plus mean/min–max; no CI."""
    means=[]
    for i,filters in enumerate(groups):
        x=select(d,**filters);assert len(x)==10,(filters,len(x))
        values=numeric(x).to_numpy();m=values.mean();means.append(m)
        ax.scatter(i+np.linspace(-.11,.11,len(values)),values,s=12,facecolors='none',edgecolors=color,lw=.6,zorder=3)
        ax.errorbar(i,m,yerr=[[m-values.min()],[values.max()-m]],fmt='D',color=color,ms=4,capsize=3,zorder=4)
    if chance is not None:ax.axhline(chance,color=GRAY,ls='--',lw=.7)
    if ylim:ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    return means


def build_s6():
    fid='supp_figure6';raw=read('supp_taskmix_tradeoff__efast_cases')
    d=select(raw,model_id='cellpfn_g1v2p',checkpoint_update='96000',status='ok')
    fig=plt.figure(figsize=(180/25.4,153/25.4));gs=fig.add_gridspec(2,3,left=.09,right=.98,bottom=.11,top=.90,
      hspace=.60,wspace=.50,height_ratios=[1,1.05]);panels=[]
    fig.text(.035,.985,'Sex and age prediction depend strongly on the task population',fontsize=8,fontweight='bold',va='top')
    fig.text(.035,.95,'Reference CellPFN checkpoint  |  Ten repeated splits for unit-level tasks; no independent-cohort replication',fontsize=7)
    ax=fig.add_subplot(gs[0,0]);s=read('fig6__operator_prereg_cases')
    x=select(s,panel='zebra_sex',model_id='cellpfn_g1v2p',checkpoint_update='96000',draw='0',support_per_class='100',status='ok')
    assert len(x)==2
    for i,unit in enumerate(['cell','gsm']):
        q=select(x,scoring_unit=unit)
        assert len(q)==1
        ax.plot(i,float(q.iloc[0].ba_pct),'D',ms=5,color=TEAL)
    ax.set_xticks([0,1],['50 cells','10 GSM samples']);ax.set_ylim(45,105)
    ax.axhline(50,color=GRAY,ls='--',lw=.7);ax.set_ylabel('Balanced accuracy (%)')
    ax.text(.5,.12,'One frozen support draw\n100 support cells per sex',transform=ax.transAxes,ha='center',fontsize=7)
    panel_label(ax,'a','Original Sayed oligodendrocytes')
    write_source(fid,'a',x)
    panels.append(rec('a','Original frozen sex case is a single GSM-separated example','fig6__operator_prereg_cases',
                     {'panel':'zebra_sex','model_id':'cellpfn_g1v2p','checkpoint_update':'96000','support_per_class':'100','draw':'0'},
                     '50 query cells, 10 query GSM samples, one support draw',
                     'No interval available; points are observed values',
                     note='GSM sample separation does not establish distinct biological donors.'))
    selected=[]
    for j,(task,title,color) in enumerate([('zsex_xy','XY-eligible positive control',TEAL),('zsex','Broader sex task',BLUE)]):
        ax=fig.add_subplot(gs[0,j+1]);x=select(d,efast_task=task,metric='unit_level_auc')
        assert len(x)==40
        means=raw_splits(ax,x,[{'support_units_per_class_k':str(k)} for k in [4,8,16,32]],'Unit-level AUC',chance=.5,ylim=(0,1.06),color=color)
        ax.set_xticks(range(4),['4','8','16','32']);ax.set_xlabel('Support units per sex')
        ax.text(.03,.05,f"{int(float(x.iloc[0].n_units))} query units per split",transform=ax.transAxes,fontsize=6)
        panel_label(ax,chr(98+j),title);write_source(fid,chr(98+j),x);selected.append(x)
        panels.append(rec(chr(98+j),title,'supp_taskmix_tradeoff__efast_cases',
                         {'model_id':'cellpfn_g1v2p','checkpoint_update':'96000','efast_task':task,'metric':'unit_level_auc'},
                         '10 repeated support/query splits at each support budget',
                         'All split values plus mean/min–max; no confidence interval',
                         numeric_anchors={str(k):m for k,m in zip([4,8,16,32],means)},
                         note='Persons where resolved; some Sayed units are age-by-sex GSM groups. Study sets and gene universes differ across sex tasks.'))
    age_groups=[('zagedev','3'),('zage_sayed','4'),('zage_sayed','8'),('zage_gerrits','4')]
    agenames=['Herring\nk = 3','Sayed\nk = 4','Sayed\nk = 8','Gerrits\nk = 4']
    for j,(metric,ylabel,title) in enumerate([('unit_level_auc','Unit-level AUC','Existing age tasks'),
                                             ('balanced_accuracy','Cell-level balanced accuracy (%)','Cell-level age classification'),
                                             ('nll','Cell-level NLL (nats)','Age prediction log loss')]):
        ax=fig.add_subplot(gs[1,j]);x=select(d,efast_task=[a for a,b in age_groups],metric=metric)
        assert len(x)==40
        raw_splits(ax,x,[{'efast_task':a,'support_units_per_class_k':b} for a,b in age_groups],
                   ylabel,chance=.5 if metric=='unit_level_auc' else None,
                   ylim=(0,1.06) if metric=='unit_level_auc' else None,color=PURPLE)
        if metric=='balanced_accuracy':
            for i,c in enumerate([25,50,50,50]):ax.hlines(c,i-.35,i+.35,color=GRAY,ls='--',lw=.7)
            ax.set_ylim(20,75)
        ax.set_xticks(range(4),agenames)
        panel_label(ax,chr(100+j),title);write_source(fid,chr(100+j),x)
        panels.append(rec(chr(100+j),title,'supp_taskmix_tradeoff__efast_cases',
                         {'model_id':'cellpfn_g1v2p','checkpoint_update':'96000','efast_task':[a for a,b in age_groups],'metric':metric},
                         '10 repeated support/query splits per task/budget',
                         'All split values plus mean/min–max; no confidence interval',
                         note='Herring age has four classes and macro one-vs-rest AUC; Sayed/Gerrits use within-study median age binary targets. NLL is not comparable across class counts without context.'))
    finish(fig,fid,title='Sex and age evaluation boundaries',
           claim='A strong sex positive control contrasts with near-chance broader sex performance and heterogeneous age results.',
           panels=panels,sources=['fig6__operator_prereg_cases','supp_taskmix_tradeoff__efast_cases',
               ROOT.parent/'hashprompt/efast/tiers.py',ROOT.parent/'hashprompt/efast/metrics.py'],
           extra={'checkpoint_update':96000,'gene_view':'Up to 8192 HVGs for unit-level tasks; all 21158 processed genes in original sex case',
                  'exclusions':'No sex-specific attribution arrays are available. No provisional ROSMAP result is plotted.'})
    legend_file(6,'Sex and age performance depends on the task population and target.',
        r'''\textbf{a}, One frozen Sayed oligodendrocyte sex case: 100 support cells per sex from twelve GSM samples and 50 query cells from ten other GSMs. GSM separation does not establish donor separation; no population interval is inferred. \textbf{b,c}, Unit-level sex AUC for studies measuring \textit{XIST} and at least four Y-linked genes (positive control; 28 query units) versus the broader task (32 query units). Populations and gene universes differ; eligibility does not identify predictive genes. \textbf{d--f}, Age AUC, cell-level accuracy and NLL. Herring excitatory neurons use four age classes ($<1$, 1--$<6$, 6--$<16$, $\geq16$ years), three supports/class and twelve query persons. Sayed/Gerrits oligodendrocyte targets split eligible units at the study median, with twelve/eight query units. Herring AUC is macro one-versus-rest; other AUCs are binary. Circles show ten repeated splits; diamonds/bars show means/ranges. Reused units are not independent cohorts. Dashed lines mark chance; NLL depends on class count. All panels use checkpoint 96,000; b--f request up to 8,192 HVGs. Units are resolved persons or Sayed age-by-sex GSM groups; cross-study identity overlap is unresolved. No sex-gene attribution is asserted.''')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--figure',choices=['1','4','5','6','all'],default='all')
    args=parser.parse_args()
    for number,fn in [('1',build_s1),('4',build_s4),('5',build_s5),('6',build_s6)]:
        if args.figure in [number,'all']:fn()
