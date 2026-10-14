# Project truth

Target: Nature Biotechnology Article. Primary audience: computational and experimental researchers in single-cell biology.

Central argument: a cellular data-generating prior supports competitive gene-anonymous inference with a compact PFN and limited training-task exposure; the same prior can improve pretrained tabular models through continued training.

The simulator is the prior, not merely a source of augmentation. PFN training amortizes support-conditioned prediction across tasks drawn from that prior. Real-cell transfer establishes empirical utility; exact Bayesian optimality is not established.

Synthetic-only refers to model-weight training. Aggregate real-data statistics and development evaluations informed prior design and model development.

Wave 1: abstract, introduction, quantitative Results, two main tables, supporting numerical appendix, bibliography and evidence notes. The entire export receives a semantic index, including negative and exploratory evidence. Wave 2: Methods grounded in code and run configuration after author discussion. Wave 3: figures. Discussion and submission materials deferred.

Current harmonized export, including its 2026-10-13 refresh, controls experimental facts. Earlier prose and code notes are subordinate when they refer to a different model or experiment.

Prior versions are explicit: the reference CellPFN saw320K episodes under v1 and64K under v2.2-B; tabular cellular adaptation uses v2.2-B throughout. Shared prior means the simulator-defined cellular prior family, not identical historical distributions.
