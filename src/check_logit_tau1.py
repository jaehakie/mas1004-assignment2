"""Colab preflight for a baseline recipe with tau=1 folded into its final bias."""
import ast
import csv
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import torch

import eval_logit_adjustment as evaluation
import official
import rules

ROOT = Path(__file__).resolve().parents[1]


def hook_fingerprint(node):
    """Hash syntax consistently across Python 3.11 and 3.12+ AST schemas."""
    def normalize(value):
        if isinstance(value, ast.AST):
            return [type(value).__name__, [[key, normalize(item)]
                    for key, item in ast.iter_fields(value)
                    if not (key == "type_params" and item == [])]]
        if isinstance(value, list):
            return [normalize(item) for item in value]
        return value
    data = json.dumps(normalize(node), ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def main():
    if not torch.cuda.is_available():
        raise SystemExit("Choose Runtime > Change runtime type > T4 GPU, then Run all. No CPU training is started.")
    path = ROOT / "track_a/recipe.py"
    problems = official.recipe_problems(path)
    if problems:
        raise ValueError(problems)
    spec = importlib.util.spec_from_file_location("logit_tau1_recipe_check", path)
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    baseline_evidence = json.loads((ROOT / "checks/logit_tau1_preparation.json").read_text())
    if evaluation.canonical_sha(path) != baseline_evidence["candidate_recipe_sha256"]:
        raise ValueError("Recipe differs from the reviewed candidate.")
    if evaluation.canonical_sha(ROOT / "track_a/selection.csv") != baseline_evidence["selection_sha256"]:
        raise ValueError("Selection changed after the candidate was prepared.")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name != "final_model":
            digest = hook_fingerprint(node)
            if digest != baseline_evidence["baseline_training_hook_ast_sha256"][node.name]:
                raise ValueError("Baseline training hook changed: " + node.name)
    with (ROOT / "track_a/selection.csv").open(newline="", encoding="utf-8-sig") as stream:
        paths = [row["path"] for row in csv.DictReader(stream)]
    cities = [path.split("/")[0] for path in paths]
    counts = Counter(cities)
    if tuple(counts[city] for city in rules.CITIES) != recipe.TRAINING_COUNTS:
        raise ValueError("Recipe counts or city order differ from the submitted selection.")
    if recipe.sample_weights(cities, paths) is not None or recipe.LOGIT_TAU != 1.0:
        raise ValueError("This candidate requires baseline sampling and tau=1.")

    # Exercise the actual recipe final_model on a small real torch classifier.
    # official.py --quick separately checks the full ResNet18 architecture/export.
    torch.manual_seed(705)
    head = torch.nn.Linear(11, 5)
    features = torch.randn(31, 11)
    model = SimpleNamespace(fc=head)
    weight_before, bias_before = head.weight.detach().clone(), head.bias.detach().clone()
    with torch.no_grad():
        before = head(features).clone()
    returned = recipe.final_model(model)
    with torch.no_grad():
        after = head(features)
    prior = torch.tensor(recipe.TRAINING_COUNTS, dtype=head.bias.dtype)
    prior /= prior.sum()
    expected = before - recipe.LOGIT_TAU * prior.log()
    gap = float((after - expected).abs().max())
    if returned is not model or not torch.equal(head.weight, weight_before) or gap > 2e-6:
        raise ValueError("Folding the adjustment into the existing bias failed.")
    if not torch.allclose(head.bias, bias_before - prior.log(), rtol=0, atol=2e-7):
        raise ValueError("Classifier bias does not implement the selected adjustment.")

    result = {
        "status": "complete", "kind": "logit_tau1_recipe_preflight_not_training",
        "recipe_sha256": evaluation.canonical_sha(path),
        "selection_sha256": evaluation.canonical_sha(ROOT / "track_a/selection.csv"),
        "cities": list(rules.CITIES), "training_counts": dict(counts),
        "tau": recipe.LOGIT_TAU, "sampling": "unchanged baseline permutation",
        "baseline_training_hooks_identical": True,
        "real_torch_head_equivalence_max_gap": gap,
        "classifier_weight_unchanged": True,
        "formula": "final fc.bias -= tau * log(selected training prior)",
        "commit": official.git_commit(),
        "next_required_check": "official.py --quick on the same recipe before Release",
    }
    out = ROOT / "results/logit_tau1_preflight"
    out.mkdir(parents=True, exist_ok=True)
    evaluation.write_json(out / "report.json", result)
    print(json.dumps(result, indent=2), flush=True)
    print("Tau-1 recipe preflight: OK. Run the official quick check next.", flush=True)


if __name__ == "__main__":
    main()
