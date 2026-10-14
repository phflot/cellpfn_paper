#!/usr/bin/env python3
"""Count prose with the skill's detex-based helper, retaining red claim prose.

Only the claim-ID apparatus is removed from two-argument unresolvedclaim macros.
The unchanged skill helper strips editorial markers/comments/floats, then detex.
"""
import json
import re
import tempfile
from pathlib import Path
from vendor.prose_wordcount import prose, DEFAULT_MARKERS, DEFAULT_FLOATS

ROOT = Path(__file__).resolve().parents[1]


def group(text, start):
    if text[start] != "{":
        raise ValueError("expected opening brace")
    i, depth = start + 1, 1
    while i < len(text) and depth:
        if text[i] == "\\":
            i += 2
            continue
        depth += (text[i] == "{") - (text[i] == "}")
        i += 1
    if depth:
        raise ValueError("unbalanced macro argument")
    return text[start + 1:i - 1], i


def unwrap_claims(text):
    out, cursor = [], 0
    for match in re.finditer(r"\\unresolvedclaim\s*(?=\{)", text):
        if match.start() < cursor:
            raise ValueError("nested claim marker")
        out.append(text[cursor:match.start()])
        _, end = group(text, match.end())
        while text[end].isspace():
            end += 1
        narrative, cursor = group(text, end)
        out.append(narrative)
    out.append(text[cursor:])
    return "".join(out)


def counts():
    result = {}
    with tempfile.TemporaryDirectory(prefix="cellpfn_wordcount_") as temp:
        for name in ("abstract", "introduction", "results"):
            source = (ROOT / "sections" / f"{name}.tex").read_text()
            path = Path(temp) / f"{name}.tex"
            path.write_text(unwrap_claims(source))
            result[name] = prose(path, DEFAULT_MARKERS, DEFAULT_FLOATS, False, False)
    result["main_text_so_far"] = result["introduction"] + result["results"]
    result["remaining_of_3000"] = 3000 - result["main_text_so_far"]
    return result


if __name__ == "__main__":
    result = counts()
    for name, n in result.items():
        print(f"{name}: {n}")
    destination = ROOT / "output/review/word_counts.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({"command": "python3 scripts/count_words.py", "method": "Brace-unwrapped claim narrative; skill prose_wordcount.py with detex -n; headings included; IDs, editorial apparatus, comments and floats excluded", **result}, indent=2) + "\n")
    if result["abstract"] > 150 or result["remaining_of_3000"] < 0:
        raise SystemExit("NBT working word limit exceeded")
