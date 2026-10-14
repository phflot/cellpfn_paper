#!/usr/bin/env python3
"""Check that indexed original sources and preserved snapshots did not change."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checked = copies = 0
    for name in ("notes/source_inventory.csv", "notes/seed_manifest.csv", "evidence/export_manifest.csv"):
        with (ROOT / name).open(newline="") as handle:
            for row in csv.DictReader(handle):
                path = ROOT.parent / row["source"]
                if digest(path) != row["sha256"]:
                    raise SystemExit(f"Source changed since snapshot: {path}")
                checked += 1
                if row.get("archived"):
                    archive = ROOT / row["archived"]
                    if digest(archive) != row["sha256"]:
                        raise SystemExit(f"Snapshot differs: {archive}")
                    copies += 1
    print(f"PASS: {checked} original source hashes and {copies} preserved copies unchanged.")


if __name__ == "__main__":
    main()
