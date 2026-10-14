# Wave 1 quantitative review

The initial Wave 1 manuscript already reported benchmark, transfer and attribution numbers. The substantive gap was quantitative support for ablations, prior screening and simulator diagnostics, plus an accessible overview table and systematic uncertainty reporting. These belong in Wave 1 Results; the full Methods audit and figure production remain later waves.

This pass extracts supplied exported values and descriptive summaries. It adds no biological analysis or new inferential test. Main text and appendix may use the records below; exact selection recipes are in `evidence/results.csv`.

## Statistical reporting boundaries

- Three-draw benchmarks: means and ranges, one model per arm. Four panels and three support budgets define twelve heterogeneous evaluation conditions, not twelve interchangeable independent experiments. No confidence interval across this aggregate.
- Twenty-draw follow-ups: supplied paired 95% t intervals cover support sampling with fixed query sets and fixed trained networks. They do not cover training-seed variation or biological-population uncertainty.
- Operator: the prespecified coarse-PBMC B10 harm outcome remains NOT SUPPORTED (−1.5625 points, allowed magnitude 1.5). Its PBMC donor-enumeration interval has approximately 80% coverage. Later descriptive results do not overturn the frozen decision.
- Proxy campaign: 10 candidate arms, one model seed, three task-stream replicates; LR alone met the keep rule. A1/A2/A3/A4 labels route future work and do not establish benefit. A7/A8d extension replicates were not run. A8d is not testable for the intended repair because proxy headroom is too small; r43 includes a documented invalid-task skip.
- Learnable CellPFN continuation: the positive one-shot changes coexist with higher B100 NLL on three panels and lower NLL on fine PBMC. GL1 received 1.671 times the cells per update; this is not a matched-data task-choice ablation. NLL is predictive log loss, not a calibration-only measure.
- Simulator diagnostics: distributions and real-data ranges describe realism; they are not confidence intervals or an independent test of biological fidelity. Simulated effects are nested within banks. The real reference was reused in development.
- DS-LOO overlap 0.43–0.56 covers changed support sizes as well as changed draws. At fixed ten-support budget, the displayed two-model range is 0.43–0.52. Query-only selected-gene fidelity does not establish causal biology.
- Generic retention uses four conventional datasets, five split seeds and budgets B1/B10/Bmax. Do not rename Bmax as B100. The 70.9% to 64.0% one-shot comparison is balanced accuracy; ordinary accuracy is 69.3% to 62.0%.

## Added source-grounded records

| ID | Claim | Unrounded registered value | Unit |
|---|---|---:|---|
| R58 | All genes minus 2000 HVGs zebra_ood B10 mean change | 7.41449647884314 | percentage_points |
| R59 | All genes minus 2000 HVGs zebra_ood B10 95% interval lower | 5.26370760387089 | percentage_points |
| R60 | All genes minus 2000 HVGs zebra_ood B10 95% interval upper | 9.56528535381539 | percentage_points |
| R61 | All genes minus 2000 HVGs pbmc_l1 B1 mean change | -3.3125 | percentage_points |
| R62 | All genes minus 2000 HVGs pbmc_l1 B1 95% interval lower | -5.20067725177135 | percentage_points |
| R63 | All genes minus 2000 HVGs pbmc_l1 B1 95% interval upper | -1.42432274822866 | percentage_points |
| R64 | All genes minus 2000 HVGs pbmc_l2 B1 mean change | -1.95625 | percentage_points |
| R65 | All genes minus 2000 HVGs pbmc_l2 B1 95% interval lower | -3.26717890738317 | percentage_points |
| R66 | All genes minus 2000 HVGs pbmc_l2 B1 95% interval upper | -0.645321092616828 | percentage_points |
| R67 | Released TabICLv2 fine PBMC B10 | 73.75 | BA_pct |
| R68 | Cellular-adapted TabICLv2 fine PBMC B10 | 64.625 | BA_pct |
| R69 | Cellular adaptation change fine PBMC B10 | -9.12500000000001 | percentage_points |
| R70 | tabicl_v2 generic-table balanced accuracy B1 | 70.9185995733063 | BA_pct |
| R71 | tabicl_v2 generic-table balanced accuracy all budgets | 87.7693053040034 | BA_pct |
| R72 | c2b40k generic-table balanced accuracy B1 | 63.9657601579453 | BA_pct |
| R73 | c2b40k generic-table balanced accuracy all budgets | 84.8405449929767 | BA_pct |
| R74 | Fine PBMC B100 no operator | 82.21875 | BA_pct |
| R75 | Fine PBMC B100 diagonal operator | 85.65625 | BA_pct |
| R76 | Fine PBMC B100 full operator | 89.025 | BA_pct |
| R77 | Fine PBMC B100 full minus none mean change | 6.80625 | percentage_points |
| R78 | Fine PBMC B100 full minus none 95% interval lower | 6.35569816977661 | percentage_points |
| R79 | Fine PBMC B100 full minus none 95% interval upper | 7.2568018302234 | percentage_points |
| R80 | Fine PBMC B100 full minus diagonal mean change | 3.36875000000001 | percentage_points |
| R81 | Fine PBMC B100 full minus diagonal 95% interval lower | 3.05601797788144 | percentage_points |
| R82 | Fine PBMC B100 full minus diagonal 95% interval upper | 3.68148202211858 | percentage_points |
| R83 | Prespecified coarse PBMC B10 full minus none | -1.5625 | percentage_points |
| R84 | Prespecified coarse PBMC B10 allowed harm magnitude | 1.5 | percentage_points |
| R85 | Prespecified coarse PBMC B10 within-network operator contribution | -0.937500000000002 | percentage_points |
| R86 | Prespecified coarse PBMC B10 approximately 80% interval lower | -3.54166666666667 | percentage_points |
| R87 | Prespecified coarse PBMC B10 approximately 80% interval upper | -0.416666666666671 | percentage_points |
| R88 | Learnable-only proxy mean gain | 1.9522613295976 | percentage_points |
| R89 | Learnable-only proxy task-stream r42 gain | 1.63330444701914 | percentage_points |
| R90 | Learnable-only proxy task-stream r43 gain | 1.61754491940739 | percentage_points |
| R91 | Learnable-only proxy task-stream r44 gain | 2.60593462236628 | percentage_points |
| R92 | Learnable-only proxy keep threshold | 1.62926207419837 | percentage_points |
| R93 | Learnable-only proxy effective control band | 1.08617471613225 | percentage_points |
| R94 | Prior-screen candidate count | 10 | candidate_arms |
| R95 | A5 proxy deciding-metric mean change | -1.37004511042547 | percentage_points |
| R96 | A6 proxy deciding-metric mean change | 0.572032798396781 | percentage_points |
| R97 | A7 proxy deciding-metric mean change | 0.197813477356007 | percentage_points |
| R98 | A8a proxy deciding-metric mean change | 0.900222938522968 | percentage_points |
| R99 | A8d proxy deciding-metric mean change | 0.349034416372528 | percentage_points |
| R100 | A8a Tier B NLL increase | 0.0987640218512889 | nats |
| R101 | A8a allowed Tier B NLL increase | 0.03 | nats |
| R102 | Learnable minus standard pbmc_l1 B1 balanced_accuracy mean change | 1.109375 | percentage_points |
| R103 | Learnable minus standard pbmc_l1 B1 balanced_accuracy 95% interval lower | 0.451058705298875 | percentage_points |
| R104 | Learnable minus standard pbmc_l1 B1 balanced_accuracy 95% interval upper | 1.76769129470113 | percentage_points |
| R105 | Learnable minus standard pbmc_l2 B1 balanced_accuracy mean change | 2.41875 | percentage_points |
| R106 | Learnable minus standard pbmc_l2 B1 balanced_accuracy 95% interval lower | 1.61229689926431 | percentage_points |
| R107 | Learnable minus standard pbmc_l2 B1 balanced_accuracy 95% interval upper | 3.22520310073569 | percentage_points |
| R108 | Learnable minus standard zebra_dev B1 balanced_accuracy mean change | 2.56331320534217 | percentage_points |
| R109 | Learnable minus standard zebra_dev B1 balanced_accuracy 95% interval lower | 1.10720058881742 | percentage_points |
| R110 | Learnable minus standard zebra_dev B1 balanced_accuracy 95% interval upper | 4.01942582186693 | percentage_points |
| R111 | Learnable minus standard zebra_ood B1 balanced_accuracy mean change | 3.49185741473446 | percentage_points |
| R112 | Learnable minus standard zebra_ood B1 balanced_accuracy 95% interval lower | 1.72744786785308 | percentage_points |
| R113 | Learnable minus standard zebra_ood B1 balanced_accuracy 95% interval upper | 5.25626696161585 | percentage_points |
| R114 | Learnable minus standard pbmc_l1 B100 nll mean change | 0.374003236651882 | nats |
| R115 | Learnable minus standard pbmc_l1 B100 nll 95% interval lower | 0.356963046604147 | nats |
| R116 | Learnable minus standard pbmc_l1 B100 nll 95% interval upper | 0.391043426699617 | nats |
| R117 | Learnable minus standard pbmc_l2 B100 nll mean change | -0.0465294079495327 | nats |
| R118 | Learnable minus standard pbmc_l2 B100 nll 95% interval lower | -0.0512044220345322 | nats |
| R119 | Learnable minus standard pbmc_l2 B100 nll 95% interval upper | -0.0418543938645332 | nats |
| R120 | Learnable minus standard zebra_dev B100 nll mean change | 0.628998024267668 | nats |
| R121 | Learnable minus standard zebra_dev B100 nll 95% interval lower | 0.606312825714543 | nats |
| R122 | Learnable minus standard zebra_dev B100 nll 95% interval upper | 0.651683222820793 | nats |
| R123 | Learnable minus standard zebra_ood B100 nll mean change | 0.345747937820128 | nats |
| R124 | Learnable minus standard zebra_ood B100 nll 95% interval lower | 0.30374262261119 | nats |
| R125 | Learnable minus standard zebra_ood B100 nll 95% interval upper | 0.387753253029067 | nats |
| R126 | Reported GL1 to GS1 cells-per-update ratio | 1.671 | ratio |
| R127 | cellpfn_gl1 realized mean cells per update | 2667.8 | cells_per_update |
| R128 | cellpfn_gs1 realized mean cells per update | 1596.6 | cells_per_update |
| R129 | Strongest class marker syn_q50 | 6.23214627652566 | log2_fold_change |
| R130 | Strongest class marker real_q50 | 7.10045142637156 | log2_fold_change |
| R131 | Strongest class marker syn_q05 | 4.27257730296515 | log2_fold_change |
| R132 | Strongest class marker syn_q95 | 10.2245361716548 | log2_fold_change |
| R133 | Strongest class marker real_min | 3.30958651185475 | log2_fold_change |
| R134 | Strongest class marker real_max | 9.761561951626 | log2_fold_change |
| R135 | Strongest class marker syn_n_units | 2688 | units |
| R136 | Strongest class marker syn_n_banks | 96 | banks |
| R137 | Strongest class marker real_n_units | 142 | units |
| R138 | Eight-class B10 nearest-centroid separability syn_q50 | 0.880714285714286 | chance_adjusted_BA_0_1 |
| R139 | Eight-class B10 nearest-centroid separability real_q50 | 0.774642857142857 | chance_adjusted_BA_0_1 |
| R140 | Eight-class B10 nearest-centroid separability syn_share_above_real_max | 0.375 | proportion |
| R141 | Eight-class B10 nearest-centroid separability syn_n_units | 96 | units |
| R142 | Eight-class B10 nearest-centroid separability syn_n_banks | 96 | banks |
| R143 | Eight-class B10 nearest-centroid separability real_n_units | 8 | units |
| R144 | Within-study donor variation syn_q50 | 0.404312094658779 | log2_SD |
| R145 | Within-study donor variation real_q50 | 0.289888444177179 | log2_SD |
| R146 | Within-study donor variation syn_q05 | 0.291280016011101 | log2_SD |
| R147 | Within-study donor variation syn_q95 | 0.527806829882107 | log2_SD |
| R148 | Within-study donor variation real_min | 0.197490067208954 | log2_SD |
| R149 | Within-study donor variation real_max | 0.39093750606097 | log2_SD |
| R150 | Within-study donor variation syn_n_units | 1024 | units |
| R151 | Within-study donor variation syn_n_banks | 128 | banks |
| R152 | Within-study donor variation real_n_units | 11 | units |
| R153 | Prior v1 strongest marker median | 1.93581285450791 | log2_fold_change |
| R154 | Class top20 overlap across support configurations min | 0.43125 | fraction_overlap |
| R155 | Class top20 overlap across support configurations max | 0.5625 | fraction_overlap |
| R156 | Class top20 overlap across same-budget support draws min | 0.43125 | fraction_overlap |
| R157 | Class top20 overlap across same-budget support draws max | 0.51875 | fraction_overlap |
| R158 | Kumo small cellular task-stream 43 low-support gain | 5.72843827910035 | percentage_points |
| R159 | Kumo small cellular task-stream 44 low-support gain | 5.17216444302734 | percentage_points |

Each numerical record includes explicit source file, exact filters, operation, selection count and interpretation caveats. Successful extraction checks validate transcription and arithmetic, not experimental design or external scientific validity.

## Independent main-Results transcription check

All new main-text comparisons were checked against the export and ledger. Two corrections were returned to the writer: the task-mixture B100 NLL-worsening range starts at 0.35, not 0.37, and the 70.9% to 64.0% generic-retention comparison must be labelled balanced accuracy. The frozen operator comparison is full minus no-operator (−1.5625 points); the additional within-network operator-off contribution is −0.9375 points, satisfying the attributable-harm clause. The two additional Kumo task streams are ledgered as R158–R159. This is a source-transcription and interpretation pass, not a new statistical-validity analysis.
