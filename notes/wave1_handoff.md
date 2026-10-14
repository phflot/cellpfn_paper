# Wave 1 handoff — 14 October 2026

The NBT-oriented abstract, introduction and quantitative Results are complete for this drafting wave in `main.tex` and `sections/`. The canonical review manuscript is the 27-page `output/cellpfn.pdf`, containing Tables 1 and 2 and Supplementary Tables S1–S9. Methods, Discussion and figures remain later work. Six unresolved scientific claims remain visibly bold red; completing Wave 1 does not establish those claims or make the manuscript submission-ready.

## Argument and evidence

The simulator defines the cellular PFN prior. Its two demonstrations are competitive biological inference by compact CellPFN after limited training-task exposure and improvement of existing tabular models through cellular continued training. Transcriptome-scale inputs and efficient classifier explanations support the utility of this approach. Conventional LDA remains strong at high support. The Results retain adverse transfer effects, the failed prespecified operator test, unsuccessful prior candidates, predictive-log-loss costs and mixed simulator realism.

The prior family is shared; historical distributions differ. CellPFN used 320K v1 episodes followed by 64K v2.2-B, whereas tabular cellular adaptation used v2.2-B throughout plus generic replay. The approximately 90-fold exposure comparison uses 384K scheduled CellPFN episodes versus approximately 35M reported TabICLv2 datasets. It does not use the 12K reused banks as the task denominator and does not establish a measured compute advantage.

Table 1 gives the PBMC and ZEBRA task/budget model comparisons. Table 2 gives the 2k-HVG, 8,192-HVG and all-gene ablation. They occupy two main display slots, leaving four for Wave 3. S1–S9 preserve detailed comparisons, training exposure and retention, scaling, operator and prior ablations, task-mixture costs, realism, gene attribution, and exploratory or provisional analyses. Table flags distinguish pretraining-exposure evidence; their scope must not be inflated into verified target-label leakage or exact-cell identity. Flagged values are gray; both the overall best and best unflagged result are bold, including all ties at displayed precision.

The additions requested during revision are included:

- Matched coarse/fine PBMC results and eight post hoc harder subtype tasks, with their separate support-draw counts and lack of draw-level intervals made explicit.
- Original GSM-disjoint ZEBRA sex classification and later XY-eligible/broader task results. Later evaluation units include age-by-sex sample groups and are not uniformly verified individual donors.
- Actual top-ranked genes and selected known cell-type markers for PBMC and ZEBRA. These are classifier explanations and selected marker matches, not an enrichment test or causal validation.
- DS-LOO described as one attribution sweep with head-gradient evaluations and depth/detection corrections, rather than literally one forward pass.
- O06 explicitly records the missing sex-gene attribution. XIST/Y-linked genes define task eligibility in the supplied results; they are not measured attribution hits.

## Evidence package

- The independent Git repository uses Philipp Flotho <PhilippFlotho@gmail.com>, single-line commit messages and no co-author trailers.
- All 68 legacy files are indexed; 11 substantive legacy sources and three seed files are preserved with immutable source paths and SHA256 hashes. The reuse map records the author-marked donor-diversity, reference-fit, known-label and controlled-variation motivations.
- All 288 refreshed export files have a semantic index, including 142 CSVs, 115 data tables and 677,812 data rows. `notes/export_index.md`, `notes/export_disposition.md` and `evidence/export_index.json` record authority, purpose, schemas, replication units and manuscript destinations.
- The evidence ledgers contain 159 R records, 159 X records and 13 T records. The generated tables bind 1,268 numerical selections to source rows in `evidence/table_values.csv`.
- The bibliography contains 48 retained records, of which 45 are actively cited. Baseline-method and cell-type marker references have primary-source verification notes in `notes/literature/`; `notes/geneformer_exposure_audit.md` distinguishes the evaluated Geneformer-V2 model and source-study overlap from verified exact-cell identity.
- `notes/open_claims.md`, `notes/paragraph_map.md`, `notes/result_allocation.md` and the review-resolution notes record the remaining evidence boundaries and section ownership.

## Verification and build

Use `make tables`, `make pdf`, `make check` and `make words`. The build uses temporary storage, verifies source and PDF hashes, and leaves one active PDF with no version/revision suffix. Historical source PDFs remain provenance; the former intermediate manuscript PDF is removed. The review package in `output/review/` records the authoritative current build and counts.

- All 327 local numerical extractions/calculations pass. One ratio depends on an externally sourced numerator; three external exposure counts and one unavailable count remain explicitly distinguished from local verification.
- All 1,268 numerical table selections agree with their recorded sources; 350 ranking/color entries pass the independent displayed-value formatting check.
- The supplied export reconciliation recomputes 1,375 checks with zero mismatches. This establishes internal numerical consistency, not independent experimental validity.
- All 359 original source hashes and 14 preserved copies are unchanged.
- The bibliography audit has no blocking issues, duplicate works/keys or missing cited keys. Offline checks do not themselves verify DOI metadata or scientific support.
- Manuscript checks require all six open-claim IDs, no unregistered factual TODOs, consistent table references and a canonical artifact matching its source manifest.
- The integrated PDF was visually inspected, including the landscape comparison, operator ablation, gene-attribution and subtype/sex tables. Table layout and final pagination are checked after rendering changes.

At final Wave 1 build, the counting script reported 143 abstract words, 472 introduction words and 1,963 Results words: 2,435 main-text words and 565 words reserved under the current 3,000-word NBT Article limit. Red narrative is included; marker IDs, comments, tables and editorial apparatus are excluded. `output/review/word_counts.json` governs if subsequent corrections change these counts.

## Next waves

Wave 2 will audit `hashprompt` and `pyscintelligentdesign` against exported run manifests and the actual model endpoint. Resolve prior configuration provenance, bank reuse and task weighting, neural-only predictions, gene transformations, support/query separation by task type, comparator settings and model selection. Document cohort releases/accessions, pretraining overlap evidence, the corrected ROSMAP labels, interval construction and DS-LOO's fixed-support target and approximation.

O01 covers independent frozen evaluation; O02 corrected neuropathology analysis; O03 disease-gene attribution and replication; O04 the abstract's aspirational synthesis; O05 controlled timing; O06 sex-gene attribution. Closure rules are in `open_claims.md`. The current draft does not demonstrate clinical utility, universal superiority or training-seed reproducibility.

Wave 3 will produce figures after the evidence chain and Methods are settled. Existing export IDs remain source anchors rather than final figure numbers. Reconcile processed versus reconstructed cortex inputs before freezing the primary benchmark; do not substitute a different panel into the current scaling or attribution result without updating the corresponding claims and source records.
