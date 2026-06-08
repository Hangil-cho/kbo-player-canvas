const ALL_TEAMS = "전체 팀";
const ALL_POSITIONS = "전체 포지션";

const monthLabels = [
  "25.07",
  "25.08",
  "25.09",
  "25.10",
  "25.11",
  "25.12",
  "26.01",
  "26.02",
  "26.03",
  "26.04",
  "26.05",
  "26.06",
];

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

const playerSeeds = [
  {
    type: "pitcher",
    name: "박영현",
    team: "kt wiz",
    position: "마무리 투수",
    positionGroup: "불펜/마무리 투수",
    roleGroup: "불펜",
    number: "60",
    summary:
      "강한 구위와 높은 삼진 생산을 바탕으로 경기 후반을 닫는 마무리 투수입니다. 불펜 기준에서는 방어율보다 WHIP, K/BB, 헛스윙률, 연투 부담을 함께 봐야 안정성을 더 잘 설명할 수 있습니다.",
    current: { era: "2.18", ip: "33.0", whip: "1.02", so: "42", kbb: "4.20", war: "1.4" },
    notes: ["불펜 상위권", "고부하", "주자 억제", "강점", "제구 안정", "구원 가치"],
    league: [["방어율", 86], ["이닝 소화율", 91], ["WHIP", 84], ["탈삼진", 88], ["K/BB", 82]],
    seasons: [
      { season: "2023", era: 2.75, ip: 75.1, whip: 1.12, so: 79, kbb: 3.2, war: 1.8 },
      { season: "2024", era: 2.52, ip: 68.0, whip: 1.08, so: 72, kbb: 3.7, war: 1.9 },
      { season: "2025", era: 2.18, ip: 33.0, whip: 1.02, so: 42, kbb: 4.2, war: 1.4 },
    ],
    monthBase: { era: 2.22, ip: 10.2, whip: 1.04, kbb: 4.1, war: 0.3 },
    advancedRows: [["2025", "149.2km", "31.4%", "32.8%", ".332", ".621", "+7.5"]],
    valueRows: [["2025", "1.4", "+8.2", "78.4%", "43.1%", "18SV", "마무리"]],
  },
  {
    type: "pitcher",
    name: "소형준",
    team: "kt wiz",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "30",
    summary:
      "선발 투수로서 경기 초반부터 중반까지 이닝을 소화하며 불펜 부담을 줄이는 유형입니다. 선발 기준에서는 방어율과 WHIP뿐 아니라 이닝 소화율과 K/BB를 함께 봐야 합니다.",
    current: { era: "3.62", ip: "72.1", whip: "1.28", so: "54", kbb: "2.57", war: "1.6" },
    notes: ["평균 이상", "선발 핵심", "관리 필요", "중간", "안정권", "누적 가치"],
    league: [["방어율", 67], ["이닝 소화율", 78], ["WHIP", 58], ["탈삼진", 52], ["K/BB", 63]],
    seasons: [
      { season: "2023", era: 3.86, ip: 81.2, whip: 1.32, so: 58, kbb: 2.23, war: 1.4 },
      { season: "2024", era: 3.74, ip: 103.0, whip: 1.3, so: 77, kbb: 2.41, war: 1.9 },
      { season: "2025", era: 3.62, ip: 72.1, whip: 1.28, so: 54, kbb: 2.57, war: 1.6 },
    ],
    monthBase: { era: 3.62, ip: 24.0, whip: 1.28, kbb: 2.6, war: 0.4 },
    advancedRows: [["2025", "144.5km", "23.6%", "29.1%", ".398", ".712", "+3.2"]],
    valueRows: [["2025", "1.6", "+7.1", "71.8%", "48.8%", "6QS", "선발"]],
  },
  {
    type: "hitter",
    name: "최원준",
    team: "kt wiz",
    position: "외야수",
    positionGroup: "외야수",
    number: "16",
    summary:
      "컨택, 주루, 외야 수비를 함께 봐야 하는 선수입니다. 장타 중심 타자와 비교하기보다 출루, 주루, 수비 가치가 합쳐지는 방식으로 평가해야 합니다.",
    current: { avg: ".291", obp: ".361", slg: ".403", ops: ".764", bbk: "0.62", war: "1.7" },
    notes: ["컨택", "상위권 근접", "보완", "평균 이상", "안정", "종합 가치"],
    league: [["타율", 68], ["출루율", 65], ["장타율", 48], ["OPS", 57], ["볼삼비", 70]],
    seasons: [
      { season: "2023", avg: .284, obp: .349, slg: .386, ops: .735, hr: 4, bbk: .55, war: 1.3 },
      { season: "2024", avg: .288, obp: .356, slg: .394, ops: .750, hr: 5, bbk: .59, war: 1.5 },
      { season: "2025", avg: .291, obp: .361, slg: .403, ops: .764, hr: 6, bbk: .62, war: 1.7 },
    ],
    monthBase: { avg: .291, obp: .361, slg: .403, ops: .764, war: .4 },
    advancedRows: [["2025", "34.8%", "5.1%", "87.4%", "18.2%", ".318", ".112", "111"]],
    valueRows: [["2025", "1.7", "+5.3", "+1.7", "+2.0", ".988", "외야수"]],
  },
  {
    type: "hitter",
    name: "안현민",
    team: "kt wiz",
    position: "외야수",
    positionGroup: "외야수",
    number: "44",
    summary:
      "강한 타구와 장타 잠재력을 우선 확인해야 하는 외야수 유형입니다. 표본이 작을수록 타율보다 타구 질과 삼진/볼넷 흐름을 같이 봐야 합니다.",
    current: { avg: ".318", obp: ".402", slg: ".570", ops: ".972", bbk: "0.72", war: "1.9" },
    notes: ["강점", "우수", "핵심", "상위권", "개선", "상승"],
    league: [["타율", 82], ["출루율", 84], ["장타율", 91], ["OPS", 92], ["볼삼비", 74]],
    seasons: [
      { season: "2023", avg: .252, obp: .323, slg: .401, ops: .724, hr: 5, bbk: .42, war: .4 },
      { season: "2024", avg: .286, obp: .361, slg: .492, ops: .853, hr: 11, bbk: .58, war: 1.1 },
      { season: "2025", avg: .318, obp: .402, slg: .570, ops: .972, hr: 14, bbk: .72, war: 1.9 },
    ],
    monthBase: { avg: .318, obp: .402, slg: .570, ops: .972, war: .5 },
    advancedRows: [["2025", "46.8%", "12.9%", "82.1%", "25.0%", ".342", ".252", "148"]],
    valueRows: [["2025", "1.9", "+13.0", "+0.2", "-0.4", ".982", "외야수"]],
  },
  {
    type: "pitcher",
    name: "원태인",
    team: "삼성 라이온즈",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "18",
    summary:
      "선발 투수 그룹 안에서 안정적인 이닝과 실점 억제를 같이 봐야 하는 선수입니다. 변화구 완성도와 제구가 성적 설명의 중심이 됩니다.",
    current: { era: "3.10", ip: "83.2", whip: "1.18", so: "68", kbb: "3.09", war: "2.1" },
    notes: ["상위권", "높음", "안정", "준수", "강점", "팀 기여"],
    league: [["방어율", 78], ["이닝 소화율", 84], ["WHIP", 74], ["탈삼진", 66], ["K/BB", 76]],
    seasons: [
      { season: "2023", era: 3.24, ip: 151.0, whip: 1.21, so: 118, kbb: 2.75, war: 3.1 },
      { season: "2024", era: 3.18, ip: 158.2, whip: 1.19, so: 126, kbb: 2.93, war: 3.4 },
      { season: "2025", era: 3.10, ip: 83.2, whip: 1.18, so: 68, kbb: 3.09, war: 2.1 },
    ],
    monthBase: { era: 3.1, ip: 28.0, whip: 1.18, kbb: 3.0, war: .6 },
    advancedRows: [["2025", "145.8km", "25.8%", "30.2%", ".370", ".668", "+9.1"]],
    valueRows: [["2025", "2.1", "+10.4", "74.2%", "45.5%", "9QS", "선발"]],
  },
  {
    type: "hitter",
    name: "박성한",
    team: "SSG 랜더스",
    position: "내야수",
    positionGroup: "내야수",
    number: "2",
    summary:
      "출루와 내야 수비, 안정적인 타석 운영이 핵심인 내야수입니다. 단순 장타 지표보다 출루율, 볼삼비, 수비 기여가 WAR로 어떻게 이어지는지 봐야 합니다.",
    current: { avg: ".337", obp: ".428", slg: ".455", ops: ".883", bbk: "0.91", war: "2.6" },
    notes: ["상위권", "핵심", "준수", "우수", "강점", "리그 상위"],
    league: [["타율", 90], ["출루율", 93], ["장타율", 66], ["OPS", 82], ["볼삼비", 88]],
    seasons: [
      { season: "2023", avg: .287, obp: .359, slg: .389, ops: .748, hr: 8, bbk: .63, war: 2.1 },
      { season: "2024", avg: .301, obp: .384, slg: .411, ops: .795, hr: 7, bbk: .75, war: 2.4 },
      { season: "2025", avg: .337, obp: .428, slg: .455, ops: .883, hr: 6, bbk: .91, war: 2.6 },
    ],
    monthBase: { avg: .337, obp: .428, slg: .455, ops: .883, war: .8 },
    advancedRows: [["2025", "37.0%", "5.8%", "89.2%", "15.4%", ".356", ".118", "139"]],
    valueRows: [["2025", "2.6", "+12.8", "+0.4", "+2.1", ".976", "내야수"]],
  },
  {
    type: "hitter",
    name: "김주원",
    team: "NC 다이노스",
    position: "내야수",
    positionGroup: "내야수",
    number: "7",
    summary:
      "수비와 주루 가치가 강하게 붙는 내야수 유형입니다. 타격 생산성이 평균권이어도 수비 범위와 주루가 WAR를 끌어올릴 수 있습니다.",
    current: { avg: ".268", obp: ".349", slg: ".422", ops: ".771", bbk: "0.61", war: "2.4" },
    notes: ["보완", "준수", "평균 이상", "준수", "개선", "수비 포함 강점"],
    league: [["타율", 48], ["출루율", 61], ["장타율", 58], ["OPS", 60], ["볼삼비", 67]],
    seasons: [
      { season: "2023", avg: .233, obp: .320, slg: .365, ops: .685, hr: 10, bbk: .42, war: 1.6 },
      { season: "2024", avg: .255, obp: .338, slg: .401, ops: .739, hr: 12, bbk: .54, war: 2.0 },
      { season: "2025", avg: .268, obp: .349, slg: .422, ops: .771, hr: 9, bbk: .61, war: 2.4 },
    ],
    monthBase: { avg: .268, obp: .349, slg: .422, ops: .771, war: .7 },
    advancedRows: [["2025", "39.8%", "7.1%", "81.0%", "26.1%", ".304", ".154", "108"]],
    valueRows: [["2025", "2.4", "+4.8", "+2.7", "+6.0", ".971", "내야수"]],
  },
  {
    type: "pitcher",
    name: "김진욱",
    team: "롯데 자이언츠",
    position: "선발 투수",
    positionGroup: "선발 투수",
    roleGroup: "선발",
    number: "15",
    summary:
      "좌완 선발로서 구위와 제구 안정성의 균형이 핵심입니다. 탈삼진 잠재력이 있어도 볼넷이 많으면 WHIP와 이닝 소화가 함께 흔들릴 수 있습니다.",
    current: { era: "4.08", ip: "61.2", whip: "1.39", so: "63", kbb: "1.97", war: "0.9" },
    notes: ["개선 필요", "중간", "관리", "강점", "핵심 과제", "상승 여지"],
    league: [["방어율", 47], ["이닝 소화율", 55], ["WHIP", 39], ["탈삼진", 72], ["K/BB", 42]],
    seasons: [
      { season: "2023", era: 4.96, ip: 44.0, whip: 1.55, so: 49, kbb: 1.48, war: .2 },
      { season: "2024", era: 4.42, ip: 72.1, whip: 1.46, so: 74, kbb: 1.74, war: .6 },
      { season: "2025", era: 4.08, ip: 61.2, whip: 1.39, so: 63, kbb: 1.97, war: .9 },
    ],
    monthBase: { era: 4.08, ip: 20.1, whip: 1.39, kbb: 2.0, war: .25 },
    advancedRows: [["2025", "146.2km", "27.8%", "28.6%", ".418", ".744", "+1.4"]],
    valueRows: [["2025", "0.9", "+2.6", "67.5%", "42.2%", "3QS", "선발"]],
  },
  {
    type: "hitter",
    name: "김도영",
    team: "KIA 타이거즈",
    position: "내야수",
    positionGroup: "내야수",
    number: "5",
    summary:
      "장타, 주루, 수비 가치가 모두 붙는 스타형 내야수입니다. OPS와 WAR를 함께 보면 단순 타격 생산을 넘어 팀 승리에 미치는 폭을 더 잘 볼 수 있습니다.",
    current: { avg: ".321", obp: ".397", slg: ".589", ops: ".986", bbk: "0.58", war: "2.4" },
    notes: ["상위권", "우수", "최상위", "핵심", "관리", "높음"],
    league: [["타율", 84], ["출루율", 80], ["장타율", 94], ["OPS", 93], ["볼삼비", 62]],
    seasons: [
      { season: "2023", avg: .303, obp: .371, slg: .453, ops: .824, hr: 12, bbk: .48, war: 2.1 },
      { season: "2024", avg: .336, obp: .412, slg: .557, ops: .969, hr: 28, bbk: .55, war: 5.1 },
      { season: "2025", avg: .321, obp: .397, slg: .589, ops: .986, hr: 13, bbk: .58, war: 2.4 },
    ],
    monthBase: { avg: .321, obp: .397, slg: .589, ops: .986, war: .8 },
    advancedRows: [["2025", "45.2%", "13.1%", "83.5%", "23.8%", ".342", ".268", "151"]],
    valueRows: [["2025", "2.4", "+13.4", "+1.4", "+2.8", ".974", "내야수"]],
  },
  {
    type: "hitter",
    name: "심우준",
    team: "한화 이글스",
    position: "내야수",
    positionGroup: "내야수",
    number: "6",
    summary:
      "수비와 주루 가치가 핵심인 내야수입니다. 타격 생산성은 보완 영역이지만 수비 안정성과 주루 기여가 팀 운영에 영향을 줄 수 있습니다.",
    current: { avg: ".251", obp: ".322", slg: ".337", ops: ".659", bbk: "0.47", war: "1.1" },
    notes: ["보완", "보통", "낮음", "관리", "개선 필요", "수비 기여"],
    league: [["타율", 38], ["출루율", 42], ["장타율", 28], ["OPS", 31], ["볼삼비", 45]],
    seasons: [
      { season: "2023", avg: .239, obp: .309, slg: .310, ops: .619, hr: 2, bbk: .39, war: .7 },
      { season: "2024", avg: .246, obp: .316, slg: .328, ops: .644, hr: 3, bbk: .43, war: .9 },
      { season: "2025", avg: .251, obp: .322, slg: .337, ops: .659, hr: 3, bbk: .47, war: 1.1 },
    ],
    monthBase: { avg: .251, obp: .322, slg: .337, ops: .659, war: .3 },
    advancedRows: [["2025", "27.6%", "2.8%", "86.0%", "17.6%", ".292", ".086", "82"]],
    valueRows: [["2025", "1.1", "-3.2", "+1.5", "+5.0", ".978", "내야수"]],
  },
];

function makeMonths(base, type) {
  return monthLabels.map((label, index) => {
    const wave = Math.sin((index + 1) / 1.7) * 0.025;
    if (type === "hitter") {
      const avg = clamp(base.avg + wave, 0.150, 0.420);
      const obp = clamp(base.obp + wave * 0.9, 0.220, 0.520);
      const slg = clamp(base.slg + wave * 1.4, 0.250, 0.720);
      return {
        label,
        avg,
        obp,
        slg,
        ops: obp + slg,
        war: Math.max(0, base.war + wave * 5),
      };
    }
    return {
      label,
      era: clamp(base.era - wave * 8, 1.2, 6.8),
      ip: Math.max(0.1, base.ip + wave * 24),
      whip: clamp(base.whip - wave * 2.5, 0.75, 1.8),
      kbb: clamp(base.kbb + wave * 7, 0.4, 6.2),
      war: Math.max(0, base.war + wave * 5),
    };
  });
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function buildPlayer(seed) {
  const isHitter = seed.type === "hitter";
  const metricLabels = isHitter
    ? ["타율", "출루율", "장타율", "OPS", "볼삼비", "WAR"]
    : ["방어율", "이닝", "WHIP", "탈삼진", "K/BB", "WAR"];
  const currentValues = isHitter
    ? [seed.current.avg, seed.current.obp, seed.current.slg, seed.current.ops, seed.current.bbk, seed.current.war]
    : [seed.current.era, seed.current.ip, seed.current.whip, seed.current.so, seed.current.kbb, seed.current.war];

  return {
    ...seed,
    chartMetrics: isHitter ? hitterChartMetrics : pitcherChartMetrics,
    months: makeMonths(seed.monthBase, seed.type),
    metrics: metricLabels.map((label, index) => [label, currentValues[index], seed.notes[index]]),
    leagueContext: isHitter
      ? "타자 대표 지표 5개 기준"
      : seed.roleGroup === "선발"
        ? "선발 투수 그룹 대표 지표 5개 기준"
        : "불펜 투수 그룹 대표 지표 5개 기준",
    detailContext: isHitter ? "타격, 주루, 수비 세부 지표" : "구위, 제구, 무브먼트, 릴리스 세부 지표",
    servantGroups: isHitter ? hitterServantGroups(seed) : pitcherServantGroups(seed),
    insights: isHitter ? hitterInsights(seed) : pitcherInsights(seed),
    detailInsights: isHitter ? hitterDetailInsights(seed) : pitcherDetailInsights(seed),
    dataNeeds: isHitter ? hitterDataNeeds : pitcherDataNeeds,
    tables: isHitter ? hitterTables(seed) : pitcherTables(seed),
  };
}

function hitterServantGroups(seed) {
  return [
    {
      title: "타구 질",
      items: [
        ["평균 타구속도", seed.name === "안현민" ? "91.2mph" : seed.name === "김도영" ? "90.8mph" : "88.4mph", "강한 타구의 출발점"],
        ["최고 타구속도", seed.name === "김도영" ? "114.0mph" : "109.1mph", "장타 잠재력"],
        ["하드힛%", seed.name === "안현민" ? "46.8%" : seed.name === "심우준" ? "27.6%" : "39.8%", "강한 타구 비율"],
        ["배럴%", seed.name === "김도영" ? "13.1%" : seed.name === "심우준" ? "2.8%" : "7.1%", "장타 직결 구간"],
      ],
    },
    {
      title: "타석 접근",
      items: [
        ["존 컨택%", seed.name === "박성한" ? "89.2%" : "83.5%", "존 안 공 대응"],
        ["헛스윙%", seed.name === "박성한" ? "15.4%" : "23.8%", "스윙 미스 억제"],
        ["추격 스윙%", seed.name === "박성한" ? "23.7%" : "27.2%", "나쁜 공 참기"],
        ["P/PA", "3.92", "타석당 투구 수"],
      ],
    },
    {
      title: "주루",
      items: [
        ["도루 성공률", seed.name === "김주원" ? "93.3%" : "78.0%", "출루 후 추가 가치"],
        ["추가 진루율", "43.0%", "안타 때 한 베이스 더"],
        ["OOB", "2", "주루사 관리"],
        ["주루 RAA", seed.name === "김도영" ? "+1.4" : "+0.7", "득점 기대값 기여"],
      ],
    },
    {
      title: "수비",
      items: [
        ["주 포지션", seed.positionGroup, "수비 비교 기준"],
        ["수비율", seed.name === "심우준" ? ".978" : ".974", "실책 억제"],
        ["수비 RAA", seed.name === "김주원" ? "+6.0" : "+2.1", "범위와 처리 기여"],
        ["송구 안정", "양호", "내야/외야별 보조 판단"],
      ],
    },
  ];
}

function pitcherServantGroups(seed) {
  return [
    {
      title: "구위와 구종",
      items: [
        ["평균 구속", seed.roleGroup === "불펜" ? "149.2km" : "145.8km", "구위의 기본 체력"],
        ["최고 구속", seed.roleGroup === "불펜" ? "153.1km" : "150.0km", "위기 상황 한계치"],
        ["주 구종 수", seed.roleGroup === "선발" ? "4개" : "3개", "타순 반복 대응"],
        ["구종 가치", seed.roleGroup === "불펜" ? "+7.5" : "+4.2", "구종별 결과 가치"],
      ],
    },
    {
      title: "무브먼트와 릴리스",
      items: [
        ["수직 무브먼트", "+14.8in", "뜬공/헛스윙 영향"],
        ["수평 무브먼트", "8.2in", "배트 중심 회피"],
        ["익스텐션", seed.roleGroup === "불펜" ? "6.4ft" : "6.1ft", "타자 체감 속도"],
        ["팔각도", seed.name === "김진욱" ? "저 3/4" : "3/4", "릴리스 높이와 궤적"],
      ],
    },
    {
      title: "제구와 승부",
      items: [
        ["존 진입률", "51.8%", "스트라이크 확보"],
        ["초구 스트라이크", "62.0%", "카운트 주도"],
        ["CSW%", "30.2%", "헛스윙+루킹"],
        ["볼넷률", seed.name === "김진욱" ? "10.8%" : "7.2%", "불필요한 주자 억제"],
      ],
    },
    {
      title: "타구 억제와 내구성",
      items: [
        ["하드힛 허용", seed.name === "김진욱" ? "37.9%" : "34.2%", "강한 타구 억제"],
        ["땅볼 유도", "45.5%", "장타 억제 방식"],
        ["연투/휴식", seed.roleGroup === "불펜" ? "확인 필요" : "해당 적음", "불펜 관리 핵심"],
        ["평균 투구수", seed.roleGroup === "선발" ? "94" : "17", "역할별 부담"],
      ],
    },
  ];
}

function hitterInsights(seed) {
  return [
    `${seed.name}은 OPS만으로 보기보다 출루, 장타, 주루, 수비 가치가 어떻게 WAR로 합쳐지는지 봐야 합니다.`,
    "타율이 비슷한 선수끼리도 하드힛%, 배럴%, 볼삼비 차이에 따라 다음 달 성적 지속성이 달라질 수 있습니다.",
    "주루와 수비가 플러스라면 같은 타격 성적의 1루수나 지명타자보다 팀 승리 기여가 더 크게 계산될 수 있습니다.",
  ];
}

function pitcherInsights(seed) {
  return [
    `${seed.name}은 ${seed.roleGroup} 기준으로 비교해야 합니다. 선발과 불펜은 이닝, 피로도, 등판 상황이 완전히 다릅니다.`,
    "방어율만 보면 결과만 보게 되므로 WHIP, K/BB, 헛스윙률, 하드힛 허용을 함께 봐야 다음 성적을 설명하기 쉽습니다.",
    seed.roleGroup === "불펜"
      ? "마무리 투수는 짧은 구간의 삼진 생산과 연투 후 구위 유지가 상세 분석의 핵심입니다."
      : "선발 투수는 구종 수, 타순 반복 대응, 평균 투구수, 이닝 소화가 상세 분석의 핵심입니다.",
  ];
}

function hitterDetailInsights(seed) {
  return [
    "타자는 타격 결과뿐 아니라 타구 질, 선구안, 주루, 수비가 모두 분리되어야 실제 가치가 보입니다.",
    "하드힛%와 배럴%는 장타율 상승의 직접 근거가 되고, 존 컨택%와 추격 스윙률은 슬럼프 위험을 설명합니다.",
    "주루 RAA와 수비 RAA가 플러스라면 타격 지표가 조금 낮아도 WAR에서는 충분히 좋은 선수로 보일 수 있습니다.",
  ];
}

function pitcherDetailInsights(seed) {
  return [
    "투수는 구속 하나보다 무브먼트, 릴리스, 팔각도, 존 진입률이 같이 움직일 때 성적 변화 이유가 더 잘 보입니다.",
    "팔각도와 익스텐션은 타자의 체감 궤적을 바꾸기 때문에 같은 구속이라도 헛스윙률과 약한 타구 비율이 달라질 수 있습니다.",
    "선발은 타순 반복과 투구수, 불펜은 연투와 휴식일을 같이 봐야 역할별 성적을 공정하게 비교할 수 있습니다.",
  ];
}

const hitterDataNeeds = [
  "KBO 공식 타격 기본/세부 기록",
  "KBO 주루 기록",
  "KBO 수비 기록",
  "Statiz WAR, 공격/주루/수비 RAA",
  "가능하면 타구속도/하드힛/배럴 대체 지표",
];

const pitcherDataNeeds = [
  "KBO 공식 투수 기본/세부 기록",
  "선발/불펜 역할 분류",
  "Statiz WAR, 선발/구원 RAA",
  "구종, 구속, 헛스윙, CSW 계열 지표",
  "팔각도/릴리스/무브먼트는 공개 데이터 확인 필요",
];

function hitterTables(seed) {
  return {
    basic: {
      headers: ["시즌", "타율", "출루율", "장타율", "OPS", "홈런", "볼삼비", "WAR"],
      rows: seed.seasons.map((row) => [row.season, fmt(row.avg), fmt(row.obp), fmt(row.slg), fmt(row.ops), row.hr, row.bbk.toFixed(2), row.war.toFixed(1)]),
    },
    advanced: {
      headers: ["시즌", "하드힛%", "배럴%", "존컨택%", "헛스윙%", "BABIP", "ISO", "wRC+"],
      rows: seed.advancedRows,
    },
    value: {
      headers: ["시즌", "WAR", "공격RAA", "주루RAA", "수비RAA", "수비율", "포지션"],
      rows: seed.valueRows,
    },
  };
}

function pitcherTables(seed) {
  return {
    basic: {
      headers: ["시즌", "방어율", "이닝", "WHIP", "탈삼진", "K/BB", "WAR"],
      rows: seed.seasons.map((row) => [row.season, row.era.toFixed(2), row.ip.toFixed(1), row.whip.toFixed(2), row.so, row.kbb.toFixed(2), row.war.toFixed(1)]),
    },
    advanced: {
      headers: ["시즌", "평균구속", "헛스윙%", "CSW%", "피장타율", "피OPS", "구종가치"],
      rows: seed.advancedRows,
    },
    value: {
      headers: ["시즌", "WAR", "역할RAA", "잔루율", "GB%", "QS/SV", "역할"],
      rows: seed.valueRows,
    },
  };
}

const players = playerSeeds.map(buildPlayer);

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
const servantGroups = document.querySelector("#servantGroups");
const detailInsightList = document.querySelector("#detailInsightList");
const dataNeedList = document.querySelector("#dataNeedList");
const trendMode = document.querySelector("#trendMode");
const metricSelect = document.querySelector("#metricSelect");
const trendChart = document.querySelector("#trendChart");
const statHead = document.querySelector("#statHead");
const statRows = document.querySelector("#statRows");
const leagueContext = document.querySelector("#leagueContext");
const detailContext = document.querySelector("#detailContext");
const dataBadge = document.querySelector("#dataBadge");
const tableContext = document.querySelector("#tableContext");
const summaryView = document.querySelector("#summaryView");
const detailView = document.querySelector("#detailView");

let currentPlayer = players[0];
let currentTable = "basic";

function unique(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b, "ko"));
}

function setOptions(select, values, selected) {
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

  setOptions(teamFilter, [ALL_TEAMS, ...unique(players.filter(matchesSearch).map((player) => player.team))], selectedTeam);

  const positions = unique(
    players
      .filter((player) => matchesSearch(player) && (teamFilter.value === ALL_TEAMS || player.team === teamFilter.value))
      .map((player) => player.positionGroup),
  );
  setOptions(positionFilter, [ALL_POSITIONS, ...positions], selectedPosition);

  const filtered = filteredPlayers();
  playerSelect.innerHTML = filtered.map((player) => `<option value="${player.name}">${player.name}</option>`).join("");
  playerSelect.value = filtered.some((player) => player.name === selectedPlayer) ? selectedPlayer : filtered[0]?.name || "";

  if (filtered.length > 0) renderPlayer(filtered.find((player) => player.name === playerSelect.value) || filtered[0]);
  else renderEmpty();
}

function topPercentLabel(percentile) {
  return `상위 ${Math.max(1, 100 - Math.round(percentile))}%`;
}

function renderBars(items) {
  leagueBars.innerHTML = items
    .map(
      ([label, value]) => `
        <div class="bar-row">
          <div class="bar-label">
            <span>${label}</span>
            <strong>${topPercentLabel(value)}</strong>
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

  trendChart.style.gridTemplateColumns = `repeat(${items.length}, minmax(0, 1fr))`;
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
  statRows.innerHTML = table.rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("");
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
  dataBadge.textContent = "데모 데이터 · 실제 기록 연결 전";

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
  renderServantGroups(player);
  detailInsightList.innerHTML = player.detailInsights.map((item) => `<li>${item}</li>`).join("");
  dataNeedList.innerHTML = player.dataNeeds.map((item) => `<li>${item}</li>`).join("");

  metricSelect.innerHTML = player.chartMetrics.map((metric) => `<option value="${metric.key}">${metric.label}</option>`).join("");
  renderTrend(player);
  renderTable(player);
}

function renderServantGroups(player) {
  servantGroups.innerHTML = player.servantGroups
    .map(
      (group) => `
        <section class="servant-group">
          <h4>${group.title}</h4>
          <div class="servant-grid">
            ${group.items
              .map(
                ([label, value, note]) => `
                  <article class="servant-card">
                    <span>${label}</span>
                    <strong>${value}</strong>
                    <em>${note}</em>
                  </article>
                `,
              )
              .join("")}
          </div>
        </section>
      `,
    )
    .join("");
}

function renderEmpty() {
  playerName.textContent = "조건에 맞는 선수가 없습니다";
  teamLine.textContent = "필터를 다시 선택해 주세요";
  summaryText.textContent = "이름, 팀명, 포지션 조건을 넓히면 선수 목록이 다시 표시됩니다.";
  uniformNumber.textContent = "-";
  metricGrid.innerHTML = "";
  leagueBars.innerHTML = "";
  insightList.innerHTML = "";
  servantGroups.innerHTML = "";
  detailInsightList.innerHTML = "";
  dataNeedList.innerHTML = "";
  trendChart.innerHTML = "";
  statHead.innerHTML = "";
  statRows.innerHTML = "";
}

function formatTrendValue(key, value) {
  if (["avg", "obp", "slg", "ops"].includes(key)) return fmt(value);
  if (["era", "whip", "kbb", "war", "ip"].includes(key)) return Number(value).toFixed(2).replace(/\.00$/, "");
  return String(value);
}

function fmt(value) {
  return Number(value).toFixed(3).replace(/^0/, ".");
}

searchInput.addEventListener("input", refreshFilters);
teamFilter.addEventListener("change", refreshFilters);
positionFilter.addEventListener("change", refreshFilters);
playerSelect.addEventListener("change", () => {
  const nextPlayer = players.find((player) => player.name === playerSelect.value);
  if (nextPlayer) renderPlayer(nextPlayer);
});

document.querySelectorAll(".view-tab").forEach((button) => {
  button.addEventListener("click", () => {
    const view = button.dataset.view;
    document.querySelectorAll(".view-tab").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    summaryView.hidden = view !== "summary";
    detailView.hidden = view !== "detail";
  });
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
