# Evaluation Methods evidence audit

Audited 2026-10-14. Authored `sections/methods_evaluation.tex` and `sections/technical_evaluation.tex`; no source repositories, exports, shared manuscript sources or bibliography were modified. This is a source audit, not a rerun of biological analyses. Existing draft numbers remain governed by the harmonized export.

## Evidence precedence and inspected source

1. Current `paper_export_20261011/FIGURES.md`, `DATA_DICTIONARY.md`, `data/fig4__panels.csv`, `glossary__panels.csv`, `fig4__methods.csv`, `fig4__best_per_family.csv`, `glossary__metrics.csv`, `supp_exposure__*`, `supp_prior_ablation__hard_tier_*`, `fig5__*` and `supp_rosmap__*` govern current cases and recorded outputs. Builder dictionary/section detail is used only where consistent with the harmonized account.
2. `hashprompt/experiments/run_practical_reference.py::_pbmc_cases` (lines 1070 onward), `iterative_improvement/manuscript_briefing/PBMC_CITESEQ_PROTOCOL_20260922.md` and the associated results record define original PBMC RNA accessions, metadata audit, doublet exclusion, donor split, eligible-class quotas, SHA256 query rankings and nested donor-round-robin supports.
3. `hashprompt/src/hashprompt/tabular_foundation_references.py::select_support_hvg` and `build_support_views` define Seurat dispersion over support rows, twenty mean bins, anonymous-column tie breaking, support normalization/clipping and PCA dimensionality. `hashprompt/src/hashprompt/practical_references.py::fit_logistic_reference`, `fit_score_celltypist` and `annotation_probability_logits` define classifier fitting and probability handling.
4. `hashprompt/experiments/run_tabular_foundation_worker.py::build_estimator` and `fit_predict` define package-default inference with fixed checkpoint paths, probability checks and query-by-query canaries. `run_kumo_tabular_worker.py` describes official checkpoint revision 1.0.0, ensemble sizes, default recipe, float32 weights, float16 CUDA autocast and frozen state-dict overrides. These support concrete inference descriptions; they do not supply all missing run-specific environment receipts.
5. `hashprompt/efast/hard_spec.py`, `hard_cases.py` and `hard_select.py` define exploratory subtype candidates, parent-label grouping, identical donor quotas, draw counts, pinned atlas hashes and reference-based task selection. **Selection is not wholly prediction-free:** it evaluates NCM/LR references on query labels. It excludes CellPFN/proxy outputs. Earlier notes' broad phrase “no model outputs” should be narrowed accordingly.
6. `hashprompt/src/hashprompt/evaluation_metrics.py::fixed_bin_ece` and `classification_metrics_from_logits` resolve a dictionary omission: ECE uses fifteen fixed-width left-closed confidence bins, final bin right-inclusive; NLL clips true-label probabilities at 1e-12. The scorer requires all declared classes in query data.
7. `hashprompt/iterative_improvement/manuscript_briefing/ZEBRA_RECONSTRUCTED_COUNTS_20260921.md` and its runner preserve the conditional count-reconstruction rule, availability masking, failed Yang Cortex cells and changed supports. Old checkpoint result rows in this document were not substituted for the current export.
8. `notes/attribution_extension.md`, `notes/geneformer_exposure_audit.md` and the matching export rows provide already-audited finer PBMC tasks, sex unit definitions and model/source-study exposure limits.

The generic `hashprompt/experiments/reference_benchmark.py` random cell split is **not** the manuscript donor/study split and is not inherited into these Methods. Older scANVI recipes in the reconstructed-count note also do not replace the current comparator recipe.

## Section-to-source map

| Manuscript component | Primary support | Boundary |
|---|---|---|
| PBMC source and split | GEO identifiers in PBMC protocol; `_pbmc_cases`; export panel glossary | Joint RNA/ADT labels, RNA-only prediction; eligibility excludes rare/poorly represented classes |
| Cortex panels | `glossary__panels` rows `zebra_dev`, `zebra_ood`; hard-case source hashes | “Held-out study” does not imply independent final model selection; exact support-donor count not supplied |
| Kidney context | `fig4__panels`; panel glossary | Existing 4,096-gene panels used a larger historical support pool; cell and donor metrics distinct |
| HVG/PCA | `select_support_hvg`, `build_support_views` | Labelled support data only; values are not silently recomputed with query statistics |
| Cortex sensitivity | Reconstruction note and current stored-zero export | Inferred integer lattice, changed genes and some supports; not raw-count retrieval or pure representation intervention |
| Comparators | `fig4__methods`; worker entrypoints; practical references | Official model versions permitted; no own-project version history in narrative |
| Model choice | `fig4__best_per_family` | Kumo best 2k-HVG mean; CellPFN explicit state selection; no assertion that every representative obeyed one best-score rule |
| Subtypes | `hard_spec`, `hard_select`; hard-tier task and CellPFN mean tables | Post hoc, reference-performance selection; no invented individual CellPFN predictions/intervals |
| Sex tasks | Three panel-glossary rows; `attribution_extension` | GSM != donor; some later units are age-by-sex sample groups; X/Y eligibility != recovered attribution |
| Metrics | `evaluation_metrics.py`; glossary | Support-draw intervals conditional on cohorts; single model seed |
| DS-LOO | Harmonized fig5 account; knockout dictionary; exact-pair and case tables | Target and first-order pooling math supported; correction implementation absent (M01) |
| ROSMAP | Panel glossary; donor-AUC metric row; aggregate AUC and issue tables | O02 unresolved labels, sequencing-release crosswalk and input mode; no new controlled data accessed |

## Unresolved reporting and citation needs

- **M01 requested for root registration:** production DS-LOO code and exact normalization/detected-fraction correction are absent from the local tree and available history. The export names server-side `gene_importance_20261008/PROTOTYPE.md`, `ARCHITECTURE.md`, `code/run_case.py` and aggregation code, but none was available for direct implementation audit. The mathematical definition and pool-only first-order expansion are explanatory derivations consistent with the supplied account, not recovered complete production pseudocode. The added Methods sentence is bold red with M01; root must add the ID and closure rule.
- **O02 reused:** exact ROSMAP sequencing accessions/release crosswalk, corrected labels, donor identity reconciliation and input mode are not recoverable from aggregate exports. Reported donor sampling and corrected repeated-split interval are existing provisional protocol records, not newly verified participant-level facts.
- **O06 reused:** no sex-gene attribution exists in supplied fig5 tables. The eligibility gene list is not a finding of model relevance.
- **Existing O01/O05 remain:** model selection used development panels and one model seed; controlled timing remains outstanding. No extra independent evaluation or timing experiment was performed.
- Root independently verified and added the original **McEvoy et al. kidney study associated with GSE202109** (`mcevoy2022kidney`) and **Nadeau--Bengio corrected repeated-split inference** (`nadeau2003inference`); these are now cited. The exact reported correction formula is grounded in the exported protocol, not asserted to have been independently rederived from the statistical paper. Existing keys also cover CITE-seq, ZEBRA, Geneformer, scGPT, tabular models, CellTypist, SingleR, scANVI, integrated gradients and ROSMAP context.
- Source-study names in ZEBRA are identifiers from the atlas record; their complete accession-level release crosswalk and model checkpoint/environment receipts should accompany the final reproducibility package. Do not substitute inferred publication years for unidentified release versions.
- The LDA export states rank/variant and input view, but does not fully identify solver, shrinkage floor and run code for all rows. The Methods table reports only documented settings. Full classical solver recipes remain an author/run-record completion item.
- Geneformer revision and weight SHA256, scGPT weight SHA256 and environment package strings are in `fig4__methods.csv`; this audit did not re-download or instantiate the checkpoints. Current Methods do not claim such execution.

## Integration checks for root

- Include the main evaluation file inside Methods, and the technical file after the existing numerical supplementary material under technical Methods. The comparator table label is `tab:evaluation-settings`; avoid renumbering numerical tables by hand.
- Add M01 to `notes/open_claims.md`, with closure requiring recovery of source code, correction equations, run/checkpoint bindings and reproduction on the exported exact-deletion fixtures.
- Existing bib keys in new files: `hao2021multimodal`, `flotho2024zebra`, `mcevoy2022kidney`, `qu2026tabiclv2`, `jaeger2026tabpfn35`, `nvidia2026kumo`, `priorlabs2026tabpfn35card`, `chen2026geneformer`, `cui2024scgpt`, `dominguezconde2022celltypist`, `aran2019singler`, `xu2021scanvi`, `bennett2018rosmap`, `sundararajan2017ig`, `nadeau2003inference`.
- Check the number of main-text words separately from Methods and technical material. Run normal compile/reference checks after root integrates the files; no new model tests are needed for prose-only changes.
