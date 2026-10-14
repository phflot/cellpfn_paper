# CellPFN paper

Working manuscript for a Nature Biotechnology Article.

## Build and review

`make pdf` builds the review PDF at `output/cellpfn.pdf`.
`make check` checks the complete export index, source provenance, numerical claims and tables, citations, manuscript structure and the built PDF.
`make words` reports prose counts, including the narrative inside red claims.
`make index` regenerates the semantic index of every export file.
`make tables` regenerates Tables 1–2 and the supporting tables from their source selections.
`make figure` regenerates the editable architecture SVG and PDF/PNG exports using Python and Inkscape.

Requirements: Python3, NumPy/pandas for the supplied export reconciliation, a TeX installation with `latexmk`, `pdflatex`, `bibtex` and `detex`, and Poppler's `pdftotext`. Evidence regeneration/checks expect the original sibling `paper_export_20261011` and seed/legacy source directories. PDF compilation needs only this repository, generated tables and figure asset. Methods provenance checks also require the two source repositories at their recorded revisions; regenerating the figure requires Inkscape. The export's checker runs on a temporary copy because it writes its own reports. After edits, run `make pdf` before `make check`; the artifact check rejects a PDF that no longer matches its sources. Compilation uses temporary storage and replaces the canonical PDF only after a successful build with resolved citations and references.

The active manuscript is `main.tex` with modular sections and `references.bib`.
Historical inputs are preserved under `input/`; they are not alternative active drafts.
Working decisions, literature synthesis and the handoff are under `notes/`.

**Draft convention:** bold red text is an unresolved scientific claim, including claims that describe the intended final abstract. Its identifier links to `notes/open_claims.md`. Such text is not a confirmed result.

The manuscript now includes the abstract, introduction, quantitative Results, full Methods, one architecture figure, two main tables and a combined supplementary appendix. Supplementary Tables S1–S9 contain measured results; S10–S14 document simulator parameters, software capabilities, model dimensions, training and evaluation. Discussion and remaining figures are deferred. The editable architecture is `figures/architecture.svg`; its PDF is a figure asset, not an intermediate manuscript. See `notes/wave2_plan.md` for the approved implementation contract and `notes/reviews/` for the independent review of frozen Wave 1.

Start with [the review PDF](output/cellpfn.pdf), then [the complete export index](notes/export_index.md), [quantitative audit](notes/quantitative_review.md), [table provenance](notes/table_provenance.md), [handoff](notes/wave1_handoff.md), [open claims](notes/open_claims.md), [legacy story index](notes/source_reuse.md), and [literature synthesis](notes/literature_review.md). Mechanical checks establish internal consistency; source-specific literature verification and scientific limitations are recorded separately. Historical source PDFs under `input/` are preserved references; superseded current-manuscript PDFs and intermediate build PDFs are removed.
