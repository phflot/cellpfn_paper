# Terminology contract

| Use | Meaning | Avoid |
|---|---|---|
| Cellular prior | Distribution of cellular data-generating processes and prediction tasks defined by the simulator | Simulator as merely a benchmark or augmentation accessory |
| CellPFN reference model | Current exported G1v2′ endpoint, 12,329,889 parameters, direct neural logits | Seed's bounded analytic-expert residual |
| Synthetic-only weight training | Model optimization consumes simulated examples; real aggregates and development panels inform design | No real data used, real-data-free development |
| Gene-anonymous | No persistent feature identity across tasks; shared support/query coordinates within a task | Arbitrarily unaligned features, demonstrated cross-species universality |
| Support-conditioned inference | Predictions use labelled examples without target-task gradient updates | Zero-shot annotation |
| Scheduled episode | A scheduled support/query training problem, including zero-weight episodes | An independent simulated biological dataset |
| Simulator bank | Reused generated dataset supplying multiple task views | Interchangeable with episode count |
| Limited task exposure | Bounded count comparison with the cited training exposure of another release | Measured FLOP/wall-clock efficiency or matched-budget learning advantage |
| Continued training | Added cellular tasks plus generic replay starting from released weights | Training from scratch or total lifetime exposure |
| Competitive | Descriptive performance in stated tasks and support regimes | Proven equivalence, universal superiority |
| Transcriptome-scale | All measured gene coordinates retained in the specified exported dataset | Every possible gene or absence of feature-processing choices |
| DS-LOO deletion | Query gene set to zero while support and its covariance fit remain fixed | Mechanistic perturbation prediction or biological gene knockout |
| Margin reversal | Original predicted class versus its original runner-up crosses zero | Complete multiclass error-rate change |
| Provisional neuropathology association | Existing export under label/provenance review | Clinical diagnosis, clinical utility, demonstrated sex difference |

## Wave 2 names and interfaces

| Use | Meaning | Avoid |
|---|---|---|
| Baseline prior | Prior used in the 320K-episode initial stage and comparison diagnostics; raw export ID `v1_late`/`v1` | Project version labels in scientific prose |
| Cellular prior | Prior used in the final 64K reference episodes and tabular cellular adaptation; raw export ID `v2.2-B` | Implying every historical CellPFN episode used this configuration |
| PyTorch-compatible streaming simulator | CPU generator with NumPy/PyTorch computation and native tensor/IterableDataset interfaces | Fully Torch/GPU-native or automatically differentiable simulator |
| Gene–gene operator | Support-fitted pooled covariance channel with learned integration | A learned causal gene-regulatory graph |
| Program tokens | Learned computational summaries in CellPFN | Identified biological pathways |
| Simulator throughput | Direct measured generator performance under declared hardware/output contract | Model-job runtime, legacy unverified numbers, code capability as completed benchmark |
