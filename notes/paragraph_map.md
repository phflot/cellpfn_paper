# Argument and paragraph ownership

Each source paragraph has a stable comment ID. IDs survive reordering. This table maps scientific jobs, not final figure numbers. Primary result anchors are declarative records in `evidence/results.csv`, `evidence/attribution_extension.csv` and `evidence/task_exposure.csv`; their source columns and filters are authoritative. Six unresolved scientific claims are tracked separately in `open_claims.md`.

| Paragraph | Scientific job | Evidence / literature |
|---|---|---|
| P-I01 | Motivate varied experimental context and donor diversity | Author-marked legacy motivation, scTab donor-vs-cell experiment |
| P-I02 | Establish representation-learning achievements and bounded opportunity | Geneformer, scGPT, scFoundation, UCE, TranscriptFormer; Kedzierska, DenAdel, Souza |
| P-I03 | Explain PFN principle and closest cellular precedents | MARS; PFN, TabPFN, TabICL; MapPFN and PerturbPFN |
| P-I04 | Explain simulation as a prior over tasks and why transfer is the test | Statistical/mechanistic/donor-aware simulators; synthesis; synthetic-to-real precedents; simulator evaluations |
| P-I05 | State two contributions and quantitative tests of their boundaries | Current export, no novelty superlative |
| P-R01 | What varies in the prior and why | fig1 facts; qualitative keys in result_summary |
| P-R02 | What information the model consumes and predicts | fig1 architecture/current neural-only contract; Deep Sets |
| P-R03 | Establish exposure units and bounded comparison | R01; T01–T07; TabICLv2 training section |
| P-R04 | Define biological tasks and comparison conditions | fig4; original PBMC and ZEBRA papers; comparator papers/cards |
| P-R05 | Establish competitive aggregate performance | R02–R07; three matched draws, model-specific input views |
| P-R05b | Retain strong support-trained conventional comparison | R54–R57; no LDA one-shot result; processed input route |
| P-R06 | Show regime dependence and development boundary | R08–R12; pretraining exposure notes; O01 |
| P-R06b | Distinguish coarse/fine PBMC annotation from post hoc harder subtype tasks | X89–X159; matched 8,192-HVG context; S9; task-specific support-draw counts |
| P-R07 | Test width extrapolation and support-dependent effects | R02, R13–R14, R41–R44, R58–R66; S3 |
| P-R08 | Put width behavior in comparator context | R03–R04, R15–R16, R19; official TabPFN3.5 guardrail |
| P-R09 | Demonstrate transfer and retain adverse task-specific change | T08–T10; R20–R25, R67–R69; Table1/S2 |
| P-R10 | Quantify task-stream consistency and generic retention costs | R26–R27, R70–R73, R158–R159; unmatched generic control; S2 |
| P-R11 | Quantify operator effects without replacing the failed frozen test | R74–R87; fig6 three-arm comparison and frozen outcome; S4 |
| P-R12 | Report the ten-candidate prior screen, including guard failures | R88–R101; S5; one model seed, three task streams |
| P-R12b | Quantify learnable-task accuracy/log-loss tradeoff and exposure confound | R102–R128; S6; twenty paired support draws |
| P-R12c | Quantify realism agreement and discrepancy with calibrated references | R129–R153; S7; statistic-specific units |
| P-R18 | Quantify sex prediction across distinct evaluation settings and identify missing gene evidence | X01–X40; S9; GSM-disjoint original case and later unit-level tasks; O06 |
| P-R13 | Define finite query-side explanation target | fig5 DS-LOO; Integrated Gradients for context |
| P-R14 | Validate approximation and distinguish timing evidence | R28–R35; O05 |
| P-R15 | Report selected known cell-type marker matches without implying enrichment | X47–X88; R36–R37; S8; Hao, Schafflick and Gong primary marker sources |
| P-R15b | Establish classifier faithfulness and quantify context sensitivity | R46–R47, R154–R157; S8; original runner-up margin reversal and support sensitivity |
| P-R16 | Draft the existing provisional biological application | R38–R40; cohort citation; O02 |
| P-R17 | State what would establish disease-signature utility | O03; no completed experiment invented |

Main text retains task/support heterogeneity, input differences, development selection, negative operator/prior outcomes and provisional disease status because they change interpretation. Supporting numerical tables are now included in the same PDF; the machine-readable ledgers bind their values to source rows. Wave3 should combine architecture and prior facts into a concise opening display; the two central performance/transfer claims need clear visual support within the four main display slots remaining after Tables 1 and 2. No figures are created in Wave1.
