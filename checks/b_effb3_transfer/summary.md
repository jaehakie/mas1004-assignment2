# EfficientNet-B3 300px: verified first Track B submission

- Training revision: `1582429`, seed 0, Tesla T4.
- Training stopped at the planned active-time budget after 10,503 steps,
  336,096 draws and 7.594360 epochs. It did not complete eight epochs.
- Submitted weights: EMA checkpoint selected at epoch **7.0**.
- Active time including final validation/export: **105.06 minutes**.
- Training images: all 44,257 starter photos. No extra images were added.

| Tau | Validation macro recall | Overall accuracy | ECE (15 bins) |
| --- | --- | --- | --- |
| 0 | 51.4952% | 54.1691% | 0.029435 |
| 0.5 | 52.6336% | 53.6060% | 0.024854 |
| **1** | **52.9979%** | 52.2315% | 0.032089 |

Tau 1 was selected by development-set macro recall. Tau 0.5 has lower ECE;
tau 0 has higher ordinary accuracy. These are different selection criteria.

| City | Recall at selected tau 1 |
| --- | --- |
| Seoul | 46.8583% |
| Busan | 52.4460% |
| Tokyo | 47.7970% |
| Osaka | 53.2425% |
| Taipei | 64.6456% |

The full 12,077-photo validation logits were produced on CUDA in float32
with official grader preprocessing. All 36,231 model/tau prediction cases
were recomputed independently from that numeric cache. No local image or
model inference was used. ONNX export equivalence and official format/limit
checks passed; a separate full CPU ONNX validation pass was not performed.

## Export checks

| Measurement | Submitted model | Limit |
| --- | --- | --- |
| Stored parameters | 10,660,275 | 12,000,000 |
| GMAC per image | 1.825613072 | 2.0 |
| File size | 42.767167 MB | 95 MB |
| Input | 300 x 300 | 96–512 |

Official output: **format and limits: OK**.

Release: [track-b-1 — EfficientNet-B3 300px progressive transfer](https://github.com/jaehakie/mas1004-assignment2/releases/tag/track-b-1).

This is one combined transfer-learning experiment, not an ingredient-level
ablation or an independent test after checkpoint/tau selection. The default
ResNet18 Track B baseline was never trained, so no measured improvement over
that baseline is claimed. Leaderboard grading is pending.
