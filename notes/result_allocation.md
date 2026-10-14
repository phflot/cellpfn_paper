# Results sequence and allocation

This allocation follows the author's integrated framing: the simulator defines a PFN prior, with two demonstrations of value—CellPFN trained from scratch at limited task exposure and continued training of existing tabular models. Wave 1 writes abstract, introduction and Results. Methods auditing, final figure construction and Discussion remain separate work. Export figure IDs below identify evidence blocks; they do not fix final figure numbering.

| Narrative unit | Evidence and role | Main text | Supporting/deferred material |
|---|---|---|---|
| Procedural cellular tasks define the prior | Export fig1 fact sheet, lineage and architecture modules | Explain what is sampled, gene anonymity with within-task correspondence, support-conditioned frozen inference and the current neural-only model | Detailed hierarchy, prior versions, task mixtures, model modules and exposure accounting go to Methods/SI; no inherited legacy equations |
| Competitive biological inference at limited task exposure | Export fig4 and fig2; R01–R12, T01–T07 | Bounded benchmark comparison, approximately 90-fold lower episode exposure than published TabICLv2 training, support/dataset dependence and compact model | Full classical-reference matrix, classifier-setting sensitivity, exposure audit and all task cells; final external evaluation remains unresolved |
| Transcriptome-scale inference | Export fig2; R02–R05, R13–R19 | View contrast and extrapolation beyond training gene widths; retain the 8,192-HVG result and vendor-setting qualifications | Random-gene controls, later checkpoint trajectories, full draw distributions, stored-zero audit and reconstructed-count sensitivity |
| The prior improves existing tabular learners | Export fig3; R20–R27, T08–T10 | One-shot gains, little high-support change and qualified Kumo-small generic-table control | Milestones, task-draw replicates, generic-table performance loss, input projections, full replay/control accounting |
| Statistical and task-design boundaries | Export fig6 and supp_prior_ablation/supp_taskmix_tradeoff | One compact paragraph preserving the failed preregistered operator outcome, regime dependence and calibration tradeoff | Full operator decomposition, proxy ablations, hard-class post-hoc analyses, uncertainty-resolution limits and simulator realism audit (fig7) |
| Efficient query-gene attribution | Export fig5; R28–R37 | Fidelity, query-side scope, measured/extrapolated cost distinction and contextual marker example | Full deletion curves, sign controls, random-gene validation, gradient comparisons and stability; omit estimated Kumo speedup headline |
| Disease application candidate | supp_rosmap; R38–R40 | Complete provisional prose in bold red if included; do not make it confirmed evidence in abstract or introduction | Corrected-label analysis, external replication and disease gene panel are future work; no invented experiments or unexported sensitive data |

## Evidence precedence

1. Harmonized `paper_export_20261011/FIGURES.md`, its `data/` CSVs and `DATA_DICTIONARY.md` govern current experimental facts. Apply the final-pass corrections and the October 13 operator refresh. The lineage fact sheet overrides shorthand `trained_on` descriptions that can misleadingly name only the last prior version.
2. `CHECKS.md` and `CHANGELOG.md` establish the numerical reconciliation; `STATUS.md` establishes readiness and open choices. Their checks establish internal agreement, not independent validation of scientific claims. Server paths are provenance, not required filesystem dependencies.
3. `hashprompt` reports and narrowly targeted implementation reads resolve exposure units and current model contracts. For example `iterative_improvement/manuscript_briefing/METHODS_AND_PROVENANCE.md` and `src/hashprompt/foundation_dataset_reuse.py` explain reused banks and episode-specific task views. A full Methods code audit remains Wave 2.
4. Earlier export builder documents under `sections/` yield to harmonized documents. Seed manuscript and old reference texts provide story elements and citation leads only. Primary literature is reopened and verified before factual literature claims enter the manuscript.

## Stale material to replace

The seed `CellPFN_NBT_model_methods_revised.tex` describes a different hybrid model: a fixed empirical-Bayes/prototype prediction plus a bounded learned residual, a 100K-task training campaign and a different parameter count. The current export explicitly says analytic logits/probabilities are not used; its current direct neural endpoint and exposure are R01/T01–T05. Preserve the motivation of learning support-conditioned inference, but remove the analytic-expert residual as the current contribution. Do not imply that planned derangement, residual-only or summary-replacement controls were completed.

The earlier hypothetical broad applicability map and prospective external evaluation remain aspirations. Keep unresolved full prose bold red rather than replacing it with fabricated outcomes. Confirmed numerical values elsewhere must still carry their local limits: one training seed, three shared benchmark draws, differing gene views, model selection on development panels and prior calibration on real-data summaries.

## Defaults and open decisions

- Use G1v2′ at the exported endpoint to connect scaling, benchmarking and DS-LOO. GL1/GS1 are explicit continuation ablations rather than an undocumented replacement model.
- Use the processed Zebra view for the current coherent Wave 1 narrative and describe reconstructed-count sensitivity separately, unless the author selects the latter as primary. Gene-view and DS-LOO results cannot silently migrate to another input panel. The final frozen evaluation is unresolved.
- Make quantitative comparison of training exposure against the verified TabICLv2 paper; leave unverified comparator counts unavailable. No wall-clock claim follows from task exposure.
- ROSMAP numerical prose remains bold red pending corrected labels. A complete aspirational abstract may include bold-red unresolved generality/application claims, but not imaginary numerical outcomes.
- Use supplied intervals only. A three-draw range is descriptive; neither query-cell pseudoreplication nor treating different result-table cells as training replicates is permitted.
- Build final figures in Wave 3. The present allocation tracks evidence ownership and captions' scientific obligations without producing new panels or analyses.
