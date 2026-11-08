# Balanced sampling: verified seed-0 comparison

All three columns use the same 12,077 validation photos, seed 0 and ONNX preprocessing.
Balanced training changed only inverse-city-frequency sampling; its logits are unadjusted.

| Method | Macro recall | Overall accuracy | ECE (15 bins) | Wrong mean confidence |
| --- | --- | --- | --- | --- |
| baseline_tau0 | 0.493478 | 0.522232 | 0.090188 | 0.539300 |
| baseline_tau1 | 0.512774 | 0.511799 | 0.078608 | 0.515175 |
| balanced_tau0 | 0.491359 | 0.503436 | 0.102839 | 0.537304 |

| City | Baseline tau 0 | Baseline tau 1 | Balanced tau 0 | Balanced vs baseline tau 0 (pp) |
| --- | --- | --- | --- | --- |
| seoul | 57.99% | 49.86% | 48.67% | -9.32 |
| busan | 39.57% | 51.94% | 44.53% | +4.96 |
| tokyo | 63.49% | 50.73% | 55.22% | -8.27 |
| osaka | 35.76% | 46.48% | 42.29% | +6.53 |
| taipei | 49.93% | 57.38% | 54.97% | +5.04 |

| True city to prediction | Baseline tau 0 | Baseline tau 1 | Balanced tau 0 |
| --- | --- | --- | --- |
| osaka_to_tokyo | 41.40% | 26.83% | 31.39% |
| tokyo_to_osaka | 11.36% | 18.84% | 18.47% |
| busan_to_seoul | 30.29% | 21.37% | 23.60% |
| seoul_to_busan | 7.52% | 15.07% | 9.65% |
| taipei_to_tokyo | 23.45% | 14.53% | 17.12% |
| taipei_to_seoul | 17.97% | 13.46% | 14.40% |

Balanced training: 34.8 minutes on CUDA at revision 78f24e0.
Official quick score: 0.2821; full-budget score: 0.4912.
Balanced ONNX evaluation: 530.02 seconds on Colab.

## Checks and scope

- Independently checked all 12,077 prediction cases, confidence bins, confusion, recalls, accuracy, ECE, error transitions and pair rates.
- Reconstructed probabilities from the exported numeric logit cache without loading a model or processing photos locally.
- Verified the five top-48 mistake sheet indexes against these predictions.
- Relative to baseline tau 0: 1,149 old errors corrected, 1,376 new errors, 1,336 rerouted but still wrong.
- Each city has expected sampling probability 20%; realized random draw counts are in verified_summary.json.
- The training-script score and diagnostic score differ slightly because of numeric inference paths and rounding.
- Only one balanced seed was trained. No significance or generalization claim follows from this comparison.
- This experiment does not establish that information/representation quality is the bottleneck.
- No recipe or Release was changed during import. Student interpretation and next experiment choice are pending.
