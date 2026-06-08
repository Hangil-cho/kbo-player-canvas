# 데이터 수집 가이드

## 오늘 만든 1차 수집 방식

`src/collect_kbo_official.py`는 KBO 공식 기록실의 공개 표를 읽어서 CSV로 저장합니다.

저장 위치:

```text
data/raw/
data/processed/
```

현재 수집 대상:

- 타자 기본기록 1
- 타자 기본기록 2
- 타자 세부기록 1
- 투수 기본기록 1
- 투수 기본기록 2
- 투수 세부기록 1
- 수비 기록
- 주루 기록

## 실행 방법

Codex가 실행해도 되고, 사용자가 직접 실행할 수도 있습니다.

```text
python src/collect_kbo_official.py
```

Codex 런타임을 쓸 때는 아래 Python을 사용합니다.

```text
C:\Users\gks12\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe src\collect_kbo_official.py
```

## 생성되는 파일

원본 수집 CSV:

```text
data/raw/kbo_hitter_basic1_2026.csv
data/raw/kbo_hitter_basic2_2026.csv
data/raw/kbo_hitter_detail1_2026.csv
data/raw/kbo_pitcher_basic1_2026.csv
data/raw/kbo_pitcher_basic2_2026.csv
data/raw/kbo_pitcher_detail1_2026.csv
data/raw/kbo_defense_basic_2026.csv
data/raw/kbo_runner_basic_2026.csv
data/raw/kbo_official_combined_2026.csv
```

관심 선수 매칭 결과:

```text
data/processed/kbo_target_players_snapshot_2026.csv
data/processed/kbo_target_players_missing_2026.csv
```

## 지금 방식의 한계

KBO 공식 기록실의 일부 페이지는 순위/규정 기준 첫 화면 중심입니다.

그래서 모든 선수가 항상 잡히지는 않습니다. 예를 들어 불펜 투수나 타석/이닝 표본이 적은 선수는 기본 순위 표에서 누락될 수 있습니다.

## 다음 보강 작업

1. 선수 상세 페이지의 `playerId`를 확보합니다.
2. 선수별 연도별 통산/시즌 기록을 상세 페이지에서 가져옵니다.
3. Statiz에서 WAR, RAA, wRC+, ERA+ 등 세이버 지표를 보강합니다.
4. 수집된 CSV를 기준으로 웹 화면의 데모 데이터를 실데이터로 교체합니다.
5. 팔각도, 릴리스, 타구속도 같은 트래킹 지표는 공개 출처 확인 후 별도 파일로 관리합니다.

