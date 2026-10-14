# CellPFN manuscript

- Target: Nature Biotechnology Article, in English.
- Active source: main.tex and sections/*.tex; references.bib is the active bibliography.
- Active scope: abstract, introduction, quantitative Results, extensive Methods, current Figures1–3, both main tables, technical supplement and Supplementary FiguresS1–S9. Figure4 is reserved for external validation; Discussion and submission materials remain deferred.
- Plot quantitative figures in Python. Keep raw local/remote artifacts read-only; join cell/gene identities before biological overlays. Do not confuse display embeddings with classifier inputs.
- Use baseline prior and cellular prior in manuscript prose; raw project version IDs belong only in provenance. Describe the final method and actual evaluated training recipe without a development-history narrative.
- Distinguish source-supported software capabilities from measured throughput, and current optional features from evaluated configurations.
- The simulator defines the PFN prior. Lead with competitive biological inference at limited training-task exposure, then transfer of the prior to pretrained tabular models.
- Preserve explicitly unresolved narrative claims in bold red, including in the abstract. Never invent completed experiments or numerical outcomes.
- Current refreshed paper export governs experimental facts. The seed and legacy texts supply historical motivation, not current numerical authority.
- Count simulator banks, scheduled episodes, loss-bearing episodes and additional adaptation tasks separately.
- Source materials outside this repository are read-only.
- Commit frequently with a single-line message. No co-author mentions or trailers. Use repository-local identity Philipp Flotho <PhilippFlotho@gmail.com>.
- Canonical PDF: output/cellpfn.pdf. Build in temporary storage; preserve historical inputs but remove intermediate manuscript PDFs. Do not introduce version/revision suffixes.
