"""Sweep fixed tau values using exported numeric logits only; no inference."""
import argparse
import copy
import csv
import hashlib
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

import eval_logit_adjustment as evaluation

ROOT = Path(__file__).resolve().parents[1]


def load_verified_cache(source, cache_dir):
    report = json.loads((source / "report.json").read_text(encoding="utf-8"))
    if report["status"] != "complete" or report["kind"] != "post_hoc_diagnostic_not_a_training_run":
        raise ValueError("A completed source diagnostic is required.")
    expected_sha = evaluation.canonical_sha(ROOT / "src/eval_logit_adjustment.py")
    if report["script_sha256"] != expected_sha:
        raise ValueError("Source diagnostic metrics implementation has changed.")
    with (source / "validation_index.csv").open(newline="", encoding="utf-8") as stream:
        index = list(csv.DictReader(stream))
    cities = report["cities"]
    true = np.array([cities.index(row["true_city"]) for row in index], dtype=np.int64)
    if len(index) != report["validation_photos"]:
        raise ValueError("Source validation index is incomplete.")
    found = []
    for model in report["models"]:
        matches = []
        for path in sorted(cache_dir.glob("*.npz")):
            with np.load(path, allow_pickle=False) as cached:
                metadata = json.loads(str(cached["metadata"].item()))
                if metadata["key"]["model_sha256"] != model["inference"]["model_sha256"]:
                    continue
                if any(metadata["key"].get(key) != model["inference"].get(key) for key in metadata["key"]):
                    continue
                if not np.array_equal(cached["true"], true):
                    raise ValueError("Cached labels differ from the verified source index.")
                logits = cached["logits"].copy()
            if logits.shape != (len(index), len(cities)) or not np.isfinite(logits).all():
                raise ValueError("Invalid cached logits.")
            matches.append((path, logits, metadata))
        if not matches:
            raise FileNotFoundError("Verified numeric cache is missing for " + model["model"] + "; no inference or retraining is started.")
        path, logits, metadata = matches[0]
        found.append((model, logits, path, metadata))
    return report, index, true, found


def flat_row(model, tau, value):
    row = {"model": model["model"], "seed": model["seed"], "tau": tau}
    for key in ("macro_recall", "accuracy", "ece", "wrong_count",
                "mean_confidence_on_current_errors", "mean_confidence_on_fixed_baseline_errors",
                "mean_true_class_probability_on_fixed_baseline_errors",
                "delta_macro_recall_vs_tau0", "delta_ece_vs_tau0"):
        row[key] = value[key]
    row.update(value["error_transitions"])
    row.update({city + "_recall": score for city, score in value["per_city_recall"].items()})
    for pair, item in value["pair_errors"].items():
        row[pair + "_count"] = item["count"]
        row[pair + "_rate"] = item["rate_among_true_source_city"]
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="results/prior_adjust_baseline_v1")
    parser.add_argument("--cache-dir", default="results/logit_cache")
    parser.add_argument("--taus", type=float, nargs="+", default=[0, 0.5, 0.75, 1, 1.25, 1.5, 2])
    parser.add_argument("--tag", default="prior_adjust_baseline_v2")
    args = parser.parse_args()
    if not evaluation.re.fullmatch(r"[a-z][a-z0-9_]{0,63}", args.tag):
        parser.error("Invalid output tag.")
    if any(not np.isfinite(tau) or tau < 0 for tau in args.taus):
        parser.error("Tau must be finite and nonnegative.")
    taus = sorted(set([0.0, *args.taus]))
    evaluation.self_test()
    source = ROOT / args.source
    original, index, true, models = load_verified_cache(source, ROOT / args.cache_dir)
    prior = np.array([original["training_priors"][city] for city in original["cities"]])
    out = ROOT / "results" / args.tag
    out.mkdir(parents=True, exist_ok=True)
    for name in ("class_counts.csv", "validation_index.csv"):
        shutil.copyfile(source / name, out / name)
    report = copy.deepcopy(original)
    report.update({"tag": args.tag, "taus": taus, "status": "running", "models": [],
                   "evaluation_script": "src/sweep_cached_logits.py",
                   "script_sha256": evaluation.canonical_sha(__file__),
                   "source_report_sha256": evaluation.file_sha(source / "report.json"),
                   "execution": "numeric cache arithmetic only; no model, image or dataset loading"})
    report.pop("mean_across_models", None)
    report.pop("finished_kst", None)
    report["tau_policy"] = "User-requested expanded validation sweep; no automatic deployment choice."
    summary = []
    for original_model, logits, cache_path, cache_metadata in models:
        model = {key: copy.deepcopy(value) for key, value in original_model.items() if key != "evaluations"}
        model["evaluations"] = []
        model["cache_source"] = cache_path.name
        model["inference"] = {**cache_metadata["key"], **cache_metadata["info"], "cache_reused": True}
        baseline_pred = logits.argmax(axis=1)
        reference, predictions = None, {}
        for tau in taus:
            value, pred, confidence = evaluation.metrics(evaluation.adjust_logits(logits, prior, tau), true,
                                                         report["cities"], 15, baseline_pred)
            if tau == 0:
                reference = value
            value.update({"tau": tau, "delta_macro_recall_vs_tau0": value["macro_recall"] - reference["macro_recall"],
                          "delta_ece_vs_tau0": value["ece"] - reference["ece"]})
            previous = next((item for item in original_model["evaluations"] if item["tau"] == tau), None)
            if previous is not None:
                for key in ("macro_recall", "accuracy", "ece"):
                    if not np.isclose(value[key], previous[key], rtol=0, atol=1e-10):
                        raise ValueError("Recomputed cached metric differs from the verified source report.")
            model["evaluations"].append(value)
            predictions[tau] = (pred, confidence)
            summary.append(flat_row(model, tau, value))
            prefix = model["model"] + "_" + evaluation.tau_name(tau)
            evaluation.write_csv(out / (prefix + "_confusion.csv"),
                                 [{"true_city": city, **dict(zip(report["cities"], value["confusion"][i]))}
                                  for i, city in enumerate(report["cities"])])
            evaluation.write_csv(out / (prefix + "_confidence_bins.csv"), value["calibration_bins"])
            print(f"{model['model']} tau={tau:g} macro={value['macro_recall']:.6f} "
                  f"accuracy={value['accuracy']:.6f} ECE={value['ece']:.6f}", flush=True)
        predicted_rows = []
        for i, indexed in enumerate(index):
            row = {"path": indexed["path"], "true_city": indexed["true_city"]}
            for tau, (pred, confidence) in predictions.items():
                name = evaluation.tau_name(tau)
                row[name + "_prediction"] = report["cities"][int(pred[i])]
                row[name + "_confidence"] = format(float(confidence[i]), ".8f")
                row[name + "_correct"] = bool(pred[i] == true[i])
            predicted_rows.append(row)
        evaluation.write_csv(out / (model["model"] + "_predictions.csv"), predicted_rows)
        report["models"].append(model)
    report["status"] = "complete"
    report["finished_kst"] = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
    report["mean_across_models"] = [
        {"tau": tau, **{key: float(np.mean([row[key] for row in summary if row["tau"] == tau]))
                       for key in ("macro_recall", "accuracy", "ece")}}
        for tau in taus]
    evaluation.write_json(out / "report.json", report)
    evaluation.write_csv(out / "metrics.csv", summary)
    print(json.dumps(report["mean_across_models"], indent=2), flush=True)
    print("Complete: numeric cached-logit sweep only; no model inference or training.", flush=True)


if __name__ == "__main__":
    main()
