# Data Collection Guide

## 현재 수집 범위

현재 자동 수집 대상은 KBO 공식 기록실의 공개 표로 제한한다.

수집 대상:

- 타자 기본기록 1
- 타자 기본기록 2
- 타자 세부기록 1
- 투수 기본기록 1
- 투수 기본기록 2
- 투수 세부기록 1
- 수비 기록
- 주루 기록

제외 대상:

- Statiz 자동 크롤링
- Naver Sports 숨은 API
- KBO 로그인 필요 문자중계
- 영상, 캡처, 오디오
- PTS/ABS 원천 데이터

제외 대상은 정식 허락, API, 라이선스가 확인되면 별도 소스로 추가한다.

## 실행 방법

```text
python src/collect_kbo_official.py
```

Codex 번들 Python으로 실행할 때:

```text
C:\Users\gks12\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe src\collect_kbo_official.py
```

## 생성 파일

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

처리 CSV:

```text
data/processed/kbo_official_column_inventory_2026.csv
data/processed/kbo_official_metric_values_2026.csv
data/processed/player_metric_values.csv
data/processed/kbo_target_players_snapshot_2026.csv
data/processed/kbo_target_players_missing_2026.csv
```

## 처리 방식

1. KBO 공식 표를 원본 그대로 `data/raw`에 저장한다.
2. 각 표의 컬럼을 `metric_catalog.csv`의 `metric_id`와 매핑한다.
3. 매핑된 지표를 long format으로 변환한다.
4. 대상 선수 10명과 매칭되는 행은 `player_metric_values.csv`에 저장한다.
5. 매칭되지 않은 선수는 missing report에 남긴다.

## 현재 한계

- 현재 수집은 공개 랭킹 표의 첫 페이지 중심이다.
- 일부 대상 선수는 규정/순위 조건 때문에 표에 없을 수 있다.
- 선수 상세 페이지 또는 전체 페이지 수집은 다음 단계에서 보강한다.
- KBO 공식 기록실에 없는 WAR, wRC+, ERA+, RAA는 자동 수집하지 않는다.
- PTS/ABS와 문자중계는 라이선스 확인 전까지 자동 수집하지 않는다.

## 다음 보강 작업

1. KBO 공식 기록실의 페이지네이션 처리
2. 선수 상세 페이지의 `pcode` 수집
3. 월별 기록 수집
4. 상황별 기록 수집
5. 리그 내 상위 n% 계산
6. 웹용 JSON 생성
7. 공식 허락 또는 라이선스가 있는 PTS/문자중계 소스 추가

