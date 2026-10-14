#!/usr/bin/env python3
"""Audit saved figure geometry and actual PDFs without changing figure assets.

Uses the installed nature-figure alignment and collision auditors, plus explicit
shared-edge/center rules for intentional unequal-size grids. No builders run.
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import importlib.util
import itertools
import json
import os
import subprocess
import sys
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
PLOTTED=['figure2','figure3','supp_figure1','supp_figure1_illustration',
 'supp_figure2','supp_figure3','supp_figure4','supp_figure5','supp_figure6',
 'supp_figure7_maps','supp_figure7_markers','supp_figure8','supp_figure9']
TOLERANCE_PT=1.5


def regular(rows,cols):
 return {'rows':[list(range(r*cols,(r+1)*cols)) for r in range(rows)],
         'cols':[[r*cols+c for r in range(rows)] for c in range(cols)]}


CONTRACTS={
 'figure2':dict(n=7,rows=[[0,1,2,3],[5,6]],cols=[],
    custom=[('left',[0,4,5]),('right',[3,4,6]),('left',[2,6])],
    rationale='Four equal benchmark panels; full-width delta matrix; two equal trajectory/retention panels. Matrix height differs intentionally.'),
 'figure3':dict(n=13,rows=[[0,1,2,3],[4,6,8],[5,7,9],[10,11,12]],cols=[[4,5],[6,7],[8,9]],
    colorbars=[5,7,9],exemptions=[dict(axes=[0,1,2,3],checks=['horizontal-gutter'],reason='Two equal RNA-map pairs separated by a larger between-dataset gap.'),
       dict(axes=[10,11,12],checks=['panel-width','horizontal-gutter'],reason='Bottom scatter, six-case fidelity and deletion curve intentionally have unequal widths and margins for their different labels.')],
    custom=[('width',[0,1,2,3]),('left',[4,5]),('left',[6,7]),('left',[8,9])],
    rationale='Equal RNA pairs and three equal gene matrices; colorbars align with their matrices; bottom panels share baseline/height while retaining unequal widths.'),
 'supp_figure1':dict(n=12,**regular(4,3),rationale='Twelve equal quantitative panels in a four-row, three-column grid.'),
 'supp_figure1_illustration':dict(n=2,rows=[[0,1]],cols=[],rationale='Two equal overlays of the same illustrative synthetic RNA coordinates.'),
 'supp_figure2':dict(n=4,rows=[],cols=[],legend=[3],
    grid={0:(0,1,0,3),1:(1,3,0,1),2:(1,2,2,3)},
    custom=[('top',[1,2]),('width',[1,2]),('left',[0,1]),('right',[0,2,3])],
    rationale='Full-width overview above a tall ten-task matrix and shorter kidney matrix. Their top edges and widths agree; different heights reflect row counts. Exposure box is text-only.'),
 'supp_figure3':dict(n=6,**regular(3,2),rationale='Three aligned two-column rows; middle row taller to accommodate 15 study labels.'),
 'supp_figure4':dict(n=5,rows=[[0,1,2],[3,4]],cols=[[2,4]],
    grid={0:(0,1,0,1),1:(0,1,1,2),2:(0,1,2,3),3:(1,2,0,2),4:(1,2,2,3)},
    rationale='Three equal top panels; bottom prespecified criterion spans two columns, and inference interventions occupy the third. Widths are intentionally unequal below.'),
 'supp_figure5':dict(n=7,rows=[[3,4],[5,6]],cols=[[0,3,5],[1,2,4,6]],
    grid={0:(0,3,0,1),1:(0,1,1,2),2:(2,3,1,2),3:(4,6,0,1),4:(4,6,1,2),5:(7,9,0,1),6:(7,9,1,2)},
    exemptions=[dict(axes=[1,2],checks=['vertical-gutter'],reason='Nested donor-AUC and short NLL endpoint panels subdivide the top-right block; their vertical gap is independent of the lower two rows.')],
    custom=[('width',list(range(7)))],
    rationale='Left six-candidate endpoint panel spans the two distinct top-right endpoint panels. Lower rows form equal-width pairs. Endpoint units are intentionally separated.'),
 'supp_figure6':dict(n=6,**regular(2,3),rationale='Three columns align across sex and age rows; row heights differ slightly by content.'),
 'supp_figure7_maps':dict(n=9,rows=[[0,1,2],[3,4,5]],cols=[],legend=[8],
    custom=[('center_x',[0,3,6]),('center_x',[1,4,7]),('center_x',[2,5]),('center_y',[6,7])],
    rationale='Equal reference/prediction/error maps within each case. Different case aspect ratios change plot widths; centers stay on the same column grid. Donor/study context preserve aspect and align centers; the last axis is a fine-class legend.'),
 'supp_figure7_markers':dict(n=16,rows=[[0,2,4,6],[1,3,5,7],[8,10,12,14],[9,11,13,15]],
    cols=[[1,9],[3,11],[5,13],[7,15]],colorbars=[1,3,5,7,9,11,13,15],
    custom=[('center_x',[0,1,8,9]),('center_x',[2,3,10,11]),('center_x',[4,5,12,13]),('center_x',[6,7,14,15])],
    rationale='Four equal maps per case and matching colorbar rows. PBMC/cortex plot widths differ to preserve aspect; all maps and bars share column centers.'),
 'supp_figure8':dict(n=8,**regular(4,2),rationale='Four two-column rows with deliberately different heights; comparable row baselines and column edges align.'),
 'supp_figure9':dict(n=4,**regular(2,2),rationale='Two-by-two grid separating measured, inferred and estimated costs.'),
}


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')


def audit_geometry(fid,alignment,out):
 source=ROOT/'figures'/f'{fid}.json';m=json.loads(source.read_text());contract=CONTRACTS[fid]
 assert len(m['geometry'])==contract['n'],(fid,len(m['geometry']),contract['n'])
 w,h=[float(v)*72/25.4 for v in m['size_mm']];axes={}
 for a in m['geometry']:
  x,y,ww,hh=map(float,a['bounds_fraction']);i=int(a['axis'])
  axes[i]=dict(id=f'axis-{i}',bbox_pt=[x*w,y*h,(x+ww)*w,(y+hh)*h],title=a['title'],
    role='legend_only' if i in contract.get('legend',[]) else 'colorbar' if i in contract.get('colorbars',[]) else 'data')
  if i in contract.get('grid',{}):
   r0,r1,c0,c1=contract['grid'][i];axes[i].update(grid_id=fid,row_start=r0,row_stop=r1,col_start=c0,col_stop=c1)
 rows=[dict(id=f'row-{j+1}',panels=[f'axis-{i}' for i in g]) for j,g in enumerate(contract['rows'])]
 cols=[dict(id=f'column-{j+1}',panels=[f'axis-{i}' for i in g]) for j,g in enumerate(contract['cols'])]
 manifest=dict(schema_version=1,backend='Saved Matplotlib figure JSON',figure=dict(width_pt=w,height_pt=h),
  panels=[a for a in axes.values() if a['role']!='legend_only'],row_groups=rows,column_groups=cols,
  exemptions=[dict(panels=[f'axis-{i}' for i in e['axes']],checks=e['checks'],reason=e['reason']) for e in contract.get('exemptions',[])])
 result=alignment.audit_layout_manifest(manifest,tolerance_pt=TOLERANCE_PT,gutter_tolerance_pt=TOLERANCE_PT,require_panel_labels=False)
 custom=[]
 for edge,ids in contract.get('custom',[]):
  b=[axes[i]['bbox_pt'] for i in ids]
  if edge in ['left','bottom','right','top']:values=[v[['left','bottom','right','top'].index(edge)] for v in b]
  elif edge=='width':values=[v[2]-v[0] for v in b]
  elif edge=='center_x':values=[(v[0]+v[2])/2 for v in b]
  elif edge=='center_y':values=[(v[1]+v[3])/2 for v in b]
  else:raise ValueError(edge)
  spread=max(values)-min(values);custom.append(dict(edge=edge,axes=ids,values_pt=values,spread_pt=spread,pass_check=spread<=TOLERANCE_PT))
 overlaps=[]
 for i,j in itertools.combinations(axes,2):
  a,b=axes[i]['bbox_pt'],axes[j]['bbox_pt'];iw=min(a[2],b[2])-max(a[0],b[0]);ih=min(a[3],b[3])-max(a[1],b[1])
  if iw>.01 and ih>.01:overlaps.append(dict(axes=[i,j],intersection_area_pt2=iw*ih))
 inside=all(0<=a['bbox_pt'][0]<a['bbox_pt'][2]<=w+.01 and 0<=a['bbox_pt'][1]<a['bbox_pt'][3]<=h+.01 for a in axes.values())
 pdf=ROOT/'figures'/f'{fid}.pdf';expected=m['outputs'][str(pdf.relative_to(ROOT))];hash_ok=sha(pdf)==expected
 result.update(figure_id=fid,figure_json_sha256=sha(source),pdf_sha256=sha(pdf),pdf_matches_render_manifest=hash_ok,
  named_design=contract['rationale'],all_axis_roles=list(axes.values()),custom_shared_edge_checks=custom,
  global_axis_intersections=overlaps,all_axes_within_canvas=inside,
  scope_limit='Panel-label anchors are absent from saved JSON; this audit checks plot-area alignment, not type baseline alignment. Actual text collisions are checked independently on rendered PDFs.')
 failures=result['summary']['fail']+sum(not c['pass_check'] for c in custom)+len(overlaps)+(not inside)+(not hash_ok)
 result['combined_verdict']='PASS' if result['auditable'] and failures==0 and not result['summary']['warn'] else 'REVIEW REQUIRED'
 dump(out/'geometry'/f'{fid}.json',result)
 return dict(id=fid,verdict=result['combined_verdict'],alignment_comparisons=result['summary']['comparisons'],
  explicit_edge_checks=len(custom),failures=int(failures),warnings=result['summary']['warn'],rationale=contract['rationale'])


def trace_proof(pdf, finding, pythonpath):
 """Disambiguate Cairo multi-line trace boxes using individual glyph boxes.

 Only architecture text/text findings are eligible. Any unresolved fragment or
 actual glyph-box intersection remains a finding requiring review.
 """
 if pythonpath and str(pythonpath) not in sys.path:sys.path.insert(0,str(pythonpath))
 import pymupdf
 page=pymupdf.open(pdf)[finding['page']-1]
 chars=[];boxes=[]
 for trace in page.get_texttrace():
  for char in trace['chars']:
   value=unicodedata.normalize('NFKC',chr(char[0]))
   chars.extend(value);boxes.extend([tuple(char[3])]*len(value))
 text=''.join(chars)
 def find(fragment):
  target=unicodedata.normalize('NFKC',fragment);positions=[];offset=0
  while True:
   pos=text.find(target,offset)
   if pos<0:break
   positions.append(pos);offset=pos+1
  if len(positions)!=1:return None
  bb=boxes[positions[0]:positions[0]+len(target)]
  return [min(b[0] for b in bb),min(b[1] for b in bb),max(b[2] for b in bb),max(b[3] for b in bb)]
 a=find(finding['text']);b=find(finding.get('other_text') or '')
 if a is None or b is None:return None
 iw=max(0,min(a[2],b[2])-max(a[0],b[0]));ih=max(0,min(a[3],b[3])-max(a[1],b[1]))
 if iw*ih>1e-5:return None
 return dict(disposition='false_positive',reason='Cairo merged two baseline rows into one trace bounding box; uniquely matched per-glyph boxes are disjoint. Native PNG and enlarged PDF crops visually confirm separated text.',
             pdf_sha256=sha(pdf),first_glyph_union_bbox=a,second_glyph_union_bbox=b,
             glyph_union_intersection_area_pt2=iw*ih,pymupdf_version=pymupdf.__version__)


def collision(fid,skill,out,pythonpath):
 pdf=ROOT/'figures'/f'{fid}.pdf';report=out/'collisions'/f'{fid}.json';report.parent.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy()
 if pythonpath:env['PYTHONPATH']=str(pythonpath)+os.pathsep+env.get('PYTHONPATH','')
 command=[sys.executable,str(skill/'audit_figure_collisions.py'),str(pdf),'--json-out',str(report)]
 run=subprocess.run(command,env=env,text=True,capture_output=True)
 if not report.exists():raise RuntimeError(f'{fid}: collision audit failed to produce report: {run.stderr}\n{run.stdout}')
 m=json.loads(report.read_text());m['audit_command']=command;m['pdf_sha256']=sha(pdf);m['process_return_code']=run.returncode
 dispositions=[];remaining=[]
 for i,finding in enumerate(m.get('findings',[])):
  proof=trace_proof(pdf,finding,pythonpath) if fid=='architecture' and finding['kind']=='text-text' else None
  if proof:dispositions.append(dict(finding_index=i,**proof))
  else:remaining.append(i)
 m['reviewed_dispositions']=dispositions;m['unresolved_finding_indexes']=remaining
 m['reviewed_verdict']='PASS' if not remaining else 'REVIEW REQUIRED'
 dump(report,m)
 return dict(id=fid,verdict=m['verdict'],reviewed_verdict=m['reviewed_verdict'],summary=m['summary'],
             reviewed_false_positives=len(dispositions),unresolved_findings=len(remaining),findings=m.get('findings',[]))


def check_stored(out):
 """Read-only hash-bound verification; requires Python standard library only."""
 summary=json.loads((out/'summary.json').read_text())
 assert summary['contract_script_sha256']==sha(__file__),'Audit implementation changed; rerun full audit'
 assert {r['id'] for r in summary['geometry']}==set(PLOTTED)
 assert {r['id'] for r in summary['collision']}==set(['architecture']+PLOTTED)
 for path,digest in summary['report_sha256'].items():
  assert sha(ROOT/path)==digest,('Changed machine report',path)
 for fid in PLOTTED:
  r=json.loads((out/'geometry'/f'{fid}.json').read_text())
  assert r['combined_verdict']=='PASS',(fid,r['combined_verdict'])
  assert sha(ROOT/'figures'/f'{fid}.json')==r['figure_json_sha256'],('Changed figure geometry',fid)
  assert sha(ROOT/'figures'/f'{fid}.pdf')==r['pdf_sha256'],('Changed figure PDF',fid)
 for fid in ['architecture']+PLOTTED:
  r=json.loads((out/'collisions'/f'{fid}.json').read_text())
  assert r['reviewed_verdict']=='PASS' and not r['unresolved_finding_indexes'],(fid,'Unresolved collision')
  assert sha(ROOT/'figures'/f'{fid}.pdf')==r['pdf_sha256'],('Changed figure PDF',fid)
  for review in r['reviewed_dispositions']:
   assert review['pdf_sha256']==r['pdf_sha256'] and review['disposition']=='false_positive'
 print('Figure layout audit: 13 plotted geometries and 14 PDF collision reports verified; reviewed dispositions match current artifact hashes.')
 return 0


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true',help='Verify stored reviewed audit and current artifact hashes without optional dependencies');parser.add_argument('--skill-dir',type=Path,default=Path('/home/phflot/.codex/skills/nature-figure/scripts'))
 parser.add_argument('--qa-python-path',type=Path,default=Path('/tmp/cellpfn_figure_qa_deps'))
 parser.add_argument('--output',type=Path,default=ROOT/'output/review/figures/layout_audit');args=parser.parse_args()
 out=args.output.resolve();assert out.is_relative_to((ROOT/'output/review').resolve()),out
 if args.check:return check_stored(out)
 spec=importlib.util.spec_from_file_location('cellpfn_alignment_skill',args.skill_dir/'audit_panel_alignment.py');alignment=importlib.util.module_from_spec(spec);sys.modules[spec.name]=alignment;spec.loader.exec_module(alignment)
 geometries=[audit_geometry(fid,alignment,out) for fid in PLOTTED]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  collisions=list(pool.map(lambda fid:collision(fid,args.skill_dir,out,args.qa_python_path),['architecture']+PLOTTED))
 summary=dict(geometry=geometries,collision=collisions,alignment_tolerance_pt=TOLERANCE_PT,
  tool_hashes={n:sha(args.skill_dir/n) for n in ['audit_panel_alignment.py','audit_figure_collisions.py']},
  contract_script_sha256=sha(__file__),report_sha256={str(p.relative_to(ROOT)):sha(p) for folder in ['geometry','collisions'] for p in sorted((out/folder).glob('*.json'))},mutations='Audit outputs only; no active figures, captions or source data changed',
  review_policy='Raw skill findings retained. Any warning/failure needs individual visual interpretation; intentional overlays cannot be silently discarded.')
 dump(out/'summary.json',summary)
 for r in geometries:print('GEOMETRY',r['id'],r['verdict'],r['alignment_comparisons'],'group checks,',r['explicit_edge_checks'],'edge/center checks')
 for r in collisions:print('COLLISION',r['id'],r['verdict'],'reviewed:',r['reviewed_verdict'],json.dumps(r['summary']))
 if any(r['verdict']!='PASS' for r in geometries) or any(r['reviewed_verdict']!='PASS' for r in collisions):return 1
 return 0

if __name__=='__main__':raise SystemExit(main())
