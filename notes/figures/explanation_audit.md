# Figure 3 and Supplementary Figure 8

## Scientific claim and scope

RNA expression provides biological context; exact query-gene deletion validates
decision-specific explanations. Marker rankings are support- and target-dependent.
No perturbation or causal-biological claim is made. Explanation cases were fixed
before visualization: PBMC coarse, 100 supports/class, draw 0; cortex development,
ten supports/class, draw 0. The selected-cell restriction is explicit.

## Source contract

- `scripts/figures_explanation.py` consumes the immutable `fig5__*.csv` exports.
- Figure 3e uses exactly the Table S8 filters: DS-LOO `rho_cell_corr` from
  `tables/dsloo_vs_exact.csv`; IG64 `rho_cell_q` from
  `tables/faithfulness_summary.csv`; full operator, query-only, evaluated set,
  cell-level Spearman. Duplicate summaries from independent recomputation are not
  averaged with the primary summaries.
- Figure 3d includes every one of the 20,365 exported PBMC 100-support full-model
  cell–gene pairs. Zero and negative effects are retained. It does not present a
  random sample as exhaustive whole-transcriptome validation.
- Figure 3c selects 19 genes by an explicit union: eight class top-1 genes and all
  13 Table S8 marker checks. This includes LYZ and LILRA4. Cross-class values must
  be recovered from complete production arrays, not filled with zero where the
  selected exact-deletion export omitted a class–gene pair.
- The complete 152-entry remote-derived gene matrix is now present. All 45 shared
  class–gene entries reconcile with exported support expression, detection and
  corrected-margin attribution (maximum absolute discrepancies approximately
  4.7e-6, 0 and 2.5e-6, respectively, consistent with export rounding).
- Biological maps require exact-case RNA coordinates with unique observation IDs,
  reference and predicted labels, correctness and explained-subset flags. Their
  expected sizes and explanation counts are asserted. Exported local integer
  attribution-cell IDs are never assumed to be global cell identifiers.
- The two RNA coordinate CSVs and accompanying metadata are now present; their
  hashes and reference checkpoint hash are asserted during rendering. Figure 3's
  manifest incorporates the raw remote source hashes, coordinate preprocessing,
  population definitions and scientific-Python versions from both metadata files.
- Deletion curves use cell-wise ordering, `class_label=ALL`, corrected DS-LOO and
  the pooled random-expressed control; the latter pools two orderings per cell.
  Plotting percentages multiply the stored fractions by 100 exactly once.
- Supplementary panels retain every documented case, no-operator error, marker
  nonhit and selected-cell coverage. The kidney modes share cells and are not
  independent cohorts. Support-budget comparisons are not pure draw comparisons.

## Graphics and numerical review

Python/Matplotlib exports editable text in SVG and embedded fonts in PDF.
Main figure is 180 × 180 mm; supplementary figure is 180 × 190 mm.
Text is at least 6 pt at the native output size. Dense scatters are rasterized
inside the vector document; all axes and text remain editable. Input hashes,
selected source-data tables, aggregation details and geometry are recorded in
each figure JSON. No confidence intervals are invented for summary-only values.

The initial visual inspection detected a fixed x-axis limit that would omit the
12.1% no-operator kidney magnitude error; the final implementation derives the
axis upper limit from all plotted values. All case errors therefore remain visible.
The skill's PDF-text audit passes for Supplementary Figure S8 at a 6-pt minimum.
The rendered collision audit, using the temporary PyMuPDF QA environment,
passes with zero failures and zero warnings after moving the magnitude-error
legend clear of the kidney data and wrapping the validation-subset tick label.
The heatmap text overlays are intentional. The exported preview was inspected
for text collisions, cropping, label correspondence and data limits. The
supplementary figure was shortened to 190 mm so its native type remains legible
when integrated into the manuscript.
Figure 3 also passes the rendered collision audit with zero failures and zero
warnings, and the PDF-text audit with minimum 6-pt type. Its complete final PNG
was inspected after lowering map subtitles and separating colorbar tick labels
from heatmap headings. The reference and error displays reuse the same RNA
coordinates; PBMC shows 25/320 prediction errors and cortex 1,229/7,769. These
error counts are ordinary classification errors, not balanced-accuracy errors.

## Rebuild

Run `MPLCONFIGDIR=/tmp/cellpfn-mpl python scripts/figures_explanation.py` from the
manuscript directory after biological data preparation. `--supplement` rebuilds
S8 without requiring remote-derived UMAP coordinates; `--main` rebuilds only
Figure 3. No checkpoint download, inference or training is performed by this
plotting script.
