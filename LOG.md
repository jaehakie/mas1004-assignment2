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

## 2026-11-08 Training photo observations: Seoul
- Sheets viewed: `results/curate/look_seoul_00.png` and `results/curate/look_seoul_01.png` (57 photos, every 200th selected training photo).
- Student's observation, verbatim:

> 서울 사진에서는 도시 한가운데를 가로지르는 한강과 그 위의 다리, 강변 자전거 대여소, 강 건너 고층 아파트와 빌딩이 가장 뚜렷한 단서인 거 같아. 남산타워가 보이는 장면, 산 위에서 내려다본 빽빽한 시가지, 도심 속 궁궐·한옥 담장, 박물관의 금관이나 '서울 올림픽 1988' 메달 같은 수도 특유의 문화·역사 요소도 있어. 초록색 시내버스, 명동 같은 번화가, 좁은 골목 사이로 간판이 겹겹이 붙은 상권도 많이 보여. 부산이 바다·항구·가파른 산비탈 주거지로 구분된다면, 서울은 강과 내륙의 완만한 산, 평평하고 촘촘한 도심으로 구분되는 거 같아. 외교 기자회견처럼 정부 기관이 연상되는 장면도 서울 쪽에 가깝고.
>
> 판단하기 어려운 장면도 꽤 많긴 한데, 김밥·떡볶이·설렁탕 같은 음식 사진, 자동차 휠이나 건물 외벽 클로즈업, 사무실·강의실·회의실 내부, 횡단보도가 있는 평범한 주택가나 상가 거리는 어느 한국 도시에서도 비슷하게 나와. 학교 건물, 역 승강장, 공항 탑승교, 공원 잔디밭이나 야간 거리 영상도 간판이나 지형이 안 보이면 서울이라고 단정하기 어려워. 한강, 남산타워, 서울 표기가 들어간 시설 같은 고유한 랜드마크가 보일 때만 확신하고, 나머지는 주변 단서와 함께 봐야 할 거 같아.
