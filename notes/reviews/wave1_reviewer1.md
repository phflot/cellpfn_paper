# Reviewer 1

## Review setup

- **Input scope** Frozen Wave 1 manuscript at commit `2275642`, abstract, introduction, Results, two main tables and Tables S1-S9. Assigned emphasis was numerical provenance and completeness.
- **Assessment boundary** Methods and figures were deliberately deferred. This report identifies details they should supply but does not count their absence as an oversight. No experiments, source edits, other reviewer reports or current manuscript revisions were used.
- **Claim summary** A compact, gene-anonymous model trained on synthetic cellular tasks supports few-shot annotation, the prior improves released tabular models, and query-gene deletion explains selected classifier decisions.
- **Evidence base** `P` below denotes `/tmp/cellpfn_wave1_review_20261014`. `E` denotes `/home/phflot/projects/ccb/hashprompt/paper/paper_export_20261011`. I independently regrouped exported case rows and inspected build definitions. I did not run the manuscript's existing check scripts.
- **Confidence limits** This verifies arithmetic, definitions and correspondence with the supplied export, not predictions against raw biological data or independent experimental replication. Some source receipts and original corpus audits are available only through exported provenance. External literature priority and the published TabICLv2 pretraining numerator were not freshly audited.

## Overall assessment

The main quantitative story is substantially supported by the supplied export. I found no wrong headline benchmark average, omitted failed prespecified operator test, or conflation of the single ZEBRA sex case with the later unit-level evaluations. The manuscript already handles many consequential limitations well. The remaining numerical presentation issues are localized, principally actual gene-panel widths, the baseline used for paired adaptation deltas, and the exposure-flag convention. The expanded biological claim in the abstract remains unsupported, as the manuscript itself marks explicitly.

**Who would be interested** Single-cell analysts working with limited labels, researchers building support-conditioned classifiers, and simulation-based learning researchers. The practical attraction is inference on large gene panels without fitting model weights to each target task. The evidence currently establishes a computational-method contribution more clearly than a new biological discovery.

**Major strengths** The tables preserve uncompetitive results, distinguish support-draw variability from model-seed replication, show conventional LDA, disclose evaluation-panel selection, retain the negative operator decision and probability-prediction tradeoffs, and keep disease results provisional. These choices materially improve the credibility of the comparison.

## Major Concerns

### R1-M1

- **Severity** Major.
- **Blocking** No for the core computational case. The expanded abstract claim cannot remain in a submission as an established result.
- **Axis** `claim-moderation`.
- **Status** Confirmed unsupported claim, already disclosed by draft marker O04. This is not a newly discovered numerical error.
- **Claim pointer** `P/sections/abstract.tex:1`, the assertion that the framework identifies neuropathology-associated cellular states and reproducible expression signatures across independent cohorts.
- **Evidence pointer** `P/sections/results.tex:82` and `:85`; `P/tables/s9.tex:42`; `E/data/supp_rosmap__label_issues.csv`, rows keyed `store` and `pending`. The only presented disease number is provisional donor AUC 0.745 with a repeated-split interval. The Results identify disease attribution and independent-cohort testing as future work.
- **Concern and importance** A repeated-split discrimination result does not establish a reproducible expression signature or independent-cohort replication. This matters especially for the biological significance presented to a Nature Biotechnology readership. The existing red marker makes the gap auditable but does not supply the missing evidence.
- **Resolution test** Remove or narrow this abstract sentence to completed computational findings, or replace it with results from a label-audited analysis, a completed gene-attribution analysis and genuinely independent cohort verification. Do not convert the reported repeated-split interval into evidence of replication.

## Minor Comments

### R1-m1

- **Severity** Minor. **Blocking** No.
- **Axis** `figures-and-tables`.
- **Status** Confirmed reporting omission. Accuracy values themselves reconcile.
- **Affected element** `P/sections/results.tex:27` and `:41`; `P/tables/overview.tex:47` and `:56`; `P/tables/s3.tex:29`; `P/tables/s9.tex:63`. The labels describe fixed “8,192 HVGs” and “2k HVGs” without explaining their caps.
- **Evidence pointer** `E/data/fig2__cases.csv`, filter `model_id=cellpfn_g1v2p`, `gene_view=hvg8192`, `support_per_class=1`, `metric=balanced_accuracy`. The three primary PBMC-coarse draws contain 7,459, 6,995 and 7,647 genes. The cortex draws contain 5,301, 3,988 and 2,209 genes, including rows 9794, 9797 and 9800 for development cortex. Across twenty cortex draws the range is 1,313 to 7,590. Even the nominal 2k view reaches only 1,313 genes for some later one-shot draws. The variable-gene rule is explicitly documented in `E/build/scaling_transfer/write_sections.py:143` through `:148`.
- **Issue** A reader can mistake a requested maximum for a controlled input width. This matters when interpreting gene scaling and the difference between three-draw and twenty-draw analyses. The all-gene widths of 33,538 and 21,158 are supported.
- **Required correction** Define these as “up to 2,000” and “up to 8,192 support-selected HVGs” in the relevant table notes, and give realized one-shot widths or a compact pointer to them in Methods. Keep the reported accuracy values unchanged.

### R1-m2

- **Severity** Minor. **Blocking** No.
- **Axis** `writing-clarity`.
- **Status** Confirmed missing task definition in the main presentation.
- **Affected element** `P/sections/results.tex:15` and Table 1, `P/tables/overview.tex:34`.
- **Evidence pointer** `E/data/glossary__panels.csv:2`, `:3`, `:4` and `:6` define 8 PBMC-coarse classes, 20 PBMC-fine classes, and four broad cortex classes in each ZEBRA panel. The cortex classes are Glia, Immune cell, Neural and Vascular cell. `E/data/fig1__facts.csv:144`, key `stream.classes`, gives training tasks with 2, 4, 6 or 8 classes.
- **Issue** “Cortex annotation” can sound like neuronal-subtype annotation. The 91.9% held-study result is four-way broad-class discrimination. PBMC class counts appear much later in S9, but main-table readers need the annotation resolution before comparing tasks. The training class-count range also supplies useful context for the genuine 20-class and 35-class evaluations.
- **Required correction** State the class counts and broad cortex categories in the main benchmark paragraph or caption. Include the training class-count range in the forthcoming Methods, without implying that the 35-class post hoc task was a prespecified class-scaling experiment.

### R1-m3

- **Severity** Minor. **Blocking** No.
- **Axis** `reproducibility`.
- **Status** Confirmed comparator-definition omission, not an incorrect exported delta.
- **Affected element** `P/tables/s2.tex:26` through `:35`, particularly Kumo-small gains +10.79 and +1.31 points.
- **Evidence pointer** `E/build/scaling_transfer/build_fig3.py:351` through `:371` distinguishes a released baseline rescored in the adaptation run from the stored benchmark baseline. In `E/data/fig3__paired.csv`, filter `model_id=k2b_s40k`, four core panels, `gene_view=hvg2000`, `metric=balanced_accuracy`, draws 0-2. The respective mean `delta` values are 10.79405 and 1.31034; `delta_vs_benchmark_base` gives 10.77428 and 1.32255. For example, row 4811 has a released score of 44.500 versus the stored 44.625.
- **Issue** Table S2 is correct for the matched rescoring comparator, but its caption reads as a direct subtraction of the released values shown in Table 1. The discrepancy is small and does not change the rounded main-text gain or conclusion.
- **Required correction** State that adaptation deltas use the released checkpoint rescored within the same scoring run, whereas Table 1 uses stored benchmark scores. Alternatively use the explicit benchmark-relative delta consistently. No new analysis is needed.

### R1-m4

- **Severity** Minor. **Blocking** No.
- **Axis** `figures-and-tables`.
- **Status** Confirmed ambiguity in flag scope. Exact-cell inclusion remains unverified.
- **Affected element** `P/tables/overview.tex:35`, especially “flags likely pretraining exposure” and the qualification about unmarked scores only “outside” the audited corpora.
- **Evidence pointer** `E/data/supp_exposure__panel_chances.csv:10` records likely scGPT exposure for approximately 3% of the ZEBRA support union, with an upper possibility near 10%. Row 11 also records Geneformer support exposure. The manuscript nevertheless leaves scGPT cortex entries unstarred, consistently with a query-source flag convention. `P/notes/geneformer_exposure_audit.md` explicitly describes that convention.
- **Issue** The caption does not say clearly that the flags follow query-source overlap. A reader could interpret the best unflagged score as free of any known pretraining exposure, including support cells, despite the recorded audit.
- **Required correction** Define the stars as query-cell or query-source exposure flags and state that support-source overlap is a separate audit dimension. Say that unmarked scores do not certify absence of exposure, including within the audited corpora. The current gray styling and bold winners can remain.

## Numerical verification and important coverage

- Independently aggregated the primary model comparisons from `E/data/fig4__cases.csv`. The overall means reproduce 72.94565 for CellPFN, 66.83125 for TabICLv2, 70.11229 for Kumo large and 74.85346 for Geneformer. All 192 numerical or missing-data positions in S1 reconcile with their source means and ranges. Decimal half-up rounding explains entries such as 83.25 becoming 83.3. Bold ties at displayed precision, including CellPFN and LDA at 94.7, follow the stated rule.
- Independently aggregated `E/data/fig2__cases.csv` and recomputed paired support-draw t intervals. The three-draw gene-view means, twenty-draw S3 means, and all twelve S3 contrast intervals agree. The 33,538 and 21,158 all-gene counts and 8,192 training maximum are supported, subject to R1-m1 for HVG views.
- The 12,329,889 parameters, 96,000 updates, 12,000 banks, 384,000 scheduled episodes and 276,828 loss-bearing episodes reconcile with `E/data/fig1__facts.csv` and `fig1__lineage.csv`. The 320,000 plus 64,000 prior windows sum correctly. Adaptation arms in `fig3__arms.csv` support 40,000 cellular tasks plus 10,000 replay tasks. The manuscript appropriately avoids treating these units as matched compute.
- Independently recomputed the full-versus-no-operator S4 contrasts and S6 accuracy and NLL intervals from `fig6__operator_cases.csv` and `fig6__taskmix_cases.csv`. They agree. S5's ten candidate effect rows agree with the decisive replicate rows in `supp_prior_ablation__replicates.csv`; the failed and non-decisive outcomes are retained. S7's cited medians and sampling units match the corresponding public-reference export summaries. This last check does not independently validate simulator realism.
- S9 PBMC coarse/fine values reproduce from the reference checkpoint's E-fast case records. The eight PBMC subtype summaries yield 32.40052%, 63.90343% and 80.17343%. The individual 9-class CD4 values and all other displayed subtype values agree. The hard-task checkpoint export contains summaries, so its unavailable draw-level uncertainty cannot be independently reconstructed. The manuscript correctly says so.
- The original ZEBRA sex case matches `fig6__operator_prereg_cases.csv` and `glossary__panels.csv`. Independent regrouping of `supp_taskmix_tradeoff__efast_cases.csv` reproduces all eight later sex-task means and ranges, including positive-control 0.97653 and broader-task 0.50742 at four units per class. The distinction between GSM samples and people, the poor broader-task result, changed study/gene universes, and absent sex-specific attribution are disclosed.
- The Geneformer source fractions recompute as 6,632/7,163 = 92.587% and 1,735/7,769 = 22.332%. These are source-study fractions, not independently verified exact-cell overlap. The manuscript preserves that distinction.
- Reaggregation of DS-LOO class-level cell-correlation medians reproduces S8. The finite-deletion example is 0.450262 among 191 explained cells versus 0.0026178 over 382 pooled random-control curves in `fig5__deletion_curves.csv`, correctly rounded to 45.0% and 0.3%. The 67.8587-second timing, 10.3625 forward equivalents and 219,623-second extrapolation reconcile with the load-matched rows of `fig5__cost_by_route.csv`. Marker ranks and the separation of cell-type from sex attributions agree with the export. These checks verify model-intervention reporting, not biological causality.

I found no further omitted numerical result that would reverse the bounded main conclusions. Important adverse findings already included are the fine-PBMC adaptation loss, generic-task retention loss, failed operator rule, higher-support NLL deterioration, post hoc hard-cortex loss, near-chance broader sex prediction, and low ranks of some familiar lineage markers.

## Technical failings and recommendation posture

No numerical blocking failure was established for the core cellular-prior and annotation claims. R1-M1 must be resolved if the biological abstract claim is retained. R1-m1 through R1-m4 can be addressed through concise source-faithful definitions and captions. The existing O01 and O06 limitations, training-seed limitations and provisional disease status remain substantive boundaries, not newly discovered errors.

**Nature-style assessment** Originality is plausible in the combination of a cellular task prior, gene-anonymous inference and finite-deletion explanation, but priority is not established by this numerical audit. Scientific importance is supported for limited-label inference; broad biological discovery remains unestablished. Interdisciplinary readership is credible. Technical soundness is strengthened by traceable numerical reporting and explicit negative results. Readability would improve with the task-class and gene-width definitions above. The computational results are promising enough to develop into a complete Article, with the final venue case dependent on the completed evidence package rather than the current unsupported biological sentence.

**Freeze statement** Completed independently on 14 October 2026. This report is frozen before any cross-review comparison.
