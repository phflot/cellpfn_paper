# Simulator Methods: evidence and implementation audit

Written 2026-10-14. Scope: `sections/methods_simulator.tex` and `sections/technical_simulator.tex`. This is a source inspection and limited execution record, not independent experimental validation or author approval.

## Governing implementation and terminology

- Current simulator main: `6c4d2d0`; principal evaluated simulator endpoint: `76ba3a3d023b462d2749b48d63685dffb5281af3`.
- Current CellPFN/hashprompt main: `c06f99d`; principal evaluated model source is separately bound by the training audit to `9e50f8e`.
- Principal configuration: hashprompt `conf/foundation_realism_v22_B_usage.yaml`, resolving its `extends` chain. Historical filenames are retained only here for reproducibility. Manuscript terminology is **cellular prior** and **baseline prior**.
- The biological specification is pinned to the evaluated endpoint. Current-main optional donor cohorts, donor-private on-switches, study-specific detection, study gene absence and metadata interaction machinery are not silently attributed to that endpoint.
- `git diff 76ba3a3 main` showed no changes to simulator `data/dataset.py` or `data_models/aging_clock.py`. It showed additions to `mixed_program_task_distribution.py` (408 insertions/21 deletions) and `foundation_targets.py` (331 insertions/6 deletions). Those current files therefore require function-level endpoint comparison.
- Original repositories and exports remain read-only; no source fixes, merges, training or throughput experiments were performed.

## Source-to-Methods crosswalk

Paths below are relative to the corresponding repository root. Line anchors refer to inspected main unless an endpoint anchor is explicitly given. Function names are the stable cross-reference if lines move.

| Manuscript claim or equation | Primary source anchors | Evidence status and boundary |
|---|---|---|
| Experiment object and provider separation | simulator `data/dataset.py:295` (`BasicDataset`); `data_models/donor_expression_provider.py:10,64` | Inspected protocol, factory dispatch and task-owned provider selection. |
| Four-study topology and 16 generated donors | hashprompt `conf/data_gate_s14_mixed_program_umi.yaml`; simulator `data/dataset.py:708` | Configuration/code; fixed-bank path selects eight donors separately. |
| 2:1:1 mean/marker/covariance family schedule | same configuration, `task_distribution.lane_schedule`; simulator mixed task constructor | Configuration-level schedule, not a universal mixture for optional ablation streams. |
| Heavy-tailed baseline and maximum gene share | simulator `data_models/random_mean_program_task_distribution.py:131,196,209` | Lognormal body and replacement outlier head; baseline share bound is distinct from class-template and cell-level bounds. |
| Weighted centring, energy normalization and tanh saturation | same file `:354,364,385`; mixed task `_build_child_task` | Class weights proportional to baseline power 0.5; saturation 4.5. |
| Class-template admission | same file `class_template_top_shares` and constructor admission loop; final configuration `class_mean_admission` | Maximum share 0.35, maximum 16 attempts. Does not bound every final cell. |
| Marker multimodality and bounded composition | simulator mixed task `:3701` (`_lane_biology`); endpoint `:3358` | Bernoulli activation, lognormal amplitude, marker + class composition before saturation. |
| Signed covariance equation | mixed task `:3274` (`_covariance_latent_rows`), `:3786` | Three paired Rademacher coordinates and six programs. Equal means refer to the specified biological layer, not an unsupported assertion about all transformed observations. |
| Hidden subtypes | mixed task `:2309` (`_build_hidden_subtypes`), `:2353`; endpoint `:2096` | Dirichlet-weighted centring, bounded offsets and optional applicability. |
| Structured cell state equation | mixed task `:2757,2816,2887,2958`; endpoint `:2542,2601,2743` | Program size is lognormal around a drawn median, not uniformly bounded 80–250 genes. Reference scale uses 256 cells/class from a separate namespace. |
| Program activation and donor usage | mixed task `_build_cell_state_programs`, `_build_cell_state_donor_usage` | Positive program loadings; Gaussian donor/program logit offsets; covariance family disables private programs. |
| Metadata construction and effects | simulator `data_models/foundation_targets.py:232,572,649`; endpoint `:497,574` | Copula metadata, linear/nonlinear gene directions; selected/other target decomposition. Direct age contribution disabled under clock. |
| Aging coordinate and exact prepared map | simulator `data_models/aging_clock.py`, `map_age_to_steps`, `_bounded_expression`, `prepare`, `apply_prepared`; `foundation_targets.py:932`; endpoint `:640` | Current aging implementation unchanged from endpoint. Stochastic clipped-coordinate adaptation, not proof of real aging mechanism/prediction. |
| Aging parameter values | final configuration chain `foundation_realism_v22_B_usage.yaml` → `foundation_realism_v21.yaml` → `foundation_realism_v2.yaml` → `foundation_rosmap_moments_meyer_v1.yaml` | SD 0.01/0.005, 105 steps, rate log-SD 0.2, reference depth 1500, ages 60–90, e±1 pre-normalization bounds. |
| Profile equation and single application of metadata/aging | mixed task `:3810` (`canonical_components`); endpoint `:3467` | Includes log-ratio substitution so metadata are not applied twice. |
| Library hierarchy, gamma–Poisson sampling | mixed task `:3996` (`observe_many`); endpoint `:3651` | Counts sampled by NumPy, terminal Poisson once. Expected-count field means realized pre-terminal intensity. |
| Class-template dispersion equation | mixed task `:1630,2719`; endpoint `:2504` | Nominal mean uses template × exp(global log-mean + 0.5 base cell variance). Shape jitter/curve clipped to [0.01,160]. |
| Calibration and development dependence | export `sections/method_realism_misc.md:220–221,291,311,397`; final YAML header | Aggregate summaries from same evaluation panels; no claim of independence from real data. Exact fitted real gene profiles are not training bank templates. |
| General composable observation effects | simulator `data_models/batch_effects.py:302,637`; `data/observation_policy.py` | nn.Module EffectStack interface; general options distinguished from task-owned principal count model. |
| Output count contract | simulator `data/count_contract.py:8`; `data/dataset.py:980` | float32 normalized profiles/intensities and int32 observed counts; shape/validity checks. |
| CPU tensor streaming | simulator `data/dataset.py:1186,1213,1322,1355,1369,1418` | IterableDataset interface; CPU restriction; task batching and shared-stack grouping. Not all-Torch kernels or GPU simulation. |
| RNG ownership and isolation | simulator `utils/runtime_context.py:64,99`; `data/dataset.py:200` | Python/NumPy/Torch CPU state restored under process lock; DataLoader worker cloning rejected. |
| Independent asynchronous task production | hashprompt `src/hashprompt/foundation_task_stream.py:910,1287` | Spawned CPU processes, bounded prefetch, deterministic result order, timeouts and receipts. |
| Bank generation, QC and storage | hashprompt `src/hashprompt/foundation_dataset_reuse.py:882,889,926,1267` | [8,8,256,8192] bank; microbatch 64; up to 8 redraws for low-count rows; uint16 only when lossless. All-zero banks rejected. |
| Model-neutral adaptation bank | hashprompt `src/hashprompt/kumo_cpt_bank.py:1` | Pure NumPy interchange avoids requiring other model environments. |
| Dense/sparse AnnData export and memory calculations | simulator `utils/dataset_helpers.py:140,203,258`; `data/dataset.py:1533,1643` | Dense 12CG bytes allocated plus copies; sparse observed counts still accompanied by two dense layers. Analytical storage terms, not observed peak RSS. |
| H5AD/Zarr/Loom and public/hidden loggers | simulator `simulation/dataset_loggers.py:21,142,188,272` | Implemented exporter modes inspected; not every export backend executed. |
| Optional native accelerator | simulator `s7_batch_rng.py`, `_s7_batch_rng.cpp`, `setup.py`, `s7_build_support.py` | Specific shared-topic RNG backend; exact NumPy version/canaries and fallback. Not a blanket accelerator for the principal mixed task. |
| Usage example | hashprompt `src/hashprompt/dataset/dataset.py:120,382,434`; simulator `CellStream.__iter__` | Signatures and field names inspected. Example explicitly calls `synchronize_task_root_seed`; setting top-level seed alone with `reseed=False` is insufficient. Full example not executed. |

## Parameter table validation

Resolved the complete YAML inheritance chain with a small read-only Python/PyYAML recursive merge and inspected `aging_clock`, `foundation_target`, `copula` and `dataset_reuse_v2`. Compared table values to the individual active configuration blocks. Confirmed the class/nuisance/trajectory/marker/dispersion distribution families from `_draw_hyperparameters` and the constructor's uniform/integer draws. This was a configuration and source audit, not execution of the simulator resolver.

The table describes final prior settings, not every stage that contributed to the final checkpoint. It deliberately distinguishes baseline and current prior semantics from their exact project filenames. Numerical analysis of gamma–Poisson conditional mean/variance and array-memory bytes was derived directly from the implementation's scale convention and dtypes.

## Executed checks

All commands used `PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONPATH=src:.`, and `pytest -p no:cacheprovider`; source-tree caches were not requested.

1. `python3 -m pytest -p no:cacheprovider -q tests/test_s7_build_support.py`: **4 passed, 1 skipped** in 0.07 s. Skip: frozen installed NumPy archive test requires explicit native-runtime opt-in. These tests check build enablement and fail-closed archive/version checks; they do not execute the native RNG backend.
2. `python3 -m pytest -p no:cacheprovider -q tests/test_spatial_noise_modules.py`: **4 passed, 2 skipped, 1 failed** in 0.07 s. Skips: unavailable optional Perlin/simplex dependencies. Failure: `test_fast_value_noise_seed_effect`; seeds 0 and 1 produce differences smaller than `numpy.allclose` tolerance. This is a standalone spatial utility, not the evaluated CellPFN path. It was not fixed during manuscript work.
3. Initial native-build test invocation without disabled plugin autoload failed before collection because an unrelated installed napari plugin attempted unavailable numba caching. The rerun disabled plugin discovery and produced result 1 above.
4. Static new-source checks: equation/longtable/verbatim begin/end counts balanced; no manuscript project `v1`/`v2` tokens. This is not a complete TeX compile (root integration performs that).
5. `git status --short` in the simulator repository remained empty after the test commands.

System Python has NumPy and pytest but lacks torch, OmegaConf and AnnData. Inspected installed Conda environments contain Torch in some cases but no discovered environment contained the full required simulator stack. No dependencies were installed. Count-contract, runtime-isolation, biological-prior, aging, DataLoader and export suites were **not run**; source evidence and existing test definitions must not be reported as passing execution.

## Capability boundaries and remaining verification

- README claims of a threaded sampler are stale relative to main's serialized runtime. Manuscript follows executable code.
- General simulator options include ambient/doublet/panel/FFPE and spatial utilities; these are not all active in the principal model's training. GRN convolution/augmentation prototypes and placeholders are excluded from active-path manuscript claims; their presence is not a completed GRN simulator claim.
- A million-cell chunk is explicitly configured in `AnnDataChunkGenerator`, but this alone establishes neither a completed million-cell run nor throughput superiority. Matched scaling measurements and scDesign3 comparisons belong to the root's performance protocol.
- Public API example is signature-checked, not execution-tested, pending a suitable dependency environment. It writes a minimal count/layer export; production loggers add controlled public/hidden metadata and provenance.
- Sparse observed-count storage is not sparse generation throughout; CPU tensor integration is not GPU simulation or end-to-end differentiability.
- Descriptions of currently available extensions must remain distinct from exact evaluated-run settings. Code hashes and resolved config receipts are retained in provenance, not development chronology in the manuscript.
- Primary bibliography keys used: existing `zappia2017splatter`; root-added `meyer2024stochasticaging`, `paszke2019pytorch`, `harris2020numpy`, `virshup2024anndata`. No additional reference key is needed by these files.
- Missing external calibration artifacts limit retrospective verification of all fitting choices; exported aggregate-calibration description supports the bounded text, not a claim that every available calibration module was used.

## Draft structure and consistency

Main Methods proceeds from experiment architecture to biological variation, observation/calibration, then software interfaces. The technical supplement supplies parameter distributions and capability boundaries, executable API syntax and memory accounting. This separates scientific generative assumptions from implementation reuse without reducing the simulator to a list of biological effects. Canonical terms: pyScIntelligentDesign, CellPFN, cellular prior, baseline prior, expected profile, expected counts/intensity, observed counts, simulation microbatch, fixed biology bank, and episode. Supplementary table labels are `tab:simulator-parameters` and `tab:software-capabilities`; numbering is delegated to integration.

## Independent integration checks

The final independent audit (`notes/reviews/wave2_simulator_check.md`) resolved effective age-dependent gamma shapes and the preservation of the expected log-state shift. Bank QC is per cell: final configuration inherits `dataset_reuse_v2.qc_min_counts=20` from `conf/foundation_realism_v2.yaml:94`; `generate_biology_bank` allows eight deterministic technical redraws, retains the highest-count attempt and rejects a bank containing any remaining zero-count cell. The phrase “all-zero banks rejected” above is weaker than the actual check. No code was changed.
