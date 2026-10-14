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
