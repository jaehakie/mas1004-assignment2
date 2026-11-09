# Track B model research and chosen experiment, 2026-11-09

The student requested a model other than the default ResNet18, informed by
open-source work and research, with approximately 1–2 hours of free Colab
GPU time. The student selected **EfficientNet-B3 at 300px**. No new Track B
training or measured improvement has occurred yet.

## Constraints and candidate choice

The official limits are 12,000,000 stored parameters, 2 GMAC per image,
95 MB ONNX file size and input size 96–512. The official `rules.py` and
`check_submission.py` remain authoritative; published FLOP estimates are
not a substitute for measuring the submitted ONNX graph.

| Candidate | Published evidence | Decision |
| --- | --- | --- |
| EfficientNet-B3, ImageNet V1, 300px | torchvision 0.21 lists ImageNet top-1 82.008%, 12,233,232 parameters with 1,000 classes, 1.83 GFLOPS | Selected. Replacing the 1,536-to-1,000 classifier with 1,536-to-5 gives 10,703,917 trainable parameters before ONNX counting; profile before training. |
| EfficientNet-B1 V2 | torchvision lists ImageNet top-1 79.838%; smaller architecture | Viable lower-cost alternative, not selected. |
| MobileNetV3-Large V2, larger input | Existing assignment implementation; small enough for 448px | Student was offered this alternative and chose B3. |
| StreetCLIP | Geographic pretraining on 1.1M street-level images; CLIP ViT-L/14 at 336px | Relevant research, but large direct model exceeds submission size constraints. Teacher distillation would need extra inference and a separate measured experiment. Not used. |
| CosPlace | Place-recognition code and pretrained descriptors, including ResNet18 | Useful related work. Its retrieval objective and SF-XL training domain do not establish superiority on these five cities. No weights or dataset used. |
| Large extra street datasets | Place recognition benefits from domain-relevant data, but new city labels, provenance and train/validation separation must be checked | No extra photographs have been collected or automatically excluded in this experiment. |

ImageNet accuracy is evidence for considering a backbone, not an estimate of
city-classification accuracy. There is no demonstrated globally best model
for this assignment under the current compute budget.

## Implemented transfer-learning protocol

- Official torchvision EfficientNet-B3 ImageNet V1 weights; five-city head.
- Target evaluation/export size 300px. Train at 240px for the first three
  epochs, then 300px. Planned maximum eight epochs and 100 active minutes,
  reserving additional time for final validation and export.
- First epoch trains the new classifier with backbone features and batch
  statistics frozen. Then fine-tune with separate peak learning rates:
  backbone 3e-5, classifier 3e-4, warmup/cosine decay.
- Retain the original random-crop/horizontal-flip augmentation and label
  smoothing. Color jitter increases from 0.1 to 0.2 with image size.
- Maintain an exponential moving average of weights and choose a checkpoint
  by development-set macro recall. This is model selection on validation,
  not an independent performance test.
- Evaluate tau 0, 0.5 and 1 on the same logits; choose by validation macro
  recall with lower tau breaking exact ties. Ordinary shuffled sampling is
  used, so this is not double correction after class-balanced sampling.
- Fold the selected adjustment into the existing classifier bias once.
- Save resumable checkpoints on Drive outside results/submission so they
  are not included in the download ZIP. Save actual steps and elapsed active
  time; interrupted or time-limited runs are not described as eight epochs.
- Profile the architecture in ONNX and run a 20-step smoke check before the
  long run. Validate the final exported submission with official tooling.

This combines several changes for a first feasible Track B submission. It
is not an ablation that isolates the effect of each change, and the original
Track B ResNet18 baseline was never trained because of the GPU quota.

## Primary sources

1. [EfficientNet paper, ICML 2019](https://arxiv.org/abs/1905.11946)
2. [torchvision 0.21 EfficientNet-B3 weights and model statistics](https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.efficientnet_b3.html)
3. [EfficientNetV2 progressive learning, ICML 2021](https://proceedings.mlr.press/v139/tan21a.html)
4. [Logit adjustment, ICLR 2021](https://arxiv.org/abs/2007.07314)
5. [StreetCLIP authors' model card](https://huggingface.co/geolocal/StreetCLIP)
6. [CosPlace official code, CVPR 2022](https://github.com/gmberton/CosPlace)
7. [torchvision official classification training references](https://github.com/pytorch/vision/tree/v0.21.0/references/classification)

The progressive-size schedule is an adaptation of an idea, not a reproduction
of EfficientNetV2's architecture or its full training recipe. The EMA and
fine-tuning settings are engineering choices to test, not guaranteed gains.
