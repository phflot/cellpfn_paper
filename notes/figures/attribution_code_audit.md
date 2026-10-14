# Production DS-LOO code audit

## Decision

The implementation has been recovered. The missing-code, exact-formula and recorded-provenance components of M01 are resolved. The manuscript can now state the exact implemented estimator and its approximation boundaries. **M01 can remain closed as a missing-method/provenance item: the recovered source, complete checkpoint-pinned dependencies, historical consistency checks and cached-array reconciliation have now been verified.** Keep the absence of a fresh model-execution reproduction explicit in the handoff rather than continuing to claim the algorithm/code is missing.

There is **no analytical error bound** in this implementation. Use “approximation with explicit limitations” rather than “bounded-error estimator.”

## Source identity

Read all of `cellpfn_attr.py`, `dsloo.py`, `dsloo_corr.py`, `run_case.py` and the relevant aggregation blocks in `aggregate.py` from the recovered local snapshot. SHA256 for `cellpfn_attr.py` (`47be0b...0662c4`) and `aggregate.py` (`a0c4cb...43cde0`) exactly matches the original export's `build/knockout/sources_sha256.csv`, independently verified here. Current full hashes of the remaining scripts are:

- `dsloo.py`: `3e0efadac1f7c3c1974b27ac53babe117af202f5ec3b583064d8279f8f323a1a`
- `dsloo_corr.py`: `7ee0bce4379899ce942ba683cc45e555cd23f071a1e9eb99fa56f1e65d27983d`
- `run_case.py`: `cb0a57611fd9f634b9e92ee762b246e6d786b5a3a233b6405ff2dda6b2123383`

Those three files were not individually pinned in the old export inventory, so their current hashes establish a recovered snapshot, not proof that every byte is the historical execution copy. Historical output hashes and parity receipts provide the additional link.

## Exact computation and approximation boundary

1. **Target and selection.** `run_case.py:83–109` selects cells correctly classified under stored bfloat16 and a float32 rerun, then fixes the float32 predicted class and original runner-up. Query-only exact deletion is base minus the fixed-pair logit margin after setting a query gene to zero. The covariance support fit and other support summaries remain fixed; count-mode query depth is recomputed. Support-plus-query experiments refit support and are a separate intervention (`run_case.py:219–323`).

2. **Pairwise head reconstruction.** `dsloo.py:56–69` reconstructs the nonlinear head from pooled relation features and an additive learned operator embedding. `cellpfn_attr.py:236–316` reconstructs query/class-pair scoring using cached support state. The operator's class-centering step still uses distances to all classes, even though only predicted/runner-up logits need scoring.

3. **Pool changes.** `dsloo.py:151–215` caches sums, squared sums, top-two maxima with indices and log-sum-exp for every summary slot and relation feature. It exactly updates each pool for replacement of one relation vector **conditional on other gene relations and row-level scalars remaining fixed**. The RMS uses the model's epsilon and a nonnegative clamp on the replacement argument. The LSE log argument is clamped below at `1e-30`. Top-two statistics implement a maximum replacement, including maximum ties. Three relation evaluations per gene/chunk are used: original totals, original reconstruction and zero replacement; this is a sweep, not one standard prediction pass.

4. **Own-gene whitening channel.** Let `A = I − U diag(1 − (1+λ)^(-1/2)) Uᵀ`, `v = inverse_scale`, and `t_c = v ⊙ (z−μ_c)`. A deletion changes only `z_g` at fixed row depth in this component. The own-coordinate update is `(A t_c)_g + A_gg v_g (z_g^0−z_g)`, followed by the original `[-8,8]` clip, division by four and gate. This is exact for that coordinate. **The changes `A_hg v_g (z_g^0−z_g)` to other genes `h != g` are omitted**, so their relation vectors are left fixed. This omission is explicit in `dsloo.py:5–9,83–96,139–150`.

5. **Operator pair-scalar branch.** The algorithm also updates the operator's all-class Mahalanobis distances exactly at fixed depth: `M_c' = M_c + 2 δ_g [Σ⁻¹(z−μ_c)]_g + δ_g² [Σ⁻¹]_gg`, followed by the implementation's nonnegative clamp. It then recomputes class-centering, variance normalization, `asinh`, gate-weighted recentering, scalar gates and the nonlinear pair MLP. Thus the **pair MLP is reevaluated**, not itself differentiated as a first-order substitute. Its changed embedding enters the final direct scorer through a first-order expansion together with the pooled changes (`dsloo.py:99–105,217–239`). A pooled-statistic-only equation omits this implemented branch.

6. **Head linearization.** At the original query, the algorithm differentiates logits with respect to the pooled representation and additive pair embedding. It contracts those derivatives with exact conditional pool/embedding changes and takes base minus deletion. With concatenated predicted/runner-up states, the uncorrected margin estimate is `−∂H/∂P · ΔP_g − ∂H/∂h · Δh_g`. The operator term vanishes for the no-operator model. Exact head replay (`dsloo.py:250–276`) recomputes the full head on those approximate conditional states for selected genes; it isolates head linearization but **does not remove omitted whitening coupling or fixed-depth/fixed-detection error**.

7. **Depth/detection correction.** `dsloo_corr.py:34–59` makes depth and detected fraction independent scalar leaves and computes `m_d` and `m_q` at the original query. The corrected estimate adds `m_d x_g + m_q 1[x_g>0]/G` in count mode and only the detection term in processed mode. The derivative follows the differentiable full query-side operator in `cellpfn_attr.py:191–225`, so depth-induced effects across whitening coordinates are included to first order. It does not restore omitted **fixed-depth** cross-coordinate deletion effects. This is additive first-order correction and contains no finite-deletion remainder/error bound. The count-depth floor (`max(sum(x),1)`) and clipping can produce nondifferentiable boundaries; in particular `x_g` is the implemented depth-change factor even if deletion would hit the floor. Do not describe it as an exact normalization correction.

8. **Precision and execution.** Operator arithmetic is float64; relation/pool/head arrays and output attributions are float32; TF32 is disabled. Gradient routines toggle training mode and return to evaluation mode. Before asserting runtime identity, preserve the checkpoint configuration and confirm its dropout/state-dependent modules; the existing original-vs-gradient endpoint receipt is the direct empirical check. `load_model` strictly loads the checkpoint, pins full reference checkpoint SHA and a prefix for the no-operator checkpoint, and compares recorded model/dependency hashes for available dependency files (`cellpfn_attr.py:89–114`). Missing dependency files are not rejected by that loop, so a complete reproduction receipt should explicitly list and hash them.

## Aggregation details that matter

- Corrected cell Spearman correlation is computed over the **original exact-deletion gene set**, median over cells within class and median over classes. Undefined/constant-vector correlations return NaN and are excluded by `nanmedian`; no uncertainty interval is generated.
- The corrected relative L2 error is a **classwise Frobenius/flattened-vector ratio over genes × selected cells**, then median over classes (`aggregate.py:292–316`). It is not a median of independently normalized per-cell L2 errors.
- Additional DS-LOO-selected extreme genes are appended only to the uncorrected `*_incl_dsloo_top` metrics in the inspected aggregator. Do not imply the main corrected statistic includes those extra genes.
- Ranking uses class means of the signed cell-level attribution; marker checks are selected descriptive checks. The exact-gene validation union is method-enriched, not a uniform sample of all genes.
- Deletion “flip” is strict `margin_drop > original_margin` against the original runner-up, not recomputation of the new global argmax (`aggregate.py:208–226`). It is a fixed-pair margin reversal.

## Independently executed checks

On 50 deterministic small NumPy systems (17 genes, three classes, rank four), evaluated every gene: **850 algebra checks**. Maximum absolute discrepancies were `1.85e-13` for all-class Mahalanobis updates, `4.44e-15` for the own whitening-coordinate update, and `9.99e-16` for pooled mean/RMS/max/LSE replacement against direct recomputation. Off-diagonal channel changes were nonzero, demonstrating that the omitted term is a real computational approximation. These are implementation-algebra checks, not new biological evidence or a reproduction of the trained model.

### Recovered historical metadata, checked after the initial source audit

All **52 recovered JSON files** match their original export-inventory SHA256 hashes exactly. These include twelve original case/arm reports, twelve DS-LOO reports, twelve correction reports, twelve support-plus-query reports and four timing comparisons. No receipt was regenerated in this audit.

- All twelve DS-LOO receipts record `max_abs_R_vs_model = 0` and `channel_recompute_maxabs = 0`.
- Reference-model logit discrepancies are `0.0009918212890625` to `0.00103759765625`; no-operator discrepancies are `0.0001373291015625` to `0.000152587890625`. Therefore the replay is **not bit-identical at the final logit**; report the recorded maximum rather than claiming exact scorer identity.
- Original knockout-path permutation noise is at most `3.0517578125e-05` margin units. Recomputed selected baseline versus knockout-path baseline differs by at most `4.57763671875e-05`.
- Independently matched **78 exported gradient/noise diagnostics** to the corresponding original JSON values at the export's six-significant-digit precision. The largest unrounded absolute difference is `4.59e-06`, explained by that serialization.
- Original receipts record the full reference checkpoint SHA256 `aa5490d5a5d4020c87eba05297d80a31c901bcbeba6ba49b4b4857acb84f9f02` and no-operator checkpoint SHA256 `cee5126d995953c65db5819171becf54b2aca59aadd6fba0cbd055c619f2e763`, plus source SHA `031adb6a9b11295f23978c0f8574c4325f6cddc4b4bb43a69b1e893aad50d1af` and six dependency names.
- The correction receipts record exactly zero depth derivative for processed inputs and finite depth/detection derivative summaries for the count cases, consistent with the recovered code.

This establishes historical source/report identity and recorded consistency checks. It does not claim that a new GPU checkpoint execution reproduced those checks. Root-owned direct cached-array reconciliation supplies the output-to-figure link.

### Complete pinned dependency closure

Verified the full principal checkpoint SHA256 before loading its metadata using `torch.load(map_location="cpu", weights_only=True)`. CUDA remained uninitialized. The 148,092,883-byte checkpoint records `dropout=0.0` and all model dimensions/settings in `evidence/remote_model_source_manifest.json`.

All **seven checkpoint-pinned source modules** (direct model plus six dependencies) are present and match the expected SHA256, both remotely and after local retrieval into `input/remote_attribution/model_source/`. Syntax parsing succeeds for every recovered Python file. The additional real-cell case loader is archived and hash-verified against its current remote copy; it was not independently pinned by the original export or checkpoint and is explicitly identified as such in the manifest.

The historical loader's missing-file behavior mattered for exactly one dependency: `episodes.py` lives at `src/hashprompt/episodes.py`, consistent with the code's explicit `from hashprompt.episodes import DenseEpisodeBatch`, rather than its assumed `models/episodes.py`. The actual file's hash is `962729e8cadf1399c93cb57fe2b0771f40a66e78a09ef17860de26b129168fd5`, exactly matching the checkpoint. This audit resolves the path and verifies the source independently; no original loader/source was modified.

Root's independent recomputation from stored arrays covers all twelve case/arm combinations and 24 principal corrected-Spearman/relative-L2 metrics. This audit independently compared those recomputed metrics in `evidence/remote_attribution_validation.json` with the original export: maximum absolute difference **4.96034506247689e-7**, within its serialized precision. No new inference or attribution execution was performed. This is the completed cached-fixture link required for M01 provenance closure.

## Cached-fixture closure checklist

1. Match all recovered historical result NPZ/JSON and case-bundle hashes to the export inventory; also verify exact cell indices, class order, gene order and checkpoint identity. Save hashes of newly recovered scripts and full dependency sources.
2. **Completed for the historical metadata:** each `__dsloo.json` and original case JSON has been recovered and SHA matched; exact recorded maxima and 78 matching gradient/noise diagnostics are documented above. Gradient/evaluation endpoint comparison is printed in the original runner rather than stored as a dedicated JSON field, so do not claim a fresh check of that quantity.
3. **Completed for the principal fidelity fixtures:** root recomputed 24 corrected per-cell-Spearman/classwise-L2 metrics directly from stored arrays, and this audit independently matched them to the export as documented above. Marker/deletion figure checks are root-owned figure validations. Agreement to serialized precision closes the principal output-to-export link without GPU recomputation.
4. Confirm absent-gene attribution/deletion effects are zero up to recorded numerical noise. Verify correction array minus uncorrected array is finite and consistent with recorded output identity. Raw depth/detection gradient leaves are not saved, so algebraic reconstruction of each correction term from outputs alone is impossible; a fresh tiny frozen-case rerun is needed only if exact computational replay is required.
5. Record whether each part is **source verified**, **cached fixture reproduced**, or **fresh model execution reproduced**. M01 may be closed as a missing-method/provenance issue once 1–3 pass, while a separate runtime-reproduction limitation remains if a new checkpoint execution has not occurred.

Suggested active-text replacements are in `attribution_methods_patch.tex`; no active manuscript or unresolved-item register was edited by this audit.
