"""Researched EfficientNet-B3 Track B transfer learning, run only on Colab GPU.

Preflight ONNX limits, progressive input size, EMA, resumable checkpoints,
development-only logit adjustment and an honest active-time budget.
The supplied official/rules/export/check_submission files are not modified.
"""
import argparse
import copy
import csv
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms as T

import eval_logit_adjustment as evaluation
import rules
from export import export_onnx
from transfer_plan import choose_tau, fingerprint, lr_factor, make_plan, next_cursor, train_size, validate_resume

ROOT = Path(__file__).resolve().parents[1]


def commit_id():
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout.strip()


def atomic_torch_save(value, path):
    temporary = path.with_suffix(path.suffix + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


class TrainPhotos(Dataset):
    def __init__(self, rows, plan, epoch):
        self.rows, self.plan, self.epoch = rows, plan, epoch
        size = train_size(plan, epoch)
        jitter = 0.1 if size < plan["size"] else 0.2
        self.transform = T.Compose([
            T.RandomResizedCrop(size, scale=(0.35, 1.0)), T.RandomHorizontalFlip(),
            T.ColorJitter(jitter, jitter, jitter), T.ToTensor(), T.Normalize(rules.MEAN, rules.STD)])

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        path, city = self.rows[index]
        # Per-photo/epoch augmentation is independent of worker scheduling or
        # a mid-epoch resume. Preserve the process's unrelated CPU RNG state.
        with torch.random.fork_rng(devices=[]):
            torch.random.default_generator.manual_seed(self.plan["seed"] + self.epoch * 1000003 + index)
            image = self.transform(rules.load_photo(path))
        return image, rules.CITIES.index(city)


class ValidationPhotos(Dataset):
    def __init__(self, rows, size):
        self.rows, self.size = rows, size
        self.mean = torch.tensor(rules.MEAN).view(3, 1, 1)
        self.std = torch.tensor(rules.STD).view(3, 1, 1)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        path, city = self.rows[index]
        image = torch.from_numpy(rules.grader_input(rules.load_photo(path), self.size))
        return (image - self.mean) / self.std, rules.CITIES.index(city)


@torch.no_grad()
def predict(net, rows, plan, workers, use_amp):
    net.eval()
    loader = DataLoader(ValidationPhotos(rows, plan["size"]), batch_size=64,
                        num_workers=workers, pin_memory=True,
                        generator=torch.Generator().manual_seed(800001))
    outputs, labels = [], []
    for x, y in loader:
        x = x.to("cuda", non_blocking=True).to(memory_format=torch.channels_last)
        with torch.autocast("cuda", dtype=torch.float16, enabled=use_amp):
            outputs.append(net(x).float().cpu().numpy())
        labels.append(y.numpy())
    return np.concatenate(outputs), np.concatenate(labels)


def evaluate(logits, labels, prior, taus):
    measurements = []
    for tau in taus:
        measured, _, _ = evaluation.metrics(evaluation.adjust_logits(logits, prior, tau),
                                            labels, list(rules.CITIES), 15, logits.argmax(1))
        measured["tau"] = tau
        measurements.append(measured)
    return measurements


@torch.no_grad()
def update_ema(ema, live, updates, decay):
    # Warm-start the average so the initial random head is not overweighted.
    decay = min(decay, (1 + updates) / (10 + updates))
    source = live.state_dict()
    for key, value in ema.state_dict().items():
        if value.is_floating_point():
            value.mul_(decay).add_(source[key], alpha=1 - decay)
        else:
            value.copy_(source[key])


def rng_state():
    return {"python": random.getstate(), "numpy": np.random.get_state(),
            "torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all()}


def restore_rng(saved):
    random.setstate(saved["python"])
    np.random.set_state(saved["numpy"])
    torch.set_rng_state(saved["torch"])
    torch.cuda.set_rng_state_all(saved["cuda"])


def dataset_identity(train, val):
    digest = hashlib.sha256()
    base = ROOT / "data/starter"
    for path, city in [*train, *val]:
        digest.update(f"{path.relative_to(base).as_posix()}|{city}|{path.stat().st_size}\n".encode())
    return digest.hexdigest()


def profile_before_training(net, plan, cache, out):
    path = cache / "preflight.onnx"
    gap = export_onnx(net, path, plan["size"])
    measured = rules.measure_onnx(path, plan["size"])
    problems = list(measured["problems"])
    if measured["parameters"] > rules.TRACK_B_MAX_PARAMETERS:
        problems.append("Over the parameter limit")
    if measured["gmacs"] > rules.TRACK_B_MAX_GMACS:
        problems.append("Over the GMAC limit")
    if measured["file_mb"] > rules.TRACK_B_MAX_FILE_MB:
        problems.append("Over the file-size limit")
    evaluation.write_json(out / "profile.json", {**measured, "onnx_gap": gap, "problems": problems})
    if problems:
        raise ValueError("ONNX preflight rejected before training: " + "; ".join(problems))
    print(f"Preflight OK: {measured['parameters']:,} parameters, {measured['gmacs']:.3f} GMAC, "
          f"{measured['file_mb']:.1f} MB at {plan['size']}px", flush=True)


def append_experiment(row):
    path = Path(os.environ.get("MAS1004_EXPERIMENTS", ROOT / "experiments.csv"))
    fields = ["finished", "track", "tag", "seed", "official_budget", "budget", "val_score", *rules.CITIES,
              "train_seconds", "device", "selection", "recipe_sha", "selection_sha", "commit"]
    existing = []
    if path.exists():
        with path.open(newline="", encoding="utf-8-sig") as stream:
            existing = list(csv.DictReader(stream))
    previous = [item for item in existing if item["track"] == "B" and item["tag"] == row["tag"]]
    if previous:
        if len(previous) != 1 or any(str(previous[0].get(key, "")) != str(row.get(key, ""))
                                     for key in ("seed", "budget", "val_score", "selection")):
            raise ValueError("This tag has a different completed experiment row.")
        return previous[0]
    with path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        if not existing:
            writer.writeheader()
        writer.writerow(row)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", args.tag) or args.workers < 0:
        parser.error("Use a lowercase experiment tag and nonnegative worker count.")
    if args.quick and args.submit:
        parser.error("A smoke-test model must not become the actual submission.")
    if not torch.cuda.is_available():
        raise SystemExit("Connect a Colab GPU before running. No CPU training was started.")
    plan = make_plan(args.quick)
    out = ROOT / "results" / args.tag
    out.mkdir(parents=True, exist_ok=True)
    cache = ROOT / ".training_cache" / args.tag
    cache.mkdir(parents=True, exist_ok=True)
    random.seed(plan["seed"])
    np.random.seed(plan["seed"])
    torch.manual_seed(plan["seed"])
    torch.cuda.manual_seed_all(plan["seed"])
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_num_threads(2)
    train = rules.list_photos(ROOT / "data/starter/train")
    val = rules.list_photos(ROOT / "data/starter/val")
    counts = Counter(city for _, city in train)
    if len(train) != 44257 or len(val) != 12077 or any(not counts[c] for c in rules.CITIES):
        raise ValueError("Expected the unchanged complete starter training/validation sets.")
    if args.quick:
        val = val[::max(1, len(val) // 200)]
    data_id = dataset_identity(train, val)
    source_hashes = {name: evaluation.canonical_sha(ROOT / "src" / name)
                     for name in ("train_b_transfer.py", "transfer_plan.py", "rules.py", "export.py", "eval_logit_adjustment.py")}
    run_id = fingerprint(plan, data_id, source_hashes)
    prior = np.array([counts[c] for c in rules.CITIES], dtype=np.float64)
    prior /= prior.sum()
    if (out / "plan.json").exists():
        if json.loads((out / "plan.json").read_text())["fingerprint"] != run_id:
            raise ValueError("An existing tag has a different plan/data/code. Use a new tag.")
    if (out / "result.json").exists():
        completed = json.loads((out / "result.json").read_text())
        if completed.get("status") == "complete":
            if completed["fingerprint"] != run_id:
                raise ValueError("Completed tag belongs to a different experiment.")
            for name, item in completed["assets"].items():
                if evaluation.file_sha(out / name) != item["sha256"]:
                    raise ValueError("Completed artifact changed: " + name)
            if args.submit:
                (ROOT / "submission").mkdir(exist_ok=True)
                for name in ("model.onnx", "submission.json"):
                    shutil.copyfile(out / name, ROOT / "submission" / name)
            print("Completed experiment reused; no training repeated.", flush=True)
            return
    evaluation.write_json(out / "plan.json", {"plan": plan, "fingerprint": run_id,
                                              "script_hashes": source_hashes, "training_counts": dict(counts)})
    net = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)
    net.classifier[-1] = nn.Linear(net.classifier[-1].in_features, len(rules.CITIES))
    profile_before_training(net, plan, cache, out)
    net = net.to("cuda").to(memory_format=torch.channels_last)
    ema = copy.deepcopy(net).eval()
    ema.requires_grad_(False)
    optimizer = torch.optim.AdamW([
        {"params": net.features.parameters(), "lr": plan["backbone_lr"]},
        {"params": net.classifier.parameters(), "lr": plan["head_lr"]}], weight_decay=plan["weight_decay"])
    scaler = torch.amp.GradScaler("cuda")
    batches = len(train) // plan["batch_size"]
    total_steps = plan["quick_steps"] if args.quick else plan["epochs"] * batches
    epoch, start_batch, step, seen = 0, 0, 0, 0
    previous_seconds, best_score, history = 0.0, -1.0, []
    last_path, best_path = cache / "last.pt", cache / "best.pt"
    if last_path.exists():
        # Only self-created checkpoint files from this exact code/data/plan.
        saved = torch.load(last_path, map_location="cpu", weights_only=False)
        validate_resume(saved, run_id)
        net.load_state_dict(saved["model"])
        ema.load_state_dict(saved["ema"])
        optimizer.load_state_dict(saved["optimizer"])
        scaler.load_state_dict(saved["scaler"])
        epoch, start_batch = saved["epoch"], saved["next_batch"]
        step, seen = saved["step"], saved["seen"]
        previous_seconds, best_score, history = saved["active_seconds"], saved["best_score"], saved["history"]
        restore_rng(saved["rng"])
        print(f"Resuming {args.tag}: epoch {epoch + 1}, next batch {start_batch}, step {step}", flush=True)
        del saved
    started = time.monotonic()

    def active_seconds():
        return previous_seconds + time.monotonic() - started

    def checkpoint(next_epoch, next_batch):
        atomic_torch_save({"fingerprint": run_id, "model": net.state_dict(), "ema": ema.state_dict(),
                           "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                           "epoch": next_epoch, "next_batch": next_batch, "step": step, "seen": seen,
                           "active_seconds": active_seconds(), "best_score": best_score,
                           "history": history, "rng": rng_state()}, last_path)

    print(f"{args.tag}: EfficientNet-B3, target 300px, {len(train)} training photos, "
          f"up to {plan['epochs']} epochs / {plan['max_active_minutes']} active minutes", flush=True)
    stop_reason = "planned_steps_complete"
    while epoch < plan["epochs"] and step < total_steps:
        if active_seconds() >= plan["max_active_minutes"] * 60 and best_path.exists():
            stop_reason = "active_time_budget"
            break
        size = train_size(plan, epoch)
        net.train()
        head_only = epoch < plan["head_only_epochs"]
        net.features.requires_grad_(not head_only)
        if head_only:
            net.features.eval()
        order = torch.randperm(len(train), generator=torch.Generator().manual_seed(plan["seed"] + epoch)).tolist()
        epoch_batches = [order[i * plan["batch_size"]:(i + 1) * plan["batch_size"]] for i in range(batches)]
        if args.quick:
            epoch_batches = epoch_batches[:plan["quick_steps"]]
        loader = DataLoader(TrainPhotos(train, plan, epoch),
                            batch_sampler=epoch_batches[start_batch:], num_workers=args.workers,
                            pin_memory=True, generator=torch.Generator().manual_seed(91000 + epoch))
        completed_batches = start_batch
        losses = []
        for batch_index, (x, y) in enumerate(loader, start=start_batch):
            if active_seconds() >= plan["max_active_minutes"] * 60 and step > 0:
                stop_reason = "active_time_budget"
                break
            factor = lr_factor(step, total_steps)
            for group, peak in zip(optimizer.param_groups, (plan["backbone_lr"], plan["head_lr"])):
                group["lr"] = peak * factor
            x = x.to("cuda", non_blocking=True).to(memory_format=torch.channels_last)
            y = y.to("cuda", non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast("cuda", dtype=torch.float16):
                loss = nn.functional.cross_entropy(net(x), y, label_smoothing=plan["label_smoothing"])
            if not torch.isfinite(loss):
                raise ValueError("Nonfinite loss; checkpoint remains available for inspection.")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            step += 1
            seen += len(y)
            completed_batches = batch_index + 1
            update_ema(ema, net, step, plan["ema_decay"])
            losses.append(float(loss.item()))
            if step % 100 == 0 or args.quick:
                print(f"epoch {epoch + 1}/{plan['epochs']} {size}px, step {step}/{total_steps}, "
                      f"loss {losses[-1]:.4f}, active {active_seconds()/60:.1f} min", flush=True)
            if step % 500 == 0:
                cursor = next_cursor(epoch, completed_batches, batches)
                checkpoint(*cursor)
            if step >= total_steps:
                break
        if completed_batches == start_batch and best_path.exists():
            break
        logits, labels = predict(ema, val, plan, args.workers, use_amp=True)
        measures = evaluate(logits, labels, prior, plan["taus"])
        selected = choose_tau(measures)
        progress = epoch + completed_batches / batches
        event = {"epoch_progress": progress, "training_size": size, "head_only": head_only,
                 "step": step, "draws": seen, "active_seconds": active_seconds(),
                 "mean_loss": float(np.mean(losses)) if losses else None,
                 "validation_backend": "CUDA float16 EMA with grader preprocessing",
                 "evaluations": measures}
        history.append(event)
        evaluation.write_json(out / "history.json", history)
        if selected["macro_recall"] > best_score:
            best_score = selected["macro_recall"]
            atomic_torch_save({"fingerprint": run_id, "model": ema.state_dict(),
                               "epoch_progress": progress, "step": step,
                               "selection_measurement": selected}, best_path)
        print(f"Validation EMA: macro={selected['macro_recall']:.5f}, tau={selected['tau']:g}; "
              f"best development score={best_score:.5f}", flush=True)
        epoch, start_batch = next_cursor(epoch, completed_batches, batches)
        checkpoint(epoch, start_batch)
        if stop_reason == "active_time_budget" or step >= total_steps:
            break
    if not best_path.exists():
        raise ValueError("No trained checkpoint is available; no submission produced.")
    if args.quick and step != plan["quick_steps"]:
        raise ValueError("Smoke check did not finish all 20 steps; long training was not authorized by this check.")

    selected_checkpoint = torch.load(best_path, map_location="cpu", weights_only=False)
    if selected_checkpoint["fingerprint"] != run_id:
        raise ValueError("Best checkpoint belongs to a different experiment.")
    net.load_state_dict(selected_checkpoint["model"])
    net.eval()
    logits, labels = predict(net, val, plan, args.workers, use_amp=False)
    measurements = evaluate(logits, labels, prior, plan["taus"])
    selected = choose_tau(measurements)
    # Save numerical evidence for later comparisons without model inference.
    np.savez_compressed(out / "validation_logits.npz", logits=logits, true=labels,
                        cities=np.asarray(rules.CITIES), training_prior=prior)
    evaluation.write_csv(out / "validation_index.csv", [
        {"path": path.relative_to(ROOT / "data/starter").as_posix(), "true_city": city}
        for path, city in val])
    evaluation.write_csv(out / "tau_metrics.csv", [
        {"tau": item["tau"], "macro_recall": item["macro_recall"], "accuracy": item["accuracy"],
         "ece": item["ece"], **{c + "_recall": item["per_city_recall"][c] for c in rules.CITIES}}
        for item in measurements])
    with torch.no_grad():
        bias = net.classifier[-1].bias
        bias.sub_(selected["tau"] * bias.new_tensor(prior).log())
    export_gap = export_onnx(net, out / "model.onnx", plan["size"])
    final_profile = rules.measure_onnx(out / "model.onnx", plan["size"])
    if (final_profile["problems"] or final_profile["parameters"] > rules.TRACK_B_MAX_PARAMETERS
            or final_profile["gmacs"] > rules.TRACK_B_MAX_GMACS
            or final_profile["file_mb"] > rules.TRACK_B_MAX_FILE_MB):
        raise ValueError("Final ONNX model exceeds official limits; no submission copied.")
    actual_progress = epoch + start_batch / batches
    info = {"image_size": plan["size"],
            "starting_weights": "torchvision efficientnet_b3 IMAGENET1K_V1; EMA fine-tuning",
            "data": "data/starter/train",
            "summary": f"EfficientNet-B3 300px progressive transfer; {actual_progress:.2f} epochs; tau={selected['tau']:g}"}
    evaluation.write_json(out / "submission.json", info)
    commit = commit_id()
    result = {"status": "complete", "track": "B", "tag": args.tag, "quick": args.quick,
              "fingerprint": run_id, "plan": plan, "commit": commit, "script_hashes": source_hashes,
              "training_counts": dict(counts), "training_prior": dict(zip(rules.CITIES, prior.tolist())),
              "actual_steps": step, "actual_draws": seen, "actual_epoch_progress": actual_progress,
              "selected_checkpoint_epoch_progress": selected_checkpoint["epoch_progress"],
              "active_seconds_including_validation": active_seconds(), "stop_reason": stop_reason,
              "validation_photos": len(val), "validation_backend": "CUDA float32, official grader preprocessing",
              "validation_note": "Development score selected on this set; not independent test accuracy. ONNX backend can differ slightly.",
              "tau_evaluations": measurements, "selected_tau": selected["tau"],
              "val_score": selected["macro_recall"], "val_per_city": selected["per_city_recall"],
              "val_confusion": selected["confusion"], "onnx_gap": export_gap,
              "final_profile": final_profile, "submission": info,
              "assets": {name: {"sha256": evaluation.file_sha(out / name), "bytes": (out / name).stat().st_size}
                         for name in ("model.onnx", "submission.json")}}
    if not args.quick:
        from datetime import datetime
        row = {"finished": datetime.now().isoformat(timespec="seconds"), "track": "B", "tag": args.tag,
               "seed": plan["seed"], "budget": seen, "val_score": round(selected["macro_recall"], 4),
               **{c: round(selected["per_city_recall"][c], 4) for c in rules.CITIES},
               "train_seconds": round(result["active_seconds_including_validation"], 1), "device": "cuda",
               "selection": "efficientnet_b3 300px progressive; data/starter/train", "commit": commit}
        result["training_row"] = append_experiment(row)
    evaluation.write_json(out / "result.json", result)
    if args.submit:
        (ROOT / "submission").mkdir(exist_ok=True)
        for name in ("model.onnx", "submission.json"):
            shutil.copyfile(out / name, ROOT / "submission" / name)
    print(f"Complete {args.tag}: validation macro={selected['macro_recall']:.5f}, "
          f"tau={selected['tau']:g}, actual epochs={actual_progress:.3f}, "
          f"{final_profile['parameters']:,} parameters, {final_profile['gmacs']:.3f} GMAC", flush=True)
    print("Smoke check only; no full-training row added." if args.quick else
          "Submission exported. Run the official check_submission.py before Release.", flush=True)


if __name__ == "__main__":
    main()
