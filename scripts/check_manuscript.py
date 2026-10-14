#!/usr/bin/env python3
"""Local structural checks; not a scientific-validity or citation-source audit."""
import re
from pathlib import Path
from count_words import unwrap_claims, counts

ROOT = Path(__file__).resolve().parents[1]
sources = [(ROOT / "sections" / f"{n}.tex").read_text() for n in ("abstract", "introduction", "results")]
for text in sources:
    unwrap_claims(text)  # raises on truncated nested argument
ids = re.findall(r"\\unresolvedclaim\{([^}]+)\}", "\n".join(sources))
registered = re.findall(r"^\| (O\d+) \|", (ROOT / "notes/open_claims.md").read_text(), re.M)
assert len(ids) == len(set(ids)), "Duplicate claim ID"
assert set(ids) == set(registered), f"Claim/register mismatch: {set(ids)^set(registered)}"
assert not re.search(r"\\cite\w*\{", sources[0]), "Abstract must be unreferenced"
assert not re.search(r"\\section", sources[1]), "Introduction must have no heading"
assert not re.search(r"CITATION NEEDED|PLACEHOLDER_|\\cite\{\s*\}", "\n".join(sources)), "Unresolved citation placeholder"
assert "\\textbf{#2}" in (ROOT / "main.tex").read_text(), "Claim marker must retain bold prose"
manuscript = "\n".join(p.read_text() for p in [ROOT / "main.tex", *sorted((ROOT / "sections").glob("*.tex")), *sorted((ROOT / "tables").glob("*.tex"))])
labels = re.findall(r"\\label\{([^}]+)\}", manuscript)
references = re.findall(r"\\(?:ref|pageref)\{([^}]+)\}", manuscript)
assert len(labels) == len(set(labels)), "Duplicate table label"
assert set(references).issubset(labels), f"Missing table labels: {set(references)-set(labels)}"
assert {"table:overview", "table:gene_ablation", *(f"tab:s{i}" for i in range(1, 10))}.issubset(labels), "Quantitative tables missing"
word_counts = counts()
assert word_counts["abstract"] <= 150, "Abstract exceeds150 words"
assert word_counts["remaining_of_3000"] >= 0, "Main text exceeds3000 words"
todos = re.findall(r"\\TODO\{([^}]*)\}", "\n".join(sources))
print(f"PASS: {len(ids)} actionable claim IDs, {sum(bool(t.strip()) for t in todos)} factual TODOs, no citation placeholders.")
print("Word counts:", word_counts)
