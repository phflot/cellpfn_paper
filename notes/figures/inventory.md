# Wave 3 figure inventory

**Delivered:** 14 rendered assets representing three main figures and nine supplementary figures. S1 and S7 each use two assets. Both existing main tables are retained. Figure 4 remains reserved for new validation; it has no fabricated or empty result panel.

The inventory below reflects the PDF/SVG/PNG assets and quantitative JSON manifests integrated into the canonical manuscript. “Delivered” denotes the current evidence package, not submission readiness or independent external validation.

| Figure | Delivered asset stem(s) | Main claim and evidence boundary |
|---|---|---|
| **1** | `architecture` | The reusable simulator supplies CellPFN training and adaptation of pretrained tabular models through explicit tensor/task interfaces. Schematic capabilities are distinct from measured throughput. |
| **2** | `figure2` | The cellular prior supports competitive compact inference and improves pretrained tabular models in some settings; adaptation and retention tradeoffs remain visible. |
| **3** | `figure3` | RNA expression gives biological context for gene-deletion explanations, whose fidelity is evaluated against the specified model-deletion target. Marker agreement is descriptive, not causal validation. |
| **S1** | `supp_figure1`; `supp_figure1_illustration` | Calibration broadens biological-effect coverage but retains excessive separability and other mismatches. Panels m,n illustrate one predetermined synthetic draw; they are not a second realism benchmark. |
| **S2** | `supp_figure2` | Performance varies across methods, annotation resolutions and biological collections; complete subgroup results qualify headline averages. |
| **S3** | `supp_figure3` | Gene coverage, requested versus realized HVG widths and missing-assay encoding affect comparisons. |
| **S4** | `supp_figure4` | Operator effects depend on support and gene coverage; the original prespecified overall criterion failed. Trained ablations and inference interventions remain separate. |
| **S5** | `supp_figure5` | Task restriction improves proxy low-support accuracy while changing composition and exposure and creating calibration tradeoffs. All ten candidates, including undecidable cases, are represented. |
| **S6** | `supp_figure6` | Strong sex-positive-control performance contrasts with near-chance broader sex performance and heterogeneous age results. Reused persons/GSM groups are not independent cohorts. |
| **S7** | `supp_figure7_maps`; `supp_figure7_markers` | Shared RNA coordinates expose annotation, errors, study context and expression/attribution patterns without discarding query cells. Unexplained cells remain identifiable. |
| **S8** | `supp_figure8` | Deletion fidelity is strong on the evaluated gene sets, while explanation coverage, stability and marker ranks remain conditional on task context. |
| **S9** | `supp_figure9` | Existing logs quantify specific computations but do not establish universal or controlled comparative speed advantages. |

Quantitative figures have panel/source manifests and source CSVs under `figures/source_data/`; biological coordinates and preparation receipts are in `figures/biological_data/`. Dense marks may be rasterized; labels and axes remain editable. The architecture schematic retains its editable SVG and source-generation instructions.

## Biological populations actually shown

All real-data maps use the reference checkpoint at update 96,000 and support draw 0. RNA geometry is fitted once on the exact support/query union without labels; display coordinates do not enter classifier inference. Counts are normalized for visualization; already processed cortex expression is preserved. Actual preparation parameters and hashes are in each case JSON.

| Map | Supports | Queries displayed | Cells with cached explanations |
|---|---:|---:|---:|
| Hao PBMC, eight coarse classes | 800 (100/class) | 320 | 191 |
| Hao PBMC, twenty fine classes | 200 (10/class) | 800 | None |
| Human ZEBRA cortex, development, four broad classes | 40 (10/class) | 7,769 | 96 |
| Human ZEBRA cortex, held studies, four broad classes | 40 (10/class) | 7,163 | None |

ZEBRA is human cortex, not zebrafish. The explanation cells are a selected correctly classified subset; maps retain all queries. PBMC expression/attribution overlays include IL7R and NKG7; cortex overlays include PLP1 and CLDN5. Other marker comparisons retain their documented selections. The synthetic illustration shows all 16,384 cells from one eight-donor/eight-type bank, selected before generation (root 44, task-stream seed 42), with anonymous genes. Kidney comparisons and sex/age endpoints are quantitative panels rather than additional new biological maps.

## Reproducibility and M01

1. **Offline redraw:** the Python figure scripts redraw the quantitative panels and saved biological coordinates from local exports/source data. No model checkpoint, new inference or remote data access is needed for this tier.
2. **Remote coordinate regeneration:** real maps require the frozen case matrices, identities and cached predictions/attributions on Rift plus the recorded Scanpy environment. The synthetic illustration additionally requires the pinned simulator/model repositories and configuration. These derivative operations use CPU resources and do not retrain classifiers.
3. **New scientific experiments:** frozen external evaluation, cross-species transfer, corrected ROSMAP, harder variables, independent training-seed replication and controlled timing need new experimental receipts. They cannot be obtained by redrawing current artifacts.

**M01 is closed for method/provenance completeness.** Recovered production code specifies pool replacement, the operator scalar branch, omitted cross-gene whitening coupling and first-order depth/detection corrections. All 52 historical JSONs match export hashes; seven checkpoint-pinned modules are archived and verified. The corrected fidelity fixtures were recomputed from original arrays for twelve case/model combinations: 24 metrics match the export within `4.97e-7`. This is cached-output reconciliation, not fresh checkpoint inference. The approximation has no analytical error bound. See `attribution_code_audit.md` and the two `evidence/remote_*` validation/source manifests.

## Reserved Figure 4: required inputs

The figure will test transfer beyond the development collections. It requires the selected species/cohorts and label releases; frozen checkpoint and splits; a decision between separate within-species evaluation and cross-species support-to-query transfer; and an ortholog/feature correspondence rule for the latter. Corrected ROSMAP additionally requires final donor/label crosswalks, exclusions, endpoints, matched splits and approved data/export access. Harder variables need prespecified outcomes and appropriate covariate/expression baselines before comparative results are inspected. Every module needs prediction-level outputs, biological evaluation units and suitable uncertainty. Existing provisional ROSMAP aggregates do not fill this figure. The complete dependency specification is `figure4_spec.md`.
