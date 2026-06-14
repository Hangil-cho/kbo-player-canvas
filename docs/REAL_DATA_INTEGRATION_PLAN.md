# 실데이터 연동 계획

## 현재 상태

실데이터 연동은 아직 끝나지 않았습니다.

현재 완료된 것은 1차 확인입니다.

- KBO 공식 기록실의 일부 공개 표를 CSV로 저장
- 관심 선수 10명 중 공식 첫 화면 표에서 잡히는 선수 확인
- CSV를 로컬 `data/raw`, `data/processed`에 저장
- CSV는 GitHub에 올리지 않도록 `.gitignore` 처리

## 문제

KBO 공식 기록실의 기본 표는 순위/규정/첫 화면 중심입니다.

그래서 다음 선수들은 현재 수집 방식에서 누락될 수 있습니다.

- 불펜 투수
- 표본이 적은 선수
- 규정 이닝/타석에서 빠지는 선수
- 순위 첫 페이지 밖에 있는 선수

따라서 다음 단계는 단순 표 수집이 아니라, 선수별 식별자와 시즌별 데이터 원장을 만드는 것입니다.

## 추천 순서

### 1. 선수 마스터 만들기

목표:

- 관심 선수 10명의 `player_id`, 이름, 팀, 포지션, 투타, 데뷔연도, 역할을 한 파일에 정리합니다.

파일:

```text
data/processed/players_master.csv
```

필요 컬럼:

- player_id
- player_name
- team
- position_group
- role_group
- throws
- bats
- debut_year
- source_url

이 작업이 먼저 필요한 이유:

- KBO와 Statiz의 선수명이 같아도 동명이인 가능성이 있습니다.
- 팀 이동, 개명, 포지션 변경이 있으면 이름만으로 조인하기 위험합니다.
- 이후 모든 수집 파일은 이 마스터를 기준으로 붙입니다.

### 2. KBO 공식 기록 상세 수집

목표:

- 타자/투수/수비/주루의 시즌별 기본 기록을 선수 단위로 수집합니다.

우선 수집:

- 타자 기본 기록
- 투수 기본 기록
- 수비 기록
- 주루 기록

저장 파일 예시:

```text
data/raw/kbo_hitter_season_raw.csv
data/raw/kbo_pitcher_season_raw.csv
data/raw/kbo_defense_season_raw.csv
data/raw/kbo_runner_season_raw.csv
```

처리 파일 예시:

```text
data/processed/player_season_batting.csv
data/processed/player_season_pitching.csv
data/processed/player_season_defense.csv
data/processed/player_season_running.csv
```

### 3. 세이버/가치 지표 보강 방식 분리

목표:

- WAR, RAA, wRC+, ERA+ 같은 세이버/가치 지표를 안전한 방식으로 보강합니다.

중요 원칙:

- Statiz는 자동 크롤링하지 않습니다.
- 공식 API, 라이선스 계약, 사용자의 수동 CSV, 직접 계산 가능한 지표만 사용합니다.

우선순위:

- WAR
- 공격 RAA
- 주루 RAA
- 수비 RAA
- wRC+
- ERA+
- FIP 계열 지표

주의:

- 출처별 계산 방식이 다를 수 있으므로 같은 이름의 지표라도 source를 반드시 남깁니다.
- 상업 공개 페이지에 쓰기 애매한 지표는 처음에는 CSV 수동 입력 템플릿으로 관리합니다.
- 정식 허락이나 API가 확인되기 전까지는 `수집 전`, `수동 보강 필요`, `라이선스 필요`로 표시합니다.

### 4. 선수별 시즌 원장 만들기

목표:

- 웹페이지가 바로 읽을 수 있는 통합 시즌 데이터를 만듭니다.

파일:

```text
data/processed/player_season_summary.csv
```

포함 내용:

- 기본 기록
- 세이버 기록
- 수비/주루 기록
- WAR
- 리그 평균 대비 위치
- 상위 몇 %

### 5. 웹 데이터 파일 생성

목표:

- CSV를 웹에서 읽기 쉬운 JSON으로 변환합니다.

파일:

```text
web/data/players.json
```

이후 화면의 데모 데이터는 `players.json`에서 불러오는 실제 데이터로 교체합니다.

### 6. 고급 서번트형 지표 분리 관리

목표:

- 타구속도, 하드힛, 배럴, 팔각도, 릴리스, 무브먼트 같은 지표를 별도 레이어로 관리합니다.

현실 체크:

- KBO는 MLB Baseball Savant처럼 모든 트래킹 데이터를 공개하지 않을 수 있습니다.
- 공개 출처가 없으면 `수동 입력`, `기사/영상 링크`, `추정 불가`로 구분합니다.

파일:

```text
data/processed/player_advanced_tracking.csv
```

## 지금 바로 할 첫 작업 추천

가장 먼저 할 일은 `players_master.csv`를 만드는 것입니다.

그 다음에 KBO 공식 기록 상세 수집을 붙이고, 마지막에 라이선스가 확인된 세이버/WAR/PTS 데이터를 붙이는 순서가 가장 안전합니다.

## 사용자가 정하면 좋은 것

- 실제 데이터 우선 적용 선수 1명
- KBO 공식 기록과 수동/라이선스 데이터 중 어느 쪽을 먼저 신뢰 기준으로 둘지
- 자동 수집이 안 되는 지표를 수동 CSV로 관리해도 되는지
- WAR 기준을 직접 계산할지, 라이선스 데이터로 받을지, 당분간 제외할지
