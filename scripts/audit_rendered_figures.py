#!/usr/bin/env python3
"""Audit actual rendered font sizes and clipping, including embedded PDF scaling.

PyMuPDF applies text and form transformation matrices; this avoids treating the
architecture's Cairo 1-pt font plus text scaling as a literal 1-pt glyph.
"""
import json,re,sys
from pathlib import Path
from figure_catalog import ROOT,ASSETS
try:import pymupdf as fitz
except ImportError as exc:
    raise SystemExit('Rendered-figure QA requires PyMuPDF; install requirements-figures.txt in the active Python environment.') from exc

records=[];failures=[]
for name in ASSETS:
    path=ROOT/'figures'/f'{name}.pdf';doc=fitz.open(path);sizes=[];outside=[]
    for page in doc:
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if not span['text'].strip():continue
                    sizes.append(span['size'])
                    rect=fitz.Rect(span['bbox'])
                    if rect.x0 < -.5 or rect.y0 < -.5 or rect.x1 > page.rect.width+.5 or rect.y1 > page.rect.height+.5:
                        outside.append(span['text'])
    record={'asset':name,'min_effective_pt':min(sizes),'text_spans':len(sizes),'clipped_text':outside}
    records.append(record)
    if min(sizes)<4.99 or outside:failures.append(record)
doc=fitz.open(ROOT/'output/cellpfn.pdf');embedded=[]
for number,page in enumerate(doc,1):
    txt=page.get_text()
    if not re.search(r'Figure\s+(?:S)?\d+\s*(?::|\(continued\))',txt):continue
    sizes=[s['size'] for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
    record={'manuscript_page':number,'min_effective_pt':min(sizes)};embedded.append(record)
    if min(sizes)<4.99:failures.append(record)
report={'method':'PyMuPDF effective text span size after PDF text/form transforms',
        'assets':records,'embedded_figure_pages':embedded,'failures':failures}
(ROOT/'output/review/figure_render_audit.json').write_text(json.dumps(report,indent=2)+'\n')
assert len(embedded)==len(ASSETS),f'Expected {len(ASSETS)} embedded figure pages, found {len(embedded)}'
assert not failures,failures
print(f'PASS: effective text >=5pt and unclipped across {len(records)} figure assets; embedded figure text checked on {len(embedded)} manuscript pages.')
