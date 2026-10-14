# Project truth

Target: Nature Biotechnology Article. Primary audience: computational and experimental researchers in single-cell biology.

Central argument: a cellular data-generating prior supports competitive gene-anonymous inference with a compact PFN and limited training-task exposure; the same prior can improve pretrained tabular models through continued training.

The simulator is the prior, not merely a source of augmentation. PFN training amortizes support-conditioned prediction across tasks drawn from that prior. Real-cell transfer establishes empirical utility; exact Bayesian optimality is not established.

Synthetic-only refers to model-weight training. Aggregate real-data statistics and development evaluations informed prior design and model development.

Wave 1 established quantitative Results and the complete export index. Wave 2 adds code-grounded Methods, five technical tables and one editable architecture figure, plus independent review of the frozen Wave 1 manuscript. Wave 3 covers the remaining figures. Discussion and submission materials remain deferred.

Current harmonized export, including its 2026-10-13 refresh, controls experimental facts. Earlier prose and code notes are subordinate when they refer to a different model or experiment.

The actual training recipe is explicit: the reference CellPFN saw 320K episodes under the baseline prior and 64K under the cellular prior; tabular cellular adaptation uses the cellular prior throughout. Raw IDs remain in provenance. Shared prior means the simulator-defined cellular prior family, not identical distributions across training stages.

The simulator is reusable CPU software with NumPy/PyTorch computation, typed streams, fixed biology reuse, independent producers and annotated exports. No completed simulator-only throughput benchmark is available; archival timing claims are excluded. Spatial utilities are optional and not active in evaluated CellPFN training.
