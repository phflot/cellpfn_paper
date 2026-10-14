# Literature synthesis for the CellPFN argument

This targeted narrative review supports the Wave1 research-article argument. It is not a systematic review and makes no exhaustive-coverage claim. Three packages contain41 retained bibliographic records, with source-specific access, metadata, claim support and exclusion boundaries:

- [Cellular simulators and synthetic-to-real motivation](literature/simulation.md), with16 records and [query log](literature/simulation_search.json).
- [PFNs, tabular models and cellular foundation models](literature/pfn_and_cells.md), with17 records and [query log](literature/pfn_search.json).
- [Benchmark context, datasets and attribution](literature/context.md), with8 records and [query log](literature/context_search.json).

The active `references.bib` combines these records without inheriting the legacy bibliography wholesale. Published versions replace stale preprints where verified. In particular, scMultiSim is2025; scDesign3 uses its2024 issue year; UCE and TranscriptFormer have2026 published records; TabICLv2 is an ICML2026 paper. MapPFN/PerturbPFN retain their preprint/workshop status, and Kumo/TabPFN feature and exposure details use labelled official model documentation. The suspicious legacy `smith2024benchmark` entry was excluded, not silently repaired with guessed metadata.

## Evidence chain and novelty boundary

| Argument step | Literature support | What CellPFN must contribute empirically |
|---|---|---|
| More cells need not supply more varied learning problems | scTab's donor-versus-cell subsampling; measured saturation in DenAdel; bounded frozen-representation evaluations | Useful support-conditioned predictions across biological contexts, with the development boundary visible |
| A generator can define the prior for a learned inference rule | Original PFN theory; TabPFN and TabICL synthetic-task training | An effective cellular distribution, architecture and measured transfer; no claim to invent PFNs or synthetic tabular learning |
| Cellular simulation supplies explicit experimental variation and labels | Splatter, SymSim, scDesign2/3, splatPop, SERGIO, dyngen, scMultiSim; learned generators | A useful task prior rather than donor simulation itself, which is established prior art |
| Synthetic-to-real success depends on useful structure, not photorealism or one fidelity score alone | FlowNet and face-analysis precedents; Crowell and Duo simulator evaluation | Real-cell transfer and targeted controls. The simulator realism audit alone cannot establish inference value |
| Cellular PFNs already exist | MapPFN and PerturbPFN | Distinguish classification from perturbation prediction; demonstrate compact transcriptome-scale inference and adaptation of existing tabular learners |
| A prior can be useful across architectures | General PFN logic supplies motivation; no external paper establishes this project's result | The exported TabICLv2/Kumo continued-training gains, qualified by generic replay and imperfect controls |
| Gene-level attribution explains predictions | Deep Sets supplies aggregation context; Integrated Gradients supplies attribution context | DS-LOO approximation fidelity and deletion tests, without converting classifier interventions into biological causality |

The inherited story is strongest when its simulator argument is precise: repeated cells do not automatically produce varied donors or tasks; simulation permits known labels and controlled variation; the generator defines the prior under which an inference rule is learned. Existing simulators already have configurable and donor-aware components. The novelty claim belongs to demonstrated inference utility and cross-architecture reuse, not a categorical claim that earlier simulation could only copy a fixed reference.

## Verification and remaining limits

Primary records, metadata and claim anchors were checked through publisher/proceedings pages, PubMed, author preprints and official model cards. Available full text was inspected for technical claims such as TabICLv2's training schedule and cellular PFN mechanisms. Abstract-only support is explicitly identified, particularly for the subscription-restricted scaling article and some model/resource records. Scholarly MCP tools were unavailable and shell Crossref access failed DNS; no claim of successful Crossref API or exhaustive Scopus/Google Scholar retrieval is made.

`scripts/vendor/audit_bib.py` checks keys, fields and duplicates offline; its generic DOI warning cannot know about the separate source inspections recorded here. Records without a verified DOI retain their official proceedings or model-card URLs. The three uncited retained records (scLong, Squair’s biological-replication context, and Tobin domain randomization) provide novelty/reporting context for later Methods/Discussion and are not printed in the current bibliography. No reference is included merely to meet a numerical quota.

The result ledgers supply the paper's own numerical evidence. Literature references do not substitute for those data. Current model performance is descriptive development evidence; corrected disease labels, independent biological replication and final Methods provenance remain open under `notes/open_claims.md`.
