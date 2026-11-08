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

## 2026-11-08 Training photo observations: Busan
- Sheet viewed: `results/curate/look_busan_00.png` (26 photos, every 200th selected training photo).
- Student's observation, verbatim:

> 이 이미지들은 간판의 한글 표기, 해운대 해수욕장 같은 해변과 고층 아파트 군집, 산비탈에 빼곡한 주택가, ‘G-STAR’ 행사장, 부산행 안내가 적힌 화면 등으로 볼 때 부산으로 보여. 바다와 가파른 산지가 맞닿아 있어서 해안 절경, 항구 풍경, 비탈진 주거지가 자주 나오고, 해변 바로 뒤로 초고층 주상복합이 솟아 있는 스카이라인이 가장 눈에 띄는 구분 단서인 거 같아.
>
> 다만 모든 사진이 부산이라고 단정하기는 어려운데, 간판이 있는 거리, 전통 한옥 건물, 지하철·경전철 같은 교통 시설, 한국어 시위 피켓과 방역 브리핑 화면 등 한국 도시 어디서든 볼 법한 장면도 섞여 있어서, 도시를 가르려면 바다·산·고층 해변 아파트 조합이나 ‘G-STAR’ 같은 지역 행사 문구를 우선 봐야 할 거 같아.
