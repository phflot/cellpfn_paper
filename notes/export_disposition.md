# Evidence disposition for quantitative Wave 1

This document allocates every export block. The per-file decisions and reasons are in [export_index.json](../evidence/export_index.json); the complete navigational inventory is [export_index.md](export_index.md). A file can support more than one destination. Figure production and code-level Methods remain later waves.

| Evidence block | Destination | Editorial decision |
|---|---|---|
| `fig1`: Model, simulator and training lineage | main; appendix; later Methods | Report architecture and training exposure now; reserve code-level construction and training details for Methods. |
| `fig2`: Gene-view and transcriptome-width comparisons | main; appendix | Quantify paired gene-width benefits and losses; preserve support-draw uncertainty and alternate views. |
| `fig3`: Transfer of the cellular prior to tabular models | main; appendix | Report matched-parent adaptation gains, support-budget dependence and negative transfer; retain generic-table tradeoffs. |
| `fig4`: Biological benchmark and model context | main; appendix | Populate the main performance table and complete panel-level appendix; distinguish declared series from post hoc diagnostics. |
| `fig5`: Gene-deletion attribution, fidelity and cost | main; appendix; later Methods | Report validated fidelity and stability with restricted validation scope; distinguish measured, inferred and hypothetical timing routes. |
| `fig6`: Operator and task-mixture ablations | main; appendix | Report all three operator arms, the failed prespecified test, later paired comparisons and probability-quality tradeoffs. |
| `fig7`: Simulator realism against public biological references | main; appendix | Quantify alignment and remaining discrepancy descriptively; calibration references are not independent validation. |
| `supp_exposure`: Pretraining-exposure qualifications | main; appendix | Qualify benchmark interpretation with public pretraining exposure and uncertain exact-cell overlap. |
| `supp_prior_ablation`: Ten-candidate prior screen and hard-tier checks | main; appendix | Report the positive filtering result alongside all neutral, rejected, unresolved and untestable candidates. |
| `supp_rosmap`: Provisional ROSMAP aggregates and label issues | main (provisional); appendix; later Methods | Keep provisional status explicit; no final biological claim before label corrections and the controlled-data analysis. |
| `supp_stored_zeros`: Stored-zero and reconstructed-count sensitivity | appendix | Retain exploratory sensitivity and support-replacement checks without changing the primary benchmark input. |
| `supp_taskmix_tradeoff`: Task-mixture checkpoint and gene-view tradeoffs | main; appendix | Preserve checkpoint/view confounding and unequal sampling; also report the distinct later Zebra donor-unit sex controls without attributing them to specific genes. |
| `glossary`: Model, panel, metric and vocabulary definitions | provenance; later Methods | Resolve the harmonized identifiers and metric meanings used by every evidence table. |

## Rules for retaining or excluding detail

- Main Results report numerical effect sizes and the important negative outcomes; the appendix holds the full benchmark and ablation matrices, input variants and sensitivity checks.
- Case-, cell- and gene-level arrays remain machine-readable source evidence. Their summaries enter the appendix; printing every underlying observation would obscure the experimental unit.
- Wide-format copies are convenience views of the long-format parents and are not additional evidence.
- Supporting diagnostics never overwrite the declared benchmark. This includes post hoc standardized embeddings, alternate feature views, reconstructed counts and hard-tier subgroup checks.
- The failed prespecified operator test remains visible separately from later twenty-draw descriptive estimates. The prespecified PBMC donor-enumeration interval has approximate 80% coverage; the Zebra donor-bootstrap interval has 95% coverage.
- The ten-candidate prior campaign retains all verdicts, noise bands and task-stream replicates, including A8d proxy-headroom failure, the two-replicate hard tier and its authorized skipped-task deviation.
- Task-mixture improvements accompany negative-log-likelihood tradeoffs and unequal cells per update; generic-table degradation accompanies biological transfer gains.
- ROSMAP aggregates remain in the main text only as bold-red provisional O02, with supporting appendix detail. Attribution timing likewise remains provisional O05; estimates and hypothetical routes are not completed measurements.
- Simulator realism is descriptive and uses calibration references. Unit counts differ by statistic and synthetic observations may share a bank.
- Every non-data file has a provenance, historical or later-Methods role; no file is left unclassified. Source hashes and source folders remain unchanged.
