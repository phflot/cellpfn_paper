#!/usr/bin/env python3
"""Deterministically render manuscript tables from the immutable harmonized export.

Only descriptive means/ranges and existing paired intervals are used. --check
compares regenerated content in memory without modifying any file.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import math
from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT.parent / 'paper_export_20261011' / 'data'
PANELS = ['pbmc_l1', 'pbmc_l2', 'zebra_dev', 'zebra_ood']
PANEL_NAMES = {'pbmc_l1':'PBMC coarse', 'pbmc_l2':'PBMC fine', 'zebra_dev':'ZEBRA development', 'zebra_ood':'ZEBRA held-study'}
BUDGETS = ['1', '10', '100']
DRAW3 = ['0','1','2']
VALUES = []
OUT = {}
CURRENT = ''

@lru_cache(None)
def rows(name):
    with (DATA / (name + '.csv')).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def select(name, filters):
    return [r for r in rows(name) if all(r[k] in ([str(x) for x in v] if isinstance(v,list) else [str(v)]) for k,v in filters.items())]

def value(name, filters, column='value', op='single', n=None, scale=1):
    selected = select(name, filters)
    if n is not None:
        assert len(selected)==n, (name, filters, len(selected), n)
    assert selected, (name,filters)
    x = [float(r[column]) for r in selected]
    assert all(math.isfinite(v) for v in x), (name,filters,column)
    if op=='single':
        assert len(x)==1, (name,filters,column,len(x))
        result=x[0]
    elif op=='mean': result=math.fsum(x)/len(x)
    elif op=='min': result=min(x)
    elif op=='max': result=max(x)
    elif op=='sum': result=math.fsum(x)
    else: raise ValueError(op)
    result *= scale
    VALUES.append(dict(id=f'TB{len(VALUES)+1:04d}',table=CURRENT,source=f'../paper_export_20261011/data/{name}.csv',filter_json=json.dumps(filters,sort_keys=True),value_column=column,aggregation=op,scale=scale,expected_rows=len(x),value=format(result,'.15g')))
    return result

def fmt(x, dp=1, signed=False):
    # Remove floating arithmetic noise far below displayed precision, then use
    # conventional decimal half-up rounding (e.g. 62.25 -> 62.3).
    decimal=Decimal(format(x,'.12f')).quantize(Decimal(1).scaleb(-dp),rounding=ROUND_HALF_UP)
    if decimal==0: decimal=abs(decimal)
    return f'{decimal:+.{dp}f}' if signed else f'{decimal:.{dp}f}'

def number(name, filters, column='value', op='single', n=None, dp=1, scale=1, signed=False):
    return fmt(value(name,filters,column,op,n,scale),dp,signed)

def interval(name, filters, mid='mean_diff', lo='ci95_lo', hi='ci95_hi', dp=2):
    return number(name,filters,mid,dp=dp,signed=True)+r' ['+number(name,filters,lo,dp=dp)+', '+number(name,filters,hi,dp=dp)+']'

def esc(s):
    for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#')]: s=s.replace(a,b)
    return s.replace('−','-').replace('≥',r'$\geq$')

def line(cells): return ' & '.join(cells)+r' \\'+'\n'

def longtable(title,label,headers,body,widths,notes=''):
    spec='@{}'+''.join(r'>{\raggedright\arraybackslash}p{'+w+'}' for w in widths)+'@{}'
    h=line(headers)
    return ('\\begin{longtable}{'+spec+'}\n'+r'\caption{'+title+r'}\label{'+label+r'}\\'+'\n'+r'\toprule'+'\n'+h+r'\midrule\endfirsthead'+'\n'+r'\multicolumn{'+str(len(headers))+r'}{l}{\small Table \thetable{} (continued)}\\\toprule'+'\n'+h+r'\midrule\endhead'+'\n'+r'\bottomrule\endfoot'+'\n'+body+r'\end{longtable}'+'\n'+notes+'\n')

MODELS=[('cellpfn_g1v2p','CellPFN','all','All genes'),('tabicl_v2','TabICLv2','hvg2000','2k HVGs'),('c2b40k','TabICLv2 + cellular prior','hvg2000','2k HVGs'),('kumo_small','Kumo small','hvg2000','2k HVGs'),('k2b_s40k','Kumo small + cellular prior','hvg2000','2k HVGs'),('kumo_large','Kumo large','hvg2000','2k HVGs'),('k2b_l40k','Kumo large + cellular prior','hvg2000','2k HVGs'),('tabpfn35','TabPFN-3.5','hvg2000','2k HVGs'),('geneformer_lr','Geneformer-V2 + LR','own_input','Native embedding'),('scgpt_lr','scGPT + LR','own_input','Native embedding'),('woodbury32_lda','Low-rank LDA','all','All genes')]
CONTEXT=[('celltypist','CellTypist','all','All genes'),('singler','SingleR','all','All genes'),('scanvi_inductive','scANVI inductive','hvg2000','2k HVGs'),('scanvi_transductive','scANVI transductive','hvg2000','2k HVGs'),('logreg','Logistic regression','hvg2000','2k HVGs')]

def benchmark_filter(model, view, panel=PANELS, support=BUDGETS):
    return dict(model_id=model,gene_view=view,panel=panel,support_per_class=support,draw=DRAW3,metric='balanced_accuracy',status='ok')

def benchmark_source(model): return 'fig2__cases' if model!='woodbury32_lda' and model not in [m[0] for m in CONTEXT] else 'fig4__cases'

def exposure_mark(model, panel):
    """Preserve the original export's exposure audit, including partial overlap."""
    family={'geneformer_lr':'geneformer','scgpt_lr':'scgpt'}.get(model)
    if family is None: return ''
    if isinstance(panel,list):
        # A summary includes exposed evaluations; never interpret it as all cells.
        marks=[exposure_mark(model,p) for p in panel]
        return r'\textsuperscript{*}' if any(marks) else ''
    matches=select('fig2__exposure_marks',dict(family=family,panel=panel))
    assert len(matches)==1,(family,panel,len(matches))
    mark=matches[0]['mark']
    return r'\textsuperscript{'+mark+'}' if mark else ''


def ranked_number(x, best, suffix='', dp=1, *, best_unflagged=None, trailing=''):
    """Bold displayed-precision ties and gray cells with exposure markers."""
    cell=fmt(x,dp)
    wins_overall=cell==fmt(best,dp)
    wins_unflagged=(not suffix and best_unflagged is not None
                    and cell==fmt(best_unflagged,dp))
    if wins_overall or wins_unflagged: cell=r'\textbf{'+cell+'}'
    cell+=suffix+trailing
    return r'\textcolor{black!55}{'+cell+'}' if suffix else cell


def overview():
    global CURRENT
    CURRENT='Table 1';body=''
    for panel in PANELS:
        for budget in BUDGETS:
            values=[]
            for model,label,view,viewlabel in MODELS:
                if model=='woodbury32_lda' and budget=='1': values.append(None)
                else: values.append(value(benchmark_source(model),benchmark_filter(model,view,panel,budget),op='mean',n=3))
            best=max(v for v in values if v is not None)
            best_unflagged=max(v for (model,_,_,_),v in zip(MODELS,values)
                               if v is not None and not exposure_mark(model,panel))
            cells=[PANEL_NAMES[panel]+', '+budget]
            for (model,_,_,_),v in zip(MODELS,values):
                cells.append('--' if v is None else ranked_number(v,best,exposure_mark(model,panel),best_unflagged=best_unflagged))
            body+=line(cells)
        body+=r'\addlinespace[2pt]'+'\n'
    values=[None if m=='woodbury32_lda' else value(benchmark_source(m),benchmark_filter(m,v),op='mean',n=36) for m,_,v,_ in MODELS]
    best=max(v for v in values if v is not None)
    best_unflagged=max(v for (model,_,_,_),v in zip(MODELS,values)
                       if v is not None and not exposure_mark(model,PANELS))
    body+=r'\midrule'+'\n'+line(['Overall']+['--' if v is None else ranked_number(v,best,exposure_mark(m,PANELS),best_unflagged=best_unflagged) for (m,_,_,_),v in zip(MODELS,values)])
    CURRENT='Table 2'; gene_body=''
    for panel in PANELS:
        cells=[PANEL_NAMES[panel]]
        for budget in BUDGETS:
            vals=[value('fig2__cases',benchmark_filter('cellpfn_g1v2p',view,panel,budget),op='mean',n=3) for view in ['hvg2000','hvg8192','all']]
            best=max(vals)
            cells += [ranked_number(v,best) for v in vals]
        gene_body+=line(cells)
    OUT['tables/overview.tex']=r'''% Generated by scripts/build_tables.py; do not edit numerical cells.
\begin{landscape}
\begin{table}[p]
\centering\setstretch{1.0}\fontsize{10}{11.5}\selectfont\setlength{\tabcolsep}{2pt}
\caption{Biological classification and cellular-prior transfer.}
\label{table:overview}
\textbf{Model comparison: balanced accuracy (\%)}\par\smallskip
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{4.1cm}*{8}{>{\centering\arraybackslash}p{1.45cm}}>{\centering\arraybackslash}p{1.85cm}*{2}{>{\centering\arraybackslash}p{1.45cm}}@{}}
\toprule
Panel, support/class & CellPFN & \multicolumn{2}{c}{TabICLv2} & \multicolumn{2}{c}{Kumo small} & \multicolumn{2}{c}{Kumo large} & TabPFN\newline 3.5 & Geneformer\newline V2 (316M) & scGPT & Low-rank LDA \\
 & All genes & Released & + prior & Released & + prior & Released & + prior & Released & + LR & + LR & All genes \\
\midrule
'''+body+r'''\bottomrule
\end{tabular}
\par\medskip\raggedright
Means over three support draws. Bold identifies the highest row mean overall and among unflagged entries, including ties at displayed precision; gray marks starred exposure flags. Rankings are descriptive, not significance claims. Overall equally weights twelve panel--budget combinations; dashes denote unevaluated settings, and LDA has no overall mean. PBMC coarse and fine panels have eight and twenty classes; both ZEBRA panels classify four broad groups (Glia, Immune cell, Neural and Vascular cell), with distinct development and held-study query panels. Model variants were selected using development evaluations. Tabular models use 2k HVGs, a requested cap of up to 2,000 support-selected genes; actual widths can be lower (Methods). CellPFN and LDA use all genes. CellPFN uses PBMC counts and processed ZEBRA values; tabular models and LDA use processed values. Geneformer/scGPT use native embeddings with logistic regression (LR); scGPT uses the declared unstandardized route, with post hoc classifier sensitivity in Table~\ref{tab:s9}. ``+ prior'' denotes released weights adapted with 40,000 cellular tasks plus generic replay. Panel-specific draw ranges appear in Table~\ref{tab:s1}. HVG, highly variable gene.\par
\textsuperscript{*} flags likely query-source pretraining overlap: PBMC query cells are assessed as likely present for Geneformer-V2 (316M)\citep{chen2026geneformer} and scGPT. Geneformer-V2 corpus records overlap source studies supplying 92.6\% of ZEBRA held-study query cells; this is an upper bound on exact-cell overlap, not verified cell matching. \textsuperscript{(*)} denotes inferred possible overlap of control query cells in ZEBRA development (at most 22.3\%). Support-source overlap is audited separately and is not encoded by these query-source stars. These marks concern cell-expression exposure, not evidence that target labels were seen. Overall starred means include flagged evaluations. Unmarked scores do not certify absence of exposure within or outside the audited Geneformer/scGPT corpora.
\end{table}
\clearpage
\begin{table}[p]
\centering\setstretch{1.0}\fontsize{10}{11.5}\selectfont\setlength{\tabcolsep}{3pt}
\caption{CellPFN gene-panel ablation.}
\label{table:gene_ablation}
\textbf{Balanced accuracy (\%)}\par\smallskip
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{4.1cm}*{9}{>{\centering\arraybackslash}p{1.8cm}}@{}}
\toprule
Panel & \multicolumn{3}{c}{1 support/class} & \multicolumn{3}{c}{10 supports/class} & \multicolumn{3}{c}{100 supports/class} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}
 & 2k HVGs & 8,192 HVGs & All genes & 2k HVGs & 8,192 HVGs & All genes & 2k HVGs & 8,192 HVGs & All genes \\
\midrule
'''+gene_body+r'''\bottomrule
\end{tabular}
\par\medskip\raggedright
Means over three support draws for the same CellPFN checkpoint and query panels used in Table~\ref{table:overview}. Bold identifies the highest mean within each panel and support-budget group, including ties at displayed precision. Rankings are descriptive, not significance claims. The labels 2k HVGs and 8,192 HVGs denote requested caps of up to 2,000 and 8,192 support-selected genes; actual widths can be lower (Methods). CellPFN uses PBMC counts and processed ZEBRA values; ZEBRA development and held-study query panels are distinct. HVG, highly variable gene. Table~\ref{tab:s3} reports the separate twenty-draw analysis, paired intervals and random-gene controls.
\end{table}
\end{landscape}
'''

def s1():
    global CURRENT
    CURRENT='Table S1'; body=''
    for panel in PANELS:
        best_by_budget={}; best_unflagged_by_budget={}
        for budget in BUDGETS:
            candidates=[]; unflagged=[]
            for model,_,view,_ in MODELS+CONTEXT:
                selected=select(benchmark_source(model),benchmark_filter(model,view,panel,budget))
                if selected:
                    assert len(selected)==3
                    mean=math.fsum(float(r['value']) for r in selected)/3
                    candidates.append(mean)
                    if not exposure_mark(model,panel): unflagged.append(mean)
            best_by_budget[budget]=max(candidates)
            best_unflagged_by_budget[budget]=max(unflagged)
        body+=r'\multicolumn{4}{@{}l}{\textbf{'+PANEL_NAMES[panel]+r'}}\\'+'\n'
        for model,label,view,_ in MODELS+CONTEXT:
            cells=[label]
            for budget in BUDGETS:
                f=benchmark_filter(model,view,panel,budget); name=benchmark_source(model)
                selected=select(name,f)
                if not selected: cells.append('--'); continue
                assert len(selected)==3,(name,f,len(selected))
                mean=value(name,f,op='mean',n=3)
                draw_range=' ['+number(name,f,op='min',n=3)+', '+number(name,f,op='max',n=3)+']'
                cells.append(ranked_number(mean,best_by_budget[budget],exposure_mark(model,panel),best_unflagged=best_unflagged_by_budget[budget],trailing=draw_range))
            body+=line(cells)
        body+=r'\addlinespace'+'\n'
    note=r'''Values are mean [minimum, maximum] balanced accuracy (\%) over the same three support draws, not confidence intervals. Within each panel and support budget, bold identifies the highest mean overall and among unflagged comparators, including ties at displayed precision. Gray means and ranges carry the exposure stars defined in Table~\ref{table:overview}; unflagged entries do not certify absence of exposure. Inputs follow Table~\ref{table:overview}; CellTypist, SingleR and low-rank LDA use all genes, whereas logistic regression and scANVI use 2k HVGs, a requested cap of up to 2,000 support-selected genes that can yield fewer genes (Methods). CellTypist\citep{dominguezconde2022celltypist} is fitted to the support cells. SingleR\citep{aran2019singler} uses support cells as its reference and the default classic marker method; the exported source notes that the single-cell-reference vignette recommends a different marker setting, so these scores describe the declared default route. The scANVI\citep{xu2021scanvi} recipe uses 400 scVI epochs followed by ten scANVI epochs, batch size 128, training fraction 0.9 and no per-label resampling (\texttt{n\_samples\_per\_label=None}). In fine-PBMC one-shot inductive training, only eighteen of twenty labelled support cells enter training, leaving at least two classes without a labelled training example. Low-support values therefore describe this constrained recipe. The transductive route additionally uses the unlabelled query pool and is contextual rather than an inductive comparison. Dashes are missing evaluations, never zero accuracy. All selected fitted model checkpoints have one training seed; support-draw variation does not measure training uncertainty. Geneformer-V2 uses the 316M checkpoint. Source-study corpus overlap does not establish exact-cell or target-label exposure. Native gene vocabularies and training histories differ. Family variants were selected using development evaluations; this is not a newly frozen independent benchmark.'''
    OUT['tables/s1.tex']=longtable('Panel-specific benchmark performance and contextual baselines.','tab:s1',['Model','1 support/class','10 supports/class','100 supports/class'],body,['4.5cm','3.45cm','3.45cm','3.45cm'],note)

def s2():
    global CURRENT
    CURRENT='Table S2';body=''
    f=dict(model_id='cellpfn_g1v2p')
    for label,col in [('Parameters','parameter_count'),('Optimizer updates','update'),('Simulated banks','datasets_completed'),('Scheduled episodes','tasks_scheduled'),('Loss-bearing episodes','tasks_gradient_bearing')]:
        body+=line(['CellPFN',label,number('fig1__lineage',f,col,dp=0)])
    for arm,label in [('c2b','TabICLv2'),('k2b_s','Kumo small'),('k2b_l','Kumo large')]:
        for title,col in [('Parameters','n_parameters'),('Additional cellular tasks','simulated_tasks'),('Adaptation updates','updates')]: body+=line([label,title,number('fig3__arms',dict(finetune_arm=arm),col,dp=0)])
    out=longtable('Training exposure, prior transfer and generic-task retention.','tab:s2',['Model','Quantity','Count'],body,['4.4cm','6.5cm','3.95cm'],r'''CellPFN banks are reused for multiple episodes; scheduled and loss-bearing episodes are distinct. Adaptation uses 40,000 cellular tasks and 10,000 generic replay tasks per arm. Released-model pretraining precedes this adaptation and is not included in these counts. TabICLv2 reports 35 million synthetic pretraining datasets\citep{qu2026tabiclv2}; this published count is distinct from CellPFN banks and scheduled episodes. These units do not establish a matched-compute comparison.''')
    body=''
    for model,label in [('c2b40k','TabICLv2'),('k2b_s40k','Kumo small'),('k2b_l40k','Kumo large')]:
        vals=[]
        for budget in BUDGETS:
            f=dict(model_id=model,gene_view='hvg2000',panel=PANELS,support_per_class=budget,draw=DRAW3,metric='balanced_accuracy')
            vals.append(number('fig3__paired',f,'delta','mean',12,dp=2,signed=True))
        body+=line([label]+vals)
    out+=r'\medskip\noindent\textbf{Adapted minus released balanced accuracy (percentage points).}\par'+'\n'+plain(['Model','1 support','10 supports','100 supports'],body,['4.4cm','3.5cm','3.5cm','3.45cm'])
    out+=r'''Each delta uses released weights re-scored in the same matched scoring run as the adapted checkpoint. Table~\ref{table:overview} instead reports the stored benchmark scores for released models; subtracting its displayed means need not reproduce these paired deltas.\par
'''
    body=''
    for model,label in [('k2b_s40k','Cellular task stream 1'),('p1_s43_40k','Cellular task stream 2'),('p1_s44_40k','Cellular task stream 3'),('p1_g40k','Generic-table control')]:
        f=dict(model_id=model,gene_view='hvg2000',panel=PANELS,support_per_class=['1','10'],draw=DRAW3,metric='balanced_accuracy')
        body+=line([label,number('fig3__paired',f,'delta','mean',24,dp=2,signed=True)])
    out+=r'\medskip\noindent\textbf{Kumo-small low-support change relative to released weights.}\par'+'\n'+plain(['Training stream','Mean change (percentage points)'],body,['7.5cm','7.35cm'])
    out+=r'''The low-support average weights eight panel--budget combinations equally (three support draws each). The three cellular runs vary the task stream with the same model seed. The generic control changes rows and columns per update, so this is not a matched-data or matched-cost contrast. No corresponding generic-only control was run for TabICLv2 or Kumo large.\par
'''
    body=''
    for model,label in [('tabicl_v2','TabICLv2 released'),('c2b40k','TabICLv2 adapted')]:
        f=dict(model_id=model,status='ok')
        vals=[]
        for budget in ['1',['1','10','']]:
            for metric in ['balanced_accuracy','accuracy']:
                vals.append(number('fig3__generic_tables_cases',dict(f,support_per_class=budget,metric=metric),'value','mean',20 if isinstance(budget,str) else 60))
        body+=line([label]+vals)
    out+=r'\medskip\noindent\textbf{Retention on four generic classification datasets.}\par'+'\n'+plain(['Model','One-shot BA','One-shot accuracy','All-budget BA','All-budget accuracy'],body,['4.1cm','2.65cm','2.65cm','2.65cm','2.8cm'])
    out+=r'''Balanced accuracy (BA) and ordinary accuracy (\%) equally weight breast cancer, digits, iris and wine, with five split seeds each. The all-budget mean additionally weights 1, 10 and the full training split equally. These exploratory retention checks do not estimate universal tabular performance.'''
    OUT['tables/s2.tex']=out

def plain(headers,body,widths):
    spec='@{}'+''.join(r'>{\raggedright\arraybackslash}p{'+w+'}' for w in widths)+'@{}'
    return '\\nopagebreak[4]\\par\\noindent\\begin{tabular}{'+spec+'}\n\\toprule\n'+line(headers)+'\\midrule\n'+body+'\\bottomrule\n\\end{tabular}\\par\n'

def s3():
    global CURRENT
    CURRENT='Table S3';body=''
    for panel in PANELS:
        for budget in BUDGETS:
            f=dict(model_id='cellpfn_g1v2p',panel=panel,support_per_class=budget,gene_view='all',metric='balanced_accuracy',draw_set='draws_0_19')
            body+=line([PANEL_NAMES[panel],budget,interval('fig2__cells',f,'delta_vs_hvg2000_mean','delta_vs_hvg2000_ci95_low','delta_vs_hvg2000_ci95_high')])
    out=longtable('Gene-panel scaling and random-gene controls.','tab:s3',['Panel','Support/class',r'All minus 2k HVGs (pp; 95\% CI)'],body,['4.8cm','3.0cm','7.05cm'],r'''Paired differences in balanced accuracy (percentage points) use twenty support draws per panel--budget combination. Intervals are the exported paired 95\% $t$ intervals over support draws. They condition on the evaluated checkpoint and query set; they do not cover training, donor-population or panel-selection uncertainty.''')
    body=''
    gene_views=[('rand2000','Random 2,000 genes'),('hvg2000','2k HVGs'),('rand8192','Random 8,192 genes'),('hvg8192','8,192 HVGs'),('all','All genes')]
    means=[]
    for view,label in gene_views:
        f=dict(model_id='cellpfn_g1v2p',gene_view=view,panel=PANELS,support_per_class=BUDGETS,metric='balanced_accuracy',draw_set='draws_0_19')
        means.append(value('fig2__cells',f,'mean','mean',12))
    best=max(means)
    for (_,label),mean in zip(gene_views,means):
        body+=line([label,ranked_number(mean,best)])
    out+=r'\medskip\noindent\textbf{Mean balanced accuracy across the twelve panel--budget combinations.}\par'+'\n'+plain(['Gene panel',r'Mean balanced accuracy (\%)'],body,['7.5cm','7.35cm'])
    out+=r'''Bold identifies the highest descriptive gene-panel average, including ties at displayed precision; paired contrast intervals above are not ranked. The 2k-HVG and 8,192-HVG labels are requested caps of up to 2,000 and 8,192 support-selected genes, with lower realized widths possible (Methods). These descriptive twenty-draw averages differ from the three-draw headline benchmark in Table~\ref{table:overview}. Random-panel controls assess the delivered panels and cannot isolate every effect of feature selection or gene coverage.'''
    OUT['tables/s3.tex']=out

def s4():
    global CURRENT
    CURRENT='Table S4';body=''
    for panel in PANELS:
        for budget in BUDGETS:
            f=dict(model_a='cellpfn_g1v2p',model_b='cellpfn_c1v2p',panel=panel,support_per_class=budget,gene_view='all',metric='balanced_accuracy')
            body+=line([PANEL_NAMES[panel],budget,interval('fig6__operator_paired_by_view',f)])
    out=longtable('Operator ablation and the prespecified decision.','tab:s4',['Panel','Support/class',r'Full minus no operator (pp; 95\% CI)'],body,['4.8cm','3.0cm','7.05cm'],r'''Twenty paired support draws, one training seed per arm, all genes. Intervals are exported paired 95\% $t$ intervals over support draws. Full and no-operator checkpoints share the parent, prior and task stream. These later descriptive evaluations do not replace the prespecified decision below.''')
    body=''
    for panel in PANELS:
        for budget in BUDGETS:
            cells=[PANEL_NAMES[panel],budget]
            for m in ['cellpfn_c1v2p','cellpfn_d1v2p','cellpfn_g1v2p']:
                f=dict(model_id=m,panel=panel,support_per_class=budget,gene_view='all',metric='balanced_accuracy',status='ok')
                cells.append(number('fig6__operator_cases',f,op='mean',n=20,dp=2))
            f=dict(model_a='cellpfn_g1v2p',model_b='cellpfn_d1v2p',panel=panel,support_per_class=budget,gene_view='all',metric='balanced_accuracy')
            cells.append(interval('fig6__operator_paired_by_view',f))
            body+=line(cells)
    out+=r'\par\medskip\noindent\textbf{Operator structure across support budgets.}\par'+'\n'+plain(['Panel','Support/ class','None','Diagonal','Full',r'Full minus diagonal (pp; 95\% CI)'],body,['3.3cm','1.4cm','1.65cm','1.65cm','1.65cm','5.2cm'])
    out+=r'''Values are mean balanced accuracy (\%). The diagonal ablation is a trained per-gene-variance-only operator arm; it shares the parent, prior and task stream with the full-operator arm. At one support per class, the inference operator gate is zero: differences between these separately trained arms reflect their learned states, not an active inference-time operator. The printed matrices use all genes. The source-value index retains additional HVG and random-panel analyses.\par
'''
    body=''
    for r in rows('fig6__operator_n3_test_wide'):
        f=dict(source_cell=r['source_cell'])
        body+=line([PANEL_NAMES[r['panel']],r['support_per_class'],number('fig6__operator_n3_test_wide',f,'delta_ba',dp=2,signed=True),number('fig6__operator_n3_test_wide',f,'theta',dp=2)])
    out+=r'\medskip\noindent\textbf{Prespecified three-draw readout.}\par'+'\n'+plain(['Panel','Support/class','Full minus none (pp)','Harm threshold (pp)'],body,['4.3cm','2.7cm','4.0cm','3.85cm'])
    out+=r'''The overall test was not supported because coarse-PBMC ten-support accuracy crossed the prespecified harm threshold (N3). Turning the full operator off at inference isolated a harmful -0.94-point operator contribution in that setting. Its donor-enumeration interval has approximately 80\% coverage, not 95\%, and is not used as a 95\% interval here. Three frozen support draws and four query donors informed the PBMC test; the later twenty-draw estimates describe support sensitivity rather than overturning the decision.'''
    value('fig6__operator_n3_test_wide',{'source_cell':'pbmc|celltype.l1|B10'},'A_operator_off')
    OUT['tables/s4.tex']=out

def s5():
    global CURRENT
    CURRENT='Table S5';body=''
    short={'LR':'Task-mixture restriction','A5':'Fewer/weaker markers and closer sibling classes','A6':'Remove signed-covariance task lane','A7':'Donor dominance','A1':'More donor-rich tasks','A3':'Sex mechanisms','A4':'Weak metadata tasks','A2':'Adult-age prior','A8a':'Study-wide gene absence','A8d':'Study-specific detection'}
    outcome={'LR':'Keep','A5':'Drop: guard','A6':'Neutral','A7':'Unresolved','A1':'Routing only','A3':'Routing only','A4':'Routing only','A2':'Routing only','A8a':'Drop: guard','A8d':'Not testable'}
    for r in rows('supp_prior_ablation__outcomes'):
        f={'arm':r['arm']};dp=2 if r['unit']=='BA_pct' else 4
        vals=[number('supp_prior_ablation__outcomes',f,c,dp=dp,signed=True) for c in ['r42','r43','r44','mean']]
        body+=line([r['arm']+' / '+r['base_stream'],short[r['arm']]]+vals+[outcome[r['arm']]])
    out=longtable('Complete ten-candidate prior screen.','tab:s5',['Arm/base','Change','r42','r43','r44','Mean','Decision'],body,['1.5cm','3.9cm','1.5cm','1.5cm','1.5cm','1.5cm','2.55cm'],r'''All changes are improvement-signed relative to the indicated base. LR, A5, A6, A7, A8a and A8d use balanced-accuracy percentage points; A1, A3 and A2 use donor AUC differences on a 0--1 scale; A4 uses negative log-loss differences (base minus arm, nats). A7 uses the held-study panel; A8a/A8d use low-support cortex; LR/A5/A6 use all low-support core panels. A1/A3/A2 respectively target donor, worse-sex and adult-age AUC. The Kumo-small proxy uses 10,000 cellular tasks, 625 updates and 2k HVGs. The three columns are task-stream replicates from one model seed, not independent model-seed replications. A5 and A4 are compared with LR; A3 with A1; A2 with the matched age-task stream. Other candidates use the pipeline control b0.''')
    out+=r'''\par\medskip
LR was the only retained change: its keep threshold was 1.63 points and effective noise band 1.09 points. A5 failed the low-support guard. A7 remained unresolved; omitting the prescribed two extension replicates departed from the frozen rule, although the required keep count was no longer attainable. A1--A4 routing labels do not establish successful donor-level or probability-prediction improvements: those endpoints were outside the proxy's trusted decision scope. A8a failed the log-loss guard (0.099-nat deterioration against a 0.03-nat limit). A8d was not testable because measured headroom (1.257 points) was below the 1.5-point keep threshold; its two extension replicates were omitted under the documented shortcut because the required keep count was no longer attainable. A8d replicate r43 skipped one invalid task, an authorized deviation made after the other two replicate readouts. None of these routing, unresolved or headroom-limited outcomes is evidence that its biological mechanism does or does not work.
'''
    # Register numerical rule context as well as outcome cells.
    for column in ['keep','band_eff']:
        value('supp_prior_ablation__outcomes',{'arm':'LR'},column)
    value('supp_prior_ablation__replicates',{'arm':'A8a','metric':'B_nll'},'diff_arm_minus_base','mean',3)
    value('supp_prior_ablation__thresholds',{'metric':'B_nll'},'guard_limit',scale=-1)
    body=''
    for arm in ['A8a','A8d']:
        f=dict(arm=arm,replicate='r42')
        body+=line([arm]+[number('supp_prior_ablation__a8_gap_shrink',f,c,dp=3) for c in ['mean_gap_shrink','band_eff_gap','headroom_HR','keep']])
    out+=r'\par\medskip\noindent\textbf{Stored-zero mechanism readout (percentage points).}\par'+'\n'+plain(['Arm','Mean gap shrinkage','Noise band','Proxy headroom','Keep threshold'],body,['1.7cm','3.65cm','3.0cm','3.3cm','3.4cm'])
    out+=r'''Gap shrinkage is the reduction in the accuracy difference between removing unmeasured genes and retaining stored zeros. The gap did not shrink beyond the noise band; the reference row repeats the three-replicate aggregate, not a single-replicate estimate.'''
    OUT['tables/s5.tex']=out

def s6():
    global CURRENT
    CURRENT='Table S6';body=''
    for panel in PANELS:
        for budget in BUDGETS:
            f=dict(model_a='cellpfn_gl1',model_b='cellpfn_gs1',panel=panel,support_per_class=budget,gene_view='all')
            body+=line([PANEL_NAMES[panel],budget,interval('fig6__taskmix_paired',dict(f,metric='balanced_accuracy'),dp=2),interval('fig6__taskmix_paired',dict(f,metric='nll'),dp=3)])
    out=longtable('Restricted task mixture versus standard CellPFN continuation.','tab:s6',['Panel','Support/class',r'Accuracy change (pp; 95\% CI)',r'Log-loss change (nats; 95\% CI)'],body,['3.8cm','2.2cm','4.5cm','4.35cm'],r'''Restricted task mixture (GL1) minus standard (GS1) at 100,000 updates; twenty paired support draws; all genes. Positive accuracy change is favourable, whereas positive log-loss change is unfavourable. Intervals are exported paired 95\% $t$ intervals over support draws. Both arms continue the same checkpoint for 4,000 updates with one model seed. Log loss measures probabilistic prediction and is not exclusively a calibration measure.''')
    law=dict(stream_id='parent_policy_law',dimension='task_family',family='all')
    out+=r'''The standard task-family mixture is '''+number('fig1__training_stream',dict(law,level=['metadata_binary','metadata_categorical']),op='mean',n=2,dp=0,scale=200)+r'\% metadata, '+number('fig1__training_stream',dict(law,level='cell_type'),dp=0,scale=100)+r'\% cell type and '+number('fig1__training_stream',dict(law,level='donor_identity'),dp=0,scale=100)+r'''\% donor identity. The restricted mixture samples cell-type and donor-identity tasks with nominal probabilities 75\% and 25\%, omits metadata tasks and skips signed-covariance tasks. This is a joint change in task families, mechanisms and training exposure, not a test of metadata-task learnability.\par
'''
    body=''
    for m,label in [('cellpfn_gl1','Restricted task mixture'),('cellpfn_gs1','Standard')]:
        f=dict(model_id=m,quantity='cells_per_update',category='mean')
        body+=line([label,number('fig6__taskmix_stream_composition',f,dp=1)])
    out+=r'\medskip\noindent\textbf{Realized training exposure during continuation.}\par'+'\n'+plain(['Task stream','Mean cells per update'],body,['7.5cm','7.35cm'])
    body=''
    for m,label in [('cellpfn_gs1','Standard'),('cellpfn_gl1','Restricted task mixture')]:
        f=dict(model_id=m,quantity='families')
        metadata='Excluded' if m=='cellpfn_gl1' else number('fig6__taskmix_stream_composition',dict(f,category=['metadata_binary','metadata_categorical']),op='mean',n=2,dp=0,scale=2)
        body+=line([label,metadata]+[number('fig6__taskmix_stream_composition',dict(f,category=c),dp=0) for c in ['cell_type','donor_identity']])
    out+=plain(['Task stream','Metadata tasks','Cell-type tasks','Donor-identity tasks'],body,['4.65cm','3.1cm','3.3cm','3.8cm'])
    out+=r'''The restricted task-mixture continuation processed approximately 1.67 times as many cells per update. Its gains therefore cannot be attributed to task filtering alone under matched cell exposure. Higher-support log loss worsened on three of four panels but improved on fine PBMC.'''
    OUT['tables/s6.tex']=out

def s7():
    global CURRENT
    CURRENT='Table S7';body=''
    specs=[('Strongest marker (log2 FC)','A class: strongest marker per pair'),('Class separation (chance-adjusted BA)','A class: separability BA B10, K-matched (real K8, 64 cells; primary)'),('Within-study donor SD (log2)','B donor: SD within study, 4x2 design (primary)')]
    for label,effect in specs:
        for prior in ['v1_late','v2.2-B']:
            f=dict(effect=effect,prior_id=prior)
            body+=line([label, 'Baseline prior' if prior=='v1_late' else 'Cellular prior',number('fig7__sim_vs_real_summary',f,'syn_q50',dp=3)+' ['+number('fig7__sim_vs_real_summary',f,'syn_q05',dp=3)+', '+number('fig7__sim_vs_real_summary',f,'syn_q95',dp=3)+']',number('fig7__sim_vs_real_summary',f,'real_q50',dp=3)+' ['+number('fig7__sim_vs_real_summary',f,'real_min',dp=3)+', '+number('fig7__sim_vs_real_summary',f,'real_max',dp=3)+']'])
    out=longtable('Simulator realism diagnostics against public biological references.','tab:s7',['Statistic','Prior','Synthetic median [5th, 95th percentile]','Real median [minimum, maximum]'],body,['4.1cm','1.7cm','4.65cm','4.4cm'],r'''Synthetic quantile ranges and observed real ranges are descriptive distributions, not confidence intervals. The reference contains public PBMC, cortex and kidney datasets; ROSMAP is excluded. Class separation uses nearest-class-mean balanced accuracy at ten supports per class with eight classes in both synthetic and primary real references.''')
    body=''
    for label,effect in specs:
        for prior in ['v1_late','v2.2-B']:
            f=dict(effect=effect,prior_id=prior)
            body+=line([label,'Baseline prior' if prior=='v1_late' else 'Cellular prior']+[number('fig7__sim_vs_real_summary',f,c,dp=0) for c in ['syn_n_banks','syn_n_units','real_n_units']]+[number('fig7__sim_vs_real_summary',f,'syn_share_above_real_max',dp=1,scale=100)])
    out+=r'\par\medskip\noindent\textbf{Sampling units and synthetic tail frequencies by prior.}\par'+'\n'+plain(['Statistic','Prior','Synthetic banks','Synthetic units','Real units',r'Synthetic above real max (\%)'],body,['3.8cm','1.6cm','2.2cm','2.2cm','1.7cm','3.35cm'])
    out+=r'''Units differ by statistic: class-pair comparisons for marker effects, dataset-level summaries for separation and donor-effect units for within-study SD. Units from one simulated bank are not independent biological replicates. The real reference helped calibrate the prior, so this is a reference-comparison diagnostic rather than independent validation. The cellular prior supplied only the final 16.7\% of scheduled CellPFN training episodes. Improved moment agreement is not itself evidence of a causal performance benefit.'''
    OUT['tables/s7.tex']=out

def s8():
    global CURRENT
    CURRENT='Table S8';body=''
    cases=[('pbmc_l1_b10_s0','PBMC, 10 supports, draw 0'),('pbmc_l1_b10_s1','PBMC, 10 supports, draw 1'),('pbmc_l1_b100_s0','PBMC, 100 supports'),('zebra_dev_b10_s0','Cortex development, 10 supports'),('kidney_core9_A_F0_count','Kidney, counts'),('kidney_core9_A_F0_processed','Kidney, processed')]
    for case,label in cases:
        vals=[]
        for model in ['cellpfn_g1v2p','cellpfn_c1v2p']:
            f=dict(case_id=case,model_id=model,gene_subset='evaluated_set',knockout_scope='query_only',level='cell',method_id='dsloo_corr_margin',metric='spearman_rho',source_column='rho_cell_corr',source_table='tables/dsloo_vs_exact.csv')
            vals.append(number('fig5__fidelity_by_case',f,dp=3))
        f=dict(case_id=case,model_id='cellpfn_g1v2p',gene_subset='evaluated_set',knockout_scope='query_only',level='cell',method_id='ig64_margin',metric='spearman_rho',source_column='rho_cell_q',source_table='tables/faithfulness_summary.csv',status='ok')
        vals.append(number('fig5__fidelity_by_case',f,dp=3))
        f=dict(case_id=case,model_id='cellpfn_g1v2p',gene_subset='evaluated_set',knockout_scope='query_only',level='pooled_cells_x_genes',method_id='dsloo_corr_margin',metric='rel_l2_error',source_column='rel_err_corr',source_table='tables/dsloo_vs_exact.csv')
        vals.append(number('fig5__fidelity_by_case',f,dp=2,scale=100))
        body+=line([label]+vals)
    out=longtable('DS-LOO fidelity and support sensitivity.','tab:s8',['Case','DS-LOO full: Spearman','DS-LOO none: Spearman','IG64 full: Spearman',r'DS-LOO full: relative error (\%)'],body,['4.65cm','2.4cm','2.4cm','2.4cm','3.0cm'],r'''Corrected-margin DS-LOO and 64-step integrated gradients (IG64) are compared with the same exact query-only single-gene deletion margin target and evaluated gene set in each case, in fp32, using correctly classified cells. IG64 is available for the full-operator model in all six cases. Spearman values summarize within-cell rank correlations, aggregated within classes and then across classes. Relative $L_2$ errors are computed per class and summarized by the median across classes. These are six case summaries per model, not minima across every cell. No one-shot or held-study cortex attribution validation is included. A positive deletion-margin attribution means that the observed gene favours the predicted class over its fixed runner-up; a negative value opposes that margin and does not mean biological downregulation. Setting an already zero query value to zero cannot measure information carried by its absence.''')
    body=''
    for comparison,label in [('support_draw','Different PBMC support choices'),('model_g_vs_c','Full versus no operator')]:
        f=dict(comparison=comparison,method_id='dsloo_corr_margin',class_label='ALL')
        body+=line([label,number('fig5__stability',f,'top20_overlap','min',dp=3)+'--'+number('fig5__stability',f,'top20_overlap','max',dp=3)])
    out+=plain(['Comparison','Range of class-mean top-20 overlap'],body,['8.5cm','6.35cm'])
    out+=r'''Overlap is the fraction of common genes among the twenty highest-ranked genes, averaged over classes for each comparison. The support comparisons include both a changed support draw at ten cells per class and a changed support budget; they are not a pure seed-only sensitivity analysis. Agreement with model knockout measures explanation fidelity, not causal biological validation.'''
    body=''
    top_body=''
    for case,label in [('pbmc_l1_b100_s0','PBMC'),('zebra_dev_b10_s0','ZEBRA')]:
        case_filters=dict(case_id=case,model_id='cellpfn_g1v2p',method_id='dsloo_corr_margin',target='margin')
        classes=sorted({r['class_label'] for r in select('fig5__top_genes',case_filters)})
        for cell_type in classes:
            genes=[]
            for rank in ['1','2','3']:
                f=dict(case_filters,class_label=cell_type,rank=rank)
                found=select('fig5__top_genes',f)
                assert len(found)==1,(f,len(found))
                value('fig5__top_genes',f,'rank')
                genes.append(esc(found[0]['gene']))
            top_body+=line([label,cell_type]+genes)
    out+=r'\par\medskip\noindent\textbf{Three highest-ranked genes for each explained cell class.}\par'+'\n'+plain(['Panel','Cell class','Rank 1','Rank 2','Rank 3'],top_body,['2.2cm','3.65cm','3.0cm','3.0cm','3.0cm'])
    out+=r'''Genes are selected directly by their class-mean corrected DS-LOO margin rank, independently of the curated marker checks below. PBMC uses 100 supports per class, draw 0; ZEBRA development uses ten supports per class, draw 0. These are model-ranked features conditional on the support set and class-discrimination target; they are not all canonical lineage markers and do not establish causal effects.\par'''
    markers=[('B','CD79A'),('B','MS4A1'),('CD4 T','IL7R'),('CD8 T','CD8A'),('DC','FCER1A'),('DC','CLEC10A'),('Mono','CD14'),('NK','GNLY'),('NK','NKG7'),('other','PPBP'),('other T','CD3E'),('DC','LILRA4'),('Mono','LYZ')]
    for cell_type,gene in markers:
        f=dict(case_id='pbmc_l1_b100_s0',model_id='cellpfn_g1v2p',method_id='dsloo_corr_margin',target='margin',class_label=cell_type,marker=gene)
        body+=line([cell_type,gene,number('fig5__marker_ranks',f,'rank',dp=0)])
    out+=r'\par\medskip\noindent\textbf{Known-marker ranks in the PBMC reference case.}\par'+'\n'+plain(['Cell class','Marker','Corrected DS-LOO rank'],body,['5.0cm','4.5cm','5.35cm'])
    out+=r'''The reference uses 100 supports per class and support draw 0, explaining 191 correctly classified query cells across eight broad classes and 33,538 genes. Ranks refer to class-mean corrected margin attribution; smaller is higher. Familiar lineage markers\citep{schafflick2020leukocytes} rank highly in several classes, but LYZ in monocytes and LILRA4 in pooled dendritic cells illustrate that marker identity does not guarantee a high rank for this class-discrimination target. These are selected descriptive marker checks, not an enrichment test or causal validation. Gene identities were assigned after inference.\par'''
    f=dict(case_id='pbmc_l1_b100_s0',model_id='cellpfn_g1v2p',class_label='Mono',marker='LYZ')
    out+=r''' For example, monocyte LYZ ranks '''+number('fig5__marker_ranks',dict(f,method_id='dsloo_corr_margin',target='margin'),'rank',dp=0)+r' for corrected-margin DS-LOO but '+number('fig5__marker_ranks',dict(f,method_id='dsloo_logit',target='logit'),'rank',dp=0)+r''' for predicted-class-logit DS-LOO. The estimand and attribution variant therefore matter when interpreting marker ranks.\par'''
    body=''
    for cell_type,gene in [('Glia','PLP1'),('Neural','SYT1'),('Vascular cell','FLT1'),('Vascular cell','CLDN5'),('Immune cell','PTPRC')]:
        f=dict(case_id='zebra_dev_b10_s0',model_id='cellpfn_g1v2p',method_id='dsloo_corr_margin',target='margin',class_label=cell_type,marker=gene)
        body+=line([cell_type,gene,number('fig5__marker_ranks',f,'rank',dp=0)])
    out+=r'\par\medskip\noindent\textbf{Contextual marker ranks in ZEBRA cell-type classification.}\par'+'\n'+plain(['Cell class','Marker','Corrected DS-LOO rank'],body,['5.0cm','4.5cm','5.35cm'])
    out+=r'''ZEBRA development, ten supports per class, draw 0. PLP1, SYT1 and CLDN5 provide contextual cell-identity checks\citep{gong2025stereoseq}. The immune-class ranking uses '''+number('fig5__classes',dict(case_id='zebra_dev_b10_s0',model_id='cellpfn_g1v2p',class_label='Immune cell'),'n_cells_explained',dp=0)+r''' correctly classified cells; the source report gives low immune-class recall (approximately 0.17), which was not reanalysed here. The ranking therefore characterizes this selected subset. These are cell-type attribution ranks; they are not explanations of the sex-classification experiments in Table~\ref{tab:s9}.'''
    OUT['tables/s8.tex']=out

def s9():
    global CURRENT
    CURRENT='Table S9';body=''
    for panel in ['zebra_dev','zebra_ood']:
        for budget in BUDGETS:
            vals=[]
            for p in [panel,panel.replace('zebra_','zebra_counts_')]:
                f=dict(model_id='cellpfn_g1v2p',panel=p,support_per_class=budget,draw=DRAW3,gene_view='all',metric='balanced_accuracy',status='ok',input_mode='count' if 'counts' in p else 'processed')
                vals.append(number('supp_stored_zeros__cases',f,op='mean',n=3))
            body+=line([PANEL_NAMES[panel],budget]+vals)
    out=longtable('Exploratory sensitivity analyses and provisional application.','tab:s9',['Panel','Support/class',r'Processed cortex BA (\%)',r'Reconstructed-count BA (\%)'],body,['4.5cm','2.7cm','3.8cm','3.85cm'],r'''Mean CellPFN balanced accuracy over three support draws. Processed and reconstructed-count cortex have different gene sets (21,158 versus 12,325), and some support identities change. These comparisons therefore do not isolate normalization, count reconstruction or stored-zero effects; the processed representation remains the primary panel.''')
    body=''
    for panel in ['zebra_dev','zebra_ood']:
        for budget in BUDGETS:
            prefix=f'tierD.{panel}.b{budget}.b_raw_minus_a'
            mid=number('supp_stored_zeros__facts',{'key':prefix},dp=2,signed=True)
            lo=number('supp_stored_zeros__facts',{'key':prefix+'_ci_low'},dp=2)
            hi=number('supp_stored_zeros__facts',{'key':prefix+'_ci_high'},dp=2)
            body+=line([PANEL_NAMES[panel],budget,mid+' ['+lo+', '+hi+']'])
    out+=r'\par\medskip\noindent\textbf{Removing unmeasured genes while retaining processed values.}\par'+'\n'+plain(['Panel','Support/class',r'Accuracy change (pp; 95\% CI)'],body,['4.5cm','2.7cm','7.65cm'])
    out+=r'''These Stage-0 contrasts remove genes not measured in every study without changing the retained expression values or re-normalizing their denominator. Values and paired 95\% $t$ intervals are the exported summaries over ten support draws. This is a separate diagnostic from the three-draw count-reconstruction comparison above.\par'''
    f=dict(diagnostic='scgpt_standardised_lr',declared_model_id='scgpt_lr',dataset='pbmc',column_or_all='all')
    out+=r'\par\medskip\textbf{Post hoc classifier sensitivity.} Standardizing scGPT embeddings before logistic regression changed the PBMC mean from '+number('fig4__posthoc_diagnostics_summary',f,'ba_declared_pct')+r'\% to '+number('fig4__posthoc_diagnostics_summary',f,'ba_diagnostic_pct')+r'''\%. This diagnostic is not substituted for the declared baseline in Table~\ref{table:overview}.\par
'''
    f=dict(stream='lr',contrast_kind='vs_base',value_key='H_b10_ba|task=zebra.ct2.sib.Neural.ood')
    out+=r'\medskip\textbf{Post hoc hard-tier boundary.} Task-mixture restriction in proxy training changed held-study cortex neuronal-subtype accuracy at ten supports by '+number('supp_prior_ablation__hard_tier_deltas',f,'diff_improvement_signed','mean',3,dp=2,signed=True)+r' percentage points across three task streams ('+number('supp_prior_ablation__hard_tier_deltas',f,'diff_improvement_signed','min',3,dp=2)+r' to '+number('supp_prior_ablation__hard_tier_deltas',f,'diff_improvement_signed','max',3,dp=2)+r'''). Hard-tier tasks were defined after the initial screen and do not change its frozen labels. A8d's hard-tier readout contains only two task-stream replicates.\par
'''
    body=''
    for view in ['all','hvg8192']:
        f=dict(gene_view=view,cell_group='PBMC low (4)',checkpoint_update='98304')
        r=select('supp_taskmix_tradeoff__view_check_groups',f)
        if r:
            body+=line(['All genes' if view=='all' else '8,192 HVGs',number('supp_taskmix_tradeoff__view_check_groups',f,'n_draws',dp=0),number('supp_taskmix_tradeoff__view_check_groups',f,'mean_diff_ba',dp=3,signed=True)])
    if body:
        out+=r'\medskip\noindent\textbf{Early task-mixture gene-view sensitivity at update 98,304.}\par'+'\n'+plain(['Gene view','Support draws','PBMC low-support change (pp)'],body,['5cm','3.3cm','6.55cm'])
        out+=r'''Changes are GL1 minus GS1, equally weighting coarse and fine PBMC at one and ten supports per class. Different draw counts and the early checkpoint prevent treating this as a final, isolated explanation of the task-mixture tradeoff.\par'''
    # Reuse the exact, already audited provisional aggregate selection in R38.
    with (ROOT/'evidence/results.csv').open(newline='') as f: registry=list(csv.DictReader(f))
    fact=next(r for r in registry if r['id']=='R38'); f=json.loads(fact['filter_json'])
    out+=r'\medskip\textcolor{red!80!black}{\textbf{Provisional ROSMAP application: sex-matched microglial CERAD discrimination gave donor AUC '+number('supp_rosmap__auc',f,dp=3)+' ['+number('supp_rosmap__auc',f,'ci_low',dp=3)+', '+number('supp_rosmap__auc',f,'ci_high',dp=3)+r''']. The supplied interval summarizes ten repeated splits with the export's correction; it is not independent cohort replication. Label corrections remain pending, so this is not a final or confirmatory biological result.}}
'''
    body=''
    for panel,label in [('pbmc_l1','Broad PBMC types (L1)'),('pbmc_l2','Fine PBMC types (L2)')]:
        cells=[label,number('glossary__panels',dict(panel_id=panel),'n_classes',dp=0)]
        for budget in BUDGETS:
            f=dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',panel=panel,gene_view='hvg8192',support_per_class=budget,metric='balanced_accuracy',status='ok')
            cells.append(number('supp_taskmix_tradeoff__efast_cases',f,op='mean',n=5 if budget=='100' else 10,dp=1))
        body+=line(cells)
    body+=r'\midrule'+'\n'
    subtype_labels={'pbmc.l2.sib.CD4T':'CD4 T siblings (L2)','pbmc.l2.sib.T':'T-cell siblings (L2)','pbmc.l3.sib.CD4T':'CD4 T siblings (L3)','pbmc.l3.sib.CD8T':'CD8 T siblings (L3)','pbmc.l3.sib.B':'B-cell siblings (L3)','pbmc.l3.sib.NK':'NK-cell siblings (L3)','pbmc.l3.sib.T':'T-cell siblings (L3)','pbmc.l3.full':'All finest PBMC types (L3)'}
    for task,label in subtype_labels.items():
        nclasses=number('supp_prior_ablation__hard_tier_tasks',dict(task=task,panel='pbmc'),'n_classes',dp=0)
        cells=[label,nclasses]
        for budget in BUDGETS:
            f=dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',gene_view='hvg8192',scope_kind='task',scope_value=task,metric=f'H_b{budget}_ba',status='ok',readout_status='final')
            cells.append(number('supp_prior_ablation__hard_tier_cellpfn_values',f,dp=1))
        body+=line(cells)
    cells=['Mean of eight subtype tasks','--']
    for budget in BUDGETS:
        f=dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',gene_view='hvg8192',scope_kind='panel',scope_value='pbmc',metric=f'H_b{budget}_ba',status='ok',readout_status='final')
        cells.append(number('supp_prior_ablation__hard_tier_cellpfn_values',f,dp=1))
    body+=r'\midrule'+'\n'+line(cells)
    out+=r'\par\medskip\noindent\textbf{PBMC annotation levels and fine-grained subtype tasks.}\par'+'\n'+plain(['Task','Classes','1 support/class','10 supports/class','100 supports/class'],body,['5.1cm','1.4cm','2.8cm','2.8cm','2.75cm'])
    out+=r'''Values are mean balanced accuracy (\%) for the reference CellPFN checkpoint with a requested cap of up to 8,192 support-selected HVGs; actual widths can be lower. Broad/fine context rows use the E-fast ten-, ten- and five-draw readouts at 1, 10 and 100 supports, respectively, rather than the three-draw main-table means. The subtype aggregate uses the corresponding ten/ten/five case design. L2 and L3 denote the supplied second and third annotation levels; sibling tasks restrict classification to a related group. These eight tasks were defined after the initial prior-screen readouts and are exploratory; they are not a formally defined ``easy versus difficult'' partition. The broad/coarse and fine primary panels remain in Table~\ref{table:overview}. The available checkpoint summaries do not provide CellPFN support-draw uncertainty, so no interval is inferred from the proxy-model case records. Different label sets and class counts prevent treating cross-task accuracy differences as isolated changes in difficulty.\par'''
    body=''
    for task,panel,label in [('zebra.ct2.full.dev','zebra_dev','Finer cortex types, development'),('zebra.ct2.sib.Neural.ood','zebra_ood','Neural siblings, held studies')]:
        cells=[label,number('supp_prior_ablation__hard_tier_tasks',dict(task=task,panel=panel),'n_classes',dp=0)]
        for budget in BUDGETS:
            f=dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',gene_view='hvg8192',scope_kind='task',scope_value=task,metric=f'H_b{budget}_ba',status='ok',readout_status='final')
            cells.append(number('supp_prior_ablation__hard_tier_cellpfn_values',f,dp=1))
        body+=line(cells)
    out+=r'\par\medskip\noindent\textbf{Finer ZEBRA annotation tasks at the reference checkpoint.}\par'+'\n'+plain(['Task','Classes','1 support/class','10 supports/class','100 supports/class'],body,['5.1cm','1.4cm','2.8cm','2.8cm','2.75cm'])
    out+=r'''The development task distinguishes Astrocyte, Endothelial, Excitatory neuron, Inhibitory neuron, Microglia, OPC and Oligodendrocyte. The held-study neural task distinguishes Excitatory neuron, Inhibitory neuron and Pvalb neuron. These post hoc exploratory tasks use the same reference checkpoint and requested cap of up to 8,192 support-selected HVGs, with ten, ten and five support draws at 1, 10 and 100 supports per class. Values are supplied checkpoint mean balanced accuracies (\%); no confidence intervals are available or inferred. They are separate from the eight-task PBMC subtype aggregate and the four-group core cortex panels, and do not constitute independent cohorts.\par'''
    out+=r'\par\medskip\noindent\textbf{Original ZEBRA sex-classification case.}\par'+'\n'
    body=''
    for unit,label in [('cell','Query cells'),('gsm','Aggregated GSM samples')]:
        f=dict(panel='zebra_sex',model_id='cellpfn_g1v2p',checkpoint_update='96000',draw='0',support_per_class='100',status='ok',scoring_unit=unit)
        body+=line([label,number('fig6__operator_prereg_cases',f,'ba_pct',dp=1),number('fig6__operator_prereg_cases',f,'nll',dp=3)])
    out+=plain(['Scoring unit','Balanced accuracy (\\%)','Log loss (nats)'],body,['7.2cm','3.8cm','3.85cm'])
    out+=r'''This single Sayed-study oligodendrocyte case used 200 support cells from 12 GSM samples and 50 query cells from ten disjoint GSM samples, with 21,158 processed genes. GSM separation does not guarantee donor separation. One support draw was evaluated; the perfect observed accuracy does not imply an uncertainty-free population estimate. This case is separate from the four core cell-type panels and is excluded from their averages.\par'''
    body=''
    for budget in ['4','8','16','32']:
        cells=[budget]
        for task in ['zsex_xy','zsex']:
            f=dict(model_id='cellpfn_g1v2p',checkpoint_update='96000',efast_task=task,support_units_per_class_k=budget,gene_view='hvg8192',metric='unit_level_auc',status='ok')
            cells.append(number('supp_taskmix_tradeoff__efast_cases',f,op='mean',n=10,dp=3)+' ['+number('supp_taskmix_tradeoff__efast_cases',f,op='min',n=10,dp=3)+', '+number('supp_taskmix_tradeoff__efast_cases',f,op='max',n=10,dp=3)+']')
        body+=line(cells)
    out+=r'\par\medskip\noindent\textbf{Later unit-level sex evaluation: positive control and broader task.}\par'+'\n'+plain(['Support units/class','XY-eligible task AUC','Broader sex task AUC'],body,['4.0cm','5.4cm','5.45cm'])
    out+=r'''Values are mean [minimum, maximum] unit-level AUC over ten support splits at the same reference CellPFN checkpoint, using a requested cap of up to 8,192 support-selected HVGs, ten support cells per unit and twenty query cells per unit. Actual gene widths can be lower. Units are persons where resolved; Sayed age-by-sex GSM groups remain a proxy, and cross-study person overlap is unknown. The XY-eligible positive control requires measured XIST and at least four Y-linked genes; this eligibility rule does not identify genes used by the model. The broader task remains close to chance. Splits reuse persons and are not independent cohort replications, so observed ranges are shown without confidence intervals. Support budgets of 16 and 32 units per class exceed the training support range. These later tasks are distinct from the original cell-level case above.\par
\textcolor{red!80!black}{\textbf{Sex-specific gene attribution remains unresolved. XIST and Y-linked genes define eligibility; they are not measured attribution hits.}}\textsuperscript{\textcolor{red!80!black}{[O06]}}
'''
    OUT['tables/s9.tex']=out


def generate():
    VALUES.clear(); OUT.clear()
    for build in [overview,s1,s2,s3,s4,s5,s6,s7,s8,s9]: build()
    f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=list(VALUES[0]),lineterminator='\n');w.writeheader();w.writerows(VALUES)
    OUT['evidence/table_values.csv']=f.getvalue()
    return OUT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=generate();failures=[]
    for name,content in outputs.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=content: failures.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    if failures:
        print('STALE: '+', '.join(failures));return 1
    print(('Verified' if args.check else 'Wrote')+f' {len(outputs)-1} tables and {len(VALUES)} numerical source selections.');return 0

if __name__=='__main__': raise SystemExit(main())
