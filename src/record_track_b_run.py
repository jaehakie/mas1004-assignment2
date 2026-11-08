"""Record the default Track B run and checked submission, without rerunning it."""
import argparse
import csv
import hashlib
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", choices=["b_baseline"], default="b_baseline")
    args = parser.parse_args()
    out = ROOT / "results" / args.tag
    model = ROOT / "submission/model.onnx"
    metadata_path = ROOT / "submission/submission.json"
    info = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected = {"image_size": 224, "starting_weights": "torchvision resnet18 IMAGENET1K_V1",
                "data": "data/starter/train", "summary": "resnet18 at 224, 4 epochs"}
    if info != expected or info != json.loads((out / "submission.json").read_text(encoding="utf-8")):
        raise ValueError("Submission metadata does not match the requested default run.")
    if digest(model) != digest(out / "model.onnx"):
        raise ValueError("Submitted model differs from the completed training export.")
    log_path = Path(os.environ.get("MAS1004_EXPERIMENTS", ROOT / "experiments.csv"))
    with log_path.open(newline="", encoding="utf-8-sig") as stream:
        rows = [row for row in csv.DictReader(stream) if row["track"] == "B" and row["tag"] == args.tag]
    if len(rows) != 1 or rows[0]["device"] != "cuda" or int(rows[0]["budget"]) != 176896:
        raise ValueError("Expected exactly one completed default CUDA training run.")
    checks = sorted((ROOT / "results/colab_logs").glob("*_check_submission.txt"))
    if not checks:
        raise ValueError("Official format-check log is missing.")
    check = checks[-1]
    check_text = check.read_text(encoding="utf-8")
    if ("format and limits: OK" not in check_text or "NOT ACCEPTED" in check_text
            or "Traceback" in check_text):
        raise ValueError("Official format check did not complete successfully.")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            check=True, capture_output=True, text=True).stdout.strip()
    if rows[0]["commit"] != commit or "# commit " + commit not in check_text:
        raise ValueError("Training and format check do not match the current code revision.")
    result = {"status": "complete", "tag": args.tag, "track": "B", "training_row": rows[0],
              "submission": info, "format_check_completed": True,
              "format_check_log": check.relative_to(ROOT).as_posix(),
              "assets": {path.name: {"sha256": digest(path), "bytes": path.stat().st_size}
                         for path in (model, metadata_path)},
              "train_b_script_sha256": digest(ROOT / "src/train_b.py"),
              "commit": commit,
              "finished_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"),
              "note": "Default unseeded starter Track B run; training-script validation only. No post-hoc adjustment or balanced sampling."}
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    print("Default Track B model and checked submission recorded: OK", flush=True)


if __name__ == "__main__":
    main()
