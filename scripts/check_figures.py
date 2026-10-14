#!/usr/bin/env python3
"""Check figure provenance, frozen biological joins and cached attribution replay."""
import hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd
from figure_catalog import ROOT,ASSETS

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

panels=source_files=0
for name in ASSETS:
    for ext in ['pdf','svg','png']:
        assert (ROOT/'figures'/f'{name}.{ext}').stat().st_size>1000,(name,ext)
    if name=='architecture':continue
    meta=json.loads((ROOT/'figures'/f'{name}.json').read_text())
    assert meta['id']==name and meta['status']=='ready'
    assert meta['panels'],name
    for key in ['source_hashes','panel_source_data','outputs']:
        assert meta[key],(name,key)
        for p,want in meta[key].items():
            path=Path(p);path=path if path.is_absolute() else ROOT/path
            assert digest(path)==want,f'Figure needs rebuilding: {name}: {path}'
    panels+=len(meta['panels']);source_files+=len(meta['panel_source_data'])

cases={'pbmc_main':('pbmc_l1',100,320,191),'cortex_main':('zebra_dev',10,7769,96),
       'pbmc_fine':('pbmc_l2',10,800,0),'cortex_held':('zebra_ood',10,7163,0)}
export=ROOT.parent/'paper_export_20261011/data'
bench=pd.read_csv(export/'fig2__cases.csv',dtype=str,keep_default_na=False)
for name,(panel,budget,n,nexp) in cases.items():
    p=ROOT/'figures/biological_data'/f'{name}.csv';d=pd.read_csv(p)
    meta=json.loads(p.with_suffix('.json').read_text())
    assert digest(p)==meta['output_sha256']
    assert len(d)==n and d.obs_id.is_unique
    assert int(d.explained.sum())==nexp
    assert np.array_equal(d.correct.to_numpy(),d.true_label.eq(d.predicted_label).to_numpy())
    assert np.isfinite(d[['umap1','umap2','confidence','entropy']].to_numpy()).all()
    assert not (d.explained & ~d.correct).any()
    ba=100*d.groupby('true_label',observed=True).correct.mean().mean()
    assert abs(ba-meta['balanced_accuracy_pct'])<1e-10
    q=bench[(bench.model_id=='cellpfn_g1v2p')&(bench.panel==panel)&(bench.gene_view=='all')&
            (bench.support_per_class==str(budget))&(bench.draw=='0')&(bench.metric=='balanced_accuracy')&(bench.status=='ok')]
    assert len(q)==1 and abs(float(q.iloc[0]['value'])-ba)<1e-6,(name,ba)
    for col in [c for c in d if c.startswith('attribution_')]:
        assert np.array_equal(d[col].notna().to_numpy(),d.explained.to_numpy())

syn=ROOT/'figures/biological_data/synthetic_illustration.csv'
s=pd.read_csv(syn);assert len(s)==16384
assert (ROOT/'notes/figures/figure4_spec.md').exists()
assert not (ROOT/'figures/figure4.pdf').exists(),'Reserved figure was rendered without new evidence'

remote=json.loads((ROOT/'evidence/remote_attribution_manifest.json').read_text())
for p,want in remote['files'].items():assert digest(ROOT/p)==want,p
model_source=json.loads((ROOT/'evidence/remote_model_source_manifest.json').read_text())
assert model_source['checkpoint_verified_before_load']
assert model_source['pinned_source_count']==len(model_source['files'])==7
for record in model_source['files']:
    assert record['exists'] and record['matches'] and record['local_verified'],record['name']
    assert digest(ROOT/record['local_path'])==record['expected_sha256']==record['actual_sha256']==record['local_sha256'],record['name']
loader=model_source['case_loader']
assert not loader['checkpoint_pinned']
assert digest(ROOT/loader['local_path'])==loader['sha256']==loader['local_sha256']
validation=json.loads((ROOT/'evidence/remote_attribution_validation.json').read_text())
fidelity=pd.read_csv(export/'fig5__fidelity_by_case.csv',dtype=str,keep_default_na=False)
recomputed=0
for row in validation['results']:
    for col in ['rho_cell_corr','rel_err_corr']:
        q=fidelity[(fidelity.case_id==row['case_id'])&(fidelity.model_id==row['model_id'])&
                   (fidelity.source_column==col)&(fidelity.source_table=='tables/dsloo_vs_exact.csv')]
        assert len(q)==1 and abs(float(q.iloc[0]['value'])-row[col])<=5e-6,(row['case_id'],col)
        recomputed+=1
assert recomputed==24
print(f'PASS: {len(ASSETS)} figure assets, {panels} source-bound quantitative/biological panels, {source_files} panel CSV bindings.')
print('PASS: four frozen query cohorts, predicted labels, gene-overlay coverage and balanced accuracies reconcile; all 16,384 synthetic cells retained.')
print('PASS: 24 cached-array attribution metrics match the export; recovered source/metadata and seven checkpoint-pinned modules match their hashes; Figure 4 remains reserved.')
