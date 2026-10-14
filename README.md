# CellPFN paper

Working manuscript for a Nature Biotechnology Article.

## Build and review

`make pdf` builds the review PDF at `output/cellpfn.pdf`.
`make check` checks the complete export index, source provenance, numerical claims and tables, citations, manuscript structure, figure/source-data bindings and the built PDF, including figure text at its embedded size.
`make words` reports prose counts, including the narrative inside red claims.
`make index` regenerates the semantic index of every export file.
`make tables` regenerates Tables 1–2 and the supporting tables from their source selections.
`make figure` regenerates the editable architecture SVG and PDF/PNG exports using Python and Inkscape.
`make figures` redraws the complete figure package from verified local inputs; it does not connect to Rift or rerun models or UMAPs.

Requirements: Python3 with `requirements-figures.txt`, a TeX installation with `latexmk`, `pdflatex`, `bibtex` and `detex`, Poppler's `pdftotext`, and Inkscape for the architecture redraw. Evidence checks and quantitative redraws expect the original sibling `paper_export_20261011`; original-source checks also require the seed/legacy directories and two source repositories at their recorded revisions. PDF compilation needs only this repository and its generated assets. Real-cell coordinates, cached predictions and display gene values are archived locally with provenance receipts, so figure redraws require neither raw RNA access nor pretrained checkpoints. Preparing new RNA coordinates needs the recorded Rift data/environment; fresh inference is a separate operation. The export's checker runs on a temporary copy because it writes its own reports. After edits, run `make pdf` before `make check`; the artifact check rejects a PDF that no longer matches its sources. Compilation uses temporary storage and replaces the canonical PDF only after a successful build with resolved citations and references.

The active manuscript is `main.tex` with modular sections and `references.bib`.
Historical inputs are preserved under `input/`; they are not alternative active drafts.
Working decisions, literature synthesis and the handoff are under `notes/`.

**Draft convention:** bold red text is an unresolved scientific claim, including claims that describe the intended final abstract. Its identifier links to `notes/open_claims.md`. Such text is not a confirmed result.

The manuscript includes the abstract, introduction, quantitative Results, full Methods, Figures1–3, both main tables and a combined supplementary appendix with FiguresS1–S9 and TablesS1–S14. S1 and S7 each span two figure assets/pages. Figure4 is reserved for new external validation; Discussion and submission materials remain deferred. Editable SVGs, PDF/PNG exports, per-panel CSVs and figure manifests are under `figures/`. These PDFs are figure assets, not alternative manuscript drafts. The package is described in [the figure inventory](notes/figures/inventory.md), [the execution contract](notes/wave3_plan.md) and [the reserved Figure4 specification](notes/figures/figure4_spec.md).

Start with [the review PDF](output/cellpfn.pdf), then [the current handoff](notes/wave3_handoff.md), [the complete export index](notes/export_index.md), [quantitative audit](notes/quantitative_review.md), [table provenance](notes/table_provenance.md), [independent review resolutions](notes/reviews/wave1_synthesis.md), [open claims](notes/open_claims.md), [legacy story index](notes/source_reuse.md), and [literature synthesis](notes/literature_review.md). Mechanical checks establish internal consistency; source-specific literature verification and scientific limitations are recorded separately. Attribution implementation provenance has been recovered and cached fidelity summaries independently reconstructed; this does not establish fresh checkpoint inference. Historical handoffs and source PDFs remain provenance. There is one current manuscript PDF.
