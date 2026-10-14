# Wave 2 implementation contract

Approved 14 October 2026. Target: Nature Biotechnology Article. This wave adds extensive Online Methods, supplementary technical descriptions and one editable overview figure. The simulator is both the cellular prior and reusable software infrastructure. Discussion, further figures, new training, production-code changes and heavy performance benchmarks are outside this wave.

## Source authority

- Software capabilities: hashprompt main `c06f99df609e4931828d8ebdceac27556c88b455`; pyScIntelligentDesign main `6c4d2d0e52db8f8ede6c662aa2b0c641454d73b9`.
- Each evaluated recipe is tied to its export/configuration/checkpoint, including simulator endpoint `76ba3a3d023b462d2749b48d63685dffb5281af3`. Current optional features must not be retroactively assigned to evaluated models.
- All available branch tips are ancestors of main in both repositories. Remote freshness beyond local tracking refs is unverified (network lookup unavailable during audit).
- Frozen export remains numerical authority. Legacy texts supply motivation, never unverified timing numbers.

## Narrative and terminology

The cellular simulator supplies controlled biological tasks both to compact CellPFN and to continued training of existing tabular models. Describe biology, execution architecture, model architecture and experiments distinctly. Use baseline prior and cellular prior in published prose; preserve raw version IDs only in provenance. Report actual training stages without a development narrative. Keep adverse findings that constrain final claims.

## Section contracts

1. Simulator Methods: biological hierarchy, programs, covariates, observation/calibration; configurable initialization, tensor contracts, CPU streaming, process parallelism, bank reuse, extensions, reproducibility and export memory.
2. Model Methods: full dimensioned computation, gene-gene operator and controls, task creation, optimization and tabular adaptation.
3. Evaluation Methods: cohorts, preprocessing, comparator routes, splits, metrics, support-draw uncertainty, ablations and attribution boundaries.
4. Supplement: five technical tables (simulator parameters, software capabilities, architecture, training, evaluation), equations and executable-interface examples.
5. Figure 1: biological prior to runtime to tensor/bank/export outputs to two learning routes; compact CellPFN inset. Editable SVG is authoritative, with PDF/PNG exports. Original graphical abstract remains an unchanged source asset.

## Verification and delivery

Trace claims to source anchors; record inspected versus executed tests. Verify citations and preserve numerical ledgers, exposure markings, tied rankings and open claims. Build once to the canonical `output/cellpfn.pdf` after integration, inspect rendering and rerun affected checks. Single-line commits with Philipp Flotho <PhilippFlotho@gmail.com>, no co-author trailers. Do not alter source repositories or original export.
