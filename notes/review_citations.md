# Independent claim–citation review

Reviewed 14 October 2026: `sections/abstract.tex`, `sections/introduction.tex`, `sections/results.tex`, the three literature notes, and `evidence/task_exposure.csv`. Primary scope: PFN theory, model-family framing, external training exposure and foundation-model claims. Simulation, attribution and dataset statements were checked against their documented claim records rather than independently reopening every underlying paper. Project performance numbers are outside this citation review and remain subject to the numerical evidence audit.

## Findings requiring action

1. **Abstract: preserve the different units in the exposure comparison.** The rounded factor of 90 is arithmetically justified, but “90-fold fewer training episodes than reported for TabICLv2” relabels its reported datasets as episodes and hides CellPFN's reused banks. The Results explains this correctly. Prefer the abstract wording “after 384,000 scheduled episodes, compared with approximately 35 million training datasets reported for TabICLv2.” If retaining the factor, call it an approximately 90-fold difference in reported task exposure, without implying matched compute or independent synthetic realizations. No abstract citation is required under the selected journal format; the cited Results supplies the provenance.

2. **Results P-R15: the biological marker interpretation needs support or neutral wording.** The export proves the IL7R/NKG7 ranks, but “recovered recognizable cell-type markers” is an external biological interpretation. The current bibliography notes do not verify the corresponding marker passages. Either verify a primary PBMC marker source and cite it here, or change the opening to a literal result such as “The gene rankings highlighted IL7R in CD4 T cells and NKG7 in natural killer cells despite the absence of gene-name embeddings.” Avoid claiming marker specificity: both genes can characterize broader or overlapping lymphocyte states.

3. **Training-exposure notes are stale for Kumo.** T11 and `notes/result_summary.md` still describe all Kumo counts as unverified. The official card now supplies approximate counts (see below). Update the registry description/status rather than retain the contradictory blanket statement. Exact original training logs remain unavailable; the card does not supply exact counts.

## External claims that pass

| Draft anchor | Assessment |
|---|---|
| Introduction P-I01, donor versus cell diversity | Supported by scTab's Fig. 2 and Results donor/cell subsampling experiment. “Can contribute more” appropriately limits the claim; it does not assert that every atlas follows the same scaling relation. |
| P-I02, named empirical foundation models | Supported by the cited primary model papers. The wording allows both fine-tuning and frozen representation use, avoiding a false universal retraining requirement. Published 2026 UCE and TranscriptFormer records are used correctly. |
| P-I02, limitations and saturation | Supported by the Kedzierska paper and DenAdel abstract/figure captions. I independently reopened the DenAdel publisher page and confirmed the bounded plateau claim. The draft does not turn these evaluations into a universal anti-scaling theorem. |
| P-I02, normalization/linear alternatives | Matches the Souza preprint abstract and is explicitly labelled preprint evidence. It concerns evaluated representations, not a claim that cellular biology is linear. |
| P-I03, PFNs and synthetic tabular priors | Correct use of Müller, TabPFN and TabICL. The generative task prior and contextual prediction are established concepts; the draft attributes them appropriately. |
| P-I03, biological PFNs | MapPFN and PerturbPFN are real, directly relevant precedents. “Recent … work” accommodates their workshop/preprint status and avoids an unsupported claim that CellPFN is the first cellular PFN. |
| P-I04, simulator families and synthetic-to-real precedents | Consistent with the simulator review's source-specific records. The collective sentence describes complementary capabilities across the cited methods; it does not claim every simulator has every feature. |
| Results P-R02, set-based learning | Deep Sets is an appropriate precedent for permutation-invariant aggregation. The sentence attributes a principle, not validation of CellPFN's exact architecture. |
| P-R03, approximately 35 million TabICLv2 datasets | Directly supported by the latest arXiv v2, Section 4.1, and compatible with the published ICML 2026 record. The 90-times comparison is a reasonable rounding, accompanied by the necessary task/compute distinction. |
| P-R04, baseline identities | Geneformer/scGPT, TabICLv2, Kumo-Tabular and TabPFN-3.5 have appropriate model-specific citations. Logistic classifiers and actual input routes are project choices, not statements established by the original model papers. |
| P-R07–P-R08, transcriptome-scale inference | This is a bounded result on tested inputs and settings. No novelty claim requires scLong to be added here; cite it if later prose claims that full-transcriptome cell modelling was previously unavailable. |
| P-R08, TabPFN-3.5 guardrail and research use | Supported by the actual official model card, separately from the general TabPFN reference. The export—not the model card—establishes which local runs refused the inputs. The draft keeps that distinction. |
| P-R09–P-R10, continued training | Reported as a project experiment rather than the invention of fine-tuning. The same model references already introduced in P-R04 are sufficient; repetition is optional. |
| P-R13, Integrated Gradients | Correctly attributed as path-based gradient attribution, with finite deletion and biological intervention carefully distinguished. |
| P-R16, ROSMAP | Bennett supplies cohort context only. The paragraph is marked provisional and does not assert that Bennett is the source of the precise exported sequencing release or AUC. Release/accession mapping remains a Methods obligation. |

## Latest-source and registry update instructions

**TabICLv2 v2 verified directly.** The current source is [arXiv 2602.11139v2, Section 4.1](https://arxiv.org/html/2602.11139v2#S4.SS1), posted 16 September 2026. It repeats approximately 35 million datasets; the three stages are 500,000, 40,000 and 10,000 updates at batch size 64. [Appendix B.1](https://arxiv.org/html/2602.11139v2#A2.SS1) repeats the schedule. Its product is 35.2 million exposures; the manuscript's explicitly approximate 35 million is faithful to the reported rounded value. The published citation remains `qu2026tabiclv2`, ICML 2026/PMLR 306, 102477–102555. Update T06/T07 and note URLs from v1 to v2; there is no numerical revision. The ratio from the rounded numerator is 91.1458, supporting “about 90 times.”

**Kumo permits an update of T11, with approximation retained.** [NVIDIA's Kumo-Tabular 1.0 model card](https://build.nvidia.com/nvidia/kumo-tabular/modelcard), “Training, Testing, and Evaluation Datasets” → “Training Dataset”, inspected again on 14 October 2026, reports approximately 35 million synthetic tables for small and 137 million for large. The same page identifies version 1.0 and the September 2026 release. Record separate small/large values, unit `synthetic_training_tables`, source key `nvidia2026kumo`, and status meaning “official model-card approximation, source read 2026-10-14.” Do not label the values exact, or infer them from parameter count. If adding manuscript ratios, the same reused-bank, unequal-table-size and unmatched-compute qualifications apply. T12 for TabPFN-3.5 should remain unverified: TabPFNv2 exposure cannot substitute for it.

## Bibliographic and completeness conclusion

All PFN/foundation-model citation keys in the reviewed prose resolve to the verified staging records. No necessary PFN citation is missing, and no citation in this scope is being used to support CellPFN's own numerical results. The two older TabPFN and TabICL historical citations could be compressed if the reference budget later becomes tight; their presence is accurate, not an integrity defect. The current manuscript does not need to cite every retained reserve source. Final BibTeX merging, duplicate checks and compilation are handled by the lead agent.

This review did not independently validate biological marker specificity, every simulator full text, or new experimental outcomes. It supplies source-support judgments rather than claiming a complete external peer review.
