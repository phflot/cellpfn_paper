# Decisions

## 2026-10-14 — authorized implementation

- Independent local Git repository at cellpfn_paper; author identity Philipp Flotho <PhilippFlotho@gmail.com>.
- Frequent single-line commits, no co-author mentions or trailers.
- NBT Article; approximately 550 introduction words and 1,850 Results words, reserving 600 for a later Discussion; abstract at most 150 words.
- The simulator defines the PFN prior. The main argument has two parts: compact CellPFN with limited task exposure, then continued training of existing tabular models under the cellular prior.
- Efficiency refers to training-task exposure, not an unmeasured FLOP or wall-clock advantage.
- Draft provisional Results and aspirational abstract claims in bold red with stable identifiers and explicit resolution requirements.
- Preserve the seed author list; repository commit identity does not set manuscript authorship.
- Preserve dataset views as reported. Do not splice processed-Zebra gene-scaling results into reconstructed-count comparisons.
- No new experiments, model retraining, Methods rewrite or figure production in Wave 1.

## 2026-10-14 — evidence review

- Use compact, rather than an unqualified efficient, in the working title. Report training-task exposure rather than measured compute advantage.
- Put prior transfer directly after the main CellPFN comparison, then transcriptome-scale behavior.
- State prior lineage: CellPFN320K v1 +64K v2.2-B episodes; tabular cellular adaptation uses v2.2-B throughout. The shared contribution is the simulator-defined prior family, not identical historical exposure.
- Disclose calibration/evaluation dataset overlap and likely foundation-model pretraining exposure to exact PBMC cells.
- Keep provisional timing prose visibly red as O05, while separating its measured and extrapolated values.

## Quantitative completion of Wave 1 — 14 October 2026

The author requested an exhaustive export index, quantitative Results and ablations, one at-a-glance Results table, and a supporting appendix in the same PDF. This supersedes the earlier decision to leave most ablations qualitative. Keep one canonical manuscript at output/cellpfn.pdf, remove intermediate manuscript PDFs, and use no version/revision suffixes. Historical source inputs remain provenance. Current export facts, including negative prespecified results and adverse outcomes, govern the revision. No new experiments, training or inferential tests are part of this work. Methods and figures remain later waves. These changes implement the approved plan; no new permission is required.

## Author additions and final table conventions — 14 October 2026

- Report PBMC and ZEBRA cell-type comparisons and the ablation with fewer/more genes. Use “2k HVGs” in the manuscript and tables.
- The model comparison is Table 1; the gene-count ablation is a separate Table 2, as explicitly requested. They occupy two main display slots and leave four for Wave 3 figures.
- Gray exposure-flagged values, retain bold for the overall best, and also bold the best unflagged value. Bold all ties at the displayed precision. Exposure flags must distinguish supported or possible unlabeled pretraining overlap from verified exact-cell identity or target-label leakage; the Geneformer/ZEBRA evidence is audited explicitly.
- Include matched coarse/fine PBMC results and the eight post hoc harder subtype tasks. Do not manufacture a prespecified easy/hard binary subgroup or intervals absent from the export.
- Include original and later ZEBRA sex results, keeping their GSM/sample-group units, input views and support budgets separate. Later units are not uniformly verified individual donors.
- Report actual top-ranked genes and selected known cell-type marker matches for PBMC and ZEBRA, with primary literature support. Marker matches do not by themselves establish enrichment, perturbation mechanisms or disease signatures.
- Use “one attribution sweep” for DS-LOO and state its head-gradient evaluations and corrections. Do not describe the exported implementation as literally one forward pass.
- Keep the missing sex-gene attribution visible as O06. XIST/Y-linked task-eligibility criteria do not supply recovered attribution genes.
- Preserve six unresolved scientific claims in red and defer Methods code auditing, Discussion and figure production to the agreed later waves.

## 14 October 2026 — Wave 2 completed

Implemented the approved extensive Methods, simulator software architecture and one editable overview figure. Three isolated Wave1 reviews were completed and frozen, then reconciled in `notes/reviews/wave1_synthesis.md`. Existing finer cortical results and comparative explanation evidence were added; task-mixture, HVG, comparator and exposure definitions were corrected. Two independent technical code checks resolved exact mathematical details in Methods. No new biological experiments, source-repository modifications or claimed simulator speed measurements were made. The current state, checks and remaining evidence gaps are in `notes/wave2_handoff.md`.
