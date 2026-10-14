# Pending simulator scalability benchmark

Status: specification only; no measurements were run for Wave 2.

## Claim and current evidence

The implemented simulator supports microbatch tensor delivery, reuse of fixed biological state and independent process producers. These are source-supported architectural properties. They do not establish a particular throughput, a million-cell completed run or a speedup over another simulator.

Legacy `scIntDesign.tex` claims one million cells in 126 s on a 128-core CPU and one billion cells in 60–70 h including compression. Another historical strategy note gives a conditional 375 s example. No matching configuration/hardware/run receipts were located. These numbers are excluded from the manuscript. Export `runtime_jobs.csv` measures model jobs, not simulator-only throughput.

Official scDesign3 documentation permits varying `ncell` and describes Gaussian-copula, marginal-fit and multivariate-normal accelerations. No universal million-cell ceiling is established: https://songdongyuan1994.github.io/scDesign3/docs/index.html (accessed 2026-10-14).

## Fixed experiment design for subsequent execution

- Grid: 10,000, 100,000 and 1,000,000 cells; 2,000 and 8,192 genes; seeds 0, 1 and 2. Keep biological complexity and configuration fixed across cell-count sizes.
- Pin both code revisions and all dependencies. Use the same dedicated CPU host; record CPU model, physical cores, BLAS/OpenMP thread limits, RAM, operating system and storage. Record time and memory caps before any run; run no competing jobs.
- Use one fixed PBMC reference with a saved donor/cell-type selection and gene panel for scDesign3 fitting, reused across output cell counts. Retain the exact input hash. This tests computational scaling, not equality of the statistical models or relative realism.
- For scDesign3 use Gaussian copula with documented practical acceleration options, `usebam=TRUE`, `fastmvn=TRUE` and an explicitly saved correlation-feature selection. Report actual retained correlation features; do not silently drop output genes. Pin the package/API before execution and record accepted options in the receipt.
- Compare counts-only outputs. Separately report fixed biological initialization or reference fitting, count sampling, tensor delivery and compressed H5AD disk output. Do not charge fitting repeatedly when reusing the same fitted model.
- Evaluate the direct CellStream interface independently of AnnData collation. Consume microbatches without retaining the full dataset, while checksumming counts to ensure work occurred. Measure a fixed 1,024-cell microbatch and report its actual tensor bytes.
- Evaluate export with the same output layers for both methods. Separately record the cost of simulator-only clean-profile/intensity truth layers. Do not call the existing dense million-cell collator bounded-memory streaming.
- Record elapsed seconds, cells/s, peak process-tree RSS, initialization time, output size, count checksum, completion status, stderr and resource caps for every run. Include all repeated runs, including timeouts/OOMs.

## Interpretation rules

Report medians and the range of the three runs, with all individual values as source data. A failure establishes feasibility only for the named configuration, hardware and caps. Do not extrapolate an unobserved billion-cell runtime, treat skipped runs as zero, or infer a universal limitation of scDesign3. No architecture ablation is required by this protocol. A numerical speed claim remains pending until the corresponding receipts exist.
