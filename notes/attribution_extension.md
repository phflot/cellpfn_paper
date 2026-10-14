# Sex classification and cell-type gene attribution

Audited 2026-10-14 against the current export. The numerical records are in `evidence/attribution_extension.csv` (X01–X159), with the same declarative schema as `results.csv`. Every record passed the read-only `check_results.extract` calculation. No new model fitting, biological analysis, confidence interval or enrichment test was performed. X89–X159 add the subsequently requested PBMC cell-subtype breakdown.

## What the export supports

ZEBRA refers to the human brain atlas, not zebrafish. Three sex tasks are present and must remain distinct:

| Task | Design and input | Reference CellPFN result | Interpretation |
|---|---|---|---|
| `zebra_sex` | One frozen Sayed 2021 oligodendrocyte case; processed expression, all 21,158 genes; 100 support cells per sex, 200 total from 12 GSM samples; 50 query cells from 10 other GSM samples | 100% cell-level balanced accuracy and 100% GSM-aggregated balanced accuracy; cell NLL 0.40867 and GSM NLL 0.39845 | Sample-disjoint positive example, not independently donor-disjoint replication; GSM is not synonymous with donor. One case gives no between-case uncertainty. X01–X12. |
| `zsex_xy` / panel `zebra_zsex_xy` | Study-matched positive control restricted to studies measuring XIST and at least four of RPS4Y1, DDX3Y, UTY, KDM5D and EIF1AY; 46 female/male unit pairs from eight studies; 14 pairs in query; 16,708 common measured genes before support-selected 8,192-HVG evaluation | Mean unit-level AUC 0.977, 0.993, 1.000 and 1.000 at 4, 8, 16 and 32 support units per sex, respectively | Ten splits reuse largely the same persons. Unit AUC is distinct from cell accuracy. X13–X24 and X37–X40. |
| `zsex` / panel `zebra_zsex` | Broader both-sex study set adds four Lim 2022 pairs, changes the common measured-gene universe to 12,668 genes, and uses 16 query pairs; same 8,192-HVG model view | Mean unit-level AUC 0.507, 0.544, 0.538 and 0.539 at the same support budgets | Near-chance result must accompany the positive control. The two tasks change studies and gene availability, so their difference is not an isolated causal gene-removal experiment. X25–X36 and X41–X44. |

Both later tasks use reference `cellpfn_g1v2p`, checkpoint 96,000. Each support unit contributes 10 cells and each query unit contributes 20 cells. Units are persons except Sayed 2021, where age-by-sex groups of GSM samples are used; cross-study person overlap is unknown. The 16- and 32-unit budgets correspond to 160 and 320 support cells per class and exceed the model's 1–100 training range. The appropriate summaries are descriptive means and ranges across the ten splits, not intervals presented as uncertainty across independent subjects or cohorts. The export explicitly warns that split-based intervals would be anti-conservative.

Exact performance sources are `fig6__operator_prereg_cases.csv` for the original case and `supp_taskmix_tradeoff__efast_cases.csv` for later controls. Design sources are the three corresponding rows of `glossary__panels.csv`; uncertainty guidance is the `supp_taskmix_tradeoff__efast_cases.csv` entry in `DATA_DICTIONARY.md`. `build/ablations/build_taskmix.py` maps `cell_balanced_accuracy` to the exported `balanced_accuracy`, whereas `mean_prob_donor_auc` maps to `unit_level_auc`; the former is **not** a donor-level balanced accuracy.

## Sex-specific gene attribution is absent

No sex case occurs in `fig5__cases.csv`, `fig5__classes.csv`, `fig5__marker_ranks.csv`, `fig5__top_genes.csv` or `fig5__fidelity_by_case.csv`. Their six case configurations cover PBMC, cortex cell types and kidney cell types, with two model states. Thus there is no exported numerical evidence identifying the most influential genes for sex predictions. XIST and the named Y-linked genes above are **task inclusion criteria**, not recovered model-attribution hits. They cannot be described as CellPFN's most relevant sex genes without additional attribution output. The manuscript can state the completed sex prediction results while marking that gene interpretation explicitly unresolved.

## Cell-type attribution supplies concrete marker examples

Use one coherent PBMC example: `case_id=pbmc_l1_b100_s0`, `model_id=cellpfn_g1v2p`, `method_id=dsloo_corr_margin`, `target=margin`. DS-LOO scores 33,538 genes for 191 correctly classified explained cells spanning eight classes. Names are restored from the case column-to-symbol map after prediction; they are not model inputs.

| Class | Supplied marker | DS-LOO class rank | DS-LOO margin effect | Exact-deletion margin effect | Ledger |
|---|---|---:|---:|---:|---|
| B | CD79A | 1 | 1.073200 | 1.072970 | X47, X63–X64 |
| B | MS4A1 | 2 | 0.785195 | 0.784692 | X48, X65–X66 |
| CD4 T | IL7R | 2 | 0.177716 | 0.177439 | X49, X67–X68 |
| CD8 T | CD8A | 2 | 0.560119 | 0.559490 | X50, X69–X70 |
| DC | FCER1A | 1 | 0.715617 | 0.715638 | X51, X71–X72 |
| DC | CLEC10A | 2 | 0.349683 | 0.349899 | X52, X73–X74 |
| Mono | CD14 | 3 | 0.253690 | 0.253447 | X53, X75–X76 |
| NK | GNLY | 2 | 0.433259 | 0.435899 | X54, X77–X78 |
| NK | NKG7 | 7 | 0.228380 | 0.229266 | X55, X79–X80 |

The effects are class means in logit-margin units. Positive means that removing the query gene reduces the predicted-class margin over its original runner-up; it does not mean upregulation or a causal biological effect. These are descriptive matches to markers listed in `code/aggregate.py MARKERS`, not a prespecified marker-enrichment analysis. Other listed markers rank poorly: LILRA4 is 4,392 in the broad DC class, LYZ 33,354 and FCGR3A 79 in monocytes, and CD3E 131 for CD4 T cells. This is a contrast-dependent explanation of the model, not a universal ranking of cell identity genes.

The cortex cell-type case `zebra_dev_b10_s0` also provides marker examples: PLP1 rank 8 in glia, SYT1 rank 7 in neural cells, and FLT1/CLDN5 ranks 5/16 in vascular cells (X81–X84). It uses processed expression, 21,158 genes, ten supports per class and 96 correctly classified explained cells. PTPRC ranks 20,710 in its broad immune class (X85). These are cell-type results and cannot stand in for sex-specific attribution. Primary biological marker support is checked separately in the literature pass.

## What “one inference step” can mean here

`sections/knockout.md`, “What is being compared”, describes one sweep over genes that updates four pooled statistics (mean, RMS, maximum and log-sum-exp), one backward pass through the small prediction head for linearization, and a second backward pass correcting read depth and detected-gene fraction. The two targets are the predicted class and its original runner-up. Query-only deletion holds support and the fitted operator fixed. DS-LOO computes a genome-wide ranking without a separate complete model forward pass per gene, but **does not perform exact all-gene attribution in one ordinary forward inference**. The observed cost remains about 10–13 exact single-gene forward equivalents under matched GPU load and is provisionally timed.

Suitable wording is: “A single sweep over gene contributions, followed by head linearization and normalization corrections, produced query-specific genome-wide attribution rankings.” Avoid “one forward pass gives exact explanations” or “one inference step recovers causal markers”.

## Suggested main-text additions

For biological interpretability: “Class-level rankings recovered established annotation markers: CD79A and MS4A1 ranked first and second in B cells, IL7R and CD8A second in their respective T-cell groups, FCER1A first in dendritic cells, and GNLY second in natural killer cells. These examples connect the gene-anonymous model's decisions to recognizable cellular expression signatures; they are descriptive marker matches rather than an enrichment test.” Attach the verified original biological citations supplied by the literature pass.

For sex prediction: “CellPFN also separated sex labels within oligodendrocytes in a sample-disjoint ZEBRA case, achieving 100% balanced accuracy on 50 query cells from ten GSM samples with 100 labelled support cells per sex. A later study-matched control restricted to studies measuring sex-linked genes reached mean unit-level AUCs of 0.977 and 0.993 with four and eight support units per sex across ten reused-person splits. The broader study set was near chance (0.507 and 0.544), limiting generalization beyond the positive control.” Follow with the explicit unresolved statement that the most relevant sex-prediction genes await matched attribution results. The initial case is one example and must not be called independent donor-level validation.

## Broad labels and difficult PBMC subtypes

The export contains broad eight-class and fine twenty-class PBMC benchmarks, plus eight exploratory tasks focused on sibling subtypes or the finest 35-label vocabulary. It does not define a formal binary “easy” versus “difficult” partition. The difficult tier was defined on 2026-10-11, after Stage 1 read-outs had been seen; its declared selection rule did not use model outputs, but the tier remains post hoc and does not select an arm or change any frozen outcome.

Use reference `cellpfn_g1v2p`, checkpoint 96,000, with 8,192 HVGs throughout this label-resolution comparison. The difficult-tier source is `supp_prior_ablation__hard_tier_cellpfn_values.csv`: `scope_kind=task`, `scope_value` equal to the task identifier, and `metric=H_b1_ba`, `H_b10_ba` or `H_b100_ba`. The task catalogue is `supp_prior_ablation__hard_tier_tasks.csv`. Class counts and label strings are explicitly supplied there.

| PBMC task | Classes | CellPFN BA at 1 support | At 10 supports | At 100 supports | Ledger |
|---|---:|---:|---:|---:|---|
| Level 2, CD4 T siblings | 4 | 36.3% | 69.2% | 85.6% | X92–X94 |
| Level 2, T-cell siblings | 9 | 27.4% | 64.4% | 83.8% | X95–X97 |
| Level 3, CD4 T siblings | 9 | 23.4% | 56.3% | 79.6% | X98–X100 |
| Level 3, CD8 T siblings | 7 | 39.5% | 69.4% | 84.4% | X101–X103 |
| Level 3, B-cell siblings | 6 | 31.6% | 63.6% | 79.8% | X104–X106 |
| Level 3, NK siblings | 6 | 36.2% | 64.3% | 73.0% | X107–X109 |
| Level 3, T-cell siblings | 17 | 25.0% | 55.7% | 76.8% | X110–X112 |
| Level 3, full vocabulary | 35 | 39.8% | 68.4% | 78.4% | X113–X115 |
| Equal-weight mean of the eight tasks | — | 32.4% | 63.9% | 80.2% | X89–X91 |

Class counts are separately registered as X116–X123. Different class counts imply different chance accuracies; raw accuracies should not be used to define a universal difficulty ordering across these heterogeneous tasks. Level-2 CD4 labels comprise naive, central-memory, effector-memory and regulatory T cells. Level-3 splits include multiple memory subtypes, naive versus memory regulatory T cells, kappa/lambda B-cell subtypes and proliferating or CD56-bright NK subsets. Full label strings remain in the task catalogue rather than being reinterpreted biologically.

The matched-view broad benchmarks come from `supp_taskmix_tradeoff__efast_cases.csv` with the same reference model, checkpoint, 8,192-HVG view and support budgets. Eight-class PBMC balanced accuracy is 62.3%, 84.2% and 91.9%; twenty-class PBMC is 53.9%, 81.8% and 90.5% (X151–X156). These are means over ten support draws at B1/B10 and five at B100, matching the difficult tier's draw counts. The tasks nevertheless change label vocabulary and query composition, so this is descriptive context, not a paired causal estimate of changing label granularity. It must not be mixed with the three-draw all-gene primary benchmark without naming the different evaluation view.

The three Kumo-small cellular-training proxy controls (`stream=S`, task streams r42/r43/r44, one common model seed) average 31.6%, 67.3% and 80.4% across the difficult PBMC tasks (X124–X126). Task-specific proxy means are X127–X150. The proxy uses 2,000 HVGs, so these are contextual comparator levels rather than matched-input estimates of architectural advantage. The source warns against treating CellPFN reference-state differences as replicated ablation effects.

Replication is limited: `supp_prior_ablation__hard_tier_cases.csv` contains proxy observations only. Its cases confirm ten support draws at B1/B10 and five at B100 (X157–X159). The CellPFN registry states that its summaries use the same 250 hard-tier cases—ten total tasks, eight PBMC plus two cortex—but its individual case values are not exported. Therefore report the supplied CellPFN means without fabricated ranges or confidence intervals. The eight PBMC tasks share populations and nested labels and do not form eight independent biological experiments. The correctly classified subset in the separate attribution export cannot supply class-specific error rates.

Suggested main-text wording: “Performance depended on label resolution. In an exploratory panel of eight PBMC sibling-subtype and fine-label tasks, the reference model reached mean balanced accuracies of 32.4%, 63.9% and 80.2% at one, ten and 100 supports per class using 8,192 HVGs. At 100 supports, accuracy was 85.6% for four CD4 T-cell subtypes, 73.0% for six NK subtypes and 78.4% across the full 35-class vocabulary. These post hoc results identify remaining annotation difficulty without defining an independent easy-versus-hard benchmark.” The main narrative can contrast the matched-view broad and finer panels if space permits, retaining the source and replication boundaries above.

## Wave 2 review additions

The same reference-checkpoint hard-tier source also supplies the seven-label development cortex task and three-label held-study neural task. Their three-budget means are now in Table S9 and records X160–X165. Tables name requested HVG caps, with realized one-shot widths bound in X166–X169; they do not imply a fixed number of eligible variable genes. Source-based selection used conventional NCM/LR query performance, though it excluded CellPFN/proxy predictions. The tasks remain post hoc.

Marker interpretation is conditional on class versus its fixed runner-up. In the PBMC monocyte example, LYZ has low margin rank but high class-logit rank. Zeroing an already absent gene cannot test the relevance of absence. The cortex immune ranking concerns 24 correctly classified cells from a low-recall class; this qualification and the matched IG64 finite-deletion comparison are now explicit in S8.
