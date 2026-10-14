# Source inventory

Every file in the legacy folder is indexed in `source_inventory.csv`. Substantive TeX, BibTeX and Markdown files are preserved under `input/legacy`; compiled PDFs and build artifacts are indexed but not duplicated.

The seed TeX, PDF and revision note are preserved under `input/seed`. The original seed is historical: its analytic-residual model is not the current experimental model.

The current export is an external, checksum-locked input. Its harmonized FIGURES.md and data tables, including the 2026-10-13 refresh, govern current findings. Builder sections and older project notes cannot override them.

Source hashes are checked by `make check`. Detailed passage-level reuse decisions are in `source_reuse.md`.

| Category | Files |
|---|---:|
| build_artifact | 32 |
| compiled_historical_manuscript | 5 |
| historical_manuscript | 5 |
| historical_note | 3 |
| unverified_bibliography | 3 |
| venue_template_or_template_output | 20 |

Total legacy files: 68. Export files recorded: 288.

Bibliographies in historical inputs are unverified leads. Only the active bibliography and literature verification notes define citations used in the new manuscript.
