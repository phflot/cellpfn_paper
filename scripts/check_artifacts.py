#!/usr/bin/env python3
"""Check the delivered PDF's source identity, table numbering and artifact hygiene."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "output/review/build_manifest.json").read_text())
    expected_paths = {"main.tex", "references.bib", "output/cellpfn.pdf"}
    expected_paths.update({"figures/architecture.pdf", "figures/architecture.svg", "scripts/build_architecture.py"})
    expected_paths.update(str(p.relative_to(ROOT)) for folder in ("sections", "tables")
                          for p in (ROOT / folder).glob("*.tex"))
    hashes = manifest["source_files_and_pdf"]
    assert set(hashes) == expected_paths, "Build manifest omits or retains stale manuscript sources"
    for name, expected in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f"Rebuild required: {name} changed"
    assert set((ROOT / "output").glob("*.pdf")) == {ROOT / "output/cellpfn.pdf"}, "Multiple current manuscript PDFs"
    assert not list((ROOT / "build").rglob("*.pdf")), "Intermediate PDF remains in build/"
    assert not list((ROOT / "output").glob("*.tmp")), "Incomplete PDF promotion remains"
    read = subprocess.run(["pdftotext", "-layout", str(ROOT / "output/cellpfn.pdf"), "-"],
                          text=True, capture_output=True, check=True)
    text = read.stdout
    assert re.findall(r"Table (\d+):", text) == ["1", "2"], "Main Tables 1–2 missing or repeated"
    numbers = re.findall(r"Table S(\d+):", text)
    assert numbers == [str(n) for n in range(1, 15)], f"Supplement table numbering: {numbers}"
    assert re.findall(r"Figure (\d+):", text) == ["1"], "Expected exactly one architecture figure"
    assert "Simulator" in text or "simulator" in text
    assert "Supplementary Methods" in text
    assert "??" not in text, "Unresolved reference in PDF"
    print(f"PASS: canonical PDF matches {len(hashes)-1} manuscript sources; Figure 1, Tables 1–2 and S1–S14 present; no intermediate PDFs.")


if __name__ == "__main__":
    main()
