#!/usr/bin/env python3
"""Run the supplied mutating export checker on a temporary copy only."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "paper_export_20261011"
with tempfile.TemporaryDirectory(prefix="cellpfn_export_check_") as temp:
    target = Path(temp) / "export"
    shutil.copytree(SOURCE, target)
    done = subprocess.run([sys.executable, str(target / "build/assemble/check_all.py")], cwd=target, text=True, capture_output=True)
    print(done.stdout, end="")
    print(done.stderr, end="", file=sys.stderr)
    if done.returncode:
        raise SystemExit(done.returncode)
    report = ROOT / "output/review/export_checks.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("<!-- Recomputed from a temporary copy; original export unchanged. Internal reconciliation only. -->\n" + (target / "CHECKS.md").read_text())
