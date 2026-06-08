const ALL_TEAMS = "전체 팀";
const ALL_POSITIONS = "전체 포지션";

const hitterChartMetrics = [
  { key: "avg", label: "타율" },
  { key: "obp", label: "출루율" },
  { key: "slg", label: "장타율" },
  { key: "ops", label: "OPS" },
  { key: "war", label: "WAR" },
];

const pitcherChartMetrics = [
  { key: "era", label: "방어율" },
  { key: "ip", label: "이닝" },
  { key: "whip", label: "WHIP" },
  { key: "kbb", label: "K/BB" },
  { key: "war", label: "WAR" },
];

function makeHitter(config) {
  return {
    type: "hitter",
    chartMetrics: hitterChartMetrics,
    leagueContext: "타자 대표 지표 5개 백분위",
    detailContext: "타구 질, 선구안, 컨택 관련 서번트형 지표",
    metrics: [
      ["타율", config.current.avg, config.notes.avg],
      ["출루율", config.current.obp, config.notes.obp],
      ["장타율", config.current.slg, config.notes.slg],
      ["OPS", config.current.ops, config.notes.ops],
      ["볼삼비", config.current.bbk, config.notes.bbk],
      ["WAR", config.current.war, config.notes.war],
    ],
    tables: {
      basic: {
        headers: ["시즌", "타율", "출루율", "장타율", "OPS", "홈런", "볼삼비", "WAR"],
        rows: config.seasons.map((row) => [
          row.season,
          row.avgText,
          row.obpText,
          row.slgText,
          row.opsText,
          row.hr,
          row.bbkText,
          row.warText,
        ]),
      },
      advanced: {
        headers: ["시즌", "하드힛%", "배럴%", "존컨택%", "헛스윙%", "BABIP", "ISO", "wRC+"],
        rows: config.advancedRows,
      },
      value: {
        headers: ["시즌", "WAR", "공격RAA", "주루RAA", "수비RAA", "수비율", "포지션"],
        rows: config.valueRows,
      },
    },
    ...config,
  };
}

function makePitcher(config) {
  return {
    type: "pitcher",
    chartMetrics: pitcherChartMetrics,
    leagueContext:
      config.roleGroup === "선발"
        ? "선발 투수 그룹 기준 대표 지표 5개 백분위"
        : "불펜 투수 그룹 기준 대표 지표 5개 백분위",
    detailContext: "구위, 제구, 타구 억제 관련 서번트형 지표",
    metrics: [
      ["방어율", config.current.era, config.notes.era],
      ["이닝", config.current.ip, config.notes.ip],
      ["WHIP", config.current.whip, config.notes.whip],
      ["탈삼진", config.current.so, config.notes.so],
      ["K/BB", config.current.kbb, config.notes.kbb],
      ["WAR", config.current.war, config.notes.war],
    ],
    tables: {
      basic: {
        headers: ["시즌", "방어율", "이닝", "WHIP", "탈삼진", "K/BB", "WAR"],
        rows: config.seasons.map((row) => [
          row.season,
          row.eraText,
          row.ipText,
          row.whipText,
          row.so,
          row.kbbText,
          row.warText,
        ]),
      },
      advanced: {
        headers: ["시즌", "평균구속", "헛스윙%", "CSW%", "피장타율", "피OPS", "구종가치"],
        rows: config.advancedRows,
      },
      value: {
        headers: ["시즌", "WAR", "역할RAA", "잔루율", "GB%", "QS/SV", "역할"],
        rows: config.valueRows,
      },
    },
    ...config,
  };
}

const players = [
  makePitcher({
    name: "박영현",
    team: "kt wiz",
    position: "마무리 투수",
    positionGroup: "불펜/마무리 투수",
    roleGroup: "불펜",
    number: "60",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "강한 구위와 높은 삼진 생산을 바탕으로 경기 후반을 닫는 마무리 투수 유형입니다. 불펜 기준으로는 방어율보다 WHIP, K/BB, 헛스윙률을 함께 봐야 안정성을 더 잘 설명할 수 있습니다.",
    current: { era: "2.18", ip: "33.0", whip: "1.02", so: "42", kbb: "4.20", war: "1.4" },
    notes: {
      era: "불펜 상위권",
      ip: "고부하",
      whip: "주자 억제",
      so: "강점",
      kbb: "제구 안정",
      war: "구원 가치",
    },
    league: [
      ["방어율", 86],
      ["이닝 소화율", 91],
      ["WHIP", 84],
      ["탈삼진", 88],
      ["K/BB", 82],
    ],
    servant: [
      ["평균 구속", "149.2km", "상위 82%"],
      ["최고 구속", "153.1km", "상위 88%"],
      ["회전수", "2,380rpm", "상위 74%"],
      ["익스텐션", "6.4ft", "상위 69%"],
      ["수직 무브먼트", "+14.8in", "상위 71%"],
      ["수평 무브먼트", "8.2in", "평균 이상"],
      ["헛스윙률", "31.4%", "상위 86%"],
      ["존 진입률", "51.8%", "안정"],
      ["하드힛 허용", "31.0%", "억제 양호"],
    ],
    insights: [
      "마무리 투수는 선발처럼 이닝을 길게 먹기보다 짧은 구간의 실점 억제와 삼진 생산이 핵심입니다.",
      "현재 샘플 해석에서는 WHIP와 K/BB가 함께 좋아 주자를 많이 쌓지 않는 유형으로 볼 수 있습니다.",
      "불펜 기준 백분위로 따로 봐야 선발 투수와 비교하는 왜곡을 줄일 수 있습니다.",
    ],
    detailInsights: [
      "평균 구속과 헛스윙률이 같이 높으면 단순히 빠른 공이 아니라 타자의 스윙을 실제로 끌어내는 구위로 해석할 수 있습니다.",
      "존 진입률이 무너지지 않으면서 K/BB가 유지되면, 강한 구위가 볼넷 증가로 상쇄되지 않는다는 점이 중요합니다.",
      "하드힛 허용이 낮다면 맞더라도 강한 타구를 줄이는 쪽으로 실점 위험을 낮추고 있다고 볼 수 있습니다.",
    ],
    seasons: [
      { season: "2023", era: 2.75, eraText: "2.75", ip: 75.1, ipText: "75.1", whip: 1.12, whipText: "1.12", so: 79, kbb: 3.2, kbbText: "3.20", war: 1.8, warText: "1.8" },
      { season: "2024", era: 2.52, eraText: "2.52", ip: 68.0, ipText: "68.0", whip: 1.08, whipText: "1.08", so: 72, kbb: 3.7, kbbText: "3.70", war: 1.9, warText: "1.9" },
      { season: "2025", era: 2.18, eraText: "2.18", ip: 33.0, ipText: "33.0", whip: 1.02, whipText: "1.02", so: 42, kbb: 4.2, kbbText: "4.20", war: 1.4, warText: "1.4" },
    ],
    months: [
      { label: "4월", era: 2.45, ip: 10.2, whip: 1.11, kbb: 3.6, war: 0.3 },
      { label: "5월", era: 1.98, ip: 11.0, whip: 0.96, kbb: 4.5, war: 0.5 },
      { label: "6월", era: 2.10, ip: 11.1, whip: 1.01, kbb: 4.4, war: 0.6 },
    ],
    advancedRows: [["2025", "149.2km", "31.4%", "32.8%", ".332", ".621", "+7.5"]],
    valueRows: [["2025", "1.4", "+8.2", "78.4%", "43.1%", "18SV", "마무리"]],
  }),
  makePitcher({
    name: "소형준",
    team: "kt wiz",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "30",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "선발 투수로서 경기 초반부터 중반까지 이닝을 소화하며 팀 불펜 부담을 줄이는 유형입니다. 선발 기준에서는 방어율과 WHIP뿐 아니라 이닝 소화율과 K/BB를 함께 봐야 합니다.",
    current: { era: "3.62", ip: "72.1", whip: "1.28", so: "54", kbb: "2.57", war: "1.6" },
    notes: { era: "평균 이상", ip: "선발 핵심", whip: "관리 필요", so: "중간", kbb: "안정권", war: "누적 가치" },
    league: [["방어율", 67], ["이닝 소화율", 78], ["WHIP", 58], ["탈삼진", 52], ["K/BB", 63]],
    servant: [
      ["평균 구속", "144.5km", "평균 이상"],
      ["체인지업 낙폭", "33.4in", "강점"],
      ["커브 회전수", "2,620rpm", "상위 77%"],
      ["익스텐션", "6.1ft", "평균"],
      ["땅볼 유도", "48.8%", "상위 70%"],
      ["헛스윙률", "23.6%", "보통"],
      ["존 진입률", "50.2%", "안정"],
      ["초구 스트라이크", "62.0%", "강점"],
      ["하드힛 허용", "36.5%", "관리"],
    ],
    insights: [
      "선발 투수는 실점 억제와 이닝 소화가 동시에 중요합니다.",
      "탈삼진이 압도적이지 않아도 땅볼 유도와 볼넷 억제가 좋으면 긴 이닝 운영이 가능합니다.",
      "WHIP가 높아지는 구간은 실점보다 먼저 위험 신호로 볼 수 있습니다.",
    ],
    detailInsights: [
      "체인지업 낙폭과 커브 회전수가 좋으면 구속 자체보다 타이밍 교란에 강점이 있는 투수로 해석할 수 있습니다.",
      "땅볼 유도율이 높은 선발은 수비와 병살 기회에 영향을 받으므로 내야 수비와 함께 봐야 합니다.",
      "초구 스트라이크 비율이 높으면 긴 승부를 줄이고 이닝 소화에 유리합니다.",
    ],
    seasons: [
      { season: "2023", era: 3.86, eraText: "3.86", ip: 81.2, ipText: "81.2", whip: 1.32, whipText: "1.32", so: 58, kbb: 2.23, kbbText: "2.23", war: 1.4, warText: "1.4" },
      { season: "2024", era: 3.74, eraText: "3.74", ip: 103.0, ipText: "103.0", whip: 1.30, whipText: "1.30", so: 77, kbb: 2.41, kbbText: "2.41", war: 1.9, warText: "1.9" },
      { season: "2025", era: 3.62, eraText: "3.62", ip: 72.1, ipText: "72.1", whip: 1.28, whipText: "1.28", so: 54, kbb: 2.57, kbbText: "2.57", war: 1.6, warText: "1.6" },
    ],
    months: [
      { label: "4월", era: 4.05, ip: 24.0, whip: 1.34, kbb: 2.1, war: 0.4 },
      { label: "5월", era: 3.44, ip: 27.1, whip: 1.22, kbb: 2.8, war: 0.7 },
      { label: "6월", era: 3.36, ip: 21.0, whip: 1.25, kbb: 2.9, war: 0.5 },
    ],
    advancedRows: [["2025", "144.5km", "23.6%", "29.1%", ".398", ".712", "+3.2"]],
    valueRows: [["2025", "1.6", "+7.1", "71.8%", "48.8%", "6QS", "선발"]],
  }),
  makeHitter({
    name: "최원준",
    team: "kt wiz",
    position: "외야수",
    positionGroup: "외야수",
    number: "16",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "컨택과 주루, 외야 수비를 함께 보는 선수입니다. 장타 중심 타자와 비교하기보다 출루, 주루, 수비 가치가 합쳐지는 방식으로 평가해야 합니다.",
    current: { avg: ".291", obp: ".361", slg: ".403", ops: ".764", bbk: "0.62", war: "1.7" },
    notes: { avg: "컨택", obp: "상위권 근접", slg: "보완", ops: "평균 이상", bbk: "안정", war: "종합 가치" },
    league: [["타율", 68], ["출루율", 65], ["장타율", 48], ["OPS", 57], ["볼삼비", 70]],
    servant: [
      ["평균 타구속도", "87.6mph", "평균"],
      ["최고 타구속도", "108.2mph", "평균 이상"],
      ["하드힛%", "34.8%", "보통"],
      ["배럴%", "5.1%", "보완"],
      ["발사각", "11.6도", "라인드라이브형"],
      ["스위트스팟%", "35.0%", "양호"],
      ["존 컨택%", "87.4%", "강점"],
      ["헛스윙%", "18.2%", "낮음"],
      ["추격 스윙%", "27.9%", "관리"],
    ],
    insights: [
      "OPS만 보면 아주 강한 장타자는 아니지만 출루와 수비 가치를 더하면 역할이 달라집니다.",
      "볼삼비가 안정적이면 타석에서 쉽게 무너지지 않는 장점으로 볼 수 있습니다.",
      "외야수는 타격 외에도 주루와 수비 기여를 함께 봐야 합니다.",
    ],
    detailInsights: [
      "존 컨택률이 높고 헛스윙률이 낮으면 공을 맞히는 능력이 강점입니다.",
      "배럴 비율이 낮으면 장타율 상승을 위해 발사각이나 강한 타구 비율 개선이 필요합니다.",
      "수비와 주루 가치가 WAR에 반영되므로 단순 OPS 비교보다 종합 가치 표가 중요합니다.",
    ],
    seasons: [
      { season: "2023", avg: .284, avgText: ".284", obp: .349, obpText: ".349", slg: .386, slgText: ".386", ops: .735, opsText: ".735", hr: 4, bbk: .55, bbkText: "0.55", war: 1.3, warText: "1.3" },
      { season: "2024", avg: .288, avgText: ".288", obp: .356, obpText: ".356", slg: .394, slgText: ".394", ops: .750, opsText: ".750", hr: 5, bbk: .59, bbkText: "0.59", war: 1.5, warText: "1.5" },
      { season: "2025", avg: .291, avgText: ".291", obp: .361, obpText: ".361", slg: .403, slgText: ".403", ops: .764, opsText: ".764", hr: 6, bbk: .62, bbkText: "0.62", war: 1.7, warText: "1.7" },
    ],
    months: [
      { label: "4월", avg: .276, obp: .344, slg: .382, ops: .726, war: .3 },
      { label: "5월", avg: .303, obp: .372, slg: .414, ops: .786, war: .6 },
      { label: "6월", avg: .294, obp: .364, slg: .411, ops: .775, war: .5 },
    ],
    advancedRows: [["2025", "34.8%", "5.1%", "87.4%", "18.2%", ".318", ".112", "111"]],
    valueRows: [["2025", "1.7", "+5.3", "+1.7", "+2.0", ".988", "외야수"]],
  }),
  makeHitter({
    name: "안현민",
    team: "kt wiz",
    position: "외야수",
    positionGroup: "외야수",
    number: "44",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "강한 타구와 장타 잠재력을 우선 확인해야 하는 외야수 유형입니다. 표본이 작을수록 타율보다 타구 질과 삼진/볼넷 흐름을 같이 봐야 합니다.",
    current: { avg: ".318", obp: ".402", slg: ".570", ops: ".972", bbk: "0.72", war: "1.9" },
    notes: { avg: "강점", obp: "우수", slg: "핵심", ops: "상위권", bbk: "개선", war: "상승" },
    league: [["타율", 82], ["출루율", 84], ["장타율", 91], ["OPS", 92], ["볼삼비", 74]],
    servant: [
      ["평균 타구속도", "91.2mph", "상위 86%"],
      ["최고 타구속도", "113.7mph", "상위 91%"],
      ["하드힛%", "46.8%", "상위 88%"],
      ["배럴%", "12.9%", "상위 90%"],
      ["발사각", "15.2도", "장타형"],
      ["스위트스팟%", "38.6%", "강점"],
      ["존 컨택%", "82.1%", "관리"],
      ["헛스윙%", "25.0%", "주의"],
      ["추격 스윙%", "29.4%", "관리"],
    ],
    insights: [
      "장타율과 OPS가 강점인 선수는 타율보다 강한 타구 비율을 함께 봐야 합니다.",
      "삼진이 늘더라도 하드힛과 배럴이 충분히 높으면 공격 생산성이 유지될 수 있습니다.",
      "표본이 작다면 월별 흐름으로 지속성을 확인하는 것이 중요합니다.",
    ],
    detailInsights: [
      "평균 타구속도와 배럴 비율이 모두 높으면 실제 장타율 상승을 설명하는 근거가 됩니다.",
      "존 컨택률이 평균 이하로 내려가면 장기적으로 슬럼프 위험이 커질 수 있습니다.",
      "볼삼비가 유지되면 장타형 타자로 변해도 타석 접근이 무너지지 않았다고 볼 수 있습니다.",
    ],
    seasons: [
      { season: "2023", avg: .252, avgText: ".252", obp: .323, obpText: ".323", slg: .401, slgText: ".401", ops: .724, opsText: ".724", hr: 5, bbk: .42, bbkText: "0.42", war: .4, warText: "0.4" },
      { season: "2024", avg: .286, avgText: ".286", obp: .361, obpText: ".361", slg: .492, slgText: ".492", ops: .853, opsText: ".853", hr: 11, bbk: .58, bbkText: "0.58", war: 1.1, warText: "1.1" },
      { season: "2025", avg: .318, avgText: ".318", obp: .402, obpText: ".402", slg: .570, slgText: ".570", ops: .972, opsText: ".972", hr: 14, bbk: .72, bbkText: "0.72", war: 1.9, warText: "1.9" },
    ],
    months: [
      { label: "4월", avg: .304, obp: .386, slg: .548, ops: .934, war: .5 },
      { label: "5월", avg: .333, obp: .417, slg: .602, ops: 1.019, war: .8 },
      { label: "6월", avg: .315, obp: .399, slg: .561, ops: .960, war: .6 },
    ],
    advancedRows: [["2025", "46.8%", "12.9%", "82.1%", "25.0%", ".342", ".252", "148"]],
    valueRows: [["2025", "1.9", "+13.0", "+0.2", "-0.4", ".982", "외야수"]],
  }),
  makePitcher({
    name: "원태인",
    team: "삼성 라이온즈",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "18",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "선발 투수 그룹 안에서 안정적인 이닝과 실점 억제를 같이 봐야 하는 선수입니다. 변화구 완성도와 제구가 성적 설명의 중심이 됩니다.",
    current: { era: "3.10", ip: "83.2", whip: "1.18", so: "68", kbb: "3.09", war: "2.1" },
    notes: { era: "상위권", ip: "높음", whip: "안정", so: "준수", kbb: "강점", war: "팀 기여" },
    league: [["방어율", 78], ["이닝 소화율", 84], ["WHIP", 74], ["탈삼진", 66], ["K/BB", 76]],
    servant: [
      ["평균 구속", "145.8km", "평균 이상"],
      ["슬라이더 무브먼트", "9.4in", "강점"],
      ["체인지업 낙폭", "34.0in", "강점"],
      ["익스텐션", "6.2ft", "양호"],
      ["헛스윙률", "25.8%", "평균 이상"],
      ["CSW%", "30.2%", "강점"],
      ["존 진입률", "52.6%", "안정"],
      ["하드힛 허용", "34.2%", "양호"],
      ["피장타 억제", ".370", "상위권"],
    ],
    insights: [
      "선발 기준에서는 방어율과 이닝 소화율을 같이 봐야 실제 팀 기여가 보입니다.",
      "WHIP가 안정적이면 큰 이닝을 허용할 위험을 낮추는 쪽으로 해석할 수 있습니다.",
      "K/BB가 좋으면 제구 기반의 지속 가능성이 비교적 높습니다.",
    ],
    detailInsights: [
      "CSW%가 높으면 헛스윙과 루킹 스트라이크를 모두 만들어내는 투구 설계가 좋다는 뜻입니다.",
      "변화구 무브먼트가 좋고 존 진입률이 유지되면 타자를 속이면서도 볼넷을 억제할 수 있습니다.",
      "피장타 억제가 좋으면 주자가 있는 상황에서 한 번에 실점이 커지는 위험을 낮춥니다.",
    ],
    seasons: [
      { season: "2023", era: 3.24, eraText: "3.24", ip: 151.0, ipText: "151.0", whip: 1.21, whipText: "1.21", so: 118, kbb: 2.75, kbbText: "2.75", war: 3.1, warText: "3.1" },
      { season: "2024", era: 3.18, eraText: "3.18", ip: 158.2, ipText: "158.2", whip: 1.19, whipText: "1.19", so: 126, kbb: 2.93, kbbText: "2.93", war: 3.4, warText: "3.4" },
      { season: "2025", era: 3.10, eraText: "3.10", ip: 83.2, ipText: "83.2", whip: 1.18, whipText: "1.18", so: 68, kbb: 3.09, kbbText: "3.09", war: 2.1, warText: "2.1" },
    ],
    months: [
      { label: "4월", era: 3.42, ip: 28.0, whip: 1.23, kbb: 2.8, war: .6 },
      { label: "5월", era: 2.88, ip: 31.2, whip: 1.12, kbb: 3.4, war: .9 },
      { label: "6월", era: 3.06, ip: 24.0, whip: 1.17, kbb: 3.0, war: .6 },
    ],
    advancedRows: [["2025", "145.8km", "25.8%", "30.2%", ".370", ".668", "+9.1"]],
    valueRows: [["2025", "2.1", "+10.4", "74.2%", "45.5%", "9QS", "선발"]],
  }),
  makeHitter({
    name: "박성한",
    team: "SSG 랜더스",
    position: "내야수",
    positionGroup: "내야수",
    number: "2",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "출루와 내야 수비, 안정적인 타석 운영이 핵심인 내야수입니다. 단순 장타 지표보다 출루율, 볼삼비, 수비 기여가 WAR로 어떻게 이어지는지 봐야 합니다.",
    current: { avg: ".337", obp: ".428", slg: ".455", ops: ".883", bbk: "0.91", war: "2.6" },
    notes: { avg: "상위권", obp: "핵심", slg: "준수", ops: "우수", bbk: "강점", war: "리그 상위" },
    league: [["타율", 90], ["출루율", 93], ["장타율", 66], ["OPS", 82], ["볼삼비", 88]],
    servant: [
      ["평균 타구속도", "88.4mph", "평균 이상"],
      ["최고 타구속도", "109.1mph", "양호"],
      ["하드힛%", "37.0%", "보통 이상"],
      ["배럴%", "5.8%", "평균"],
      ["발사각", "10.8도", "라인드라이브형"],
      ["스위트스팟%", "39.5%", "강점"],
      ["존 컨택%", "89.2%", "상위권"],
      ["헛스윙%", "15.4%", "낮음"],
      ["추격 스윙%", "23.7%", "우수"],
    ],
    insights: [
      "출루율과 볼삼비가 모두 좋으면 타석에서 팀 공격의 흐름을 끊지 않는 가치가 큽니다.",
      "내야수는 수비 포지션 가치가 WAR에 크게 반영되므로 타격표만 보면 과소평가될 수 있습니다.",
      "장타율이 압도적이지 않아도 출루와 수비가 합쳐지면 팀 기여도가 높습니다.",
    ],
    detailInsights: [
      "존 컨택률과 낮은 헛스윙률은 타석 안정성의 직접적인 근거입니다.",
      "추격 스윙률이 낮으면 나쁜 공에 손을 덜 대고 출루율을 끌어올릴 수 있습니다.",
      "수비RAA가 플러스라면 같은 OPS의 1루수나 지명타자보다 종합 가치는 더 높게 평가될 수 있습니다.",
    ],
    seasons: [
      { season: "2023", avg: .287, avgText: ".287", obp: .359, obpText: ".359", slg: .389, slgText: ".389", ops: .748, opsText: ".748", hr: 8, bbk: .63, bbkText: "0.63", war: 2.1, warText: "2.1" },
      { season: "2024", avg: .301, avgText: ".301", obp: .384, obpText: ".384", slg: .411, slgText: ".411", ops: .795, opsText: ".795", hr: 7, bbk: .75, bbkText: "0.75", war: 2.4, warText: "2.4" },
      { season: "2025", avg: .337, avgText: ".337", obp: .428, obpText: ".428", slg: .455, slgText: ".455", ops: .883, opsText: ".883", hr: 6, bbk: .91, bbkText: "0.91", war: 2.6, warText: "2.6" },
    ],
    months: [
      { label: "4월", avg: .318, obp: .407, slg: .430, ops: .837, war: .7 },
      { label: "5월", avg: .356, obp: .449, slg: .475, ops: .924, war: 1.0 },
      { label: "6월", avg: .332, obp: .421, slg: .459, ops: .880, war: .9 },
    ],
    advancedRows: [["2025", "37.0%", "5.8%", "89.2%", "15.4%", ".356", ".118", "139"]],
    valueRows: [["2025", "2.6", "+12.8", "+0.4", "+2.1", ".976", "내야수"]],
  }),
  makeHitter({
    name: "김주원",
    team: "NC 다이노스",
    position: "내야수",
    positionGroup: "내야수",
    number: "7",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "수비와 주루 가치가 강하게 붙는 내야수 유형입니다. 타격 생산성이 평균권이어도 수비 범위와 주루가 WAR를 끌어올릴 수 있습니다.",
    current: { avg: ".268", obp: ".349", slg: ".422", ops: ".771", bbk: "0.61", war: "2.4" },
    notes: { avg: "보완", obp: "준수", slg: "평균 이상", ops: "준수", bbk: "개선", war: "수비 포함 강점" },
    league: [["타율", 48], ["출루율", 61], ["장타율", 58], ["OPS", 60], ["볼삼비", 67]],
    servant: [
      ["평균 타구속도", "88.9mph", "평균 이상"],
      ["최고 타구속도", "110.6mph", "강점"],
      ["하드힛%", "39.8%", "양호"],
      ["배럴%", "7.1%", "평균 이상"],
      ["발사각", "14.1도", "장타 여지"],
      ["스위트스팟%", "34.7%", "평균"],
      ["존 컨택%", "81.0%", "관리"],
      ["헛스윙%", "26.1%", "주의"],
      ["추격 스윙%", "28.0%", "보통"],
    ],
    insights: [
      "타율보다 수비와 주루가 종합 가치를 크게 만든 선수로 볼 수 있습니다.",
      "장타율이 평균 이상이면 하위 타순 내야수 이상의 공격 가치를 기대할 수 있습니다.",
      "삼진과 컨택 관리가 안정되면 타격 지표가 한 단계 더 올라갈 수 있습니다.",
    ],
    detailInsights: [
      "하드힛과 배럴이 평균 이상이면 낮은 타율에도 장타 잠재력은 남아 있습니다.",
      "존 컨택률이 개선되면 출루율과 장타율이 동시에 안정될 가능성이 있습니다.",
      "수비RAA가 강점이라면 타격이 평균이어도 팀 승리에 미치는 영향은 더 크게 볼 수 있습니다.",
    ],
    seasons: [
      { season: "2023", avg: .233, avgText: ".233", obp: .320, obpText: ".320", slg: .365, slgText: ".365", ops: .685, opsText: ".685", hr: 10, bbk: .42, bbkText: "0.42", war: 1.6, warText: "1.6" },
      { season: "2024", avg: .255, avgText: ".255", obp: .338, obpText: ".338", slg: .401, slgText: ".401", ops: .739, opsText: ".739", hr: 12, bbk: .54, bbkText: "0.54", war: 2.0, warText: "2.0" },
      { season: "2025", avg: .268, avgText: ".268", obp: .349, obpText: ".349", slg: .422, slgText: ".422", ops: .771, opsText: ".771", hr: 9, bbk: .61, bbkText: "0.61", war: 2.4, warText: "2.4" },
    ],
    months: [
      { label: "4월", avg: .244, obp: .329, slg: .389, ops: .718, war: .6 },
      { label: "5월", avg: .279, obp: .361, slg: .435, ops: .796, war: .9 },
      { label: "6월", avg: .276, obp: .354, slg: .431, ops: .785, war: .8 },
    ],
    advancedRows: [["2025", "39.8%", "7.1%", "81.0%", "26.1%", ".304", ".154", "108"]],
    valueRows: [["2025", "2.4", "+4.8", "+2.7", "+6.0", ".971", "내야수"]],
  }),
  makePitcher({
    name: "김진욱",
    team: "롯데 자이언츠",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "15",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "좌완 선발로서 구위와 제구 안정성의 균형이 핵심입니다. 탈삼진 잠재력이 있어도 볼넷이 많으면 WHIP와 이닝 소화가 함께 흔들릴 수 있습니다.",
    current: { era: "4.08", ip: "61.2", whip: "1.39", so: "63", kbb: "1.97", war: "0.9" },
    notes: { era: "개선 필요", ip: "중간", whip: "관리", so: "강점", kbb: "핵심 과제", war: "상승 여지" },
    league: [["방어율", 47], ["이닝 소화율", 55], ["WHIP", 39], ["탈삼진", 72], ["K/BB", 42]],
    servant: [
      ["평균 구속", "146.2km", "양호"],
      ["슬라이더 회전수", "2,480rpm", "강점"],
      ["커브 낙폭", "45.0in", "상위권"],
      ["익스텐션", "6.0ft", "평균"],
      ["헛스윙률", "27.8%", "강점"],
      ["CSW%", "28.6%", "평균 이상"],
      ["존 진입률", "47.0%", "보완"],
      ["볼넷률", "10.8%", "주의"],
      ["하드힛 허용", "37.9%", "관리"],
    ],
    insights: [
      "탈삼진 능력은 좋지만 K/BB가 낮으면 이닝을 길게 가져가기 어렵습니다.",
      "WHIP 상승은 안타뿐 아니라 볼넷 영향도 크므로 제구 지표를 같이 봐야 합니다.",
      "선발 백분위에서 이닝 소화율이 올라가면 팀 기여도가 빠르게 좋아질 수 있습니다.",
    ],
    detailInsights: [
      "헛스윙률이 좋다는 것은 구위 자체의 가능성을 보여줍니다.",
      "존 진입률과 볼넷률이 개선되면 같은 구위로도 방어율과 WHIP가 함께 낮아질 수 있습니다.",
      "변화구 낙폭이 강점이면 카운트 유리 상황을 얼마나 자주 만드는지가 중요합니다.",
    ],
    seasons: [
      { season: "2023", era: 4.96, eraText: "4.96", ip: 44.0, ipText: "44.0", whip: 1.55, whipText: "1.55", so: 49, kbb: 1.48, kbbText: "1.48", war: .2, warText: "0.2" },
      { season: "2024", era: 4.42, eraText: "4.42", ip: 72.1, ipText: "72.1", whip: 1.46, whipText: "1.46", so: 74, kbb: 1.74, kbbText: "1.74", war: .6, warText: "0.6" },
      { season: "2025", era: 4.08, eraText: "4.08", ip: 61.2, ipText: "61.2", whip: 1.39, whipText: "1.39", so: 63, kbb: 1.97, kbbText: "1.97", war: .9, warText: "0.9" },
    ],
    months: [
      { label: "4월", era: 4.72, ip: 19.0, whip: 1.52, kbb: 1.5, war: .1 },
      { label: "5월", era: 3.88, ip: 23.2, whip: 1.31, kbb: 2.2, war: .5 },
      { label: "6월", era: 3.96, ip: 19.0, whip: 1.36, kbb: 2.1, war: .3 },
    ],
    advancedRows: [["2025", "146.2km", "27.8%", "28.6%", ".418", ".744", "+1.4"]],
    valueRows: [["2025", "0.9", "+2.6", "67.5%", "42.2%", "3QS", "선발"]],
  }),
  makeHitter({
    name: "김도영",
    team: "KIA 타이거즈",
    position: "내야수",
    positionGroup: "내야수",
    number: "5",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "장타, 주루, 수비 가치가 모두 붙는 스타형 내야수입니다. OPS와 WAR를 함께 보면 단순 타격 생산을 넘어 팀 승리에 미치는 폭을 더 잘 볼 수 있습니다.",
    current: { avg: ".321", obp: ".397", slg: ".589", ops: ".986", bbk: "0.58", war: "2.4" },
    notes: { avg: "상위권", obp: "우수", slg: "최상위", ops: "핵심", bbk: "관리", war: "높음" },
    league: [["타율", 84], ["출루율", 80], ["장타율", 94], ["OPS", 93], ["볼삼비", 62]],
    servant: [
      ["평균 타구속도", "90.8mph", "상위 82%"],
      ["최고 타구속도", "114.0mph", "상위 92%"],
      ["하드힛%", "45.2%", "상위 85%"],
      ["배럴%", "13.1%", "상위 91%"],
      ["발사각", "16.4도", "장타형"],
      ["스위트스팟%", "37.8%", "강점"],
      ["존 컨택%", "83.5%", "평균 이상"],
      ["헛스윙%", "23.8%", "관리"],
      ["추격 스윙%", "27.2%", "보통"],
    ],
    insights: [
      "OPS 상승은 타율보다 장타율 상승의 영향을 크게 받을 수 있습니다.",
      "장타와 주루가 함께 붙으면 단순 중심타자보다 공격 전반에 영향을 줍니다.",
      "내야 수비 가치가 플러스라면 같은 OPS의 코너 포지션 선수보다 WAR가 더 높아질 수 있습니다.",
    ],
    detailInsights: [
      "배럴 비율과 최고 타구속도가 모두 높으면 홈런과 2루타 증가를 설명하는 강한 근거가 됩니다.",
      "헛스윙률이 과하게 오르지 않으면 장타를 늘리면서도 생산성을 유지하는 좋은 변화로 볼 수 있습니다.",
      "주루RAA가 플러스라면 출루 이후에도 팀 득점 기대값을 끌어올리는 선수로 해석할 수 있습니다.",
    ],
    seasons: [
      { season: "2023", avg: .303, avgText: ".303", obp: .371, obpText: ".371", slg: .453, slgText: ".453", ops: .824, opsText: ".824", hr: 12, bbk: .48, bbkText: "0.48", war: 2.1, warText: "2.1" },
      { season: "2024", avg: .336, avgText: ".336", obp: .412, obpText: ".412", slg: .557, slgText: ".557", ops: .969, opsText: ".969", hr: 28, bbk: .55, bbkText: "0.55", war: 5.1, warText: "5.1" },
      { season: "2025", avg: .321, avgText: ".321", obp: .397, obpText: ".397", slg: .589, slgText: ".589", ops: .986, opsText: ".986", hr: 13, bbk: .58, bbkText: "0.58", war: 2.4, warText: "2.4" },
    ],
    months: [
      { label: "4월", avg: .306, obp: .382, slg: .551, ops: .933, war: .6 },
      { label: "5월", avg: .333, obp: .406, slg: .608, ops: 1.014, war: 1.0 },
      { label: "6월", avg: .326, obp: .402, slg: .601, ops: 1.003, war: .8 },
    ],
    advancedRows: [["2025", "45.2%", "13.1%", "83.5%", "23.8%", ".342", ".268", "151"]],
    valueRows: [["2025", "2.4", "+13.4", "+1.4", "+2.8", ".974", "내야수"]],
  }),
  makeHitter({
    name: "심우준",
    team: "한화 이글스",
    position: "내야수",
    positionGroup: "내야수",
    number: "6",
    dataStatus: "데모 데이터 · 실제 기록 연결 전",
    summary:
      "수비와 주루 가치가 핵심인 내야수입니다. 타격 생산성은 보완 영역이지만 수비 안정성과 주루 기여가 팀 운영에 영향을 줄 수 있습니다.",
    current: { avg: ".251", obp: ".322", slg: ".337", ops: ".659", bbk: "0.47", war: "1.1" },
    notes: { avg: "보완", obp: "보통", slg: "낮음", ops: "관리", bbk: "개선 필요", war: "수비 기여" },
    league: [["타율", 38], ["출루율", 42], ["장타율", 28], ["OPS", 31], ["볼삼비", 45]],
    servant: [
      ["평균 타구속도", "84.9mph", "낮음"],
      ["최고 타구속도", "104.4mph", "보통"],
      ["하드힛%", "27.6%", "보완"],
      ["배럴%", "2.8%", "낮음"],
      ["발사각", "8.4도", "땅볼형"],
      ["스위트스팟%", "31.0%", "보통"],
      ["존 컨택%", "86.0%", "양호"],
      ["헛스윙%", "17.6%", "낮음"],
      ["추격 스윙%", "30.8%", "관리"],
    ],
    insights: [
      "장타 생산보다 수비와 주루에서 가치를 찾는 선수로 봐야 합니다.",
      "타격 개선의 1차 목표는 장타율보다 출루율 안정일 가능성이 높습니다.",
      "수비 위치 가치가 높기 때문에 WAR 표에서 수비 기여를 별도로 확인해야 합니다.",
    ],
    detailInsights: [
      "낮은 헛스윙률은 공을 맞히는 능력을 보여주지만, 하드힛 비율이 낮으면 생산성으로 이어지기 어렵습니다.",
      "추격 스윙률을 줄이면 출루율 개선 여지가 있습니다.",
      "수비RAA가 플러스라면 낮은 OPS 일부를 종합 가치에서 보완할 수 있습니다.",
    ],
    seasons: [
      { season: "2023", avg: .239, avgText: ".239", obp: .309, obpText: ".309", slg: .310, slgText: ".310", ops: .619, opsText: ".619", hr: 2, bbk: .39, bbkText: "0.39", war: .7, warText: "0.7" },
      { season: "2024", avg: .246, avgText: ".246", obp: .316, obpText: ".316", slg: .328, slgText: ".328", ops: .644, opsText: ".644", hr: 3, bbk: .43, bbkText: "0.43", war: .9, warText: "0.9" },
      { season: "2025", avg: .251, avgText: ".251", obp: .322, obpText: ".322", slg: .337, slgText: ".337", ops: .659, opsText: ".659", hr: 3, bbk: .47, bbkText: "0.47", war: 1.1, warText: "1.1" },
    ],
    months: [
      { label: "4월", avg: .228, obp: .304, slg: .301, ops: .605, war: .2 },
      { label: "5월", avg: .260, obp: .330, slg: .352, ops: .682, war: .5 },
      { label: "6월", avg: .266, obp: .334, slg: .359, ops: .693, war: .4 },
    ],
    advancedRows: [["2025", "27.6%", "2.8%", "86.0%", "17.6%", ".292", ".086", "82"]],
    valueRows: [["2025", "1.1", "-3.2", "+1.5", "+5.0", ".978", "내야수"]],
  }),
];

const searchInput = document.querySelector("#searchInput");
const teamFilter = document.querySelector("#teamFilter");
const positionFilter = document.querySelector("#positionFilter");
const playerSelect = document.querySelector("#playerSelect");
const playerName = document.querySelector("#playerName");
const teamLine = document.querySelector("#teamLine");
const summaryText = document.querySelector("#summaryText");
const uniformNumber = document.querySelector("#uniformNumber");
const metricGrid = document.querySelector("#metricGrid");
const leagueBars = document.querySelector("#leagueBars");
const insightList = document.querySelector("#insightList");
const detailToggle = document.querySelector("#detailToggle");
const detailSection = document.querySelector("#detailSection");
const servantGrid = document.querySelector("#servantGrid");
const detailInsightList = document.querySelector("#detailInsightList");
const trendMode = document.querySelector("#trendMode");
const metricSelect = document.querySelector("#metricSelect");
const trendChart = document.querySelector("#trendChart");
const statHead = document.querySelector("#statHead");
const statRows = document.querySelector("#statRows");
const leagueContext = document.querySelector("#leagueContext");
const detailContext = document.querySelector("#detailContext");
const dataBadge = document.querySelector("#dataBadge");
const tableContext = document.querySelector("#tableContext");

let currentPlayer = players[0];
let currentTable = "basic";

function unique(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b, "ko"));
}

function optionList(select, values, selected) {
  select.innerHTML = values.map((value) => `<option value="${value}">${value}</option>`).join("");
  select.value = values.includes(selected) ? selected : values[0];
}

function matchesSearch(player) {
  const keyword = searchInput.value.trim().toLowerCase();
  if (!keyword) return true;
  return `${player.name} ${player.team} ${player.position}`.toLowerCase().includes(keyword);
}

function filteredPlayers() {
  const team = teamFilter.value || ALL_TEAMS;
  const position = positionFilter.value || ALL_POSITIONS;

  return players.filter((player) => {
    const teamOk = team === ALL_TEAMS || player.team === team;
    const positionOk = position === ALL_POSITIONS || player.positionGroup === position;
    return matchesSearch(player) && teamOk && positionOk;
  });
}

function refreshFilters() {
  const selectedTeam = teamFilter.value || ALL_TEAMS;
  const selectedPosition = positionFilter.value || ALL_POSITIONS;
  const selectedPlayer = playerSelect.value || currentPlayer.name;

  const teams = unique(players.filter(matchesSearch).map((player) => player.team));
  optionList(teamFilter, [ALL_TEAMS, ...teams], selectedTeam);

  const positions = unique(
    players
      .filter((player) => matchesSearch(player) && (teamFilter.value === ALL_TEAMS || player.team === teamFilter.value))
      .map((player) => player.positionGroup),
  );
  optionList(positionFilter, [ALL_POSITIONS, ...positions], selectedPosition);

  const filtered = filteredPlayers();
  playerSelect.innerHTML = filtered
    .map((player) => `<option value="${player.name}">${player.name}</option>`)
    .join("");

  if (filtered.some((player) => player.name === selectedPlayer)) {
    playerSelect.value = selectedPlayer;
  } else if (filtered.length > 0) {
    playerSelect.value = filtered[0].name;
  }

  if (filtered.length > 0) {
    currentPlayer = filtered.find((player) => player.name === playerSelect.value) || filtered[0];
    renderPlayer(currentPlayer);
  } else {
    renderEmpty();
  }
}

function formatTrendValue(key, value) {
  if (["avg", "obp", "slg", "ops"].includes(key)) {
    return Number(value).toFixed(3).replace(/^0/, ".");
  }
  if (["era", "whip", "kbb", "war", "ip"].includes(key)) {
    return Number(value).toFixed(2).replace(/\.00$/, "");
  }
  return String(value);
}

function renderBars(items) {
  leagueBars.innerHTML = items
    .map(
      ([label, value]) => `
        <div class="bar-row">
          <div class="bar-label">
            <span>${label}</span>
            <strong>${value} 백분위</strong>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${value}%"></div>
          </div>
        </div>
      `,
    )
    .join("");
}

function renderTrend(player) {
  const key = metricSelect.value;
  const items = trendMode.value === "season" ? player.seasons.map((row) => ({ ...row, label: row.season })) : player.months;
  const values = items.map((item) => Number(item[key]));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  trendChart.innerHTML = items
    .map((item) => {
      const value = Number(item[key]);
      const height = Math.max(14, ((value - min) / range) * 88 + 12);
      return `
        <div class="chart-bar">
          <span class="value">${formatTrendValue(key, value)}</span>
          <span class="column" style="height: ${height}%"></span>
          <span>${item.label}</span>
        </div>
      `;
    })
    .join("");
}

function renderTable(player) {
  const table = player.tables[currentTable];
  statHead.innerHTML = `<tr>${table.headers.map((header) => `<th>${header}</th>`).join("")}</tr>`;
  statRows.innerHTML = table.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`)
    .join("");
  tableContext.textContent =
    player.type === "hitter"
      ? "타격 기본, 세부 타격, 수비·WAR를 전환해서 봅니다."
      : "투구 기본, 세부 투구, 역할·WAR를 전환해서 봅니다.";
}

function renderPlayer(player) {
  currentPlayer = player;
  playerName.textContent = player.name;
  teamLine.textContent = `${player.team} · ${player.position}`;
  summaryText.textContent = player.summary;
  uniformNumber.textContent = player.number;
  leagueContext.textContent = player.leagueContext;
  detailContext.textContent = player.detailContext;
  dataBadge.textContent = player.dataStatus;

  metricGrid.innerHTML = player.metrics
    .map(
      ([label, value, note]) => `
        <article class="metric">
          <span>${label}</span>
          <strong>${value}</strong>
          <em>${note}</em>
        </article>
      `,
    )
    .join("");

  renderBars(player.league);
  insightList.innerHTML = player.insights.map((item) => `<li>${item}</li>`).join("");

  servantGrid.innerHTML = player.servant
    .map(
      ([label, value, note]) => `
        <article class="servant-card">
          <span>${label}</span>
          <strong>${value}</strong>
          <em>${note}</em>
        </article>
      `,
    )
    .join("");
  detailInsightList.innerHTML = player.detailInsights.map((item) => `<li>${item}</li>`).join("");

  metricSelect.innerHTML = player.chartMetrics
    .map((metric) => `<option value="${metric.key}">${metric.label}</option>`)
    .join("");

  renderTrend(player);
  renderTable(player);
}

function renderEmpty() {
  playerName.textContent = "조건에 맞는 선수가 없습니다";
  teamLine.textContent = "필터를 다시 선택해 주세요";
  summaryText.textContent = "이름, 팀명, 포지션 조건을 넓히면 선수 목록이 다시 표시됩니다.";
  uniformNumber.textContent = "-";
  metricGrid.innerHTML = "";
  leagueBars.innerHTML = "";
  insightList.innerHTML = "";
  servantGrid.innerHTML = "";
  detailInsightList.innerHTML = "";
  trendChart.innerHTML = "";
  statHead.innerHTML = "";
  statRows.innerHTML = "";
}

searchInput.addEventListener("input", refreshFilters);
teamFilter.addEventListener("change", refreshFilters);
positionFilter.addEventListener("change", refreshFilters);
playerSelect.addEventListener("change", () => {
  const nextPlayer = players.find((player) => player.name === playerSelect.value);
  if (nextPlayer) renderPlayer(nextPlayer);
});

detailToggle.addEventListener("click", () => {
  detailSection.hidden = !detailSection.hidden;
  detailToggle.textContent = detailSection.hidden ? "상세보기" : "상세닫기";
});

trendMode.addEventListener("change", () => renderTrend(currentPlayer));
metricSelect.addEventListener("change", () => renderTrend(currentPlayer));

document.querySelectorAll(".segment").forEach((button) => {
  button.addEventListener("click", () => {
    currentTable = button.dataset.table;
    document.querySelectorAll(".segment").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderTable(currentPlayer);
  });
});

refreshFilters();
