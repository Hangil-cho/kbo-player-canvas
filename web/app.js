const ALL_TEAMS = "전체 팀";
const ALL_POSITIONS = "전체 포지션";
const DATA_URL = "./data/player-canvas-2026.json";

const searchInput = document.querySelector("#searchInput");
const teamFilter = document.querySelector("#teamFilter");
const positionFilter = document.querySelector("#positionFilter");
const playerSelect = document.querySelector("#playerSelect");
const playerName = document.querySelector("#playerName");
const teamLine = document.querySelector("#teamLine");
const summaryText = document.querySelector("#summaryText");
const uniformNumber = document.querySelector("#uniformNumber");
const metricGrid = document.querySelector("#metricGrid");
const leagueCards = document.querySelector("#leagueCards");
const insightList = document.querySelector("#insightList");
const servantGroups = document.querySelector("#servantGroups");
const detailInsightList = document.querySelector("#detailInsightList");
const dataNeedList = document.querySelector("#dataNeedList");
const trendMode = document.querySelector("#trendMode");
const metricSelect = document.querySelector("#metricSelect");
const trendChart = document.querySelector("#trendChart");
const statHead = document.querySelector("#statHead");
const statRows = document.querySelector("#statRows");
const detailStatHead = document.querySelector("#detailStatHead");
const detailStatRows = document.querySelector("#detailStatRows");
const leagueContext = document.querySelector("#leagueContext");
const detailContext = document.querySelector("#detailContext");
const dataBadge = document.querySelector("#dataBadge");
const tableContext = document.querySelector("#tableContext");
const detailTableContext = document.querySelector("#detailTableContext");
const summaryView = document.querySelector("#summaryView");
const detailView = document.querySelector("#detailView");

let players = [];
let currentPlayer = null;
let currentTable = "basic";

async function init() {
  document.body.dataset.view = "summary";
  renderLoading();
  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    players = payload.players || [];
    if (!players.length) throw new Error("No players in web data");
    currentPlayer = players[0];
    bindEvents();
    refreshFilters();
  } catch (error) {
    renderLoadError(error);
  }
}

function bindEvents() {
  searchInput.addEventListener("input", refreshFilters);
  teamFilter.addEventListener("change", refreshFilters);
  positionFilter.addEventListener("change", refreshFilters);
  playerSelect.addEventListener("change", () => {
    const nextPlayer = players.find((player) => player.id === playerSelect.value);
    if (nextPlayer) renderPlayer(nextPlayer);
  });

  document.querySelectorAll(".view-tab").forEach((button) => {
    button.addEventListener("click", () => {
      const view = button.dataset.view;
      document.querySelectorAll(".view-tab").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      summaryView.hidden = view !== "summary";
      detailView.hidden = view !== "detail";
      document.body.dataset.view = view;
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
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "ko"));
}

function setOptions(select, values, selected) {
  select.innerHTML = values.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join("");
  select.value = values.includes(selected) ? selected : values[0];
}

function matchesSearch(player) {
  const keyword = searchInput.value.trim().toLowerCase();
  if (!keyword) return true;
  return `${player.name} ${player.team} ${player.teamShort} ${player.position}`.toLowerCase().includes(keyword);
}

function filteredPlayers() {
  const team = teamFilter.value || ALL_TEAMS;
  const position = positionFilter.value || ALL_POSITIONS;
  return players.filter(
    (player) =>
      matchesSearch(player) &&
      (team === ALL_TEAMS || player.team === team) &&
      (position === ALL_POSITIONS || player.positionGroup === position),
  );
}

function refreshFilters() {
  const selectedTeam = teamFilter.value || ALL_TEAMS;
  const selectedPosition = positionFilter.value || ALL_POSITIONS;
  const selectedPlayerId = playerSelect.value || currentPlayer?.id;

  setOptions(teamFilter, [ALL_TEAMS, ...unique(players.filter(matchesSearch).map((player) => player.team))], selectedTeam);
  setOptions(
    positionFilter,
    [
      ALL_POSITIONS,
      ...unique(
        players
          .filter((player) => matchesSearch(player) && (teamFilter.value === ALL_TEAMS || player.team === teamFilter.value))
          .map((player) => player.positionGroup),
      ),
    ],
    selectedPosition,
  );

  const filtered = filteredPlayers();
  playerSelect.innerHTML = filtered
    .map((player) => `<option value="${escapeHtml(player.id)}">${escapeHtml(player.name)}</option>`)
    .join("");
  playerSelect.value = filtered.some((player) => player.id === selectedPlayerId) ? selectedPlayerId : filtered[0]?.id || "";

  if (filtered.length > 0) {
    renderPlayer(filtered.find((player) => player.id === playerSelect.value) || filtered[0]);
  } else {
    renderEmpty();
  }
}

function renderPlayer(player) {
  if (!player) return;
  currentPlayer = player;
  playerName.textContent = player.name;
  teamLine.textContent = `${player.team} · ${player.position}`;
  summaryText.textContent = player.summary;
  uniformNumber.textContent = player.profileCode || "KBO";
  leagueContext.textContent = player.leagueContext;
  detailContext.textContent = player.detailContext;
  dataBadge.textContent = player.dataBadge;

  metricGrid.innerHTML = player.metrics
    .map(
      (metric) =>
        `<article class="metric"><span>${escapeHtml(metric.label)}</span><strong>${escapeHtml(metric.value)}</strong><em>${escapeHtml(metric.note)}</em></article>`,
    )
    .join("");

  renderLeagueCards(player.league);
  insightList.innerHTML = player.insights.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  renderServantGroups(player);
  detailInsightList.innerHTML = player.detailInsights.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  dataNeedList.innerHTML = player.dataNeeds.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  metricSelect.innerHTML = player.chartMetrics
    .map((metric) => `<option value="${escapeHtml(metric.key)}">${escapeHtml(metric.label)}</option>`)
    .join("");
  renderTrend(player);
  renderTable(player);
  renderDetailTable(player);
}

function renderLeagueCards(items) {
  leagueCards.innerHTML = items
    .map((item) => {
      const width = Number.isFinite(Number(item.value)) ? Number(item.value) : 0;
      return `<article class="rank-card"><div class="rank-card-top"><span>${escapeHtml(item.label)}</span><strong>${escapeHtml(item.rankLabel)}</strong></div><div class="rank-value">${escapeHtml(item.rawValue)}</div><div class="bar-track"><div class="bar-fill" style="width: ${width}%"></div></div></article>`;
    })
    .join("");
}

function renderTrend(player) {
  if (!player) return;
  const key = metricSelect.value || player.chartMetrics[0]?.key;
  const items = trendMode.value === "season" ? player.seasons : player.months;
  const availableValues = items.map((item) => Number(item[key])).filter((value) => Number.isFinite(value));
  const min = Math.min(...availableValues);
  const max = Math.max(...availableValues);
  const range = Number.isFinite(max - min) && max !== min ? max - min : 1;
  trendChart.style.gridTemplateColumns = `repeat(${items.length}, minmax(0, 1fr))`;
  trendChart.innerHTML = items
    .map((item) => {
      const value = Number(item[key]);
      const hasValue = Number.isFinite(value);
      const height = hasValue ? Math.max(14, ((value - min) / range) * 88 + 12) : 8;
      return `<div class="chart-bar ${hasValue ? "" : "empty"}"><span class="value">${hasValue ? formatTrendValue(key, value) : "-"}</span><span class="column" style="height: ${height}%"></span><span>${escapeHtml(item.label || item.season || "")}</span></div>`;
    })
    .join("");
}

function renderTable(player) {
  if (!player) return;
  const table = player.tables[currentTable] || player.tables.basic;
  statHead.innerHTML = `<tr>${table.headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr>`;
  statRows.innerHTML = table.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(String(cell ?? ""))}</td>`).join("")}</tr>`)
    .join("");
  tableContext.textContent = player.type === "hitter" ? "KBO 공식 타격·주루·수비 기록" : "KBO 공식 투구·역할 기록";
}

function renderDetailTable(player) {
  if (!player) return;
  const advanced = player.tables.advanced || player.tables.basic;
  const value = player.tables.value || { headers: [], rows: [] };
  const headers = [...advanced.headers, ...value.headers.slice(1)];
  const rowCount = Math.max(advanced.rows.length, value.rows.length);
  const rows = Array.from({ length: rowCount }, (_item, index) => {
    const left = advanced.rows[index] || [];
    const right = value.rows[index] || [];
    return [...left, ...right.slice(1)];
  });
  detailStatHead.innerHTML = `<tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr>`;
  detailStatRows.innerHTML = rows
    .map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(String(cell ?? ""))}</td>`).join("")}</tr>`)
    .join("");
  detailTableContext.textContent =
    player.type === "hitter" ? "타석 접근·주루·수비 지표 연결" : "투구 결과·역할·제구 지표 연결";
}

function renderServantGroups(player) {
  servantGroups.innerHTML = player.servantGroups
    .map(
      (group) =>
        `<section class="servant-group"><h4>${escapeHtml(group.title)}</h4><div class="servant-grid">${group.items
          .map(
            (item) =>
              `<article class="servant-card"><span>${escapeHtml(item.label)}</span><strong>${escapeHtml(item.value)}</strong><em>${escapeHtml(item.note)}</em></article>`,
          )
          .join("")}</div></section>`,
    )
    .join("");
}

function renderLoading() {
  playerName.textContent = "데이터 불러오는 중";
  teamLine.textContent = "KBO 공식 기록";
  summaryText.textContent = "수집된 CSV를 변환한 JSON을 연결하고 있습니다.";
  uniformNumber.textContent = "KBO";
  dataBadge.textContent = "";
  metricGrid.innerHTML = "";
  leagueCards.innerHTML = "";
  insightList.innerHTML = "";
  servantGroups.innerHTML = "";
  detailInsightList.innerHTML = "";
  dataNeedList.innerHTML = "";
  trendChart.innerHTML = "";
  statHead.innerHTML = "";
  statRows.innerHTML = "";
  detailStatHead.innerHTML = "";
  detailStatRows.innerHTML = "";
}

function renderLoadError(error) {
  playerName.textContent = "데이터를 불러오지 못했습니다";
  teamLine.textContent = "JSON 연결 오류";
  summaryText.textContent = `web/data/player-canvas-2026.json 파일을 확인해 주세요. (${error.message})`;
  uniformNumber.textContent = "!";
}

function renderEmpty() {
  playerName.textContent = "조건에 맞는 선수가 없습니다";
  teamLine.textContent = "필터를 다시 선택해 주세요";
  summaryText.textContent = "이름, 팀명, 포지션 조건을 넓히면 선수 목록이 다시 표시됩니다.";
  uniformNumber.textContent = "-";
  metricGrid.innerHTML = "";
  leagueCards.innerHTML = "";
  insightList.innerHTML = "";
  servantGroups.innerHTML = "";
  detailInsightList.innerHTML = "";
  dataNeedList.innerHTML = "";
  trendChart.innerHTML = "";
  statHead.innerHTML = "";
  statRows.innerHTML = "";
  detailStatHead.innerHTML = "";
  detailStatRows.innerHTML = "";
}

function formatTrendValue(key, value) {
  if (["avg", "obp", "slg", "ops", "iso", "opponent_avg"].includes(key)) {
    return Number(value).toFixed(3).replace(/^0/, "");
  }
  if (["era", "whip", "hitter_bb_k", "pitcher_k_bb"].includes(key)) {
    return Number(value).toFixed(2);
  }
  return Number(value).toFixed(1).replace(/\.0$/, "");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

init();
