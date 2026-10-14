#!/usr/bin/env python3
"""Compile in temporary storage and atomically publish the canonical manuscript.

The checked-in tables make PDF compilation independent of the original export.
Only a successful, fully resolved build replaces the existing manuscript PDF.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "output"
    review = output / "review"
    review.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cellpfn_pdf_") as directory:
        command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                   f"-outdir={directory}", "main.tex"]
        built = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        log_path = Path(directory) / "main.log"
        log = log_path.read_text(errors="replace") if log_path.exists() else built.stdout + built.stderr
        (review / "build.log").write_text("\n".join(line.rstrip() for line in log.splitlines()).rstrip() + "\n")
        if built.returncode:
            print((built.stdout + built.stderr)[-6000:])
            raise SystemExit("PDF compilation failed; canonical PDF preserved")
        unresolved = re.findall(r"(?:Citation|Reference) .+? undefined|There were undefined (?:references|citations)", log)
        if unresolved:
            raise SystemExit(f"Unresolved citations/references; canonical PDF preserved: {unresolved}")
        candidate = output / ".cellpfn.pdf.tmp"
        try:
            shutil.copyfile(Path(directory) / "main.pdf", candidate)
            os.replace(candidate, output / "cellpfn.pdf")
        finally:
            candidate.unlink(missing_ok=True)
    # These are known intermediate manuscript artifacts, not historical inputs.
    for old in (output / "cellpfn_wave1.pdf", ROOT / "build/main.pdf"):
        old.unlink(missing_ok=True)
    sources = [ROOT / "main.tex", ROOT / "references.bib", *sorted((ROOT / "sections").glob("*.tex")),
               *sorted((ROOT / "tables").glob("*.tex")), output / "cellpfn.pdf"]
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    manifest = {"source_files_and_pdf": hashes, "build": "make pdf", "checks": "make check",
                "word_count": "make words", "temporary_build_removed": True}
    (review / "build_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    warnings = [line for line in log.splitlines() if "Warning:" in line or "Overfull" in line]
    print("Built output/cellpfn.pdf; temporary build removed.")
    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    main()
