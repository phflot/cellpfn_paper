#!/usr/bin/env python3
"""Check the delivered PDF's source identity, table numbering and artifact hygiene."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from figure_catalog import manuscript_inputs

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "output/review/build_manifest.json").read_text())
    expected_paths = {str(p.relative_to(ROOT)) for p in manuscript_inputs()} | {"output/cellpfn.pdf"}
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
    assert re.findall(r"Figure (\d+):", text) == ["1","2","3"], "Expected current Figures 1–3; Figure 4 remains reserved"
    assert re.findall(r"Figure S(\d+):", text) == [str(n) for n in range(1,10)], "Supplementary figures S1–S9 missing or duplicated"
    assert "Simulator" in text or "simulator" in text
    assert "Supplementary Methods" in text
    assert "??" not in text, "Unresolved reference in PDF"
    print(f"PASS: canonical PDF matches {len(hashes)-1} manuscript sources; Figures 1–3/S1–S9, Tables 1–2 and S1–S14 present; no intermediate PDFs.")


if __name__ == "__main__":
    main()
