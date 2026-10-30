"""Prepare the unchanged starter selection and include it in the Colab download."""
import hashlib
import json
import runpy
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    module = runpy.run_path(str(ROOT / "scripts/make_selection.py"))
    selection = module["main"]()
    out = ROOT / "results/midpoint"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(selection, out / "selection.csv")
    recipe = ROOT / "track_a/recipe.py"
    manifest = {
        "recipe_sha256": hashlib.sha256(recipe.read_bytes()).hexdigest(),
        "selection_sha256": hashlib.sha256(selection.read_bytes()).hexdigest(),
        "selection_rows": len(selection.read_text(encoding="utf-8").splitlines()) - 1,
    }
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
