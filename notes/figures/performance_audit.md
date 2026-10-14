# Quantitative figure implementation and audit

Implemented by `scripts/figures_performance.py` from the immutable harmonized paper export. Reproduce with:

```bash
MPLCONFIGDIR=/tmp/cellpfn-matplotlib python scripts/figures_performance.py
```

## Outputs

- Figure 2: seven panels, 180 × 175 mm, 450 selected source rows.
- Supplementary Figure S2: four panels, 180 × 190 mm, 674 selected source rows.
- Supplementary Figure S3: six panels, 180 × 190 mm, 249 selected source rows.
- Supplementary Figure S9: four panels, 180 × 180 mm, 44 selected source rows.

Each has PDF, editable-text SVG, 300-dpi PNG, JSON panel manifest, per-panel selected source CSVs, and a LaTeX legend body. Figure titles are embedded once, and legends are supplied as text for the parent manuscript's figure environment. No source export file was modified.

## Scientific selections and exclusions

### Figure 2

Benchmark curves use the same exact inputs and three support draws as Table 1, with unavailable one-shot LDA omitted. CellPFN uses all genes; tabular models use up to 2k HVGs; single-cell encoders use native embeddings. Small points show all three draws; connected symbols are means. Exposure annotations come from the export audit.

Adaptation changes use `fig3__paired.delta` and its matched-run released scores. They are deliberately not computed by subtracting the independent stored benchmark means. The 108 selected records represent three models × four panels × three budgets × three draws. Both harmful and beneficial changes are displayed.

Trajectories retain the declared `c2b_root`, `k2b_root`, and `p1_root` three-draw scoring runs. The stage-0 ten-draw reruns are excluded to avoid duplicating checkpoints with different evaluation draws. Kumo-small task-stream repeats are shown as separate trajectories; all runs have one model training seed. The generic control is named and its unmatched row/column exposure is disclosed.

Retention uses the 120 declared TabICL released/adapted balanced-accuracy records (four datasets × three support budgets × five splits × two states). Small dots are dataset means; large points equally average datasets and splits. No CI across datasets is manufactured.

### Supplementary Figure S2

The 16-row core benchmark uses all declared comparator routes, including the transductive scANVI context. Missing values are dashes. The best overall and best unflagged scores are bolded with decimal half-up ties at displayed precision, matching the manuscript table rule. Flagged values are gray. No score adjustment for exposure is applied.

All eight fine PBMC tasks and both fine cortex tasks use the reference checkpoint's supplied aggregate values; uncertainty is not imported from proxy runs. Class counts, post hoc status and 10/10/5 support-draw design are disclosed. Full core PBMC resolution appears in panel a; finer tasks use the separately supplied up-to-8,192-HVG configuration.

Kidney evaluates both count and processed CellPFN routes on the four cell-type panels. Sex tasks are left to the sex/age supplement. Fold rows are preserved; alternative input modes are not averaged together. Geneformer kidney exposure follows the source audit.

### Supplementary Figure S3

Realized HVG widths are read from case records; one-shot reduced-width examples are not shown as full 8,192-gene inputs. Twenty-draw paired intervals come directly from `fig2__cells`. Random-panel control points are condition means, not independent replicates.

Study-level missing-assay percentages include the study roles in the source CSV. The Stage-0 zero-removal diagnostic keeps processed values and their normalization denominator fixed. Its ten-draw paired intervals are separate from the three-draw count-reconstruction comparison, which changes gene coverage and some support identities.

### Supplementary Figure S9

Adaptation optimizer compute is measured and excludes vendor pretraining, evaluation, startup and checkpoints. GPU-lock waiting is separate. Attribution panels distinguish measured route times, extrapolated all-gene exact times and unexecuted Kumo estimates. For Kumo, processed cortex is selected via `kumo_panel=zebra`; reconstructed-count cortex is excluded to avoid duplicate task labels. No universal model-speed or simulator-throughput claim follows from these timings. Shared-GPU and fp32/fp16 differences remain explicit.

## Validation performed

- All four builders executed successfully, with exact selected-row and uniqueness assertions.
- **138 benchmark means independently reconciled against the existing `evidence/table_values.csv` numerical ledger** to absolute tolerance 1e-10, including overall means.
- Twenty-one panels contain 1,417 selected source rows in total, with SHA-256 fingerprints of source files and rendered outputs.
- Final PNGs visually inspected. Initial main-figure title/legend overlap and timing-panel legend overlaps were corrected. All plotting text is at least 6 pt, with 7-pt axis labels and 8-pt panel letters.
- PDF text-box inspection with PyMuPDF found an exposure-star collision in Figure 2 and dense study labels in S3; star offsets and row heights were corrected. Repeated inspection found no text collisions exceeding 10% of the smaller text box and no out-of-page text in any of the four final PDFs. This screen complements the visual check and does not test marker occlusion.
- SVG text remains editable (`svg.fonttype=none`); PDFs use embedded TrueType fonts. Fixed physical canvas sizes are preserved.
- Source-specific uncertainty units, missing conditions, exposure marks, unflagged ties and post hoc status retained. No new statistical testing or model execution was performed.

## Integration notes

Legend bodies: `sections/legend_figure2.tex`, `sections/legend_supp_figure2.tex`, `sections/legend_supp_figure3.tex`, `sections/legend_supp_figure9.tex`. These files contain no enclosing float/caption commands and no numbering assumptions. The parent manuscript controls figure numbering and placement. Main Figure 2 is 175 mm high and supplementary figures at most 190 mm; lengthy legends may require a following caption page in the manuscript's draft layout.
