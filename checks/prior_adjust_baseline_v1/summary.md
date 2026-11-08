# prior_adjust_baseline_v1: verified diagnostic results

Both saved baseline models were evaluated on the same 12,077 validation photos.
All tau values reuse each model's original ONNX logits. No retraining occurred.
The evaluator completed at revision bfa91cc. All 72,462 model/tau prediction cases
were independently checked from the exported prediction CSVs.
Numbers below are arithmetic means of the two model-specific metrics.

| Tau | Macro recall | Overall accuracy | ECE (15 bins) | Mean confidence on current errors |
| --- | --- | --- | --- | --- |
| 0 | 0.498212 | 0.524675 | 0.087887 | 0.538763 |
| 0.5 | 0.511549 | 0.523557 | 0.077591 | 0.526057 |
| 1 | 0.516638 | 0.514159 | 0.077232 | 0.517338 |

## City recall

| City | Tau 0 | Tau 0.5 | Tau 1 | Change 0 to 1 (percentage points) |
| --- | --- | --- | --- | --- |
| seoul | 59.36% | 55.98% | 51.11% | -8.25 |
| busan | 40.68% | 47.16% | 52.99% | +12.30 |
| tokyo | 62.46% | 56.65% | 50.17% | -12.29 |
| osaka | 35.62% | 40.98% | 45.65% | +10.03 |
| taipei | 50.98% | 55.02% | 58.40% | +7.42 |

## Pair error rates

Denominator: all validation photos of the true/source city.

| True city to prediction | Tau 0 | Tau 0.5 | Tau 1 |
| --- | --- | --- | --- |
| osaka_to_tokyo | 39.22% | 31.93% | 25.54% |
| tokyo_to_osaka | 11.63% | 14.94% | 18.81% |
| busan_to_seoul | 30.79% | 25.83% | 21.94% |
| seoul_to_busan | 7.29% | 10.27% | 15.09% |
| taipei_to_tokyo | 21.36% | 16.96% | 13.11% |
| taipei_to_seoul | 18.57% | 16.30% | 13.69% |

## Error transitions

| Model | Tau | Corrected old errors | New errors | Rerouted but still wrong |
| --- | --- | --- | --- | --- |
| baseline_seed0 | 0.5 | 341 | 342 | 325 |
| baseline_seed0 | 1 | 607 | 733 | 696 |
| baseline_seed1 | 0.5 | 295 | 321 | 319 |
| baseline_seed1 | 1 | 576 | 704 | 618 |

## Scope

- Comparisons use full validation, not just the 48 most confident mistakes.
- Tau 0 was recomputed using the same ONNX backend as the adjusted predictions.
- Its differences from the training-script scores are recorded in report.json.
- ECE is sample weighted under the validation class mixture. Macro recall gives every city equal weight.
- The mean confidence on current errors changes its sample population; fixed-error metrics are in metrics.csv.
- These are development-set comparisons, not an independent test of a selected tau.
- No tau has been chosen for submission automatically. Track A inputs remain unchanged.
- The student's interpretation and next experiment choice are pending.
