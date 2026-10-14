# Simulator-prior literature for CellPFN

Search date: 2026-10-14. Scope: 16 verified original sources for the integrated CellPFN story, including reserves. This was a targeted search, not a systematic review. Exact queries, extracted bibliographic metadata, inclusion decisions and access limitations are in [simulation_search.json](simulation_search.json); the companion BibTeX file is [simulation_references.bib](simulation_references.bib).

“Verified” means bibliographic identity and the specific claim below were checked against an original article, publisher record or official proceedings record. It does not imply every full paper or supplement was read. Source access is stated separately. Local Crossref API access failed at DNS resolution; verification used publisher records, PubMed/PMC, official CVF proceedings and author arXiv records through the web tool.

## How the literature should support Wave 1

Use a compact progression: simulations provide controlled tasks and known latent variables; existing tools span statistical, process-based and learned generators; simulation fidelity is multidimensional and its usefulness must be tested for the intended task. CellPFN uses a procedural generator to define the PFN training prior, so the decisive empirical question is whether that prior teaches useful inference and transfers across backbones. That last connection is the manuscript's argument and must be supported by the current paper export, not attributed to the simulator literature.

Lead with competitive biological inference at limited task exposure. Avoid recasting the project as a universal-fidelity competition or a separate simulator benchmark. Distinguish measured donors from generated donors and task diversity from total cell count. SymSim, splatPop and scMultiSim prevent broad novelty claims about controlled biological, donor or technical variation. Splatter and scDesign2 also allow user control; the contrast is the training objective and task distribution, not an absolute inability of existing tools to change a reference dataset.

Possible compact citation groups: (i) Splatter, SymSim and scDesign2/3 for simulation foundations; (ii) SERGIO, dyngen and scMultiSim for mechanistic/modal scope if needed; (iii) cscGAN and scDiffusion for data-driven augmentation/generation; (iv) Crowell and Duo for fidelity/utility boundaries; (v) Wood and Tobin for a short sim-to-real precedent. FlowNet, Squair and splatPop can remain reserve citations unless their specific argument enters the prose. Thorough research does not require citing every retained source in one introduction.

## Verified source-to-claim records

### 1. `zappia2017splatter` (2017)

- **Source:** [Original record](https://link.springer.com/article/10.1186/s13059-017-1305-0); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/28899397/).
- **Use:** Core: statistical simulation precedent.
- **Access:** Full publisher HTML opened; Abstract, Background and Splatter framework inspected.
- **Support anchor:** Abstract; Background; Results: The Splatter framework; Results: Splat.
- **Supported claim:** Splatter provides reproducible count simulation, including gamma–Poisson Splat, controlled populations and trajectories. Parameters may be estimated from data or supplied by the user.
- **Boundary:** Do not describe all existing simulators as necessarily reference-dependent: Splatter explicitly permits default or user-supplied parameters. Its presence does not establish any CellPFN speed advantage.

### 2. `zhang2019symsim` (2019)

- **Source:** [Original record](https://www.nature.com/articles/s41467-019-10500-w); [cross-check or access route](https://pmc.ncbi.nlm.nih.gov/articles/PMC6565723/).
- **Use:** Core: biological/observation factors.
- **Access:** Full publisher HTML opened; Abstract, Introduction and variability sections inspected.
- **Support anchor:** Abstract; Introduction; Results: Allele intrinsic variation / Extrinsic variation / Technical variation.
- **Supported claim:** SymSim separates transcriptional stochasticity, cell-state variation and assay effects, with controls for discrete/continuous states and experimental steps.
- **Boundary:** Explicit biological and technical randomization predates CellPFN. Cite as a foundation for controllable simulation, not as an inferior method without direct comparison.

### 3. `sun2021scdesign2` (2021)

- **Source:** [Original record](https://link.springer.com/article/10.1186/s13059-021-02367-2); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/34034771/).
- **Use:** Core: reference-fit statistical simulation.
- **Access:** Full updated publisher HTML opened; Abstract and model overview inspected.
- **Support anchor:** Introduction: properties 4–6; Results: An overview of scDesign2.
- **Supported claim:** scDesign2 fits cell-type-specific count marginals and a Gaussian copula to real data, preserves gene correlations and permits different cell counts and sequencing depths.
- **Boundary:** It also permits parameter adjustment; do not claim fitted models merely duplicate a fixed atlas. Publisher lists 2021 and 2023 corrections; use the updated article.

### 4. `song2024scdesign3` (2024)

- **Source:** [Original record](https://www.nature.com/articles/s41587-023-01772-1); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/37169966/).
- **Use:** Core: modern flexible statistical simulator and NBT precedent.
- **Access:** Publisher metadata and PubMed abstract verified; indexed PMC author-manuscript body/Fig. 1–2 extracts read. Direct PMC open encountered CAPTCHA.
- **Support anchor:** Abstract; Fig. 1 overview; Fig. 2 experimental-design examples.
- **Supported claim:** scDesign3 learns interpretable parameters from real data to simulate varied cell states, feature modalities and experimental designs, including spatial and multimodal settings.
- **Boundary:** Do not claim that reference-fit methods lack adjustable batch effects or customized controls. Bibliographic year is the 2024 issue year; online publication was 11 May 2023.

### 5. `dibaeinia2020sergio` (2020)

- **Source:** [Original record](https://doi.org/10.1016/j.cels.2020.08.003); [cross-check or access route](https://pmc.ncbi.nlm.nih.gov/articles/PMC7530147/).
- **Use:** Core or grouped citation: mechanistic simulation.
- **Access:** Indexed publisher and PMC full-text extracts read; direct publisher open failed and PMC open encountered CAPTCHA.
- **Support anchor:** Summary; Introduction; model description of stochastic transcription and user-specified GRNs.
- **Supported claim:** SERGIO uses specified regulatory networks and stochastic transcription to generate steady-state or differentiating single-cell expression with controlled noise.
- **Boundary:** This is a mechanistic simulation precedent. CellPFN’s current prior must not be represented as a validated GRN-dynamics model merely because it includes correlated programs.

### 6. `cannoodt2021dyngen` (2021)

- **Source:** [Original record](https://www.nature.com/articles/s41467-021-24152-2).
- **Use:** Core or grouped citation: dynamics and mechanistic ground truth.
- **Access:** Full publisher HTML opened; Abstract and Introduction inspected.
- **Support anchor:** Abstract; Introduction: three simulation stages; Fig. 1.
- **Supported claim:** dyngen translates regulatory networks into reactions, simulates cellular dynamics and emulates measurement protocols to benchmark trajectory, regulatory-network and RNA-velocity methods.
- **Boundary:** Known latent truth and controllable simulation are established capabilities; the CellPFN distinction is the use of a prior for learning inference across tasks.

### 7. `li2025scmultisim` (2025)

- **Source:** [Original record](https://www.nature.com/articles/s41592-025-02651-0); [cross-check or access route](https://pmc.ncbi.nlm.nih.gov/articles/PMC10543280/).
- **Use:** Core or grouped citation: current broad simulator capabilities.
- **Access:** Final publisher metadata, Abstract and extended-data captions opened; main final article subscription-only. Earlier PMC preprint indexed, not substituted for final-version claims.
- **Support anchor:** Final Abstract; Extended Data Figs. 1–3.
- **Supported claim:** scMultiSim combines cell identity, regulatory networks, cell–cell interactions, chromatin accessibility and technical noise while generating linked modalities.
- **Boundary:** Use final 2025 Nature Methods record, not the historical 2023 preprint. Multimodal or spatial capabilities are context, not demonstrated CellPFN capabilities.

### 8. `crowell2023shaky` (2023)

- **Source:** [Original record](https://link.springer.com/article/10.1186/s13059-023-02904-1); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/36991470/).
- **Use:** Core: reason to test transfer rather than infer usefulness from fidelity.
- **Access:** Full updated publisher HTML opened; Abstract, Background and benchmark design inspected.
- **Support anchor:** Abstract Conclusions; Background paragraphs on de novo/reference-based trade-offs; Benchmark design.
- **Supported claim:** The evaluation of 16 simulators found artifacts in complex designs, optimistic integration performance and potentially unreliable clustering rankings; summary similarity alone was not an established guarantee of valid comparisons.
- **Boundary:** Supports caution and downstream validation, not a claim that no simulator can be useful. Distinguish their benchmarking question from training a PFN prior. Publisher lists a July 2024 correction.

### 9. `duo2024systematic` (2024)

- **Source:** [Original record](https://link.springer.com/article/10.1186/s13059-024-03290-y); [cross-check or access route](https://pmc.ncbi.nlm.nih.gov/articles/PMC11149245/).
- **Use:** Core: multidimensional simulation evaluation.
- **Access:** Full PMC article opened; authors, Abstract, Background and Results framework inspected.
- **Support anchor:** Abstract Results/Conclusions; Results: overall benchmark framework; Fig. 1.
- **Supported claim:** A benchmark of 49 methods across 152 reference datasets assessed accuracy, functionality, scalability and usability, finding trade-offs and no best method on every criterion.
- **Boundary:** Its method accuracy measures resemblance under the evaluated scenarios; these do not directly measure PFN training utility. Cite Duo, not the incorrect Liu-led attribution in the old strategy note.

### 10. `wood2021fake` (2021)

- **Source:** [Original record](https://openaccess.thecvf.com/content/ICCV2021/html/Wood_Fake_It_Till_You_Make_It_Face_Analysis_in_the_ICCV_2021_paper.html); [cross-check or access route](https://openaccess.thecvf.com/content/ICCV2021/papers/Wood_Fake_It_Till_You_Make_It_Face_Analysis_in_the_ICCV_2021_paper.pdf).
- **Use:** Core short precedent for ground truth and synthetic-only learning.
- **Access:** Indexed official CVF article/BibTeX and accepted-paper PDF page-one extracts read; direct HTML open failed.
- **Support anchor:** Abstract; Introduction; official CVF BibTeX.
- **Supported claim:** Procedurally rendered faces train landmark and parsing models that transfer to real images, with label types that would be difficult or impossible to annotate manually.
- **Boundary:** A precedent, not proof of CellPFN transfer. Use the six authors in the final CVF proceedings; the later arXiv record has a different author list. DOI not verified and omitted.

### 11. `tobin2017domain` (2017)

- **Source:** [Original record](https://doi.org/10.1109/IROS.2017.8202133); [cross-check or access route](https://arxiv.org/abs/1703.06907).
- **Use:** Core short precedent for task-relevant domain randomization.
- **Access:** IEEE indexed Abstract/DOI verified; arXiv author Abstract page opened. Main paper not fully inspected.
- **Support anchor:** Abstract.
- **Supported claim:** Randomizing simulated visual properties enabled an object-localization model to transfer to real robotic settings despite non-photorealistic textures.
- **Boundary:** Motivates domain randomization; does not guarantee that arbitrary or larger biological randomization improves transfer. Proceedings pages not independently verified and omitted.

### 12. `dosovitskiy2015flownet` (2015)

- **Source:** [Original record](https://openaccess.thecvf.com/content_iccv_2015/html/Dosovitskiy_FlowNet_Learning_Optical_ICCV_2015_paper.html); [cross-check or access route](https://openaccess.thecvf.com/content_iccv_2015/papers/Dosovitskiy_FlowNet_Learning_Optical_ICCV_2015_paper.pdf).
- **Use:** Reserve: one additional example if the simulator motivation needs it.
- **Access:** Indexed official CVF article/BibTeX and accepted-paper PDF page-one extracts read; direct HTML open failed.
- **Support anchor:** Abstract; official CVF publication metadata.
- **Supported claim:** Flying Chairs supplied supervised optical-flow examples when available ground-truth data were insufficient; the trained networks generalized to other optical-flow datasets.
- **Boundary:** Do not describe all evaluated datasets as real imagery: Sintel is synthetic, whereas KITTI supplies a real-world evaluation. DOI not verified and omitted.

### 13. `marouf2020cscgan` (2020)

- **Source:** [Original record](https://www.nature.com/articles/s41467-019-14018-z).
- **Use:** Core: distinguish augmentation from the PFN-prior route.
- **Access:** Full publisher HTML opened; Abstract, Introduction, conditional generation and Discussion inspected.
- **Support anchor:** Abstract; Results: Conditional generation of specific cell types; Discussion.
- **Supported claim:** cscGAN learns from measured multi-cell-type data to generate specified populations; augmentation improves analyses of sparse cell populations and classifier robustness.
- **Boundary:** This is learned generation and augmentation from real observations, distinct from procedural-only parameter training. Do not imply prior single-cell simulation lacked downstream classification utility.

### 14. `luo2024scdiffusion` (2024)

- **Source:** [Original record](https://academic.oup.com/bioinformatics/article/40/9/btae518/7738782); [cross-check or access route](https://academic.oup.com/bioinformatics/advance-article-pdf/doi/10.1093/bioinformatics/btae518/58889831/btae518.pdf).
- **Use:** Core or grouped citation: current learned synthetic generation.
- **Access:** Indexed publisher full-text Methods extracts and PDF front matter read; direct HTML open failed.
- **Support anchor:** Abstract; Introduction final paragraphs; Section 2 Materials and methods / Fig. 1.
- **Supported claim:** scDiffusion uses a pretrained SCimilarity autoencoder, diffusion denoising and conditional guidance to generate expression under specified or combined conditions.
- **Boundary:** Generation learns from real cell data and a pretrained foundation model. Cite for controlled neural generation, not synthetic-only pretraining without real-data-derived weights.

### 15. `squair2021false` (2021)

- **Source:** [Original record](https://www.nature.com/articles/s41467-021-25960-2); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/34584091/).
- **Use:** Reserve: supports donor structure and independent biological units.
- **Access:** Indexed publisher Abstract/Results/Discussion extracts and PubMed complete authors verified; direct publisher open failed.
- **Support anchor:** Abstract; Results: False discoveries in single-cell DE; Discussion.
- **Supported claim:** Between-biological-replicate variability matters for valid differential-expression inference, and treating cell observations as substitutes for replicate-aware inference can create false discoveries.
- **Boundary:** This is evidence about differential expression, not a direct experiment on CellPFN or atlas-pretraining diversity. Use narrowly for donor-aware motivation or later Methods.

### 16. `azodi2021splatpop` (2021)

- **Source:** [Original record](https://link.springer.com/article/10.1186/s13059-021-02546-1); [cross-check or access route](https://pubmed.ncbi.nlm.nih.gov/34911537/).
- **Use:** Core or reserve: prevents overstating the novelty of donor-aware simulation.
- **Access:** Full publisher HTML opened; Abstract and Background inspected; PubMed metadata cross-check.
- **Support anchor:** Abstract; Background; Results: model overview.
- **Supported claim:** splatPop already models population-scale expression with known eQTLs, batch/cell-group effects and conditional differences between individuals or cohorts.
- **Boundary:** Donor/cohort-aware simulation is not novel by itself. CellPFN’s contribution should be the sampled task prior and its measured value for learning inference.

## Corrections to historical reference material

- Use the final **2025** scMultiSim Nature Methods paper, not the 2023 preprint.
- Use **2024** as scDesign3's issue year; its online publication date and DOI year are 2023.
- The 49-simulator evaluation is **Duo et al.**, with the complete author list verified against PMC. The old publication-strategy note incorrectly called it Liu et al.; an OpenAlex search extract was also incomplete.
- The cscGAN paper's first author is **Matteo Marouf**. The legacy bibliography note's Mohamed is incorrect.
- The final dyngen title begins **Spearheading future omics analyses**.
- Wood's final CVF proceedings entry has six authors; do not merge it with the different author list on the later arXiv record.
- No unverified DOI was manufactured. Wood and FlowNet retain official proceedings URLs; Tobin's IEEE DOI is verified, but its page range was not independently checked and is omitted.

## Remaining literature boundary

A 2026 scDesignPop record surfaced during donor-simulation searches ([PubMed](https://pubmed.ncbi.nlm.nih.gov/41808987/)). It is a follow-up lead, not a verified citation in this package. No assertion of being the first population-aware or procedural single-cell simulator is justified by this bounded search. The current manuscript does not need that assertion.


## Local verification

The citation-management validator parsed all 16 entries with zero errors and zero duplicates. Its one warning is Tobin’s omitted recommended page range, explicitly retained as unverified against the original proceedings source. JSON/key consistency checks passed. These checks establish file consistency, not independent scientific validation of the literature or the CellPFN results.
