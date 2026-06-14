# Data Collection Guide

## 현재 수집 범위

현재 자동 수집 대상은 KBO 공식 기록실의 공개 표로 제한한다.

수집 대상:

- KBO 기록실 타자 기본기록 1/2
- KBO 기록실 타자 세부기록 1
- KBO 기록실 투수 기본기록 1/2
- KBO 기록실 투수 세부기록 1
- KBO 기록실 수비 기록
- KBO 기록실 주루 기록
- KBO 선수 조회를 통한 대상 선수 `playerId` 확인
- 선수 상세 기본기록
- 선수 상세 통산/연도별 기록
- 선수 상세 일자별 기록과 월별 합계
- 선수 상세 경기별 기록 원본
- 선수 상세 상황별 기록

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
data/raw/kbo_player_detail_tables_2026.csv
```

처리 CSV:

```text
data/processed/kbo_player_directory_2026.csv
data/processed/kbo_player_profiles_2026.csv
data/processed/kbo_player_monthly_records_2026.csv
data/processed/kbo_player_situation_records_2026.csv
data/processed/kbo_official_column_inventory_2026.csv
data/processed/kbo_official_metric_values_2026.csv
data/processed/player_metric_values.csv
data/processed/kbo_target_players_snapshot_2026.csv
data/processed/kbo_target_players_missing_2026.csv
```

## 처리 방식

1. KBO 공식 표를 원본 그대로 `data/raw`에 저장한다.
2. 기록실 표는 페이지네이션을 가능한 범위까지 따라간다.
3. 선수 조회 페이지에서 대상 선수 10명의 KBO `playerId`를 찾는다.
4. 선수 상세 `Basic`, `Total`, `Daily`, `Game`, `Situation` 페이지를 수집한다.
5. 각 표의 컬럼을 `metric_catalog.csv`의 `metric_id`와 매핑한다.
6. 매핑된 지표를 long format으로 변환한다.
7. 대상 선수 10명과 매칭되는 행은 `player_metric_values.csv`에 저장한다.
8. 매칭되지 않은 선수는 missing report에 남긴다.

## 현재 한계

- 기록실 페이지네이션은 KBO의 ASP.NET 폼 검증에 따라 일부 페이지에서 실패할 수 있어, 선수 상세 페이지 수집으로 대상 10명 충족을 보장한다.
- 선수 상세 `Daily`의 일별 행은 보관하지만, 현재 정규화 지표는 월별 `합계` 행 중심으로 생성한다.
- 선수 상세 `Game`은 원본 표 보관 단계이며, 추후 필요 지표만 정규화한다.
- KBO 공식 기록실에 없는 WAR, wRC+, ERA+, RAA는 자동 수집하지 않는다.
- PTS/ABS와 문자중계는 라이선스 확인 전까지 자동 수집하지 않는다.

## 다음 보강 작업

1. 리그 내 상위 n% 계산
2. 선수 상세 `Game` 원본에서 필요한 경기별 지표 정규화
3. 수집 CSV를 웹용 JSON으로 변환
4. 웹 화면을 `player_metric_values.csv` 기반으로 연결
5. 공식 허락 또는 라이선스가 있는 PTS/문자중계 소스 추가
