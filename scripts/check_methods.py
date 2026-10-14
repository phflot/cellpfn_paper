#!/usr/bin/env python3
"""Check Wave 2 provenance and contracts, not independent scientific validity."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT/'evidence/methods_source_manifest.json').read_text())
count = 0
for repo, record in manifest.items():
    path = ROOT.parent/repo
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip() == record['head']
    assert subprocess.check_output(['git','status','--porcelain'],cwd=path,text=True) == record['status'], f'{repo} status changed'
    for name, expected in record['hashes'].items():
        assert hashlib.sha256((path/name).read_bytes()).hexdigest() == expected, f'Source changed: {repo}/{name}'
        count += 1

required = ['methods_simulator','methods_model','methods_evaluation',
            'technical_simulator','technical_model','technical_evaluation']
for name in required:
    assert (ROOT/'sections'/f'{name}.tex').stat().st_size > 500, f'Missing substantive section: {name}'
tex='\n'.join(p.read_text() for folder in ['sections','tables'] for p in (ROOT/folder).glob('*.tex'))
assert not re.search(r'(?<![A-Za-z0-9_])v1(?![A-Za-z0-9_])|v2\.2-B', tex), 'Project version label remains in manuscript'
assert '\\label{fig:architecture}' in tex
for name in ['simulator-parameters','software-capabilities','model-architecture','training-recipe','evaluation-settings']:
    assert f'\\label{{tab:{name}}}' in tex, f'Missing technical table: {name}'

tree=ET.parse(ROOT/'figures/architecture.svg')
ns={'s':'http://www.w3.org/2000/svg'}
assert not tree.findall('.//s:image',ns), 'Editable schematic unexpectedly embeds a raster'
labels=tree.findall('.//s:text',ns)
assert len(labels)>40
assert min(float(t.attrib['font-size']) for t in labels)>=13
assert hashlib.sha256((ROOT/'figures/graphical_abstract_source.png').read_bytes()).hexdigest() == hashlib.sha256((ROOT.parent/'graphical_abstract.png').read_bytes()).hexdigest()
print(f'PASS: {count} source files unchanged; six Methods sections, five technical tables and editable Figure 1 contracts present.')
