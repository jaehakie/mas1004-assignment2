"""List all starter training photos, respecting any explicitly dropped photos."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    train = ROOT / "data/starter/train"
    cities = ("seoul", "busan", "tokyo", "osaka", "taipei")
    paths = sorted(p.relative_to(train).as_posix()
                   for city in cities for p in (train / city).glob("*.jpg"))
    if not paths:
        raise SystemExit("Starter photos are missing; run src/get_data.py first.")
    dropped_file = ROOT / "track_a/dropped.csv"
    dropped = set()
    if dropped_file.exists():
        with dropped_file.open(newline="", encoding="utf-8-sig") as f:
            dropped = {r["path"] for r in csv.DictReader(f)}
    paths = [p for p in paths if p not in dropped]
    target = ROOT / "track_a/selection.csv"
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path"])
        writer.writerows([p] for p in paths)
    print(f"Wrote {len(paths)} training paths to track_a/selection.csv; {len(dropped)} explicit exclusions.")
    return target


if __name__ == "__main__":
    main()
