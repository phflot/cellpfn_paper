# Wave 1 independent review and resolution

Post-review synthesis, 14 October 2026. This document was not shown to the reviewers. The three reports were generated in separate fresh contexts from the same immutable packet at manuscript commit `2275642`. They did not read one another's reports or the evolving Wave 2 manuscript. Report hashes and packet hashes are recorded in `evidence/wave1_review_packet.json`; original reports remain unchanged.

## What the reviewers established

The reviewers found no incorrect headline average or newly demonstrated leakage in the inspected evidence. Reviewer 1 independently recalculated core means, all 192 S1 entries, paired gene/operator/task-mixture intervals, finer PBMC and sex summaries, exposure fractions and selected attribution values from export rows, rather than relying on the manuscript checker. This verifies correspondence to the export, not raw-data validity or independent experimental replication.

The important new omissions were biological label resolution, available finer cortical results, and the task-family intervention concealed by “learnable-only.” Other corrections concern HVG caps, comparator recipes, matched adaptation deltas and explanation/exposure semantics. These are resolved below using existing sources. There is no evidence that context-window size caused any particular omission.

Consensus limitations were development-conditioned evaluation (R2/R3) and the unavailable independent disease-signature evidence (all three). They remain open rather than being declared resolved by editorial revision. All reviewers classified these as nonblocking for the bounded descriptive computational contribution, while limiting stronger biological/generalization claims. Their assessments are author-facing guidance, not journal decisions.

## Disposition of every concern

| Concern | Resolution in the current manuscript | State |
|---|---|---|
| R1-M1, R2-M2, R3-M4 | O02–O04 remain visibly unresolved. Methods now names the provisional endpoints, donor matching and interval; sequencing-release/label reconciliation, actual disease attribution and independent replication remain required. The standing draft instruction preserves aspirational red prose. It must be narrowed or supported before submission. | Evidence pending; no promotion to fact |
| R2-M1, R3-M3 | Results identifies two biological collections with four panels; Table 1 explicitly states development selection. Methods distinguishes donor/study splits from an independent evaluation of model development. O01 remains open. | Reporting resolved; external validation pending |
| R3-M1 | Results and S5/S6 use “restricted task mixture.” Standard 80% metadata/15% type/5% identity is contrasted with 75% type/25% identity and excluded signed-covariance banks. S6 gives realized task counts and unequal cell exposure. Methods specifies the distribution and curriculum. | Resolved from existing evidence |
| R1-m2, R3-M2 | Main Results/Table 1 state 8/20 PBMC classes and four broad cortex compartments. S9 adds seven-label development cortex and three-label held-study neural tasks, their three-budget means and label definitions. Exploratory status and unavailable draw-level intervals remain explicit. | Resolved; new bindings X160–X165 |
| R1-m1 | Tables 1/2/S1/S3/S9 define HVG labels as requested caps. Methods gives actual primary one-shot widths and support-only eligibility rules. | Resolved; width bindings X166–X169 |
| R1-m3 | S2 states that paired adaptation deltas use a released checkpoint rescored in the same run, whereas Table 1 uses stored benchmark values. | Resolved without changing values |
| R1-m4 | Table 1 stars explicitly mark query-source overlap. Support-source overlap is separate; unflagged scores do not certify absence of exposure. Gray/overall-best/unflagged-best formatting and displayed-precision ties are preserved. | Resolved |
| R2-m1 | Evaluation Methods gives cohort/accession, donor or proxy units, fixed query sizes, split studies and support-only transformations; S14 supplies comparator settings. PBMC levels reuse donors/cells and cortex panels share support data, as the described construction makes explicit. | Resolved reporting; identity limits retained |
| R2-m2 | S1 and Methods state the scANVI 400+10-epoch recipe, batch128, training fraction0.9 and no label resampling. Fine-PBMC one-shot trains on18/20 cells and omits at least two classes from optimization. SingleR classic/default mode is explicit; scGPT sensitivity remains linked to S9. | Resolved; no retuned scores substituted |
| R2-m3 | Operator equation and S4 note give the exact zero one-shot gate and distinguish trained-arm contrasts from fixed-weight inference interventions. | Resolved |
| R3-m1 | Methods and S8 explain margin sign, the inability of zero-deletion to assess absent-gene information, and LYZ margin versus class-logit ranks. | Resolved |
| R3-m2 | S8 states24 explained cortex immune cells and source-reported recall approximately0.17, explicitly not independently reanalysed. | Resolved with source boundary |
| R3-m3 | Results notes evaluation at20 and35 classes despite a training maximum of8. Methods gives2/4/6/8 class sampling. No unseen-cell-type discovery claim is made. | Resolved |
| R3-m4 | S8 adds full-model IG64 margin Spearman for all six cases, using the same exported exact-deletion target and evaluated-gene set. No universal superiority or interchangeability of attribution objectives is inferred. | Resolved |

## Independent Wave 2 technical checks

Separate model and simulator inspections checked the new prose against executable source and the evaluated source pins. Their reports are `wave2_model_check.md` and `wave2_simulator_check.md`. Resolved corrections include affine support-attention notation, constant-support denominator safeguards, the globally floored standard deviation in neural features, strict admission threshold, ECE bin indexing, age-dependent effective gamma shapes, preservation of log-state expectation, per-cell zero-count QC, and the operator's classifier-scalar path in Figure 1.

M01 records a distinct unresolved reproducibility gap found during Methods reconstruction: the complete production DS-LOO code/corrections are unavailable. A fixed covariance fit still allows query-side cross-gene dependencies, so its handling must be recovered together with normalization/detection corrections. The documented approximation and measured fidelity rows do not replace that implementation audit. No allegation that the existing fidelity measurements are wrong is inferred from missing code.

## Review boundary and next evidence

The frozen reports identified seven major concerns and eleven minor comments across three reviews. Repeated concerns were reconciled only after all reports were frozen. Most new reporting issues were answerable from existing files. Independent cohorts/training replication, corrected neuropathology and disease/sex attribution, controlled attribution timing and matched simulator throughput remain new-evidence tasks. The simulator benchmark specification is in `notes/simulator_scalability_protocol.md`; no performance experiment was run in this wave.

The literature reviewer made targeted primary-source checks of donor diversity, cellular PFN precedents, marker associations and the atlas citation, and found no confirmed reference error. This was not a fresh systematic review of every citation. Mechanical bibliography checks and source-specific verification remain distinct.
