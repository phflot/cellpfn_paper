#!/usr/bin/env python3
"""Preserve historical text inputs and index external sources without editing them."""
from pathlib import Path
import csv
import hashlib
import shutil

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
SEED = WORKSPACE / 'CellPFN_model_methods_revision(2)' / 'CellPFN_model_methods_revision'
LEGACY = WORKSPACE / 'CellPFN_model_methods_revision(2)' / 'old_reference_texts'
EXPORT = WORKSPACE / 'paper_export_20261011'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def category(path):
    if path.name.startswith('neurips_'):
        return 'venue_template_or_template_output'
    if path.suffix == '.tex':
        return 'historical_manuscript'
    if path.suffix == '.bib':
        return 'unverified_bibliography'
    if path.suffix == '.md':
        return 'historical_note'
    if path.suffix == '.pdf':
        return 'compiled_historical_manuscript'
    return 'build_artifact'

def main():
    rows = []
    for path in sorted(LEGACY.rglob('*')):
        if not path.is_file():
            continue
        kind = category(path)
        archived = ''
        if kind in {'historical_manuscript', 'unverified_bibliography', 'historical_note'}:
            dest = ROOT / 'input' / 'legacy' / path.relative_to(LEGACY)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            archived = str(dest.relative_to(ROOT))
        rows.append(dict(source=str(path.relative_to(WORKSPACE)), category=kind,
                         bytes=path.stat().st_size, sha256=digest(path), archived=archived))
    with (ROOT / 'notes/source_inventory.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['source','category','bytes','sha256','archived'])
        writer.writeheader(); writer.writerows(rows)
    seed_rows = []
    for name in ['CellPFN_NBT_model_methods_revised.tex', 'CellPFN_NBT_model_methods_revised.pdf', 'REVISION_NOTES.md']:
        path = SEED / name
        dest = ROOT / 'input/seed' / name
        shutil.copy2(path, dest)
        seed_rows.append(dict(source=str(path.relative_to(WORKSPACE)),sha256=digest(path),archived=str(dest.relative_to(ROOT))))
    with (ROOT / 'notes/seed_manifest.csv').open('w', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['source','sha256','archived'])
        writer.writeheader();writer.writerows(seed_rows)
    export_rows=[]
    for path in sorted(EXPORT.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            export_rows.append(dict(source=str(path.relative_to(WORKSPACE)),sha256=digest(path)))
    with (ROOT/'evidence/export_manifest.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['source','sha256'])
        writer.writeheader();writer.writerows(export_rows)
    summary = ['# Source inventory', '',
        'Every file in the legacy folder is indexed in `source_inventory.csv`. Substantive TeX, BibTeX and Markdown files are preserved under `input/legacy`; compiled PDFs and build artifacts are indexed but not duplicated.', '',
        'The seed TeX, PDF and revision note are preserved under `input/seed`. The original seed is historical: its analytic-residual model is not the current experimental model.', '',
        'The current export is an external, checksum-locked input. Its harmonized FIGURES.md and data tables, including the 2026-10-13 refresh, govern current findings. Builder sections and older project notes cannot override them.', '',
        'Source hashes are checked by `make check`. Detailed passage-level reuse decisions are in `source_reuse.md`.', '',
        '| Category | Files |', '|---|---:|']
    from collections import Counter
    summary += [f'| {k} | {v} |' for k,v in sorted(Counter(x['category'] for x in rows).items())]
    summary += ['',f'Total legacy files: {len(rows)}. Export files recorded: {len(export_rows)}.', '',
                'Bibliographies in historical inputs are unverified leads. Only the active bibliography and literature verification notes define citations used in the new manuscript.']
    (ROOT/'notes/source_index.md').write_text('\n'.join(summary)+'\n')
    print(f'Indexed {len(rows)} legacy files; preserved {sum(bool(x["archived"]) for x in rows)} substantive files; recorded {len(export_rows)} export hashes.')

if __name__ == '__main__':
    main()
