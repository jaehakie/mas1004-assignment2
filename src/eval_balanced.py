"""Evaluate the balanced seed-0 model at tau 0 against matched baseline seed 0.

Run on Colab: uses photos and the saved model there. No post-hoc adjustment
is applied to the balanced model. Reuses the original baseline numeric cache.
"""
import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

import eval_logit_adjustment as evaluation
from sweep_cached_logits import load_verified_cache, flat_row

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--ort-threads", type=int, default=2)
    args = parser.parse_args()
    if min(args.batch, args.workers, args.ort_threads) < 1:
        parser.error("Batch, workers and threads must be positive.")
    evaluation.self_test()
    import rules
    original, index, true, cached = load_verified_cache(
        ROOT / "results/prior_adjust_baseline_v1", ROOT / "results/logit_cache")
    if original["cities"] != list(rules.CITIES):
        raise ValueError("City order changed.")
    baseline, old_logits, _, _ = next(item for item in cached if item[0]["seed"] == 0)
    rows = rules.list_photos(ROOT / "data/starter/val")
    current = [{"path": path.relative_to(ROOT / "data/starter").as_posix(), "true_city": city}
               for path, city in rows]
    if current != [{"path": row["path"], "true_city": row["true_city"]} for row in index]:
        raise ValueError("Validation photo order differs from the baseline cache.")
    data_id = evaluation.validation_fingerprint(rows, ROOT / "data/starter/val", ROOT / "src/rules.py")
    if data_id != original["validation_fingerprint"]:
        raise ValueError("Validation photo metadata changed since the baseline diagnostic.")
    model = ROOT / "results/balanced_seed0/model.onnx"
    metadata = json.loads(model.with_name("result.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "results/balanced_sampling_seed0/sampling_audit.json").read_text(encoding="utf-8"))
    counts = evaluation.selection_counts(ROOT / "track_a/selection.csv", ROOT / "data/starter/train", rules.CITIES)
    if (metadata["tag"] != "balanced" or metadata["seed"] != 0 or not metadata["official_budget"]
            or metadata["recipe_sha"] != evaluation.canonical_sha(ROOT / "track_a/recipe.py")[:12]
            or metadata["selection_sha"] != evaluation.canonical_sha(ROOT / "track_a/selection.csv")[:12]
            or metadata["selection_counts"] != dict(counts) or dict(counts) != original["training_counts"]
            or audit["recipe_sha"] != metadata["recipe_sha"] or audit["selection_sha"] != metadata["selection_sha"]
            or audit["seed"] != 0 or audit["draws"] != metadata["budget"]):
        raise ValueError("Balanced model, sampler audit and current inputs do not agree.")
    logits, inference = evaluation.infer_or_cache(model, rows, true, data_id, ROOT / "results/logit_cache", args)
    value, pred, confidence = evaluation.metrics(logits, true, rules.CITIES, 15, old_logits.argmax(axis=1))
    if abs(value["macro_recall"] - metadata["val_score"]) > 0.005:
        raise ValueError("ONNX score differs from training validation by more than 0.5 percentage points.")
    reference = next(item for item in baseline["evaluations"] if item["tau"] == 0)
    adjusted_reference = next(item for item in baseline["evaluations"] if item["tau"] == 1)
    value.update({"tau": 0.0,
                  "delta_macro_recall_vs_tau0": value["macro_recall"] - reference["macro_recall"],
                  "delta_ece_vs_tau0": value["ece"] - reference["ece"]})
    record = {"model": "balanced_seed0", "seed": 0, "training_metadata": metadata,
              "inference": inference, "evaluations": [value]}
    report = {
        "status": "complete", "kind": "balanced_sampling_tau0_diagnostic",
        "tag": "balanced_eval_seed0", "cities": list(rules.CITIES), "taus": [0.0],
        "validation_photos": len(rows), "validation_fingerprint": data_id,
        "script_sha256": evaluation.canonical_sha(__file__), "models": [record],
        "sampling_audit": audit, "matched_baseline_seed0": reference,
        "matched_baseline_seed0_tau1_provisional": adjusted_reference,
        "delta_macro_vs_baseline_seed0_tau1": value["macro_recall"] - adjusted_reference["macro_recall"],
        "ece_definition": original["ece_definition"],
        "error_transition_reference": "baseline seed 0 at tau 0 on the same ONNX backend",
        "notes": ["No logit adjustment is applied to the balanced model.",
                  "One new training seed only; compare against seed 0, not a two-seed baseline mean.",
                  "A gain alone does not identify whether representations or decision boundaries changed.",
                  "Validation is a development set; no leaderboard or final-test tuning."],
        "finished_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"),
    }
    out = ROOT / "results/balanced_eval_seed0"
    out.mkdir(parents=True, exist_ok=True)
    evaluation.write_json(out / "report.json", report)
    evaluation.write_csv(out / "metrics.csv", [flat_row(record, 0.0, value)])
    evaluation.write_csv(out / "validation_index.csv", index)
    evaluation.write_csv(out / "predictions.csv", [
        {"path": row["path"], "true_city": row["true_city"],
         "prediction": rules.CITIES[int(pred[i])], "confidence": format(float(confidence[i]), ".8f"),
         "baseline_tau0_prediction": rules.CITIES[int(old_logits[i].argmax())]}
        for i, row in enumerate(index)])
    evaluation.write_csv(out / "confusion.csv", [
        {"true_city": city, **dict(zip(rules.CITIES, value["confusion"][i]))}
        for i, city in enumerate(rules.CITIES)])
    evaluation.write_csv(out / "confidence_bins.csv", value["calibration_bins"])
    import curate
    for number, city in enumerate(rules.CITIES):
        wrong = np.flatnonzero((true == number) & (pred != true))
        chosen = wrong[np.argsort(-confidence[wrong], kind="stable")[:48]]
        curate.draw_sheets("mistakes_balanced_seed0_" + city,
                           [(rows[i][0], f"-> {rules.CITIES[int(pred[i])]} {confidence[i]:.2f}") for i in chosen])
    print(json.dumps({"balanced_tau0_macro_recall": value["macro_recall"],
                      "baseline_seed0_tau0_macro_recall": reference["macro_recall"],
                      "baseline_seed0_tau1_macro_recall": adjusted_reference["macro_recall"],
                      "accuracy": value["accuracy"], "ece": value["ece"],
                      "per_city_recall": value["per_city_recall"],
                      "error_transitions_vs_baseline_seed0_tau0": value["error_transitions"]}, indent=2), flush=True)
    print("Complete: balanced model at tau 0; five mistake sheets reused these logits.", flush=True)


if __name__ == "__main__":
    main()
