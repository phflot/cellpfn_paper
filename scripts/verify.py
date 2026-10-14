#!/usr/bin/env python3
"""Run local reproducibility checks and persist their exact output."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
commands = [
    ["scripts/check_sources.py"],
    ["scripts/index_export.py", "--check"],
    ["scripts/check_results.py"],
    ["scripts/check_tables.py"],
    ["scripts/check_manuscript.py"],
    ["scripts/check_methods.py"],
    ["scripts/vendor/audit_bib.py", "--bib", "references.bib", "--tex", "main.tex", "--tex", "sections/*.tex", "--tex", "tables/*.tex"],
    ["scripts/count_words.py"],
    ["scripts/check_export.py"],
    ["scripts/check_sources.py"],
    ["scripts/check_artifacts.py"],
]
logs, records = [], []
for args in commands:
    done = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    log = "$ python3 " + " ".join(args) + "\n" + done.stdout + done.stderr
    logs.append(log)
    records.append({"command": ["python3", *args], "returncode": done.returncode})
    print(log)
out = ROOT / "output/review"
out.mkdir(parents=True, exist_ok=True)
(out / "validation.txt").write_text("\n".join(logs))
(out / "validation.json").write_text(json.dumps(records, indent=2) + "\n")
raise SystemExit(any(record["returncode"] for record in records))
