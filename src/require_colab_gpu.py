"""Stop the Colab queue before training if no GPU is connected."""
import torch

if not torch.cuda.is_available():
    raise SystemExit("Choose Runtime > Change runtime type > T4 GPU, then Run all. Training has not started.")
print("Colab GPU ready:", torch.cuda.get_device_name(0), flush=True)
