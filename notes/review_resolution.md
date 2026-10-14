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
