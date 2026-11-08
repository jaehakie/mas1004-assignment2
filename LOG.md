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

## 2026-11-08 Training photo observations: Taipei, Osaka and Tokyo
- Sheets viewed: `results/curate/look_taipei_00.png` (37 photos), `results/curate/look_osaka_00.png` (36 photos), `results/curate/look_tokyo_00.png` and `results/curate/look_tokyo_01.png` (67 photos); every 200th selected training photo.
- Student's observations and comparison, verbatim:

> **타이베이**: 번체자 간판과 안내문이 가장 강한 단서인 거 같아. 여기에 노란 택시와 오토바이 혹은 스쿠터가 가득한 도로, 아열대 느낌의 짙은 녹음과 반얀나무 같은 큰 나무, 야시장 노점의 굴전 먹거리, 타이베이 101, 중정기념당의 광장과 지붕, 노란 어깨띠를 두른 선거 유세 장면이 눈에 띄어. 판단하기 어려운 건 도자기·청동기 같은 박물관 유물, 인물 사진, 음식 접시, 흐릿한 숲이나 자전거도로, 간판이 안 보이는 회색 건물과 베란다 클로즈업이야. 이런 장면은 타이완이라는 근거가 없는 거 같아.
>
> **오사카**: 랜드마크가 분명한 사진이 많아. 성벽과 해자가 있는 오사카성, 금빛 장식이 얹힌 천수각 지붕, 우메다 스카이빌딩, 붉은 아치형 다리가 있는 신사 계단, 'Hack Osaka' 간판, 난카이·한큐·게이한 계열로 보이는 전철, 노면전차, 강과 다리 풍경, 형형색색의 가게 간판과 지붕이 있는 상점가가 그런 거 같아. 판단하기 어려운 건 맥주병, 라멘집 내부, 꽃 클로즈업, 왜가리, 마네킹, 장난감 가게, 전철 차내, 좁은 골목이나 일반 도로야. 일본이라는 건 알 수 있어도 오사카라고 하기는 어려운 거 같아.
>
> **도쿄**: 지하철 긴자역 입구 표지, 도쿄돔, 시부야 스크램블 교차로, 후지산 앞으로 날아가는 비행기, 항구의 컨테이너 크레인, 아키하바라 느낌의 밤거리, 파란 조명 가로수, 메이지신궁 같은 울창한 숲길이 단서라고 생가해. 대로변 고층 오피스 빌딩과 고가 고속도로, 은행나무 가로수길도 자주 보여. 반면 횡단보도, 역 승강장, 자판기, 주택가 골목, 공중전화, 평범한 학교나 사무 건물, 터널, 차량 대시캠 영상은 일본 어디서든 나올 법해서 도쿄라고 단정하기 어려운 거 같아.
>
> **도쿄와 오사카의 차이**는 다음과 같이 정리할 수 있을 거 같아.
>
> - 도쿄 사진은 넓은 도로와 고층 오피스 거리, 대규모 환승역, 공원이 많아 정돈되고 규모가 커. 오사카 사진은 강과 다리, 성, 지붕이 튀는 상점가 간판 등 개성 있고 장식적인 인상이 강해.
> - 오사카에서는 성곽과 해자라는 역사 유적, 강변 풍경이 자주 나오지만, 도쿄에서는 후지산, 항만 크레인, 도쿄돔 같은 대형 시설이 눈에 띄어.
> - 다만 도쿄 사진 상당수가 일반 거리 영상이라, 건물이나 도로 모양만으로는 두 도시를 가르기 어려워서 간판 문구, 노선 표지, 랜드마크가 있을 때만 구분이 가능했던 거 같아.

## 2026-11-08 baseline (Track A): starter recipe, seeds 0 and 1
- Conditions: unchanged starter recipe and all 44,257 selected training photos;
  only the random seed differs between the two runs. Both are full official-budget runs on Colab GPU.
- Training revision: `de14ca6`; recipe SHA `17ac485223fa`, selection SHA `365384496af8`.
- Results, as printed by the training code and recorded in `experiments.csv`:

| Seed | Validation score | Training seconds | Training minutes (rounded) |
| --- | --- | --- | --- |
| 0 | 0.4933 | 2154.5 | 35.9 |
| 1 | 0.5028 | 2073.4 | 34.6 |

- Arithmetic mean of the two recorded scores: 0.49805. Their absolute difference
  is 0.0095 (0.95 percentage points).
- Evidence: `checks/baseline_seed0.json`, `checks/baseline_seed1.json`, and
  `results/colab_logs/1108_150248_official_baseline_seed0.txt` /
  `results/colab_logs/1108_154254_official_baseline_seed1.txt`.
- `curate.py mistakes` completed on all 12,077 validation photos using seed 0.
  It produced one sheet per city, showing that city's 48 most confident wrong predictions.
- Student reviews are recorded below as they are provided.

## 2026-11-08 Baseline mistake observations: Busan
- Sheet viewed: results/curate/mistakes_baseline_seed0_busan_00.png (48 validation photos).
- Student's observations and hypotheses about the model's decisions, verbatim:

> **1. 한국 어디에나 있는 전통 건축과 공공시설이 서울로 예측된 거 같아.** 부산 #1(서울 0.99), #2·#3(서울 0.98), #7(서울 0.95), #17·#30·#31·#48 같은 한옥식 건물, 사찰 문, 성문은 모두 서울로 갔어. 궁궐과 한옥을 서울과 연결 지은 것 같은데, 이런 건물은 전국에 있어. 부산 #5(경찰 파출소), #6(관공서), #9(우체국), #11(소방서), #19(학교), #4와 #41(역사 내부)처럼 전국 공통 디자인의 시설도 서울 0.86\~0.98로 갔어. 한글 간판이 보이면 '한국, 그중에서도 서울'로 고르는 경향이 있는 거 같아. 부산 #12·#18·#23의 우산 쓴 노점 시장, 부산 #40·#47의 한글 네온이 있는 밤거리도 같은 경우야.
>
> **2. 바다와 항만, 고가도로가 있는 풍경은 도쿄로 예측된 거 같아.** 부산 #8(도쿄 0.94), #20·#21(도쿄 0.91), #22(도쿄 0.90), #25(컨테이너 크레인이 보이는 다리, 도쿄 0.90), #26(바닷가 케이블카 철탑, 도쿄 0.90), #32(도쿄 0.89)는 대시캠 고속도로, 항만, 고가 구조물, 아파트 단지가 보이는 장면이야. 읽을 수 있는 한글이 없으면 대형 항구와 고가 도로가 있는 대도시라는 이유로 도쿄로 간 거 같아. 바다와 항만은 부산의 가장 큰 특징인데 오히려 도쿄 근거로 쓰인 셈이야. 비 오거나 흐린 대시캠 장면인 부산 #29(도쿄 0.90)와 #43(도쿄 0.86)도 글자가 안 보여서 같은 방향으로 간 듯해. 부산 #27(암벽 마애불)이 도쿄로 간 것도, 한글 없는 불교 석조물이 일본처럼 보였기 때문일 수 있어.
>
> **3. 지역 단서가 거의 없는 클로즈업, 식당, 무성한 식생은 타이베이로 간 거 같아.** 부산 #15(감자칩 클로즈업, 타이베이 0.91)는 도시 정보가 거의 없어. 부산 #33(울창한 숲 속 석등 계단에 알록달록한 연등, 타이베이 0.88)은 아열대 느낌의 식생과 연등이, 부산 #36(분주한 식당 내부와 빽빽한 메뉴판, 타이베이 0.88)은 야시장 같은 분위기가 이유인 듯해. 이런 장면은 한국이라는 단서마저 약해서 다른 아시아 도시로 빠지기 쉬워.
>
> **종합하면** 모델은 '한글이 읽히는가'를 먼저 보고 읽히면 서울, 안 읽히면 도쿄나 타이베이로 갈랐던 거 같아. 부산 #13(옹벽과 비탈, 뒤쪽 고층 아파트), #34와 #44(바닷가 자전거길), #45(산 쪽으로 이어진 전통 건물) 같은 부산다운 지형 단서도 있었지만 판단에 반영되지 않은 듯해. 확률이 높은 것도 한국다움이라는 큰 단서에 확신을 두고 도시 수준의 단서는 보지 않았기 때문일 수 있어.

## 2026-11-08 Baseline mistake observations: Seoul
- Sheet viewed: results/curate/mistakes_baseline_seed0_seoul_00.png (48 validation photos).
- Student's observations and hypotheses about the model's decisions, verbatim:

> **1. 특징 없는 일반 거리와 대시캠 장면은 도쿄로 갔어.**
>
> - 서울 #8(도쿄 0.93), #10·#11·#12(도쿄 0.92), #15·#16(도쿄 0.90), #29·#37(도쿄 0.85), #48(도쿄 0.82)은 인도, 고층 건물, 마스크를 쓴 보행자, 겨울 거리 같은 평범한 대도시 풍경이야.
> - 서울 #17·#19(도쿄 0.90, 0.89)와 #28(도쿄 0.86)은 어두운 밤 도로 영상이야.
> - 서울 #24·#39(도쿄 0.88, 0.84)는 울타리 옆 녹지 산책로야.
> - 한글이 크게 보이지 않고 서울만의 지형도 없으면 가장 흔한 동아시아 대도시인 도쿄로 가는 경향이 있어 보여.
>
> **2. 지하철역 표지와 승강장은 부산으로 갔어.**
>
> - 서울 #4(신이문역, 부산 0.96), #5(신갈, 부산 0.95), #25(구성역, 부산 0.88)는 한글 역명 표지판이 분명히 보이는 사진이야.
> - 서울 #14·#22·#34(부산 0.91, 0.88, 0.85)도 스크린도어가 있는 승강장이야.
> - 노선 번호나 역 번호가 들어간 표지판은 서울 외 지역에도 비슷하게 있어서, 한국이라는 건 맞췄지만 도시는 부산으로 잘못 고른 거 같아. 서울 #40(파란 시내버스, 부산 0.84)도 지역 구분이 약한 버스 디자인이야.
>
> **3. 지역 단서가 약한 클로즈업과 실내 사진은 타이베이·오사카로 흩어졌어.**
>
> - 서울 #20(망고 디저트, 타이베이 0.89), #46(디저트 접시, 오사카 0.83), #47(전시장의 빨간 SUV, 오사카 0.82), #38(빨간 소형차, 타이베이 0.85)은 도시 정보가 거의 없어.
> - 서울 #1(대시캠 정체 도로, 타이베이 0.99)과 #9(복도에 사람이 모인 장면, 타이베이 0.93)도 마찬가지야. #1은 가장 높은 확신으로 틀렸는데 근거는 안 보여.
>
> **4. 서울다운 단서가 있는데도 놓친 사례가 있어.**
>
> - 서울 #33은 남산타워와 산이 보이는데 타이베이(0.85)로 갔어. 타워가 작게 찍혀서 반영되지 않았을 수 있어.
> - 서울 #18(궁궐 돌담, 도쿄 0.90)과 #43(나무 사이 한옥, 오사카 0.83)도 전통 건축이 일본으로 갔어.
> - 서울 #36(흰옷 입은 사람들이 모인 옛 사진)은 부산 0.85로 갔어.
> - 서울 #35(야경과 다리 불빛, 오사카 0.85)는 한강 야경으로 보이는데 강과 다리 구조가 근거로 쓰이지 않은 듯해.
>
> **5. 공항 사진도 도시 근거가 못 되는 거 같아.**
>
> - 서울 #3(아시아나 여객기, 부산 0.98), #6(여객기, 도쿄 0.95), #44(대한항공 여객기, 도쿄 0.83)는 같은 공항 풍경인데 예측이 갈렸어.
> - 항공사 로고가 한국 항공사인데도 도시로 이어지지 않았어.
>
> **종합하면** 앞서 본 부산 오분류와 거울상이야. 부산 사진은 한글이 읽히면 서울로 갔고, 서울 사진은 한글이 읽혀도 역 표지판이면 부산, 글자가 흐리면 도쿄로 갔어. 모델이 '한국 도시'까지는 어느 정도 좁혀도 서울과 부산을 가르는 도시 수준의 단서는 거의 쓰지 못하는 것 같아. 서울은 평범한 도심 풍경이 많아서 결과적으로 도쿄로 가장 많이 빠진 듯해.

## 2026-11-08 Baseline mistake observations: Tokyo
- Sheet viewed: results/curate/mistakes_baseline_seed0_tokyo_00.png (48 validation photos).
- Student's observations and hypotheses about the model's decisions, verbatim:

> **서울로 간 사진 (28장): 비 오는 날 넓은 가로수 거리와 현대적인 상점가야.**
>
> - 도쿄 #2·#4·#11(서울 0.97, 0.96, 0.94)은 비 내리는 대로변에 우산 쓴 보행자, 유리 외벽 상가, 노란 점자블록이 보여.
> - 도쿄 #17·#25·#32·#37·#39·#40·#41(서울 0.88\~0.93)도 젖은 길에 앙상한 가로수, 우산, 점자블록이 있는 비슷한 장면이야.
> - 이런 장면에서는 일본어 글자가 크게 안 보이면 서울로 가는 경향이 있는 거 같아.
> - 도쿄 #3(캐논 EOS World 전시, 서울 0.96), #7(출근길 인파, 서울 0.96), #33(전시된 차량, 서울 0.89), #47(실내 행사장, 서울 0.88)은 로마자 위주이거나 일본 단서가 약한 장면이야.
>
> **오사카로 간 사진 (17장): 네온 간판이 빽빽한 번화가와 아케이드 상점가야.**
>
> - 도쿄 #1(오사카 0.97)과 #15(0.94)는 붉은 기둥과 천장이 있는 아케이드 상점가야. 오사카 상점가와 닮았는데 실제로는 도쿄야.
> - 도쿄 #16·#18·#19·#26·#30·#31(오사카 0.91\~0.94)은 네온사인과 일본어 간판이 가득한 밤거리(아키하바라 같은 곳)야.
> - 도쿄 #20(붉은 도리이와 신사, 오사카 0.92)과 #12(식당 간판 거리, 오사카 0.94)도 일본 전통 요소가 오사카로 갔어.
> - 도쿄 #24(신칸센, 오사카 0.92)는 철도 설비만 보고 오사카로 간 거 같아.
> - 오사카는 일본이라는 건 맞췄지만 도쿄/오사카를 가르는 단서는 못 쓴 모양이야.
>
> **타이베이로 간 사진 (2장)**
>
> - 도쿄 #9(흐린 거리, 타이베이 0.95)와 #27(한자로 크게 쓴 노란 밴, 타이베이 0.91)이야. 한자 간판이 번체자 문화권과 연결된 듯해.
>
> **부산으로 간 사진 (2장)**
>
> - 도쿄 #8(색이 번진 이미지, 부산 0.96)과 #36(야경 속 다리와 강, 부산 0.90)이야. #8은 화질 문제로 보이고, #36은 강과 다리 야경이 부산 같아 보였을 수 있어.
>
> **눈에 띄는 점**은 도쿄 #14·#38·#42·#43 같은 도쿄 스카이트리가 있는 전경, 도쿄 게이트 브리지, 하늘에서 본 도시 전경도 오사카로 갔다는 거야. 도쿄 고유 랜드마크가 분명한 사진도 놓친 거 같아.

### Mechanical cross-check against the sheet CSV
- Source: results/curate/mistakes_baseline_seed0_tokyo_00.csv.
- Among these 48 displayed photos, prediction counts are Seoul 28, Osaka 16,
  Taipei 2 and Busan 2. These are counts for this sheet, not the full validation set.
- The student's original wording above is preserved. The CSV gives the following
  labels for referenced photo numbers whose labels or probabilities differ:

| Photo number | Prediction in CSV |
| --- | --- |
| 30 | busan 0.90 |
| 31 | seoul 0.90 |
| 36 | seoul 0.88 |
| 37 | osaka 0.88 |
| 42 | seoul 0.88 |
| 47 | seoul 0.87 |

- Numerical summaries in the report should use the CSV labels and counts.

## 2026-11-08 Baseline mistake observations: Osaka
- Sheet viewed: results/curate/mistakes_baseline_seed0_osaka_00.png (48 validation photos).
- Student's observations and hypotheses about the model's decisions, verbatim:

> **도쿄로 간 사진 (42장): 일본이라는 건 맞췄지만 도시는 도쿄로 기본 설정한 것 같아.**
>
> - 방음벽이 있는 고가·도시고속도로 대시캠 장면이 특히 많아. 오사카 #4·#7(도쿄 0.97), #9·#10·#11(0.96), #12·#14(0.95), #17·#18(0.94), #26·#30(0.92), #36(0.91)이야. 도로 구조만으로는 두 도시를 가를 수 없어서 전부 도쿄로 갔어.
> - 신사와 도리이 같은 일본 전통 건축도 도쿄로 갔어. 오사카 #1(도쿄 0.98), #5(0.97), #31(0.92), #44(0.90)야. 가장 높은 확신으로 틀린 게 #1이야.
> - 배낭 멘 보행자가 있는 일반 거리인 #6(0.97), #15(0.94), #32(0.92), #35(0.92)도 같은 경우야.
> - 평범한 주택가, 좁은 골목, 오래된 상점 거리인 #8, #27, #29, #33, #37, #45도 도쿄로 갔어.
> - 불꽃놀이 #21(0.93)과 #45(0.90), 고층 아파트가 보이는 도로 #20(0.94)도 도시 단서가 약했어.
> - 오사카 #25, #28, #40(도로 옆 터널 입구)은 오사카다운 지형이나 간판이 거의 안 보여.
>
> **서울로 간 사진 (5장): 글자나 사물이 일본 단서로 안 읽힌 경우야.**
>
> - 오사카 #2(서울 0.98)는 일본어 자막이 있는 거리인데도 서울로 갔어. 일본어를 읽고 있는지 의심스러워.
> - 오사카 #47(서울 0.90)도 일본어 표지판이 있는데 서울로 갔어.
> - 오사카 #19(검은 벤츠, 서울 0.94), #22(넓은 공터의 전통 건물, 서울 0.93), #48(국물 요리 한 그릇, 서울 0.89)은 도시 단서가 약하거나 한국 건축과 닮았어.
>
> **타이베이로 간 사진 (1장)**
>
> - 오사카 #38(붉은 아치형 다리와 연못, 타이베이 0.91)이야. 스미요시 다리처럼 오사카를 대표할 만한 장면인데 타이완 쪽으로 갔어.
>
> **눈에 띄는 점**은 오사카 정답 중 도쿄로 예측된 게 거의 대부분이라는 거야. 앞서 본 도쿄 오분류는 오사카로 17장이 갔는데, 오사카 오분류는 도쿄로 42장이 가서 비대칭이 커. 모델이 도쿄를 기본 선택으로 쓰고, 오사카 특유의 단서가 있어도 따로 반영하지 못하는 걸로 보여.

### Mechanical cross-check against the sheet CSV
- Source: results/curate/mistakes_baseline_seed0_osaka_00.csv.
- Among these 48 displayed photos, prediction counts are Tokyo 42, Seoul 5
  and Taipei 1, matching the Osaka counts in the student's observation.
- The Tokyo comparison uses Osaka 16, as verified in
  results/curate/mistakes_baseline_seed0_tokyo_00.csv; the original reference
  to 17 above is preserved verbatim.
- These comparisons describe the 48 most confident errors selected from each
  city, not the prediction frequencies over the full validation sets.

## 2026-11-08 Baseline mistake observations: Taipei
- Sheet viewed: results/curate/mistakes_baseline_seed0_taipei_00.png (48 validation photos).
- Student's observations and hypotheses about the model's decisions, verbatim:

> **도쿄로 간 사진 (25장): 간판이 안 보이는 평범한 도로, 주택가, 녹지야.**
>
> - 대시캠이나 도로 장면인 타이베이 #8·#12·#20·#21·#30·#46(도쿄 0.83\~0.93)이 대표적이야. 산이 보이는 도로(#8, #46)는 타이베이의 지형 단서일 수 있는데 반영되지 않은 것 같아.
> - 타이베이 #2(잔디밭, 도쿄 0.96), #3(계단 있는 건물, 도쿄 0.96), #11·#45(숲길), #29·#37(아파트와 주택가), #39(덩굴 덮인 옛 건물)도 도쿄로 갔어.
> - \#18과 #34(도쿄 0.88, 0.85)는 왼쪽 위에 작은 국기 아이콘이 있는데, 타이완 국기처럼 보여도 단서로 쓰이지 않은 듯해.
> - \#44(네온 간판 야경, 도쿄 0.83)와 #41(한자 간판이 붙은 건물, 도쿄 0.84)은 한자 간판이 일본으로 읽힌 것 같아.
>
> **서울로 간 사진 (18장): 사람 많은 야시장과 상점가, 어안렌즈 영상이야.**
>
> - 타이베이 #4·#5(서울 0.95), #7(0.93), #26, #33, #36, #48(0.83\~0.86)은 인파와 가게 간판이 빽빽한 번화가야. 한국 명동이나 시장 같은 분위기로 읽혔을 수 있어.
> - \#10·#17·#24·#32·#43(서울 0.84\~0.92)은 아래가 둥글게 휘어진 파노라마(어안) 영상이라 화질 문제로 도시 정보가 약했을 거야.
> - 휴대용 화장실 #9(서울 0.92), 호수 위 정자 #13(서울 0.91), 교실 #35(서울 0.85)처럼 도시 단서가 약한 장면도 있어.
>
> **오사카로 간 사진 (4장): 한자와 사찰, 네온이야.**
>
> - \#22(한자 현수막, 오사카 0.87), #27(등불 가득한 사당, 오사카 0.86), #14(네온 간판 거리, 오사카 0.89)는 한자나 장식적인 간판, 사찰이 오사카로 이어진 것 같아.
> - \#1(고층 타워, 오사카 0.96)은 가장 높은 확신으로 틀렸는데, 타워가 타이베이의 랜드마크일 수도 있어 보여.
>
> \*\*부산으로 간 사진 (1장)\*\*은 #47(푸른 언덕 산책로, 부산 0.83)이야. 산지 풍경이 부산으로 간 것 같아.
>
> **눈에 띄는 점**은 번체자 간판이 있는 사진(#22, #27, #41, #44, #48)도 타이베이로 안 갔다는 거야. 한자 때문에 일본이나 한국으로 간 거 같아. 앞의 도시들처럼 모델은 글자가 안 읽히면 도쿄, 인파가 많으면 서울로 가는 경향이 있어. 타이베이만의 단서인 열대 식생, 산, 스쿠터 같은 건 잘 못 쓴 것 같아.

### Mechanical cross-check against the sheet CSV
- Source: results/curate/mistakes_baseline_seed0_taipei_00.csv.
- Among these 48 displayed photos, verified prediction counts are Tokyo 24,
  Seoul 19, Osaka 4 and Busan 1.
- The student's original counts above are preserved verbatim; numerical
  summaries in the report should use these CSV counts.
- These are the city's 48 most confident errors, not the full validation set.

## 2026-11-08 Experiment proposal: training-class imbalance
- Student's requested change, hypothesis, rationale and limits, verbatim:

> 학습 데이터의 도시별 불균형을 보정하는 걸 바꿔보고 싶어. 방법은 클래스 균형 샘플링이나, 재학습 없이 되는 사후 로짓 보정(예측 로짓에서 τ·log(클래스 사전확률)을 빼는 방식)이야.
>
> **이유는 오분류가 한쪽으로 쏠려 있어서야.**
>
> - 오사카 정답 48장 중 42장이 도쿄로 갔는데, 도쿄 정답 중 오사카로 간 건 17장이야.
> - 부산 정답은 34장이 서울로 갔고, 서울 정답 중 부산으로 간 건 12장이야.
> - 타이베이 정답도 도쿄로 25장, 서울로 18장이 갔어.
> - 도시 단서가 없는 방음벽 도로, 평범한 골목, 클로즈업은 대부분 도쿄나 서울로 가. 모델이 애매하면 데이터가 많은 큰 도시를 고르는 사전확률 편향이 있는 것 같아.
> - 틀린 사진의 확률이 0.85\~0.99로 높다는 것도 같은 방향이야. 근거가 약한데도 높은 확률이 나온 건 데이터 분포가 확률에 그대로 반영됐다는 신호로 읽혀.
>
> 이건 내가 보고 세운 가설이고 학습 데이터의 도시별 장수는 내가 못 봤어. 그래서 실험 전에 클래스별 장수부터 확인하면 좋겠어.
>
> **Colab 실험 제안은 다음과 같아.**
>
> - 비교: 현재 모델 vs 사후 로짓 보정(τ를 0.5, 1.0 등으로 바꿔가며). 사후 보정은 재학습이 없어서 가장 빨라.
> - 지표: 도시별 recall, 혼동행렬, 틀린 샘플의 평균 확률(보정 정도), ECE.
> - 확인할 것: 오사카→도쿄, 부산→서울 쏠림이 줄어드는지, 그 대가로 도쿄·서울 recall이 얼마나 떨어지는지.
>
> **한계도 있어.** 도시 단서가 아예 없는 사진(오사카 방음벽 도로 등)은 보정해도 맞히기 어려워서, 오류가 다른 도시로 옮겨 가기만 할 수 있어. 그건 이 실험으로 얼마나 개선되는지 가를 수 있고, 개선이 작으면 입력 해상도나 글자 인식 같은 다음 조건을 보면 돼.

### Verified class counts before the experiment
- Source: the committed track_a/selection.csv, containing all 44,257 starter
  training photos, once each. Evidence: checks/training_class_counts.json.

| City | Selected training photos | Share (rounded) |
| --- | --- | --- |
| Seoul | 11274 | 25.47% |
| Busan | 5191 | 11.73% |
| Tokyo | 13347 | 30.16% |
| Osaka | 7200 | 16.27% |
| Taipei | 7245 | 16.37% |

- The most-confident-error sheets are selected subsets. Their verified counts
  are recorded in the preceding cross-checks, including Tokyo-to-Osaka 16 and
  Taipei-to-Tokyo 24 / Taipei-to-Seoul 19.
- Class imbalance is present; whether it causes the observed mistakes remains
  the student's hypothesis to examine. Selecting the most confident mistakes
  alone does not establish a cause of overconfidence.

### Prepared experiment: prior_adjust_baseline_v1
- First perform the requested no-retraining diagnostic on both saved baseline
  seeds using fixed tau values 0, 0.5 and 1.0. Balanced sampling is a separate
  retraining condition and is not combined with this diagnostic.
- Use selected-training frequencies only for priors. Apply
  adjusted_logits = logits - tau * log(prior), without fitting parameters.
- Use all 12,077 validation photos with the official preprocessing and class
  order. Cache one ONNX inference per model, and reuse those logits for every tau.
- Recompute tau 0 with the same backend as other tau values. ONNX float32
  predictions can differ slightly from the original CUDA mixed-precision scores.
- Record official macro recall, ordinary accuracy, per-city recall, confusion
  matrices and row-normalized pair error rates in both directions.
- Record top-label ECE with 15 equal-width confidence bins, confidence on current
  errors, and confidence / true-class probability on the fixed baseline-error set.
- Count corrected baseline errors, newly introduced errors, and errors that
  merely move to a different wrong city.
- Save separate diagnostic results under results/prior_adjust_baseline_v1/.
  These are not new training rows in experiments.csv. No best tau is selected
  automatically, and no model is exported or released by this analysis.
- Validation is a development set; choosing tau using these results does not
  turn the same validation score into an independent test estimate.
- The Track A recipe and selection remain unchanged. Any later submission
  implementation requires a separate recipe change and official quick check.
- References: [Menon et al., logit adjustment](https://arxiv.org/abs/2007.07314);
  [Guo et al., calibration](https://proceedings.mlr.press/v70/guo17a.html).

## 2026-11-08 prior_adjust_baseline_v1 results (post-hoc diagnostic)
- Completed on Colab at evaluation revision bfa91cc, using both saved baseline
  ONNX models and all 12,077 validation photos per model. No retraining occurred.
- The six model/tau evaluations were checked independently from their exported
  prediction CSVs: confusion matrices, recall, accuracy, ECE and error
  transitions agreed across all 72,462 prediction cases.
- Tau 0 was recomputed using the same ONNX backend as adjusted predictions.
  Its macro recall differs from the rounded training-script scores by
  +0.0001784400 (seed 0) and +0.0001462091 (seed 1).
- The table contains arithmetic means of the two model-specific metrics:

| Tau | Macro recall | Overall accuracy | ECE (15 bins) | Mean confidence on current errors |
| --- | --- | --- | --- | --- |
| 0 | 0.498212 | 0.524675 | 0.087887 | 0.538763 |
| 0.5 | 0.511549 | 0.523557 | 0.077591 | 0.526057 |
| 1 | 0.516638 | 0.514159 | 0.077232 | 0.517338 |

- Tau 1 increases mean macro recall by 1.842576 percentage points and changes
  overall accuracy by -1.051586 percentage points relative to tau 0.
- Macro recall increases for both seeds at tau 0.5 and tau 1. Among these
  pre-specified tau values, tau 1 has the highest validation macro recall
  for each seed.

| City | Mean recall at tau 0 | Mean recall at tau 0.5 | Mean recall at tau 1 |
| --- | --- | --- | --- |
| Seoul | 59.36% | 55.98% | 51.11% |
| Busan | 40.68% | 47.16% | 52.99% |
| Tokyo | 62.46% | 56.65% | 50.17% |
| Osaka | 35.62% | 40.98% | 45.65% |
| Taipei | 50.98% | 55.02% | 58.40% |

- Pair error rates below use all validation photos of the true/source city as
  their denominator and are averaged over the two models:

| True city to prediction | Tau 0 | Tau 0.5 | Tau 1 |
| --- | --- | --- | --- |
| Osaka to Tokyo | 39.22% | 31.93% | 25.54% |
| Tokyo to Osaka | 11.63% | 14.94% | 18.81% |
| Busan to Seoul | 30.79% | 25.83% | 21.94% |
| Seoul to Busan | 7.29% | 10.27% | 15.09% |
| Taipei to Tokyo | 21.36% | 16.96% | 13.11% |
| Taipei to Seoul | 18.57% | 16.30% | 13.69% |

| Model | Tau | Corrected baseline errors | New errors | Rerouted but still wrong |
| --- | --- | --- | --- | --- |
| seed 0 | 0.5 | 341 | 342 | 325 |
| seed 0 | 1 | 607 | 733 | 696 |
| seed 1 | 0.5 | 295 | 321 | 319 |
| seed 1 | 1 | 576 | 704 | 618 |

- Evidence: checks/prior_adjust_baseline_v1/report.json, metrics.csv,
  verified_summary.json, summary.md and summary.png.
- Original predictions and confidence-bin / confusion-matrix CSVs remain in
  results/prior_adjust_baseline_v1/. Execution output is in
  results/colab_logs/1108_192403_eval_logit_adjustment_prior_adjust_baseline_v1.txt.
- These diagnostic evaluations do not add training rows to experiments.csv.
  The Track A recipe and selection remain unchanged, and no new release was made.
- The student's interpretation and choice of the next method or tau are pending.

## 2026-11-08 Student interpretation of prior adjustment and next experiment (verbatim)

내 해석은 이래. **사후 보정은 쏠림을 줄였지만, 모델이 도시를 더 잘 구분하게 된 건 아니야.** 그냥 판정 경계를 옮긴 거에 가까워 보여.

**1. 도시별 변화가 거의 제로섬이야.**

- 부산 +12.3p, 오사카 +10.0p, 타이베이 +7.4p가 올랐고, 도쿄 −12.3p, 서울 −8.3p가 내려갔어.
- 평균하면 macro recall만 +1.84p 오르고 전체 정답률은 −1.05p 내려가. 큰 도시에서 잃은 만큼 작은 도시에서 얻었다는 뜻이야.
- 도시별 recall 평균이 표의 macro recall과 맞아떨어져서 숫자는 일관돼 보여.

**2. 오류 이동 표는 내가 예상한 한계를 그대로 보여줘.**

- τ=1에서 기존 오답을 고친 건 607건인데 새로 생긴 오답은 733건이야(seed 0). seed 1도 576 대 704로 같은 방향이야.
- 다른 도시로 옮겨 갔지만 여전히 틀린 것도 696건이나 돼. 도시 단서가 없는 사진은 prior를 바꿔도 맞히지 못한다는 얘기야.

**3. 내 가설 중 일부는 약해졌어.**

- 내가 틀린 사진들의 확률이 0.85\~0.99로 높다는 걸 사전확률 편향 신호로 읽었는데, 오답 평균 확률은 0.5388에서 0.5173으로 거의 안 줄었고 ECE도 0.0879에서 0.0772로 조금만 나아졌어.
- 높은 확신으로 틀리는 건 prior 때문만은 아니고, 한글·한자 같은 표면 단서에 과신하는 영향이 더 커 보여.
- 다만 내가 본 건 확률이 가장 높은 오답 48장이라 표의 전체 평균과 같은 기준은 아니야. 이 부분은 단정하지 않는 게 좋아.

**4. τ=0.5와 τ=1 차이는 아직 확신하기 어려워.**

- macro recall이 0.5115와 0.5166이고 ECE는 0.0776과 0.0772로 거의 같아. seed가 2개뿐이라 이 정도 차이는 노이즈일 수 있어.
- 더 신경 쓰이는 건 τ=1이 내가 돌린 값 중 가장 큰 값이라 탐색 범위 끝에서 최고라는 점이야. 더 큰 τ에서 더 오를지, 도쿄·서울 손실이 더 커질지 아직 몰라.

**다음 단계 제안**

- **먼저 τ를 더 촘촘하게 훑어봐(0.75, 1.25, 1.5, 2.0 정도).** 재학습이 필요 없어서 비용이 거의 없고, 피크가 τ=1 근처인지 확인할 수 있어. τ는 반드시 검증셋에서 고르고 최종 점수에는 쓰지 않는 게 안전해.
- **그다음 균형 샘플링을 별도 실험으로 돌려보는 걸 추천해.** 사후 보정은 마지막 판정만 바꾸고 표현은 안 바꾸니까, 샘플링은 특징 학습 자체에 영향을 줄 가능성이 있어서 비교 가치가 있어.
- 두 방법을 같이 쓰면 안 돼. 균형 샘플링 뒤에는 prior가 이미 균등에 가까워서 사후 보정을 또 하면 과보정이 돼. 균형 샘플링 모델은 τ=0부터 다시 확인하는 게 맞아.
- 개선이 둘 다 1\~2p 수준으로 작으면, 병목은 prior가 아니라 입력 정보라는 쪽에 무게를 둘 만해. 그때는 해상도나 글자 단서를 쓰는 방법을 보는 게 나아.

제출용 τ는 sweep 결과를 보고 정해도 늦지 않아. 지금은 τ=1을 잠정값으로 두는 정도가 적당해 보여.

### Implementation and interpretation boundaries (agent notes)
- The post-hoc experiment changes only output decision boundaries, with fixed
  learned weights. It cannot demonstrate improved feature learning; it also
  does not establish that the existing model uses no city-level features.
- The recorded user interpretation is a hypothesis. Surface/text shortcuts
  and missing information were not causally tested by this numeric sweep.
- These comparisons are deterministic on the fixed cached logits and validation
  set. Two training seeds do not establish generalization or significance.
- Tune tau only on the development/validation set, then freeze the chosen
  value and apply it at final inference if that method is selected. Do not tune
  using final-test or leaderboard feedback. No submission tau is finalized here.
- For the requested balanced model, evaluate unadjusted logits (tau 0).
  Reusing the raw training-count correction on that model would not describe
  its effective sampling prior. The two methods are kept separate in this test.
- Track A image size is fixed at 224. A later image-size experiment belongs to
  Track B and needs a separate student choice and a model-limit check.

## 2026-11-08 prior_adjust_baseline_v2: expanded numeric-cache sweep
- Reused the two exported baseline logit caches. No local model inference,
  image processing, training or dependency installation occurred.
- Evaluated tau 0, 0.5, 0.75, 1, 1.25, 1.5 and 2. The original three settings
  reproduce v1 metrics; all 169,078 model/tau prediction cases were independently
  checked from exported prediction CSVs, including confusion matrices,
  city recalls, accuracy, ECE, confidence and error transitions.
- Means below average the two model-specific measurements:

| Tau | Macro recall | Overall accuracy | ECE (15 bins) |
| --- | --- | --- | --- |
| 0 | 0.498212 | 0.524675 | 0.087887 |
| 0.5 | 0.511549 | 0.523557 | 0.077591 |
| 0.75 | 0.513032 | 0.518009 | 0.077642 |
| 1 | 0.516638 | 0.514159 | 0.077232 |
| 1.25 | 0.516385 | 0.506459 | 0.082115 |
| 1.5 | 0.515150 | 0.498510 | 0.087753 |
| 2 | 0.512718 | 0.482156 | 0.102763 |

- The highest mean validation macro recall among these settings is at tau 1,
  now inside the tested range. Tau 1 exceeds tau 1.25 by only 0.025288
  percentage points in this mean. Seed 0 peaks at tau 1.25; seed 1 at tau 1.
- Higher tau continues trading Seoul/Tokyo recall for Busan/Osaka/Taipei
  recall. From tau 1 to 2 the mean overall accuracy falls and ECE increases.
- Evidence: checks/prior_adjust_baseline_v2/report.json, metrics.csv,
  verified_summary.json, summary.md and summary.png. Reproduction:
  `src/sweep_cached_logits.py` with the existing original logit caches.
- No training rows or Release were added by this diagnostic.

## 2026-11-08 balanced: requested experiment prepared; Colab execution pending
- Student reason: the verbatim proposal above asks for class-balanced sampling
  as a separate comparison because it can affect learning, unlike post-hoc
  adjustment. No additional data curation or recipe change was requested.
- Recipe change: add collections.Counter and return inverse city-frequency
  sample weights. The theoretical city drawing probabilities are 20% each;
  the official sampler draws with replacement, so realized counts fluctuate.
- All 44,257 selected rows are retained. The other recipe functions, batch
  size 64 and official training budget are unchanged. No post-hoc correction
  is applied to the balanced model.
- Tag balanced, seed 0 only. Colab queue: audit expected/realized sampler
  counts, official quick check, official full-budget run, unadjusted ONNX
  evaluation against matched baseline seed 0 and five new mistake sheets.
- CUDA is required for the training commands; the preparation audit stops
  before training if the Colab GPU is unavailable.
- Local static-rule, syntax and sampler arithmetic checks are preparation
  checks only. The official quick check and full training remain pending on
  Colab; no new score is claimed and experiments.csv still has two baseline rows.

## 2026-11-08 balanced (Track A): completed Colab run and verified comparison
- changed: only inverse city-frequency sample weights, as recorded in the
  preceding preparation entry. Selection remains all 44,257 training rows;
  batch size 64, ResNet18, augmentation and optimizer settings are unchanged.
- why: the student's verbatim proposal above requests a separate balanced
  sampling experiment to compare a change to learning against post-hoc
  adjustment. The balanced model is evaluated without logit correction (tau 0).
- official validation: 0.4912 (matched baseline seed 0: 0.4933).
- training: seed 0, CUDA, 3,906 steps / 249,984 photo draws, 2,088.0 seconds
  (34.8 minutes), revision 78f24e0, recipe SHA prefix 7eb0f0acc97f and selection
  SHA prefix 365384496af8. Completed at 2026-11-08 21:04:53 KST.
- official quick check: 20 steps / 1,280 draws, validation 0.2821, before the
  full run; export gaps were below 0.001 for both quick and full models.
- sampler audit: expected city probability 20% each; realized counts were
  Seoul 50,023, Busan 50,153, Tokyo 50,124, Osaka 49,745 and Taipei 49,939.
  The counts sum to the official 249,984 draws.
- diagnostic: all 12,077 validation photos, same ONNX preprocessing/backend
  as baseline comparisons, 15-bin ECE. Colab inference took 530.02 seconds.
  Full training-script and diagnostic scores differ slightly because of
  numeric inference paths and rounding; compare like with like below.

| Method (seed 0 throughout) | ONNX macro recall | Overall accuracy | ECE | Mean confidence on current errors |
| --- | --- | --- | --- | --- |
| Baseline, tau 0 | 0.493478 | 0.522232 | 0.090188 | 0.539300 |
| Baseline, tau 1 | 0.512774 | 0.511799 | 0.078608 | 0.515175 |
| Balanced, tau 0 | 0.491359 | 0.503436 | 0.102839 | 0.537304 |

| City | Baseline tau 0 recall | Baseline tau 1 recall | Balanced tau 0 recall | Balanced minus baseline tau 0 (pp) |
| --- | --- | --- | --- | --- |
| Seoul | 57.99% | 49.86% | 48.67% | -9.32 |
| Busan | 39.57% | 51.94% | 44.53% | +4.96 |
| Tokyo | 63.49% | 50.73% | 55.22% | -8.27 |
| Osaka | 35.76% | 46.48% | 42.29% | +6.53 |
| Taipei | 49.93% | 57.38% | 54.97% | +5.04 |

- Measured differences: balanced macro recall is -0.211913 pp versus baseline
  tau 0 and -2.141495 pp versus baseline tau 1. Overall accuracy is -1.879606 pp
  versus baseline tau 0; ECE is higher by 0.012651531.
- Error transitions versus baseline seed 0, tau 0: 1,149 old errors corrected,
  1,376 new errors, 1,336 rerouted but still wrong, 3,285 unchanged wrong.
- Independent verification checked all 12,077 exported prediction cases,
  confusion matrices, city recalls, accuracy, confidence, ECE bins, pair
  error rates and transitions. Tau-0 probabilities were also reconstructed
  directly from exported numeric logits. No model or raw dataset was loaded
  locally, and no local training environment was installed.
- The five new top-48 mistake sheets were checked against the exact validation
  predictions; indexes and previews are under results/curate/ with prefix
  mistakes_balanced_seed0_. These are selected high-confidence mistakes,
  not estimates of full validation city-confusion frequencies.
- Evidence: checks/balanced_seed0.json, checks/balanced_check_seed0.json,
  checks/balanced_eval_seed0/report.json, metrics.csv, confidence_bins.csv,
  confusion.csv, verified_summary.json, summary.md and summary.png.
- Original output: results/colab_logs/1108_202032_audit_balanced.txt,
  1108_202310_official_balanced_check_seed0.txt,
  1108_202604_official_balanced_seed0.txt and 1108_210454_eval_balanced.txt.
- experiments.csv now has three full-training rows: baseline seeds 0 and 1,
  and balanced seed 0. Quick and diagnostic runs are not training rows.
- Scope: one balanced training seed only. These measurements do not establish
  statistical significance or identify whether the bottleneck is input
  information, representation learning or another training choice.
- what it means: student interpretation requested; pending. No interpretation
  has been invented for the student and no new release has been made.
- Next: record the student's interpretation and chosen next change. The
  current working recipe remains balanced; the existing release is unchanged.

## 2026-11-08 Student interpretation of balanced sampling (verbatim)

균형 샘플링은 이번 설정에서는 효과가 없었다고 봐. seed 0 기준으로 baseline 49.35%, 균형 샘플링 49.14%, 사후 보정(τ=1) 51.28%야. 샘플링은 −0.21p로 baseline과 구분이 안 되고, 사후 보정은 +1.93p로 앞서 두 seed 평균에서 본 +1.84p와 비슷하게 재현됐어.

### Measurement scope (agent notes)
- This records the student's interpretation without changing their wording.
- Baseline seed 0 and its tau-1 prediction numbers reuse the same saved model
  and logits already included in the earlier two-seed comparison. They are
  not a new independent replication of post-hoc adjustment; the balanced
  seed-0 training is the new run.
- A -0.21 pp observed difference from one balanced seed establishes neither
  equivalence nor a statistically significant difference. No gain was observed
  in this run under the requested setting.
- Student interpretation is now recorded. The next change and submission
  method have not been chosen; no new training or Release is queued here.

## 2026-11-08 logit_tau1: student-selected Track A Release preparation
- Student request (verbatim): "우선 오늘 자정 전에 track A를 제출해보고 싶어. 그 다음 track b를 해도 되려나?"
- Submitted choice question (verbatim): "오늘 제출할 Track A는 ‘baseline + 사후 보정 τ=1’, Release 제목은 ‘logit adjustment tau=1’로 할까요? 검증 점수가 가장 높은 후보이며, 선택하시면 짧은 Colab 검증을 통과한 뒤 제출하겠습니다."
- Student answer (verbatim): "이 제출안과 제목 사용 (권장)"
- Decision: submit baseline training plus fixed tau-1 post-hoc adjustment;
  proposed next tag track-a-2 and student-selected title
  "logit adjustment tau=1". Release creation is authorized after verification.
- Reason/evidence: the student's interpretation in the preceding entry
  compares seed-0 macro recalls 49.35%, 49.14% and 51.28% and concludes that
  balanced sampling did not help in this setting. The expanded validation
  sweep has its highest two-seed mean at tau 1. No leaderboard/final-test
  outcome has been used to tune this value.
- changed: restore every baseline training hook, including unweighted
  permutation sampling, and only in final_model subtract log(training prior)
  from the existing classifier bias. The architecture, classifier weight,
  training selection and budget do not change. This is not combined with
  balanced sampling.
- The counts are constants matching the accompanying selection.csv, in the
  official city order: Seoul 11,274, Busan 5,191, Tokyo 13,347, Osaka 7,200,
  Taipei 7,245. The recipe reads no files and needs only the allowed imports.
- Candidate canonical SHA256:
  61846a0692ccd893703a514dfbd84ac5298e46b2b6957fe0edfe9bd42c444856.
- Local checks: exact official static recipe checker, syntax, matching
  selection hash and AST identity of every baseline training hook passed.
  Existing numeric caches also showed no changed predictions for either
  baseline seed when evaluating the prior subtraction in float32 versus
  float64. This numeric check is not a test of a new trained model.
- Colab queue: real torch classifier-bias equivalence preflight, then the
  official 20-step quick check under tag logit_tau1_check, seed 0, CUDA.
  The preflight and training command require a GPU; no local training runs.
- Full baseline training is not repeated here. Previously recorded full-run
  adjusted validation measurements remain diagnostic evidence; the official
  quick check tests the submitted recipe/architecture/export, not its final
  full-budget leaderboard score. No new full-training row is claimed.
- Pending: import and verify the new Colab output, commit the result evidence,
  create track-a-2 with recipe.py and selection.csv, and verify the published
  assets and time before 2026-11-09 00:00 KST. Then proceed to Track B.

## 2026-11-08 logit_tau1 preflight: AST version compatibility fix
- Returned output at revision 6d9a4fb stopped in the auxiliary preflight with
  `ValueError: Baseline training hook changed: train_transform`.
- The official quick run was not started, no new full-training row was
  added, and no new Release was created. The failed output is preserved in
  results/colab_logs/1108_214600_check_logit_tau1.txt.
- Cause: the auxiliary comparison hashed Python AST dumps produced on
  different Python versions. Python 3.12 adds an empty type_params field to
  function nodes; the baseline hash prepared on Python 3.11 did not include
  that field. This was a checker bug, not a requested recipe change.
- Fixed the auxiliary fingerprint to serialize AST fields consistently,
  omitting only an empty type_params field. Nonempty fields remain checked.
- Verified locally that adding the newer empty field preserves all baseline
  hook fingerprints, while a real change to the crop size is still detected.
  Static recipe checks, syntax and baseline-hook comparisons also pass.
- The selected recipe and selection are unchanged, including canonical recipe
  SHA256 61846a0692ccd893703a514dfbd84ac5298e46b2b6957fe0edfe9bd42c444856.
- Pending: rerun the corrected preflight and the official quick check on Colab,
  then complete the already authorized track-a-2 Release with title
  "logit adjustment tau=1". No additional method/title approval is needed.

## 2026-11-08 logit_tau1: release checks passed
- The corrected preflight completed on Colab at revision 366f440. All
  baseline training hooks match, sampling remains unweighted, selected city
  counts match, and the actual torch classifier-bias implementation matches
  output-logit adjustment with maximum error 2.384185791015625e-07.
- Official quick check completed on CUDA at 2026-11-08 21:52:24 KST: 20 steps,
  batch size 64, 1,280 photo draws, 13.0 seconds training. Validation score
  0.2990 on 202 strided validation photos; ONNX export gap
  1.1920928955078125e-06. Architecture and export checks passed.
- This is a format/execution check, not a full-budget score. The earlier
  51.28% seed-0 / 51.66% two-seed-mean adjusted full-validation measurements
  remain separate diagnostic evidence. experiments.csv still has three
  full-training rows; no extra full training was performed for this check.
- Evidence: checks/logit_tau1_preflight.json,
  checks/logit_tau1_check_seed0.json and checks/track_a_2_prepublication.json.
  Original output: results/colab_logs/1108_214925_check_logit_tau1.txt and
  results/colab_logs/1108_214930_official_logit_tau1_check_seed0.txt.
- Froze the exact tested LF-normalized recipe.py and selection.csv for
  release. Their SHA256 values are respectively
  61846a0692ccd893703a514dfbd84ac5298e46b2b6957fe0edfe9bd42c444856 and
  365384496af87eef64262c7d69ea2e6c0b466b4a54ae5e6b2da81f533db0bf0e.
- Next action is the already authorized track-a-2 Release with the selected
  title "logit adjustment tau=1", followed by verification of published assets.

## 2026-11-08 track-a-2 published and downloaded assets verified
- Release: https://github.com/jaehakie/mas1004-assignment2/releases/tag/track-a-2
- Student-selected title: "logit adjustment tau=1".
- Published 2026-11-08 21:55:49 KST (12:55:49 UTC), before the requested
  2026-11-09 00:00 KST cutoff. Public, not a draft or prerelease.
- Target commit: 9fe33c5d40b5fd71e2e6b81fbeb67cd0e3d0dcc3.
- Exactly two assets: recipe.py (3,373 bytes) and selection.csv
  (1,345,856 bytes, all 44,257 selected photos). No model, dataset or starter
  download link is attached.
- Downloaded both published assets and verified byte-for-byte equality with
  the frozen tested assets. Their downloaded SHA256 values and GitHub asset
  digests agree with checks/track_a_2_prepublication.json.
- Evidence: checks/track_a_2_release.json and checks/track_a_2_verified.json.
- The Track A submission requested for tonight is complete. Actual grading
  and leaderboard reflection are pending the nightly grader; no leaderboard
  score for this release is claimed. The existing registration is unchanged.
- Next assignment work: Track B's first trained model and valid Release,
  followed by the remaining reports before the final deadline.
