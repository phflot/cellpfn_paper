# Final figure geometry and collision audit

## Result

All **13 plotted assets** pass alignment checks: **78 named row/column/shared-boundary comparisons and 20 additional edge/center comparisons**, using a 1.5-point physical tolerance. Every saved axis rectangle is inside its declared canvas, no axis rectangles overlap, and each PDF matches its rendering manifest.

The installed `nature-figure` collision auditor was run on all **14 final figure PDFs**, including architecture. All 13 quantitative/biological assets now report **zero failures and zero warnings**. The architecture produces nine raw text/text failures, all individually resolved as false positives: Cairo combines multiple text baselines into a trace rectangle, although the actual rendered lines are separated. For each finding, the audit locates each text fragment uniquely in normalized glyph traces, constructs its own per-character bounding union, and verifies zero intersection. Those geometry proofs, exact PDF hashes and raw findings are retained. Enlarged architecture crops and the native PNG were inspected; no architecture editing was necessary.

No unresolved figure collision remains. These are layout checks, not statistical or accessibility certification.

## Corrections made after the first collision pass

- **Figure 2:** moved gray exposure annotations from crowded curve points into the unused lower panel area. Panel-specific Geneformer/scGPT exposure meanings remain unchanged. Added lower space for the trajectory legend so its TabICLv2 label no longer intersects a generic-control point.
- **S7 maps:** moved raw error counts below the map rectangles, removing their contact with displayed query points and background edges.
- **S7 context headers:** manually anchored panel g/h letters and titles to the same figure-coordinate baseline. Their map geometry and equal-aspect scaling are unchanged. Saved axis JSON lacks text-anchor information, so this header alignment was additionally checked by inspection.

Only Figure 2 and S7 map assets were rerendered for these corrections. Data values, cell populations, selections, scientific transformations and source CSVs are unchanged.

## Explicit geometry design

Equal-size tests apply only within comparable groups. The audit records intentional distinctions rather than forcing every rectangle to the same dimensions:

- Figure 2: four equal benchmark plots; one spanning heatmap; two equal bottom plots.
- Figure 3: two RNA-map pairs, three equal gene matrices with corresponding colorbars, and three intentionally unequal bottom plots.
- S1: a regular four-by-three diagnostic grid; the illustration uses two equal coordinate overlays.
- S2: a spanning benchmark, tall ten-task matrix and shorter kidney matrix. Shared tops and widths are checked; the exposure paragraph is a text-only axis.
- S3: two aligned columns with a taller middle row for fifteen study labels.
- S4: three top panels; a two-column criterion panel beside a one-column intervention panel below.
- S5: a large accuracy endpoint block beside separate donor-AUC and NLL blocks; lower rows align in two columns. The two nested upper-right blocks have a documented independent gutter.
- S6 and S8: regular columns with content-dependent row heights.
- S7: per-case equal maps retain their original aspect ratios, so cross-case columns are checked by centers rather than forced width. Colorbars have separate row/column rules. The fine-class legend is text-only.
- S9: an equal two-by-two cost grid.

## Reproduction and verification

Refresh the audit after changing figure assets:

```bash
python scripts/audit_figure_layout.py
```

The full audit uses the installed `audit_panel_alignment.py` and `audit_figure_collisions.py`; `--skill-dir` can override their location. The optional PyMuPDF environment is selected with `--qa-python-path` (currently `/tmp/cellpfn_figure_qa_deps`). Tool-source hashes are recorded in the summary. The full run performs no rendering and changes only audit outputs.

For ordinary manuscript verification, use the **standard-library-only, read-only** command:

```bash
python scripts/audit_figure_layout.py --check
```

This checks all current PDF and geometry-manifest hashes, the audit implementation hash, the machine-report hashes, all reviewed verdicts and every architecture disposition. It requires neither the skill installation nor PyMuPDF. A changed figure, audit implementation or machine report requires a refreshed full audit; stale receipts do not pass.

Machine results: `output/review/figures/layout_audit/summary.json`, with per-asset `geometry/` and `collisions/` reports. The architecture's raw failure count remains visible alongside its reviewed PASS verdict. Known false positives are not silently removed from raw outputs.
