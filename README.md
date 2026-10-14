# CellPFN paper

Working manuscript for a Nature Biotechnology Article.

## Build and review

`make pdf` builds the review PDF at `output/cellpfn_wave1.pdf`.
`make check` checks source provenance, numerical evidence, citations and manuscript structure.
`make words` reports prose counts, including the narrative inside red claims.

Requirements: Python3, NumPy/pandas for the supplied export reconciliation, and a TeX installation with `latexmk`, `pdflatex`, `bibtex` and `detex`. Evidence checks expect the original sibling `paper_export_20261011` and seed/legacy source directories. PDF compilation needs only this repository. The export's checker runs on a temporary copy because it writes its own reports.

The active manuscript is `main.tex` with modular sections and `references.bib`.
Historical inputs are preserved under `input/`; they are not alternative active drafts.
Working decisions, literature synthesis and the handoff are under `notes/`.

**Draft convention:** bold red text is an unresolved scientific claim, including claims that describe the intended final abstract. Its identifier links to `notes/open_claims.md`. Such text is not a confirmed result.

Wave 1 covers the abstract, introduction and Results. Methods and figures will be developed in subsequent waves; Discussion is deferred.

Start with [the review PDF](output/cellpfn_wave1.pdf), then [the handoff](notes/wave1_handoff.md), [open claims](notes/open_claims.md), [legacy story index](notes/source_reuse.md), and [literature synthesis](notes/literature_review.md). Mechanical checks establish internal consistency; source-specific literature verification and scientific limitations are recorded separately.
