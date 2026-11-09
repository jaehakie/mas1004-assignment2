"""Pure configuration and bookkeeping for the researched Track B experiment."""
import hashlib
import json
import math


def make_plan(quick=False):
    return {
        "schema": 1, "model": "efficientnet_b3", "weights": "IMAGENET1K_V1",
        "size": 300, "small_size": 240, "small_epochs": 0 if quick else 3,
        "epochs": 1 if quick else 8, "batch_size": 32, "head_only_epochs": 0 if quick else 1,
        "backbone_lr": 3e-5, "head_lr": 3e-4, "weight_decay": 0.05,
        "label_smoothing": 0.1, "ema_decay": 0.99,
        "max_active_minutes": 4 if quick else 100,
        "seed": 0, "taus": [0.0] if quick else [0.0, 0.5, 1.0],
        "quick": quick, "quick_steps": 20 if quick else None,
        "sampling": "ordinary shuffle; no class balancing",
        "augmentation": "random resized crop scale 0.35..1, horizontal flip, stage-wise color jitter",
        "validation": "full validation at 300px with official grader preprocessing; smoke uses a stride",
    }


def fingerprint(plan, dataset_id, script_hashes):
    value = {"plan": plan, "dataset_id": dataset_id, "scripts": script_hashes}
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def train_size(plan, epoch):
    return plan["small_size"] if epoch < plan["small_epochs"] else plan["size"]


def lr_factor(step, total_steps):
    warm = max(1, int(total_steps * 0.05))
    if step < warm:
        return 0.1 + 0.9 * step / warm
    progress = min(1.0, max(0.0, (step - warm) / max(1, total_steps - warm)))
    return 0.01 + 0.99 * 0.5 * (1 + math.cos(math.pi * progress))


def next_cursor(epoch, completed_batches, batches_per_epoch):
    if not 0 <= completed_batches <= batches_per_epoch:
        raise ValueError("Invalid completed-batch count")
    return (epoch + 1, 0) if completed_batches == batches_per_epoch else (epoch, completed_batches)


def choose_tau(evaluations):
    """Largest development macro recall; exact ties prefer less correction."""
    if not evaluations:
        raise ValueError("No validation measurements")
    return max(evaluations, key=lambda row: (row["macro_recall"], -row["tau"]))


def validate_resume(saved, expected_fingerprint):
    if saved.get("fingerprint") != expected_fingerprint:
        raise ValueError("Checkpoint configuration, data or code changed; use a new tag.")
    if saved.get("epoch", -1) < 0 or saved.get("next_batch", -1) < 0:
        raise ValueError("Invalid checkpoint cursor")
