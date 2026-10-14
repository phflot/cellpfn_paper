# CellPFN paper

Working manuscript for a Nature Biotechnology Article.

## Build and review

`make pdf` builds the review PDF at `output/cellpfn.pdf`.
`make check` checks the complete export index, source provenance, numerical claims and tables, citations, manuscript structure and the built PDF.
`make words` reports prose counts, including the narrative inside red claims.
`make index` regenerates the semantic index of every export file.
`make tables` regenerates Tables 1–2 and the supporting tables from their source selections.

Requirements: Python3, NumPy/pandas for the supplied export reconciliation, a TeX installation with `latexmk`, `pdflatex`, `bibtex` and `detex`, and Poppler's `pdftotext`. Evidence regeneration/checks expect the original sibling `paper_export_20261011` and seed/legacy source directories. PDF compilation needs only this repository and its generated tables. The export's checker runs on a temporary copy because it writes its own reports. After edits, run `make pdf` before `make check`; the artifact check rejects a PDF that no longer matches its sources. Compilation uses temporary storage and replaces the canonical PDF only after a successful build with resolved citations and references.

The active manuscript is `main.tex` with modular sections and `references.bib`.
Historical inputs are preserved under `input/`; they are not alternative active drafts.
Working decisions, literature synthesis and the handoff are under `notes/`.

**Draft convention:** bold red text is an unresolved scientific claim, including claims that describe the intended final abstract. Its identifier links to `notes/open_claims.md`. Such text is not a confirmed result.

Wave 1 covers the abstract, introduction, quantitative Results, two main tables and the supporting numerical appendix in the same PDF. Methods and figures will be developed in subsequent waves; Discussion is deferred. Numerical supporting tables belong to Wave 1 and do not wait for figure production.

Start with [the review PDF](output/cellpfn.pdf), then [the complete export index](notes/export_index.md), [quantitative audit](notes/quantitative_review.md), [table provenance](notes/table_provenance.md), [handoff](notes/wave1_handoff.md), [open claims](notes/open_claims.md), [legacy story index](notes/source_reuse.md), and [literature synthesis](notes/literature_review.md). Mechanical checks establish internal consistency; source-specific literature verification and scientific limitations are recorded separately. Historical source PDFs under `input/` are preserved references; superseded current-manuscript PDFs and intermediate build PDFs are removed.
