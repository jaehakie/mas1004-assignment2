"""Check the requested balanced sampler on Colab before any training starts."""
import argparse
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

import official
import rules

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if not official.torch.cuda.is_available():
        raise SystemExit("A Colab GPU is required. Choose Runtime > Change runtime type > T4 GPU, then Run all. No CPU training is started.")
    recipe_path = ROOT / "track_a/recipe.py"
    problems = official.recipe_problems(recipe_path)
    if problems:
        raise ValueError(problems)
    spec = importlib.util.spec_from_file_location("balanced_recipe_audit", recipe_path)
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    rows, _ = official.read_selection(ROOT / "data/starter", ROOT / "track_a")
    cities = [city for _, city in rows]
    counts = Counter(cities)
    weights = recipe.sample_weights(cities, [path for path, _ in rows])
    if weights is None or len(weights) != len(rows):
        raise ValueError("Balanced weights are missing or have the wrong length.")
    if any(not math.isfinite(value) or value <= 0 for value in weights):
        raise ValueError("Sampler weights must be positive and finite.")
    mass = {city: math.fsum(w for w, label in zip(weights, cities) if label == city)
            for city in rules.CITIES}
    total = math.fsum(weights)
    probability = {city: value / total for city, value in mass.items()}
    if any(not math.isclose(value, 0.2, abs_tol=1e-12) for value in probability.values()):
        raise ValueError("Each city must have 20% expected drawing probability.")
    draws = (rules.TRACK_A_BUDGET // recipe.BATCH_SIZE) * recipe.BATCH_SIZE
    order = official.draw_order(len(rows), draws, weights, args.seed)
    realized = Counter(cities[i] for i in order)
    evidence = {
        "tag": "balanced", "seed": args.seed, "selection_counts": dict(counts),
        "recipe_sha": official.file_hash(recipe_path),
        "selection_sha": official.file_hash(ROOT / "track_a/selection.csv"),
        "sampling": "inverse city frequency; weighted draws with replacement",
        "expected_city_probability": probability, "realized_city_draws": dict(realized),
        "draws": draws, "batch_size": recipe.BATCH_SIZE,
        "post_hoc_tau": 0, "commit": official.git_commit(),
    }
    out = ROOT / "results/balanced_sampling_seed0"
    out.mkdir(parents=True, exist_ok=True)
    (out / "sampling_audit.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2), flush=True)
    print("Balanced sampler audit: OK. Actual random counts need not be exactly equal.", flush=True)


if __name__ == "__main__":
    main()
