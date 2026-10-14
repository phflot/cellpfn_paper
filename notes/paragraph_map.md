# Argument and paragraph ownership

Each source paragraph has a stable comment ID. IDs survive reordering. This table maps scientific jobs, not final figure numbers. Primary result anchors are declarative records in `evidence/results.csv` and `evidence/task_exposure.csv`; their source columns and filters are authoritative.

| Paragraph | Scientific job | Evidence / literature |
|---|---|---|
| P-I01 | Motivate varied experimental context and donor diversity | Author-marked legacy motivation, scTab donor-vs-cell experiment |
| P-I02 | Establish representation-learning achievements and bounded opportunity | Geneformer, scGPT, scFoundation, UCE, TranscriptFormer; Kedzierska, DenAdel, Souza |
| P-I03 | Explain PFN principle and closest cellular precedents | MARS; PFN, TabPFN, TabICL; MapPFN and PerturbPFN |
| P-I04 | Explain simulation as a prior over tasks and why transfer is the test | Statistical/mechanistic/donor-aware simulators; synthesis; synthetic-to-real precedents; simulator evaluations |
| P-I05 | State two contributions and supporting architectural capabilities | Current export, no novelty superlative |
| P-R01 | What varies in the prior and why | fig1 facts; qualitative keys in result_summary |
| P-R02 | What information the model consumes and predicts | fig1 architecture/current neural-only contract; Deep Sets |
| P-R03 | Establish exposure units and bounded comparison | R01; T01–T07; TabICLv2 training section |
| P-R04 | Define biological tasks and comparison conditions | fig4; original PBMC and ZEBRA papers; comparator papers/cards |
| P-R05 | Establish competitive aggregate performance | R02–R07; three matched draws, model-specific input views |
| P-R05b | Retain strong support-trained conventional comparison | R54–R57; no LDA one-shot result; processed input route |
| P-R06 | Show regime dependence and development boundary | R08–R12; pretraining exposure notes; O01 |
| P-R07 | Test width extrapolation without gene vocabulary | R02, R13–R14, R41–R44 |
| P-R08 | Put width behavior in comparator context | R03–R04, R15–R16, R19; official TabPFN3.5 guardrail |
| P-R09 | Demonstrate transfer of cellular training to other architectures | T08–T10; R20–R25; prior-v2.2-B adaptation stream |
| P-R10 | Bound attribution of gains to task content | R26–R27; imperfect generic-table control |
| P-R11 | Preserve negative prespecified operator outcome | fig6 preregistration and later three-arm comparison |
| P-R12 | State task-design and realism boundaries | fig6 task mix; fig7 distributional audit |
| P-R13 | Define finite query-side explanation target | fig5 DS-LOO; Integrated Gradients for context |
| P-R14 | Validate approximation and distinguish timing evidence | R28–R35; O05 |
| P-R15 | Establish classifier faithfulness without biological causality | R36–R37, R46–R47 |
| P-R16 | Draft the existing provisional biological application | R38–R40; cohort citation; O02 |
| P-R17 | State what would establish disease-signature utility | O03; no completed experiment invented |

Main text retains task/support heterogeneity, input differences, development selection, the negative operator result and provisional disease status because they change interpretation. Full per-case numbers, run schedules and broader diagnostics remain in the evidence ledger for Methods/SI. Wave3 should combine architecture and prior facts into a concise opening display; the two central performance/transfer claims must each receive clear visual support. No figures are created in Wave1.
