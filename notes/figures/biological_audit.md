# Supplementary Figure S7 biological maps

The figure uses two continuation assets under one supplementary figure number:

- `supp_figure7_maps`: fine-PBMC and held-study cortex annotation/prediction/error views, plus coarse-PBMC donor and development-cortex study context (panels a–h).
- `supp_figure7_markers`: IL7R/NKG7 and PLP1/CLDN5 expression and signed-attribution overlays (panels i–p).

Implementation: `scripts/figures_biological.py`. Separate legend bodies: `sections/legend_supp_figure7_maps.tex` (a–h) and `sections/legend_supp_figure7_markers.tex` (i–p). Shared per-panel source files are in `figures/source_data/supp_figure7` and explicitly linked and hashed in each asset manifest.

## Inputs and invariants

The renderer consumes the remote-derived `figures/biological_data/{case}.csv` and its matching JSON receipt. It verifies the full CSV SHA-256 against the receipt, unique observation IDs, finite coordinates, declared query counts, exact prediction/correctness agreement, explained-cell counts and the receipt's balanced accuracy. The producer previously verified case manifests, stored-logit IDs, class/gene order, count/processed mode and attribution alignment; the renderer performs no new cell-index join.

Expected populations: coarse PBMC 320 queries / 191 explained; fine PBMC 800 queries; development cortex 7,769 queries / 96 explained; held-study cortex 7,163 queries. Every query is retained. The renderer reuses the supplied coordinates and makes no additional embedding, normalization, model inference or sampling. Fine-PBMC and cortex views have independent RNA coordinate frames; overlays within each case share exactly the same coordinates and limits.

## Visual and scientific choices

- Coarse cortex colors match `CLASS_COLORS` in the main biological figure. Fine PBMC uses one explicit twenty-category palette, identical for reference and predictions.
- Categorical draw order uses a fixed seed-42 permutation to avoid a class-ordered stack without sampling cells. Errors are plotted over a gray correct-cell background.
- Donor/study context uses the main coarse-PBMC and development-cortex cases, matching the main figure and marker panels. No batch integration is introduced.
- Expression uses supplied log1p CP10k for PBMC and supplied processed cortex values. Full observed color ranges are retained; no percentile clipping, smoothing or score rescaling is used.
- Attribution uses symmetric per-gene full observed limits around zero. Every explained cell is shown, including zero scores; unexplained cells remain gray and are never treated as zero attribution. Enlarged outlined attribution points make the sparse 96-cell cortex explanation coverage visible and do not encode effect magnitude.
- Attribution sign is tied to the predicted-versus-fixed-runner-up margin; it is not expression direction, regulation or causality. Selection of correctly classified cells is disclosed.
- Source rows retain cell IDs, coordinates and each panel's displayed values. Dense scatter marks are rasterized; labels, legends, axes and color scales remain editable vector objects.

## Validation status

Both assets rendered and visually inspected after the held-study derivative became available. All four input hashes, query populations, prediction identities, balanced-accuracy receipts and explanation coverage assertions pass. The maps page contains eight panels and the marker continuation contains eight panels; sixteen per-panel source files retain all displayed cells. PDF text-box QA reports no text collisions over the declared 10%-of-smaller-box threshold, no text outside either page and minimum 6-pt text. Canvas sizes are 180 × 180 mm (maps) and 180 × 150 mm (markers). No data filtering was required for layout.
