#!/usr/bin/env python3
"""Read-only numeric ledger and generated-table consistency check."""
from __future__ import annotations
import csv
import math
import re
from decimal import Decimal
from pathlib import Path
import check_results
from functools import lru_cache
check_results.read_csv = lru_cache(None)(check_results.read_csv)
from check_results import extract
from build_tables import generate, MODELS, CONTEXT, PANEL_NAMES

ROOT=Path(__file__).resolve().parents[1]

def check_ranking(failures):
    """Audit displayed rankings independently of the generator's rank helper."""
    count=0
    def check_group(cells,where):
        nonlocal count
        entries=[]
        for cell in cells:
            if cell=='--': continue
            match=re.search(r'\d+\.\d+',cell)
            if not match:
                failures.append(f'{where}: missing numerical mean: {cell}')
                continue
            flagged=r'\textsuperscript{*}' in cell or r'\textsuperscript{(*)}' in cell
            gray=cell.startswith(r'\textcolor{black!55}{') and cell.endswith('}')
            if flagged != gray:
                failures.append(f'{where}: exposure flag and gray formatting differ: {cell}')
            entries.append((Decimal(match.group()),flagged,r'\textbf{' in cell,cell))
        if not entries: return
        overall=max(x[0] for x in entries)
        unflagged=max((x[0] for x in entries if not x[1]),default=None)
        for mean,flagged,bold,cell in entries:
            expected=mean==overall or (not flagged and mean==unflagged)
            if bold != expected:
                failures.append(f'{where}: wrong displayed-precision rank: {cell}')
            count+=1

    main_rows=0
    for line in (ROOT/'tables/overview.tex').read_text().splitlines():
        cells=line.removesuffix(r' \\').split(' & ')
        if cells[0]=='Overall' or any(cells[0].startswith(panel+', ') for panel in PANEL_NAMES.values()):
            check_group(cells[1:],'Table 1 '+cells[0]); main_rows+=1
        elif cells[0] in PANEL_NAMES.values():
            for i in range(3): check_group(cells[1+3*i:4+3*i],'Table 2 '+cells[0])
    if main_rows!=13: failures.append(f'Table 1: expected 13 ranked rows, found {main_rows}')
    overview=(ROOT/'tables/overview.tex').read_text()
    if overview.count(r'\caption{')!=2:
        failures.append('Expected two independently captioned main tables')
    for label in ['table:overview','table:gene_ablation']:
        if overview.count(r'\label{'+label+'}')!=1:
            failures.append('Missing or duplicate main-table label: '+label)

    panel=None; groups={}
    labels={model[1] for model in MODELS+CONTEXT}
    for line in (ROOT/'tables/s1.tex').read_text().splitlines():
        for name in PANEL_NAMES.values():
            if line.startswith(r'\multicolumn{4}{@{}l}{\textbf{'+name+'}'):
                panel=name; groups[panel]=[]
        cells=line.removesuffix(r' \\').split(' & ')
        if cells[0] in labels:
            if panel is None: failures.append('Table S1: model row before panel header')
            else: groups[panel].append(cells[1:])
    if len(groups)!=4: failures.append(f'Table S1: expected four panels, found {len(groups)}')
    for panel,model_rows in groups.items():
        if len(model_rows)!=len(labels): failures.append(f'Table S1 {panel}: incomplete model rows')
        for budget in range(3): check_group([row[budget] for row in model_rows],f'Table S1 {panel} budget {budget}')
    return count

def main():
    failures=[]; seen=set();count=0
    with (ROOT/'evidence/table_values.csv').open(newline='') as f:
        for fact in csv.DictReader(f):
            try:
                if fact['id'] in seen: raise ValueError('duplicate ID')
                seen.add(fact['id'])
                actual,_=extract(fact)
                if not math.isclose(actual,float(fact['value']),rel_tol=0,abs_tol=1e-7):
                    raise ValueError(f"computed {actual}; registered {fact['value']}")
                count+=1
            except (ValueError,KeyError,OSError,ZeroDivisionError) as e:
                failures.append(f"{fact['id']}: {e}")
    for name,content in generate().items():
        if not (ROOT/name).exists() or (ROOT/name).read_text()!=content:
            failures.append('stale generated file: '+name)
    ranked=check_ranking(failures)
    for failure in failures:print('FAIL '+failure)
    print(f'Checked {count} table-value source selections, {ranked} ranking/color entries and deterministic rendering; {len(failures)} failures.')
    return bool(failures)

if __name__=='__main__':raise SystemExit(main())
