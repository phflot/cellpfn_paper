# Wave 1 numerical evidence and wording

The simulator is the PFN prior. Lead with CellPFN's competitive real-cell inference after limited training-task exposure, then demonstrate that the prior also improves released tabular models. Full-transcriptome operation and faithful attribution show capabilities of the cellular architecture. Avoid a universal leaderboard claim.

`evidence/results.csv` records 49 numerical facts; `evidence/task_exposure.csv` records exposure quantities and unavailable comparator counts. Each local entry gives its source, exact string-valued filters, aggregation, selected-row count, units and limitations. Values retain precision for checking; prose should round. `python scripts/check_results.py` reads the original sibling export without changing it. It verifies extraction and arithmetic, not scientific validity or that every numeral in manuscript prose is registered. Its external-source and externally dependent outputs remain explicitly distinct.

## Model and exposure

- **R01; T01–T05:** the reference G1v2′ endpoint has 12,329,889 trainable parameters, 384,000 scheduled episodes from 12,000 simulated banks and 276,828 loss-bearing episodes, at 96,000 update opportunities. Each bank supplies 32 views. Do not call the bank count the training-task count or call the episode views independent biological datasets.
- **T06–T07:** TabICLv2 reports approximately 35 million synthetic training datasets in its primary article, section 4.1. Against 384,000 scheduled CellPFN episodes this is approximately 91-fold greater task exposure, or about 90-fold fewer for CellPFN. The article was opened and read on 2026-10-14; the local check cannot verify its claim. This is a descriptive cross-paper exposure comparison, not matched-compute or causal training-efficiency evidence.
- **T08–T10:** current continued training adds 40,000 cellular tasks and 10,000 generic replay tasks over 2,500 updates. The released pretraining is additional. Do not describe 40,000 as total lifetime training or omit replay when accounting for exposure.
- **T11–T12:** exact Kumo and TabPFN-3.5 pretraining-task counts are unverified here. TabPFN-v2 numbers and the old Google TabFM campaign must not substitute for them.

## Comparable performance with a compact cellular model

**R02–R07:** across the four core panel definitions and three support budgets, using the same three support draws, CellPFN's all-gene balanced accuracy is 72.9%, against 66.8% for released TabICLv2, 70.1% for released Kumo large and 72.4% for continued-trained Kumo large, each on 2,000 highly variable genes. Geneformer-LR and scGPT-LR yield 74.9% and 69.4% using their native input routes. The aggregate is an equal-weight descriptive average of distinct tasks, not an independent replicate set. Models use different gene views and preprocessing; family variants were selected on these panels.

**R08–R12:** the useful regime qualification is essential. On PBMC fine cell types with one support cell per class, Geneformer-LR yields 68.8% versus CellPFN's 51.1%. On the cortex query from held-out studies with ten supports per class, CellPFN yields 91.9% versus 87.4% for Geneformer-LR and 87.2% for scGPT-LR. These are three-draw descriptive means. Both cellular foundation models likely encountered the exact PBMC cells during unlabeled pretraining; Geneformer also encountered studies contributing most cortex OOD queries. Exposure is not evidence of label leakage or its causal effect. scGPT's unstandardized logistic classifier matters: do not treat this as a clean ranking of embedding architectures.

The term “competitive” describes this bounded regime map. “Matches” cannot imply statistical equivalence, and “limited training-task exposure” cannot imply lower measured compute. Stronger broad claims remain bold red until the planned final evaluation resolves them.

## Full-transcriptome operation

**R13, R14, R02:** CellPFN moves from 71.2% with 2,000 HVGs to 73.8% with 8,192 HVGs and 72.9% with all genes. Thus all genes improve over 2,000 HVGs, while 8,192 HVGs give the highest aggregate in this comparison. Benefits are not uniform across tasks. Use the three-draw series throughout cross-model contrasts; do not silently replace CellPFN with its different twenty-draw means.

**R03–R05, R15–R18:** released TabICLv2 drops from 66.8% to 48.3%, Kumo large from 70.1% to 66.4%, and continued-trained Kumo large from 72.4% to 70.4% when given all genes. Continued-trained TabICLv2 yields 55.4% with all genes. These reflect vendor default inference configurations, including model-specific column handling and ensembling, not inability in principle to process additional genes.

**R19:** TabPFN-3.5 refuses all 36 all-gene benchmark cases under its default feature guard. Neither overriding the guard nor removing support-constant columns was tested. State its non-commercial research usage wherever its results are included.

**R41–R45:** training tasks contain at most 8,192 genes; all-gene inference uses 33,538 for PBMC and 21,158 for processed Zebra. Reconstructed-count Zebra contains 12,325; the kidney panel contains 4,096. Thus the first three widths extrapolate beyond training, whereas kidney does not. Keep “full transcriptome” tied to the delivered dataset's measured coordinates, not every gene in the organism.

## Transferable value of the prior

**R20–R22:** after 40,000 added cellular tasks plus replay, one-shot gains average +7.3, +10.8 and +5.6 percentage points for TabICLv2, Kumo small and Kumo large, respectively, across the four core panels. **R23–R25:** the corresponding changes at 100 supports per class are +0.77, −0.22 and +0.26 points, supporting “little change” rather than a formal equivalence result.

**R26–R27:** the Kumo-small generic-table control changes the average over the eight low-support panel/budget cells by −0.05 points, versus +6.05 points for cellular continued training. This is an eight-cell low-support contrast; do not label these the one-shot-only changes above. The control has different rows and columns per update. It supports content specificity with qualifications, not a fully matched causal attribution. Comparable generic-table-only controls do not exist for the other two architectures. Task-draw replicates share the model seed.

## Architecture-enabled attribution

**R28–R31:** DS-LOO's case summaries of within-cell ranking agreement span 0.979–0.998 across six cases and two models. These are medians over cells and classes, not a minimum guaranteed correlation for every cell. Corrected magnitude errors for G1v2′ span 0.5–4.9%. Validation uses correctly classified cells, query-only knockouts and fp32; it does not cover the entire benchmark, low-margin failures or the benchmark's bf16 mode.

**R32–R35:** the load-matched timing comparison is 10.4–12.9 exact-single-gene-forward equivalents. PBMC DS-LOO took 67.9 seconds; an exhaustive exact pass over all genes is extrapolated as 61.0 hours from individual forward timings. The latter was not run. Shared-GPU timing remains provisional; Kumo knockout timings are estimates and are excluded from the headline.

**R36–R37:** IL7R ranks second for CD4 T cells and NKG7 seventh for NK cells in the specified PBMC class-margin ranking. These are contextual model explanations relative to runner-up classes; gene names are attached after anonymous inference. They are not perturbation predictions, causal mechanisms, expression direction or a biological validation experiment. DS-LOO follows query-side pooled gene statistics and also works without the covariance operator.

**R46–R49:** deleting each cell's top 50 DS-LOO-ranked genes reduces the mean original-runner-up margin by 5.66 logits, compared with 0.14 for random expressed genes. The original-runner-up margin crosses below zero in 45.0% versus 0.3% of explanations, respectively. The stored column is named `frac_calls_flipped`, but its definition is this original pairwise margin reversal; do not reword it as a benchmark balanced-accuracy change or a complete multiclass argmax-call-flip rate. This is the specified PBMC case and correctly classified explained cells only.

## Provisional application and honest boundaries

**R38–R40:** the exported pooled, sex-matched ROSMAP microglial CERAD contrast reports donor AUC 0.745 with the supplied corrected repeated-split interval [0.700, 0.790]. It remains NOT FINAL pending donor-label corrections. A sentence using this result must be bold red, including its numerical outcome and clinical interpretation, and cannot be presented as confirmatory generalization. Only aggregates already in the export are used here.

Do not conceal the operator's preregistered NOT SUPPORTED outcome behind later descriptive benefits. The variance-only ablation partitions some effects, but each arm has one training run. The learnable-only task stream trades accuracy against calibration and changes cells per update. Simulator realism is mixed and was assessed against calibration datasets, not independent real validation. These limitations qualify the supported story without requiring every diagnostic table in the main Results.

## Audited qualitative source anchors

The following anchors are exact `key` values in `../paper_export_20261011/data/fig1__facts.csv`; each row carries its original source file/line and status. The matching prose is in `FIGURES.md`, fact sheet beginning at line 167. These establish what the current export supports without importing the stale seed's mechanism descriptions.

| Intended prose | Exact source keys | Boundary |
|---|---|---|
| A hierarchy of studies, donors, cell types and cells; related cell classes | `sim.hierarchy`, `sim.class_tree`, `sim.bank_shape` | The simulator generates a larger donor universe than the training bank uses. Do not imply every generated donor enters each task. |
| Distributed class effects, rare-marker/multimodal classes, covariance-distinguished classes | `sim.lanes`, `sim.lane_meaning`, `sim.class_markers`, `sim.class_energy` | The covariance lane has equal means by construction. These are modelled capability families, not validated regulatory networks. |
| Within-type heterogeneity, donor-dependent state-program usage and hidden subtypes | `sim.programs` | This key is explicitly FROM_REPORT rather than an independent code audit. Avoid adding new trajectory or pathway claims from the old seed. |
| Study/batch shifts vary depth and expression; donors vary cell-type composition | `sim.study_effects`, `sim.composition_code` | `sim.no_gene_absence` says structural panel absence is not simulated. Do not claim support for missing-panel gene matching or arbitrary study-specific detection. |
| Mean-dependent gamma–Poisson observation noise | `sim.count_model`, `sim.dispersion` | Observation dropout is switched off in the trained prior. Zeros arise through count sampling; do not describe an added zero-inflation/dropout module as trained here. |
| Task-local gene alignment with changing anonymous panels; cell classes have local labels | `episode.gene_anonymity`, `episode.no_persistent_gene_ids`; `FIGURES.md:173–180` | Anonymity does not solve orthology or unaligned feature panels. Support and query columns must correspond. |
| Support/query separation depends on the target | `episode.split.cell_type_tasks`, `episode.split.metadata_tasks`, `episode.split.donor_identity_tasks` | Cell-type and metadata tasks separate donors; donor-identity tasks deliberately share donors but use disjoint cells. Do not inherit the old seed's universal donor-and-study-disjoint claim. |
| Shared same-gene relation functions followed by invariant pooling and a small head | `arch.support_stats`, `arch.support_router`, `arch.relation_mlp`, `arch.gene_pooling`, `arch.head` | The query trunk mixes genes through pooled summaries; the covariance operator has its own cross-gene dependency. Avoid saying no part of the architecture ever mixes genes. |
| Frozen neural inference without an analytic-logit base or query-query interaction | `model_contract.output`, `model_contract.analytic_logits_or_probabilities_used`, `model_contract.query_inference`, `arch.queries_independent` | The output is unbounded direct logits. Remove “bounded residual on empirical Bayes” and “learned analytic correction” from descriptions of the current model. |
| Support-conditioned covariance features | `operator.support_fitted_parameter_free`, `operator.contract.gene_channel`, `operator.entry_gene_channel`, `operator.gate_formula` | The support covariance fit is analytic and detached; learned consumers use its features. This is not an analytic classifier whose logits are added to the model output. The operator is off with one support cell per class. |
| Evidence for the operator is conditional | `operator.verdict_preregistered`; `FIGURES.md:1323–1346`, `1579–1611` | The failed preregistered test remains reported; subsequent three-arm results and expanded support-draw analyses do not reverse it. |
| Synthetic-only parameter training with real-informed development | `training.simulated_only.statement`, `training.simulated_only.design_choices_caveat`, `sim.real_data_role`, `sim.real_data_leak_caveat` | Real aggregate calibration and development-panel inspection occurred. Do not write “no real data used” or “fully independent validation”. |
| Checkpoint policy and research selection are different | `training.checkpoint_selection`, `training.selection_policy`; `FIGURES.md:971–1004` | Latest sealed milestones were used under the later policy, but earlier design choices and best-family presentation used real-panel results. Neither policy erases that history. |
| One model-training seed | `training.replicate_seeds`; `FIGURES.md:40–56` | Support draws and task-draw replicates do not measure model-training variance. No claim of training-seed reproducibility follows from their intervals. |
| Simulator utility is not uniform realism | `sim.known_misses`, `sim.age_signal`; `FIGURES.md:1635–1720` | Age effects are effectively null in the trained prior, and other statistics miss real regimes. Use the transfer results to support utility; keep comprehensive realism and age/disease mechanism claims bold red if aspirational. |

The deletion metric definition is independently anchored in `FIGURES.md:1149–1160` and its caveat at `FIGURES.md:1294`, in addition to the registry's precise CSV selections. Dimensionality comes from the panel glossary and the training-width fact, not assumptions about raw source matrices. No new experiment, p value, or confidence interval was produced in this audit.
