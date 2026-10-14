# Independent cross-review of quantitative figures

Reviewed Figure 2 and Supplementary Figures S1--S6 and S9, including the S1
synthetic illustration. This reviewer did not author these figures. Review used
the rendered PNGs, legends, panel manifests and selected plotted source data,
with the integrated captions checked on canonical-PDF pages 11, 62--68 and 72.

## Findings

No blocking scientific or presentation issue was identified in the inspected
material. The key negative results remain visible: fine-PBMC adaptation harm,
generic-task retention loss, excessive synthetic separability, the failed
prespecified operator criterion, unequal task-mixture exposure, worse NLL under
some restricted-mixture conditions, and near-chance performance on the broader
sex task.

One minor terminology improvement is available: Supplementary Figure S4 labels
its contrasts as “accuracy,” although its manifest and source rows specify
**balanced accuracy**. Adding “balanced” to the S4 caption's first metric
definition would remove this ambiguity without lengthening every axis label.
The same clarification could be made for the S5 restricted-minus-standard
accuracy panel. This is a naming issue, not a numerical discrepancy.

## Specific checks and resolved visual concerns

- Figure 2 raw support draws and means are distinguished from training-seed
  uncertainty. Adaptation changes use paired, rescored released baselines; the
  caption correctly warns against subtracting the separately stored benchmark
  means. The replay and generic-control exposure qualifications are explicit.
- S1 uses synthetic IQR/5--95% intervals versus public median/range summaries,
  rather than implying matching confidence intervals. Its below-zero baseline
  LDA-gain tail in panel l is visible: source q05 is -0.00396875 in fractional
  accuracy (approximately -0.397 percentage points). The panel preserves that
  negative tail; the chosen quantiles do not claim to show the full raw range.
- S2's dense matrix was checked against extracted PDF text and source data after
  a scaled PNG made one adjacent value hard to distinguish. Kumo-large-plus-prior
  fine-PBMC 100-support accuracy is correctly **89.2**, followed by **42.8** for
  development-cortex one-shot accuracy; no value is missing or shifted. The
  94.7 CellPFN/LDA tie is retained. Exposure marking distinguishes source overlap
  from proven target-label exposure, and absent evaluations remain dashes.
- S3 makes the realized HVG width and the conditioning of paired 95% intervals
  explicit. Its random-gene dots are condition means, not biological replicates.
  The reconstruction comparison discloses simultaneous gene/support changes.
- S4 retains the original -1.5625-point harm finding against the -1.50 threshold
  and the unequal donor-interval coverage. Later twenty-draw estimates are not
  substituted for the prespecified decision. Inference interventions remain
  separate from independently trained configurations.
- S5 task shares agree with recorded counts after displayed rounding: standard
  binary/categorical metadata counts are 9,651/3,165, cell type 2,398 and donor
  identity 786; restricted counts are 12,001/3,999. Exposures remain 6,386,352 and
  10,671,056. Distinct AUC/NLL/accuracy endpoints are not merged onto one scale.
- S6 preserves all repeated-split points, observed ranges, the GSM/person caveat,
  distinct sex-task populations and the four-class versus binary-age distinction.
  The successful frozen sex example is not presented as population replication.
- S9 separates measured adaptation/attribution times from extrapolated exact
  deletion and estimated Kumo deletion. Different precision, scope and GPU-load
  conditions prevent controlled speedup claims, as stated in the caption.

The integrated captions are complete on their corresponding pages. Native
renderings are readable; this inspection found no unexplained clipped estimate,
hidden adverse finding or inferred uncertainty interval. Automated font-size and
collision checks are owned by the root audit and are not independently certified
by this review. This review samples source reconciliation; it does not replace
the complete numerical provenance checks or validate the underlying experiments.
