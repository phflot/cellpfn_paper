"""Shared, source-bound Matplotlib conventions for the CellPFN manuscript."""
from pathlib import Path
import hashlib
import json
import platform
import string
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT.parent / 'paper_export_20261011/data'
FIGURES = ROOT / 'figures'
SOURCE = FIGURES / 'source_data'
TEAL, BLUE, PURPLE, GRAY = '#167C80', '#3F69A5', '#826199', '#65717B'
COLORS = {'cellpfn_g1v2p': TEAL, 'cellpfn_c1v2p': '#91BDB7',
          'tabicl_v2': BLUE, 'c2b40k': BLUE, 'kumo_small': '#B79DC8',
          'kumo_large': PURPLE, 'k2b_s40k': '#B79DC8', 'k2b_l40k': PURPLE,
          'geneformer_lr': '#A67C00', 'scgpt_lr': '#CC6E3B',
          'woodbury32_lda': GRAY, 'tabpfn35': '#825237'}
PANELS = ['pbmc_l1','pbmc_l2','zebra_dev','zebra_ood']
PANEL_NAMES = {'pbmc_l1':'PBMC coarse (8 classes)', 'pbmc_l2':'PBMC fine (20 classes)',
               'zebra_dev':'Cortex development (4 classes)', 'zebra_ood':'Cortex held studies (4 classes)'}
MODEL_NAMES = {'cellpfn_g1v2p':'CellPFN','cellpfn_c1v2p':'CellPFN, no operator',
               'tabicl_v2':'TabICLv2','kumo_small':'Kumo small','kumo_large':'Kumo large',
               'geneformer_lr':'Geneformer + LR','scgpt_lr':'scGPT + LR',
               'woodbury32_lda':'Low-rank LDA','tabpfn35':'TabPFN-3.5',
               'c2b40k':'TabICLv2 + prior','k2b_s40k':'Kumo small + prior','k2b_l40k':'Kumo large + prior'}

plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],
                    'font.size':7, 'axes.titlesize':7, 'axes.labelsize':7,
                    'xtick.labelsize':6, 'ytick.labelsize':6, 'legend.fontsize':6,
                    'axes.linewidth':.6, 'lines.linewidth':1.1,
                    'axes.spines.top':False, 'axes.spines.right':False,
                    'svg.fonttype':'none', 'pdf.fonttype':42, 'ps.fonttype':42,
                    'savefig.facecolor':'white','figure.facecolor':'white'})

def read(stem):
    return pd.read_csv(DATA / f'{stem}.csv', dtype=str, keep_default_na=False)

def select(frame, **filters):
    mask = pd.Series(True, index=frame.index)
    for key,value in filters.items():
        vals = value if isinstance(value,(list,tuple,set)) else [value]
        mask &= frame[key].isin([str(v) for v in vals])
    return frame.loc[mask].copy()

def numeric(frame, column='value'):
    return pd.to_numeric(frame[column], errors='raise')

def panel_label(ax, letter, title=None):
    ax.annotate(letter, xy=(0,1), xycoords='axes fraction', xytext=(-13,9),
                textcoords='offset points', fontsize=8, fontweight='bold',
                ha='left',va='bottom',annotation_clip=False)
    if title: ax.set_title(title,loc='left',pad=8)

def write_source(fid, panel, frame):
    folder=SOURCE/fid
    folder.mkdir(parents=True,exist_ok=True)
    file=folder/f'{panel}.csv'
    frame.to_csv(file,index=False)
    return str(file.relative_to(ROOT))

def save_figure(fig, fid, *, title, claim, panels, sources, status='ready', extra=None):
    """Save vector graphics, preview, source hashes and measurable panel geometry.

    panels: list of dictionaries describing letter, claim, source filters,
    aggregation, n/unit, uncertainty, and exclusions/availability. Each author
    records its actual selection; this helper cannot establish scientific truth.
    """
    FIGURES.mkdir(exist_ok=True)
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    geometry=[]
    for i,ax in enumerate(fig.axes):
        bbox=ax.get_position()
        geometry.append({'axis':i,'bounds_fraction':list(bbox.bounds),
                         'xlabel':ax.get_xlabel(),'ylabel':ax.get_ylabel(),
                         'title':ax.get_title(loc='left') or ax.get_title()})
    input_hashes={}
    for source in sources:
        path=Path(source)
        if not path.is_absolute():
            candidate=DATA/(str(source) if str(source).endswith('.csv') else str(source)+'.csv')
            path=candidate if candidate.exists() else ROOT/path
        if not path.exists():raise FileNotFoundError(path)
        input_hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
    files={}
    for suffix in ['pdf','svg','png']:
        path=FIGURES/f'{fid}.{suffix}'
        fig.savefig(path,dpi=300 if suffix=='png' else 600,bbox_inches=None)
        files[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    sources_written={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted((SOURCE/fid).glob('*.csv'))}
    manifest={'id':fid,'title':title,'claim':claim,'status':status,
              'size_mm':[float(v*25.4) for v in fig.get_size_inches()],
              'backend':'Python/Matplotlib','versions':{'python':platform.python_version(),
              'matplotlib':matplotlib.__version__,'numpy':np.__version__,'pandas':pd.__version__},
              'source_hashes':input_hashes,'panel_source_data':sources_written,'panels':panels,
              'geometry':geometry,'outputs':files,'extra':extra or {}}
    (FIGURES/f'{fid}.json').write_text(json.dumps(manifest,indent=2,default=str)+'\n')
    plt.close(fig)
    print(f'Built {fid}: {len(panels)} panels, {len(sources_written)} source-data files')

def symmetric_limit(values, floor=1):
    x=np.asarray(values,dtype=float)
    x=x[np.isfinite(x)]
    return max(floor,float(np.abs(x).max()) if len(x) else floor)

