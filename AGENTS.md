# CellPFN manuscript

- Target: Nature Biotechnology Article, in English.
- Active source: main.tex and sections/*.tex; references.bib is the active bibliography.
- Active scope: abstract, introduction, quantitative Results, extensive Methods, technical supplement and one editable architecture figure. Discussion, remaining figures and submission materials are deferred.
- Use baseline prior and cellular prior in manuscript prose; raw project version IDs belong only in provenance. Describe the final method and actual evaluated training recipe without a development-history narrative.
- Distinguish source-supported software capabilities from measured throughput, and current optional features from evaluated configurations.
- The simulator defines the PFN prior. Lead with competitive biological inference at limited training-task exposure, then transfer of the prior to pretrained tabular models.
- Preserve explicitly unresolved narrative claims in bold red, including in the abstract. Never invent completed experiments or numerical outcomes.
- Current refreshed paper export governs experimental facts. The seed and legacy texts supply historical motivation, not current numerical authority.
- Count simulator banks, scheduled episodes, loss-bearing episodes and additional adaptation tasks separately.
- Source materials outside this repository are read-only.
- Commit frequently with a single-line message. No co-author mentions or trailers. Use repository-local identity Philipp Flotho <PhilippFlotho@gmail.com>.
- Canonical PDF: output/cellpfn.pdf. Build in temporary storage; preserve historical inputs but remove intermediate manuscript PDFs. Do not introduce version/revision suffixes.
