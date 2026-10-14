# Geneformer pretraining exposure audit

Audited 14 October 2026 after the author asked whether there is evidence that Geneformer has seen ZEBRA. This note separates independently checked model provenance from the study matches recorded by the supplied export.

## Conclusion and manuscript wording

There is evidence for **overlap between Geneformer-V2's pretraining sources and the studies contributing ZEBRA query cells**. The evidence does not establish that every query cell was in the trained checkpoint, and it does not establish exposure to the target cell-type labels. ZEBRA is an integrated atlas: overlap can arise through its original constituent studies even if the assembled ZEBRA release was never used in pretraining.

Use `*` and gray text for reported likely query-cell exposure based on source-study matches; retain `(*)` and gray text for the weaker, inferred partial overlap in the development panel. Define this as an exposure flag, not a finding of supervised label leakage. The best non-gray result is the best result **without a flagged query-source overlap**. It is not a guarantee that every unflagged model has been exhaustively audited or that it has never seen any support cell.

Suggested caption wording: “Gray values carry reported or inferred query-source overlap with pretraining data; this does not establish exposure to the target labels. Bold marks the best displayed result overall and the best unflagged result. Geneformer-V2 overlaps studies contributing 92.6% of held-out-study query cells; potential development-panel overlap is limited to at most 22.3%, with library identity unresolved.”

## Checkpoint and primary publication

The export identifies the evaluated baseline as **Geneformer-V2-316M with frozen embeddings and a logistic-regression head**, not the original 2023 Geneformer model: `../paper_export_20261011/build/benchmark/build_fig4.py:785` and `build/benchmark/build_supp_exposure.py:25`.

The [official model card](https://huggingface.co/ctheodoris/Geneformer) identifies V2-316M as a December 2024 model pretrained on approximately 104 million transcriptomes. The [published V2 paper](https://www.nature.com/articles/s43588-026-00972-4) describes masked-gene pretraining, the Genecorpus-104M corpus and its dataset composition in Supplementary Table 1. Its identity and metadata were checked against [PubMed PMID 41896605](https://pubmed.ncbi.nlm.nih.gov/41896605/). The [official corpus card](https://huggingface.co/datasets/theodoris-lab/Genecorpus-104M) links the same corpus and publication.

Added bibliography key `chen2026geneformer`: Chen, H. et al. *Nature Computational Science* **6**, 450–463 (2026), DOI `10.1038/s43588-026-00972-4`. This is the appropriate source for the evaluated model generation and its pretraining corpus; `theodoris2023geneformer` remains appropriate for the original method. All eight authors, issue 5, pages and DOI are source verified. Machine-readable extraction record: `notes/literature/geneformer_v2_metadata.json`.

## Query-study evidence in the export

Source: `../paper_export_20261011/data/supp_exposure__study_exposure.csv`. The “verified” and “inferred” categories below are the **original audit's** labels; this revision did not independently re-match cell barcodes.

| ZEBRA panel | Study | Query cells in the exported case pool | Evidence recorded by the original audit | Source line |
|---|---|---:|---|---:|
| Held-out study | Herring 2022 | 4,388 | 32 corpus rows totaling 211,458 cells match the 32 GEO snRNA samples by cell count; study/sample match labelled verified | 25 |
| Held-out study | Yang 2022 vascular | 1,642 | 18 corpus rows match 18 GEO sample matrices, including all 8 cortex samples; study/sample match labelled verified | 28 |
| Held-out study | Jaekel 2019 | 602 | Study listed as a 208,629-cell corpus row; study match labelled verified, identity of the query nuclei inferred | 31 |
| Held-out study | Hardwick 2022 | 531 | No matching study DOI reported | 34 |
| Development | Velmeshev 2019 controls | 1,735 | Possible reuse through a 700,391-cell Velmeshev 2023 corpus row; inferred, with library identity unresolved | 10 |
| Development | Velmeshev 2019 ASD | 1,779 | No evidence reported; own DOI absent | 13 |
| Development | Absinta 2021; Kihara 2022; Lim 2022 | 2,324; 1,045; 886 | No matching study DOI reported | 16, 19, 22 |

The held-out-study fraction is `(4388 + 1642 + 602) / (4388 + 1642 + 602 + 531) = 6632 / 7163 = 92.587%`, rounded to **92.6%**. This is the fraction of query cells originating in matched source studies, not a measured rate of identical cell inclusion in the trained checkpoint. The development-panel upper bound is `1735 / (1735 + 1779 + 2324 + 1045 + 886) = 1735 / 7769 = 22.332%`, rounded to **22.3%**. Neither fraction is a probability of overlap or an uncertainty interval. Panel denominators and interpretation are also in `supp_exposure__panel_chances.csv:7` and `:9`.

PBMC exposure is likewise an inference from a very close source match: the Geneformer corpus study row has the same 161,764 cells as Hao 2021 GEO GSM5008737, while the benchmark uses an 8,516-cell subset (`supp_exposure__study_exposure.csv:4`). It should not be presented as direct proof that the trained checkpoint consumed every one of those cells or labels.

## What remains unverified

The export preserves structured findings and a SHA-256 provenance record for `pretraining_exposure_20261008/EXPOSURE_REPORT.md` (`build/benchmark/sources_supp_exposure.csv:4`), but the original `/share/runs/.../EXPOSURE_REPORT.md` path is unavailable in this workspace. The V2 paper's [Supplementary Table 1 XLSX](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs43588-026-00972-4/MediaObjects/43588_2026_972_MOESM3_ESM.xlsx) was located, but the web reader cannot parse its binary format and shell downloads fail because networking is unavailable. Therefore the study rows are currently **supported by the supplied export, not freshly independently re-extracted from the XLSX**. This limitation must remain explicit in any audit description.

Before a definitive exact-cell claim, retrieve the original report and corpus table, preserve the matching study/accession rows, compare library and cell identifiers, and account for training/validation exclusion and preprocessing filters. No evidence here supports wording that Geneformer was trained on the benchmark's target labels.

Support-cell overlap is a separate issue: the export reports possible ZEBRA support overlap for both Geneformer and scGPT (`supp_exposure__panel_chances.csv:10–11`). The table's symbols follow the query exposure convention and should not be interpreted as a complete support/query contamination classification.

## Verification performed in this revision

- Recomputed both query-source fractions from the exported study rows and checked their denominators against the panel summary.
- Confirmed the checkpoint generation from local builder records and the official model card.
- Read the primary V2 paper's corpus and pretraining description and verified bibliographic metadata against PubMed.
- Attempted the citation-management DOI extraction script; recorded shell-network failure, then rendered the independently checked metadata with the skill's BibTeX renderer.
- Left original export files unchanged.
