# Illustrative cellular-prior bank

Supplementary Figure S1 panels **m,n** are delivered as `figures/supp_figure1_illustration.{svg,pdf,png}` (180 × 90 mm), preserving the existing quantitative S1 asset. Both panels use exactly the same unsupervised RNA coordinates, coloured by simulated type or donor. All 16,384 cells are displayed; no labels enter PCA, neighbours or UMAP. The panel is explicitly illustrative, not a realism validation or performance result.

## Selection and execution

Bounded read-only searches of the supplied realism snapshots, synthetic-reference parts, calibration and judgment directories did not locate a saved count bank. Therefore generated **one** bank in the authorized new derivative directory `cellpfn_paper_figures/synthetic_illustration` on Rift. No original artifact was changed.

Predeclared selection: build a four-bank schedule with root start 42, task-stream seed 42 and mature curriculum offset 10,000; take the first mean-program specification, root **44**, before generating or viewing any data. Only that bank was generated. Shape: eight donors × eight types × 256 cells × 8,192 anonymous genes; storage is lossless `uint16`. No bank search or visual screening occurred.

- Hashprompt revision: `c06f99df609e4931828d8ebdceac27556c88b455`.
- Simulator revision: `6c4d2d0e52db8f8ede6c662aa2b0c641454d73b9`.
- Principal config: `foundation_realism_v22_B_usage.yaml` with current main's resolved chain identity `cc68d5c1d32854b56e61d83b884705dfe16adb00a5f1b7616f282af7bb7aa428`.
- Bank array identity: `c5c54a81e5bb254b510514d820d4c7ff5deb9f0460ccdce059eb7b8adf98ab9e`.
- CUDA remained uninitialized. Environment limits were four CPU threads; the generator's worker initialization sets Torch to one thread. No training or GPU work was launched.
- The environment's default simulator import pointed at a different checkout; the script explicitly bound and asserted the audited main source paths before generation, without modifying any installed environment or repository.

The generation receipt records approximately 41 seconds for this bank and 87 seconds for the entire derivative operation. These are incidental execution diagnostics, **not a controlled throughput benchmark** and not a basis for simulator-speed or comparative-scaling claims.

## Coordinates and preservation

Normalize counts to 10,000 per cell; log1p; select exactly 2,000 HVGs using Scanpy's Seurat dispersion flavor; 50 ARPACK principal components; Euclidean 15-neighbour graph; UMAP `min_dist=0.3`, seed 42. No batch correction or label-driven optimization. Both plots use identical limits, coordinates and deterministic point order, with rasterized marks and editable labels.

The full generated count bank remains on Rift as `counts.npy`. The local manuscript stores coordinate CSV, anonymous selected-gene CSV and full JSON generation/configuration receipt under `figures/biological_data/synthetic_illustration*`. Retrieved CSV hashes match the remote receipt. Per-panel source data and figure manifests are additionally provided by the common figure builder.

## Checks

- All 64 donor/type groups have exactly 256 cells.
- All coordinates are finite and all eight type/donor labels are represented.
- Source revisions, module paths, mature-prior status, root, shape and output hashes are asserted.
- Render-time alignment passes. PDF text minimum is 6 pt. Rendered collision audit: zero FAIL and zero WARN. Complete preview inspected.
- Caption is 91 whitespace-delimited words, including its title.

Reproduction: run `scripts/figures_synthetic.py --generate <authorized derivative directory>` on Rift using the named main repositories and existing CPU environment, then retrieve the three synthetic CSV/JSON outputs and run `python scripts/figures_synthetic.py` locally. A completed derivative is reused; an unfinished count file triggers refusal to overwrite silently.

The compact existing captions were also updated in both `figures_prior.py` and their TeX files: S1 177 words, S4 184, S5 193, S6 185. Their quantitative graphics and scientific selections are unchanged.
