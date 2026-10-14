# CellPFN model and simulator methods revision

## Scope

This revision deliberately leaves the manuscript story, Abstract, Results and Discussion unchanged. It expands the main Online Methods description of CellPFN and adds citations where the simulator or training description relies on established statistical or machine-learning methodology.

## Model section

The main Methods now includes:

- an operational definition of CellPFN as a prior-data fitted network;
- a complete computation graph from support-row encoding to class induction, same-gene relations, latent program attention and the bounded analytic residual;
- explicit equations for task-local class profiles and the full 28-dimensional relation vector;
- the architectural intuition behind each reduction and attention stage;
- connections to prototypical and matching networks, Relation Networks, Deep Sets, Set Transformer, attentive neural processes, Perceiver and Transformers;
- an explicit statement of inductive query scoring, gene-permutation invariance and approximate linear complexity in genes and support rows;
- clarification that class-summary routing and the neural correction are learned end to end only from synthetic query cross-entropy;
- citations for activation checkpointing, AdamW and cosine scheduling;
- a cited and renamed architecture-family summary with no use of the former working name.

## Simulator section

Citations were added, without changing the mathematical construction, for:

- heavy-tailed gene-abundance and count-simulator context;
- random gene programs and structured latent biological effects;
- within-label multimodality;
- gene-gene dependence and covariance structure;
- trajectory and sample/domain effects;
- Poisson/negative-binomial UMI observation models and empirical-Bayes count inference;
- online PFN task sampling;
- generator-adaptation-based filtering of trivial or shortcut-dominated tasks.

The frozen claim-bearing simulator scope remains unchanged. Ambient RNA, explicit dropout, panel masking and doublets are still described as broader platform capabilities that were not active in the frozen 100K path.

## Citation and naming checks

- The bibliography contains exactly 50 cited references.
- There are no unresolved citations.
- The former working name does not occur anywhere in the LaTeX source.
- The source compiles without LaTeX warnings, overfull boxes or undefined references.
- The final PDF contains 38 pages and was visually rendered for inspection.
