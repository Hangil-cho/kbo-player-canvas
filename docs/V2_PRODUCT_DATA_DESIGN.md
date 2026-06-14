# KBO Player Canvas V2 Design

## 1. 제품 목적

KBO Player Canvas는 단순히 선수 기록을 보여주는 페이지가 아니다.

목표는 사용자가 특정 선수를 골랐을 때 아래 질문에 답하게 만드는 것이다.

1. 이 선수의 현재 스탯은 어떤가?
2. 같은 리그, 같은 역할, 같은 포지션 선수들과 비교하면 어느 정도인가?
3. 시즌별, 월별로 무엇이 좋아졌고 무엇이 나빠졌는가?
4. 그 성적 변화가 어떤 상세 지표 변화와 연결되는가?

가장 중요한 질문은 4번이다.

따라서 화면과 데이터 구조는 모두 "결과 지표"와 "원인 후보 지표"를 연결하는 방식으로 설계한다.

예시:

- OPS가 올랐다 -> 출루율 때문인가, 장타율 때문인가?
- 장타율이 올랐다 -> ISO, 홈런 비율, 2루타 비율, 타구 질 지표가 같이 올랐는가?
- ERA가 좋아졌다 -> WHIP, K/BB, 피홈런, BABIP, 이닝 소화, 구원/선발 역할 변화 중 무엇이 영향을 줬는가?
- WAR가 올랐다 -> 타격, 주루, 수비, 포지션 가치 중 어느 부분이 커졌는가?

## 2. 화면 구조

### 전체 구조

```text
KBO Player Canvas

[검색/필터/선수 선택]

[공통 선수 영역]
  - 선수명, 팀, 포지션, 역할
  - 현재 시즌 핵심 요약
  - 데이터 기준 시즌/출처/업데이트 상태
  - 화면 전환: 대표 지표 보기 / 상세 지표 보기

[선택된 화면]
  A. 대표 지표 보기
  B. 상세 지표 보기

[별도 진입]
  C. 선수 상세 분석 페이지
```

공통 선수 영역은 항상 고정한다.

다만 "대표 지표 보기"와 "상세 지표 보기"는 동시에 보이지 않는다. 사용자가 스위치를 눌러 한 화면만 본다.

선수 상세 분석 페이지는 더 깊은 분석용 별도 페이지로 둔다.

### 2.1 공통 선수 영역

공통 영역은 사용자가 어느 화면에 있든 계속 같은 맥락을 유지하게 해준다.

구성:

- 상단 제목: `KBO Player Canvas`
- 검색/필터:
  - 이름 검색
  - 팀 선택
  - 포지션 선택
  - 선수 선택
- 선수 프로필:
  - 선수명
  - 팀
  - 포지션
  - 역할: 선발 투수, 불펜 투수, 내야수, 외야수 등
  - 투타, 데뷔연도, 최근 소속팀
- 핵심 요약 카드:
  - 타자: AVG, OBP, SLG, OPS, BB/K, WAR
  - 투수: ERA, IP, WHIP, K/BB, K%, WAR
  - 수비/주루가 중요한 야수는 수비 RAA, 주루 RAA를 보조 카드로 노출
- 데이터 상태:
  - 실데이터 연결 전
  - 일부 수집 완료
  - 수동 보강 필요
  - 출처 확인 필요

### 2.2 대표 지표 보기

대표 지표 보기는 "이 선수가 지금 어느 정도인가"를 빠르게 이해하는 화면이다.

구성:

1. 리그 내 위치
   - 대표 지표 5개 또는 6개
   - 각 지표는 `상위 n%`로 표시
   - 비교 기준을 함께 표시
     - 타자: 규정 타석 또는 일정 타석 이상 타자
     - 선발 투수: 선발 투수 그룹
     - 불펜 투수: 불펜 투수 그룹
     - 포지션 비교: 내야수, 외야수, 포수 등

2. 성적 흐름
   - 시즌별 / 월별 스위치
   - 월별은 최근 12개월 기준
   - 지표 드롭다운
   - 기본 지표 예시:
     - 타자: OPS, AVG, OBP, SLG, BB/K, WAR
     - 투수: ERA, WHIP, K/BB, K%, IP, WAR
   - 그래프에는 리그 평균선과 선수 자신의 전년도 기준선을 같이 표시

3. 기록표
   - 선수가 활동한 전체 시즌을 내림차순으로 표시
   - 기본 / 가치 / 수비·주루 탭
   - 값이 없는 지표는 빈칸이 아니라 `수집 전`, `출처 없음`, `해당 없음`으로 구분

### 2.3 상세 지표 보기

상세 지표 보기는 "대표 지표를 만든 원인 후보"를 확인하는 화면이다.

구성:

1. 상세 리그 내 위치
   - 대표 지표보다 많은 지표를 카테고리별로 보여준다.
   - 모든 지표는 `상위 n%`, 순위, 비교 그룹을 함께 표시한다.

2. 상세 지표 흐름
   - 시즌별 / 월별 스위치
   - 지표 카테고리 선택
   - 여러 지표를 같은 그래프에서 비교할 수 있게 한다.

3. 변화 후보 요약
   - "이 선수가 좋아진 부분"
   - "나빠진 부분"
   - "성적 변화와 같이 움직인 지표"
   - "표본이 작아 판단 보류할 지표"

4. 선수 상세 분석 페이지 진입
   - 특정 결과 지표 카드에서 `왜 바뀌었나 보기` 버튼 제공
   - 예: OPS 카드 -> OPS 변화 원인 분석 페이지
   - 예: ERA 카드 -> ERA 변화 원인 분석 페이지

### 2.4 선수 상세 분석 페이지

이 페이지가 프로젝트의 핵심이다.

역할:

- 결과 지표가 왜 바뀌었는지 분석한다.
- 상세 지표와 결과 지표의 관계를 보여준다.
- 분석 근거와 데이터 한계를 함께 보여준다.

구성:

1. 질문 설정 영역
   - 분석 지표: OPS, WAR, ERA, WHIP, wRC+, ERA+ 등
   - 비교 기간:
     - 전년 대비
     - 전반기 대비 후반기
     - 최근 12개월
     - 특정 월 대비 특정 월
   - 비교 기준:
     - 본인 과거
     - 리그 평균
     - 같은 포지션
     - 같은 역할
     - 특정 선수

2. 결과 변화 요약
   - 결과 지표가 얼마나 변했는지
   - 리그 내 위치가 어떻게 변했는지
   - 변화가 표본상 의미 있는지

3. 원인 후보 분해
   - 타자 예시:
     - OPS 변화
     - OBP 변화, SLG 변화
     - BB%, K%, BB/K
     - ISO, BABIP, HR/PA
     - 주루 RAA, 수비 RAA, WAR 구성 변화
   - 투수 예시:
     - ERA 변화
     - WHIP, K/BB, K%, BB%, HR/9
     - BABIP, LOB%, 피장타율
     - 이닝 소화, 선발/불펜 역할 변화
     - 구종 비율, 구속, 무브먼트, 릴리스 포인트

4. 그래프
   - 결과 지표와 상세 지표를 같은 시간축에 표시
   - 변화 시점을 강조
   - 원인 후보별 기여도 막대 또는 waterfall 차트

5. 근거와 한계
   - 데이터 출처
   - 공개 데이터 여부
   - 수동 입력 여부
   - 추정 여부
   - 확신도: 높음, 보통, 낮음

## 3. 지표 설계

### 3.1 지표 구분

모든 지표는 아래 네 종류 중 하나로 분류한다.

```text
결과 지표
  사용자가 최종 성과로 이해하는 지표
  예: OPS, ERA, WAR, wRC+, ERA+

직접 구성 지표
  결과 지표를 수식상 직접 구성하는 지표
  예: OPS = OBP + SLG

원인 후보 지표
  결과 지표에 영향을 줄 가능성이 있는 상세 지표
  예: K%, BB%, ISO, BABIP, HR/9, K/BB

맥락 지표
  해석에 필요한 조건 지표
  예: 타석, 이닝, 팀, 구장, 포지션, 선발/불펜
```

### 3.2 타자 지표

대표 지표:

- AVG
- OBP
- SLG
- OPS
- BB/K
- WAR

상세 지표:

- 타석, 타수, 안타, 2루타, 3루타, 홈런
- BB%, K%, BB/K
- ISO
- BABIP
- HR/PA
- 득점권 성적
- 좌우 투수 상대 성적
- 주루 RAA 또는 주루 가치
- 도루, 도루 실패, 도루 성공률
- 수비 이닝, 실책, 수비율
- 수비 RAA 또는 수비 가치
- 포지션별 출장 비율

공개 데이터가 있으면 추가할 지표:

- 타구 속도
- 하드힛 비율
- 발사각
- 타구 방향
- 존별 타격 성적
- 스윙률
- 컨택률
- 헛스윙률

### 3.3 투수 지표

대표 지표:

- ERA
- IP
- WHIP
- K/BB
- K%
- WAR

상세 지표:

- 선발/불펜 역할
- 경기, 선발, 세이브, 홀드
- 이닝
- 피안타, 피홈런, 볼넷, 사구, 탈삼진
- K%, BB%, K-BB%
- HR/9
- H/9
- BABIP
- LOB%
- FIP 또는 유사 지표
- ERA+
- 피OPS
- 선발 투수는 이닝 소화율, QS, 경기당 이닝
- 불펜 투수는 레버리지, 멀티이닝, 연투 여부

공개 데이터가 있으면 추가할 지표:

- 평균 구속
- 최고 구속
- 구종 수
- 구종 비율
- 구종별 피OPS
- 구종별 헛스윙률
- 구종별 가치
- 릴리스 포인트
- 팔각도
- 수직/수평 무브먼트
- 존 비율
- 초구 스트라이크율
- CSW%

## 4. 데이터 저장 설계

처음부터 서버 DB를 만들 필요는 없다.

권장 구조는 `CSV -> 정제 CSV -> 웹용 JSON`이다.

나중에 데이터가 커지면 같은 구조를 SQLite나 DuckDB로 옮긴다.

### 4.1 폴더 구조

```text
data/
  raw/
    source_name_original_files.csv
  processed/
    players_master.csv
    metric_catalog.csv
    player_metric_values.csv
    league_metric_baselines.csv
    player_metric_rankings.csv
    player_period_changes.csv
    metric_driver_map.csv
    player_driver_analysis.csv
    player_media_evidence.csv
    data_quality_notes.csv

web/
  data/
    player_index.json
    players/
      player_id.json
    league/
      season_group.json
```

### 4.2 핵심 테이블

#### players_master.csv

선수의 기준 정보.

```text
player_id
player_name
team
position_group
role_group
throws
bats
debut_year
kbo_url
statiz_url
active_from
active_to
```

#### metric_catalog.csv

지표 사전.

```text
metric_id
metric_name_kr
metric_name_en
metric_group
metric_kind
unit
higher_is_better
source_priority
description
```

예시:

```text
ops,OPS,OPS,batting,result,rate,true,kbo/statiz,출루율과 장타율의 합
obp,출루율,OBP,batting,direct_component,rate,true,kbo,출루 능력
slg,장타율,SLG,batting,direct_component,rate,true,kbo,장타 생산력
iso,ISO,ISO,batting,driver,rate,true,statiz,순수 장타력
```

#### player_metric_values.csv

모든 선수 지표를 같은 형태로 저장하는 핵심 테이블.

```text
player_id
season
period_type
period_value
team
role_group
position_group
metric_id
value
sample_size
source
source_url
quality_flag
collected_at
```

예시:

```text
kbo_park_younghyun,2026,season,2026,kt wiz,reliever,pitcher,era,2.18,33.0,kbo,...
kbo_park_younghyun,2026,season,2026,kt wiz,reliever,pitcher,whip,1.02,33.0,kbo,...
kbo_park_younghyun,2026,month,2026-06,kt wiz,reliever,pitcher,kbb,4.20,8.1,kbo,...
```

이 구조를 쓰면 시즌, 월, 통산, 특정 기간을 모두 같은 방식으로 처리할 수 있다.

#### league_metric_baselines.csv

리그 평균과 비교 그룹 평균.

```text
season
period_type
period_value
comparison_group
metric_id
avg_value
median_value
min_value
max_value
qualified_count
source
```

comparison_group 예시:

- league_hitter
- league_pitcher
- starter_pitcher
- reliever_pitcher
- infielder
- outfielder
- catcher

#### player_metric_rankings.csv

상위 n%와 순위 계산 결과.

```text
player_id
season
period_type
period_value
comparison_group
metric_id
rank
qualified_count
top_pct
value
league_avg
```

표시 방식:

- `rank = 8`
- `qualified_count = 62`
- `top_pct = 12.9`
- 화면 표시: `상위 13%`

낮을수록 좋은 지표는 정렬 방향을 바꿔 계산한다.

예:

- ERA는 낮을수록 좋음
- WHIP는 낮을수록 좋음
- BB%는 맥락에 따라 낮을수록 좋음

#### player_period_changes.csv

기간 간 변화량.

```text
player_id
metric_id
from_period_type
from_period_value
to_period_type
to_period_value
from_value
to_value
delta
delta_pct
league_delta
relative_delta
sample_warning
```

#### metric_driver_map.csv

결과 지표와 원인 후보 지표의 관계.

```text
outcome_metric_id
driver_metric_id
relationship_type
direction
weight
required_sample_size
note
```

예시:

```text
ops,obp,direct_component,positive,1.00,50,OPS 직접 구성 요소
ops,slg,direct_component,positive,1.00,50,OPS 직접 구성 요소
slg,iso,driver,positive,0.80,50,장타력 변화 후보
slg,babip,context,positive,0.40,50,인플레이 타구 결과 변동
era,whip,driver,negative,0.80,10,출루 허용 억제
era,kbb,driver,positive,0.70,10,삼진/볼넷 안정성
```

#### player_driver_analysis.csv

실제 분석 결과.

```text
player_id
outcome_metric_id
from_period
to_period
driver_metric_id
driver_change
driver_rank_change
contribution_score
confidence
analysis_text
```

분석 문장은 이 테이블을 기반으로 자동 생성한다.

중요 원칙:

- 데이터로 확인되지 않는 내용은 단정하지 않는다.
- `~때문이다`보다 `~와 함께 움직였다`, `영향 가능성이 높다`로 표현한다.
- 표본이 작으면 `판단 보류`로 표시한다.

#### player_media_evidence.csv

사진, 영상, 기사, 인터뷰 링크를 저장한다.

```text
player_id
season
period_value
evidence_type
title
url
related_metric_id
note
source
```

예:

- 박영현 구종 변화 기사
- 김도영 타격폼 변화 인터뷰
- 원태인 구속 변화 관련 영상

## 5. 분석 로직

### 5.1 상위 n% 계산

```text
top_pct = rank / qualified_count * 100
```

화면에는 소수점 없이 표시한다.

예:

- 8위 / 62명 = 상위 13%

높을수록 좋은 지표와 낮을수록 좋은 지표를 metric_catalog에서 관리한다.

### 5.2 변화 원인 분석 v1

처음부터 완벽한 인과 분석을 하지 않는다.

1차 분석은 "결과 지표 변화와 같이 움직인 상세 지표 후보"를 찾는 방식이다.

절차:

1. 결과 지표 선택
   - 예: OPS
2. 비교 기간 선택
   - 예: 2025 시즌 -> 2026 시즌
3. 결과 지표 변화 계산
   - OPS +0.084
4. 직접 구성 지표 변화 확인
   - OBP +0.031
   - SLG +0.053
5. 원인 후보 지표 변화 확인
   - BB% 증가
   - K% 감소
   - ISO 증가
   - BABIP 증가
6. 리그 변화와 비교
   - 리그 전체도 올랐는지
   - 선수만 크게 올랐는지
7. 기여 후보 점수 계산
   - 변화 크기
   - 리그 대비 변화
   - 지표 관계 가중치
   - 표본 크기
8. 분석 문장 생성

### 5.3 분석 문장 예시

타자:

```text
2026년 OPS 상승은 장타율 상승의 비중이 더 큽니다.
SLG가 전년 대비 +0.053 올랐고, ISO와 홈런 비율도 함께 상승했습니다.
반면 BABIP 상승분도 있어 타구 질 개선과 결과 변동이 함께 섞여 있을 가능성이 있습니다.
```

투수:

```text
ERA 개선은 WHIP 하락과 K/BB 상승이 같이 나타난 구간에서 두드러집니다.
볼넷 허용이 줄고 탈삼진 비율이 유지되면서 주자 누적이 줄어든 흐름입니다.
다만 BABIP도 낮아져 수비와 타구 결과의 영향은 별도로 확인해야 합니다.
```

## 6. 실데이터 연동 추천 순서

### Step 1. 지표 사전부터 만든다

파일:

```text
data/processed/metric_catalog.csv
data/processed/metric_driver_map.csv
```

이유:

- 어떤 데이터를 가져올지 기준이 생긴다.
- 지표별로 높을수록 좋은지, 낮을수록 좋은지 관리할 수 있다.
- 결과 지표와 원인 후보 지표를 연결할 수 있다.

### Step 2. 선수 마스터를 만든다

파일:

```text
data/processed/players_master.csv
```

우선 10명으로 시작한다.

1. kt wiz 박영현
2. kt wiz 소형준
3. kt wiz 최원준
4. kt wiz 안현민
5. 삼성 라이온즈 원태인
6. ssg 랜더스 박성한
7. nc 다이노스 김주원
8. 롯데 자이언츠 김진욱
9. 기아 타이거즈 김도영
10. 한화 이글스 심우준

### Step 3. KBO 공식 기록을 수집한다

우선 수집:

- 타자 시즌 기록
- 투수 시즌 기록
- 수비 기록
- 주루 기록
- 월별 기록

목표:

- 대표 지표 보기 화면을 실데이터로 채운다.

### Step 4. 공식/라이선스/수동 보강 지표를 분리한다

Statiz는 자동 크롤링하지 않는다.

우선 분류:

- KBO 공식 기록으로 직접 계산 가능한 지표
- 공식 API 또는 라이선스 계약이 필요한 지표
- 사용자가 수동 CSV로 입력할 지표
- 기사/영상 링크를 근거로만 남길 지표

목표:

- 상세 지표 보기와 변화 원인 분석에 쓸 수 있는 데이터만 안전하게 붙인다.
- WAR, wRC+, ERA+, RAA 계열은 정식 허락 또는 계산 방식이 확인될 때까지 `수집 전` 또는 `수동 보강 필요`로 둔다.

### Step 5. long format으로 정규화한다

파일:

```text
data/processed/player_metric_values.csv
```

모든 출처의 데이터를 이 형태로 합친다.

### Step 6. 리그 내 위치를 계산한다

파일:

```text
data/processed/league_metric_baselines.csv
data/processed/player_metric_rankings.csv
```

대표 지표와 상세 지표 모두 `상위 n%`를 계산한다.

### Step 7. 웹용 JSON을 만든다

파일:

```text
web/data/player_index.json
web/data/players/{player_id}.json
```

GitHub Pages에서는 이 JSON을 읽어서 화면에 표시한다.

### Step 8. 변화 원인 분석 v1을 만든다

파일:

```text
data/processed/player_period_changes.csv
data/processed/player_driver_analysis.csv
```

처음에는 규칙 기반으로 만든다.

예:

- OPS는 OBP, SLG를 먼저 본다.
- SLG는 ISO, HR/PA, BABIP를 본다.
- ERA는 WHIP, K/BB, HR/9, BABIP를 본다.
- WAR는 타격, 수비, 주루, 투구 가치로 나눠 본다.

## 7. 먼저 구현할 MVP 범위

1차 목표는 "완전한 서번트 앱"이 아니다.

먼저 아래만 제대로 되면 된다.

1. 선수 선택
2. 공통 선수 영역
3. 대표 지표 보기
4. 상세 지표 보기
5. 시즌별/월별 흐름
6. 전체 시즌 기록표
7. 리그 내 상위 n%
8. OPS 또는 ERA 변화 원인 분석 v1

추천 첫 분석 선수:

- 타자: 김도영
- 투수: 박영현

이유:

- 타자와 투수 구조를 둘 다 검증할 수 있다.
- 대표 지표와 상세 지표의 차이가 잘 드러난다.
- 이후 나머지 8명에 같은 구조를 적용하기 쉽다.

## 8. 확인이 필요한 결정

실데이터 연동 전에 사용자가 정하면 좋은 것:

1. 첫 실데이터 연결 선수
   - 추천: 김도영 1명 + 박영현 1명
2. 데이터 기준 시즌
   - 추천: 2026 현재 시즌 + 가능한 전체 과거 시즌
3. 월별 데이터 범위
   - 추천: 최근 12개월 + 시즌 전체 월별
4. 고급 지표 처리 방식
   - 공개 출처에서 자동 수집
   - CSV 수동 입력
   - 기사/영상 링크 기반 보조 근거
5. 분석 문장 톤
   - 조심스러운 해석
   - 조금 더 리포트형 요약
   - 데이터 한계를 강하게 표시

## 9. 다음 작업

다음 작업은 코드보다 데이터 구조부터 시작한다.

추천 순서:

1. `metric_catalog.csv` 초안 생성
2. `metric_driver_map.csv` 초안 생성
3. `players_master.csv` 생성
4. KBO 공식 기록과 라이선스 가능한 외부 데이터 컬럼 재확인
5. 수집 코드 수정
6. `player_metric_values.csv` 생성
7. 대표 지표 화면을 실데이터로 교체
8. 상세 지표 화면을 실데이터로 교체
9. 변화 원인 분석 v1 생성
