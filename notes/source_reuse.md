# Legacy motivation to retain for CellPFN

This index records reusable arguments, not current experimental evidence. Current experimental facts come from the refreshed paper export. All legacy paths below are relative to `../../CellPFN_model_methods_revision(2)/old_reference_texts/` from this file. Source files remain unchanged. The full source inventory and archival manifest are maintained separately.

## Priority passages and their intended use

| Argument | Exact legacy anchor | Use in the new manuscript | Boundary |
|---|---|---|---|
| Cell count does not substitute for donor diversity or trustworthy annotations | `pyScIntelligentDesign/scIntDesign.tex:143–145`; repeated in `hashprompt/hashprompt_v2.tex:70–72` | Motivate a controllable distribution of experimental settings, not simply more synthetic cells | The historical numerical claims about atlas sizes and donor counts require current references; synthetic donors are not additional measured biological individuals |
| Simulation provides labels and latent factors that are difficult to annotate in reality | `cell_foundation/cell_foundation.tex:171–173`; `hashprompt/hashprompt_v2.tex:63–65` | Brief synthetic-to-real precedent from face analysis and optical flow; explain the value of known task construction | Simulated truth is true within the chosen generator, not proof that the generator is biologically complete |
| Reference-fit generators reproduce what can be estimated from their reference | `pyScIntelligentDesign/scIntDesign.tex:145,819` | Motivate explicit randomization of effects, hierarchies and nuisance factors | Do not assert that existing simulators cannot vary fitted parameters or that the present prior recovers unknown real mechanisms |
| Simulator and inference model are coupled contributions | `hashprompt/hashprompt_v2.tex:97,122,237` | Introduce the simulator as the distribution defining the PFN prior; current export Figure 3 adds evidence of utility across model backbones | Avoid a separate simulator-benchmark or GigaCell-release narrative |
| Train on new experimental prediction problems, not one static synthetic atlas | `hashprompt/hashprompt_v2.tex:132–134`; `hashprompt/hashprompt_v3.tex:188–192`; `hashprompt/hashprompt_v4.tex:149` | Explain episode-based PFN learning and why study/donor/task variation matters | Use the current simulator-bank and scheduled-episode counts, not old online-stream claims |
| Useful randomization must match the deployment problem | `hashprompt/hashprompt_v4.tex:61`; `hashprompt/hashprompt_v2.tex:132–151` | Connect hierarchical biological variation and observation noise to the inference problems sampled during training | Do not claim that all prior ingredients improve transfer or that stronger perturbations are always better |
| Gene anonymity isolates inference from persistent marker-name memorization | `hashprompt/hashprompt_v4.tex:63,94–98` | State what the model learns from support labels and task-local gene correspondence | Support and query still need matching gene coordinates; no general orthology, missing-panel or cross-species claim follows |
| Transfer tests the usefulness of the training prior; marginal realism alone is insufficient | `hashprompt/hashprompt_v3.tex:81`; `hashprompt/hashprompt_v4.tex:85–90`; `hashprompt/pyScIntelligentDesign_publication_strategy_2026-03-19.md:209–237` | Lead with biological prediction and transfer of the prior; use realism checks as bounded supporting evidence | Do not claim universal simulator fidelity, universal runtime superiority or mechanistic completeness |

## Provenance of the motivation

The source contains `\phflo{...}` wrappers at `cell_foundation.tex:171–185` and `scIntDesign.tex:143–147,208–209,229,813`, with corresponding passages repeated or revised in HashPrompt versions. Other text has `\gpt{...}` wrappers. These are file-level provenance cues, not proof of handwritten authorship. Preserve their location and discuss them as passages *marked* `\phflo`; do not assign personal authorship to unmarked or later-rewritten text by inference.

The most valuable marked passage is the linked argument at `scIntDesign.tex:143–145`: acquisition and donor-diversity constraints motivate simulation, while dependence on a measured reference constrains the effects a fitted generator can estimate. Its new role is to motivate a configurable PFN prior. The manuscript should then test that prior by downstream performance rather than asserting that simulated experiments replace empirical biology.

## Legacy content excluded from active factual claims

- Hash tokenization, hashed class prompts, the 300K-parameter model, RoleSlotsV2, old curricula and old checkpoint scores are historical implementations.
- Do not call labelled-support inference “zero-shot annotation.”
- Gene anonymity does not imply arbitrary feature alignment, demonstrated cross-species transfer, universal cell-type knowledge or immunity to missing assay panels.
- The billion-cell GigaCell release, leaderboard, GRN/causal simulation, denoising outcomes, exact throughput and fidelity values in `scIntDesign.tex:136,211–221,726–823` are not current CellPFN evidence.
- The source argument that attention pooling is “never worse” than averaging (`cell_foundation.tex:261–277`) is not established by its displayed derivation.
- The old claim that real cells enter only at evaluation is too broad: the current export records calibration of simulator ranges and development choices using real datasets. Distinguish synthetic-only weight training from real-data-informed development.
- The March simulator publication strategy is historical advice, not a requirement to add a separate simulator benchmark or to change the authorized NBT target.
- `prototype_bib.md` explicitly records assistant-added bibliography entries; `reference_candidates_2026-03-19.md` is a staging list. Neither substitutes for primary-source verification.

## Wave 1 narrative consequence

Connect the inherited motivation to the current evidence: controlled experimental variation defines a PFN prior; limited synthetic task exposure yields competitive biological inference; the same prior improves pretrained tabular models; CellPFN handles transcriptome-scale input and permits efficient gene-level prediction explanations. Keep model-explanation knockouts distinct from experimentally validated genetic perturbations.
