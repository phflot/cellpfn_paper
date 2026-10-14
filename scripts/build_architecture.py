#!/usr/bin/env python3
"""Build the single editable architecture schematic; no simulated observations.

SVG text/shapes are the editable source. Inkscape exports PDF and PNG.
Geometry is in a fixed 900 x 840 viewBox at 180 mm final width.
"""
from pathlib import Path
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
INK = '#24364B'
GRAY = '#637587'
TEAL = '#167C80'
BLUE = '#3F69A5'
PURPLE = '#826199'
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="180mm" height="168mm" viewBox="0 0 900 840">',
         '<title>A reusable cellular simulator supplies two learning routes</title>',
         '<desc>Hierarchical biology and observation parameters feed CPU microbatch generation. PyTorch tensor streams and reusable banks train CellPFN or adapt pretrained tabular models; annotated data can also be exported. CellPFN compares queries with support summaries, optionally using a support-fitted gene covariance operator.</desc>',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#637587"/></marker></defs>',
         '<rect width="900" height="840" fill="white"/>']

def box(x,y,w,h,fill='white',stroke='#D0D9E3',radius=9):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

def text(x,y,s,size=14,color=INK,weight='normal',anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')

def lines(x,y,items,size=14,color=INK,gap=21):
    for k,s in enumerate(items): text(x,y+k*gap,s,size,color)

def arrow(points):
    parts.append(f'<polyline points="{points}" fill="none" stroke="{GRAY}" stroke-width="1.8" stroke-linejoin="round" marker-end="url(#arrow)"/>')

def circle(x,y,r,color):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')

def panel(letter,title,x,y):
    text(x,y,letter,20,INK,'bold'); text(x+26,y,title,17,INK,'bold')

panel('a','Controlled biological and observation variation',20,27)
# Layered study cards echo the author-supplied graphical abstract.
for x,title,fill,stroke in [(20,'Study and donor context','#ECF6F4',TEAL),(314,'Cell identities and programs','#F2EDF7',PURPLE),(608,'Observation conditions','#EFF4FA',BLUE)]:
    box(x+8,47,264,178,'#F5F7FA','#D5DCE5')
    box(x+4,51,264,178,'#F8FAFC','#CAD4DF')
    box(x,55,264,178,fill,stroke)
    text(x+15,82,title,15,stroke,'bold')
lines(35,108,['Donor composition and covariates','Study-associated shifts'])
for j in range(4):
    cx=63+j*54
    circle(cx,160,9,TEAL)
    parts.append(f'<path d="M {cx-13} 194 v -16 q 13 -13 26 0 v 16" fill="#82BCB5"/>')
text(35,216,'Fixed context; repeated cell draws',13,GRAY)
lines(329,108,['Hierarchical cell-type differences','Distributed and rare signals'])
for endx in [344,393,442,491]:
    arrow(f'419,148 419,160 {endx},160 {endx},179')
for j in range(4): circle(344+j*49,189,9,['#B5A2C9','#8C76AA','#A8C7CF','#7FAEB9'][j])
text(329,216,'Known labels and latent variation',13,GRAY)
lines(623,108,['Depth, capture and dispersion','Study and batch variation'])
for j,h in enumerate([34,57,24,46,39,62,29]):
    parts.append(f'<rect x="{632+j*29}" y="{200-h}" width="17" height="{h}" rx="2" fill="{BLUE}" opacity="{.45+.07*j}"/>')
text(623,216,'Observed counts plus hidden truth',13,GRAY)
arrow('450,237 450,266')

panel('b','pyScIntelligentDesign: reusable simulation runtime',20,291)
box(20,307,860,182,'#F7FAFC','#B8C7D5')
for x,w,title,body in [
    (38,247,'Initialize biological state',['Resolved configuration','Reusable donor/program state']),
    (324,248,'Generate microbatches',['Batched transformations','Count sampling on CPU']),
    (610,252,'Deliver typed tensors',['Cells × genes + metadata','Counts, expectations, profiles'])]:
    box(x,326,w,80,'white','#A7BBCB')
    text(x+13,348,title,15,INK,'bold')
    lines(x+13,371,body,13,gap=20)
arrow('289,367 319,367');arrow('576,367 605,367')
text(38,430,'NumPy / PyTorch CPU backend',13,GRAY)
text(38,452,'Isolated seeds · independent processes · bounded prefetch',13,GRAY)
box(610,421,252,51,'#EDF4FA','#A7BBCB')
text(623,442,'Annotated dataset export',14,BLUE,'bold')
text(623,461,'AnnData · H5AD / Zarr / Loom',13,GRAY)
arrow('736,407 736,416')
arrow('610,410 590,410 590,476 237,476 237,515')

panel('c','One prior, two learning routes',20,544)
box(20,561,429,258,'#F7FAFC','#B8C7D5')
box(37,575,395,43,'#EDF6F4','#96BDB8')
text(235,594,'Tensor episodes and reusable biology banks',14,TEAL,'bold','middle')
text(235,610,'Labelled support + unlabelled queries',13,GRAY,'normal','middle')
arrow('132,620 132,641');arrow('338,620 338,641')
box(37,647,190,86,'#EDF6F4','#96BDB8')
box(242,647,190,86,'#F3EFF8','#B8A7CB')
text(50,671,'Train CellPFN',15,TEAL,'bold')
lines(50,694,['Compact neural predictor','Synthetic weight training'],13)
text(255,671,'Adapt tabular models',14,PURPLE,'bold')
lines(255,694,['TabICL / Kumo','Cellular tasks + replay'],13)
arrow('132,735 132,751 235,751 235,769');arrow('338,735 338,751 240,751')
text(235,790,'Biological prediction from labelled support',13,INK,'bold','middle')
text(235,808,'No target-task gradient updates',13,GRAY,'normal','middle')

panel('d','CellPFN inference architecture',475,544)
box(475,561,405,258,'white','#B8C7D5')
box(490,576,180,47,'#EDF6F4','#96BDB8')
text(580,595,'Labelled support',14,TEAL,'bold','middle')
text(580,613,'Class summaries / slots',13,GRAY,'normal','middle')
box(686,576,177,47,'#EFF4FA','#A6BAD2')
text(774,595,'Query cell',14,BLUE,'bold','middle')
text(774,613,'Independent queries',13,GRAY,'normal','middle')
arrow('580,625 580,643');arrow('774,625 774,643')
box(490,649,373,48,'#F5F6F9','#BCC6D1')
text(677,668,'Shared per-gene relation encoder',14,INK,'bold','middle')
text(677,687,'Optional support-fitted gene–gene operator',13,PURPLE,'normal','middle')
arrow('677,699 677,715')
box(490,721,373,43,'#F5F6F9','#BCC6D1')
text(677,740,'Symmetric pooling + 8 program tokens',14,INK,'normal','middle')
text(677,756,'2 transformer layers → class logits',13,GRAY,'normal','middle')
# Draw the classifier-scalar branch above the box so its arrow remains visible.
arrow('852,688 872,688 872,754 848,754')
text(860,713,'3 scalars',13,PURPLE,'normal','end')
arrow('677,766 677,782')
text(677,802,'Gene-anonymous; no query–query conditioning',13,INK,'normal','middle')
parts.append('</svg>')
OUT.mkdir(exist_ok=True)
svg=OUT/'architecture.svg'
svg.write_text('\n'.join(parts)+'\n')
for suffix in ('pdf','png'):
    command=['inkscape',str(svg),f'--export-type={suffix}',f'--export-filename={OUT / ("architecture."+suffix)}']
    if suffix=='png': command+=['--export-dpi=300']
    subprocess.run(command,check=True,capture_output=True)
print('Built editable figures/architecture.svg and PDF/PNG exports.')

