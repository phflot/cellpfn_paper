# Prototype bibliography notes for `hashprompt/refs.bib`

This note records bibliography entries that were added manually during the HashPrompt merge work and were **not** present in the union of:

- `cell_foundation/refs.bib`
- `pyScIntelligentDesign/refs.bib`
- `1Bcell/refs.bib`

The goal is provenance and later cleanup, not final BibTeX polish.

## Assistant-added entries beyond the original three source bibs

These six keys are present in `hashprompt/refs.bib` but were not present in the three original source bib files:

1. `singleR`
   - **Title:** Reference-based analysis of lung single-cell sequencing reveals a transitional profibrotic macrophage
   - **Authors:** Aran, Dvir; Looney, Agnieszka P.; Liu, Leqian; Wu, Esther; Fong, Valerie; Hsu, Austin; Chak, Suzanna; Naikawadi, Ram P.; Wolters, Paul J.; Abate, Adam R.; Butte, Atul J.; Bhattacharya, Mallar
   - **Year:** 2019
   - **Reason added:** clean reference-mapping baseline for the HashPrompt framing

2. `scmapcell`
   - **Title:** scmap: projection of single-cell RNA-seq data across data sets
   - **Authors:** Kiselev, Vladimir Yu; Yiu, Andrew; Hemberg, Martin
   - **Year:** 2018
   - **Reason added:** simple projection / reference-transfer baseline

3. `symphony`
   - **Title:** Efficient and precise single-cell reference atlas mapping with Symphony
   - **Authors:** Kang, Joyce B.; Nathan, Aparna; Weinand, Kathryn; Zhang, Fan; Millard, Nghia; Rumker, Laurie; Moody, D. Branch; Korsunsky, Ilya; Raychaudhuri, Soumya
   - **Year:** 2021
   - **Reason added:** important reference-mapping comparator distinct from plain kNN transfer

4. `saturn`
   - **Title:** Toward universal cell embeddings: integrating single-cell RNA-seq datasets across species with SATURN
   - **Authors:** Rosen, Yanay; Brbi{\'c}, Maria; Roohani, Yusuf; Swanson, Kyle; Li, Ziang; Leskovec, Jure
   - **Year:** 2024
   - **Reason added:** vocabulary-relaxed / cross-species comparison context

5. `uce`
   - **Title:** Universal Cell Embeddings: A Foundation Model for Cell Biology
   - **Authors:** Rosen, Yanay; Roohani, Yusuf; Agrawal, Ayush; Samotorcan, Leon; Consortium, Tabula Sapiens; Quake, Stephen R.; Leskovec, Jure
   - **Year:** 2023
   - **Reason added:** broader foundation-model / universal-embedding context

6. `transcriptformer`
   - **Title:** A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model
   - **Authors:** Pearce, James D; Simmonds, Sara E; Mahmoudabadi, Gita; Krishnan, Lakshmi; Palla, Giovanni; Istrate, Ana-Maria; Tarashansky, Alexander; Nelson, Benjamin; Valenzuela, Omar; Li, Donghui; Quake, Stephen R; Karaletsos, Theofanis
   - **Year:** 2025
   - **Reason added:** cross-species / vocabulary-relaxed context for positioning

## Notes

- These additions were made during the HashPrompt merge rounds to support the revised literature framing.
- `hashprompt/refs.bib` was later sanitized for LaTeX-friendlier punctuation while preserving the same citation keys.
- Future cleanup step: decide which of these entries should remain in the final paper, then re-check titles, author formatting, and venue metadata against authoritative BibTeX sources.
