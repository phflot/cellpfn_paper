# Wave 2 Methods reference verification

Checked 14 October 2026. This is targeted primary-source verification of added methodological references, supplementing the broader Wave 1 literature review. It does not claim a new systematic literature search.

| Key | Verified primary source | Role and scope |
|---|---|---|
| paszke2019pytorch | https://proceedings.neurips.cc/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html | Authors, title, NeurIPS32 and2019 verified from proceedings. Supports attribution to the PyTorch framework; source code determines our CPU/device behavior. |
| harris2020numpy | https://arxiv.org/abs/2006.10256 and DOI10.1038/s41586-020-2649-2 publisher metadata | NumPy array programming. Nature585,357–362(2020); publisher direct page intermittently redirected to inaccessible authentication, primary author manuscript opened. |
| virshup2024anndata | https://joss.theoj.org/papers/10.21105/joss.04371 | All five authors, JOSS9(101),4371(2024) and DOI verified from publisher BibTeX. Annotated matrix storage; not a performance claim about our exporter. |
| vaswani2017attention | https://papers.nips.cc/paper/7181-attention-is-all-you-need | Eight authors, title and NeurIPS30(2017) verified from proceedings. Transformer attribution; exact CellPFN dimensions come from its implementation. |
| loshchilov2019adamw | https://arxiv.org/abs/1711.05101 and authors' https://github.com/loshchil/AdamW-and-SGDW | AdamW method, ICLR2019. OpenReview browser challenge prevented direct forum read; author manuscript and author code record supply primary provenance. |
| meyer2024stochasticaging | https://www.nature.com/articles/s43587-024-00619-x and https://pubmed.ncbi.nlm.nih.gov/38724736/ | Meyer and Schumacher, Nature Aging4,871–885(2024), DOI verified across publisher/PubMed. Stochastic aging-clock inspiration. Our clipped-coordinate adaptation and numerical settings are source-derived; no real aging mechanism is inferred. |
| mcevoy2022kidney | https://www.nature.com/articles/s41467-022-35297-z; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202109; PubMed36496458 | Primary healthy-kidney cohort and accession. The manuscript's 27,675-cell processed evaluation artifact differs from the original study's 27,677 high-quality cells; retain processed-panel provenance rather than changing it to match the publication. |
| nadeau2003inference | https://link.springer.com/article/10.1023/A:1024068626366 | Authors, title, Machine Learning52,239–281(2003), DOI and abstract verified. Full publisher text requires access. Exact correction used in the provisional ROSMAP analysis comes from exported protocol records, not a claim of a fresh implementation or independent replication of the statistical derivation. |

Existing references cover set-based models, PFNs, simulator precedents, benchmark datasets, released comparators and integrated gradients. New references acknowledge intellectual/software dependencies; they do not validate our experimental outcomes. All comparisons and checkpoint-specific claims remain bound to the export and source/configuration audit.

The simulator scalability protocol additionally uses the official scDesign3 documentation (https://songdongyuan1994.github.io/scDesign3/docs/index.html) for configurable cell counts and acceleration options. Neither that documentation nor the available local measurements establishes a universal inability to generate one million cells.
