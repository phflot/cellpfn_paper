#!/usr/bin/env python3
"""Source-bound Figure 3 and Supplementary Figure 8.

Run ``python scripts/figures_explanation.py --supplement`` before remote RNA
coordinates exist, or without arguments once biological_data is available.
No cell-level attribution is joined using the exported case-local cell number.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm
from matplotlib.lines import Line2D
from figures_common import (ROOT, DATA, FIGURES, TEAL, BLUE, PURPLE, GRAY,
                            read, select, numeric, panel_label, write_source,
                            save_figure)

FULL = 'cellpfn_g1v2p'
NONE = 'cellpfn_c1v2p'
PBMC = 'pbmc_l1_b100_s0'
CORTEX = 'zebra_dev_b10_s0'
CASES = ['pbmc_l1_b10_s0', 'pbmc_l1_b10_s1', PBMC, CORTEX,
         'kidney_core9_A_F0_count', 'kidney_core9_A_F0_processed']
SHORT = ['PBMC 10 / 0', 'PBMC 10 / 1', 'PBMC 100 / 0',
         'Cortex 10 / 0', 'Kidney counts', 'Kidney processed']
PBMC_CLASSES = ['B','CD4 T','CD8 T','DC','Mono','NK','other','other T']
MARKERS = [('B','CD79A'),('B','MS4A1'),('CD4 T','IL7R'),('CD8 T','CD8A'),
           ('DC','FCER1A'),('DC','CLEC10A'),('Mono','CD14'),('NK','GNLY'),
           ('NK','NKG7'),('other','PPBP'),('other T','CD3E'),
           ('DC','LILRA4'),('Mono','LYZ')]
CLASS_COLORS = {'B':'#3F69A5','CD4 T':'#39957B','CD8 T':'#CC6E3B',
                'DC':'#A67C00','Mono':'#826199','NK':'#BC5D80',
                'other':'#727D49','other T':'#56A4B3',
                'Glia':'#826199','Immune cell':'#CC6E3B',
                'Neural':'#167C80','Vascular cell':'#3F69A5'}
CASE_COLORS = ['#167C80','#70A7A3','#3F69A5','#CC6E3B','#826199','#B79DC8']


def numbers(frame, cols):
    frame = frame.copy()
    for col in cols:
        frame[col] = pd.to_numeric(frame[col], errors='raise')
    return frame


def unique_row(frame, **filters):
    out = select(frame, **filters)
    assert len(out) == 1, (filters, len(out))
    return out.iloc[0]


def metadata(letter, claim, sources, filters, n, unit, aggregation='none',
             exclusions='none', uncertainty='none; descriptive values'):
    return dict(letter=letter,claim=claim,sources=sources,filters=filters,
                n=n,unit=unit,aggregation=aggregation,exclusions=exclusions,
                uncertainty=uncertainty)


def heatmap(ax, matrix, *, cmap='viridis', vmin=None, vmax=None, norm=None,
            annotate=False, fmt='.2f'):
    cm=plt.get_cmap(cmap).copy(); cm.set_bad('#E5E6E7')
    image=ax.imshow(np.ma.masked_invalid(matrix.to_numpy(dtype=float)),
                    cmap=cm, vmin=vmin, vmax=vmax, norm=norm,
                    aspect='auto', interpolation='nearest')
    ax.set_xticks(np.arange(matrix.shape[1]),matrix.columns)
    ax.set_yticks(np.arange(matrix.shape[0]),matrix.index)
    ax.tick_params(axis='both',length=0,pad=2)
    for spine in ax.spines.values():spine.set_visible(False)
    if annotate:
        for (i,j),v in np.ndenumerate(matrix.to_numpy(dtype=float)):
            if np.isfinite(v):
                rgba=image.cmap(image.norm(v)); lum=.2126*rgba[0]+.7152*rgba[1]+.0722*rgba[2]
                ax.text(j,i,format(v,fmt),ha='center',va='center',fontsize=6,
                        color='white' if lum<.48 else '#20252A')
    return image


def case_fidelity():
    data=read('fig5__fidelity_by_case')
    common=dict(model_id=FULL,knockout_scope='query_only',level='cell',
                gene_subset='evaluated_set',metric='spearman_rho')
    a=select(data,**common,method_id='dsloo_corr_margin',
             source_table='tables/dsloo_vs_exact.csv',source_column='rho_cell_corr')
    b=select(data,**common,method_id='ig64_margin',
             source_table='tables/faithfulness_summary.csv',source_column='rho_cell_q')
    out=numbers(pd.concat([a,b],ignore_index=True),['value'])
    assert len(out)==12 and not out.duplicated(['case_id','method_id']).any()
    return out


def deletion_data():
    d=select(read('fig5__deletion_curves'),model_id=FULL,class_label='ALL',
             ordering_scope='cell',ordering_method=['dsloo','ig64_margin','random_expressed'])
    d=d[(d.ordering_method!='random_expressed')|(d.random_replicate=='pooled')]
    d=numbers(d,['k','frac_calls_flipped','n_cells','n_curves_pooled'])
    assert not d.duplicated(['case_id','ordering_method','k']).any()
    return d


def selected_genes():
    top=select(read('fig5__top_genes'),case_id=PBMC,model_id=FULL,
               method_id='dsloo_corr_margin',target='margin',rank='1')
    assert len(top)==8
    first=top.set_index('class_label').loc[PBMC_CLASSES,'gene'].tolist()
    return list(dict.fromkeys(first+[g for _,g in MARKERS]))


def gene_matrix():
    """Use complete remote-derived statistics and reconcile exported entries."""
    genes=selected_genes()
    path=FIGURES/'biological_data/pbmc_gene_matrix.csv'
    if path.exists():
        d=pd.read_csv(path)
        required=['class_label','gene','mean_log_expression','detected_fraction','dsloo_corr_margin']
        assert set(required)<=set(d.columns)
        d=d[d.class_label.isin(PBMC_CLASSES)&d.gene.isin(genes)].copy()
        assert len(d)==len(genes)*len(PBMC_CLASSES)
        assert not d.duplicated(['class_label','gene']).any()
        assert d[required[2:]].notna().all().all()
        exported=select(read('fig5__ko_pairs_by_class'),case_id=PBMC,model_id=FULL,gene=genes)
        matched=d.merge(exported,on=['class_label','gene'])
        assert len(matched)==45
        for a,b in [('mean_log_expression','expr_mean_class_support'),
                    ('detected_fraction','det_frac_class_support'),
                    ('dsloo_corr_margin','score_dsloo_corr_margin')]:
            assert np.allclose(matched[a],numeric(matched,b),rtol=5e-5,atol=5e-6), (a,b)
        return d, str(path), 'complete support-expression and explained-query attribution matrix'
    raise FileNotFoundError(f'Complete remote-derived gene matrix required: {path}')


def rna_maps(fig, left, width, csv, letter, title, expected_n, expected_explained):
    d=pd.read_csv(csv,dtype={'obs_id':str})
    needed=['obs_id','umap1','umap2','true_label','predicted_label','correct','explained']
    assert set(needed)<=set(d.columns)
    assert d.obs_id.is_unique and len(d)==expected_n
    for key in ['correct','explained']:
        if d[key].dtype!=bool:
            d[key]=d[key].astype(str).str.lower().map({'true':True,'false':False,'1':True,'0':False})
            assert d[key].notna().all()
    assert d.explained.sum()==expected_explained
    assert (d.correct==(d.true_label==d.predicted_label)).all()
    axes=[fig.add_axes([left,.767,width*.475,.18]),
          fig.add_axes([left+width*.525,.767,width*.475,.18])]
    for ax in axes:
        ax.set(xticks=[],yticks=[]);ax.set_axis_off();ax.set_aspect('equal',adjustable='datalim')
    for label in sorted(d.true_label.unique()):
        q=d[d.true_label==label]
        axes[0].scatter(q.umap1,q.umap2,s=5 if len(d)<1000 else .5,
                        color=CLASS_COLORS[label],linewidths=0,rasterized=True,label=label)
    q=d[d.correct];e=d[~d.correct]
    axes[1].scatter(q.umap1,q.umap2,s=4 if len(d)<1000 else .4,color='#CFD3D5',
                    linewidths=0,rasterized=True)
    axes[1].scatter(e.umap1,e.umap2,s=8 if len(d)<1000 else 1.8,color='#B44742',
                    linewidths=0,rasterized=True)
    axes[0].set_title('Reference labels',fontsize=6,pad=2)
    axes[1].set_title(f'Errors: {len(e):,}/{len(d):,}',fontsize=6,pad=2)
    fig.text(left-.027,.983,letter,fontsize=8,fontweight='bold',va='center')
    fig.text(left,.983,title,fontsize=7,va='center')
    handles=[Line2D([],[],marker='o',color='none',markerfacecolor=CLASS_COLORS[x],
                    markeredgewidth=0,markersize=3,label=x) for x in sorted(d.true_label.unique())]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(left-.01,.752),
               ncol=4 if len(handles)==8 else 2,frameon=False,handlelength=.7,
               columnspacing=.6,handletextpad=.3,labelspacing=.25,fontsize=6)
    return d


def figure3():
    fid='figure3'; panels=[]
    bio=[FIGURES/'biological_data/pbmc_main.csv',FIGURES/'biological_data/cortex_main.csv']
    bio_meta=[path.with_suffix('.json') for path in bio]
    for path in bio:
        if not path.exists():raise FileNotFoundError(f'Remote-derived biological map required: {path}')
    provenance=[json.loads(path.read_text()) for path in bio_meta]
    for path,info in zip(bio,provenance):
        assert info['output_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
        assert info['checkpoint_sha256']=='aa5490d5a5d4020c87eba05297d80a31c901bcbeba6ba49b4b4857acb84f9f02'
    fig=plt.figure(figsize=(180/25.4,180/25.4))
    a=rna_maps(fig,.065,.415,bio[0],'a','PBMC coarse · 100 supports/class',320,191)
    b=rna_maps(fig,.555,.415,bio[1],'b','Cortex · 10 supports/class',7769,96)
    for letter,data,path in [('a',a,bio[0]),('b',b,bio[1])]:
        write_source(fid,letter+'_rna_coordinates',data)
        panels.append(metadata(letter,'RNA reference labels and prediction errors over every query',
                      str(path),'exact case, draw 0; all query cells',len(data),'query cells',
                      exclusions='support cells determine RNA geometry but are not shown'))

    genes=selected_genes(); gm,gsource,gstatus=gene_matrix()
    write_source(fid,'c_gene_statistics',gm)
    specs=[('mean_log_expression','Support expression','viridis',0,None),
           ('detected_fraction','Support detection','Blues',0,1),
           ('dsloo_corr_margin','Query attribution','RdBu_r',None,None)]
    for i,(key,title,cmap,vmin,vmax) in enumerate(specs):
        ax=fig.add_axes([.075+i*.31,.443,.26,.197])
        mat=gm.pivot(index='class_label',columns='gene',values=key).reindex(index=PBMC_CLASSES,columns=genes)
        lim=max(abs(float(mat.min().min())),abs(float(mat.max().max()))) if key=='dsloo_corr_margin' else None
        if key=='dsloo_corr_margin':vmin,vmax=-lim,lim
        im=heatmap(ax,mat,cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_xticklabels(genes,rotation=90,fontstyle='italic',fontsize=6)
        if i:ax.set_yticklabels([])
        ax.set_title(title,fontsize=7,pad=23)
        cax=fig.add_axes([.075+i*.31,.665,.26,.011])
        cb=fig.colorbar(im,cax=cax,orientation='horizontal')
        cb.ax.tick_params(labelsize=6,length=2,pad=1)
        cb.ax.xaxis.set_ticks_position('bottom')
    fig.text(.035,.699,'c',fontsize=8,fontweight='bold')
    panels.append(metadata('c','Expression and detection differ from signed model importance',
                  [gsource,'fig5__top_genes','fig5__marker_ranks'],
                  {'case':PBMC,'model':FULL,'genes':'union of each class top1 and Table S8 marker checks'},
                  len(gm),'class-gene entries','mean support log1p(CP10k), support detection fraction, mean corrected query margin attribution',
                  exclusions=gstatus))

    pairs=select(read('fig5__ko_pairs_by_cell__pbmc'),case_id=PBMC,model_id=FULL)
    pairs=numbers(pairs,['exact_ko_margin','dsloo_corr_margin'])
    assert len(pairs)==20365
    write_source(fid,'d_exact_deletion_pairs',pairs)
    ax=fig.add_axes([.09,.095,.23,.222])
    ax.scatter(pairs.exact_ko_margin,pairs.dsloo_corr_margin,s=.3,alpha=.22,
               color=TEAL,linewidths=0,rasterized=True)
    lo=min(pairs.exact_ko_margin.min(),pairs.dsloo_corr_margin.min()); hi=max(pairs.exact_ko_margin.max(),pairs.dsloo_corr_margin.max())
    ax.plot([lo,hi],[lo,hi],color='#747A7E',lw=.7,ls='--')
    ax.set(xlabel='Exact deletion (margin)',ylabel='DS-LOO (margin)',xlim=(lo-.1,hi+.1),ylim=(lo-.1,hi+.1))
    panel_label(ax,'d','Finite-deletion agreement')
    ax.text(.03,.96,'20,365 cell–gene pairs',transform=ax.transAxes,va='top',fontsize=6)
    panels.append(metadata('d','DS-LOO approximates exact finite query-gene deletion',
                  'fig5__ko_pairs_by_cell__pbmc',{'case_id':PBMC,'model_id':FULL},len(pairs),'cell-gene validation pairs',
                  exclusions='validation gene union; includes zero and negative effects; selected correctly classified cells'))

    fidelity=case_fidelity();write_source(fid,'e_case_fidelity',fidelity)
    ax=fig.add_axes([.505,.095,.185,.222])
    for idx,case in enumerate(CASES):
        q=fidelity[fidelity.case_id==case].set_index('method_id').value
        ax.plot([q['ig64_margin'],q['dsloo_corr_margin']],[idx,idx],color='#B7BDC1',lw=1)
        ax.scatter(q['dsloo_corr_margin'],idx,s=13,color=TEAL,marker='o',zorder=3)
        ax.scatter(q['ig64_margin'],idx,s=14,color=PURPLE,marker='^',zorder=3)
    ax.set(yticks=range(6),yticklabels=SHORT,xlim=(0,1.03),ylim=(5.5,-.5),xlabel='Spearman ρ')
    ax.set_xticks([0,.5,1]);ax.tick_params(axis='y',length=0)
    panel_label(ax,'e','Matched fidelity')
    ax.legend(handles=[Line2D([],[],color=TEAL,marker='o',lw=0,label='DS-LOO',markersize=3),
                       Line2D([],[],color=PURPLE,marker='^',lw=0,label='IG64',markersize=3)],
              loc='lower right',bbox_to_anchor=(1.05,-.37),frameon=False,ncol=2,handletextpad=.2,columnspacing=.5)
    panels.append(metadata('e','Matched DS-LOO and IG64 validation across six cases',
                  'fig5__fidelity_by_case',{'model_id':FULL,'gene_subset':'evaluated_set','level':'cell',
                   'knockout_scope':'query_only','metric':'spearman_rho','source':'exact Table S8 filters'},
                  6,'case configurations','median within-cell rank correlation, summarized within then across classes',
                  exclusions='kidney modes share biological cells; cases are not independent cohorts'))

    curves=select(deletion_data(),case_id=PBMC,ordering_method=['dsloo','random_expressed'])
    write_source(fid,'f_deletion_curves',curves)
    ax=fig.add_axes([.80,.095,.17,.222])
    for method,color,style,label in [('dsloo',TEAL,'-','DS-LOO'),('random_expressed',GRAY,'--','Random expressed')]:
        q=curves[curves.ordering_method==method].sort_values('k')
        ax.plot(q.k,100*q.frac_calls_flipped,color=color,ls=style,lw=1.2,label=label)
    ax.set(xlabel='Genes deleted',ylabel='Margin reversed (%)',xlim=(0,50),ylim=(0,50),xticks=[0,25,50])
    panel_label(ax,'f','Deletion consequence')
    ax.legend(loc='upper left',frameon=False,fontsize=6,handlelength=1.5,handletextpad=.3)
    panels.append(metadata('f','Ranked query-gene sets reverse the fixed runner-up margin more often',
                  'fig5__deletion_curves',{'case_id':PBMC,'model_id':FULL,'ordering_scope':'cell','class_label':'ALL',
                    'methods':['dsloo','random_expressed'],'random_replicate':'pooled'},
                  191,'explained query cells','fraction of original margins below zero; random pools two orderings per cell'))
    save_figure(fig,fid,title='Gene-deletion explanations in biological context',
                claim='RNA expression provides biological context while exact deletion validates decision-specific gene explanations.',
                panels=panels,sources=[*bio,*bio_meta,gsource,'fig5__ko_pairs_by_class','fig5__top_genes','fig5__marker_ranks',
                'fig5__ko_pairs_by_cell__pbmc','fig5__fidelity_by_case','fig5__deletion_curves'],
                extra={'cell_map':'RNA-derived; not model embedding','gene_matrix_availability':gstatus,
                       'biological_provenance':provenance,
                       'selected_gene_order':genes,'attribution_causality':'model deletion, not biological perturbation'})


def supplementary8():
    fid='supp_figure8';panels=[]
    fig=plt.figure(figsize=(180/25.4,190/25.4))
    gs=fig.add_gridspec(4,2,left=.18,right=.975,bottom=.095,top=.96,wspace=.72,hspace=.60,
                        height_ratios=[.9,1.05,1.05,.95])
    axes=[fig.add_subplot(gs[i,j]) for i in range(4) for j in range(2)]
    f=read('fig5__fidelity_by_case')
    methods=['dsloo_corr_margin','dsloo_margin','gxi_margin','gxi_trunk_margin','ig16_margin','ig64_margin','op_ko_margin','op_mid_margin']
    names=['DS-LOO','Uncorrected','Grad × input','Grad, trunk','IG16','IG64','Operator KO','Operator midpoint']
    d=numbers(select(f,model_id=FULL,source_table='adversarial/recompute_faithfulness.json',
                     method_id=methods,gene_subset='evaluated_set',level='cell',
                     knockout_scope='query_only',metric='spearman_rho'),['value'])
    assert len(d)==48
    mat=d.pivot(index='method_id',columns='case_id',values='value').reindex(index=methods,columns=CASES)
    mat.index=names;mat.columns=['P10/0','P10/1','P100/0','C10/0','K count','K proc.']
    im=heatmap(axes[0],mat,cmap='viridis',vmin=0,vmax=1,annotate=True,fmt='.3f')
    axes[0].tick_params(axis='x',labelrotation=45)
    panel_label(axes[0],'a','Attribution-method fidelity')
    write_source(fid,'a_method_fidelity',d)
    panels.append(metadata('a','Fidelity depends on attribution method', 'fig5__fidelity_by_case',
                'full operator; adversarial recomputation; evaluated_set; query_only; cell; spearman_rho',
                48,'case-method summaries','within-cell Spearman correlations summarized by class then case'))

    d=numbers(select(read('fig5__cases'),model_id=FULL),['n_query','n_cells_explained'])
    d=d.set_index('case_id').loc[CASES].reset_index();d['coverage_percent']=100*d.n_cells_explained/d.n_query
    ax=axes[1];ax.barh(np.arange(6),d.coverage_percent,color=TEAL,height=.52)
    ax.set(yticks=np.arange(6),yticklabels=SHORT,ylim=(5.6,-.6),xlim=(0,123),xlabel='Explained queries (%)',xticks=[0,50,100])
    for i,row in d.iterrows():ax.text(min(row.coverage_percent+2,104),i,f'{row.n_cells_explained}/{row.n_query}',fontsize=6,va='center')
    panel_label(ax,'b','Selected correct-cell coverage')
    write_source(fid,'b_explanation_coverage',d)
    panels.append(metadata('b','Explanations cover a selected correctly classified subset', 'fig5__cases',
                  {'model_id':FULL},6,'case configurations','explained cells / all queries',
                  exclusions='selected correct in both BF16 and FP32; cap 24/class (40 kidney)'))

    d=numbers(select(read('fig5__fidelity_by_class'),case_id=[PBMC,CORTEX],model_id=FULL,
                 method_id=['dsloo_corr_margin','ig64_margin'],knockout_scope='query_only',
                 level='cell_median',metric='spearman_rho',source_column='rho_cell_q_median'),['value'])
    assert len(d)==24
    labels=[(PBMC,c) for c in PBMC_CLASSES]+[(CORTEX,c) for c in ['Glia','Immune cell','Neural','Vascular cell']]
    ax=axes[2]
    for i,(case,cl) in enumerate(labels):
        q=select(d,case_id=case,class_label=cl).set_index('method_id').value
        ax.plot([q['ig64_margin'],q['dsloo_corr_margin']],[i,i],color='#B9BFC2',lw=.8)
        ax.scatter(q['dsloo_corr_margin'],i,s=11,color=TEAL);ax.scatter(q['ig64_margin'],i,s=12,color=PURPLE,marker='^')
    ax.axhline(7.5,lw=.6,color='#C8CDD0')
    ax.set(yticks=range(12),yticklabels=[c for _,c in labels],ylim=(11.6,-.6),xlim=(0,1.04),xlabel='Median cell Spearman ρ')
    ax.tick_params(axis='y',length=0)
    ax.legend(handles=[Line2D([],[],marker='o',color=TEAL,lw=0,label='DS-LOO',markersize=3),
                       Line2D([],[],marker='^',color=PURPLE,lw=0,label='IG64',markersize=3)],loc='lower left',frameon=False)
    panel_label(ax,'c','PBMC and cortex class fidelity')
    write_source(fid,'c_class_fidelity',d)
    panels.append(metadata('c','Class-specific fidelity includes the cortex immune compartment',
                  'fig5__fidelity_by_class','PBMC 100/0 and cortex 10/0; full operator; query_only; cell_median; rho_cell_q_median',
                  12,'class summaries','median within-cell Spearman per class'))

    d=numbers(select(f,model_id=[FULL,NONE],method_id='dsloo_corr_margin',
                     gene_subset='evaluated_set',knockout_scope='query_only',level='pooled_cells_x_genes',
                     metric='rel_l2_error',source_table='tables/dsloo_vs_exact.csv',source_column='rel_err_corr'),['value'])
    assert len(d)==12
    ax=axes[3]
    for i,case in enumerate(CASES):
        q=select(d,case_id=case).set_index('model_id').value*100
        ax.plot([q[FULL],q[NONE]],[i,i],color='#C0C5C8',lw=.8)
        ax.scatter(q[FULL],i,s=13,color=TEAL);ax.scatter(q[NONE],i,s=15,color=GRAY,marker='s',facecolors='none')
    ax.set(yticks=range(6),yticklabels=SHORT,ylim=(5.5,-.5),xlabel='Relative L₂ error (%)',
           xlim=(0,float(d.value.max())*105))
    ax.legend(handles=[Line2D([],[],marker='o',color=TEAL,lw=0,label='Full operator',markersize=3),
                       Line2D([],[],marker='s',color=GRAY,markerfacecolor='none',lw=0,label='No operator',markersize=3)],
                       loc='upper right',frameon=False)
    panel_label(ax,'d','Finite-deletion magnitude error')
    write_source(fid,'d_magnitude_error',d)
    panels.append(metadata('d','Magnitude fidelity with and without the operator','fig5__fidelity_by_case',
                  'DS-LOO corrected; evaluated_set; query_only; pooled_cells_x_genes; rel_err_corr; tables/dsloo_vs_exact.csv',
                  12,'case-model summaries','relative L2 error computed per class, median across classes'))

    d=numbers(select(read('fig5__stability'),comparison='support_draw',method_id='dsloo_corr_margin'),['top20_overlap'])
    ax=axes[4];rng=np.random.default_rng(42)
    configs=[(FULL,'pbmc_l1_b10_s1','Full: draw'),(FULL,PBMC,'Full: budget'),
             (NONE,'pbmc_l1_b10_s1','None: draw'),(NONE,PBMC,'None: budget')]
    for i,(model,case,label) in enumerate(configs):
        q=select(d,model_a=model,case_b=case);q=q[q.class_label!='ALL']
        assert len(q)==8
        ax.scatter(np.full(8,i)+rng.uniform(-.13,.13,8),q.top20_overlap,s=12,
                   marker='o' if model==FULL else 's',color=TEAL if model==FULL else GRAY,alpha=.8)
        mean=float(unique_row(d,model_a=model,case_b=case,class_label='ALL').top20_overlap)
        ax.plot([i-.25,i+.25],[mean,mean],color='#232A2D',lw=1.2)
    ax.set(xticks=range(4),xticklabels=[x[2] for x in configs],ylim=(0,1),ylabel='Top-20 gene overlap')
    ax.tick_params(axis='x',labelrotation=35)
    panel_label(ax,'e','Support-context sensitivity')
    write_source(fid,'e_support_stability',d)
    panels.append(metadata('e','Ranked genes depend on support draw and support budget','fig5__stability',
                  'support_draw rows; DS-LOO corrected; full and no-operator models; PBMC 10/0 vs 10/1 or 100/0',
                  8,'classes per comparison','points are classes; horizontal segment is exported class mean'))

    d=select(read('fig5__marker_ranks'),model_id=FULL,case_id=CASES[:3],method_id='dsloo_corr_margin',target='margin')
    keys=set(MARKERS);d=d[[ (cl,g) in keys for cl,g in zip(d.class_label,d.marker) ]].copy()
    d=numbers(d,['rank']);d['class_gene']=d.class_label+': '+d.marker
    index=[c+': '+g for c,g in MARKERS]
    mat=d.pivot(index='class_gene',columns='case_id',values='rank').reindex(index=index,columns=CASES[:3]);mat.columns=['10 / 0','10 / 1','100 / 0']
    heatmap(axes[5],mat,cmap='viridis_r',norm=LogNorm(vmin=1,vmax=33538),annotate=True,fmt='.0f')
    axes[5].set_xlabel('PBMC supports / draw')
    panel_label(axes[5],'f','Marker ranks vary with context')
    write_source(fid,'f_marker_ranks',d)
    panels.append(metadata('f','Recognizable markers include low-ranking counterexamples','fig5__marker_ranks',
                  {'model_id':FULL,'method_id':'dsloo_corr_margin','target':'margin','markers':'all Table S8 PBMC checks'},
                  39,'case-class-marker rankings','class-mean signed-margin rank; log color scale; lower rank is higher importance'))

    subsets=['evaluated_set','random_expressed_only','no_low_genes_no_dsloo_extremes','genes_moved_above_1e-4_per_cell']
    d=numbers(select(f,model_id=FULL,source_table='adversarial/recompute_faithfulness.json',
              method_id=['dsloo_corr_margin','ig64_margin'],gene_subset=subsets,level='cell',
              knockout_scope='query_only',metric='spearman_rho'),['value'])
    ax=axes[6]
    for i,case in enumerate(CASES):
        for method,ls,marker in [('dsloo_corr_margin','-','o'),('ig64_margin','--','^')]:
            q=select(d,case_id=case,method_id=method).set_index('gene_subset').loc[subsets]
            ax.plot(range(4),q.value,color=CASE_COLORS[i],ls=ls,marker=marker,markersize=2.5,lw=.8,alpha=.8)
    ax.set(xticks=range(4),xticklabels=['Evaluated','Random','No\nextremes','Nonzero'],ylim=(0,1.03),ylabel='Case Spearman ρ')
    ax.legend(handles=[Line2D([],[],color=GRAY,ls='-',marker='o',label='DS-LOO',markersize=2.5),
                       Line2D([],[],color=GRAY,ls='--',marker='^',label='IG64',markersize=2.5)],loc='lower left',frameon=False)
    panel_label(ax,'g','Gene-set sensitivity')
    write_source(fid,'g_gene_subset_sensitivity',d)
    panels.append(metadata('g','Fidelity checked across selected and random validation subsets','fig5__fidelity_by_case',
                  'adversarial recomputation; full model; corrected DS-LOO and IG64; four exported gene subsets',
                  48,'case-method-subset summaries','exported median cell/class rank correlations',
                  exclusions='Nonzero means |exact effect| > 1e-4 per cell; No extremes excludes low genes and DS-LOO extremes'))

    d=deletion_data();d=select(d,ordering_method=['dsloo','random_expressed'])
    ax=axes[7]
    for i,case in enumerate(CASES):
        for method,style in [('dsloo','-'),('random_expressed','--')]:
            q=select(d,case_id=case,ordering_method=method).sort_values('k')
            ax.plot(q.k,100*q.frac_calls_flipped,color=CASE_COLORS[i],ls=style,lw=.9)
    ax.set(xlabel='Genes deleted',ylabel='Margin reversed (%)',xlim=(0,50),ylim=(0,70),xticks=[0,25,50])
    panel_label(ax,'h','Deletion across case configurations')
    write_source(fid,'h_all_deletion_curves',d)
    panels.append(metadata('h','Cell-wise ranked deletion is compared with random expressed genes in every case',
                  'fig5__deletion_curves','full model; all classes; cell orderings; DS-LOO solid and pooled random dashed',
                  6,'case configurations','fraction of selected cells with reversed original margin; random pools two curves/cell'))
    handles=[Line2D([],[],color=CASE_COLORS[i],lw=1.2,label=SHORT[i]) for i in range(6)]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.56,.005),ncol=3,
               frameon=False,fontsize=6,columnspacing=1.2,handlelength=1.5)
    save_figure(fig,fid,title='Explanation fidelity, coverage and support sensitivity',
                claim='Deletion explanations are faithful to selected model deletions while their coverage and marker ranks remain conditional on task context.',
                panels=panels,sources=['fig5__fidelity_by_case','fig5__fidelity_by_class','fig5__cases',
                      'fig5__stability','fig5__marker_ranks','fig5__deletion_curves'],
                extra={'case_key':dict(zip(CASES,SHORT)),
                       'plot_semantics':'No confidence intervals; cases share cells and are not independent cohorts.',
                       'missing_validation':'No one-shot or held-study-cortex exact-deletion case.'})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--supplement',action='store_true')
    parser.add_argument('--main',action='store_true');args=parser.parse_args()
    if not args.main:supplementary8()
    if not args.supplement:figure3()
