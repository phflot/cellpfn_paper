"""Canonical figure assets, including genuine multipage SI continuations."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS=['architecture','figure2','figure3','supp_figure1','supp_figure1_illustration',
        'supp_figure2','supp_figure3','supp_figure4','supp_figure5','supp_figure6',
        'supp_figure7_maps','supp_figure7_markers','supp_figure8','supp_figure9']

def manuscript_inputs():
    paths=[ROOT/'main.tex',ROOT/'references.bib']
    paths+=sorted((ROOT/'sections').glob('*.tex'))+sorted((ROOT/'tables').glob('*.tex'))
    paths += [ROOT/'figures'/f'{name}.{suffix}' for name in ASSETS for suffix in ['pdf','svg']]
    paths += [ROOT/'scripts/build_architecture.py', ROOT/'scripts/figures_common.py',
              ROOT/'scripts/prepare_biological_figures.py',ROOT/'scripts/figure_catalog.py']
    paths += sorted((ROOT/'scripts').glob('figures_*.py'))
    return sorted(set(paths))
