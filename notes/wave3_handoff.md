# Wave 3 handoff

Completed 14 October 2026. The canonical manuscript is `output/cellpfn.pdf` (72 pages). It contains the abstract, introduction, quantitative Results, extensive Methods, Figures 1–3, both main tables, and the combined supplementary appendix with Figures S1–S9 and Tables S1–S14. S1 and S7 each have one genuine continuation page. Figure 4 remains reserved for new external validation. Discussion and submission materials remain deferred.

This completes the approved figure-production and integration work. It does not close the six outstanding scientific claims O01–O06 or establish submission readiness.

## Delivered evidence and figures

- Figure 1 retains the editable simulator/runtime/model architecture, including the two learning routes and gene–gene operator integration. Software capabilities remain distinct from measured speed.
- Figure 2 links biological performance to adaptation of pretrained tabular models. It preserves adverse adaptation outcomes, generic-task retention, exposure flags and training-task accounting.
- Figure 3 combines PBMC/cortex RNA maps, prediction errors, support expression/detection, query attribution, finite-deletion fidelity and deletion consequences. The manuscript distinguishes the 20,365 plotted cell–gene pairs (including 1,625 extra DS-LOO-selected pairs) from the original gene set used for matched fidelity summaries.
- Supplementary Figures S1–S9 cover calibration and one synthetic illustration; the full benchmark and harder subtypes; gene/input sensitivity; operator ablations and the failed prespecified criterion; prior/task-mixture controls; existing sex/age results; biological maps and marker overlays; explanation robustness; and bounded computational-cost observations.
- All 14 figure assets have PDF, editable SVG and PNG exports. The 13 plotted assets additionally bind 83 panel descriptions to 82 panel CSV selections with input/output hashes, population/filter definitions, aggregation, uncertainty and geometry. The schematic has source-code and build-hash provenance. See `notes/figures/inventory.md`.

## Biological data and remote work

Authorized SSH access to `rift_baest` succeeded through network escalation. Existing artifacts under `/share/runs/2026/30-03-phflot-hashprompt` were read only. All new remote derivatives were confined to the new `cellpfn_paper_figures` directory under that root.

Four exact frozen query populations are displayed: coarse PBMC (320 cells, 800 supports), fine PBMC (800 cells, 200 supports), development cortex (7,769 cells, 40 supports) and held-study cortex (7,163 cells, 40 supports). Cached labels, probabilities, observation identifiers, class order and gene order were reconciled with the reference checkpoint's case bundles. All queries remain visible. Attribution is available for the original correctly classified subsets of 191 PBMC and 96 development-cortex queries; unexplained queries remain distinct from zero-valued attribution.

Real RNA coordinates use the unlabelled support/query union, visualization-only variable genes, PCA and UMAP with recorded parameters. The same coordinates are reused across each case's overlays and never become classifier inputs. The synthetic illustration displays all 16,384 cells from one predetermined eight-donor/eight-type bank. Its anonymous genes and separate preprocessing/coordinates make it an illustration, not an additional real-data validation or simulator throughput benchmark.

Local biological derivatives, preparation receipts and hashes are archived in `figures/biological_data/`. Model training and fresh checkpoint inference were not performed.

## Attribution Methods: M01 resolved

The production attribution implementation, 52 original metadata JSONs, seven checkpoint-pinned modules and the case loader were recovered from Rift. The 52 metadata hashes match the original export. All seven pinned modules match the checkpoint's expected hashes; the package-level `episodes.py` was resolved independently of the historical loader's incorrect assumed path. The case loader is archived with its current hash and is explicitly not checkpoint-pinned.

Independent cached-array recomputation reproduces 24 corrected Spearman/relative-error metrics for 12 case/model combinations within export serialization precision (maximum absolute difference below 5e-7). The audit also reconciles 78 recorded gradient/noise diagnostics and 850 CPU algebra checks. These are cached-output/source checks, not a fresh attribution inference run.

Methods now gives the exact conditional pool updates, own-gene channel update, operator-scalar branch and final-head linearization, and specifies the omitted fixed-depth cross-gene whitening changes. It states what the first-order depth/detection correction does and does not restore. Recorded final-logit parity is approximate, with a maximum discrepancy of about 1.04e-3; bit-identical output or an analytical approximation bound is not asserted. Evidence and limits are in `notes/figures/attribution_code_audit.md` and `evidence/remote_attribution_validation.json`.

## Validation and review

The final PDF build resolves all citations and references without overfull boxes or oversized floats. All 14 commands in `make check` pass. Numerical, table, provenance, export, manuscript and figure checks cover the following:

- 337 local numerical extractions/calculations, 1,293 table selections and 350 displayed-precision ranking/color entries reconcile. External pretraining counts retain their separate verification states.
- The complete 288-file export index and 1,375 export reconciliation checks pass. All 359 original source hashes, 14 preserved copies and 1,380 source-code files remain unchanged.
- All 14 figure assets and their source-data bindings reconcile. The four frozen cell cohorts, predicted labels, balanced accuracies, attribution coverage and synthetic cell count are checked explicitly.
- The PDF matches 77 manuscript/figure sources. PyMuPDF checks effective text size after all PDF transforms: asset text is at least 6 pt, and the smallest embedded figure text is 5.053 pt. No figure text is clipped at its asset boundary. This avoids the false 1 pt report produced by reading the architecture's untransformed Cairo font size.
- Two independent figure cross-reviews found no blocking numerical selection error in the panels inspected. Their support/query wording, DS-LOO gene-set, balanced-accuracy and continuation-heading corrections were incorporated. Reports are under `notes/figures/cross_review_*.md`.
- The main figures and a contact sheet of all supplementary assets were visually inspected, along with full manuscript pages for Figure 3, S7 marker overlays and S8. The stronger collision audit prompted clearer exposure annotations, a separated trajectory legend and error-count labels outside the UMAP points. No underlying result or cell selection changed.
- All 13 plotted layouts pass 78 named-group and 20 explicit edge/center comparisons. All 14 PDF collision reports are reviewed and bound to current hashes. Nine architecture text-box warnings are retained as documented false positives: the corresponding uniquely matched glyph boxes do not intersect. The remaining rendered figures have no reported collisions. `scripts/audit_figure_layout.py --check` verifies the saved reports without optional skill-tool dependencies; a full refresh uses the installed Nature figure auditors.

The bibliography contains 58 entries and 55 cited works, with no missing or duplicate cited keys. Scanpy and UMAP references received targeted primary-source verification. The offline bibliography check does not independently validate each citation's support.

Word counts exclude editorial apparatus, captions, tables and code but include red narrative: abstract 143; introduction 472; Results 2,026; main text so far 2,498, leaving 502 words under the recorded 3,000-word working budget for Discussion. Methods 6,695; supplementary Methods prose 3,214. These are prose counts, not limits on the full technical appendix.

## Reproduction and remaining inputs

`make pdf` rebuilds the canonical manuscript from committed source and figure assets. `make figures` redraws from the local export and saved biological derivatives without SSH, model inference or UMAP regeneration. `make check` verifies evidence and the built PDF. Install `requirements-figures.txt` in the chosen Python environment; Inkscape, TeX and Poppler are also required for their respective build/check steps. The final QA run used Python 3.13.13, with PyMuPDF 1.28.2 loaded from a temporary dependency directory rather than changing the base environment: `PYTHONPATH=/tmp/cellpfn_figure_qa_deps make check`. Remote preparation uses the environment and raw-artifact paths recorded in the biological receipts. Full model/simulator runtime replication remains a separate exercise; historical Wave 2 runtime limitations have not been relabelled as passes.

The Figure 4 specification is `notes/figures/figure4_spec.md`. Required inputs are the species/cohort and transfer direction, ortholog policy for cross-species support-to-query transfer, frozen checkpoint/splits/comparators, corrected ROSMAP donor/label crosswalks and permitted export scope, and prespecified harder targets with suitable baselines. Independent biological uncertainty, new scientific results and controlled timing cannot be recovered by redrawing current exports.

Continue from this handoff and the canonical source. Earlier handoffs remain historical; their previously deferred figures and unresolved M01 status are superseded here. O01–O06 remain governed by `notes/open_claims.md`.
