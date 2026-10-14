# Wave 1 handoff — 14 October 2026

The NBT-oriented abstract, introduction and Results are drafted in `main.tex` / `sections/`, with a compiled review PDF at `output/cellpfn_wave1.pdf`. Methods, Discussion and figures are intentionally deferred. Provisional prose remains visibly bold red, including the destination claim in the abstract; completing the writing does not imply that the red scientific claims are established.

## Argument now in the draft

The simulator defines the cellular PFN prior. Its two demonstrations are compact CellPFN inference after limited training-task exposure and improvement of existing tabular models through cellular continued training. Transcriptome-scale input and efficient classifier explanations support the utility of this approach. Conventional LDA remains close at high support. The prespecified operator result, input-view differences, prior-version history, development selection and real-data-informed calibration are retained.

The prior family is shared; historical distributions differ: CellPFN used 320K v1 episodes followed by 64K v2.2-B, whereas tabular cellular adaptation used v2.2-B throughout plus generic replay. The approximately 90-fold comparison refers to 384K scheduled CellPFN episodes versus approximately 35M reported TabICLv2 datasets, not 12K reused banks or measured compute.

## Deliverables

- New independent Git repository using Philipp Flotho <PhilippFlotho@gmail.com>, single-line messages without co-author trailers.
- All 68 legacy files indexed; 11 substantive legacy sources and 3 seed files preserved, with immutable original paths and SHA256 hashes.
- Source reuse map focused on the author-marked donor-diversity, reference-fit, known-label and controlled-variation motivations.
- Three literature packages, 42 retained verified bibliographic records, 39 actively cited references, documented primary-source anchors and access limits.
- 57 numerical result records and 13 exposure records, with exact table selections and limitations.
- Five open claim IDs, a paragraph/evidence map, terminology contract, independent review notes and their resolution record.
- Reproducible build and local checks, with the original export checker isolated in a temporary copy.

## Verification

Commands: `make pdf`, `make check`, and `python3 scripts/count_words.py`.

- PDF builds without undefined citations or LaTeX warnings; title/abstract and representative red-result pages visually inspected.
- 66 local result/exposure extractions or calculations agree with exported tables; the ratio's external numerator is explicitly outside local verification. Three external model-exposure records and one unavailable count remain labelled as such.
- The supplied export reconciliation recomputed 1,375 checks with zero mismatches. This establishes internal numerical agreement, not independent experimental validity.
- 359 original source-file hashes and 14 preserved copies are unchanged.
- Bibliography audit: no duplicate keys/works, missing cited keys, missing required fields or blocking issues. Source-level evidence verification is documented in the literature notes; the offline audit does not resolve DOIs itself.
- Five actionable unresolved-claim IDs and zero factual TODO macros, with exact source/register agreement.
- Prose counts: abstract 138; introduction 488; Results 1,644; main text so far 2,132. This leaves 868 words under the current 3,000-word NBT Article limit for the later Discussion/adjustments. Red narrative is included, while marker IDs, comments and editorial apparatus are excluded; headings are included. The command and method are stored in `output/review/word_counts.json`.

## Next wave after the Methods discussion

Audit `hashprompt` and `pyscintelligentdesign` code against the exported run manifests and actual model endpoint. Resolve prior version/configuration provenance, bank reuse and task weighting, current neural-only predictions, gene transformations, support/query separation by task type, comparator classifier settings and model selection. Document the exact cohort releases/accessions and overlap, the corrected ROSMAP labels and interval construction, and DS-LOO's fixed-support target and approximation.

O01 covers independent frozen evaluation; O02 corrected neuropathology analysis; O03 disease-gene attribution and replication; O04 the abstract's aspirational synthesis; O05 controlled timing. Full closure criteria are in `open_claims.md`. The disease application is the largest unresolved component of the intended biological utility claim. The current draft does not demonstrate clinical use, universal superiority or training-seed reproducibility.

Wave 3 will produce figures after the textual evidence chain and Methods are settled. Existing export IDs remain evidence anchors rather than final figure numbering. Reconcile processed versus reconstructed cortex inputs before freezing the primary benchmark. Do not quietly substitute a different panel into the current gene-scaling or attribution result.
