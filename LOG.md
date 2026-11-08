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
