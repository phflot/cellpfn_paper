# Reviewer 2

## Review setup

- **Frozen input** Commit `2275642`, represented by `/tmp/cellpfn_wave1_review_20261014`. Manuscript pointers below refer exclusively to that packet, not the active manuscript.
- **Emphasis** Evaluation design, statistical interpretation, information separation and biological evaluation units.
- **Scope** Abstract, Introduction, Results, main Tables 1 and 2, and Tables S1 to S9. Methods and figures were deliberately deferred. Requests for their content below are implementation requirements for that next stage, not findings that the authors accidentally omitted them.
- **Evidence base** The frozen text, `paper_export_20261011` and selected read-only code in `hashprompt`. Exported case summaries, protocols and caveat records were inspected. No new experiment or model inference was run. No other reviewer report, synthesis or current manuscript was read. No external literature verification was undertaken.
- **Verification boundary** This is an independent source and design assessment, not independent experimental replication. Source code shows implemented safeguards but cannot, by itself, prove the identity or biological independence of every evaluated specimen. Original server artifacts and individual ROSMAP records were unavailable in this packet.

## Overall assessment

The defensible result is a promising computational proof of concept. A relatively compact model trained with synthetic episodes reaches useful cell-annotation performance, and continued training on the cellular task stream improves several released learners in the tested low-support settings. The strongest evidence is the paired comparison on common cases, the explicit accounting of input representations and the willingness to report losses as well as gains.

The main limitation is the distinction between performance on repeatedly inspected development panels and generalization to a new biological collection. The manuscript mostly makes that distinction correctly. It should preserve this restraint when the Methods and figures are added. A second, separate issue is the abstract's unresolved assertion of reproducible neuropathology-associated expression signatures across independent cohorts. That result does not exist in the supplied evidence and must not survive as an asserted finding in a submission version.

I found no new demonstrated support/query label leak, numerical integrity failure or misuse of a cell-level confidence interval as donor replication in the inspected material. That is a bounded finding, not a certificate that every underlying dataset is free of overlap.

## Who would be interested

Single-cell analysts working with scarce annotations, researchers developing task-conditioned models, and simulator developers would be interested in whether a procedural cellular task distribution can teach useful inference without persistent gene identifiers. The transplantation of that distribution into released tabular learners may be especially informative because it separates the practical utility of the task stream from the specific CellPFN architecture. A wider biotechnology readership would need a stronger demonstration on genuinely new collections or a completed biological application.

## Major strengths

- The evaluation keeps model performance conditional on its input route. It does not present all-gene CellPFN, 2k-HVG tabular learners and native foundation-model embeddings as an isolated architecture comparison.
- The uncertainty descriptions are unusually careful. Three-draw ranges, twenty-draw paired intervals, task-stream replicates and single model seeds are distinguished. The twelve panel-budget combinations are used as a descriptive average rather than twelve independent experiments.
- The failed prespecified operator decision, high-support log-loss deterioration, hard-subtype failures and generic-task retention losses remain visible. Subsequent descriptive gains do not retroactively reverse the frozen decision.
- The exposure audit distinguishes source-study overlap from exact-cell identity and target-label exposure. The sex analyses likewise distinguish GSM separation from established donor separation.

## Major Concerns

### R2-M1

- **Issue key** development_selection_limits_generalization
- **Severity** Major
- **Blocking** No
- **Axis** experimental-design
- **Status** Confirmed and already disclosed design limitation. Performance on an untouched cohort remains unresolved, not a measured failure.
- **Claim pointer** `sections/abstract.tex:1`, competitive classification across four panels; `sections/results.tex:15-24`, particularly the development-panel model selection and O01; `tables/overview.tex:13-35`, headline comparisons and overall average.
- **Evidence pointer** `paper_export_20261011/data/fig4__best_per_family.csv`, rows for `cellpfn_r10k`, `cellpfn_c1v2p`, `cellpfn_g1v2p` and the family selection rules; `paper_export_20261011/FIGURES.md:909-916` and `:1002-1004`; `paper_export_20261011/data/fig4__caveats.csv`, keys `step6_selection_history` and `best_per_family_selection`. `sections/results.tex:4` additionally states that statistics of the evaluated real datasets informed the prior.
- **Concern** The reported case pools contributed to earlier architecture and prior development, and family variants were selected with their results available. Study separation between support and query does not turn those query results into an independent test of model development. The four panels also comprise two PBMC annotation levels and two cortex query sets, not four independent biological domains. More support draws from those same pools cannot resolve this selection problem. The current prose discloses these facts and avoids a universal ranking, so the descriptive proof of concept remains interpretable. The breadth and reliability of the proposed inference method are nevertheless not established by these numbers alone.
- **Why it matters** Generalization across heterogeneous experiments motivates the paper. A strong performance average after repeated use of the same panels is a different estimand from expected performance on an unseen collection. This is a substantive scientific limitation even when transparently reported. It does not invalidate the narrower observed performance claim, hence the nonblocking classification.
- **Resolution test** For a stronger generalization claim, freeze the checkpoint, gene views, preprocessing, comparator classifiers, endpoints and analysis before opening additional cohorts that were not used for prior calibration or design choices. Resolve donor identity and study reuse across support, query and development data, then report performance at the independent donor or study level alongside conditional support-draw variability. If that evidence is outside the present scope, consistently describe this as development-panel evidence and narrow the claimed breadth. Add the selection status directly to the main-table caption so the standalone table carries the same limit as Results and S1. Independent training seeds would address training-run robustness, but would not replace the new-cohort test.

### R2-M2

- **Issue key** neuropathology_signature_claim_precedes_evidence
- **Severity** Major
- **Blocking** No
- **Axis** claim-moderation
- **Status** Confirmed unsupported draft assertion, explicitly marked unresolved. Label correction, disease attribution and independent replication remain unresolved.
- **Claim pointer** `sections/abstract.tex:1`, O04 asserts that the framework identifies neuropathology-associated cellular states and reproducible predictive expression signatures across independent cohorts. Contrast `sections/results.tex:82-85`, O02 and O03, and `tables/s9.tex:42`.
- **Evidence pointer** `paper_export_20261011/FIGURES.md:2284-2289`, `:2333-2342` and `:2349-2356`; `paper_export_20261011/data/supp_rosmap__label_issues.csv`, especially `I4`, `sex-label`, `store` and `pending`; `paper_export_20261011/data/supp_rosmap__auc.csv`, the pooled matched microglial T1 headline record. The export explicitly has no ROSMAP gene-level result.
- **Concern** A provisional donor AUC from repeated splits supports neither discovery of reproducible expression signatures nor replication across independent cohorts. The Results correctly present those steps as future work, while the abstract currently states their success. The red unresolved marker makes this an auditable draft issue rather than a concealed result, but it does not supply the missing evidence. The pending audit includes donor aliases, missing labels and possible sex-label or demultiplexing issues, so it is more specific than simply waiting for a final AUC value.
- **Why it matters** This sentence supplies much of the paper's biological reach beyond annotation benchmarking. Readers must not infer that a disease mechanism, disease-gene signature or independent replication has been demonstrated. Removal of that unsupported claim would leave the computational proof of concept intact, hence this concern does not block that narrower central case.
- **Resolution test** Remove or recast O04 as prospective until the corrected frozen donor analysis, actual gene-attribution output and independent cohort evaluation exist. If the application is retained, the Methods should document donor alias resolution, support/query donor separation, endpoint coding, exclusions, cell-to-donor score aggregation, sex matching and the repeated-split interval correction. Show the appropriate simple expression and covariate baselines already represented in the export before attributing utility to CellPFN. Do not imply that all listed label defects changed the current 0.745 estimate. The export says the Mount Sinai CERAD-scale problem and the raw-column inversion affect zero donors in the reported pools; the current concern is unresolved provenance and validation, not proof that this AUC is wrong.

## Minor Comments

### R2-m1

- **Issue key** evaluation_units_and_information_flow_map
- **Severity** Minor
- **Axis** reproducibility
- **Status** Required Methods detail, with implemented safeguards located. Actual biological independence is not fully assessable from exported summaries.
- **Affected element** `sections/results.tex:15-24` and `tables/overview.tex:34`. Readers currently receive support budgets and draw counts without a compact map of sample units, query sizes and split definitions.
- **Evidence pointer** `paper_export_20261011/data/fig4__panels.csv`, PBMC and ZEBRA records; `hashprompt/src/hashprompt/frozen_evaluation.py:1406-1422`; `hashprompt/experiments/run_tabular_foundation_reference.py:170-193`, `:317-344` and `:417-420`; `hashprompt/src/hashprompt/tabular_foundation_references.py`, `build_support_views`; `paper_export_20261011/data/fig4__caveats.csv`, key `step6_views`.
- **Issue** PBMC uses support donors P1/P3/P5/P7 and query donors P2/P4/P6/P8, with 320 coarse and 800 fine query cells. The cortex query panels contain 7,769 and 7,163 cells. The frozen cortex loader checks observation, donor-identifier and study disjointness. Support-only HVG/PCA construction is also implemented. These are important positive controls that should be reported explicitly. Identifier-disjoint checks do not establish that differently named samples cannot come from the same person.
- **Required correction** Add a Methods design table giving source studies, classes, support and query cells, unique donors or unresolved proxies, biological split unit, fixed versus resampled query pools, and fitting scope of every data-derived preprocessing step. State whether PBMC annotation levels reuse cells and donors and whether cortex panels reuse their support pool. Preserve the distinction between cell-level balanced accuracy and donor-level inference. This request does not allege leakage or criticize the deliberate deferral of Methods.

### R2-m2

- **Issue key** contextual_baseline_training_recipe_caveats
- **Severity** Minor
- **Axis** experimental-design
- **Status** Confirmed omitted comparator caveats in the current S1 caption. scGPT scaling sensitivity is already disclosed in S9.
- **Affected element** `tables/s1.tex:24-25`, `:42-43` and `:83`; `tables/overview.tex:34`; `tables/s9.tex:31`.
- **Evidence pointer** `paper_export_20261011/data/fig4__caveats.csv`, keys `realcell_c01`, `realcell_c05`, `realcell_c06` and `realcell_c08`; `paper_export_20261011/FIGURES.md:979-989`; `paper_export_20261011/data/fig4__scanvi_training_budget.csv`.
- **Issue** S1 flags the transductive scANVI route but omits the more consequential low-support training caveat. The documented inductive recipe used ten scANVI epochs and a training holdout. At fine-PBMC one-shot support, only 18 of the 20 labelled cells entered training, leaving at least two classes without a training example. The low-support scores therefore describe this recipe, not the method's attainable few-label performance. SingleR also used the default marker mode despite the source recording a different recommended single-cell-reference setting. Separately, changing scGPT's classifier standardization changes its PBMC mean by four points, already reported in S9.
- **Required correction** Flag scANVI B1/B10 values as constrained by the declared training recipe and report the removed-label detail. State the SingleR marker setting in Methods and label its scores accordingly. Link the main scGPT caption to the existing classifier-sensitivity result. Do not silently substitute post hoc tuned baselines into the original frozen comparison. The minor severity reflects that these are contextual baselines and the current central claim does not rely on defeating scANVI or SingleR.

### R2-m3

- **Issue key** operator_gate_and_training_effects
- **Severity** Minor
- **Axis** causal-vs-correlative
- **Status** Confirmed implementation detail needed to interpret the ablation table.
- **Affected element** `sections/results.tex:7` and `:49`; `tables/s4.tex:10-21`, `:29-40` and `:43-54`.
- **Evidence pointer** `hashprompt/src/hashprompt/models/gene_gene_operator.py:137-146`; `paper_export_20261011/data/fig1__facts.csv`, keys `operator.gate_formula` and `operator.gate_values`.
- **Issue** The support-size gate is exactly zero with one support cell per class. Consequently, the nonzero B1 differences between separately trained full, diagonal and no-operator models cannot be interpreted as direct use of covariance at one-shot inference. They can reflect the different learned weights produced by the training arms. The Results already say that these are separately trained models, and S4 separately identifies an inference-time operator-off control, so there is no demonstrated causal misstatement. An explicit sentence would prevent a predictable misreading of the table.
- **Required correction** State the gate and explain that trained-arm contrasts include learning-history effects, whereas an operator-off intervention with the same weights addresses the operator's immediate inference contribution. Retain the existing single-training-seed qualification and failed prespecified decision.

## Checks that did not generate additional concerns

- **Training exposure denominators** Results line 10 and S2 correctly distinguish 12,000 banks, 384,000 scheduled episodes, 276,828 loss-bearing episodes and added tabular adaptation tasks. The approximately ninety-fold comparison to TabICLv2 is explicitly between different exposure units and is not claimed as matched-compute efficiency. No denominator correction is requested.
- **Support draws versus training seeds** S3, S4 and S6 correctly condition their intervals on support resampling. Task-stream replicates share a model seed. These data should not acquire an independent-training or donor-population interpretation in future figures, but the present text does not make that error.
- **Prior and task-mixture causality** Results lines 36 and 55 disclose unmatched generic-control dimensions and 1.67-fold cell exposure. S5 preserves unsuccessful, routing-only and unresolved outcomes. These support practical training-recipe observations, not a uniquely identified biological mechanism. The current caveats are adequate for that limited inference.
- **Post hoc subtype selection** Results line 27 and S9 lines 43 to 63 expressly identify the eight tasks as exploratory, retain class counts and avoid inventing support-draw intervals from proxy records. Their overlapping taxonomic definitions do not constitute eight independent biological replications, but the current descriptive aggregate does not claim that they do.
- **Exposure evidence** The 92.6% quantity is a source-study fraction, not a measured exact-cell overlap rate. The frozen audit explicitly describes the unavailable original corpus-matching artifacts. I did not independently verify the corpus records. There is no basis here to infer supervised label leakage or to assign the Geneformer advantage causally to exposure.
- **Sex evaluation bounds** Results line 63 and S9 lines 72 to 84 correctly disclose GSM proxies, unresolved person overlap, repeated-person splits, different eligibility rules and the near-chance broader task. The XY-positive-control AUC does not identify the features used by the model, and O06 correctly leaves attribution unresolved. No additional claim reduction is needed beyond preserving these limits.
- **Processed cortex sensitivity** S9 keeps the changed-gene-universe reconstruction comparison separate from the ten-draw removal of unmeasured genes. It does not falsely isolate normalization from those comparisons.

## Technical failings to address before a stronger case is established

R2-M1 is the principal limitation on claims of generalization. R2-M2 must be resolved by evidence or removal of the uncompleted abstract claim before submission. Neither is a newly detected numerical invalidation of the narrower synthetic-training proof of concept. No additional blocking concern was established from the reviewed materials.

## Assessment against Nature-style criteria

- **Originality** The combination of a cellular procedural prior, gene-anonymous inference and transfer of the prior to existing tabular models is a plausible contribution. This design review does not establish priority over the cited literature.
- **Scientific importance** The limited-label setting is important. Current evidence supports an interesting method and task-stream result, with limited evidence for generality or new biological discovery.
- **Interdisciplinary readership** The prior-transfer result can connect single-cell analysis, simulation and machine learning. The paper should make clear which inference is portable and which observations are specific to the two tissue domains represented here.
- **Technical soundness** Pairing and uncertainty descriptions are strong. Development selection and biological identity resolution remain the major limits. Implementation guards support the intended separation but are not a replacement for a specimen-level provenance audit.
- **Readability for nonspecialists** Most claims are restrained and interpretable. A compact evaluation-unit diagram or Methods table would be more useful than additional statistical caveats scattered through Results. The unexplained operator difference at one-shot support and the draft biological promise are the most preventable sources of confusion.

## Recommendation posture

Substantive completion is needed before treating this as a broadly validated Nature Biotechnology Article. The present material supports continued development and a carefully bounded computational account. It does not yet establish independent-cohort generalization or reproducible disease expression signatures. This is an author-facing assessment, not an editorial decision.

## Risk and unsupported claims

The independent-cohort signature claim is unsupported. Donor independence in every pooled biological dataset, exact-cell foundation-model exposure and population-level uncertainty are not fully assessable from the supplied aggregates. None of these unresolved points should be reported as an observed negative result. Detailed Methods and figures were outside the frozen Wave 1 packet and were not judged as missing submissions.

**Frozen on 14 October 2026.** This report was finalized independently and will not be revised in response to other reports or a synthesis.
