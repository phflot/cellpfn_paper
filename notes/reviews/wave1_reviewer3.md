# Reviewer 3

Frozen independent Wave 1 report, 14 October 2026.

## Review setup

- **Input scope** Frozen commit 2275642 in `/tmp/cellpfn_wave1_review_20261014`, covering the abstract, introduction, Results, two main tables and Tables S1-S9. Assigned emphasis was biological interpretation, literature support, legacy motivation and important omitted evidence.
- **Assessment boundary** Methods and figures were deliberately deferred. Requests below that concern protocol detail are requirements for that planned material, not allegations that its absence was overlooked. This is a source-to-claim review, not an independent experiment, raw-data audit or experimental replication. No models were run and no new biological analyses were performed.
- **Independence** Only the frozen packet, its legacy inputs and the original current export were consulted. No other reviewer report, synthesis or live manuscript was read. No subagents were used.
- **Shared manuscript claim summary** A compact, gene-anonymous PFN trained on synthetic cellular tasks achieves competitive descriptive classification performance with limited labelled support, and the same prior improves some released tabular models. Query-only gene deletion provides faithful explanations of selected model decisions. The neuropathology extension remains provisional.
- **Visible evidence base** The current numerical authority was `/home/phflot/projects/ccb/hashprompt/paper/paper_export_20261011`. Public literature checks used titles, DOIs, author names and identifiers only as outbound queries. No unpublished text was sent to external services.
- **Missing materials affecting confidence** There is no frozen independent external evaluation, no finalized disease-label audit or disease-gene result, and no sex-gene attribution. Those absences are already disclosed. Raw donor linkage and independent biological validation cannot be inferred from aggregate exports.

Pointers below use `P` for the immutable packet root and `E` for the current export root given above. Line numbers refer to those files, not the live draft. CSV selectors identify the exact records where more useful than physical line numbers.

## Overall assessment

The defensible contribution is a method for support-conditioned classification, with evidence that a procedurally generated cellular task distribution can train a useful inference rule and adapt existing tabular learners. The introduction now has a coherent biological motivation and treats existing simulators and foundation models fairly. The present data do not yet establish a biological discovery or broadly independent generalization. Much of this distinction is already stated well.

Two substantive omissions remain within the completed Wave 1 material. The term “learnable-only” hides a large change in biological prediction targets, and the cortical evaluation is presented mostly at four broad compartments despite available finer-label results. These can be corrected largely from existing sources. I found no confirmed numerical or citation error in the targeted checks described below.

**Who would be interested in the results, and why** Single-cell atlas builders would be interested in prediction from scarce reference labels without a fixed gene vocabulary. Computational biologists and tabular-learning researchers would be interested in a biological prior that transfers across model families. The gene-deletion route is useful to researchers inspecting context-dependent classifier decisions, provided it is not interpreted as perturbation biology.

**Major strengths**

- The motivation distinguishes the number of measured cells from independent biological diversity. This preserves the strongest point in the author-written legacy introduction, `P/input/legacy/pyScIntelligentDesign/scIntDesign.tex` lines 143-145, while avoiding its unsupported general claims about simulator scale and fidelity.
- `P/sections/introduction.tex` lines 8-11 acknowledges meta-learning, tabular PFNs, cellular perturbation PFNs, statistical and mechanistic simulators, learned generators and simulator-evaluation literature. There is no unsupported first-biological-PFN claim.
- The manuscript explicitly reports negative and mixed outcomes, including poor one-shot PBMC subtype performance, the broad sex task near chance, failed operator and prior-screen criteria, and higher-support log-loss deterioration.
- DS-LOO is described as approximate query-only finite deletion, with fixed support, selected correctly classified cells and fp32 validation. The manuscript correctly rejects a literal one-forward-pass or biological-knockout interpretation.

## Major Concerns

### R3-M1

- **Issue key** task_family_change_hidden_by_filtering_name
- **Severity** Major
- **Blocking** No
- **Axis** mechanism-evidence
- **Status** Missed substantive reporting detail. The unequal cell exposure is already disclosed, but the change in prediction targets is not.
- **Claim pointer** `P/sections/results.tex` lines 52-55 describes “learnable-task filtering” and “learnable-task continuation” as the retained intervention. `P/tables/s5.tex` line 10 calls it “Learnable-only tasks”; `P/tables/s6.tex` lines 23-33 reports the cell-count difference without defining the changed task mixture.
- **Evidence pointer** `E/FIGURES.md` lines 139-142 and 1449-1459. The standard continuation contains approximately 80% donor-metadata tasks, 15% cell-type tasks and 5% donor-identity tasks. The alternative contains approximately 75% cell-type tasks and 25% donor-identity tasks and excludes the signed-covariance lane. The realized 16,000-task counts are 12,816 metadata, 2,398 cell-type and 786 donor-identity tasks for GS1, versus 12,001 cell-type and 3,999 donor-identity tasks for GL1. Machine-readable sources are `E/data/fig1__training_stream.csv` and `E/data/fig6__taskmix_stream_composition.csv`.
- **Concern** This is a substantial retargeting of training toward the evaluated cell-type problem, alongside removal of one signal family. A reader cannot assess why accuracy or log loss changes when the intervention is described primarily as filtering. The restriction also matters biologically because improved cell typing does not establish improved donor-metadata inference. The caveat about 1.67 times as many cells addresses a different confound.
- **Why it matters** Task-distribution design is a central scientific contribution. Its interpretation changes materially when most metadata prediction is replaced with cell typing and donor recognition.
- **Resolution test** Define both task mixtures and the excluded lane in one Results sentence and a compact Table S6 entry. Carry the exact sampling rules into Methods. Describe the observed gain as a consequence of this combined task-mixture intervention; retain the exposure caveat and do not isolate learnability as its cause. No new experiment is required to make the present result interpretable.

### R3-M2

- **Issue key** cortical_label_resolution_and_omitted_finer_readouts
- **Severity** Major
- **Blocking** No
- **Axis** claim-moderation
- **Status** Missed source-supported biological scope and results, not evidence that the reported broad-label numbers are wrong.
- **Claim pointer** `P/sections/results.tex` lines 15-24 calls the tasks cortex annotation and highlights 91.9% balanced accuracy on held-out cortex. `P/tables/overview.tex` labels these simply ZEBRA development and held-study. `P/tables/s9.tex` lines 43-63 supplies PBMC subtype results, but no corresponding finer cortical reference-checkpoint results.
- **Evidence pointer** `E/data/glossary__panels.csv`, rows `panel_id=zebra_dev` and `zebra_ood`, defines four broad classes, Glia, Immune cell, Neural and Vascular cell. `E/data/supp_prior_ablation__hard_tier_tasks.csv` lines 10-11 defines the three-label held-study neural task and seven-label development task. `E/data/supp_prior_ablation__hard_tier_cellpfn_values.csv`, `model_id=cellpfn_g1v2p`, `checkpoint_update=96000`, `gene_view=hvg8192`, `scope_kind=task`, records development seven-label balanced accuracies of 67.75, 76.32 and 79.33% and held-study neural balanced accuracies of 52.46, 62.14 and 69.60% at 1, 10 and 100 supports, respectively. The relevant physical lines are 16-17, 48-49 and 80-81.
- **Concern** The headline cortical score measures broad compartment separation, not resolution of neuronal subtypes. The difference is particularly consequential for biological readers because all neurons form one class in the core task. The existing finer cortical evidence is informative in both directions and should accompany the PBMC subtype boundary. This is not a controlled comparison of difficulty because the labels and evaluated cells change, as the source itself states.
- **Why it matters** Label resolution determines what biological utility has been demonstrated. Omitting the available cortical extension makes the scope harder to assess and loses a useful explanation of the high broad-label performance.
- **Resolution test** State the four cortical compartments in Results and main-table annotations. Add the two source-defined cortical tasks to the exploratory supplementary table, with their full label definitions, gene view and summary-only uncertainty limitation. Keep them distinct from the eight PBMC tasks and from the primary benchmark; do not infer a numerical “difficulty penalty” from the cross-task differences. Methods should also report the published PBMC annotation provenance, donor filtering and the distinction between same-atlas study transfer and independent-cohort validation.

### R3-M3

- **Issue key** outer_generalization_remains_development_conditioned
- **Severity** Major
- **Blocking** No
- **Axis** experimental-design
- **Status** Already disclosed limitation, O01. It is not newly discovered leakage or a negative measured result.
- **Claim pointer** `P/sections/abstract.tex` line 1 and `P/sections/results.tex` lines 12-24 present competitive biological inference. Results line 4 discloses real-data calibration and line 24 discloses model selection on the panels. `P/tables/overview.tex` line 35 marks foundation-model exposure.
- **Evidence pointer** `E/FIGURES.md` lines 46, 49-51 and 304-306 states that the evaluation panels informed prior ranges and design decisions. `E/data/glossary__panels.csv`, rows `pbmc_l1`, `pbmc_l2`, `zebra_dev` and `zebra_ood`, shows that four panels comprise two annotation levels of the same PBMC collection and two study splits of the same cortex atlas. `P/sections/results.tex` line 58 and `P/tables/s7.tex` line 31 correctly identify the realism reference as calibration rather than independent validation.
- **Concern** The four-panel average supports a descriptive development result. It does not estimate transfer to previously unused cohorts, and query-study separation alone does not make the whole model-development process external. The pretraining-overlap audit appropriately qualifies Geneformer and scGPT, but does not make CellPFN an independently validated comparator.
- **Why it matters** Generalization across biological experiments is the primary motivation. The limitation affects the strength and breadth of that conclusion even when every reported prediction is computed correctly.
- **Resolution test** Preserve O01 until a frozen external evaluation exists. In the current bounded manuscript, name the evidence as two biological collections with four evaluation panels, preserve the disclosed calibration and selection, and keep rankings descriptive. Methods should distinguish cell/donor or study separation inside a panel from separation of the complete evaluation cohort from model development. This concern does not invalidate the narrow finding that synthetic task training yields useful predictions on these datasets.

### R3-M4

- **Issue key** provisional_disease_prediction_is_not_replicated_state_discovery
- **Severity** Major
- **Blocking** No
- **Axis** claim-moderation
- **Status** Explicitly unresolved claims O02-O04, not a hidden fabrication. The expanded biological claim cannot be treated as achieved; the core classification contribution can stand separately.
- **Claim pointer** The unresolved abstract sentence in `P/sections/abstract.tex` line 1 states that the framework identifies neuropathology-associated cellular states and reproducible predictive expression signatures across independent cohorts. `P/sections/results.tex` lines 82-85 instead describes a provisional donor AUC and future gene analysis and replication.
- **Evidence pointer** `E/FIGURES.md` lines 2288-2293, 2333-2342 and 2351-2356. All exported disease scores are marked nonfinal, the label and donor records have unresolved issues, no disease gene-level result is exported, and the nearest-class-mean comparison is only a point-estimate comparison. `E/sections/knockout.md` lines 139-150 states that expression-direction agreement can also appear under permuted labels and therefore is insufficient biological evidence.
- **Concern** Donor discrimination from microglial expression does not by itself identify a cellular state, a disease mechanism or a reproducible gene signature. Completion of a label rerun alone would not establish those broader endpoints. The current text already recognizes this, but these distinct resolution requirements should remain explicit when the draft is finalized.
- **Why it matters** The abstract disease sentence is the strongest biological-discovery hook, and its evidentiary requirements exceed the current performance result.
- **Resolution test** Maintain the required unresolved markers during drafting. Before presenting the sentence as a finding, require the audited donor-level rerun, an identified gene/state result with held-out-donor and label-specificity evidence, and the claimed independent-cohort replication. If those remain unavailable, remove or narrow the final discovery claim. If the provisional application is retained, its planned Methods should name the expression-data source in addition to the ROSMAP cohort overview and include the existing baseline and cell-type context without claiming a tested microglia-versus-oligodendrocyte difference.

## Minor Comments

### R3-m1

- **Issue key** deletion_attribution_sign_and_absence_boundary
- **Severity** Minor
- **Blocking** No
- **Axis** causal-vs-correlative
- **Status** Missed explanation boundary within an otherwise well-qualified section.
- **Affected element** `P/sections/results.tex` lines 68-77 and `P/tables/s8.tex` lines 45-77.
- **Evidence pointer** `E/sections/knockout.md` lines 55-64 and 213-222. Positive attribution supports the chosen class against its original runner-up; negative attribution opposes that margin. Zeroing a gene already at zero cannot measure the information carried by its absence. `E/data/fig5__marker_ranks.csv` lines 594 and 600 gives LYZ rank 33,354 for the monocyte margin but rank 5 for the monocyte logit.
- **Issue** “Not causal” and “selected marker checks” do not fully explain the semantics of the score. A biological reader may still read sign as up/downregulation or a low rank as evidence that a marker is uninformative. The LYZ contrast already provides a clear counterexample.
- **Required correction** Add the sign convention and zero-baseline limitation to the planned explanation Methods or table note, and use the margin-versus-logit LYZ example to explain context dependence. Do not interpret a low deletion rank as absence of biological relevance.

### R3-m2

- **Issue key** cortex_immune_marker_selection_context
- **Severity** Minor
- **Blocking** No
- **Axis** data-resource-quality
- **Status** Missed class-specific qualification. Correctly classified-cell selection is already disclosed globally.
- **Affected element** `P/tables/s8.tex` lines 39-45 and 74-77.
- **Evidence pointer** `E/sections/knockout.md` lines 249-252 reports approximately 0.17 recall for the development cortex Immune cell class and says its gene ranking describes correctly classified cells. `E/data/fig5__classes.csv`, `case_id=zebra_dev_b10_s0`, `model_id=cellpfn_g1v2p`, `class_label=Immune cell`, contains 24 explained cells.
- **Issue** PTPRC's very low rank and the noncanonical top genes are difficult to interpret without knowing that the explained cells are a selected successful subset of a poorly recovered class. This does not demonstrate an incorrect attribution algorithm or an incorrect atlas label.
- **Required correction** Add the source-reported low-recall qualification and explained-cell count to the cortex attribution note. Keep the recall explicitly tied to the source report unless verified from the underlying class predictions during the planned Methods pass.

### R3-m3

- **Issue key** class_count_extrapolation_not_explained
- **Severity** Minor
- **Blocking** No
- **Axis** writing-clarity
- **Status** Omitted positive capability supported by the current source.
- **Affected element** `P/sections/results.tex` lines 27 and 41; `P/tables/s9.tex` lines 46-63.
- **Evidence pointer** `E/data/fig1__training_stream.csv` lines 18-27 gives training class counts of 2, 4, 6 or 8. The supplied primary fine PBMC task contains 20 classes and the exploratory finest task contains 35, as recorded in `P/tables/s9.tex` and `E/data/supp_prior_ablation__hard_tier_tasks.csv` line 9.
- **Issue** The manuscript explains extrapolation in gene count but leaves class-count extrapolation implicit. This helps a reader understand why task-local labels matter and what the 35-label result demonstrates.
- **Required correction** State the training class-count range and note application to 20 and 35 supplied classes. Keep this an architectural/evaluation capability, with the measured accuracy and exploratory qualification, rather than a claim of unseen-cell-type discovery.

### R3-m4

- **Issue key** finite_deletion_comparison_evidence_underused
- **Severity** Minor
- **Blocking** No
- **Axis** novelty-significance
- **Status** Omitted positive evidence. No missing experiment is alleged.
- **Affected element** `P/sections/results.tex` lines 68-74 contrasts DS-LOO with integrated gradients conceptually but does not present their existing matched finite-deletion comparison.
- **Evidence pointer** `E/sections/knockout.md` lines 88-100 and 170-172; `E/data/fig5__marker_ranks.csv` lines 538-545 and 610-617. For the PBMC reference margin, IL7R and NKG7 have DS-LOO ranks 2 and 7 but IG64 ranks 33,538. Their logit-attribution ranks differ, illustrating that the target matters.
- **Issue** The current presentation explains the speed advantage against exhaustive deletion but leaves the reason to prefer DS-LOO over another inexpensive explanation method underspecified. Existing matched-target evidence can substantiate the finite-deletion objective.
- **Required correction** Include a compact matched-target fidelity comparison in Table S8 or the planned figure, preserving the restriction to the evaluated cases and selected genes. Do not present it as universal superiority to integrated gradients or use margin ranks interchangeably with logit ranks.

## Literature and legacy-motivation check

The following were targeted verification checks, not a full bibliography audit.

- The donor-diversity sentence is supported by the donor-versus-cell subsampling analysis in [scTab, Results and Fig. 2](https://www.nature.com/articles/s41467-024-51059-5). The source also supports the existing manuscript's restrained wording rather than the legacy assertion that modern resources contain only a few hundred donors.
- The statement about pretraining-performance saturation is consistent with the public author-hosted abstract of [DenAdel and colleagues](https://www.microsoft.com/en-us/research/publication/evaluating-the-role-of-pretraining-dataset-size-and-diversity-on-single-cell-foundation-model-performance/). I did not re-evaluate that study's benchmark design.
- [MapPFN](https://arxiv.org/abs/2601.21092) and [PerturbPFN](https://arxiv.org/abs/2607.23447) explicitly concern synthetic-prior cellular perturbation inference. Their inclusion and the distinction from classification are appropriate. MapPFN also permits arbitrary gene sets, so gene-set flexibility alone should not later be promoted to an exclusive novelty claim.
- The cited PBMC marker associations are supported by [Schafflick and colleagues, Fig. 1 and accompanying Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC6959356/). The cortex associations PLP1, SYT1 and CLDN5 are explicitly present in [Gong and colleagues, Fig. 5 and accompanying Results](https://www.nature.com/articles/s41467-024-54715-y). These verify lineage context, not the model's attribution accuracy or disease relevance.
- The ZEBRA bibliography entry matches the [public author-institution manuscript](https://universaar.uni-saarland.de/bitstream/20.500.11880/37183/1/gkad990.pdf). The main task is a selected human cortex subset of the broader murine/human resource.
- The simulator paragraph has sufficient breadth for this scope. It retains the author-written motivation of controlled biological and measurement variation without calling reference-fitted simulators inherently inadequate. The legacy billion-cell throughput, detailed noise-stack and streaming claims are not current numerical evidence and should not be restored by copying the old abstract. `E/FIGURES.md` lines 274-297 documents the evaluated configuration, including no structural gene absence and observation dropout switched off. The planned Methods should name the simulator implementation and distinguish available features from activated features.

## Technical failings that need to be addressed before the case is established

For the current bounded method claim, R3-M1 and R3-M2 need substantive clarification using existing evidence. R3-M3 limits any claim of independently demonstrated generalization. R3-M4 must remain visibly unresolved unless the biological discovery evidence is supplied. No new blocking defect in the narrow descriptive classification result was established by this review.

**Assessment against Nature-style criteria** Originality is plausible in the combination of a cellular task prior, gene-anonymous support-conditioned inference and finite-deletion explanations, rather than in synthetic data, cellular PFNs or marker recovery individually. Scientific importance is strongest as a computational method and currently weaker as a biological-discovery story. Interdisciplinary readership is credible if the label resolution and task mixture are explained. Technical soundness is helped by unusually explicit caveats but remains bounded by development-set selection and provisional disease data. Readability would improve by replacing opaque prior/version and task-stream labels with their biological meaning while retaining raw identifiers in provenance.

**Recommendation posture** Substantive revision of the biological interpretation and reporting, with most newly identified issues resolvable from existing exports. External generalization and disease discovery should retain their present unresolved status. This is not an editorial decision or a prediction of journal acceptance.

## Remaining uncertainty

The internal technical taxonomy was checked within this report's scope. No raw-data statistical audit, full reproducibility assessment, deferred-figure review or governance review was performed. The manuscript does not claim clinical validation. Missing materials in these areas were not converted into presumed deficiencies.

**Risk / unsupported claims** No evidence in this packet establishes causal perturbation responses, universal marker recovery, sex-specific expression mechanisms used by the model, an independently replicated disease signature or external-cohort performance. These are absent or explicitly unresolved, not failed measurements. The report is frozen on completion and must not be revised in response to other reviewers.
