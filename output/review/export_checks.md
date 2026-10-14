<!-- Recomputed from a temporary copy; original export unchanged. Internal reconciliation only. -->
# Checks: every "number to check" recomputed from the exported data

Written by `build/assemble/check_all.py`. The script reads only the files under `data/` and
`checks/expected.csv`; it recomputes each value with the file, filter and aggregation that `FIGURES.md` names
and compares it with the expected value. Run it again on any machine with python 3, pandas and numpy:

    python build/assemble/check_all.py

It ends with exit code 1 if a value differs.

- Checks: **1375**. Mismatches: **0**.
- Tolerance: 0.0001 for numbers (the expected values are stored with 4 decimals), 0 for counts, exact for text.
- `checks/expected.csv` was written by the same script (`--freeze`) on 2026-10-11 from the harmonised data, after
  the values had been compared with the builders' numbers, and frozen again after the final pass (what changed between
  the two is listed in `CHANGELOG.md` and in `checks/expected_changes_final_pass.csv`). The column "in builder text" says whether the value,
  rounded as printed, stands in the builder's own figure concept (`sections/<block>.md`), which that builder's
  script computed before the ids were harmonised: `yes` is an independent confirmation, `-` means the value is not
  printed there in this form (a count, a text value, an interval end, or a check added by the assembler).
- How each exported number compares with the SOURCE REPORTS on the server is in `checks/<block>.md`
  (written by the builders, who could read the reports; 0 unexplained differences).
- ROSMAP values are NOT FINAL (label fixes pending). Hard-class-tier values are POST HOC and from the final read-out of the tier.
- The section "final pass" holds the checks added on 2026-10-11 for the corrections of `CHANGELOG.md` (ids `final.*`).
- The section "A8d refresh" holds the checks added in the evening of 2026-10-11, when arm A8d was read with three replicates
  (ids `refresh_a8d.*`). The expected values were frozen once more for it: three changed (`supp_prior_ablation.A8d.r43`, `.mean`,
  `.label`), the new ids were added, every other value is unchanged (`checks/expected_changes_a8d_refresh.csv`; the freeze before
  it is `checks/expected_before_a8d_refresh.csv`). In a second step of the refresh the two supp_stored_zeros files that name A8d
  were rebuilt and the values frozen again: one value changed (`cross.a8_gap_cases_vs_proxy_gap_cases.n_common_cases`), the two ids
  `refresh_a8d.not_rebuilt.*` gave way to `refresh_a8d.stored_zeros.*`, every other value is unchanged
  (`checks/expected_changes_a8d_refresh_2.csv`; the freeze before it is `checks/expected_before_a8d_refresh_2.csv`).
- The checks of the operator-arm refresh (2026-10-13, after the variance-only arm D1v2' was scored) are in the section fig6
  (ids `fig6.operator.d1v2p.*`, `.vn.*`, `.fv.*`, `.readings.*`, `.level.d1v2p.*`). The expected values were frozen once more for it:
  one changed (`fig6.operator.pending_rows`, 180 to 0), 234 were added, every other value is unchanged
  (`checks/expected_changes_operator_arm.csv`; the freeze before it is `checks/expected_before_operator_arm.csv`).
- The section "cross-block agreement" compares quantities that two builders exported independently.

## fig1

14 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig1.params_g1v2p` | 12329889 | 12329889 | 0.000000 | ok | yes | fig1__architecture_modules.csv: sum of parameter_count over the modules (row TOTAL left out) |
| `fig1.params_operator` | 404544 | 404544 | 0.000000 | ok | yes | fig1__facts.csv: key operator.learned_parameters |
| `fig1.params_operator_from_modules` | 404544 | 404544 | 0.000000 | ok | yes | fig1__architecture_modules.csv: lcs_pair_head + the 448 extra_stem parameters listed under relation_mlp |
| `fig1.params_c1v2p` | 11925345 | 11925345 | 0.000000 | ok | yes | fig1__lineage.csv: parameter_count of cellpfn_c1v2p (R10K has the same) |
| `fig1.params_per_gene_networks` | 130400 | 130400 | 0.000000 | ok | yes | fig1__architecture_modules.csv: relation_mlp + support_gene_mlp |
| `fig1.tasks_g1v2p` | 384000 | 384000 | 0.000000 | ok | yes | fig1__lineage.csv: tasks_scheduled of cellpfn_g1v2p |
| `fig1.share_tasks_v22b_pct` | 16.6667 | 16.6667 | 0.000000 | ok | yes | fig1__facts.csv: key lineage.share_of_tasks_on_v22B_at_96000 |
| `fig1.gs1_metadata_share_pct` | 80.1000 | 80.1000 | 0.000000 | ok | yes | fig1__training_stream.csv: stream_id gs1_window, dimension task_family, family all: (metadata_binary + metadata_categorical) / 16,000 |
| `fig1.gate_values` | B1 0; B10 0.6923; B100 0.9612 | B1 0; B10 0.6923; B100 0.9612 |  | ok | yes | fig1__facts.csv: key operator.gate_values |
| `fig1.gate_b10_formula` | 0.6923 | 0.6923 | 0.000008 | ok | yes | formula of key operator.gate_formula at 10 cells per class |
| `fig1.gate_b100_formula` | 0.9612 | 0.9612 | -0.000035 | ok | yes | formula of key operator.gate_formula at 100 cells per class |
| `fig1.count_mode_share_pct` | 70.0000 | 70.0000 | 0.000000 | ok | yes | fig1__facts.csv: key input.count_task_share |
| `fig1.gl1_cell_type_tasks` | 12001 | 12001 | 0.000000 | ok | yes | fig1__training_stream.csv: gl1_window, task_family, cell_type |
| `fig1.n_facts` | 236 | 236 | 0.000000 | ok | - | fig1__facts.csv: rows |

## fig2

68 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig2.mean12.cellpfn_g1v2p.hvg2000.draws0_2` | 71.1652 | 71.1652 | 0.000030 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.hvg8192.draws0_2` | 73.8091 | 73.8091 | -0.000021 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.all.draws0_2` | 72.9456 | 72.9456 | 0.000048 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_l40k.hvg2000.draws0_2` | 72.4208 | 72.4208 | -0.000026 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_l40k.hvg8192.draws0_2` | 72.0478 | 72.0478 | -0.000039 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_l40k.all.draws0_2` | 70.3656 | 70.3656 | 0.000017 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_large.hvg2000.draws0_2` | 70.1123 | 70.1123 | -0.000007 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_large.hvg8192.draws0_2` | 67.9781 | 67.9781 | -0.000033 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_large.all.draws0_2` | 66.3558 | 66.3558 | 0.000049 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.tabicl_v2.hvg2000.draws0_2` | 66.8313 | 66.8313 | -0.000047 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.tabicl_v2.hvg8192.draws0_2` | 56.8041 | 56.8041 | -0.000021 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.tabicl_v2.all.draws0_2` | 48.3065 | 48.3065 | -0.000015 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.c2b40k.hvg2000.draws0_2` | 69.3568 | 69.3568 | -0.000018 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.c2b40k.hvg8192.draws0_2` | 61.9926 | 61.9926 | -0.000027 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.c2b40k.all.draws0_2` | 55.3874 | 55.3874 | -0.000044 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_s40k.hvg2000.draws0_2` | 71.8006 | 71.8006 | -0.000036 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_s40k.hvg8192.draws0_2` | 69.7094 | 69.7094 | 0.000007 | ok | - | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.k2b_s40k.all.draws0_2` | 68.5264 | 68.5264 | 0.000027 | ok | - | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_small.hvg2000.draws0_2` | 67.8411 | 67.8411 | -0.000012 | ok | - | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_small.hvg8192.draws0_2` | 66.2462 | 66.2462 | -0.000022 | ok | - | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.kumo_small.all.draws0_2` | 64.7419 | 64.7419 | -0.000034 | ok | - | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.tabpfn35.hvg2000.draws0_2` | 67.0142 | 67.0142 | 0.000014 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.tabpfn35.hvg8192.draws0_2` | 65.9505 | 65.9505 | -0.000050 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, benchmark_draw == 1; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.hvg2000.draws0_19` | 72.4240 | 72.4240 | -0.000014 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, all 20 draws; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.hvg8192.draws0_19` | 74.0686 | 74.0686 | -0.000022 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, all 20 draws; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.all.draws0_19` | 73.6898 | 73.6898 | -0.000038 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, all 20 draws; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.rand2000.draws0_19` | 62.9475 | 62.9475 | 0.000045 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, all 20 draws; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.mean12.cellpfn_g1v2p.rand8192.draws0_19` | 69.3849 | 69.3849 | 0.000034 | ok | yes | fig2__cases.csv: metric balanced_accuracy, status ok, all 20 draws; mean over draws per panel x support size, then mean over the 12 result cells |
| `fig2.delta12_all_minus_hvg2000.cellpfn_g1v2p.draws0_2` | 1.7804 | 1.7804 | 0.000018 | ok | yes (1 decimal) | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.k2b_l40k.draws0_2` | -2.0552 | -2.0552 | 0.000043 | ok | yes (1 decimal) | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.kumo_large.draws0_2` | -3.7564 | -3.7564 | -0.000044 | ok | yes (1 decimal) | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.c2b40k.draws0_2` | -13.9694 | -13.9694 | -0.000026 | ok | yes | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.tabicl_v2.draws0_2` | -18.5248 | -18.5248 | 0.000032 | ok | yes | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.k2b_s40k.draws0_2` | -3.2741 | -3.2741 | -0.000037 | ok | yes (1 decimal) | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.kumo_small.draws0_2` | -3.0992 | -3.0992 | -0.000022 | ok | yes (1 decimal) | difference of the two 12-cell means (same draws, so equal to the mean paired change) |
| `fig2.delta12_all_minus_hvg2000.cellpfn_r10k.draws0_19` | 3.4553 | 3.4553 | -0.000048 | ok | yes (1 decimal) | as above with all 20 draws |
| `fig2.delta12_all_minus_hvg2000.cellpfn_c1v2p.draws0_19` | 0.4469 | 0.4469 | -0.000040 | ok | yes (1 decimal) | as above with all 20 draws |
| `fig2.delta12_all_minus_hvg2000.cellpfn_g1v2p.draws0_19` | 1.2658 | 1.2658 | -0.000024 | ok | yes (1 decimal) | as above with all 20 draws |
| `fig2.tabpfn35_all_refused_cases` | 36 | 36 | 0.000000 | ok | - | fig2__cases.csv: tabpfn35, gene_view all, one row per case: status refused |
| `fig2.tabpfn35_all_ok_cases` | 0 | 0 | 0.000000 | ok | - | same rows with status ok |
| `fig2.cell.cellpfn_g1v2p.zebra_ood.B10.hvg2000` | 80.9355 | 80.9355 | 0.000025 | ok | yes | cell mean, draws 0-2 |
| `fig2.cell.cellpfn_g1v2p.zebra_ood.B10.all` | 91.9195 | 91.9195 | -0.000036 | ok | yes | cell mean, draws 0-2 |
| `fig2.paired20.cellpfn_g1v2p.zebra_ood.B10.all_minus_hvg2000.mean` | 7.4145 | 7.4145 | -0.000004 | ok | yes (1 decimal) | 20 draws, paired by draw |
| `fig2.paired20.cellpfn_g1v2p.zebra_ood.B10.all_minus_hvg2000.ci_low` | 5.2637 | 5.2637 | 0.000008 | ok | yes (1 decimal) | 95% t interval over the 20 paired differences |
| `fig2.paired20.cellpfn_g1v2p.zebra_ood.B10.all_minus_hvg2000.ci_high` | 9.5653 | 9.5653 | -0.000015 | ok | yes (1 decimal) | 95% t interval over the 20 paired differences |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l1.B1.hvg2000_minus_all.mean` | 3.3125 | 3.3125 | 0.000000 | ok | yes (1 decimal) | 20 draws, paired by draw |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l1.B1.hvg2000_minus_all.ci_low` | 1.4243 | 1.4243 | 0.000023 | ok | yes (1 decimal) |  |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l1.B1.hvg2000_minus_all.ci_high` | 5.2007 | 5.2007 | -0.000023 | ok | yes (1 decimal) |  |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l2.B1.hvg2000_minus_all.mean` | 1.9562 | 1.9562 | 0.000050 | ok | yes (1 decimal) | 20 draws, paired by draw |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l2.B1.hvg2000_minus_all.ci_low` | 0.6453 | 0.6453 | 0.000021 | ok | yes (1 decimal) |  |
| `fig2.paired20.cellpfn_g1v2p.pbmc_l2.B1.hvg2000_minus_all.ci_high` | 3.2672 | 3.2672 | -0.000021 | ok | yes (1 decimal) |  |
| `fig2.cell.c2b40k.pbmc_l2.B10.hvg2000` | 64.6250 | 64.6250 | -0.000000 | ok | yes | cell mean, draws 0-2 |
| `fig2.cell.c2b40k.pbmc_l2.B10.all` | 13.6250 | 13.6250 | 0.000000 | ok | yes | cell mean, draws 0-2 |
| `fig2.cell.tabicl_v2.pbmc_l2.B100.hvg2000` | 83.6250 | 83.6250 | 0.000000 | ok | yes | cell mean, draws 0-2 |
| `fig2.cell.tabicl_v2.pbmc_l2.B100.all` | 29.8750 | 29.8750 | 0.000000 | ok | yes | cell mean, draws 0-2 |
| `fig2.rows_cases` | 12600 | 12600 | 0.000000 | ok | yes | fig2__cases.csv: rows |
| `fig2.model_means_file.cellpfn_g1v2p.all.draws0_2` | 72.9456 | 72.9456 | 0.000048 | ok | yes | fig2__model_means.csv: the same number from the derived file |
| `fig2.same_varying_set_cases` | 7 | 7 | 0.000000 | ok | - | fig2__varying_genes.csv: same_varying_set == 1 |
| `fig2.max_varying_genes_pbmc` | 19594 | 19594 | 0.000000 | ok | yes | fig2__varying_genes.csv: max n_varying_all on PBMC |
| `fig2.max_varying_genes_zebra` | 18235 | 18235 | 0.000000 | ok | yes | fig2__varying_genes.csv: max n_varying_all on Zebra |
| `fig2.nll.cellpfn_g1v2p.pbmc_l1.B1.hvg2000` | 1.1332 | 1.1332 | -0.000008 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.pbmc_l1.B1.all` | 1.4171 | 1.4171 | 0.000022 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.pbmc_l2.B1.hvg2000` | 1.5168 | 1.5168 | 0.000026 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.pbmc_l2.B1.all` | 2.0754 | 2.0754 | 0.000027 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.zebra_dev.B1.hvg2000` | 1.1250 | 1.1250 | -0.000031 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.zebra_dev.B1.all` | 1.2208 | 1.2208 | 0.000048 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.zebra_ood.B1.hvg2000` | 1.0194 | 1.0194 | -0.000003 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |
| `fig2.nll.cellpfn_g1v2p.zebra_ood.B1.all` | 1.1224 | 1.1224 | -0.000009 | ok | yes | fig2__cases.csv: metric nll, draws 0-2 |

## fig3

76 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig3.mean8.c2b5k` | 0.0749 | 0.0749 | 0.000008 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.c2b10k` | 3.0493 | 3.0493 | -0.000000 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.c2b20k` | 2.2018 | 2.2018 | -0.000027 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.c2b40k` | 3.4014 | 3.4014 | -0.000048 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.n_positive_of_8.c2b40k` | 6 | 6 | 0.000000 | ok | - | number of the 8 cells with a positive mean change |
| `fig3.mean8.k2b_s5k` | 3.7655 | 3.7655 | -0.000003 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_s10k` | 4.8412 | 4.8412 | 0.000034 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_s20k` | 5.1629 | 5.1629 | -0.000014 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_s40k` | 6.0522 | 6.0522 | -0.000006 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.n_positive_of_8.k2b_s40k` | 8 | 8 | 0.000000 | ok | - | number of the 8 cells with a positive mean change |
| `fig3.mean8.k2b_l5k` | 1.9542 | 1.9542 | -0.000040 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_l10k` | 2.9005 | 2.9005 | 0.000024 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_l20k` | 2.6365 | 2.6365 | -0.000048 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.k2b_l40k` | 3.3325 | 3.3325 | -0.000008 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run k2b_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.n_positive_of_8.k2b_l40k` | 7 | 7 | 0.000000 | ok | - | number of the 8 cells with a positive mean change |
| `fig3.mean8.p1_s43_40k` | 5.7284 | 5.7284 | 0.000038 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.p1_s44_40k` | 5.1722 | 5.1722 | -0.000036 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.p1_g40k` | -0.0469 | -0.0469 | 0.000029 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.p1_s43_10k` | 3.9203 | 3.9203 | 0.000035 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.p1_s44_10k` | 3.6988 | 3.6988 | 0.000009 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.p1_g10k` | -0.3551 | -0.3551 | 0.000024 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run p1_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.c2a40k` | 3.1682 | 3.1682 | 0.000032 | ok | - | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2a_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8.c2a_random40k` | -41.5834 | -41.5834 | -0.000008 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run c2a_root, low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.n_positive_of_8.c2a_random40k` | 0 | 0 | 0.000000 | ok | - |  |
| `fig3.mean8_10draws.k2b_s10k` | 3.4926 | 3.4926 | -0.000042 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run stage0_efast (10 draws), low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8_10draws.p1_s43_10k` | 2.7493 | 2.7493 | -0.000004 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run stage0_efast (10 draws), low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8_10draws.p1_s44_10k` | 2.4064 | 2.4064 | -0.000017 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run stage0_efast (10 draws), low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.mean8_10draws.p1_g10k` | -2.3761 | -2.3761 | 0.000047 | ok | yes | fig3__paired.csv: metric balanced_accuracy, gene_view hvg2000, scoring_run stage0_efast (10 draws), low_support_core_cell == 1; mean of delta over draws per cell, then over the 8 cells |
| `fig3.released_level_10draws.kumo_small` | 61.9632 | 61.9632 | 0.000042 | ok | yes | same rows, mean of value_base over the 8 cells |
| `fig3.delta_by_support.c2b40k.B1` | 7.2982 | 7.2982 | -0.000049 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.c2b40k.B10` | -0.4954 | -0.4954 | -0.000047 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.c2b40k.B100` | 0.7722 | 0.7722 | 0.000023 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_s40k.B1` | 10.7940 | 10.7940 | 0.000049 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_s40k.B10` | 1.3103 | 1.3103 | 0.000039 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_s40k.B100` | -0.2184 | -0.2184 | -0.000004 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_l40k.B1` | 5.5829 | 5.5829 | 0.000019 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_l40k.B10` | 1.0821 | 1.0821 | -0.000036 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.delta_by_support.k2b_l40k.B100` | 0.2605 | 0.2605 | -0.000039 | ok | yes | fig3__paired.csv as above without the low-support filter: mean over the four core panels at this support size |
| `fig3.pbmc_l1_B1.base.tabicl_v2` | 50.2083 | 50.2083 | 0.000033 | ok | yes | value_base, mean over draws 0-2 |
| `fig3.pbmc_l1_B1.finetune.c2b40k` | 62.2917 | 62.2917 | -0.000033 | ok | yes | value_finetune, mean over draws 0-2 |
| `fig3.pbmc_l1_B1.base.kumo_small` | 45.8333 | 45.8333 | 0.000033 | ok | yes | value_base, mean over draws 0-2 |
| `fig3.pbmc_l1_B1.finetune.k2b_s40k` | 62.8125 | 62.8125 | 0.000000 | ok | yes | value_finetune, mean over draws 0-2 |
| `fig3.pbmc_l1_B1.base.kumo_large` | 58.8542 | 58.8542 | -0.000033 | ok | yes | value_base, mean over draws 0-2 |
| `fig3.pbmc_l1_B1.finetune.k2b_l40k` | 62.1875 | 62.1875 | 0.000000 | ok | yes | value_finetune, mean over draws 0-2 |
| `fig3.c2b40k.pbmc_l2.B10.base` | 73.7500 | 73.7500 | 0.000000 | ok | yes | fig3__paired.csv: value_base |
| `fig3.c2b40k.pbmc_l2.B10.finetune` | 64.6250 | 64.6250 | 0.000000 | ok | yes | fig3__paired.csv: value_finetune |
| `fig3.c2b40k.pbmc_l2.B10.delta` | -9.1250 | -9.1250 | -0.000000 | ok | yes (1 decimal) | fig3__paired.csv: delta |
| `fig3.c2b40k.pbmc_l2.B10.draws_below_base` | 3 | 3 | 0.000000 | ok | - | number of the 3 draws with delta < 0 |
| `fig3.p1_g40k.pbmc_cells.min` | -6.7708 | -6.7708 | -0.000033 | ok | yes (1 decimal) | control G at 40K: smallest of the four PBMC low-support cells |
| `fig3.p1_g40k.pbmc_cells.max` | 0.0417 | 0.0417 | -0.000033 | ok | yes (1 decimal) | largest of the four |
| `fig3.p1_g40k.zebra_dev.B1` | 4.5678 | 4.5678 | 0.000041 | ok | yes (1 decimal) | control G at 40K |
| `fig3.p1_g40k.zebra_ood.B1` | 3.5912 | 3.5912 | -0.000004 | ok | yes (1 decimal) | control G at 40K |
| `fig3.trajectory_file.k2b_s40k.mean8` | 6.0522 | 6.0522 | -0.000006 | ok | yes | fig3__trajectory.csv: the same number from the derived file |
| `fig3.mean8_nll.k2b_s40k` | -0.2175 | -0.2175 | 0.000034 | ok | yes | fig3__trajectory.csv: mean_delta_NLL_8_low_support_cells |
| `fig3.mean8_nll.k2b_l40k` | -0.2375 | -0.2375 | 0.000008 | ok | yes | fig3__trajectory.csv: mean_delta_NLL_8_low_support_cells |
| `fig3.mean8_nll.c2b40k` | -0.0699 | -0.0699 | 0.000011 | ok | yes | fig3__trajectory.csv: mean_delta_NLL_8_low_support_cells |
| `fig3.mean8_nll.c2a40k` | 0.0904 | 0.0904 | -0.000031 | ok | yes | fig3__trajectory.csv: mean_delta_NLL_8_low_support_cells |
| `fig3.mean8_wide_view.c2b40k.hvg8192` | 7.4934 | 7.4934 | 0.000046 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.mean8_wide_view.c2b40k.all` | 7.4448 | 7.4448 | -0.000048 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.mean8_wide_view.k2b_s40k.hvg8192` | 5.3852 | 5.3852 | 0.000012 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.mean8_wide_view.k2b_s40k.all` | 5.7773 | 5.7773 | 0.000029 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.mean8_wide_view.k2b_l40k.hvg8192` | 5.9820 | 5.9820 | 0.000041 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.mean8_wide_view.k2b_l40k.all` | 5.7419 | 5.7419 | -0.000024 | ok | yes (1 decimal) | fig3__trajectory.csv: scoring_run diag_1d |
| `fig3.gpu_hours.c2b40k` | 5.3800 | 5.3800 | 0.000000 | ok | yes | fig3__finetune_cost.csv: gpu_hours_compute_cumulative |
| `fig3.gpu_hours.k2b_s40k` | 2.8800 | 2.8800 | 0.000000 | ok | yes | fig3__finetune_cost.csv: gpu_hours_compute_cumulative |
| `fig3.hours_waiting.k2b_s40k` | 3.5400 | 3.5400 | 0.000000 | ok | yes | fig3__finetune_cost.csv: hours_waiting_for_gpu_lock_cumulative |
| `fig3.gpu_hours.k2b_l40k` | 5.1500 | 5.1500 | 0.000000 | ok | yes | fig3__finetune_cost.csv: gpu_hours_compute_cumulative |
| `fig3.hours_waiting.k2b_l40k` | 10.1700 | 10.1700 | 0.000000 | ok | yes | fig3__finetune_cost.csv: hours_waiting_for_gpu_lock_cumulative |
| `fig3.gpu_hours.c2a40k` | 5.3200 | 5.3200 | 0.000000 | ok | yes (1 decimal) | fig3__finetune_cost.csv: gpu_hours_compute_cumulative |
| `fig3.generic_tables.tabicl_v2.B1` | 70.9186 | 70.9186 | -0.000000 | ok | yes | fig3__generic_tables_cases.csv: metric balanced_accuracy, support_budget B1; mean over tables and split seeds |
| `fig3.generic_tables.tabicl_v2.all_budgets` | 87.7693 | 87.7693 | 0.000005 | ok | yes | same, all support budgets |
| `fig3.generic_tables.c2b40k.B1` | 63.9658 | 63.9658 | -0.000040 | ok | yes | fig3__generic_tables_cases.csv: metric balanced_accuracy, support_budget B1; mean over tables and split seeds |
| `fig3.generic_tables.c2b40k.all_budgets` | 84.8405 | 84.8405 | 0.000045 | ok | yes | same, all support budgets |
| `fig3.rows_cases` | 15744 | 15744 | 0.000000 | ok | yes | fig3__cases.csv: rows |
| `fig3.rows_paired` | 11952 | 11952 | 0.000000 | ok | yes | fig3__paired.csv: rows |
| `fig3.stream.cell_type_tasks` | 5993 | 5993 | 0.000000 | ok | yes | fig3__training_stream.csv: n_tasks of level cell_type |

## fig4

147 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig4.cell.cellpfn.pbmc_l1.B1` | 60.1042 | 60.1042 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.pbmc_l1.B10` | 83.9583 | 83.9583 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.pbmc_l1.B100` | 91.8750 | 91.8750 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.pbmc_l2.B1` | 51.0833 | 51.0833 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.pbmc_l2.B10` | 78.9583 | 78.9583 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.pbmc_l2.B100` | 88.9583 | 88.9583 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_dev.B1` | 41.3626 | 41.3626 | 0.000008 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_dev.B10` | 63.5848 | 63.5848 | -0.000026 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_dev.B100` | 66.0501 | 66.0501 | -0.000041 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_ood.B1` | 62.8365 | 62.8365 | -0.000049 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_ood.B10` | 91.9195 | 91.9195 | -0.000036 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.cellpfn.zebra_ood.B100` | 94.6569 | 94.6569 | 0.000023 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.cellpfn` | 72.9456 | 72.9456 | 0.000048 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.geneformer.pbmc_l1.B1` | 67.0833 | 67.0833 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.pbmc_l1.B10` | 88.5417 | 88.5417 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.pbmc_l1.B100` | 92.7083 | 92.7083 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.pbmc_l2.B1` | 68.8333 | 68.8333 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.pbmc_l2.B10` | 84.8750 | 84.8750 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.pbmc_l2.B100` | 90.3750 | 90.3750 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_dev.B1` | 43.1491 | 43.1491 | -0.000025 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_dev.B10` | 61.0840 | 61.0840 | -0.000022 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_dev.B100` | 65.4138 | 65.4138 | -0.000025 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_ood.B1` | 58.4429 | 58.4429 | 0.000013 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_ood.B10` | 87.4485 | 87.4485 | 0.000030 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.geneformer.zebra_ood.B100` | 90.2866 | 90.2866 | 0.000031 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.geneformer` | 74.8535 | 74.8535 | -0.000036 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.scgpt.pbmc_l1.B1` | 64.8958 | 64.8958 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.pbmc_l1.B10` | 77.5000 | 77.5000 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.pbmc_l1.B100` | 80.7292 | 80.7292 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.pbmc_l2.B1` | 55.7083 | 55.7083 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.pbmc_l2.B10` | 65.8750 | 65.8750 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.pbmc_l2.B100` | 72.0000 | 72.0000 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_dev.B1` | 47.5822 | 47.5822 | 0.000026 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_dev.B10` | 60.2069 | 60.2069 | -0.000049 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_dev.B100` | 65.8122 | 65.8122 | 0.000002 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_ood.B1` | 65.5377 | 65.5377 | 0.000044 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_ood.B10` | 87.1643 | 87.1643 | 0.000049 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.scgpt.zebra_ood.B100` | 89.4819 | 89.4819 | -0.000041 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.scgpt` | 69.3745 | 69.3745 | -0.000036 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.kumo_finetune.pbmc_l1.B1` | 62.1875 | 62.1875 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.pbmc_l1.B10` | 82.5000 | 82.5000 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.pbmc_l1.B100` | 92.8125 | 92.8125 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.pbmc_l2.B1` | 50.8750 | 50.8750 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.pbmc_l2.B10` | 82.1667 | 82.1667 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.pbmc_l2.B100` | 89.2083 | 89.2083 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_dev.B1` | 42.8311 | 42.8311 | 0.000012 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_dev.B10` | 60.5982 | 60.5982 | -0.000032 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_dev.B100` | 65.8064 | 65.8064 | 0.000023 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_ood.B1` | 60.7649 | 60.7649 | -0.000024 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_ood.B10` | 85.8729 | 85.8729 | 0.000015 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo_finetune.zebra_ood.B100` | 93.4258 | 93.4258 | -0.000001 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.kumo_finetune` | 72.4208 | 72.4208 | -0.000025 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.tabicl_finetune.pbmc_l1.B1` | 62.2917 | 62.2917 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.pbmc_l1.B10` | 85.2083 | 85.2083 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.pbmc_l1.B100` | 93.4375 | 93.4375 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.pbmc_l2.B1` | 29.0833 | 29.0833 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.pbmc_l2.B10` | 64.6250 | 64.6250 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.pbmc_l2.B100` | 85.3333 | 85.3333 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_dev.B1` | 44.5550 | 44.5550 | 0.000002 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_dev.B10` | 60.6392 | 60.6392 | 0.000017 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_dev.B100` | 65.3182 | 65.3182 | -0.000050 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_ood.B1` | 62.7491 | 62.7491 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_ood.B10` | 85.8155 | 85.8155 | 0.000050 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl_finetune.zebra_ood.B100` | 93.2252 | 93.2252 | 0.000030 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.tabicl_finetune` | 69.3568 | 69.3568 | -0.000018 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.kumo.pbmc_l1.B1` | 58.8542 | 58.8542 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.pbmc_l1.B10` | 81.6667 | 81.6667 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.pbmc_l1.B100` | 92.8125 | 92.8125 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.pbmc_l2.B1` | 46.2917 | 46.2917 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.pbmc_l2.B10` | 83.2500 | 83.2500 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.pbmc_l2.B100` | 89.2500 | 89.2500 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_dev.B1` | 40.1268 | 40.1268 | -0.000027 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_dev.B10` | 56.8031 | 56.8031 | -0.000022 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_dev.B100` | 65.0893 | 65.0893 | 0.000024 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_ood.B1` | 49.0542 | 49.0542 | 0.000005 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_ood.B10` | 85.0897 | 85.0897 | 0.000048 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.kumo.zebra_ood.B100` | 93.0594 | 93.0594 | -0.000014 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.kumo` | 70.1123 | 70.1123 | -0.000007 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.tabicl.pbmc_l1.B1` | 50.2083 | 50.2083 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.pbmc_l1.B10` | 81.3542 | 81.3542 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.pbmc_l1.B100` | 92.3958 | 92.3958 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.pbmc_l2.B1` | 30.0000 | 30.0000 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.pbmc_l2.B10` | 73.7500 | 73.7500 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.pbmc_l2.B100` | 83.6250 | 83.6250 | 0.000000 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_dev.B1` | 39.5055 | 39.5055 | 0.000025 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_dev.B10` | 59.9189 | 59.9189 | 0.000045 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_dev.B100` | 65.2632 | 65.2632 | 0.000007 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_ood.B1` | 49.7726 | 49.7726 | 0.000006 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_ood.B10` | 83.2468 | 83.2468 | -0.000025 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabicl.zebra_ood.B100` | 92.9346 | 92.9346 | 0.000047 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.tabicl` | 66.8313 | 66.8313 | -0.000047 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.cell.tabpfn.pbmc_l1.B1` | 34.2708 | 34.2708 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.pbmc_l1.B10` | 82.6042 | 82.6042 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.pbmc_l1.B100` | 91.4583 | 91.4583 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.pbmc_l2.B1` | 33.0417 | 33.0417 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.pbmc_l2.B10` | 79.3333 | 79.3333 | 0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.pbmc_l2.B100` | 86.9167 | 86.9167 | -0.000033 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_dev.B1` | 38.4074 | 38.4074 | 0.000040 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_dev.B10` | 59.3154 | 59.3154 | -0.000023 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_dev.B100` | 65.5007 | 65.5007 | -0.000046 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_ood.B1` | 54.0985 | 54.0985 | 0.000017 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_ood.B10` | 85.3016 | 85.3016 | 0.000001 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.cell.tabpfn.zebra_ood.B100` | 93.9220 | 93.9220 | -0.000020 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws |
| `fig4.mean12.tabpfn` | 67.0142 | 67.0142 | 0.000014 | ok | yes | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; metric balanced_accuracy, status ok; mean over the 3 draws; mean of the 12 cells |
| `fig4.paired.g1v2p_minus_geneformer_lr.pbmc.mean` | -6.2465 | -6.2465 | -0.000028 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|count minus geneformer_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_minus_geneformer_lr.pbmc.n_higher` | 0 | 0 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_minus_geneformer_lr.pbmc.n_lower` | 17 | 17 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_minus_geneformer_lr.pbmc.n_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `fig4.paired.g1v2p_minus_geneformer_lr.zebra.mean` | 2.4309 | 2.4309 | -0.000004 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|processed minus geneformer_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_minus_geneformer_lr.zebra.n_higher` | 13 | 13 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_minus_geneformer_lr.zebra.n_lower` | 5 | 5 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_minus_geneformer_lr.zebra.n_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.zebra_counts.mean` | 4.2932 | 4.2932 | 0.000001 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|count minus geneformer_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.zebra_counts.n_higher` | 13 | 13 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.zebra_counts.n_lower` | 5 | 5 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.zebra_counts.n_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.kidney.mean` | -1.2500 | -1.2500 | 0.000000 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|count minus geneformer_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.kidney.n_higher` | 2 | 2 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.kidney.n_lower` | 10 | 10 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_count_minus_geneformer_lr.kidney.n_cases` | 12 | 12 | 0.000000 | ok | - | cases compared |
| `fig4.paired.g1v2p_minus_scgpt_lr.pbmc.mean` | 6.3715 | 6.3715 | 0.000028 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|count minus scgpt_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_minus_scgpt_lr.pbmc.n_higher` | 12 | 12 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_minus_scgpt_lr.pbmc.n_lower` | 6 | 6 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_minus_scgpt_lr.pbmc.n_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `fig4.paired.g1v2p_minus_scgpt_lr.zebra.mean` | 0.7708 | 0.7708 | 0.000041 | ok | yes (1 decimal) | fig4__cases.csv: series cellpfn_g1v2p\|all\|processed minus scgpt_lr\|own_input\|own on identical cases (panel, support size, draw); mean |
| `fig4.paired.g1v2p_minus_scgpt_lr.zebra.n_higher` | 12 | 12 | 0.000000 | ok | - | cases with a positive difference |
| `fig4.paired.g1v2p_minus_scgpt_lr.zebra.n_lower` | 6 | 6 | 0.000000 | ok | - | cases with a negative difference |
| `fig4.paired.g1v2p_minus_scgpt_lr.zebra.n_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `fig4.singler_series` | singler\|all\|own | singler\|all\|own |  | ok | - | series ids of SingleR in fig4__cases.csv |
| `fig4.paired.g1v2p_minus_singler.pbmc.mean` | 6.0243 | 6.0243 | 0.000006 | ok | yes (1 decimal) | as above for SingleR (singler\|all\|own) |
| `fig4.paired.g1v2p_minus_singler.pbmc.n_higher` | 17 | 17 | 0.000000 | ok | - |  |
| `fig4.paired.g1v2p_minus_singler.pbmc.n_lower` | 1 | 1 | 0.000000 | ok | - |  |
| `fig4.g1v2p.zebra_dev.B1.processed_panel` | 41.3626 | 41.3626 | 0.000008 | ok | yes | series cellpfn_g1v2p\|all\|processed on zebra_dev |
| `fig4.g1v2p.zebra_counts_dev.B1.processed_mode` | 47.1166 | 47.1166 | -0.000004 | ok | yes | series cellpfn_g1v2p\|all\|processed on zebra_counts_dev |
| `fig4.g1v2p.zebra_counts_dev.B1.count_mode` | 51.4218 | 51.4218 | -0.000039 | ok | yes | series cellpfn_g1v2p\|all\|count on zebra_counts_dev |
| `fig4.g1v2p.zebra_dev.B1.draw_min` | 33.0810 | 33.0810 | -0.000045 | ok | yes | smallest of the 3 draws |
| `fig4.g1v2p.zebra_dev.B1.draw_max` | 47.3722 | 47.3722 | -0.000021 | ok | yes | largest of the 3 draws |
| `fig4.limit_rows` | 36 | 36 | 0.000000 | ok | - | fig4__cases.csv: rows with status limit |
| `fig4.limit_models` | scanvi_inductive;scanvi_transductive | scanvi_inductive;scanvi_transductive |  | ok | - | models of these rows |
| `fig4.limit_panels` | zebra_dev;zebra_ood | zebra_dev;zebra_ood |  | ok | - | panels of these rows |
| `fig4.kidney_main_series.min` | 94.0000 | 94.0000 | 0.000000 | ok | yes | kidney cell-type panels, the 8 main series: smallest cell mean |
| `fig4.kidney_main_series.max` | 98.2407 | 98.2407 | 0.000041 | ok | yes | largest cell mean |
| `fig4.n_series` | 84 | 84 | 0.000000 | ok | - | fig4__cases.csv: distinct series_id |
| `fig4.n_models_cases` | 62 | 62 | 0.000000 | ok | - | fig4__cases.csv: distinct model_id |
| `fig4.rows_cases` | 12890 | 12890 | 0.000000 | ok | - | fig4__cases.csv: rows |
| `fig4.best_per_family.scgpt_ncm_mean12` | 69.3835 | 69.3835 | -0.000033 | ok | yes | fig4__best_per_family.csv: mean_ba_pct_own_input |
| `fig4.best_per_family.scgpt_lr_mean12` | 69.3745 | 69.3745 | -0.000033 | ok | yes | fig4__best_per_family.csv: mean_ba_pct_own_input |

## fig5

85 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig5.scatter.n_points` | 20365 | 20365 | 0.000000 | ok | yes | fig5__ko_pairs_by_cell__pbmc.csv: case_id pbmc_l1_b100_s0, model_id cellpfn_g1v2p; rows |
| `fig5.scatter.n_points_without_dsloo_extra` | 18740 | 18740 | 0.000000 | ok | yes | same, gene_set != dsloo_extra |
| `fig5.scatter.n_cells` | 191 | 191 | 0.000000 | ok | - | distinct cells |
| `fig5.scatter.pearson_r` | 0.9998 | 0.9998 | 0.000008 | ok | yes | Pearson r of dsloo_corr_margin against exact_ko_margin over all points |
| `fig5.scatter.rel_l2_error_pct` | 1.9268 | 1.9268 | 0.000015 | ok | yes (1 decimal) | norm(estimate - exact) / norm(exact) over all points, in percent |
| `fig5.scatter.share_abs_exact_le_1e-4_pct` | 34.3973 | 34.3973 | -0.000050 | ok | - | share of points with abs(exact_ko_margin) <= 1e-4 |
| `fig5.scatter.share_negative_pct` | 29.3690 | 29.3690 | 0.000015 | ok | - | share of points with exact_ko_margin < -1e-4 |
| `fig5.scatter.exact_min` | -1.5152 | -1.5152 | 0.000000 | ok | yes | smallest exact_ko_margin |
| `fig5.scatter.exact_max` | 2.2475 | 2.2475 | 0.000000 | ok | yes | largest exact_ko_margin |
| `fig5.rho_cell.dsloo_corr.min` | 0.9793 | 0.9793 | 0.000001 | ok | yes | fig5__fidelity_by_case.csv: source_column rho_cell_q, method_id dsloo_corr_margin; smallest of the 12 case x model values |
| `fig5.rho_cell.dsloo_corr.max` | 0.9979 | 0.9979 | 0.000008 | ok | yes | largest of the 12 |
| `fig5.rho_cell.dsloo_corr.reference_case` | 0.9976 | 0.9976 | -0.000018 | ok | yes | reference case, G1v2' |
| `fig5.rho_cell.operator_readout.g1v2p.min` | 0.7892 | 0.7892 | 0.000034 | ok | yes | rho_cell_q of op_ko_margin, cellpfn_g1v2p: smallest over the 6 cases |
| `fig5.rho_cell.operator_readout.g1v2p.max` | 0.9113 | 0.9113 | 0.000000 | ok | yes | largest over the 6 cases |
| `fig5.rho_cell.operator_readout.c1v2p.min` | 0.6882 | 0.6882 | -0.000049 | ok | yes | rho_cell_q of op_ko_margin, cellpfn_c1v2p: smallest over the 6 cases |
| `fig5.rho_cell.operator_readout.c1v2p.max` | 0.8404 | 0.8404 | 0.000026 | ok | - | largest over the 6 cases |
| `fig5.rho_cell.gxi.g1v2p.min` | 0.7701 | 0.7701 | 0.000007 | ok | yes | rho_cell_q of gxi_margin, cellpfn_g1v2p: smallest over the 6 cases |
| `fig5.rho_cell.gxi.g1v2p.max` | 0.8883 | 0.8883 | -0.000045 | ok | yes | largest over the 6 cases |
| `fig5.rho_cell.gxi.c1v2p.min` | 0.4080 | 0.4080 | -0.000028 | ok | yes | rho_cell_q of gxi_margin, cellpfn_c1v2p: smallest over the 6 cases |
| `fig5.rho_cell.gxi.c1v2p.max` | 0.7415 | 0.7415 | 0.000037 | ok | yes | largest over the 6 cases |
| `fig5.rho_cell.ig.g1v2p.min` | 0.7892 | 0.7892 | 0.000014 | ok | yes | rho_cell_q of integrated gradients (64 steps where run, else 16), cellpfn_g1v2p: smallest over the 6 cases |
| `fig5.rho_cell.ig.g1v2p.max` | 0.9366 | 0.9366 | -0.000031 | ok | - | largest over the 6 cases |
| `fig5.rho_cell.ig.c1v2p.min` | 0.5418 | 0.5418 | 0.000004 | ok | yes | rho_cell_q of integrated gradients (64 steps where run, else 16), cellpfn_c1v2p: smallest over the 6 cases |
| `fig5.rho_cell.ig.c1v2p.max` | 0.8224 | 0.8224 | 0.000037 | ok | yes | largest over the 6 cases |
| `fig5.rho_class.dsloo_corr.min` | 0.9998 | 0.9998 | -0.000031 | ok | yes | source_column rho_class_q, method dsloo_corr_margin; smallest of the 12 |
| `fig5.rel_err_corr_pct.g1v2p.min` | 0.4804 | 0.4804 | 0.000023 | ok | yes (1 decimal) | source_column rel_err_corr, G1v2': smallest of the 6 cases, percent |
| `fig5.rel_err_corr_pct.g1v2p.max` | 4.8820 | 4.8820 | 0.000040 | ok | yes (1 decimal) | largest of the 6 cases |
| `fig5.rel_err_corr_pct.c1v2p.min` | 0.6128 | 0.6128 | 0.000036 | ok | yes (1 decimal) | C1v2': smallest |
| `fig5.rel_err_corr_pct.c1v2p.max` | 12.0858 | 12.0858 | -0.000000 | ok | yes | C1v2': largest (kidney count) |
| `fig5.rel_err_lin_pct.max` | 19.7922 | 19.7922 | -0.000000 | ok | yes | source_column rel_err_lin (before the correction): largest of the 12 |
| `fig5.rel_err_lin_pct.kidney_count_g1v2p` | 19.7922 | 19.7922 | -0.000000 | ok | yes | before the correction, kidney count, G1v2' |
| `fig5.rho_cell_random_genes.min` | 0.8953 | 0.8953 | 0.000040 | ok | yes | source_column dsloo_corr\|cell_rand: smallest of the 12 (random expressed genes only) |
| `fig5.rho_cell_random_genes.n_below_0.90` | 1 | 1 | 0.000000 | ok | - | number of the 12 below 0.90 |
| `fig5.cost.forwards.pbmc_g1v2p` | 10.3625 | 10.3625 | 0.000000 | ok | yes | fig5__cost_by_route.csv: timing_context load_matched, route dsloo_plus_correction: n_exact_forward_equivalents |
| `fig5.cost.speedup.pbmc_g1v2p` | 3236.4800 | 3236.4800 | 0.000000 | ok | yes | same row: speedup_vs_exact_same_scope |
| `fig5.cost.dsloo_seconds.pbmc_g1v2p` | 67.8587 | 67.8587 | 0.000000 | ok | yes | same row: seconds |
| `fig5.cost.exact_hours.pbmc_g1v2p` | 61.0064 | 61.0064 | -0.000011 | ok | yes | route exact_ko_all_genes_explained_cells: seconds / 3600 |
| `fig5.cost.forwards.pbmc_c1v2p` | 11.6279 | 11.6279 | 0.000000 | ok | yes | fig5__cost_by_route.csv: timing_context load_matched, route dsloo_plus_correction: n_exact_forward_equivalents |
| `fig5.cost.speedup.pbmc_c1v2p` | 2884.2600 | 2884.2600 | 0.000000 | ok | yes | same row: speedup_vs_exact_same_scope |
| `fig5.cost.dsloo_seconds.pbmc_c1v2p` | 68.9705 | 68.9705 | 0.000000 | ok | - | same row: seconds |
| `fig5.cost.exact_hours.pbmc_c1v2p` | 55.2581 | 55.2581 | -0.000044 | ok | - | route exact_ko_all_genes_explained_cells: seconds / 3600 |
| `fig5.cost.forwards.zebra_g1v2p` | 12.9009 | 12.9009 | 0.000000 | ok | yes | fig5__cost_by_route.csv: timing_context load_matched, route dsloo_plus_correction: n_exact_forward_equivalents |
| `fig5.cost.speedup.zebra_g1v2p` | 1640.0400 | 1640.0400 | 0.000000 | ok | yes | same row: speedup_vs_exact_same_scope |
| `fig5.cost.dsloo_seconds.zebra_g1v2p` | 22.6007 | 22.6007 | 0.000000 | ok | yes | same row: seconds |
| `fig5.cost.exact_hours.zebra_g1v2p` | 10.2961 | 10.2961 | 0.000039 | ok | yes | route exact_ko_all_genes_explained_cells: seconds / 3600 |
| `fig5.cost.forwards.kidney_count_g1v2p` | 11.6507 | 11.6507 | 0.000000 | ok | yes | fig5__cost_by_route.csv: timing_context load_matched, route dsloo_plus_correction: n_exact_forward_equivalents |
| `fig5.cost.speedup.kidney_count_g1v2p` | 351.5660 | 351.5660 | 0.000000 | ok | yes | same row: speedup_vs_exact_same_scope |
| `fig5.cost.dsloo_seconds.kidney_count_g1v2p` | 18.8297 | 18.8297 | 0.000000 | ok | yes | same row: seconds |
| `fig5.cost.exact_hours.kidney_count_g1v2p` | 1.8389 | 1.8389 | -0.000047 | ok | yes | route exact_ko_all_genes_explained_cells: seconds / 3600 |
| `fig5.cost.forwards.retimed_cases.min` | 10.3625 | 10.3625 | 0.000000 | ok | yes | route dsloo_plus_correction, retimed_load_matched_case True, both timing contexts: smallest |
| `fig5.cost.forwards.retimed_cases.max` | 31.0052 | 31.0052 | 0.000000 | ok | yes | largest |
| `fig5.cost.forwards.not_retimed_cases.max` | 37.1147 | 37.1147 | 0.000000 | ok | yes | the eight case x model that were not re-timed: largest (not to be quoted) |
| `fig5.deletion.dsloo.margin_drop.k1` | 0.6917 | 0.6917 | -0.000041 | ok | yes | fig5__deletion_curves.csv: reference case, class_label ALL, ordering_scope cell, ordering_method dsloo |
| `fig5.deletion.dsloo.margin_drop.k10` | 2.5263 | 2.5263 | -0.000040 | ok | yes | fig5__deletion_curves.csv: reference case, class_label ALL, ordering_scope cell, ordering_method dsloo |
| `fig5.deletion.dsloo.margin_drop.k50` | 5.6590 | 5.6590 | -0.000020 | ok | yes | fig5__deletion_curves.csv: reference case, class_label ALL, ordering_scope cell, ordering_method dsloo |
| `fig5.deletion.dsloo.calls_flipped_pct.k50` | 45.0262 | 45.0262 | 0.000000 | ok | - | same rows: frac_calls_flipped at k = 50 |
| `fig5.deletion.random.margin_drop.k50` | 0.1378 | 0.1378 | 0.000015 | ok | yes | ordering_method random_expressed |
| `fig5.deletion.random.calls_flipped_pct.k50` | 0.2618 | 0.2618 | -0.000020 | ok | yes (1 decimal) | ordering_method random_expressed |
| `fig5.deletion.median_base_margin` | 6.0518 | 6.0518 | -0.000030 | ok | yes | median_base_margin |
| `fig5.deletion.area_over_49.dsloo` | 3.8549 | 3.8549 | 0.000023 | ok | - | area under mean_margin_drop for k = 1..50 (trapezoid) divided by 49, ordering dsloo |
| `fig5.deletion.area_over_49.random` | 0.0649 | 0.0649 | 0.000045 | ok | - | same for random expressed genes |
| `fig5.marker_rank.IL7R.dsloo` | 2 | 2 | 0.000000 | ok | - | fig5__marker_ranks.csv: reference case, class CD4 T, method dsloo_corr_margin |
| `fig5.marker_rank.IL7R.ig64` | 33538 | 33538 | 0.000000 | ok | yes | method ig64_margin |
| `fig5.marker_rank.NKG7.dsloo` | 7 | 7 | 0.000000 | ok | - | fig5__marker_ranks.csv: reference case, class NK, method dsloo_corr_margin |
| `fig5.marker_rank.NKG7.ig64` | 33538 | 33538 | 0.000000 | ok | yes | method ig64_margin |
| `fig5.marker_rank.LYZ.dsloo_margin` | 33354 | 33354 | 0.000000 | ok | yes | LYZ for monocytes on the margin target |
| `fig5.marker_rank.LYZ.dsloo_logit` | 5 | 5 | 0.000000 | ok | - | LYZ on the logit target (method dsloo_logit) |
| `fig5.marker_exact.IL7R` | 0.1774 | 0.1774 | 0.000039 | ok | yes | fig5__ko_pairs_by_class.csv: exact_ko_margin_mean, class CD4 T |
| `fig5.marker_ig64.IL7R` | -0.2424 | -0.2424 | 0.000033 | ok | yes | score_ig64_margin |
| `fig5.marker_exact.NKG7` | 0.2293 | 0.2293 | -0.000034 | ok | yes | class NK |
| `fig5.marker_ig64.NKG7` | -0.8698 | -0.8698 | 0.000007 | ok | yes | score_ig64_margin |
| `fig5.stability.support_draws.min` | 0.4313 | 0.4313 | -0.000050 | ok | yes | fig5__stability.csv: method dsloo_corr_margin, class_label ALL, comparison support_draw: smallest |
| `fig5.stability.support_draws.max` | 0.5625 | 0.5625 | 0.000000 | ok | yes | largest |
| `fig5.stability.g_vs_c.min` | 0.6625 | 0.6625 | 0.000000 | ok | yes | comparison model_g_vs_c: smallest |
| `fig5.stability.g_vs_c.max` | 0.8778 | 0.8778 | -0.000022 | ok | yes | largest |
| `fig5.kumo.library_minutes.pbmc` | 46.2000 | 46.2000 | 0.000000 | ok | - | fig5__cost_dsloo_vs_kumo.csv: kumo_large, route A_library_as_is, PBMC: kumo_seconds / 60 (estimated) |
| `fig5.kumo.dsloo_minutes_low.pbmc` | 1.5456 | 1.5456 | -0.000045 | ok | yes (1 decimal) | dsloo_seconds_low / 60 (all query cells; inferred) |
| `fig5.kumo.dsloo_minutes_high.pbmc` | 1.8948 | 1.8948 | 0.000033 | ok | yes (1 decimal) | dsloo_seconds_high / 60 |
| `fig5.kumo.ratio_low.pbmc` | 24.3821 | 24.3821 | 0.000000 | ok | - | ratio_kumo_over_dsloo_low |
| `fig5.kumo.ratio_high.pbmc` | 29.8922 | 29.8922 | 0.000000 | ok | - | ratio_kumo_over_dsloo_high |
| `fig5.kumo.genes_seen_by_no_member_pct.large` | 1.4500 | 1.4500 | 0.000000 | ok | - | fig5__kumo_gene_coverage.csv: 2,000 varying genes |
| `fig5.kumo.genes_seen_by_no_member_pct.small` | 9.5500 | 9.5500 | 0.000000 | ok | - | fig5__kumo_gene_coverage.csv: 2,000 varying genes |
| `fig5.n_cell_model_combinations` | 2738 | 2738 | 0.000000 | ok | yes | fig5__cells.csv: rows |
| `fig5.n_cell_gene_pairs` | 271061 | 271061 | 0.000000 | ok | yes | rows of the three fig5__ko_pairs_by_cell__*.csv files |
| `fig5.n_case_model` | 12 | 12 | 0.000000 | ok | - | fig5__cases.csv: rows |

## fig6

477 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig6.operator.all.pbmc_l1.B1.mean` | 0.2031 | 0.2031 | 0.000025 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B1.ci_low` | -0.2325 | -0.2325 | 0.000016 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B1.ci_high` | 0.6387 | 0.6387 | 0.000034 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B10.mean` | -0.5000 | -0.5000 | -0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B10.ci_low` | -1.2448 | -1.2448 | -0.000048 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B10.ci_high` | 0.2448 | 0.2448 | 0.000048 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B100.mean` | 2.6875 | 2.6875 | 0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B100.ci_low` | 2.3540 | 2.3540 | -0.000012 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l1.B100.ci_high` | 3.0210 | 3.0210 | 0.000012 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B1.mean` | 0.6125 | 0.6125 | 0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B1.ci_low` | 0.1911 | 0.1911 | 0.000007 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B1.ci_high` | 1.0339 | 1.0339 | -0.000007 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B10.mean` | 4.1750 | 4.1750 | 0.000000 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B10.ci_low` | 3.4783 | 3.4783 | -0.000016 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B10.ci_high` | 4.8717 | 4.8717 | 0.000016 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B100.mean` | 6.8063 | 6.8063 | -0.000050 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B100.ci_low` | 6.3557 | 6.3557 | -0.000002 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.pbmc_l2.B100.ci_high` | 7.2568 | 7.2568 | 0.000002 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B1.mean` | -0.2932 | -0.2932 | 0.000035 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B1.ci_low` | -0.5964 | -0.5964 | -0.000035 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B1.ci_high` | 0.0101 | 0.0101 | 0.000005 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B10.mean` | 1.9704 | 1.9704 | 0.000006 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B10.ci_low` | 0.9915 | 0.9915 | 0.000046 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B10.ci_high` | 2.9493 | 2.9493 | -0.000034 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B100.mean` | 2.0702 | 2.0702 | 0.000002 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B100.ci_low` | 1.7739 | 1.7739 | -0.000023 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_dev.B100.ci_high` | 2.3665 | 2.3665 | 0.000027 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B1.mean` | -1.3547 | -1.3547 | -0.000026 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B1.ci_low` | -1.9804 | -1.9804 | 0.000047 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B1.ci_high` | -0.7291 | -0.7291 | 0.000001 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B10.mean` | 2.7147 | 2.7147 | 0.000026 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B10.ci_low` | 1.3875 | 1.3875 | -0.000035 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B10.ci_high` | 4.0420 | 4.0420 | -0.000013 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B100.mean` | 2.3321 | 2.3321 | 0.000023 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B100.ci_low` | 1.8638 | 1.8638 | 0.000003 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.zebra_ood.B100.ci_high` | 2.8004 | 2.8004 | 0.000042 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.all.B10_B100.intervals_above_below_including_zero` | 7/0/1 | 7/0/1 |  | ok | - | the 8 cells at 10 and 100 cells per class: interval above zero / below zero / including zero |
| `fig6.operator.hvg8192.pbmc_l1.B1.mean` | -0.1875 | -0.1875 | 0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B1.ci_low` | -1.0526 | -1.0526 | -0.000023 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B1.ci_high` | 0.6776 | 0.6776 | 0.000023 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B10.mean` | 0.7656 | 0.7656 | 0.000025 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B10.ci_low` | -0.0569 | -0.0569 | -0.000005 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B10.ci_high` | 1.5882 | 1.5882 | -0.000045 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B100.mean` | 1.9531 | 1.9531 | 0.000025 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B100.ci_low` | 1.6895 | 1.6895 | -0.000039 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l1.B100.ci_high` | 2.2168 | 2.2168 | -0.000011 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B1.mean` | -0.0062 | -0.0062 | -0.000050 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B1.ci_low` | -0.4775 | -0.4775 | -0.000015 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B1.ci_high` | 0.4650 | 0.4650 | 0.000015 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B10.mean` | 3.0562 | 3.0562 | 0.000050 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B10.ci_low` | 2.5073 | 2.5073 | -0.000001 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B10.ci_high` | 3.6052 | 3.6052 | 0.000001 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B100.mean` | 4.6688 | 4.6688 | -0.000050 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B100.ci_low` | 4.3896 | 4.3896 | 0.000017 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.pbmc_l2.B100.ci_high` | 4.9479 | 4.9479 | -0.000017 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B1.mean` | 0.4577 | 0.4577 | -0.000010 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B1.ci_low` | -0.2494 | -0.2494 | -0.000046 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B1.ci_high` | 1.1648 | 1.1648 | 0.000025 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B10.mean` | 2.5007 | 2.5007 | -0.000043 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B10.ci_low` | 1.4911 | 1.4911 | 0.000010 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B10.ci_high` | 3.5102 | 3.5102 | 0.000003 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B100.mean` | 1.6669 | 1.6669 | 0.000001 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B100.ci_low` | 1.3319 | 1.3319 | -0.000006 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_dev.B100.ci_high` | 2.0019 | 2.0019 | 0.000008 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B1.mean` | -0.1463 | -0.1463 | 0.000048 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B1.ci_low` | -1.0625 | -1.0625 | 0.000043 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B1.ci_high` | 0.7700 | 0.7700 | -0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B10.mean` | 3.3965 | 3.3965 | -0.000031 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B10.ci_low` | 2.3106 | 2.3106 | 0.000021 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B10.ci_high` | 4.4823 | 4.4823 | 0.000018 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B100.mean` | 1.3279 | 1.3279 | 0.000039 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B100.ci_low` | 0.8073 | 0.8073 | -0.000023 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.zebra_ood.B100.ci_high` | 1.8486 | 1.8486 | 0.000002 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg8192.B10_B100.intervals_above_below_including_zero` | 7/0/1 | 7/0/1 |  | ok | - | the 8 cells at 10 and 100 cells per class: interval above zero / below zero / including zero |
| `fig6.operator.hvg2000.pbmc_l1.B1.mean` | -0.4062 | -0.4062 | -0.000050 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B1.ci_low` | -0.9895 | -0.9895 | -0.000033 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B1.ci_high` | 0.1770 | 0.1770 | 0.000033 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B10.mean` | 1.5625 | 1.5625 | -0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B10.ci_low` | 0.9971 | 0.9971 | -0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B10.ci_high` | 2.1279 | 2.1279 | 0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B100.mean` | 3.5156 | 3.5156 | 0.000025 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B100.ci_low` | 3.0228 | 3.0228 | -0.000017 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l1.B100.ci_high` | 4.0085 | 4.0085 | -0.000033 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B1.mean` | -0.5313 | -0.5313 | 0.000050 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B1.ci_low` | -0.9836 | -0.9836 | 0.000042 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B1.ci_high` | -0.0789 | -0.0789 | -0.000042 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B10.mean` | 2.0187 | 2.0187 | 0.000050 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B10.ci_low` | 1.5329 | 1.5329 | -0.000019 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B10.ci_high` | 2.5046 | 2.5046 | 0.000019 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B100.mean` | 3.7875 | 3.7875 | 0.000000 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B100.ci_low` | 3.4228 | 3.4228 | 0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.pbmc_l2.B100.ci_high` | 4.1522 | 4.1522 | -0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B1.mean` | 0.1752 | 0.1752 | 0.000007 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B1.ci_low` | -0.3492 | -0.3492 | 0.000003 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B1.ci_high` | 0.6996 | 0.6996 | 0.000010 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B10.mean` | 1.3777 | 1.3777 | -0.000040 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B10.ci_low` | 0.7269 | 0.7269 | 0.000037 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B10.ci_high` | 2.0284 | 2.0284 | -0.000017 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B100.mean` | 0.7304 | 0.7304 | 0.000014 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B100.ci_low` | 0.4840 | 0.4840 | 0.000040 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_dev.B100.ci_high` | 0.9768 | 0.9768 | -0.000012 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B1.mean` | 0.6746 | 0.6746 | -0.000009 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B1.ci_low` | -0.0883 | -0.0883 | 0.000045 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B1.ci_high` | 1.4374 | 1.4374 | 0.000038 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B10.mean` | -0.9417 | -0.9417 | 0.000003 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B10.ci_low` | -2.1591 | -2.1591 | -0.000037 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B10.ci_high` | 0.2757 | 0.2757 | 0.000043 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B100.mean` | -0.3661 | -0.3661 | 0.000001 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B100.ci_low` | -0.8690 | -0.8690 | -0.000029 | ok | yes | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.zebra_ood.B100.ci_high` | 0.1368 | 0.1368 | 0.000031 | ok | yes (1 decimal) | fig6__operator_cases.csv: arm_role ablation_arm, metric balanced_accuracy; G1v2' minus C1v2' paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.hvg2000.B10_B100.intervals_above_below_including_zero` | 6/0/2 | 6/0/2 |  | ok | - | the 8 cells at 10 and 100 cells per class: interval above zero / below zero / including zero |
| `fig6.operator.derived_file_agrees` | yes | yes |  | ok | yes | fig6__operator_paired_by_view.csv agrees with the recomputation from the cases in all 36 cells |
| `fig6.operator.level.g1v2p.pbmc_l1.B100` | 91.8281 | 91.8281 | 0.000025 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.c1v2p.pbmc_l1.B100` | 89.1406 | 89.1406 | 0.000025 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.g1v2p.pbmc_l2.B100` | 89.0250 | 89.0250 | 0.000000 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.c1v2p.pbmc_l2.B100` | 82.2188 | 82.2188 | -0.000050 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.g1v2p.zebra_ood.B10` | 91.3056 | 91.3056 | -0.000034 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.c1v2p.zebra_ood.B10` | 88.5908 | 88.5908 | 0.000040 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.pending_rows` | 0 | 0 | 0.000000 | ok | - | fig6__operator_cases.csv: rows with status pending (must be 0: all three arms exist since 2026-10-13) |
| `fig6.operator.pending_rows_with_value` | 0 | 0 | 0.000000 | ok | - | pending rows that carry a value (must be 0) |
| `fig6.operator.d1v2p.rows` | 3600 | 3600 | 0.000000 | ok | - | fig6__operator_cases.csv: rows of model cellpfn_d1v2p (1,200 cases x 3 metrics) |
| `fig6.operator.d1v2p.draws_per_cell` | 20 | 20 | 0.000000 | ok | - | fig6__operator_cases.csv: smallest number of draws of D1v2' in a cell (must be 20) |
| `fig6.operator.level.d1v2p.pbmc_l1.B100` | 88.8906 | 88.8906 | 0.000025 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.d1v2p.pbmc_l2.B100` | 85.6562 | 85.6562 | 0.000050 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.level.d1v2p.zebra_ood.B10` | 91.1135 | 91.1135 | 0.000008 | ok | yes | fig6__operator_cases.csv: all genes, mean over 20 draws |
| `fig6.operator.vn.all.pbmc_l1.B1.mean` | -0.7187 | -0.7187 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l1.B1.ci_low` | -1.2516 | -1.2516 | -0.000000 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l1.B1.ci_high` | -0.1859 | -0.1859 | 0.000000 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l1.B10.mean` | -0.1562 | -0.1562 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l1.B10.ci_low` | -0.6200 | -0.6200 | 0.000037 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l1.B10.ci_high` | 0.3075 | 0.3075 | -0.000037 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l1.B100.mean` | -0.2500 | -0.2500 | 0.000000 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l1.B100.ci_low` | -0.5082 | -0.5082 | 0.000037 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l1.B100.ci_high` | 0.0082 | 0.0082 | -0.000037 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B1.mean` | 0.0813 | 0.0813 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l2.B1.ci_low` | -0.2840 | -0.2840 | 0.000017 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B1.ci_high` | 0.4465 | 0.4465 | -0.000017 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B10.mean` | 2.8438 | 2.8438 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l2.B10.ci_low` | 2.3754 | 2.3754 | -0.000001 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B10.ci_high` | 3.3121 | 3.3121 | 0.000001 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B100.mean` | 3.4375 | 3.4375 | -0.000000 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.pbmc_l2.B100.ci_low` | 3.0837 | 3.0837 | -0.000022 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.pbmc_l2.B100.ci_high` | 3.7913 | 3.7913 | 0.000022 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B1.mean` | -0.1690 | -0.1690 | -0.000004 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_dev.B1.ci_low` | -0.4054 | -0.4054 | -0.000001 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B1.ci_high` | 0.0674 | 0.0674 | -0.000006 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B10.mean` | 1.8359 | 1.8359 | 0.000047 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_dev.B10.ci_low` | 0.8572 | 0.8572 | -0.000044 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B10.ci_high` | 2.8147 | 2.8147 | 0.000039 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B100.mean` | 1.0389 | 1.0389 | -0.000002 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_dev.B100.ci_low` | 0.8162 | 0.8162 | -0.000043 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_dev.B100.ci_high` | 1.2616 | 1.2616 | 0.000039 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B1.mean` | -0.6872 | -0.6872 | -0.000005 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_ood.B1.ci_low` | -1.1174 | -1.1174 | -0.000003 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B1.ci_high` | -0.2570 | -0.2570 | -0.000008 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B10.mean` | 2.5227 | 2.5227 | -0.000032 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_ood.B10.ci_low` | 1.3708 | 1.3708 | -0.000017 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B10.ci_high` | 3.6746 | 3.6746 | -0.000048 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B100.mean` | 1.4698 | 1.4698 | -0.000048 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.all.zebra_ood.B100.ci_low` | 1.2821 | 1.2821 | 0.000043 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.zebra_ood.B100.ci_high` | 1.6574 | 1.6574 | -0.000038 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.all.B10_B100.intervals_above_below_including_zero` | 6/0/2 | 6/0/2 |  | ok | - | the 8 cells at 10 and 100 cells per class, D1v2' minus C1v2' (variance-only minus none): interval above zero / below zero / including zero |
| `fig6.operator.vn.hvg8192.pbmc_l1.B1.mean` | -0.0312 | -0.0312 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l1.B1.ci_low` | -0.6498 | -0.6498 | 0.000044 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l1.B1.ci_high` | 0.5873 | 0.5873 | -0.000044 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l1.B10.mean` | 0.2969 | 0.2969 | -0.000025 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l1.B10.ci_low` | -0.4420 | -0.4420 | -0.000017 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l1.B10.ci_high` | 1.0358 | 1.0358 | -0.000033 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l1.B100.mean` | -0.4531 | -0.4531 | -0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l1.B100.ci_low` | -0.8033 | -0.8033 | -0.000049 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l1.B100.ci_high` | -0.1029 | -0.1029 | -0.000001 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B1.mean` | -0.0625 | -0.0625 | 0.000000 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l2.B1.ci_low` | -0.4859 | -0.4859 | 0.000046 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B1.ci_high` | 0.3609 | 0.3609 | -0.000046 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B10.mean` | 2.1500 | 2.1500 | -0.000000 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l2.B10.ci_low` | 1.6818 | 1.6818 | -0.000045 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B10.ci_high` | 2.6182 | 2.6182 | 0.000045 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B100.mean` | 1.8750 | 1.8750 | 0.000000 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.pbmc_l2.B100.ci_low` | 1.5585 | 1.5585 | 0.000032 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.pbmc_l2.B100.ci_high` | 2.1915 | 2.1915 | -0.000032 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B1.mean` | 0.3507 | 0.3507 | -0.000018 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_dev.B1.ci_low` | -0.5118 | -0.5118 | -0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B1.ci_high` | 1.2132 | 1.2132 | -0.000011 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B10.mean` | 2.0711 | 2.0711 | 0.000040 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_dev.B10.ci_low` | 1.2622 | 1.2622 | -0.000027 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B10.ci_high` | 2.8801 | 2.8801 | 0.000008 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B100.mean` | 0.3011 | 0.3011 | -0.000020 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_dev.B100.ci_low` | 0.0672 | 0.0672 | 0.000035 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_dev.B100.ci_high` | 0.5349 | 0.5349 | 0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B1.mean` | -0.2753 | -0.2753 | 0.000042 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_ood.B1.ci_low` | -1.0055 | -1.0055 | -0.000045 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B1.ci_high` | 0.4550 | 0.4550 | 0.000029 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B10.mean` | 2.8788 | 2.8788 | -0.000027 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_ood.B10.ci_low` | 2.0069 | 2.0069 | 0.000034 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B10.ci_high` | 3.7506 | 3.7506 | 0.000011 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B100.mean` | 1.2408 | 1.2408 | -0.000047 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg8192.zebra_ood.B100.ci_low` | 0.9143 | 0.9143 | -0.000039 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.zebra_ood.B100.ci_high` | 1.5672 | 1.5672 | 0.000044 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg8192.B10_B100.intervals_above_below_including_zero` | 6/1/1 | 6/1/1 |  | ok | - | the 8 cells at 10 and 100 cells per class, D1v2' minus C1v2' (variance-only minus none): interval above zero / below zero / including zero |
| `fig6.operator.vn.hvg2000.pbmc_l1.B1.mean` | -0.4219 | -0.4219 | 0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l1.B1.ci_low` | -0.9423 | -0.9423 | 0.000028 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l1.B1.ci_high` | 0.0985 | 0.0985 | 0.000022 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l1.B10.mean` | -0.0469 | -0.0469 | 0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l1.B10.ci_low` | -0.4694 | -0.4694 | 0.000036 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l1.B10.ci_high` | 0.3756 | 0.3756 | 0.000014 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l1.B100.mean` | 0.2344 | 0.2344 | -0.000025 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l1.B100.ci_low` | -0.0905 | -0.0905 | -0.000001 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l1.B100.ci_high` | 0.5593 | 0.5593 | -0.000049 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B1.mean` | -0.1937 | -0.1937 | -0.000050 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l2.B1.ci_low` | -0.4219 | -0.4219 | 0.000009 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B1.ci_high` | 0.0344 | 0.0344 | -0.000009 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B10.mean` | 1.0563 | 1.0563 | -0.000050 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l2.B10.ci_low` | 0.6904 | 0.6904 | 0.000026 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B10.ci_high` | 1.4221 | 1.4221 | -0.000026 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B100.mean` | 1.1500 | 1.1500 | 0.000000 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.pbmc_l2.B100.ci_low` | 0.8978 | 0.8978 | -0.000034 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.pbmc_l2.B100.ci_high` | 1.4022 | 1.4022 | 0.000034 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B1.mean` | 0.0028 | 0.0028 | 0.000030 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_dev.B1.ci_low` | -0.4815 | -0.4815 | 0.000029 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B1.ci_high` | 0.4871 | 0.4871 | 0.000031 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B10.mean` | 1.3429 | 1.3429 | -0.000016 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_dev.B10.ci_low` | 0.7798 | 0.7798 | 0.000014 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B10.ci_high` | 1.9060 | 1.9060 | -0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B100.mean` | 0.4525 | 0.4525 | 0.000029 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_dev.B100.ci_low` | 0.2780 | 0.2780 | -0.000045 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_dev.B100.ci_high` | 0.6271 | 0.6271 | 0.000003 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B1.mean` | 0.3302 | 0.3302 | -0.000020 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_ood.B1.ci_low` | -0.2599 | -0.2599 | 0.000031 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B1.ci_high` | 0.9202 | 0.9202 | 0.000029 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B10.mean` | 0.4370 | 0.4370 | 0.000030 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_ood.B10.ci_low` | -0.5566 | -0.5566 | 0.000034 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B10.ci_high` | 1.4306 | 1.4306 | 0.000026 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B100.mean` | 0.3618 | 0.3618 | 0.000014 | ok | yes (1 decimal) | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.vn.hvg2000.zebra_ood.B100.ci_low` | -0.0142 | -0.0142 | -0.000019 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.zebra_ood.B100.ci_high` | 0.7378 | 0.7378 | 0.000048 | ok | yes | fig6__operator_cases.csv: D1v2' minus C1v2' (variance-only minus none) |
| `fig6.operator.vn.hvg2000.B10_B100.intervals_above_below_including_zero` | 4/0/4 | 4/0/4 |  | ok | - | the 8 cells at 10 and 100 cells per class, D1v2' minus C1v2' (variance-only minus none): interval above zero / below zero / including zero |
| `fig6.operator.fv.all.pbmc_l1.B1.mean` | 0.9219 | 0.9219 | -0.000025 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l1.B1.ci_low` | 0.3903 | 0.3903 | 0.000047 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l1.B1.ci_high` | 1.4534 | 1.4534 | 0.000003 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l1.B10.mean` | -0.3438 | -0.3438 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l1.B10.ci_low` | -0.8633 | -0.8633 | -0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l1.B10.ci_high` | 0.1758 | 0.1758 | 0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l1.B100.mean` | 2.9375 | 2.9375 | -0.000000 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l1.B100.ci_low` | 2.6397 | 2.6397 | -0.000049 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l1.B100.ci_high` | 3.2353 | 3.2353 | 0.000049 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B1.mean` | 0.5312 | 0.5312 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l2.B1.ci_low` | 0.1296 | 0.1296 | -0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B1.ci_high` | 0.9329 | 0.9329 | 0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B10.mean` | 1.3312 | 1.3312 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l2.B10.ci_low` | 0.8725 | 0.8725 | -0.000042 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B10.ci_high` | 1.7900 | 1.7900 | 0.000042 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B100.mean` | 3.3688 | 3.3688 | -0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.pbmc_l2.B100.ci_low` | 3.0560 | 3.0560 | 0.000018 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.pbmc_l2.B100.ci_high` | 3.6815 | 3.6815 | -0.000018 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B1.mean` | -0.1242 | -0.1242 | 0.000039 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_dev.B1.ci_low` | -0.4906 | -0.4906 | 0.000027 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B1.ci_high` | 0.2423 | 0.2423 | -0.000049 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B10.mean` | 0.1345 | 0.1345 | -0.000041 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_dev.B10.ci_low` | -0.4783 | -0.4783 | 0.000026 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B10.ci_high` | 0.7472 | 0.7472 | -0.000008 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B100.mean` | 1.0313 | 1.0313 | 0.000004 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_dev.B100.ci_low` | 0.8862 | 0.8862 | 0.000031 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_dev.B100.ci_high` | 1.1764 | 1.1764 | -0.000022 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B1.mean` | -0.6675 | -0.6675 | -0.000021 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_ood.B1.ci_low` | -1.0804 | -1.0804 | 0.000037 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B1.ci_high` | -0.2547 | -0.2547 | 0.000022 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B10.mean` | 0.1921 | 0.1921 | -0.000042 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_ood.B10.ci_low` | -0.3169 | -0.3169 | -0.000046 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B10.ci_high` | 0.7011 | 0.7011 | -0.000037 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B100.mean` | 0.8624 | 0.8624 | -0.000029 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.all.zebra_ood.B100.ci_low` | 0.4019 | 0.4019 | 0.000023 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.zebra_ood.B100.ci_high` | 1.3228 | 1.3228 | 0.000019 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.all.B10_B100.intervals_above_below_including_zero` | 5/0/3 | 5/0/3 |  | ok | - | the 8 cells at 10 and 100 cells per class, G1v2' minus D1v2' (full minus variance-only): interval above zero / below zero / including zero |
| `fig6.operator.fv.hvg8192.pbmc_l1.B1.mean` | -0.1563 | -0.1563 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l1.B1.ci_low` | -0.7267 | -0.7267 | 0.000048 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l1.B1.ci_high` | 0.4142 | 0.4142 | -0.000048 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l1.B10.mean` | 0.4687 | 0.4687 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l1.B10.ci_low` | -0.0232 | -0.0232 | -0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l1.B10.ci_high` | 0.9607 | 0.9607 | 0.000035 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l1.B100.mean` | 2.4063 | 2.4063 | -0.000050 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l1.B100.ci_low` | 2.1095 | 2.1095 | 0.000038 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l1.B100.ci_high` | 2.7030 | 2.7030 | -0.000038 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B1.mean` | 0.0562 | 0.0562 | 0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l2.B1.ci_low` | -0.2078 | -0.2078 | 0.000040 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B1.ci_high` | 0.3203 | 0.3203 | -0.000040 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B10.mean` | 0.9063 | 0.9063 | -0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l2.B10.ci_low` | 0.5568 | 0.5568 | 0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B10.ci_high` | 1.2557 | 1.2557 | -0.000047 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B100.mean` | 2.7938 | 2.7938 | -0.000050 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.pbmc_l2.B100.ci_low` | 2.5542 | 2.5542 | 0.000008 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.pbmc_l2.B100.ci_high` | 3.0333 | 3.0333 | -0.000008 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B1.mean` | 0.1070 | 0.1070 | 0.000007 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_dev.B1.ci_low` | -0.2207 | -0.2207 | 0.000007 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B1.ci_high` | 0.4347 | 0.4347 | 0.000008 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B10.mean` | 0.4295 | 0.4295 | 0.000016 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_dev.B10.ci_low` | 0.1206 | 0.1206 | -0.000018 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B10.ci_high` | 0.7385 | 0.7385 | -0.000049 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B100.mean` | 1.3658 | 1.3658 | 0.000021 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_dev.B100.ci_low` | 1.1399 | 1.1399 | -0.000018 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_dev.B100.ci_high` | 1.5918 | 1.5918 | -0.000040 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B1.mean` | 0.1290 | 0.1290 | 0.000006 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_ood.B1.ci_low` | -0.3605 | -0.3605 | 0.000025 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B1.ci_high` | 0.6185 | 0.6185 | -0.000013 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B10.mean` | 0.5177 | 0.5177 | -0.000003 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_ood.B10.ci_low` | 0.1165 | 0.1165 | -0.000001 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B10.ci_high` | 0.9189 | 0.9189 | -0.000005 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B100.mean` | 0.0872 | 0.0872 | -0.000013 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg8192.zebra_ood.B100.ci_low` | -0.4021 | -0.4021 | -0.000038 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.zebra_ood.B100.ci_high` | 0.5765 | 0.5765 | 0.000011 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg8192.B10_B100.intervals_above_below_including_zero` | 6/0/2 | 6/0/2 |  | ok | - | the 8 cells at 10 and 100 cells per class, G1v2' minus D1v2' (full minus variance-only): interval above zero / below zero / including zero |
| `fig6.operator.fv.hvg2000.pbmc_l1.B1.mean` | 0.0156 | 0.0156 | 0.000025 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l1.B1.ci_low` | -0.3215 | -0.3215 | 0.000004 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l1.B1.ci_high` | 0.3527 | 0.3527 | 0.000046 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l1.B10.mean` | 1.6094 | 1.6094 | -0.000025 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l1.B10.ci_low` | 1.1318 | 1.1318 | 0.000047 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l1.B10.ci_high` | 2.0869 | 2.0869 | 0.000003 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l1.B100.mean` | 3.2813 | 3.2813 | -0.000050 | ok | - | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l1.B100.ci_low` | 2.9002 | 2.9002 | -0.000040 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l1.B100.ci_high` | 3.6623 | 3.6623 | 0.000040 | ok | - | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B1.mean` | -0.3375 | -0.3375 | -0.000000 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l2.B1.ci_low` | -0.6574 | -0.6574 | -0.000021 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B1.ci_high` | -0.0176 | -0.0176 | 0.000021 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B10.mean` | 0.9625 | 0.9625 | -0.000000 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l2.B10.ci_low` | 0.6647 | 0.6647 | 0.000042 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B10.ci_high` | 1.2603 | 1.2603 | -0.000042 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B100.mean` | 2.6375 | 2.6375 | 0.000000 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.pbmc_l2.B100.ci_low` | 2.3363 | 2.3363 | -0.000046 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.pbmc_l2.B100.ci_high` | 2.9387 | 2.9387 | 0.000046 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B1.mean` | 0.1724 | 0.1724 | -0.000023 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_dev.B1.ci_low` | -0.0871 | -0.0871 | 0.000006 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B1.ci_high` | 0.4318 | 0.4318 | 0.000047 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B10.mean` | 0.0348 | 0.0348 | -0.000023 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_dev.B10.ci_low` | -0.2995 | -0.2995 | 0.000014 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B10.ci_high` | 0.3690 | 0.3690 | 0.000039 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B100.mean` | 0.2779 | 0.2779 | -0.000015 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_dev.B100.ci_low` | 0.0965 | 0.0965 | 0.000020 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_dev.B100.ci_high` | 0.4592 | 0.4592 | 0.000050 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B1.mean` | 0.3444 | 0.3444 | 0.000011 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_ood.B1.ci_low` | -0.1846 | -0.1846 | -0.000007 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B1.ci_high` | 0.8734 | 0.8734 | 0.000030 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B10.mean` | -1.3787 | -1.3787 | -0.000027 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_ood.B10.ci_low` | -2.1818 | -2.1818 | -0.000008 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B10.ci_high` | -0.5756 | -0.5756 | -0.000046 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B100.mean` | -0.7279 | -0.7279 | -0.000013 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only), paired by draw (20 draws); mean / 95% t interval |
| `fig6.operator.fv.hvg2000.zebra_ood.B100.ci_low` | -1.2151 | -1.2151 | -0.000028 | ok | yes (1 decimal) | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.zebra_ood.B100.ci_high` | -0.2407 | -0.2407 | 0.000001 | ok | yes | fig6__operator_cases.csv: G1v2' minus D1v2' (full minus variance-only) |
| `fig6.operator.fv.hvg2000.B10_B100.intervals_above_below_including_zero` | 5/2/1 | 5/2/1 |  | ok | - | the 8 cells at 10 and 100 cells per class, G1v2' minus D1v2' (full minus variance-only): interval above zero / below zero / including zero |
| `fig6.operator.readings.ba.sentences.covariance` | 5 | 5 | 0.000000 | ok | - | fig6__operator_readings.csv: balanced-accuracy cells (24) whose plan sentence says: covariance |
| `fig6.operator.readings.ba.sentences.variance` | 3 | 3 | 0.000000 | ok | - | fig6__operator_readings.csv: balanced-accuracy cells (24) whose plan sentence says: variance |
| `fig6.operator.readings.ba.sentences.both` | 2 | 2 | 0.000000 | ok | - | fig6__operator_readings.csv: balanced-accuracy cells (24) whose plan sentence says: both |
| `fig6.operator.readings.ba.sentences.none` | 14 | 14 | 0.000000 | ok | - | fig6__operator_readings.csv: balanced-accuracy cells (24) whose plan sentence says: none |
| `fig6.operator.readings.rows` | 48 | 48 | 0.000000 | ok | - | fig6__operator_readings.csv: rows (2 metrics x 3 gene views x 8 cells) |
| `fig6.operator.readings.theta_min` | 1.5000 | 1.5000 | 0.000000 | ok | yes | smallest theta of the balanced-accuracy cells |
| `fig6.operator.readings.theta_max` | 4.4724 | 4.4724 | 0.000039 | ok | yes | largest theta of the balanced-accuracy cells |
| `fig6.n3.pbmc_l1.B10.delta_ba` | -1.5625 | -1.5625 | 0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_ba |
| `fig6.n3.pbmc_l1.B10.delta_lo` | -3.5417 | -3.5417 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_lo |
| `fig6.n3.pbmc_l1.B10.delta_hi` | -0.4167 | -0.4167 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_hi |
| `fig6.n3.pbmc_l1.B10.theta` | 1.5000 | 1.5000 | 0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column theta |
| `fig6.n3.pbmc_l1.B10.A_operator_off` | -0.9375 | -0.9375 | -0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column A_operator_off |
| `fig6.n3.pbmc_l1.B10.R_rank0` | 1.1458 | 1.1458 | 0.000033 | ok | yes (1 decimal) | fig6__operator_n3_test_wide.csv: column R_rank0 |
| `fig6.n3.zebra_ood.B10.delta_ba` | 3.2955 | 3.2955 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_ba |
| `fig6.n3.zebra_ood.B10.delta_lo` | 2.7872 | 2.7872 | -0.000017 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_lo |
| `fig6.n3.zebra_ood.B10.delta_hi` | 3.8064 | 3.8064 | 0.000006 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_hi |
| `fig6.n3.zebra_ood.B10.theta` | 2.7248 | 2.7248 | -0.000021 | ok | yes | fig6__operator_n3_test_wide.csv: column theta |
| `fig6.n3.zebra_ood.B10.A_operator_off` | 5.3578 | 5.3578 | 0.000027 | ok | yes | fig6__operator_n3_test_wide.csv: column A_operator_off |
| `fig6.n3.zebra_ood.B10.R_rank0` | 0.3211 | 0.3211 | 0.000038 | ok | yes | fig6__operator_n3_test_wide.csv: column R_rank0 |
| `fig6.n3.pbmc_l1.B100.delta_ba` | 3.0208 | 3.0208 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_ba |
| `fig6.n3.pbmc_l1.B100.delta_lo` | 0.8333 | 0.8333 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_lo |
| `fig6.n3.pbmc_l1.B100.delta_hi` | 6.2500 | 6.2500 | 0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column delta_hi |
| `fig6.n3.pbmc_l1.B100.theta` | 1.5000 | 1.5000 | 0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column theta |
| `fig6.n3.pbmc_l1.B100.A_operator_off` | 3.1250 | 3.1250 | 0.000000 | ok | yes | fig6__operator_n3_test_wide.csv: column A_operator_off |
| `fig6.n3.pbmc_l1.B100.R_rank0` | 4.5833 | 4.5833 | 0.000033 | ok | yes | fig6__operator_n3_test_wide.csv: column R_rank0 |
| `fig6.n3.verdict` | NOT SUPPORTED, N3 (harm) | NOT SUPPORTED, N3 (harm) |  | ok | - | fig6__operator_n3_test_wide.csv: overall_verdict, overall_label |
| `fig6.n3.pbmc_l1.B10.donor_deltas` | -0.8 / -4.6 / -0.4 / -0.4 | -0.8 / -4.6 / -0.4 / -0.4 |  | ok | - | fig6__operator_n3_donor_deltas.csv: the four PBMC query donors (P2, P4, P6, P8), support 10 |
| `fig6.logit_share.operator_off.min` | 0.5251 | 0.5251 | 0.000018 | ok | yes | fig6__operator_logit_share.csv: support 10 and 100; mean per source_panel (dataset) x input_mode x support size; smallest rel_logit_change_operator_off |
| `fig6.logit_share.operator_off.max` | 0.7356 | 0.7356 | -0.000010 | ok | yes | fig6__operator_logit_share.csv: support 10 and 100; mean per source_panel (dataset) x input_mode x support size; largest |
| `fig6.logit_share.argmax_flip_pct.min` | 1.9352 | 1.9352 | -0.000015 | ok | yes (1 decimal) | fig6__operator_logit_share.csv: support 10 and 100; mean per source_panel (dataset) x input_mode x support size; smallest argmax_flip_share_operator_off, percent |
| `fig6.logit_share.argmax_flip_pct.max` | 13.8379 | 13.8379 | 0.000015 | ok | - | fig6__operator_logit_share.csv: support 10 and 100; mean per source_panel (dataset) x input_mode x support size; largest |
| `fig6.controls.zebra_ood.B10.rank0` | 91.5983 | 91.5983 | 0.000026 | ok | yes | fig6__operator_prereg_cases.csv: checkpoint_update 96000, source_row_id cellpfn_G1v2p_12K_rank0; mean of ba_pct over the 3 frozen draws |
| `fig6.controls.zebra_ood.B10.full` | 91.9195 | 91.9195 | -0.000036 | ok | yes | source_row_id cellpfn_G1v2p_12K |
| `fig6.controls.pbmc_l1.B100.rank0` | 87.2917 | 87.2917 | -0.000033 | ok | yes | rank 0 control |
| `fig6.controls.pbmc_l1.B100.full` | 91.8750 | 91.8750 | 0.000000 | ok | yes | full operator |
| `fig6.controls.model_ids_of_control_rows` | cellpfn_g1v2p_geneshuf;cellpfn_g1v2p_labelperm;cellpfn_g1v2p_opoff;cellpfn_g1v2p_rank0 | cellpfn_g1v2p_geneshuf;cellpfn_g1v2p_labelperm;cellpfn_g1v2p_opoff;cellpfn_g1v2p_rank0 |  | ok | - | model ids of the rows with an inference control |
| `fig6.taskmix.ba.pbmc_l1.B1.mean` | 1.1094 | 1.1094 | -0.000025 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B1.ci_low` | 0.4511 | 0.4511 | -0.000041 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B1.ci_high` | 1.7677 | 1.7677 | -0.000009 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B10.mean` | -1.4688 | -1.4688 | 0.000050 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B10.ci_low` | -2.1230 | -2.1230 | 0.000008 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B10.ci_high` | -0.8145 | -0.8145 | -0.000008 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B100.mean` | -1.5625 | -1.5625 | -0.000000 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B100.ci_low` | -1.9391 | -1.9391 | -0.000032 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l1.B100.ci_high` | -1.1859 | -1.1859 | 0.000032 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B1.mean` | 2.4188 | 2.4188 | -0.000050 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B1.ci_low` | 1.6123 | 1.6123 | -0.000003 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B1.ci_high` | 3.2252 | 3.2252 | 0.000003 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B10.mean` | 1.0625 | 1.0625 | -0.000000 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B10.ci_low` | 0.2630 | 0.2630 | -0.000050 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B10.ci_high` | 1.8620 | 1.8620 | 0.000050 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B100.mean` | 0.5000 | 0.5000 | 0.000000 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B100.ci_low` | 0.2223 | 0.2223 | 0.000039 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.pbmc_l2.B100.ci_high` | 0.7777 | 0.7777 | -0.000039 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B1.mean` | 2.5633 | 2.5633 | 0.000013 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B1.ci_low` | 1.1072 | 1.1072 | 0.000001 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B1.ci_high` | 4.0194 | 4.0194 | 0.000026 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B10.mean` | 1.3394 | 1.3394 | -0.000026 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B10.ci_low` | 0.3493 | 0.3493 | 0.000036 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B10.ci_high` | 2.3294 | 2.3294 | 0.000012 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B100.mean` | 0.3331 | 0.3331 | -0.000014 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B100.ci_low` | 0.1858 | 0.1858 | -0.000046 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_dev.B100.ci_high` | 0.4804 | 0.4804 | 0.000019 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B1.mean` | 3.4919 | 3.4919 | -0.000043 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B1.ci_low` | 1.7274 | 1.7274 | 0.000048 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B1.ci_high` | 5.2563 | 5.2563 | -0.000033 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B10.mean` | 1.3835 | 1.3835 | -0.000043 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B10.ci_low` | 0.7179 | 0.7179 | -0.000038 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B10.ci_high` | 2.0491 | 2.0491 | -0.000047 | ok | yes (1 decimal) | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B100.mean` | 0.2358 | 0.2358 | 0.000014 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B100.ci_low` | -0.0221 | -0.0221 | -0.000049 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.zebra_ood.B100.ci_high` | 0.4938 | 0.4938 | -0.000022 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B1.mean` | -0.3322 | -0.3322 | -0.000014 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B1.ci_low` | -0.3998 | -0.3998 | -0.000048 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B1.ci_high` | -0.2646 | -0.2646 | 0.000021 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B10.mean` | 0.4164 | 0.4164 | -0.000018 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B10.ci_low` | 0.3372 | 0.3372 | -0.000015 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B10.ci_high` | 0.4956 | 0.4956 | -0.000021 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B100.mean` | 0.3740 | 0.3740 | 0.000003 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B100.ci_low` | 0.3570 | 0.3570 | -0.000037 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l1.B100.ci_high` | 0.3910 | 0.3910 | 0.000043 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B1.mean` | -0.7416 | -0.7416 | 0.000045 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B1.ci_low` | -0.7729 | -0.7729 | 0.000037 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B1.ci_high` | -0.7102 | -0.7102 | -0.000046 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B10.mean` | -0.1586 | -0.1586 | -0.000003 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B10.ci_low` | -0.1720 | -0.1720 | -0.000021 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B10.ci_high` | -0.1452 | -0.1452 | 0.000016 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B100.mean` | -0.0465 | -0.0465 | -0.000029 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B100.ci_low` | -0.0512 | -0.0512 | -0.000004 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.pbmc_l2.B100.ci_high` | -0.0419 | -0.0419 | 0.000046 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B1.mean` | -0.0542 | -0.0542 | -0.000032 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B1.ci_low` | -0.2051 | -0.2051 | -0.000025 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B1.ci_high` | 0.0967 | 0.0967 | -0.000039 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B10.mean` | 0.2807 | 0.2807 | 0.000011 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B10.ci_low` | 0.1981 | 0.1981 | -0.000030 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B10.ci_high` | 0.3634 | 0.3634 | -0.000048 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B100.mean` | 0.6290 | 0.6290 | -0.000002 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B100.ci_low` | 0.6063 | 0.6063 | 0.000013 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_dev.B100.ci_high` | 0.6517 | 0.6517 | -0.000017 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B1.mean` | -0.2510 | -0.2510 | 0.000044 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B1.ci_low` | -0.3626 | -0.3626 | -0.000048 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B1.ci_high` | -0.1393 | -0.1393 | 0.000035 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B10.mean` | 0.2491 | 0.2491 | 0.000029 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B10.ci_low` | 0.1864 | 0.1864 | -0.000039 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B10.ci_high` | 0.3119 | 0.3119 | -0.000003 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B100.mean` | 0.3457 | 0.3457 | 0.000048 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B100.ci_low` | 0.3037 | 0.3037 | 0.000043 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.nll.zebra_ood.B100.ci_high` | 0.3878 | 0.3878 | -0.000047 | ok | yes | fig6__taskmix_cases.csv: GL1 minus GS1 paired by draw (20 draws, all genes, update 100,000); mean / 95% t interval |
| `fig6.taskmix.ba.intervals_above_below_including_zero` | 9/2/1 | 9/2/1 |  | ok | - | the 12 cells: accuracy interval above zero / below zero / including zero |
| `fig6.taskmix.derived_file_agrees` | yes | yes |  | ok | yes | fig6__taskmix_paired.csv agrees with the recomputation from the cases in all 24 rows |
| `fig6.taskmix.ba.8_low_cells.mean` | 1.4875 | 1.4875 | -0.000015 | ok | yes | mean over the low-support cells per draw, then mean and 95% t interval over the 20 draws |
| `fig6.taskmix.ba.8_low_cells.ci_low` | 1.0817 | 1.0817 | 0.000005 | ok | yes |  |
| `fig6.taskmix.ba.8_low_cells.ci_high` | 1.8933 | 1.8933 | -0.000036 | ok | yes |  |
| `fig6.taskmix.ba.zebra_low_4.mean` | 2.1945 | 2.1945 | 0.000000 | ok | yes | mean over the low-support cells per draw, then mean and 95% t interval over the 20 draws |
| `fig6.taskmix.ba.zebra_low_4.ci_low` | 1.4657 | 1.4657 | -0.000010 | ok | yes |  |
| `fig6.taskmix.ba.zebra_low_4.ci_high` | 2.9233 | 2.9233 | 0.000011 | ok | yes |  |
| `fig6.taskmix.ba.pbmc_low_4.mean` | 0.7805 | 0.7805 | -0.000031 | ok | yes | mean over the low-support cells per draw, then mean and 95% t interval over the 20 draws |
| `fig6.taskmix.ba.pbmc_low_4.ci_low` | 0.3826 | 0.3826 | 0.000010 | ok | yes |  |
| `fig6.taskmix.ba.pbmc_low_4.ci_high` | 1.1783 | 1.1783 | 0.000027 | ok | yes |  |
| `fig6.taskmix.nll.8_low_cells.mean` | -0.0739 | -0.0739 | -0.000017 | ok | yes | NLL, mean over the 8 low-support cells per draw, 20 draws |
| `fig6.taskmix.nll.8_low_cells.ci_low` | -0.1122 | -0.1122 | 0.000039 | ok | yes |  |
| `fig6.taskmix.nll.8_low_cells.ci_high` | -0.0357 | -0.0357 | 0.000027 | ok | yes |  |
| `fig6.stream.gl1.cell_type_share_pct` | 75.0062 | 75.0062 | 0.000050 | ok | - | fig6__taskmix_stream_composition.csv: quantity families, share |
| `fig6.stream.gl1.donor_identity_share_pct` | 24.9938 | 24.9938 | -0.000050 | ok | - | same |
| `fig6.stream.gs1.families_pct` | cell_type 15; donor_identity 5; metadata_binary 60; metadata_categorical 20 | cell_type 15; donor_identity 5; metadata_binary 60; metadata_categorical 20 |  | ok | - | GS1: share per task family, percent |
| `fig6.stream.cells_per_update_ratio_gl1_over_gs1` | 1.6709 | 1.6709 | 0.000026 | ok | yes | fig6__taskmix_stream_composition.csv: quantity cells_per_update, category mean: GL1 / GS1 |
| `fig6.trajectory.kidney_core5_a.B100.count.update100000.ba.gl1` | 95.3333 | 95.3333 | 0.000033 | ok | yes | fig6__taskmix_trajectory.csv: panel kidney_core5_a, support 100, input_mode count, checkpoint_update 100000 |
| `fig6.trajectory.kidney_core5_a.B100.count.update100000.nll.gl1` | 0.5777 | 0.5777 | -0.000027 | ok | yes | same row: nll_mean |
| `fig6.trajectory.kidney_core5_a.B100.count.update100000.ba.gs1` | 95.6667 | 95.6667 | -0.000033 | ok | yes | fig6__taskmix_trajectory.csv: panel kidney_core5_a, support 100, input_mode count, checkpoint_update 100000 |
| `fig6.trajectory.kidney_core5_a.B100.count.update100000.nll.gs1` | 0.3168 | 0.3168 | 0.000015 | ok | yes | same row: nll_mean |

## fig7

21 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `fig7.sep_b10.v22b.syn_q50` | 0.8807 | 0.8807 | 0.000014 | ok | yes | fig7__sim_vs_real_summary.csv: effect "A class: separability BA B10, K-matched (real K8, 64 cells; primary)", prior_id v2.2-B: syn_q50 |
| `fig7.sep_b10.real_q50` | 0.7746 | 0.7746 | 0.000043 | ok | yes | same row: real_q50 (stored value) |
| `fig7.sep_b10.v22b.share_above_real_max_pct` | 37.5000 | 37.5000 | 0.000000 | ok | - | same row: syn_share_above_real_max |
| `fig7.sep_b10.v1.syn_q50` | 0.0218 | 0.0218 | -0.000014 | ok | yes | prior_id v1_late |
| `fig7.sep_b100.v22b.syn_q50` | 0.9907 | 0.9907 | 0.000014 | ok | yes | effect B100 |
| `fig7.sep_b100.real_q50` | 0.9148 | 0.9148 | 0.000021 | ok | yes | real_q50 (stored value) |
| `fig7.top_marker.v22b.syn_q50` | 6.2321 | 6.2321 | 0.000046 | ok | yes | effect "A class: strongest marker per pair" |
| `fig7.top_marker.real_q50` | 7.1005 | 7.1005 | -0.000049 | ok | yes (1 decimal) | real_q50 |
| `fig7.top_marker.v1.syn_q50` | 1.9358 | 1.9358 | 0.000013 | ok | yes | prior v1_late |
| `fig7.donor_sd.v22b.syn_q50` | 0.4043 | 0.4043 | 0.000012 | ok | yes | effect "B donor: SD within study, 4x2 design (primary)" |
| `fig7.donor_sd.ratio_v22b_over_real` | 1.3947 | 1.3947 | 0.000016 | ok | yes | syn_q50 / real_q50 |
| `fig7.nb_phi.v22b.syn_q50` | 0.4477 | 0.4477 | -0.000031 | ok | yes | effect "D marginal: NB phi" |
| `fig7.zero_excess.v22b.syn_q50` | 0.0380 | 0.0380 | 0.000034 | ok | yes | effect "D marginal: zero excess" |
| `fig7.gene_gene_gain_b10.v22b.syn_q50_x100` | 2.3437 | 2.3437 | 0.000050 | ok | yes (1 decimal) | effect "E gene-gene: LDA gain B10 (full - diagonal), K-matched (real K8, 64 cells)": syn_q50 x 100 |
| `fig7.n_primary_rows` | 34 | 34 | 0.000000 | ok | - | fig7__statistics.csv: rows with primary_row == yes |
| `fig7.n_statistics` | 45 | 45 | 0.000000 | ok | - | fig7__statistics.csv: rows |
| `fig7.verdicts.v22b` | inside 14; too high 13; too low 5; too wide 2 | inside 14; too high 13; too low 5; too wide 2 |  | ok | - | verdict of the primary rows of prior v2.2-B, grouped by its first words |
| `fig7.verdicts.v1` | inside 5; too high 8; too low 21 | inside 5; too high 8; too low 21 |  | ok | - | verdict of the primary rows of prior v1_late, grouped by its first words |
| `fig7.sim_units.rows_v22b` | 49532 | 49532 | 0.000000 | ok | yes | fig7__sim_units.csv: rows of prior v2.2-B |
| `fig7.sim_units.rows_v1` | 37152 | 37152 | 0.000000 | ok | yes | rows of prior v1_late |
| `fig7.sep_b10.v22b.median_from_units` | 0.8807 | 0.8807 | 0.000014 | ok | yes | fig7__sim_units.csv: statistic chance_adj_ba_ncm_B10, tier 64, prior v2.2-B: median of the unit values |

## supp_exposure

22 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `supp_exposure.rows` | 75 | 75 | 0.000000 | ok | - | supp_exposure__study_exposure.csv: rows |
| `supp_exposure.study_entries` | 25 | 25 | 0.000000 | ok | - | rows / number of corpora |
| `supp_exposure.pbmc_cells` | 8516 | 8516 | 0.000000 | ok | yes | n_cells_in_our_cases, PBMC (one corpus) |
| `supp_exposure.kidney_cells` | 3263 | 3263 | 0.000000 | ok | yes | n_cells_in_our_cases, kidney |
| `supp_exposure.zebra_dev_query_cells` | 7769 | 7769 | 0.000000 | ok | yes | sum of n_cells_in_our_cases over the studies of this role |
| `supp_exposure.zebra_dev_query_share_in_geneformer_pct` | 22.3323 | 22.3323 | 0.000047 | ok | yes | cells of studies with exposure == yes (corpus geneformer_v2) / all cells of the role |
| `supp_exposure.zebra_ood_query_cells` | 7163 | 7163 | 0.000000 | ok | yes | sum of n_cells_in_our_cases over the studies of this role |
| `supp_exposure.zebra_ood_query_share_in_geneformer_pct` | 92.5869 | 92.5869 | 0.000005 | ok | yes | cells of studies with exposure == yes (corpus geneformer_v2) / all cells of the role |
| `supp_exposure.entries.scgpt_whole_human` | 1/1/23/0 | 1/1/23/0 |  | ok | - | exposure counts yes/partly/no/unknown over the 25 study entries |
| `supp_exposure.entries.geneformer_v2` | 10/0/12/3 | 10/0/12/3 |  | ok | - | exposure counts yes/partly/no/unknown over the 25 study entries |
| `supp_exposure.marks.geneformer_lr` | kidney_core5_a *; kidney_core5_b *; kidney_core9_a *; kidney_core9_b *; kidney_pt_sex_a *; kidney_pt_sex_b *; pbmc_l1 *; pbmc_l2 *; zebra_counts_dev (*); zebra_counts_ood *; zebra_dev (*); zebra_ood * | kidney_core5_a *; kidney_core5_b *; kidney_core9_a *; kidney_core9_b *; kidney_pt_sex_a *; kidney_pt_sex_b *; pbmc_l1 *; pbmc_l2 *; zebra_counts_dev (*); zebra_counts_ood *; zebra_dev (*); zebra_ood * |  | ok | - | supp_exposure__figure_marks.csv: marked panels of geneformer_lr |
| `supp_exposure.marks.scgpt_lr` | pbmc_l1 *; pbmc_l2 * | pbmc_l1 *; pbmc_l2 * |  | ok | - | marked panels of scgpt_lr |
| `supp_exposure.models_with_a_mark` | geneformer_cls_lr;geneformer_cls_ncm;geneformer_lr;geneformer_ncm;scgpt_lr;scgpt_ncm | geneformer_cls_lr;geneformer_cls_ncm;geneformer_lr;geneformer_ncm;scgpt_lr;scgpt_ncm |  | ok | - | models with at least one mark |
| `supp_exposure.geneformer_lr_minus_g1v2p.pbmc_l2.B1` | 17.7500 | 17.7500 | -0.000000 | ok | - | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |
| `supp_exposure.geneformer_lr_minus_g1v2p.pbmc_l2.B10` | 5.9167 | 5.9167 | -0.000033 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |
| `supp_exposure.geneformer_lr_minus_g1v2p.pbmc_l2.B100` | 1.4167 | 1.4167 | -0.000033 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |
| `supp_exposure.geneformer_lr_minus_g1v2p.zebra_ood.B1` | -4.3935 | -4.3935 | -0.000038 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|processed |
| `supp_exposure.geneformer_lr_minus_g1v2p.zebra_ood.B10` | -4.4709 | -4.4709 | -0.000034 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|processed |
| `supp_exposure.geneformer_lr_minus_g1v2p.zebra_ood.B100` | -4.3703 | -4.3703 | 0.000008 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of geneformer_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|processed |
| `supp_exposure.scgpt_lr_minus_g1v2p.pbmc_l1.B1` | 4.7917 | 4.7917 | -0.000033 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of scgpt_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |
| `supp_exposure.scgpt_lr_minus_g1v2p.pbmc_l1.B10` | -6.4583 | -6.4583 | -0.000033 | ok | yes (1 decimal) | fig4__cases.csv: cell mean of scgpt_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |
| `supp_exposure.scgpt_lr_minus_g1v2p.pbmc_l1.B100` | -11.1458 | -11.1458 | -0.000033 | ok | yes | fig4__cases.csv: cell mean of scgpt_lr\|own_input\|own minus cell mean of cellpfn_g1v2p\|all\|count |

## supp_prior_ablation

90 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `supp_prior_ablation.LR.r42` | 1.6333 | 1.6333 | 0.000004 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.LR.r43` | 1.6175 | 1.6175 | 0.000045 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.LR.r44` | 2.6059 | 2.6059 | 0.000035 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.LR.mean` | 1.9523 | 1.9523 | -0.000039 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.LR.label` | KEEP | KEEP |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A5.r42` | -1.5214 | -1.5214 | 0.000044 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A5.r43` | -1.0505 | -1.0505 | 0.000045 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A5.r44` | -1.5383 | -1.5383 | -0.000025 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A5.mean` | -1.3700 | -1.3700 | -0.000045 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A5.label` | DROP | DROP |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A6.r42` | -0.1854 | -0.1854 | 0.000027 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A6.r43` | 0.7426 | 0.7426 | -0.000047 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A6.r44` | 1.1589 | 1.1589 | 0.000019 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A6.mean` | 0.5720 | 0.5720 | 0.000033 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A6.label` | NEUTRAL | NEUTRAL |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A7.r42` | 0.1608 | 0.1608 | -0.000039 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A7.r43` | -0.2147 | -0.2147 | -0.000009 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A7.r44` | 0.6474 | 0.6474 | -0.000011 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A7.mean` | 0.1978 | 0.1978 | 0.000013 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A7.label` | UNRESOLVED | UNRESOLVED |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A1.r42` | -0.0008 | -0.0008 | 0.000021 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A1.r43` | -0.0080 | -0.0080 | -0.000050 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A1.r44` | -0.0133 | -0.0133 | 0.000035 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A1.mean` | -0.0074 | -0.0074 | 0.000035 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A1.label` | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A3.r42` | -0.0089 | -0.0089 | -0.000029 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A3.r43` | -0.0089 | -0.0089 | -0.000029 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A3.r44` | 0.0357 | 0.0357 | 0.000014 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A3.mean` | 0.0060 | 0.0060 | -0.000048 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A3.label` | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A4.r42` | 0.0110 | 0.0110 | -0.000040 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A4.r43` | -0.0347 | -0.0347 | -0.000004 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A4.r44` | -0.0325 | -0.0325 | -0.000050 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A4.mean` | -0.0188 | -0.0188 | 0.000036 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A4.label` | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A2.r42` | 0.0083 | 0.0083 | 0.000033 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A2.r43` | 0.0000 | 0.0000 | 0.000000 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A2.r44` | 0.0000 | 0.0000 | 0.000000 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A2.mean` | 0.0028 | 0.0028 | -0.000022 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A2.label` | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) | STAGE 2 CANDIDATE (Tier A + guards; decisive metric reported only) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A8a.r42` | 0.5226 | 0.5226 | 0.000007 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8a.r43` | 0.5362 | 0.5362 | 0.000005 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8a.r44` | 1.6419 | 1.6419 | -0.000043 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8a.mean` | 0.9002 | 0.9002 | 0.000023 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A8a.label` | DROP (guard) | DROP (guard) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.A8d.r42` | -0.4272 | -0.4272 | 0.000036 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8d.r43` | 0.6041 | 0.6041 | -0.000029 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8d.r44` | 0.8702 | 0.8702 | -0.000004 | ok | yes | supp_prior_ablation__replicates.csv: is_decisive_metric yes, contrast_kind vs_base: diff_improvement_signed |
| `supp_prior_ablation.A8d.mean` | 0.3490 | 0.3490 | 0.000034 | ok | yes | mean over the replicates that exist |
| `supp_prior_ablation.A8d.label` | NOT_TESTABLE (proxy headroom) | NOT_TESTABLE (proxy headroom) |  | ok | yes | supp_prior_ablation__outcomes.csv: outcome_label_frozen_applier |
| `supp_prior_ablation.outcomes_file_agrees_with_replicates` | yes | yes |  | ok | yes | r42 / r43 / r44 of the outcomes file equal the replicates file |
| `supp_prior_ablation.routing_only_arms` | A1;A3;A4;A2 | A1;A3;A4;A2 |  | ok | - | arms with label_is_routing_only == yes |
| `supp_prior_ablation.threshold.A_low_ba.band_eff` | 1.0862 | 1.0862 | -0.000025 | ok | yes | supp_prior_ablation__thresholds.csv |
| `supp_prior_ablation.threshold.A_low_ba.keep` | 1.6293 | 1.6293 | -0.000038 | ok | yes |  |
| `supp_prior_ablation.threshold.A_ood_ba.band_eff` | 1.5356 | 1.5356 | 0.000026 | ok | yes |  |
| `supp_prior_ablation.threshold.A_ood_ba.keep` | 2.3034 | 2.3034 | 0.000039 | ok | yes |  |
| `supp_prior_ablation.threshold.A_zebra_low_ba.band_eff` | 0.8552 | 0.8552 | -0.000038 | ok | yes | rule set A8 |
| `supp_prior_ablation.threshold.A_zebra_low_ba.keep` | 1.5000 | 1.5000 | 0.000000 | ok | yes | rule set A8 |
| `supp_prior_ablation.threshold.G3_limit` | -0.0300 | -0.0300 | 0.000000 | ok | yes | guard G3: guard_limit (nats) |
| `supp_prior_ablation.LR.zebra_low.r42` | 3.3244 | 3.3244 | 0.000021 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.zebra_low.r43` | 3.2507 | 3.2507 | 0.000015 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.zebra_low.r44` | 4.4525 | 4.4525 | -0.000006 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.zebra_low.mean` | 3.6759 | 3.6759 | -0.000023 | ok | yes | mean over the three replicates |
| `supp_prior_ablation.LR.pbmc_low.r42` | -0.0578 | -0.0578 | -0.000013 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.pbmc_low.r43` | -0.0156 | -0.0156 | -0.000025 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.pbmc_low.r44` | 0.7594 | 0.7594 | -0.000025 | ok | yes | supp_prior_ablation__cell_means.csv: metric balanced_accuracy, efast_tier A, stream lr minus b0 paired on replicate and efast_cell; mean over the four cells |
| `supp_prior_ablation.LR.pbmc_low.mean` | 0.2286 | 0.2286 | 0.000046 | ok | yes | mean over the three replicates |
| `supp_prior_ablation.A8a.gap_shrink.r42` | -0.6006 | -0.6006 | 0.000016 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv |
| `supp_prior_ablation.A8a.gap_shrink.r43` | -0.0090 | -0.0090 | 0.000002 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv |
| `supp_prior_ablation.A8a.gap_shrink.r44` | 0.8248 | 0.8248 | -0.000027 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv |
| `supp_prior_ablation.A8a.gap_shrink.mean` | 0.0717 | 0.0717 | 0.000030 | ok | yes | mean over the 3 replicates |
| `supp_prior_ablation.A8.gap_band` | 0.6202 | 0.6202 | -0.000014 | ok | yes | band_eff_gap |
| `supp_prior_ablation.A8.headroom_HR` | 1.2570 | 1.2570 | 0.000002 | ok | yes | headroom_HR |
| `supp_prior_ablation.hard_tier.lr.H_b100_nll.pbmc.r42` | 0.0982 | 0.0982 | -0.000043 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `supp_prior_ablation.hard_tier.lr.H_b100_nll.pbmc.r43` | 0.1015 | 0.1015 | 0.000044 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `supp_prior_ablation.hard_tier.lr.H_b100_nll.pbmc.r44` | 0.1103 | 0.1103 | -0.000001 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `supp_prior_ablation.hard_tier.lr.H_b100_nll.pbmc.mean` | 0.1033 | 0.1033 | 0.000033 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `supp_prior_ablation.hard_tier.lr.H_b100_nll.pbmc.band` | 0.0558 | 0.0558 | 0.000022 | ok | yes | band_eff |
| `supp_prior_ablation.hard_tier.lr.H_b10_ba.zebra_ood.r42` | -6.6181 | -6.6181 | 0.000043 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `supp_prior_ablation.hard_tier.lr.H_b10_ba.zebra_ood.r43` | -4.5610 | -4.5610 | 0.000045 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `supp_prior_ablation.hard_tier.lr.H_b10_ba.zebra_ood.r44` | -6.3219 | -6.3219 | -0.000004 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `supp_prior_ablation.hard_tier.lr.H_b10_ba.zebra_ood.mean` | -5.8336 | -5.8336 | -0.000039 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `supp_prior_ablation.hard_tier.lr.H_b10_ba.zebra_ood.band` | 3.0164 | 3.0164 | -0.000049 | ok | yes | band_eff |
| `supp_prior_ablation.hard_tier.a5.H_b10_ba.pbmc.mean` | 0.0062 | 0.0062 | 0.000019 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=pbmc |
| `supp_prior_ablation.hard_tier.a5.H_b10_ba.pbmc.band` | 2.0629 | 2.0629 | 0.000013 | ok | yes | band_eff |
| `supp_prior_ablation.hard_tier.a5.H_b100_ba.pbmc.mean` | -0.0868 | -0.0868 | 0.000024 | ok | yes | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_ba\|panel=pbmc |
| `supp_prior_ablation.hard_tier.a5.H_b100_ba.pbmc.band` | 0.9899 | 0.9899 | 0.000004 | ok | yes | band_eff |
| `supp_prior_ablation.hard_tier.readout_status` | final | final |  | ok | yes | readout_status of the hard-tier rows |
| `supp_prior_ablation.hard_tier.readout_id` | readout | readout |  | ok | yes | readout_id |
| `supp_prior_ablation.hard_tier.n_models` | 41 | 41 | 0.000000 | ok | - | n_models_in_readout |

## supp_taskmix_tradeoff

18 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `supp_taskmix_tradeoff.all_genes_20draws.8_low_cells` | 1.4875 | 1.4875 | -0.000015 | ok | yes | supp_taskmix_tradeoff__view_check_groups.csv: read_out "20-draw read-out, all genes, 20 draws" |
| `supp_taskmix_tradeoff.hvg8192_10draws.8_low_cells.five_states` | +0.19 / +0.32 / +0.26 / +0.06 / +0.01 | +0.19 / +0.32 / +0.26 / +0.06 / +0.01 |  | ok | yes | read_out "E-fast, HVG-8192, 10 draws": mean_diff_ba at updates 96256, 96768, 97280, 97792, 98304 |
| `supp_taskmix_tradeoff.hvg8192_10draws.8_low_cells.mean_of_states` | 0.1681 | 0.1681 | -0.000031 | ok | yes | mean of the five states |
| `supp_taskmix_tradeoff.all_genes_20draws.zebra_low_4` | 2.1945 | 2.1945 | 0.000000 | ok | yes | supp_taskmix_tradeoff__view_check_groups.csv: read_out "20-draw read-out, all genes, 20 draws" |
| `supp_taskmix_tradeoff.hvg8192_10draws.zebra_low_4.five_states` | +1.02 / +1.34 / +1.38 / +0.93 / +0.91 | +1.02 / +1.34 / +1.38 / +0.93 / +0.91 |  | ok | yes | read_out "E-fast, HVG-8192, 10 draws": mean_diff_ba at updates 96256, 96768, 97280, 97792, 98304 |
| `supp_taskmix_tradeoff.hvg8192_10draws.zebra_low_4.mean_of_states` | 1.1165 | 1.1165 | -0.000049 | ok | yes | mean of the five states |
| `supp_taskmix_tradeoff.all_genes_20draws.pbmc_low_4` | 0.7805 | 0.7805 | -0.000031 | ok | yes | supp_taskmix_tradeoff__view_check_groups.csv: read_out "20-draw read-out, all genes, 20 draws" |
| `supp_taskmix_tradeoff.hvg8192_10draws.pbmc_low_4.five_states` | -0.64 / -0.71 / -0.85 / -0.81 / -0.89 | -0.64 / -0.71 / -0.85 / -0.81 / -0.89 |  | ok | yes | read_out "E-fast, HVG-8192, 10 draws": mean_diff_ba at updates 96256, 96768, 97280, 97792, 98304 |
| `supp_taskmix_tradeoff.hvg8192_10draws.pbmc_low_4.mean_of_states` | -0.7803 | -0.7803 | -0.000012 | ok | yes | mean of the five states |
| `supp_taskmix_tradeoff.hvg8192.ba.8_low_cells.recomputed_from_cases` | +0.19 / +0.32 / +0.26 / +0.06 / +0.01 | +0.19 / +0.32 / +0.26 / +0.06 / +0.01 |  | ok | yes | supp_taskmix_tradeoff__efast_cases.csv: tier A, the 8 low-support cells; GL1 minus GS1 per state |
| `supp_taskmix_tradeoff.hvg8192.nll.8_low_cells.five_states` | +0.221 / +0.228 / +0.274 / +0.307 / +0.278 | +0.221 / +0.228 / +0.274 / +0.307 / +0.278 |  | ok | yes | same for metric nll |
| `supp_taskmix_tradeoff.tierB.cells` | kidney_core5.b100;kidney_pt_age.b100;kidney_pt_age.b200;kidney_pt_sex.b100;kidney_pt_sex.b200;zebra_sex.b100 | kidney_core5.b100;kidney_pt_age.b100;kidney_pt_age.b200;kidney_pt_sex.b100;kidney_pt_sex.b200;zebra_sex.b100 |  | ok | - | tier B cells |
| `supp_taskmix_tradeoff.tierB.nll.six_cells.five_states` | +0.106 / +0.136 / +0.202 / +0.213 / +0.195 | +0.106 / +0.136 / +0.202 / +0.213 / +0.195 |  | ok | yes | tier B, metric nll, mean over the 6 cells |
| `supp_taskmix_tradeoff.tierB.nll.kidney_cells.five_states` | +0.181 / +0.210 / +0.303 / +0.308 / +0.287 | +0.181 / +0.210 / +0.303 / +0.308 / +0.287 |  | ok | yes | tier B, kidney cells only |
| `supp_taskmix_tradeoff.kidney_pt_sex.B100.update97792.mean_confidence.gs1` | 0.6181 | 0.6181 | -0.000030 | ok | yes | supp_taskmix_tradeoff__efast_cases.csv: efast_cell kidney_pt_sex.b100, checkpoint_update 97792, metric mean_confidence |
| `supp_taskmix_tradeoff.kidney_pt_sex.B100.update97792.accuracy.gs1` | 57.1746 | 57.1746 | 0.000003 | ok | yes | metric accuracy |
| `supp_taskmix_tradeoff.kidney_pt_sex.B100.update97792.mean_confidence.gl1` | 0.8321 | 0.8321 | -0.000026 | ok | yes | supp_taskmix_tradeoff__efast_cases.csv: efast_cell kidney_pt_sex.b100, checkpoint_update 97792, metric mean_confidence |
| `supp_taskmix_tradeoff.kidney_pt_sex.B100.update97792.accuracy.gl1` | 55.4286 | 55.4286 | -0.000029 | ok | yes | metric accuracy |

## supp_stored_zeros

100 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `supp_stored_zeros.lim2022.genes_not_measured` | 6313 | 6313 | 0.000000 | ok | yes | supp_stored_zeros__study_gene_availability.csv |
| `supp_stored_zeros.studies_with_at_most_2_missing` | 5 | 5 | 0.000000 | ok | - | studies with genes_not_measured <= 2 |
| `supp_stored_zeros.n_studies` | 15 | 15 | 0.000000 | ok | - | rows |
| `supp_stored_zeros.genes_not_measured.min` | 2 | 2 | 0.000000 | ok | - | smallest per study |
| `supp_stored_zeros.genes_not_measured.max` | 6313 | 6313 | 0.000000 | ok | yes | largest per study |
| `supp_stored_zeros.genes_dropped` | 8833 | 8833 | 0.000000 | ok | yes | supp_stored_zeros__facts.csv: key zebra.genes_dropped |
| `supp_stored_zeros.genes_counts_panel` | 12325 | 12325 | 0.000000 | ok | yes | key zebra.genes_counts_panel |
| `supp_stored_zeros.tierD.zebra_dev.B1.b_raw_minus_a_all.mean` | 3.6246 | 3.6246 | 0.000045 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_dev.B1.b_raw_minus_a_all.ci_low` | 0.4232 | 0.4232 | 0.000018 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_dev.B1.b_raw_minus_a_all.ci_high` | 6.8261 | 6.8261 | -0.000028 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_dev.B1.n_draws` | 10 | 10 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_dev.B1.b_renorm_minus_b_raw.mean` | -0.2587 | -0.2587 | -0.000017 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.zebra_dev.B10.b_raw_minus_a_all.mean` | 0.6389 | 0.6389 | -0.000026 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_dev.B10.b_raw_minus_a_all.ci_low` | 0.3817 | 0.3817 | -0.000027 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_dev.B10.b_raw_minus_a_all.ci_high` | 0.8961 | 0.8961 | -0.000024 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_dev.B10.n_draws` | 10 | 10 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_dev.B10.b_renorm_minus_b_raw.mean` | -0.2760 | -0.2760 | 0.000046 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.zebra_dev.B100.b_raw_minus_a_all.mean` | 0.1395 | 0.1395 | -0.000019 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_dev.B100.b_raw_minus_a_all.ci_low` | -0.0980 | -0.0980 | 0.000024 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_dev.B100.b_raw_minus_a_all.ci_high` | 0.3769 | 0.3769 | 0.000038 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_dev.B100.n_draws` | 5 | 5 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_dev.B100.b_renorm_minus_b_raw.mean` | -0.0181 | -0.0181 | -0.000021 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.zebra_ood.B1.b_raw_minus_a_all.mean` | 1.0397 | 1.0397 | -0.000025 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_ood.B1.b_raw_minus_a_all.ci_low` | -0.6687 | -0.6687 | 0.000046 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_ood.B1.b_raw_minus_a_all.ci_high` | 2.7480 | 2.7480 | 0.000003 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_ood.B1.n_draws` | 10 | 10 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_ood.B1.b_renorm_minus_b_raw.mean` | -0.5036 | -0.5036 | -0.000009 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.zebra_ood.B10.b_raw_minus_a_all.mean` | 0.5081 | 0.5081 | -0.000046 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_ood.B10.b_raw_minus_a_all.ci_low` | 0.0287 | 0.0287 | -0.000035 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_ood.B10.b_raw_minus_a_all.ci_high` | 0.9874 | 0.9874 | 0.000043 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_ood.B10.n_draws` | 10 | 10 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_ood.B10.b_renorm_minus_b_raw.mean` | -0.1998 | -0.1998 | -0.000037 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.zebra_ood.B100.b_raw_minus_a_all.mean` | -0.4726 | -0.4726 | -0.000034 | ok | yes | supp_stored_zeros__tierD_cases.csv: metric balanced_accuracy; b_raw minus a_all paired by draw |
| `supp_stored_zeros.tierD.zebra_ood.B100.b_raw_minus_a_all.ci_low` | -1.6573 | -1.6573 | 0.000039 | ok | yes | 95% t interval over the draws |
| `supp_stored_zeros.tierD.zebra_ood.B100.b_raw_minus_a_all.ci_high` | 0.7120 | 0.7120 | -0.000007 | ok | yes |  |
| `supp_stored_zeros.tierD.zebra_ood.B100.n_draws` | 5 | 5 | 0.000000 | ok | - | number of draws |
| `supp_stored_zeros.tierD.zebra_ood.B100.b_renorm_minus_b_raw.mean` | 0.0469 | 0.0469 | -0.000004 | ok | yes | re-normalising on top |
| `supp_stored_zeros.tierD.mean_gain_four_B1_B10_cells` | 1.4528 | 1.4528 | 0.000012 | ok | yes | mean of the four B1 / B10 gains |
| `supp_stored_zeros.abc.r10k.dev.B1.a` | 43.3264 | 43.3264 | -0.000028 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B1.b` | 52.1439 | 52.1439 | 0.000003 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B1.c` | 54.0292 | 54.0292 | 0.000041 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B10.a` | 65.1263 | 65.1263 | 0.000030 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B10.b` | 65.4272 | 65.4272 | 0.000041 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B10.c` | 63.9309 | 63.9309 | 0.000005 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B100.a` | 65.5370 | 65.5370 | -0.000042 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B100.b` | 65.7282 | 65.7282 | -0.000001 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.dev.B100.c` | 64.3376 | 64.3376 | 0.000003 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B1.a` | 68.1927 | 68.1927 | 0.000049 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B1.b` | 70.5074 | 70.5074 | 0.000003 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B1.c` | 70.5852 | 70.5852 | 0.000047 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B10.a` | 93.3279 | 93.3279 | 0.000037 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B10.b` | 94.2423 | 94.2423 | 0.000046 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B10.c` | 93.6563 | 93.6563 | -0.000013 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B100.a` | 94.6542 | 94.6542 | -0.000003 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B100.b` | 95.2394 | 95.2394 | 0.000029 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.r10k.ood.B100.c` | 94.0280 | 94.0280 | -0.000038 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B1.a` | 41.1666 | 41.1666 | 0.000043 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B1.b` | 47.3579 | 47.3579 | -0.000034 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B1.c` | 51.6073 | 51.6073 | -0.000008 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B10.a` | 60.8655 | 60.8655 | -0.000036 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B10.b` | 59.9800 | 59.9800 | -0.000036 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B10.c` | 60.4725 | 60.4725 | -0.000019 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B100.a` | 63.9247 | 63.9247 | -0.000003 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B100.b` | 62.8831 | 62.8831 | 0.000020 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.dev.B100.c` | 61.7186 | 61.7186 | 0.000005 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B1.a` | 63.0927 | 63.0927 | 0.000007 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B1.b` | 63.6137 | 63.6137 | 0.000049 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B1.c` | 65.7736 | 65.7736 | 0.000049 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B10.a` | 88.6239 | 88.6239 | 0.000031 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B10.b` | 87.7608 | 87.7608 | -0.000017 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B10.c` | 89.2901 | 89.2901 | 0.000045 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B100.a` | 92.2075 | 92.2075 | 0.000031 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B100.b` | 91.8750 | 91.8750 | 0.000007 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.c1v2p.ood.B100.c` | 90.9331 | 90.9331 | -0.000001 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B1.a` | 41.3626 | 41.3626 | 0.000008 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B1.b` | 47.1166 | 47.1166 | -0.000004 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B1.c` | 51.4218 | 51.4218 | -0.000039 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B10.a` | 63.5848 | 63.5848 | -0.000026 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B10.b` | 63.7320 | 63.7320 | -0.000010 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B10.c` | 63.3868 | 63.3868 | -0.000014 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B100.a` | 66.0501 | 66.0501 | -0.000041 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B100.b` | 66.0359 | 66.0359 | -0.000024 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.dev.B100.c` | 64.9272 | 64.9272 | 0.000011 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B1.a` | 62.8365 | 62.8365 | -0.000049 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B1.b` | 62.8003 | 62.8003 | 0.000024 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B1.c` | 65.8914 | 65.8914 | -0.000040 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B10.a` | 91.9195 | 91.9195 | -0.000036 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B10.b` | 92.0628 | 92.0628 | 0.000016 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B10.c` | 92.8879 | 92.8879 | -0.000039 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B100.a` | 94.6569 | 94.6569 | 0.000023 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting a; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B100.b` | 94.3345 | 94.3345 | 0.000020 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting b; mean over draws 0-2 |
| `supp_stored_zeros.abc.g1v2p.ood.B100.c` | 93.7827 | 93.7827 | -0.000045 | ok | yes | supp_stored_zeros__cases.csv: metric balanced_accuracy, setting c; mean over draws 0-2 |
| `supp_stored_zeros.r10k.dev.B1.c_minus_a` | 10.7029 | 10.7029 | -0.000031 | ok | yes | c minus a |
| `supp_stored_zeros.g1v2p.dev.B1.b_minus_a` | 5.7540 | 5.7540 | -0.000012 | ok | yes (1 decimal) | b minus a |
| `supp_stored_zeros.other_methods.dev.B1.n_series` | 17 | 17 | 0.000000 | ok | - | series (model x gene view) with both settings at development B1 |
| `supp_stored_zeros.other_methods.dev.B1.min` | -1.1129 | -1.1129 | 0.000046 | ok | yes (1 decimal) | counts panel minus processed panel: smallest |
| `supp_stored_zeros.other_methods.dev.B1.min_model` | geneformer_lr | geneformer_lr |  | ok | yes | model of the smallest |
| `supp_stored_zeros.other_methods.dev.B1.max` | 5.5518 | 5.5518 | 0.000001 | ok | yes (1 decimal) | largest |
| `supp_stored_zeros.other_methods.dev.B1.max_model` | kumo_small | kumo_small |  | ok | yes | model of the largest |
| `supp_stored_zeros.proxy_headroom_b0` | 1.2570 | 1.2570 | 0.000002 | ok | yes | supp_stored_zeros__proxy_gap_cases.csv: per model mean over the 4 cells of (panel_12325_genes minus processed_panel); mean over the 3 b0 replicates |

## supp_rosmap

36 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `supp_rosmap.rows` | 918 | 918 | 0.000000 | ok | - | supp_rosmap__auc.csv: rows |
| `supp_rosmap.rows_not_marked_not_final` | 0 | 0 | 0.000000 | ok | - | rows whose finality is not "not final: label fixes pending" |
| `supp_rosmap.pooled_matched.T1.microglia.all.auc` | 0.7450 | 0.7450 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T1.microglia.all.ci_low` | 0.7000 | 0.7000 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T1.microglia.all.ci_high` | 0.7900 | 0.7900 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T1.microglia.women.auc` | 0.8040 | 0.8040 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T1.microglia.men.auc` | 0.6860 | 0.6860 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.pooled_matched.T1.oligo.all.auc` | 0.5750 | 0.5750 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T1.oligo.all.ci_low` | 0.5100 | 0.5100 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T1.oligo.all.ci_high` | 0.6390 | 0.6390 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T1.oligo.women.auc` | 0.5930 | 0.5930 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T1.oligo.men.auc` | 0.5570 | 0.5570 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.pooled_matched.T2.microglia.all.auc` | 0.6840 | 0.6840 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T2.microglia.all.ci_low` | 0.6190 | 0.6190 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T2.microglia.all.ci_high` | 0.7480 | 0.7480 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T2.microglia.women.auc` | 0.6960 | 0.6960 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T2.microglia.men.auc` | 0.6710 | 0.6710 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.pooled_matched.T2.oligo.all.auc` | 0.5840 | 0.5840 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T2.oligo.all.ci_low` | 0.5320 | 0.5320 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T2.oligo.all.ci_high` | 0.6350 | 0.6350 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T2.oligo.women.auc` | 0.5680 | 0.5680 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T2.oligo.men.auc` | 0.6020 | 0.6020 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.pooled_matched.T3.microglia.all.auc` | 0.7030 | 0.7030 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T3.microglia.all.ci_low` | 0.6110 | 0.6110 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T3.microglia.all.ci_high` | 0.7950 | 0.7950 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T3.microglia.women.auc` | 0.7410 | 0.7410 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T3.microglia.men.auc` | 0.6650 | 0.6650 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.pooled_matched.T3.oligo.all.auc` | 0.6320 | 0.6320 | 0.000000 | ok | yes | supp_rosmap__auc.csv: analysis pooled_matched_model, headline_in_answer yes, model cellpfn_g1v2p, sex_query all (NOT FINAL) |
| `supp_rosmap.pooled_matched.T3.oligo.all.ci_low` | 0.5420 | 0.5420 | 0.000000 | ok | yes | corrected repeated-split 95% interval, lower end |
| `supp_rosmap.pooled_matched.T3.oligo.all.ci_high` | 0.7210 | 0.7210 | 0.000000 | ok | yes | upper end |
| `supp_rosmap.pooled_matched.T3.oligo.women.auc` | 0.6150 | 0.6150 | 0.000000 | ok | yes | sex_query women |
| `supp_rosmap.pooled_matched.T3.oligo.men.auc` | 0.6450 | 0.6450 | 0.000000 | ok | yes | sex_query men |
| `supp_rosmap.per_sex.T1.microglia.women.41_support_donors` | 0.7520 | 0.7520 | 0.000000 | ok | yes | analysis per_sex_model, women, 41 support donors per class (NOT FINAL) |
| `supp_rosmap.per_sex.T1.microglia.men.41_support_donors` | 0.6600 | 0.6600 | 0.000000 | ok | yes | analysis per_sex_model, men, 41 support donors per class (NOT FINAL) |
| `supp_rosmap.analysis_row_counts` | earlier_unmatched_sexes_pooled 36; per_sex_model 336; pooled_matched_model 546 | earlier_unmatched_sexes_pooled 36; per_sex_model 336; pooled_matched_model 546 |  | ok | - | rows per analysis |
| `supp_rosmap.columns_with_donor_or_gene_index` | none | none |  | ok | yes | columns that would index donors, genes or cells (must be none) |

## cross-block agreement

32 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `cross.fig2_cases_vs_fig4_table_best_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000049 | ok | - | fig2__cases.csv (draws 0-2) against fig4__table_best_cases.csv on model, gene view, panel, support size, draw: balanced accuracy |
| `cross.fig2_cases_vs_fig4_table_best_cases.n_common_cases` | 1188 | 1188 | 0.000000 | ok | - | cases compared |
| `cross.tabpfn_all_genes_refused.fig4_table_best_cases` | 36 | 36 | 0.000000 | ok | - | fig4__table_best_cases.csv: tabpfn35, all genes, status refused (fig2__cases.csv: see fig2.tabpfn35_all_refused_cases) |
| `cross.fig6_operator_cases_vs_fig2_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig6__operator_cases.csv against fig2__cases.csv (CellPFN rows; same source run) on model, gene view, panel, support size, draw, metric |
| `cross.fig6_operator_cases_vs_fig2_cases.n_common_rows` | 10800 | 10800 | 0.000000 | ok | - | rows compared |
| `cross.fig2_later_states_vs_fig6_taskmix_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig2__cases_cellpfn_later_states.csv (all genes, update 100,000) against fig6__taskmix_cases.csv |
| `cross.fig2_later_states_vs_fig6_taskmix_cases.n_common_rows` | 960 | 960 | 0.000000 | ok | - | rows compared |
| `cross.fig2_later_states_vs_efast_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig2__cases_cellpfn_later_states.csv (hvg8192) against supp_taskmix_tradeoff__efast_cases.csv (tier A) |
| `cross.fig2_later_states_vs_efast_cases.n_common_rows` | 3000 | 3000 | 0.000000 | ok | - | rows compared |
| `cross.fig3_cases_vs_fig4_cases.c2b40k.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig3__cases.csv (scoring_run c2b_root) against fig4__cases.csv, 2,000-gene view, four core panels |
| `cross.fig3_cases_vs_fig4_cases.c2b40k.n_common_cases` | 36 | 36 | 0.000000 | ok | - | cases compared |
| `cross.fig3_cases_vs_fig4_cases.k2b_l40k.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig3__cases.csv (scoring_run k2b_root) against fig4__cases.csv, 2,000-gene view, four core panels |
| `cross.fig3_cases_vs_fig4_cases.k2b_l40k.n_common_cases` | 36 | 36 | 0.000000 | ok | - | cases compared |
| `cross.fig3_cases_vs_fig4_cases.tabicl_v2.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig3__cases.csv (scoring_run benchmark_20260928) against fig4__cases.csv, 2,000-gene view, four core panels |
| `cross.fig3_cases_vs_fig4_cases.tabicl_v2.n_common_cases` | 36 | 36 | 0.000000 | ok | - | cases compared |
| `cross.fig3_cases_vs_fig4_cases.kumo_large.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig3__cases.csv (scoring_run kumo_benchmark_20261005) against fig4__cases.csv, 2,000-gene view, four core panels |
| `cross.fig3_cases_vs_fig4_cases.kumo_large.n_common_cases` | 36 | 36 | 0.000000 | ok | - | cases compared |
| `cross.stored_zeros_setting_a_vs_fig4_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | supp_stored_zeros__cases.csv (G1v2', setting a) against fig4__cases.csv (series cellpfn_g1v2p\|all\|processed) |
| `cross.stored_zeros_setting_a_vs_fig4_cases.n_common_cases` | 18 | 18 | 0.000000 | ok | - | cases compared |
| `cross.a8_gap_cases_vs_proxy_gap_cases.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | supp_prior_ablation__a8_gap_cases.csv against supp_stored_zeros__proxy_gap_cases.csv (both settings) |
| `cross.a8_gap_cases_vs_proxy_gap_cases.n_common_cases` | 480 | 480 | 0.000000 | ok | - | cases compared |
| `cross.fig1_training_stream_vs_fig6_stream_composition.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | task-family counts of the GS1 and GL1 windows in fig1__training_stream.csv and fig6__taskmix_stream_composition.csv |
| `cross.fig1_training_stream_vs_fig6_stream_composition.n_common` | 6 | 6 | 0.000000 | ok | - | entries compared |
| `cross.exposure_marks.fig2_vs_supp_exposure.n_different` | 0 | 0 | 0.000000 | ok | - | fig2__exposure_marks.csv against supp_exposure__figure_marks.csv (Geneformer and scGPT on the four core panels): marks that differ |
| `cross.exposure_marks.fig2_vs_supp_exposure.n_compared` | 8 | 8 | 0.000000 | ok | - | marks compared |
| `cross.glossary_panels_vs_fig4_panels.n_classes_different` | 0 | 0 | 0.000000 | ok | - | glossary__panels.csv against fig4__panels.csv: panels whose number of classes differs |
| `cross.k2b_s10k_is_stage1_control_s42.max_abs_diff` | 0.0000 | 0.0000 | 0.000000 | ok | - | fig3__cases.csv (k2b_s10k, scoring_run stage0_efast) against supp_prior_ablation__cases.csv (the model called s42 before unification): same checkpoint, same scores |
| `cross.k2b_s10k_is_stage1_control_s42.n_common_cases` | 100 | 100 | 0.000000 | ok | - | cases compared |
| `cross.model_ids_not_in_glossary` | 0 | 0 | 0.000000 | ok | - | model_id values of the data files that are missing in glossary__models.csv |
| `cross.model_labels_different_from_glossary` | 0 | 0 | 0.000000 | ok | - | distinct (model_id, model_label) pairs in the data files whose label is not the glossary label |
| `cross.model_families_different_from_glossary` | 0 | 0 | 0.000000 | ok | - | distinct (model_id, family) pairs whose family is not the glossary family |
| `cross.n_models_in_glossary` | 130 | 130 | 0.000000 | ok | - | glossary__models.csv: rows |

## final pass (corrections of 2026-10-11)

141 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `final.hard_tier.n_arm_streams` | 12 | 12 | 0.000000 | ok | - | supp_prior_ablation__hard_tier_deltas.csv: streams with a contrast against their base |
| `final.hard_tier.rows_not_run` | 80 | 80 | 0.000000 | ok | - | rows with status not_run (the missing replicate r43 of a8d; no value) |
| `final.hard_tier.streams_with_missing_replicate` | a8d | a8d |  | ok | - | streams that have such rows |
| `final.hard_tier.beyond_band.better` | a1 H_b100_nll; a1 H_b100_nll\|group=sibling; a1 H_b100_nll\|panel=pbmc; lr H_b100_nll; lr H_b100_nll\|group=sibling; lr H_b100_nll\|panel=pbmc | a1 H_b100_nll; a1 H_b100_nll\|group=sibling; a1 H_b100_nll\|panel=pbmc; lr H_b100_nll; lr H_b100_nll\|group=sibling; lr H_b100_nll\|panel=pbmc |  | ok | - | all-task, group and panel scopes: stream and value with beyond_band yes and a positive (improvement-signed) mean |
| `final.hard_tier.beyond_band.worse` | a8a H_b100_nll\|group=sibling; a8a H_b100_nll\|panel=zebra_ood; a8a H_b10_ba\|panel=zebra_ood; a8a H_b10_nll\|panel=zebra_ood; a8a H_b1_ba; a8a H_b1_ba\|group=finest; a8a H_b1_ba\|panel=pbmc; lr H_b10_ba\|panel=zebra_ood | a8a H_b100_nll\|group=sibling; a8a H_b100_nll\|panel=zebra_ood; a8a H_b10_ba\|panel=zebra_ood; a8a H_b10_nll\|panel=zebra_ood; a8a H_b1_ba; a8a H_b1_ba\|group=finest; a8a H_b1_ba\|panel=pbmc; lr H_b10_ba\|panel=zebra_ood |  | ok | - | the same with a negative mean |
| `final.hard_tier.pbmc_ba_b10_b100.n_entries` | 24 | 24 | 0.000000 | ok | - | stream x support entries of H_b10_ba\|panel=pbmc and H_b100_ba\|panel=pbmc |
| `final.hard_tier.pbmc_ba_b10_b100.n_beyond_band` | 0 | 0 | 0.000000 | ok | - | of them with beyond_band yes |
| `final.hard_tier.pbmc_ba_b10_b100.n_blank` | 2 | 2 | 0.000000 | ok | - | of them blank (two replicates) |
| `final.hard_tier.a1.H_b100_nll.pbmc.r42` | 0.1101 | 0.1101 | -0.000040 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `final.hard_tier.a1.H_b100_nll.pbmc.r43` | 0.1320 | 0.1320 | -0.000050 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `final.hard_tier.a1.H_b100_nll.pbmc.r44` | 0.1225 | 0.1225 | -0.000025 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|panel=pbmc |
| `final.hard_tier.a1.H_b100_nll.pbmc.mean` | 0.1215 | 0.1215 | -0.000005 | ok | - | mean of the three replicates |
| `final.hard_tier.a1.H_b100_nll.pbmc.band` | 0.0558 | 0.0558 | 0.000022 | ok | - | band_eff |
| `final.hard_tier.a1.H_b100_nll.pbmc.beyond_band` | yes | yes |  | ok | - | beyond_band |
| `final.hard_tier.a8a.H_b1_ba.pbmc.r42` | -1.6675 | -1.6675 | -0.000033 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.a8a.H_b1_ba.pbmc.r43` | -1.1834 | -1.1834 | -0.000008 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.a8a.H_b1_ba.pbmc.r44` | -1.4990 | -1.4990 | -0.000033 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.a8a.H_b1_ba.pbmc.mean` | -1.4500 | -1.4500 | 0.000009 | ok | - | mean of the three replicates |
| `final.hard_tier.a8a.H_b1_ba.pbmc.band` | 0.9560 | 0.9560 | 0.000028 | ok | - | band_eff |
| `final.hard_tier.a8a.H_b1_ba.pbmc.beyond_band` | yes | yes |  | ok | - | beyond_band |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.r42` | -9.2455 | -9.2455 | 0.000042 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.r43` | -5.8910 | -5.8910 | 0.000031 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.r44` | -8.8848 | -8.8848 | 0.000025 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=zebra_ood |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.mean` | -8.0071 | -8.0071 | 0.000033 | ok | - | mean of the three replicates |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.band` | 3.0164 | 3.0164 | -0.000049 | ok | - | band_eff |
| `final.hard_tier.a8a.H_b10_ba.zebra_ood.beyond_band` | yes | yes |  | ok | - | beyond_band |
| `final.hard_tier.lr.H_b1_ba.pbmc.r42` | 0.4472 | 0.4472 | 0.000025 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b1_ba.pbmc.r43` | 0.9022 | 0.9022 | 0.000003 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b1_ba.pbmc.r44` | 0.6482 | 0.6482 | -0.000027 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b1_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b1_ba.pbmc.mean` | 0.6659 | 0.6659 | -0.000033 | ok | - | mean of the three replicates |
| `final.hard_tier.lr.H_b1_ba.pbmc.band` | 0.9560 | 0.9560 | 0.000028 | ok | - | band_eff |
| `final.hard_tier.lr.H_b1_ba.pbmc.beyond_band` | no | no |  | ok | - | beyond_band |
| `final.hard_tier.lr.H_b10_ba.pbmc.r42` | -0.6894 | -0.6894 | 0.000040 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b10_ba.pbmc.r43` | 0.6036 | 0.6036 | 0.000036 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b10_ba.pbmc.r44` | 1.1347 | 1.1347 | -0.000010 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b10_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b10_ba.pbmc.mean` | 0.3497 | 0.3497 | -0.000045 | ok | - | mean of the three replicates |
| `final.hard_tier.lr.H_b10_ba.pbmc.band` | 2.0629 | 2.0629 | 0.000013 | ok | - | band_eff |
| `final.hard_tier.lr.H_b10_ba.pbmc.beyond_band` | no | no |  | ok | - | beyond_band |
| `final.hard_tier.lr.H_b100_ba.pbmc.r42` | -0.0762 | -0.0762 | -0.000040 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b100_ba.pbmc.r43` | 0.4440 | 0.4440 | -0.000025 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b100_ba.pbmc.r44` | 0.6838 | 0.6838 | 0.000012 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_ba\|panel=pbmc |
| `final.hard_tier.lr.H_b100_ba.pbmc.mean` | 0.3505 | 0.3505 | 0.000015 | ok | - | mean of the three replicates |
| `final.hard_tier.lr.H_b100_ba.pbmc.band` | 0.9899 | 0.9899 | 0.000004 | ok | - | band_eff |
| `final.hard_tier.lr.H_b100_ba.pbmc.beyond_band` | no | no |  | ok | - | beyond_band |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.r42` | 0.7388 | 0.7388 | -0.000047 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.r43` | 0.7338 | 0.7338 | -0.000009 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.r44` | 0.7229 | 0.7229 | 0.000033 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.mean` | 0.7318 | 0.7318 | 0.000026 | ok | - | mean of the three replicates |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.band` | 0.1184 | 0.1184 | -0.000011 | ok | - | band_eff |
| `final.hard_tier.lr.H_b100_nll.task_CD4T.beyond_band` | yes | yes |  | ok | - | beyond_band |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.r42` | 0.7358 | 0.7358 | -0.000018 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.r43` | 0.7535 | 0.7535 | 0.000012 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.r44` | 0.7242 | 0.7242 | -0.000017 | ok | - | supp_prior_ablation__hard_tier_deltas.csv (final read-out; POST HOC): contrast_kind vs_base, value_key H_b100_nll\|task=pbmc.l2.sib.CD4T |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.mean` | 0.7378 | 0.7378 | 0.000026 | ok | - | mean of the three replicates |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.band` | 0.1184 | 0.1184 | -0.000011 | ok | - | band_eff |
| `final.hard_tier.a1.H_b100_nll.task_CD4T.beyond_band` | yes | yes |  | ok | - | beyond_band |
| `final.hard_tier.lr.H_b100_nll.pbmc_without_CD4T.r42` | 0.0066 | 0.0066 | 0.000043 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.lr.H_b100_nll.pbmc_without_CD4T.r43` | 0.0112 | 0.0112 | 0.000022 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.lr.H_b100_nll.pbmc_without_CD4T.r44` | 0.0228 | 0.0228 | -0.000020 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.lr.H_b100_nll.pbmc_without_CD4T.mean` | 0.0135 | 0.0135 | 0.000049 | ok | - | mean of the three replicates |
| `final.hard_tier.a1.H_b100_nll.pbmc_without_CD4T.r42` | 0.0207 | 0.0207 | -0.000029 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.a1.H_b100_nll.pbmc_without_CD4T.r43` | 0.0432 | 0.0432 | -0.000044 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.a1.H_b100_nll.pbmc_without_CD4T.r44` | 0.0365 | 0.0365 | 0.000017 | ok | - | supp_prior_ablation__hard_tier_cases.csv: metric nll, support 100, panel pbmc, task != pbmc.l2.sib.CD4T; mean over draws per task, mean over the 7 tasks; -(arm - b0) per replicate |
| `final.hard_tier.a1.H_b100_nll.pbmc_without_CD4T.mean` | 0.0334 | 0.0334 | 0.000048 | ok | - | mean of the three replicates |
| `final.hard_tier.controls.H_b100_ba.pbmc.min` | 79.8436 | 79.8436 | 0.000025 | ok | - | supp_prior_ablation__hard_tier_values.csv: stream S, value_key H_b100_ba\|panel=pbmc |
| `final.hard_tier.controls.H_b100_ba.pbmc.max` | 80.8335 | 80.8335 | 0.000029 | ok | - | the same |
| `final.hard_tier.cellpfn.rows` | 400 | 400 | 0.000000 | ok | - | supp_prior_ablation__hard_tier_cellpfn_values.csv: rows |
| `final.hard_tier.cellpfn.states` | G1v2p; GL1_098304; GL1_100000; GS1_098304; GS1_100000 | G1v2p; GL1_098304; GL1_100000; GS1_098304; GS1_100000 |  | ok | - | source_model_id values |
| `final.hard_tier.cellpfn.H_b100_ba.pbmc.min` | 79.9738 | 79.9738 | -0.000028 | ok | - | value_key H_b100_ba\|panel=pbmc over the five states |
| `final.hard_tier.cellpfn.H_b100_ba.pbmc.max` | 81.8109 | 81.8109 | -0.000011 | ok | - | the same |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b1_ba.pbmc.update_098304` | 0.9772 | 0.9772 | -0.000042 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b1_ba.pbmc.update_100000` | 1.9205 | 1.9205 | -0.000008 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b10_ba.pbmc.update_098304` | 3.6027 | 3.6027 | -0.000037 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b10_ba.pbmc.update_100000` | 3.5177 | 3.5177 | 0.000020 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b100_ba.pbmc.update_098304` | 1.4371 | 1.4371 | 0.000012 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b100_ba.pbmc.update_100000` | 1.8371 | 1.8371 | 0.000018 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b10_ba.zebra_ood.update_098304` | 3.8419 | 3.8419 | 0.000048 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b10_ba.zebra_ood.update_100000` | 5.2924 | 5.2924 | 0.000002 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b100_ba.zebra_ood.update_098304` | -3.3887 | -3.3887 | -0.000010 | ok | - | GL1 minus GS1 at the same update |
| `final.hard_tier.cellpfn.GL1_minus_GS1.H_b100_ba.zebra_ood.update_100000` | -4.4784 | -4.4784 | -0.000022 | ok | - | GL1 minus GS1 at the same update |
| `final.fig7.rows_naming_rosmap_as_dataset` | 0 | 0 | 0.000000 | ok | - | fig7__real_by_dataset.csv and fig7__real_by_study.csv: rows with dataset == ROSMAP (must be 0) |
| `final.fig7.real_by_dataset.rows` | 264 | 264 | 0.000000 | ok | - | rows |
| `final.fig7.real_by_study.rows` | 830 | 830 | 0.000000 | ok | - | rows |
| `final.fig7.real_by_study.n_statistics` | 7 | 7 | 0.000000 | ok | - | distinct statistics |
| `final.fig7.real_by_study.n_dataset_study` | 13 | 13 | 0.000000 | ok | - | dataset x study combinations |
| `final.fig7.summary.rows_real_side_public_only` | 240 | 240 | 0.000000 | ok | - | fig7__sim_vs_real_summary.csv: rows whose real reference had ROSMAP units removed |
| `final.fig7.summary.rows_reference_unchanged` | 120 | 120 | 0.000000 | ok | - | rows whose reference never held a ROSMAP unit |
| `final.fig7.summary.rows_verdict_class_differs` | 23 | 23 | 0.000000 | ok | - | rows with verdict_differs_from_source_report yes |
| `final.fig7.verdicts_source_report.v22b` | inside 17; too high 11; too low 4; too wide 2 | inside 17; too high 11; too low 4; too wide 2 |  | ok | - | primary rows of prior v2.2-B: verdict_source_report (the report's verdict, reference with ROSMAP), grouped by its first words |
| `final.fig7.primary_rows_verdict_differs.v22b` | 3 | 3 | 0.000000 | ok | - | primary rows whose verdict class differs from the report's |
| `final.fig7.verdicts_source_report.v1` | inside 5; too high 8; too low 21 | inside 5; too high 8; too low 21 |  | ok | - | primary rows of prior v1_late: verdict_source_report (the report's verdict, reference with ROSMAP), grouped by its first words |
| `final.fig7.primary_rows_verdict_differs.v1` | 0 | 0 | 0.000000 | ok | - | primary rows whose verdict class differs from the report's |
| `final.fig7.top_marker.real_n_units` | 142 | 142 | 0.000000 | ok | - | real units of the public reference (class pairs) |
| `final.fig7.top_marker.real_n_units_source_report` | 211 | 211 | 0.000000 | ok | - | number in the source report (with ROSMAP) |
| `final.fig7.top_marker.real_max` | 9.7616 | 9.7616 | -0.000038 | ok | - | real_max, public datasets only |
| `final.fig7.nb_phi.real_q50` | 0.2345 | 0.2345 | -0.000047 | ok | - | real_q50, public datasets only |
| `final.fig7.nb_phi.real_max` | 0.9988 | 0.9988 | 0.000028 | ok | - | real_max, public datasets only |
| `final.fig7.zero_excess.real_max` | 0.0366 | 0.0366 | 0.000044 | ok | - | real_max, public datasets only |
| `final.fig7.v1.primary_class_rows` | 10 | 10 | 0.000000 | ok | - | primary rows of family class, prior v1_late |
| `final.fig7.v1.primary_class_rows_too_low` | 10 | 10 | 0.000000 | ok | - | of them with verdict too low |
| `final.fig7.class_granularity.rows_naming_rosmap` | 0 | 0 | 0.000000 | ok | - | fig7__class_granularity.csv: groups that name ROSMAP (must be 0) |
| `final.fig1.total_row.belongs_to_operator` | not applicable (total row) | not applicable (total row) |  | ok | - | fig1__architecture_modules.csv: row TOTAL, column belongs_to_operator |
| `final.fig1.sum_with_total_row` | 24659778 | 24659778 | 0.000000 | ok | - | sum of parameter_count over ALL rows (twice the model: the TOTAL row must be left out) |
| `final.fig2.model_means.refused_rows` | tabpfn35 all | tabpfn35 all |  | ok | - | fig2__model_means.csv: model and view of the rows with status refused |
| `final.fig2.model_means.ncm_nll_status` | not_run | not_run |  | ok | - | status of the NLL rows of the nearest-class-mean models |
| `final.fig2.cells.status_values` | not_run; ok; refused | not_run; ok; refused |  | ok | - | fig2__cells.csv: values of status |
| `final.tabpfn_note.fig2__cells` | 0 | 0 | 0.000000 | ok | - | fig2__cells.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.tabpfn_note.fig2__cells_wide` | 0 | 0 | 0.000000 | ok | - | fig2__cells_wide.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.tabpfn_note.fig2__model_means` | 0 | 0 | 0.000000 | ok | - | fig2__model_means.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.tabpfn_note.fig2__inputs_and_cost` | 0 | 0 | 0.000000 | ok | - | fig2__inputs_and_cost.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.tabpfn_note.fig2__library_column_use` | 0 | 0 | 0.000000 | ok | - | fig2__library_column_use.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.tabpfn_note.fig4__default_series` | 0 | 0 | 0.000000 | ok | - | fig4__default_series.csv: TabPFN-3.5 rows WITHOUT the licence note (must be 0) |
| `final.fig2.sd20.cellpfn_g1v2p.all.B1.min` | 4.2335 | 4.2335 | 0.000040 | ok | - | fig2__cases.csv: cellpfn_g1v2p, gene_view all, SD over the 20 draws per panel: smallest of the four panels |
| `final.fig2.sd20.cellpfn_g1v2p.all.B1.max` | 12.8551 | 12.8551 | -0.000003 | ok | - | largest of the four panels |
| `final.fig2.sd20.cellpfn_g1v2p.all.B100.min` | 0.6106 | 0.6106 | 0.000049 | ok | - | fig2__cases.csv: cellpfn_g1v2p, gene_view all, SD over the 20 draws per panel: smallest of the four panels |
| `final.fig2.sd20.cellpfn_g1v2p.all.B100.max` | 1.2325 | 1.2325 | 0.000018 | ok | - | largest of the four panels |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_ood.B1.draw0` | -14.5313 | -14.5313 | 0.000005 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_ood.B1.draw1` | -7.3168 | -7.3168 | -0.000049 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_ood.B1.draw2` | 13.7443 | 13.7443 | -0.000033 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_dev.B1.draw0` | -7.5807 | -7.5807 | 0.000032 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_dev.B1.draw1` | -11.0192 | -11.0192 | -0.000024 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_scgpt.zebra_dev.B1.draw2` | -0.0590 | -0.0590 | 0.000037 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_geneformer.zebra_dev.B10.draw0` | 2.0352 | 2.0352 | 0.000010 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_geneformer.zebra_dev.B10.draw1` | 6.5822 | 6.5822 | 0.000030 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.per_draw.cellpfn_minus_geneformer.zebra_dev.B10.draw2` | -1.1151 | -1.1151 | 0.000045 | ok | - | fig4__cases.csv joined with fig4__default_series.csv (role main_best_per_family) on series_id and panel; the two families paired by draw |
| `final.fig4.pbmc_l1.B100.highest_family` | tabicl_finetune | tabicl_finetune |  | ok | - | family with the highest mean over the 3 draws |
| `final.fig4.pbmc_l1.B100.highest_minus_second` | 0.6250 | 0.6250 | 0.000000 | ok | - | highest minus second-highest family mean |
| `final.fig4.n_lines_by_series_id` | 9 | 9 | 0.000000 | ok | - | distinct series_id of the main series on the four core panels (9: the CellPFN line has two) |
| `final.fig4.n_lines_by_family` | 8 | 8 | 0.000000 | ok | - | distinct families (8 lines) |
| `final.fig4.scgpt_lr.mean12` | 69.3745 | 69.3745 | -0.000033 | ok | - | fig4__best_per_family.csv: scgpt_lr, mean_ba_pct_own_input |
| `final.fig4.scgpt_ncm.mean12` | 69.3835 | 69.3835 | -0.000033 | ok | - | scgpt_ncm |
| `final.fig5.reference_scatter.pct_exact_below_minus_1e-4` | 29.3690 | 29.3690 | 0.000015 | ok | - | fig5__ko_pairs_by_cell__pbmc.csv, reference case: share of points with exact_ko_margin < -1e-4 |
| `final.fig5.reference_scatter.pct_exact_below_0` | 30.0663 | 30.0663 | -0.000010 | ok | - | share with exact_ko_margin < 0 |
| `final.fig5.cost.exact_ko_status` | inferred | inferred |  | ok | - | fig5__cost_by_route.csv: status of every exact-knockout-of-all-genes row |
| `final.fig5.cost.dsloo_load_matched_status` | measured | measured |  | ok | - | status of the load-matched DS-LOO rows |
| `final.fig5.fidelity.n_values.ig16_margin` | 12 | 12 | 0.000000 | ok | - | rows of ig16_margin under faithfulness_summary.csv / rho_cell_q |
| `final.fig5.fidelity.n_values.ig64_margin` | 8 | 8 | 0.000000 | ok | - | rows of ig64_margin |
| `final.supp_rosmap.export_scope.core` | 332 | 332 | 0.000000 | ok | - | supp_rosmap__auc.csv: rows with export_scope core (AUC with a printed interval) |
| `final.supp_rosmap.export_scope.wider` | 586 | 586 | 0.000000 | ok | - | rows with export_scope wider |
| `final.supp_rosmap.earlier_unmatched_rows` | 36 | 36 | 0.000000 | ok | - | rows of the earlier unmatched run |
| `final.supp_rosmap.core_rows_without_interval` | 0 | 0 | 0.000000 | ok | - | core rows without ci_low / ci_high (must be 0) |

## A8d refresh (2026-10-11, after the A8 read-out of 19:39 UTC)

48 checks, 0 mismatches.

| check | recomputed from data/ | expected | difference | result | in builder text | how |
|---|---|---|---|---|---|---|
| `refresh_a8d.outcomes.n_replicates` | 3 | 3 | 0.000000 | ok | - | supp_prior_ablation__outcomes.csv, arm A8d: n_replicates |
| `refresh_a8d.outcomes.rule_7_3` | UNRESOLVED | UNRESOLVED |  | ok | yes | arm A8d: rule_10_3_reading_reported_only (for the A8 arms: rule 7.3 on three replicates) |
| `refresh_a8d.outcomes.counted_guard_failures` | none | none |  | ok | yes | arm A8d: counted_guard_failures |
| `refresh_a8d.signs_of_the_three_differences` | - + + | - + + |  | ok | - | supp_prior_ablation__replicates.csv, arm A8d, decisive metric: sign of diff_improvement_signed for r42 r43 r44 |
| `refresh_a8d.n_differences_beyond_band` | 1 | 1 | 0.000000 | ok | - | of the three differences, how many exceed band_eff (fewer than two: the extension short cut of the frozen rule) |
| `refresh_a8d.gap_shrink.r42` | -0.1989 | -0.1989 | 0.000022 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv, arm A8d: gap_shrink |
| `refresh_a8d.gap_shrink.r43` | 0.4704 | 0.4704 | -0.000040 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv, arm A8d: gap_shrink |
| `refresh_a8d.gap_shrink.r44` | -0.0582 | -0.0582 | -0.000035 | ok | yes | supp_prior_ablation__a8_gap_shrink.csv, arm A8d: gap_shrink |
| `refresh_a8d.gap_shrink.mean` | 0.0711 | 0.0711 | -0.000018 | ok | yes | mean over the 3 replicates |
| `refresh_a8d.mechanism_confirmed_M` | no | no |  | ok | yes | arm A8d: mechanism_confirmed_M |
| `refresh_a8d.label_in_gap_file` | NOT_TESTABLE (proxy headroom) | NOT_TESTABLE (proxy headroom) |  | ok | yes | arm A8d: label (the same label as in the outcomes file) |
| `refresh_a8d.headroom_below_keep` | yes | yes |  | ok | yes | headroom_HR < keep: the reason why the label is NOT_TESTABLE and not DROP |
| `refresh_a8d.r43.model_metrics.rows` | 5 | 5 | 0.000000 | ok | - | supp_prior_ablation__model_metrics.csv: rows of A8d replicate r43 |
| `refresh_a8d.r43.model_metrics.rows_status_ok` | 5 | 5 | 0.000000 | ok | - | of them with status ok |
| `refresh_a8d.r43.model_metrics.rows_with_deviation_note` | 5 | 5 | 0.000000 | ok | - | of them whose note states the deviation (one invalid task skipped, on the owner's decision) |
| `refresh_a8d.r43.replicates.rows` | 5 | 5 | 0.000000 | ok | - | supp_prior_ablation__replicates.csv: rows of A8d replicate r43 |
| `refresh_a8d.r43.replicates.rows_status_ok` | 5 | 5 | 0.000000 | ok | - | of them with status ok |
| `refresh_a8d.r43.replicates.rows_with_deviation_note` | 5 | 5 | 0.000000 | ok | - | of them whose note states the deviation (one invalid task skipped, on the owner's decision) |
| `refresh_a8d.r43.a8_gap_shrink.rows` | 1 | 1 | 0.000000 | ok | - | supp_prior_ablation__a8_gap_shrink.csv: rows of A8d replicate r43 |
| `refresh_a8d.r43.a8_gap_shrink.rows_status_ok` | 1 | 1 | 0.000000 | ok | - | of them with status ok |
| `refresh_a8d.r43.a8_gap_shrink.rows_with_deviation_note` | 1 | 1 | 0.000000 | ok | - | of them whose note states the deviation (one invalid task skipped, on the owner's decision) |
| `refresh_a8d.r43.a8_gap_cases.rows` | 40 | 40 | 0.000000 | ok | - | supp_prior_ablation__a8_gap_cases.csv: rows of A8d replicate r43 |
| `refresh_a8d.r43.a8_gap_cases.rows_status_ok` | 40 | 40 | 0.000000 | ok | - | of them with status ok |
| `refresh_a8d.r43.a8_gap_cases.rows_with_deviation_note` | 40 | 40 | 0.000000 | ok | - | of them whose note states the deviation (one invalid task skipped, on the owner's decision) |
| `refresh_a8d.cases.n_proxy_models` | 42 | 42 | 0.000000 | ok | - | supp_prior_ablation__cases.csv: distinct model_id |
| `refresh_a8d.cases.rows_a8d_r43` | 1069 | 1069 | 0.000000 | ok | - | rows of s1_a8d_r43 |
| `refresh_a8d.cases.rows_a8d_r42` | 1069 | 1069 | 0.000000 | ok | - | rows of s1_a8d_r42 (the same cases) |
| `refresh_a8d.a8_gap_cases.n_proxy_models` | 12 | 12 | 0.000000 | ok | - | supp_prior_ablation__a8_gap_cases.csv: distinct model_id |
| `refresh_a8d.stage1_files.rows_not_run` | 0 | 0 | 0.000000 | ok | - | rows with status not_run in the model-metrics, replicates and gap-shrink files (none since A8d r43 exists) |
| `refresh_a8d.hard_tier.a8d.n_replicates_with_value` | 2 | 2 |  | ok | yes | supp_prior_ablation__hard_tier_deltas.csv, stream a8d: n_replicates_with_value (left as it is: the tier was scored before a8d_r43 existed) |
| `refresh_a8d.hard_tier.a8d.replicates_with_status_ok` | r42;r44 | r42;r44 |  | ok | - | replicates of a8d with a value on the hard-class tier |
| `refresh_a8d.stored_zeros.proxy_gap_cases.a8d_replicates` | 42;43;44 | 42;43;44 |  | ok | - | supp_stored_zeros__proxy_gap_cases.csv, arm a8d: task_draw_replicate |
| `refresh_a8d.stored_zeros.proxy_gap_cases.n_proxy_models` | 12 | 12 | 0.000000 | ok | - | supp_stored_zeros__proxy_gap_cases.csv: distinct model_id |
| `refresh_a8d.stored_zeros.proxy_gap_cases.rows_a8d_r43` | 80 | 80 | 0.000000 | ok | - | supp_stored_zeros__proxy_gap_cases.csv: rows of s1_a8d_r43 (40 cases x 2 settings) |
| `refresh_a8d.stored_zeros.proxy_gap_cases.rows_a8d_r43_status_ok` | 80 | 80 | 0.000000 | ok | - | of them with status ok |
| `refresh_a8d.stored_zeros.proxy_gap_cases.rows_a8d_r43_with_deviation_note` | 80 | 80 | 0.000000 | ok | - | of them whose note states the deviation (one invalid task skipped, on the owner's decision) |
| `refresh_a8d.stored_zeros.a8d_gap_shrink_from_proxy_file.r42` | -0.1989 | -0.1989 | 0.000022 | ok | yes | supp_stored_zeros__proxy_gap_cases.csv: gap of b0 minus gap of a8d in the same replicate (gap = per model the mean over the 4 cells of panel_12325_genes minus processed_panel); the same quantity as refresh_a8d.gap_shrink.r42, from the method block's file |
| `refresh_a8d.stored_zeros.a8d_gap_shrink_from_proxy_file.r43` | 0.4704 | 0.4704 | -0.000040 | ok | yes | supp_stored_zeros__proxy_gap_cases.csv: gap of b0 minus gap of a8d in the same replicate (gap = per model the mean over the 4 cells of panel_12325_genes minus processed_panel); the same quantity as refresh_a8d.gap_shrink.r43, from the method block's file |
| `refresh_a8d.stored_zeros.a8d_gap_shrink_from_proxy_file.r44` | -0.0582 | -0.0582 | -0.000035 | ok | yes | supp_stored_zeros__proxy_gap_cases.csv: gap of b0 minus gap of a8d in the same replicate (gap = per model the mean over the 4 cells of panel_12325_genes minus processed_panel); the same quantity as refresh_a8d.gap_shrink.r44, from the method block's file |
| `refresh_a8d.stored_zeros.facts.a8d_label` | NOT_TESTABLE (proxy headroom) | NOT_TESTABLE (proxy headroom) |  | ok | yes | supp_stored_zeros__facts.csv, key a8d.label |
| `refresh_a8d.stored_zeros.facts.a8d_label_equals_outcomes_file` | yes | yes |  | ok | yes | the same label as outcome_label_frozen_applier of arm A8d in supp_prior_ablation__outcomes.csv |
| `refresh_a8d.stored_zeros.facts.a8d_deltas_decisive_metric` | -0.43 / +0.60 / +0.87 | -0.43 / +0.60 / +0.87 |  | ok | yes | supp_stored_zeros__facts.csv, key a8d.deltas_decisive_metric |
| `refresh_a8d.stored_zeros.facts.a8d_deltas_agree_with_replicates_file` | yes | yes |  | ok | yes | the three printed differences equal diff_improvement_signed of supp_prior_ablation__replicates.csv at two decimals |
| `refresh_a8d.stored_zeros.facts.a8d_mean_gap_shrink` | +0.07 | +0.07 |  | ok | yes | supp_stored_zeros__facts.csv, key a8d.mean_gap_shrink |
| `refresh_a8d.stored_zeros.facts.a8d_guard_failures` | none | none |  | ok | yes | supp_stored_zeros__facts.csv, key a8d.guard_failures |
| `refresh_a8d.stored_zeros.facts.a8_keep_threshold` | 1.5000 | 1.5000 | 0.000000 | ok | yes | supp_stored_zeros__facts.csv, key a8.keep_threshold |
| `refresh_a8d.stored_zeros.facts.r43_deviation_equals_ablations_note` | yes | yes |  | ok | yes | key a8d.r43_training_deviation: the same sentence as note of the A8d r43 row in supp_prior_ablation__a8_gap_shrink.csv |
| `refresh_a8d.stored_zeros.facts.rows` | 71 | 71 | 0.000000 | ok | - | supp_stored_zeros__facts.csv: rows |

