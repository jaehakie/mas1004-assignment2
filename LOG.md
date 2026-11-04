# Log

One entry for each recipe, selection or Track B model you train, newest at
the bottom. The numbers come from `experiments.csv`. "Why" and "what it means"
are in your own words: your agent asks you for them and does not make them up.
End the log with your plan for what to try next.

<!-- The form of an entry:

## <date> <tag> (Track A or B)
- changed: what is different from the run before
- why: your reason
- validation: 0.000 (before: 0.000)
- what it means: what you think the result says
-->

## 2026-10-30 Midpoint setup: unchanged starter recipe (Track A)
- Requested task: submit the unchanged starter recipe for the midpoint check.
- Recipe: unchanged from the supplied template.
- Selection: all 44,257 starter training photos, each listed once; no exclusions.
- Verification: `python src/official.py --quick` completed on Colab with seed 0,
  20 steps, batch size 64, and validation score 0.306.
- The quick run estimated 48 minutes for a full run on that Colab session.
- Evidence: `checks/midpoint_quick.json`; original output is kept locally in
  `results/colab_logs/1030_212920_official.txt`.
- This is a setup check, not a full baseline experiment; no full training was run.

## 2026-11-04 Local First setup verification
- Requested task: complete First setup in the existing working folder.
- Installed the versions in uv.lock with uv; Python 3.12.15,
  torch 2.6.0, torchvision 0.21.0.
- The official downloader verified and unpacked 44,257 training
  photos and 12,077 validation photos locally.
- The unchanged starter recipe completed 20 steps on CPU, seed 0,
  with validation score 0.2875.
- The quick check estimated 320 minutes for a full run on this computer.
- Evidence: checks/setup_local_20261104.json. Original output remains in
  results/setup/quick-20261104.log. This is a setup check, not a full baseline run.
- The existing Track A release is present in the leaderboard updated
  2026-11-04 00:41 KST: score 0.3958, grader validation mean 0.4917666666666667.
  Evidence: checks/leaderboard_20261104.json.
