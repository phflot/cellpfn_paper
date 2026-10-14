#!/usr/bin/env python3
"""Replot verified local figure inputs; does not access SSH or rerun models."""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR','/tmp/cellpfn_mpl')
for name in ['build_architecture.py','figures_performance.py','figures_prior.py',
             'figures_explanation.py','figures_biological.py','figures_synthetic.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)
