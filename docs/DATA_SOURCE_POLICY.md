# Data Source Policy

Last checked: 2026-06-14

## 핵심 원칙

KBO Player Canvas는 나중에 광고가 붙은 공개 웹페이지가 될 수 있으므로, 데이터 출처를 보수적으로 관리한다.

기준은 아래와 같다.

1. 공개 페이지에 보이는 숫자라도 상업 이용 허락이 명확하지 않으면 `conditional_review`로 둔다.
2. 로그인, 숨은 API, 우회 접근, 대량 요청이 필요한 데이터는 쓰지 않는다.
3. 영상, 캡처, 오디오, 하이라이트는 기록 데이터와 별개로 권리 처리가 필요하다.
4. Statiz는 크롤링하지 않는다.
5. Naver Sports의 숨은 API나 문자중계 데이터는 정식 허락 전에는 쓰지 않는다.
6. PTS/ABS 같은 투구 추적 데이터는 공식 제공자 또는 라이선스 계약이 확인된 뒤에만 붙인다.
7. 출처, 수집일, 품질 상태를 모든 처리 CSV에 남긴다.

## 현재 사용 가능 후보

### KBO 공식 기록실

사용 범위:

- 타자 기본/세부 기록
- 투수 기본/세부 기록
- 수비 기록
- 주루 기록
- 시즌/월/상황별 공개 표

프로젝트 상태:

- 수집 코드 사용 가능
- 원본 표는 `data/raw`
- 정규화 결과는 `data/processed`
- 상업 공개 전에는 출처 표기와 이용 허락 여부를 재확인

주의:

- KBO 공식 사이트는 하단에 `Copyright KBO, All Rights Reserved`를 표시한다.
- 따라서 원본 표 전체를 재배포하는 서비스가 아니라, 분석 결과와 요약 지표 중심으로 사용한다.
- 요청량을 낮게 유지한다.

### KBO 스코어보드

사용 범위 후보:

- 경기 일정
- 경기 상태
- 점수
- 이닝별 스코어
- 박스스코어 요약

주의:

- 문자중계 상세 데이터와 스코어보드 요약은 분리한다.
- 문자중계는 로그인/권리 확인이 필요할 수 있으므로 자동 수집 대상에서 제외한다.

## 현재 제외할 출처

### Statiz

이유:

- 상업 사이트 성격이 강하고 명시적 API/라이선스가 확인되지 않았다.
- WAR, wRC+, ERA+, RAA 같은 매력적인 지표가 있지만 자동 크롤링하지 않는다.

대안:

- 직접 계산 가능한 유사 지표를 만든다.
- 공개 공식 기록으로 계산 가능한 범위만 사용한다.
- 필요한 경우 사용자가 수동 입력 CSV로 보강한다.
- 정식 허락 또는 API가 확인되면 별도 소스로 추가한다.

### Naver Sports

이유:

- 문자중계와 pitch-level 데이터가 기술적으로 존재할 수 있으나, 자동화 수집과 상업 서비스 편입은 약관/권리 문제가 크다.
- 숨은 API를 호출하는 방식은 사용하지 않는다.

대안:

- 정식 제휴 API 또는 권리자 허락이 확인되면 별도 소스로 추가한다.
- 연구용 공개 데이터도 라이선스와 상업 이용 가능 여부가 명확하지 않으면 사용하지 않는다.

## PTS/ABS 데이터 전략

PTS/ABS 데이터는 이 프로젝트의 4번 목표, 즉 "왜 성적이 바뀌었는가" 분석에 매우 중요하다.

필요 컬럼 예시:

- game_id
- pitch_id
- pitcher_id
- batter_id
- inning
- ball_count
- strike_count
- pitch_type
- pitch_velocity
- pitch_result
- plate_x
- plate_z
- release_height
- release_side
- arm_angle
- vertical_movement
- horizontal_movement
- batted_ball_speed
- launch_angle
- hit_location

하지만 현재는 공식적으로 상업 이용 가능한 공개 API를 확인하지 못했다.

따라서 진행 순서는 아래와 같다.

1. KBO/KBOP/스포츠투아이 또는 공식 데이터 제공자에게 PTS/ABS 데이터 이용 가능 여부 문의
2. 제공 방식 확인
   - API
   - CSV 납품
   - 월별 리포트
   - 연구용 제한 데이터
3. 라이선스 범위 확인
   - 공개 웹페이지 사용 가능 여부
   - 광고 부착 가능 여부
   - 재가공 지표 표시 가능 여부
   - 원본 데이터 재배포 가능 여부
4. 계약 또는 허락이 있으면 `licensed_pts_provider` 소스로 추가
5. 그 전까지는 수동 입력 또는 기사/영상 링크 메타데이터만 사용

## 문자중계 데이터 전략

문자중계는 play-by-play 분석에 유용하다.

필요 컬럼 예시:

- game_id
- event_id
- inning
- batting_team
- pitcher
- batter
- count
- base_state
- outs
- event_text
- event_result
- runs_scored
- rbi
- pitch_sequence

진행 조건:

1. 공식적으로 사용할 수 있는 API 또는 CSV 제공 경로 확인
2. 로그인 우회나 숨은 API 호출 금지
3. 문자중계 원문을 그대로 재게시하지 않기
4. 이벤트 결과를 구조화한 데이터로 변환 가능 여부 확인
5. 출처와 권리 범위 표시

추천 구현 방식:

- `data/raw/live_text/`에 원본 저장
- `data/processed/play_by_play_events.csv`로 구조화
- `player_metric_values.csv`에는 결과 지표만 반영
- 원문 중계 문장은 웹에 길게 노출하지 않고 요약/계산 결과만 사용

## 출처 카탈로그

출처별 정책은 아래 CSV로 관리한다.

```text
data/processed/data_source_catalog.csv
```

수집 코드를 추가할 때는 이 CSV에 먼저 소스를 등록하고, `commercial_status`가 허용 또는 조건부 검토 상태인지 확인한다.

