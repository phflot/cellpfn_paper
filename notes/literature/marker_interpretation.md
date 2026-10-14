# Marker interpretation and sex-task evidence

Checked 2026-10-14. This is a focused, claim-led audit of the genes actually present in the export, not a systematic review of cell-type or sex markers. Literature search scope was primary human single-cell studies, with no date restriction and preference for the existing atlas citation and Nature/Cell-family sources. Only public article identities and gene names were searched; no unpublished data were sent to external services.

## Experimental anchors and limits

`fig5__cases.csv` contains six cell-typing cases for each of two CellPFN states: coarse PBMC at ten supports (draws 0 and 1), coarse PBMC at 100 supports (draw 0), cortex development at ten supports (draw 0), and kidney core9 count/processed inputs at 100 supports (donor fold 0). There is **no Zebra-sex or zsex_xy attribution case**. `fig5__marker_ranks.csv`, `fig5__top_genes.csv` and `fig5__ko_pairs_by_class.csv` therefore support cell-type explanations, not sex-task gene rankings.

A coherent illustrative setting is `case_id == pbmc_l1_b100_s0`, `model_id == cellpfn_g1v2p`, `method_id == dsloo_corr_margin`. In the fixed predicted-versus-runner-up margin ranking:

| Broad class | Selected exported marker | Rank | Interpretation |
|---|---|---:|---|
| B | CD79A | 1 | B-lineage-associated gene |
| B | MS4A1 | 2 | B-cell-associated gene; not a universal B-lineage marker because plasma cells can lack it |
| CD4 T | IL7R | 2 | Consistent with CD4 T-cell-associated expression; not exclusive to all CD4 cells |
| CD8 T | CD8A | 2 | Consistent with CD8 T-cell-associated expression |
| DC | FCER1A | 1 | Consistent with conventional/myeloid dendritic-cell identity |
| DC | CLEC10A | 2 | Consistent with a conventional/myeloid dendritic-cell subtype; broad DC labels combine subtypes |
| Mono | CD14 | 3 | Consistent with a monocyte-associated marker |
| NK | GNLY | 2 | Consistent with cytotoxic/NK-cell-associated expression |
| NK | NKG7 | 7 | Consistent with cytotoxic/NK-cell-associated expression, not NK specificity |

The numerical ranks are the present study's results, not claims derived from an external paper. At the same setting CD3E ranks 131 for CD4 T, LILRA4 ranks 4,392 for broad DC, and LYZ ranks 33,354 for monocytes. Consequently, the supported claim is recovery of **selected established markers in a contrast-specific ranking**, not universal marker recovery or a marker-enrichment statistic. Positive attribution is support for the model's predicted-versus-runner-up margin; expression direction is separate and must not be inferred from attribution sign. Cells used for fidelity checks were correctly predicted and selected; the result is not evidence of causal biological perturbation responses.

Recommended compact narrative: “After restoring gene symbols to the anonymous input columns, the rankings highlighted established cell-type-associated genes, including CD79A and MS4A1 for B cells, IL7R for CD4 T cells, and GNLY and NKG7 for NK cells. In the coarse-PBMC example with 100 labelled cells per class, these ranked first, second, second, second and seventh, respectively. The agreement supports biological interpretability of these model-specific explanations; rankings remain dependent on the support context and comparison class.” Cite the marker-identity clause, not the new ranks.

## Primary literature verification

| Claim segment | Source and verified anchor | Support level and use |
|---|---|---|
| PBMC atlas and cell-state provenance | Hao et al., *Cell* 184, 3573–3587.e29 (2021), DOI [10.1016/j.cell.2021.04.048](https://pubmed.ncbi.nlm.nih.gov/34062119/), existing key `hao2021multimodal`. PubMed abstract and legends for Figures 3, 4 and S4 were opened. | Strong for atlas provenance and multimodal immune-state characterization. The accessible text did not explicitly list every selected marker, so it was not used as the sole verification of each gene identity. No duplicate citation added. |
| IL7R/CD4 T; GNLY/NKG7/NK; CD79A/B lineage; CD8A/B/CD8 T; FCER1A/CLEC10A/myeloid DC; CD14/monocytes | Schafflick et al., *Nature Communications* 11, 247 (2020), DOI [10.1038/s41467-019-14118-w](https://www.nature.com/articles/s41467-019-14118-w), PMID [31937773](https://pubmed.ncbi.nlm.nih.gov/31937773/), new key `schafflick2020leukocytes`. Publisher Results “Single-cell transcriptomics of cells in CSF and blood”, Figure 1c and its legend were opened. | Direct primary observational support for these lineage-associated markers. It also identifies plasmablasts lacking MS4A1/CD20, which limits blanket B-lineage specificity. Does not validate CellPFN, rank ordering or causal importance. |

The second study directly assigns human blood/CSF clusters using the indicated marker expression; the marker paragraph and its Figure 1 are the relevant source, rather than the paper's disease-specific conclusions. Its complete ordered 14-author list, title, year, volume, article number and DOI were cross-checked between the PubMed record and publisher page. The author name “Meyer zu Horste” follows the publication's spelling. This directly inspected PBMC study and the cortical study below supply two new bibliographic entries. No speculative sex-gene reference was added to disguise the absence of model-specific attribution results.

Search log: exact-title queries for Hao 2021 with IL7R/NKG7; primary-source queries for IL7R, NKG7, GNLY, CD79A and MS4A1 in PBMCs; PubMed title lookup and publisher full-text verification for Schafflick 2020. Zheng et al. 2017 and several newer computational/clinical papers appeared in discovery but were not added because one directly inspected primary study supplied the required marker support. The PMC copy of Hao returned a browser challenge and its Cell page could not be opened; this limitation is why gene-specific support was checked elsewhere. No claim relies on a secondary search result alone.

## Cortical marker examples and highest-ranked genes

At `zebra_dev_b10_s0`, `cellpfn_g1v2p`, `dsloo_corr_margin`, the export has 21,158 genes. Selected established-marker ranks are PLP1 8 for broad Glia, SYT1 7 for Neural, CLDN5 16 and FLT1 5 for Vascular cell. These are the study's attribution ranks; external literature supplies the biological interpretation, not the ranking. `marker_set_origin` explicitly says the report author chose the marker set; it was not supplied in the task. This is illustrative biological agreement, not a prespecified marker-recovery test.

Directly verified primary support for three examples is Gong et al., *Nature Communications* 16, 482 (2025), DOI [10.1038/s41467-024-54715-y](https://www.nature.com/articles/s41467-024-54715-y), PMID [39779708](https://pubmed.ncbi.nlm.nih.gov/39779708/), new key `gong2025stereoseq`. The Results paragraph immediately before Figure 5 and Figure 5B identify PLP1 in oligodendrocytes, SYT1 in excitatory neurons, and CLDN5 in endothelial cells. The full ordered 17-author list and bibliographic fields were checked against PubMed and the publisher. The publication year is **2025**, despite “024” in the DOI. This source supports cell-type-associated expression in adult human cortex; it does not make any CellPFN or developmental-benchmark claim.

Use “the oligodendrocyte-associated PLP1 within glia, neuronal SYT1, and endothelial CLDN5 within vascular cells” or similarly qualified language. Glia and vascular are broad labels; PLP1 does not mark every glial cell and CLDN5 does not mark every vascular subtype. The full marker table includes weaker examples, including GFAP rank 657 and AQP4 1,107 for Glia and PTPRC rank 20,710 for Immune cell. It therefore does not support universal or exhaustive marker recovery.

The top three positive genes by absolute rank are separately exported as NPAS3/PCDH9/PPP2R2B for Glia, FGF12/RGS7/RBFOX1 for Neural, and PTPRG/MALAT1/LAMA2 for Vascular cell. Describe these as the **highest-ranked genes for the model's margin**, not as a set of canonical markers. These lists must not be replaced with hand-selected marker examples under a “top three genes” label.

Cortical search/access log: searched original ZEBRA paper and selected gene symbols; queried the Grubman 2019 entorhinal atlas and marker names; opened the Grubman publisher preview, PubMed record, and authors' [atlas application](https://adsn.ddnetbio.com/). The application includes these genes, but its static text does not show gene-to-cell-type assignments; the publisher marker figure/full text and downloadable source table were not accessible through this browser. Consequently, Grubman was not added as if its gene-level claim had been directly inspected. A primary replication, [Li et al. 2023](https://doi.org/10.1002/alz.12979), explicitly reports FLT1/CLDN5 as endothelial markers and reproduces the other assignments; it is available as additional support if FLT1 biology is developed. The compact main-text examples can use the three genes directly verified in Gong without adding a further reference. Search discoveries alone were not treated as evidence. Original ZEBRA remains the dataset-provenance citation, rather than a substitute for gene-specific biological support.

## Zebra sex: what the export does and does not show

Two distinct tasks must remain separate:

- `zebra_sex` is a single frozen oligodendrocyte sex case from Sayed 2021: 100 support cells per class, 50 query cells, GSM-sample-disjoint support/query. GSM samples are not independent donors. Its performance is in the operator/task-mixture/prior-campaign tables, not the main four-panel cell-typing benchmark.
- `zebra_zsex_xy` / `zsex_xy` is a person-level positive control with ten splits, study-matched female/male pairs, and support-unit counts that expand to multiple support cells. Sayed units are age-by-sex groups of GSM samples; cross-study person overlap is unknown. It is not a set of independent test cohorts.

The `zebra_zsex_xy` glossary entry says eligible studies measured **XIST and at least four of RPS4Y1, DDX3Y, UTY, KDM5D and EIF1AY**. Those are **task-design eligibility genes**, not exported ranked attributions. They may be named when describing the positive-control design, explicitly in that role. No gene importance value, ordering, class-specific direction or sex-classification deletion effect can be assigned from this list. The donor-sex performance ledger is handled separately by the quantitative-evidence audit; no confidence interval across cells or model checkpoints is warranted by the one-case task.

To complete a sex-gene recovery claim, obtain the actual sex-classification attribution export: selected checkpoint/input route, positive class and margin target, query/support units, ranked gene scores, expression direction, and exact-deletion validation or a clear exploratory label. No new experiment or result is presumed here.

## “One inference step” wording

The source contract is `FIGURES.md`, fig5, “What is being compared”, mirrored in `sections/knockout.md`. CellPFN predicts without task-specific gradient updates. DS-LOO computes deletion effects for all query genes in **one sweep over gene contributions**, followed by a linearized-head backward pass and a second backward pass correcting read-depth/detected-gene coupling. Support data and the fitted covariance remain fixed; no model refit is required. These are distinct claims.

Supported wording: “CellPFN couples support-conditioned prediction with a single attribution sweep over all genes, without refitting the model or running a separate model forward pass for every gene.” Add the head-linearization and normalization-correction detail in Methods when that wave is written. “A single forward pass yields classification and all exact gene effects” is unsupported: effects are approximate and head/correction computations are additional. All-gene runtimes are still a separate provisional result.
