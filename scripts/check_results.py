#!/usr/bin/env python3
"""Read-only verification of manuscript registries against the original export.

No export is regenerated. This checks extraction/arithmetic, not experimental
validity, manuscript completeness, or the truth of externally cited numbers.
"""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def extract(fact):
    """Return an exported value and selection count from a declarative recipe."""
    source = (ROOT / fact["source"]).resolve()
    export = (ROOT.parent / "paper_export_20261011" / "data").resolve()
    if not source.is_relative_to(export):
        raise ValueError(f"local source outside the original export: {source}")
    filters = json.loads(fact["filter_json"])
    rows = [row for row in read_csv(source)
            if all(row[key] in ([str(v) for v in value] if isinstance(value, list)
                                else [str(value)]) for key, value in filters.items())]
    if len(rows) != int(fact["expected_rows"]):
        raise ValueError(f"selected {len(rows)} rows; expected {fact['expected_rows']}")
    op = fact["aggregation"]
    if not rows:
        raise ValueError("empty selection")
    if op == "count":
        return float(len(rows)), len(rows)
    if op in {"regex_integer", "regex_number"}:
        if len(rows) != 1:
            raise ValueError(f"{op} requires one source row")
        match = re.search(fact["argument"], rows[0][fact["value_column"]])
        if match is None:
            raise ValueError("declared number not found")
        return float(match.group(1).replace(",", "")) * float(fact.get("scale") or 1), 1
    values = [float(row[fact["value_column"]]) for row in rows]
    if op == "single":
        if len(values) != 1:
            raise ValueError("single requires one source row")
        result = values[0]
    elif op == "mean":
        result = math.fsum(values) / len(values)
    elif op == "min":
        result = min(values)
    elif op == "max":
        result = max(values)
    elif op == "ratio_columns":
        if len(rows) != 1:
            raise ValueError("ratio_columns requires one source row")
        result = values[0] / float(rows[0][fact["argument"]])
    elif op == "external_numerator_ratio":
        if len(rows) != 1:
            raise ValueError("external_numerator_ratio requires one source row")
        # Arithmetic only: the external numerator is NOT validated here.
        result = float(fact["argument"]) / values[0]
    else:
        raise ValueError(f"unknown aggregation: {op}")
    return result * float(fact.get("scale") or 1), len(rows)


def main():
    checked = external = unavailable = partial = 0
    failures = []
    ids = set()
    for registry in ("results.csv", "task_exposure.csv"):
        for fact in read_csv(ROOT / "evidence" / registry):
            identifier = fact["id"]
            if identifier in ids:
                failures.append(f"{identifier}: duplicate ID")
                continue
            ids.add(identifier)
            if fact["aggregation"] == "external_primary_source":
                external += 1
                print(f"EXTERNAL {identifier}: {fact['value']} {fact['unit']}; not locally verified")
                continue
            if fact["aggregation"] == "unavailable":
                unavailable += 1
                print(f"UNAVAILABLE {identifier}: no numerical pretraining claim")
                continue
            try:
                actual, _ = extract(fact)
                expected = float(fact["value"])
                if not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=0, abs_tol=1e-6):
                    raise ValueError(f"computed {actual:.12g}; registered {expected:.12g}")
                if fact["aggregation"] == "external_numerator_ratio":
                    partial += 1
                    print(f"ARITHMETIC ONLY {identifier}: external numerator not locally verified")
                checked += 1
            except (ValueError, KeyError, OSError, ZeroDivisionError) as exc:
                failures.append(f"{identifier}: {exc}")
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"Checked {checked} local extractions/calculations ({partial} externally dependent); "
          f"{external} external source, {unavailable} unavailable; {len(failures)} failures.")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
