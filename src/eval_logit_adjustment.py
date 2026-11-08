"""Evaluate fixed post-hoc prior adjustments on saved baseline ONNX models.

No training, model rewriting, Track A recipe change, or automatic tau selection.
Each model is inferred once; tau values reuse those same cached logits.

References:
https://arxiv.org/abs/2007.07314
https://proceedings.mlr.press/v70/guo17a.html
"""

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CACHE_SCHEMA = 1


def file_sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, rows, fields=None):
    rows = list(rows)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def softmax(logits):
    logits = np.asarray(logits, dtype=np.float64)
    if logits.ndim != 2 or not np.isfinite(logits).all():
        raise ValueError("Expected finite two-dimensional logits.")
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=1, keepdims=True)


def adjust_logits(logits, prior, tau):
    prior = np.asarray(prior, dtype=np.float64)
    if np.any(prior <= 0) or not np.isclose(prior.sum(), 1.0):
        raise ValueError("Training priors must be positive and sum to one.")
    return np.asarray(logits, dtype=np.float64) - tau * np.log(prior)[None, :]


def calibration(probabilities, true, bins):
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == true
    indices = np.minimum((confidence * bins).astype(int), bins - 1)
    details, ece = [], 0.0
    for index in range(bins):
        mask = indices == index
        count = int(mask.sum())
        accuracy = float(correct[mask].mean()) if count else None
        mean_confidence = float(confidence[mask].mean()) if count else None
        gap = abs(accuracy - mean_confidence) if count else None
        if count:
            ece += count / len(true) * gap
        details.append({
            "bin": index, "lower": index / bins, "upper": (index + 1) / bins,
            "count": count, "accuracy": accuracy,
            "mean_confidence": mean_confidence, "absolute_gap": gap,
        })
    return float(ece), details


def error_transitions(true, baseline_pred, pred):
    old_wrong, new_wrong = baseline_pred != true, pred != true
    result = {
        "corrected_baseline_errors": int((old_wrong & ~new_wrong).sum()),
        "new_errors_on_baseline_correct": int((~old_wrong & new_wrong).sum()),
        "rerouted_still_wrong": int((old_wrong & new_wrong & (pred != baseline_pred)).sum()),
        "unchanged_still_wrong": int((old_wrong & new_wrong & (pred == baseline_pred)).sum()),
    }
    assert (result["corrected_baseline_errors"] - result["new_errors_on_baseline_correct"]
            == int(old_wrong.sum() - new_wrong.sum()))
    return result


def metrics(logits, true, cities, bins, baseline_pred):
    true = np.asarray(true, dtype=np.int64)
    probabilities = softmax(logits)
    if probabilities.shape != (len(true), len(cities)) or len(true) == 0:
        raise ValueError("Prediction dimensions do not match validation labels.")
    pred = probabilities.argmax(axis=1)
    confidence = probabilities.max(axis=1)
    confusion = np.zeros((len(cities), len(cities)), dtype=np.int64)
    np.add.at(confusion, (true, pred), 1)
    support = confusion.sum(axis=1)
    if np.any(support == 0):
        raise ValueError("Every city must have validation examples.")
    row_rates = confusion / support[:, None]
    recall = np.diag(row_rates)
    wrong, baseline_wrong = pred != true, baseline_pred != true
    ece, details = calibration(probabilities, true, bins)
    result = {
        "macro_recall": float(recall.mean()),
        "accuracy": float((pred == true).mean()),
        "per_city_recall": {city: float(recall[i]) for i, city in enumerate(cities)},
        "true_city_counts": {city: int(support[i]) for i, city in enumerate(cities)},
        "predicted_city_counts": {city: int((pred == i).sum()) for i, city in enumerate(cities)},
        "confusion": confusion.tolist(),
        "row_normalized_confusion": row_rates.tolist(),
        "wrong_count": int(wrong.sum()),
        "mean_confidence_on_current_errors": float(confidence[wrong].mean()) if wrong.any() else None,
        "mean_confidence_on_fixed_baseline_errors": float(confidence[baseline_wrong].mean()) if baseline_wrong.any() else None,
        "mean_true_class_probability_on_fixed_baseline_errors": float(probabilities[np.arange(len(true)), true][baseline_wrong].mean()) if baseline_wrong.any() else None,
        "ece": ece, "calibration_bins": details,
        "error_transitions": error_transitions(true, baseline_pred, pred),
        "pair_errors": {},
    }
    for source, target in (("osaka", "tokyo"), ("tokyo", "osaka"),
                           ("busan", "seoul"), ("seoul", "busan"),
                           ("taipei", "tokyo"), ("taipei", "seoul")):
        if source in cities and target in cities:
            i, j = cities.index(source), cities.index(target)
            result["pair_errors"][source + "_to_" + target] = {
                "count": int(confusion[i, j]),
                "rate_among_true_source_city": float(row_rates[i, j]),
            }
    return result, pred, confidence


def self_test():
    cities = ["a", "b"]
    true = np.array([0, 1])
    logits = np.log(np.array([[0.8, 0.2], [0.2, 0.8]]))
    result, pred, _ = metrics(logits, true, cities, 10, np.array([0, 1]))
    assert result["macro_recall"] == 1 and result["accuracy"] == 1
    assert np.isclose(result["ece"], 0.2)
    assert result["mean_confidence_on_current_errors"] is None
    wrong, _, _ = metrics(logits, true[::-1], cities, 10, pred)
    assert wrong["macro_recall"] == 0 and np.isclose(wrong["ece"], 0.8)
    assert np.isclose(wrong["mean_confidence_on_current_errors"], 0.8)
    assert wrong["confusion"] == [[0, 1], [1, 0]]
    imbalanced, _, _ = metrics(np.tile([10.0, 0.0], (4, 1)),
                               np.array([0, 0, 0, 1]), cities, 15, np.zeros(4, dtype=int))
    assert imbalanced["macro_recall"] == 0.5 and imbalanced["accuracy"] == 0.75
    assert np.allclose(softmax(logits + 1000), softmax(logits))
    assert np.allclose(softmax(adjust_logits(logits, [0.5, 0.5], 1)), softmax(logits))
    assert adjust_logits(np.zeros((1, 2)), [0.8, 0.2], 1).argmax() == 1
    ece, bins = calibration(np.eye(2), true, 15)
    assert ece == 0 and bins[-1]["count"] == 2
    changed = error_transitions(np.array([0, 0, 0]), np.array([1, 1, 0]), np.array([0, 2, 1]))
    assert changed == {"corrected_baseline_errors": 1, "new_errors_on_baseline_correct": 1,
                       "rerouted_still_wrong": 1, "unchanged_still_wrong": 0}
    json.dumps(result, allow_nan=False)
    print("Metric self-tests: OK", flush=True)


def selection_counts(selection, train_dir, cities):
    counts = Counter()
    with selection.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["path"]:
            raise ValueError("Expected a selection CSV with one path column.")
        for row in reader:
            rel = row["path"].replace("\\", "/")
            path = train_dir / rel
            if (rel.split("/")[0] not in cities or not path.is_file()
                    or train_dir.resolve() not in path.resolve().parents):
                raise ValueError("Invalid selection path: " + rel)
            counts[rel.split("/")[0]] += 1
    if any(counts[city] == 0 for city in cities):
        raise ValueError("Each city needs selected training photos.")
    return counts


def validation_fingerprint(rows, folder, rules_path):
    digest = hashlib.sha256(file_sha(rules_path).encode())
    for path, city in rows:
        stat = path.stat()
        digest.update(f"{city}|{path.relative_to(folder).as_posix()}|{stat.st_size}|{stat.st_mtime_ns}\n".encode())
    return digest.hexdigest()


def infer_or_cache(model, rows, true, data_id, cache_dir, args):
    import onnxruntime as ort
    import rules

    model_sha = file_sha(model)
    providers = ["CPUExecutionProvider"]
    if "CUDAExecutionProvider" in ort.get_available_providers():
        providers.insert(0, "CUDAExecutionProvider")
    key = {"schema": CACHE_SCHEMA, "model_sha256": model_sha,
           "validation_fingerprint": data_id, "script_sha256": file_sha(__file__),
           "onnxruntime_version": ort.__version__, "size": rules.TRACK_A_IMAGE_SIZE,
           "requested_providers": providers, "batch": args.batch,
           "ort_threads": args.ort_threads}
    key_id = hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()[:24]
    cache_path = cache_dir / (key_id + ".npz")
    if cache_path.exists():
        with np.load(cache_path, allow_pickle=False) as cached:
            saved = json.loads(str(cached["metadata"].item()))
            if saved["key"] != key or not np.array_equal(cached["true"], true):
                raise ValueError("Cached logits have inconsistent inputs.")
            logits = cached["logits"]
        if logits.shape != (len(rows), len(rules.CITIES)) or not np.isfinite(logits).all():
            raise ValueError("Cached logits have invalid dimensions or values.")
        print(f"{model.parent.name}: reusing cached logits", flush=True)
        return logits, {**key, **saved["info"], "cache_reused": True}
    options = ort.SessionOptions()
    options.intra_op_num_threads = args.ort_threads
    options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(model), sess_options=options, providers=providers)
    print(f"{model.parent.name}: providers {session.get_providers()}", flush=True)
    outputs = []
    started = time.time()

    def prepare(path):
        return rules.grader_input(rules.load_photo(path), rules.TRACK_A_IMAGE_SIZE)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for start in range(0, len(rows), args.batch):
            batch_rows = rows[start:start + args.batch]
            images = np.stack(list(pool.map(prepare, [path for path, _ in batch_rows])))
            values = np.asarray(session.run(["logits"], {"image": images})[0], dtype=np.float32)
            if values.shape != (len(batch_rows), len(rules.CITIES)) or not np.isfinite(values).all():
                raise ValueError("Invalid ONNX output.")
            outputs.append(values)
            done = start + len(batch_rows)
            if done % 512 == 0 or done == len(rows):
                print(f"  {done}/{len(rows)} validation photos ({time.time() - started:.0f}s)", flush=True)
    logits = np.concatenate(outputs)
    cache_dir.mkdir(parents=True, exist_ok=True)
    info = {"inference_seconds": round(time.time() - started, 2), "providers": session.get_providers()}
    np.savez_compressed(cache_path, logits=logits, true=true,
                        metadata=json.dumps({"key": key, "info": info}, sort_keys=True))
    return logits, {**key, **info, "cache_reused": False}


def tau_name(tau):
    return "tau" + format(tau, "g").replace(".", "p")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", default=["results/baseline_seed0/model.onnx", "results/baseline_seed1/model.onnx"])
    parser.add_argument("--taus", nargs="+", type=float, default=[0, 0.5, 1.0])
    parser.add_argument("--tag", default="prior_adjust_baseline_v1")
    parser.add_argument("--bins", type=int, default=15)
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--ort-threads", type=int, default=2)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        return
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", args.tag):
        parser.error("Use a short lowercase tag containing letters, numbers and underscores.")
    if min(args.bins, args.batch, args.workers, args.ort_threads) < 1:
        parser.error("Bin, batch, worker and thread counts must be positive.")
    if any(not math.isfinite(tau) or tau < 0 for tau in args.taus):
        parser.error("Tau values must be finite and nonnegative.")
    taus = sorted(set([0.0, *args.taus]))
    sys.path.insert(0, str(ROOT / "src"))
    import rules

    cities = list(rules.CITIES)
    models = [(ROOT / name).resolve() for name in args.models]
    if len({model.parent.name for model in models}) != len(models):
        raise ValueError("Each model needs a distinct parent folder.")
    for model in models:
        if not model.is_file() or not model.with_name("result.json").is_file():
            raise SystemExit(f"Missing saved baseline model or result: {model}. It should remain in your Colab Drive; no retraining is started automatically.")
    data = ROOT / "data/starter"
    selection = ROOT / "track_a/selection.csv"
    counts = selection_counts(selection, data / "train", cities)
    prior = np.array([counts[city] for city in cities], dtype=np.float64)
    prior /= prior.sum()
    rows = rules.list_photos(data / "val")
    if len(rows) != 12077:
        raise ValueError(f"Expected all 12,077 validation photos, found {len(rows)}.")
    true = np.array([cities.index(city) for _, city in rows], dtype=np.int64)
    val_counts = Counter(city for _, city in rows)
    out = ROOT / "results" / args.tag
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "class_counts.csv", [{"city": city, "selected_training_photos": counts[city],
                                         "training_prior": float(prior[i]), "validation_photos": val_counts[city]}
                                        for i, city in enumerate(cities)])
    write_csv(out / "validation_index.csv", [{"index": i, "path": path.relative_to(data).as_posix(), "true_city": city}
                                            for i, (path, city) in enumerate(rows)])
    data_id = validation_fingerprint(rows, data / "val", ROOT / "src/rules.py")
    report = {
        "status": "running", "kind": "post_hoc_diagnostic_not_a_training_run",
        "tag": args.tag, "cities": cities, "taus": taus,
        "formula": "adjusted_logits = original_logits - tau * log(selected_training_prior)",
        "training_counts": dict(counts), "training_priors": dict(zip(cities, prior.tolist())),
        "validation_counts": dict(val_counts), "validation_photos": len(rows),
        "ece_definition": f"sample-weighted top-label ECE, {args.bins} equal-width confidence bins; confidence 1 included in final bin",
        "macro_recall_definition": "unweighted mean of five city recalls, matching the official score",
        "confusion_axes": "rows=true city, columns=predicted city, in cities order",
        "tau_policy": "pre-specified exploratory comparison; no automatic winner, fitted parameter, model export or release",
        "notes": [
            "Tau 0 is recomputed by the same ONNX backend used for every tau.",
            "ONNX float32 predictions can differ slightly from the training script's CUDA mixed-precision validation.",
            "Mean confidence on current errors changes its sample population; fixed-baseline-error metrics and error transitions are also provided.",
            "ECE uses the actual validation class mixture; macro recall gives every city equal weight.",
            "Validation is a development set, not an independent test of a tau chosen using these results.",
        ],
        "python": platform.python_version(), "numpy": np.__version__,
        "script_sha256": file_sha(__file__), "validation_fingerprint": data_id,
        "models": [],
    }
    summary = []
    recipe_sha = canonical_sha(ROOT / "track_a/recipe.py")[:12]
    selection_sha = canonical_sha(selection)[:12]
    print("Training selection counts and priors:", flush=True)
    for i, city in enumerate(cities):
        print(f"  {city:8s} {counts[city]:6d}  prior={prior[i]:.6f}", flush=True)
    for model in models:
        metadata = json.loads(model.with_name("result.json").read_text(encoding="utf-8"))
        if (metadata["tag"] != "baseline" or not metadata["official_budget"]
                or metadata["recipe_sha"] != recipe_sha or metadata["selection_sha"] != selection_sha
                or metadata["selection_counts"] != dict(counts)):
            raise ValueError("Saved model metadata does not match the unchanged baseline inputs.")
        logits, cache = infer_or_cache(model, rows, true, data_id, ROOT / "results/logit_cache", args)
        baseline_pred = logits.argmax(axis=1)
        model_report = {"model": model.parent.name, "seed": metadata["seed"], "training_metadata": metadata,
                        "inference": cache, "evaluations": []}
        predictions = {}
        reference = None
        for tau in taus:
            measurement, pred, confidence = metrics(adjust_logits(logits, prior, tau), true, cities, args.bins, baseline_pred)
            if tau == 0:
                reference = measurement
                difference = abs(measurement["macro_recall"] - metadata["val_score"])
                model_report["tau0_delta_from_training_score"] = float(measurement["macro_recall"] - metadata["val_score"])
                if difference > 0.005:
                    raise ValueError("ONNX baseline differs from its recorded training score by over 0.5 percentage points. Check model, data and preprocessing.")
            measurement["tau"] = tau
            measurement["delta_macro_recall_vs_tau0"] = measurement["macro_recall"] - reference["macro_recall"]
            measurement["delta_ece_vs_tau0"] = measurement["ece"] - reference["ece"]
            model_report["evaluations"].append(measurement)
            predictions[tau] = (pred, confidence)
            prefix = model.parent.name + "_" + tau_name(tau)
            write_csv(out / (prefix + "_confusion.csv"),
                      [{"true_city": city, **{other: measurement["confusion"][i][j] for j, other in enumerate(cities)}}
                       for i, city in enumerate(cities)])
            write_csv(out / (prefix + "_confidence_bins.csv"), measurement["calibration_bins"])
            row = {"model": model.parent.name, "seed": metadata["seed"], "tau": tau,
                   "macro_recall": measurement["macro_recall"], "accuracy": measurement["accuracy"],
                   "ece": measurement["ece"], "wrong_count": measurement["wrong_count"],
                   "mean_confidence_on_current_errors": measurement["mean_confidence_on_current_errors"],
                   "mean_confidence_on_fixed_baseline_errors": measurement["mean_confidence_on_fixed_baseline_errors"],
                   "mean_true_class_probability_on_fixed_baseline_errors": measurement["mean_true_class_probability_on_fixed_baseline_errors"],
                   "delta_macro_recall_vs_tau0": measurement["delta_macro_recall_vs_tau0"],
                   "delta_ece_vs_tau0": measurement["delta_ece_vs_tau0"],
                   **measurement["error_transitions"]}
            row.update({city + "_recall": measurement["per_city_recall"][city] for city in cities})
            for pair, values in measurement["pair_errors"].items():
                row[pair + "_count"] = values["count"]
                row[pair + "_rate"] = values["rate_among_true_source_city"]
            summary.append(row)
            print(f"{model.parent.name} tau={tau:g}  macro_recall={measurement['macro_recall']:.6f}  "
                  f"accuracy={measurement['accuracy']:.6f}  ECE={measurement['ece']:.6f}  "
                  f"corrected={measurement['error_transitions']['corrected_baseline_errors']}  "
                  f"new_errors={measurement['error_transitions']['new_errors_on_baseline_correct']}", flush=True)
        prediction_rows = []
        for i, (path, city) in enumerate(rows):
            row = {"path": path.relative_to(data).as_posix(), "true_city": city}
            for tau in taus:
                pred, confidence = predictions[tau]
                row[tau_name(tau) + "_prediction"] = cities[int(pred[i])]
                row[tau_name(tau) + "_confidence"] = format(float(confidence[i]), ".8f")
                row[tau_name(tau) + "_correct"] = bool(pred[i] == true[i])
            prediction_rows.append(row)
        write_csv(out / (model.parent.name + "_predictions.csv"), prediction_rows)
        report["models"].append(model_report)
        write_json(out / "report.json", report)
        write_csv(out / "metrics.csv", summary)
    report["status"] = "complete"
    report["finished_kst"] = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
    report["mean_across_models"] = [
        {"tau": tau, "macro_recall": float(np.mean([row["macro_recall"] for row in summary if row["tau"] == tau])),
         "ece": float(np.mean([row["ece"] for row in summary if row["tau"] == tau]))}
        for tau in taus]
    write_json(out / "report.json", report)
    print(f"Complete: {len(models)} models x {len(taus)} tau values; no retraining. Results: {out}", flush=True)


if __name__ == "__main__":
    main()
