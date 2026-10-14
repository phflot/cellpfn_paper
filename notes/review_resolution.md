# Resolution of Wave1 independent reviews

The three `review_*.md` files preserve findings on the first complete draft. They are historical review records, not a list of still-unfixed errors. The following changes resolve their actionable issues:

| Finding | Resolution |
|---|---|
| Same simulator confused with identical prior history | Results now gives320K v1 +64K v2.2-B CellPFN episodes and identifies v2.2-B throughout tabular cellular adaptation. Abstract says “the cellular prior”; introduction says tasks from the same simulator. |
| Transfer too late in the evidence sequence | Moved cross-architecture continued training directly after the main CellPFN comparison. Stable paragraph IDs are retained. |
| Generic efficiency claim and ambiguous exposure units | Title now says compact; abstract says reported task exposure; Results distinguishes384K scheduled episodes,12K reused banks and approximately35M TabICLv2 datasets. |
| Evaluation not independent of real-informed development | Explicit calibration/evaluation overlap, variant selection and one training seed; O01 marks the future frozen external evaluation. |
| Foundation-model pretraining exposure vague | Names likely exact PBMC-cell exposure and Geneformer cortex-source exposure without claiming label leakage or a causal explanation of performance. Classifier standardization difference is explicit. |
| Kumo exposure ledger stale | Added official approximate35M small and137M large table counts as external-only records; TabPFN3.5 remains unspecified. TabICLv2 source links updated to verifiedv2. |
| Attribution metric imprecise | Defines original predicted-minus-runner-up margin and relativeL2 error. Deletion comparison is pairwise margin reversal, not benchmark error rate. |
| Unsupported marker interpretation | Reports literal IL7R/NKG7 rankings without asserting biological marker specificity. |
| Provisional timing not visibly separated | O05 marks the full timing prose red; measured example and extrapolated exhaustive cost remain distinguished. |
| Disease application over-interpreted by heading | Heading now says neuropathology-associated expression; donor AUC interval labelled95%; future attribution “will test whether”. O02–O04 stay bold red. |
| Conventional comparator not quantified in main prose | Added all-gene low-rank LDA at matched ten/100-support budgets, including its strong100-support result; no nonexistent one-shot LDA result is inferred. |
| Missing open-claim register during early review | `open_claims.md` now defines all five IDs with evidence required for closure; local checker enforces exact source/register correspondence. |
| Simulator narrative could better recover the legacy reference-fit motivation | Introduction now describes generating diverse labelled problems beyond reproducing a reference, while acknowledging configurable predecessors. |
| Historical and repeated explanatory clutter | Removed the obsolete analytic-logit contrast and repeated rhetorical conclusions; renamed the ablation subsection to cover both prior and architecture changes. |

We retained the main comparator means and the explicit timing example because they make this initial figure-free draft reviewable. They can be compressed into legends in Wave3. Extensive verified citations remain in the introduction as requested; reserve references are separate from the printed citation list.

Final word counts and checks are in `output/review/`. These reviews verify the stated evidence boundaries; they do not replace an independent biological replication or peer review.

## Quantitative completion and author additions — 14 October 2026

This pass supersedes the initial five-claim and mostly qualitative Results state above. It retains the historical review record while adding the complete numerical evidence and the author's subgroup and attribution requests.

| Finding | Resolution |
|---|---|
| Wave 1 did not expose enough quantitative support for its argument | Main Results now quantify the benchmark, transfer, gene-count scaling, operator/prior/task-mixture ablations and simulator realism. Tables 1 and 2 plus S1–S9 make the selected claims and their adverse outcomes reviewable in the same PDF. |
| Export coverage was difficult to audit | All 288 files are semantically indexed with authority, schemas, units, status and manuscript disposition; original source files remain unchanged. |
| Gene-count and panel-specific comparisons were insufficiently visible | Table 1 gives PBMC/ZEBRA model comparisons; Table 2 gives the 2k-HVG, 8,192-HVG and all-gene ablation. Two main display items leave four slots for later figures. |
| Table ranking did not distinguish exposure flags | Flagged values are gray; overall-best and best unflagged values are bold, including ties at shown precision. Legends bound the exposure evidence rather than implying that unlabeled pretraining means target-label leakage. |
| Ordinary accuracy and balanced accuracy could be conflated | Generic-retention reporting names each metric separately; the main claim uses balanced accuracy. Replicate units and model seeds remain explicit. |
| Frozen operator intervals could be read as uniformly 95% | S4 preserves the exported interval coverage, including the approximately 80% PBMC frozen interval. The failed global verdict is explained in prose rather than repeated against individual positive rows. |
| Task-mixture predictive-loss costs were incompletely summarized | Main Results now report NLL worsening by 0.35–0.63 on three high-support panels and improvement by 0.05 on fine PBMC, alongside unequal cells processed per update. |
| PBMC difficulty was not represented | Results and S9 distinguish matched coarse/fine contexts and all eight harder tasks. The harder tasks are explicitly post hoc, with ten/ten/five support draws and no invented intervals or prespecified binary subgroup. |
| Sex scores lacked evaluation-unit boundaries | Original GSM-disjoint classification and later unit-level AUC tasks are separated. Later units include age-by-sex groups, so neither GSMs nor all later units are called independent donors. Study and gene-universe changes prevent attributing their difference solely to sex-linked genes. |
| Sex-associated gene names risked becoming unsupported attribution results | O06 records that sex-specific gene attribution is absent. XIST/Y-linked eligibility rules are not reported as recovered model explanations. |
| Cell-type explanations were underreported | S8 gives actual top-ranked genes and selected known-marker ranks with verified primary references, including nonhits and support sensitivity. Main prose makes selected marker matches rather than enrichment or causal claims. |
| One inference step could be mistaken for one forward pass | DS-LOO is described as one attribution sweep using head-gradient evaluations and depth/detection corrections; it avoids a full forward pass for each gene but is not literally one forward pass. |
| Numerical rounding could create inconsistent displayed ties | Tables use a consistent half-up formatter. Winner emphasis follows the displayed precision as requested by the author. |
| Old output names and pagination obscured the current artifact | The build leaves only `output/cellpfn.pdf` as the active manuscript, preserves historical inputs and cleans temporary build PDFs. The final table layout and pagination are visually reviewed. |

The expanded ledgers contain 159 R, 159 X and 13 T records; 327 local numerical checks and 1,268 table-value selections pass, and the original export reconciliation passes all 1,375 checks. Six open claims remain registered. These checks establish source consistency and arithmetic, not an independent experimental validation or submission approval.
