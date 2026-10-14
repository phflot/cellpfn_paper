# Wave 2 handoff

Completed 14 October 2026. The canonical manuscript is `output/cellpfn.pdf` (56 pages), with abstract, introduction, quantitative Results, full Methods, Figure1, Tables1–2 and Supplementary TablesS1–S14. Discussion, the remaining figures and submission materials remain later work. This completes the authorized writing/review wave, not the outstanding scientific experiments or submission approval.

## Scientific and technical additions

- Methods covers the prediction task; biological prior and observation model; calibration; simulator software layers, PyTorch interfaces, CPU/process execution, bank reuse and export memory; exact CellPFN tensor computation; no/diagonal/full gene–gene operators; optimization and tabular adaptation; biological data, preprocessing, selection, metrics and attribution.
- Technical supplement gives full simulator parameters, available-versus-evaluated software capabilities, feature definitions and architecture dimensions, training recipes, comparator settings, interface example and source/checkpoint bindings. Main is the software reference, with experiment-specific revisions retained. No historical development narrative or own-project version labels remain in scientific prose.
- Figure1 is the single editable overview. `figures/architecture.svg` and `scripts/build_architecture.py` are its editable sources; PDF/PNG are exports. It preserves the layered study-card idea of the unchanged source graphical abstract and adds the runtime, bank/export routes, two learning applications and both operator integration paths.
- The simulator is described as a CPU NumPy/PyTorch engine with PyTorch-compatible streaming. Its implementation supports reusable task delivery, but no simulator-only throughput benchmark was located. Historical million/billion-cell timing numbers were excluded. `notes/simulator_scalability_protocol.md` is a pending measurement specification, not a completed experiment.

## Review and changes to Wave 1

Three reviewers received the same frozen Wave1 packet in fresh isolated contexts. Their reports were frozen before synthesis and are hash-protected. They found no wrong headline benchmark means or newly demonstrated leakage within their inspected evidence. Their source checks are not raw-data replication.

The review led to substantive additions and clarifications:

- Existing finer cortical tasks now appear alongside the PBMC subtype analysis, with separate label sets and three support budgets. The core cortex benchmark is explicitly four broad compartments.
- HVG labels mean requested caps, with actual one-shot widths recorded; “2k HVGs” remains the table display label.
- The “learnable-only” intervention is now a restricted task mixture, with its metadata/type/identity proportions, covariance-family exclusion and different cell exposure stated.
- Query-source exposure stars, matched-versus-stored adaptation baselines, constrained scANVI recipe, SingleR defaults and the zero one-shot operator gate are explained.
- S8 adds matched IG64 finite-deletion fidelity, margin-versus-logit marker context, the zero-baseline limitation and selected cortex immune-cell scope.

All18 concerns and dispositions are in `notes/reviews/wave1_synthesis.md`. Two additional source checks independently reviewed the new model and simulator Methods. Corrections included the floored neural standard-deviation feature, effective age-dependent gamma shape, expected log-state preservation, strict admission rule and equation notation.

## Verification

`make pdf` and all11 commands in `make check` passed after final source edits. The build has no unresolved citations/references or overfull boxes; some justified table cells produce underfull-box notices. The complete56-page contact sheet and selected full-size pages were inspected, including Table1, Figure1, operator equations, attribution comparison, finer cortex/PBMC tasks, simulator tables and the API-example placement. Portrait-page bounding-box inspection found no text below the body boundary. Temporary review renders are outside the repository; there is one current manuscript PDF.

- 337 numerical extractions/calculations passed, including one arithmetic check with an externally sourced numerator. Three other external-source counts and one unavailable count retain their distinct verification states.
- 1,293 table-value selections and350 displayed-precision ranking/color entries passed. Tied best values and gray exposure flags are preserved.
- The supplied export reconciliation passed1,375 checks with zero mismatches; all288 export files remain indexed.
- All359 original source hashes,14 preserved copies and1,380 source-code files are unchanged. Both code repositories retain their recorded clean status and main revisions.
- Bibliography has56 records and53 cited works, with no missing or duplicate cited keys. Eight added Methods references received targeted primary-source verification; offline syntax checks do not establish reference support independently.
- `make words` uses detex after removing apparatus, floats, longtables and verbatim code, while retaining red narrative. Abstract143; introduction472; Results2,018; current main text2,490, leaving510 under the recorded3,000-word working limit for Discussion. Methods6,279; supplementary Methods prose2,889. Tables and code are additional technical material.

Runtime verification is narrower than manuscript checking. Native-build contract tests had4 passes/1 skip. Standalone spatial-utility tests had4 passes/2 skips/1 existing failure (`test_fast_value_noise_seed_effect`, seeds0/1 differ below the test's `allclose` tolerance). This optional utility is outside the evaluated CellPFN path. No source fix was made. The full simulator/model suites and API example were not executed because the required dependency environment was unavailable. Static parameter arithmetic and source/configuration checks are documented separately; they are not reported as runtime passes.

## Remaining evidence and next wave

O01–O06 remain open for independent evaluation, corrected neuropathology and disease signatures, abstract synthesis, controlled attribution timing and sex-specific gene attribution. M01 additionally records the unavailable production DS-LOO implementation and exact normalization/detection/operator-coupling corrections. The current source describes the deletion target and a bounded pooled approximation; complete implementation reproducibility awaits the named missing artifacts. These gaps remain visible in the PDF.

Before stronger simulator speed claims, run the specified matched throughput/resource benchmark. Before final biological claims, satisfy the closure rules in `notes/open_claims.md`. No review finding is silently closed by wording where new data are needed.

Wave3 may use three further main display items after Figure1 and Tables1–2. Build them from the resolved Results/Methods evidence chain, retaining source-row bindings, support/donor units, negative results and input-view distinctions. No new figure number should be inferred from historical export figure IDs.

Continue from the canonical source and this handoff. `notes/wave1_handoff.md` is historical; do not restore its deferred-Methods status or superseded terminology.
