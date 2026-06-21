"""
Build the static JSON payload consumed by the KBO Player Canvas web app.

The input CSV files are local generated artifacts from collect_kbo_official.py.
The output JSON is committed because GitHub Pages needs it at runtime.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
WEB_DATA_DIR = PROJECT_ROOT / "web" / "data"
OUTPUT_PATH = WEB_DATA_DIR / "player-canvas-2026.json"
SEASON = 2026

LEAGUE_SOURCE_KEYS = {
    "hitter_basic1",
    "hitter_basic2",
    "hitter_detail1",
    "pitcher_basic1",
    "pitcher_basic2",
    "pitcher_detail1",
    "defense_basic",
    "runner_basic",
}

CURRENT_SOURCE_PRIORITY = {
    "player_detail_basic": 0,
    "player_detail_total": 1,
    "hitter_basic1": 2,
    "hitter_basic2": 2,
    "hitter_detail1": 2,
    "pitcher_basic1": 2,
    "pitcher_basic2": 2,
    "pitcher_detail1": 2,
    "defense_basic": 2,
    "runner_basic": 2,
}

TEAM_DISPLAY = {
    "kt wiz": "kt wiz",
    "삼성 라이온즈": "삼성 라이온즈",
    "SSG 랜더스": "SSG 랜더스",
    "NC 다이노스": "NC 다이노스",
    "롯데 자이언츠": "롯데 자이언츠",
    "KIA 타이거즈": "KIA 타이거즈",
    "한화 이글스": "한화 이글스",
}

POSITION_LABEL = {
    "pitcher": "투수",
    "infielder": "내야수",
    "outfielder": "외야수",
    "catcher": "포수",
}

ROLE_LABEL = {
    "starter": "선발 투수",
    "reliever_closer": "마무리 투수",
    "outfielder": "외야수",
    "infielder": "내야수",
}

HITTER_REP_METRICS = ["avg", "obp", "slg", "ops", "hitter_bb_k"]
PITCHER_REP_METRICS = ["era", "ip", "whip", "pitcher_strikeouts", "pitcher_k_bb"]

HITTER_CHART_METRICS = [
    ("avg", "타율"),
    ("obp", "출루율"),
    ("slg", "장타율"),
    ("ops", "OPS"),
    ("hitter_bb_k", "볼삼비"),
]
PITCHER_CHART_METRICS = [
    ("era", "방어율"),
    ("ip", "이닝"),
    ("whip", "WHIP"),
    ("pitcher_strikeouts", "탈삼진"),
    ("pitcher_k_bb", "K/BB"),
]

DERIVED_METRIC_IDS = {
    "hitter_bb_pct",
    "hitter_k_pct",
    "babip",
    "hr_pa",
    "pitcher_k_pct",
    "pitcher_bb_pct",
    "k_minus_bb_pct",
    "k9",
    "bb9",
    "h9",
    "hr9",
    "fip",
    "babip_allowed",
    "lob_pct",
    "opponent_ops",
    "ip_per_start",
}

HITTER_BASIC_TABLE = ["avg", "obp", "slg", "ops", "hits", "home_runs", "hitter_bb_k", "sb"]
PITCHER_BASIC_TABLE = ["era", "ip", "whip", "pitcher_strikeouts", "pitcher_walks", "pitcher_k_bb", "saves"]
HITTER_ADVANCED_TABLE = ["pa", "hitter_bb_pct", "hitter_k_pct", "hitter_bb_k", "pitches_per_pa", "iso", "babip", "hr_pa", "xr", "gpa"]
PITCHER_ADVANCED_TABLE = [
    "total_batters_faced",
    "pitch_count",
    "pitcher_k_pct",
    "pitcher_bb_pct",
    "k_minus_bb_pct",
    "h9",
    "hr9",
    "fip",
    "babip_allowed",
    "lob_pct",
    "opponent_ops",
]
HITTER_VALUE_TABLE = ["sb", "cs", "sb_pct", "errors", "fielding_pct", "putouts", "assists"]
PITCHER_VALUE_TABLE = ["games_pitched", "games_started", "ip_per_start", "saves", "holds", "qs", "pitcher_wins", "pitcher_losses"]


@dataclass
class DataBundle:
    metrics: pd.DataFrame
    directory: pd.DataFrame
    metric_catalog: pd.DataFrame
    monthly: pd.DataFrame
    situations: pd.DataFrame


def main() -> None:
    bundle = load_data()
    catalog = build_catalog_lookup(bundle.metric_catalog)
    league_constants = build_league_constants(bundle.metrics)
    league_lookup = build_league_lookup(bundle.metrics, bundle.metric_catalog, league_constants)
    players = [
        build_player_payload(row, bundle, catalog, league_lookup, league_constants)
        for _, row in bundle.directory.iterrows()
    ]

    payload = {
        "meta": {
            "season": SEASON,
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
            "source": "KBO official public records",
            "playerCount": len(players),
            "metricRowCount": int(len(bundle.metrics)),
        },
        "players": players,
    }

    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved {OUTPUT_PATH.relative_to(PROJECT_ROOT)} players={len(players)}")


def load_data() -> DataBundle:
    return DataBundle(
        metrics=pd.read_csv(PROCESSED_DIR / "player_metric_values.csv"),
        directory=pd.read_csv(PROCESSED_DIR / f"kbo_player_directory_{SEASON}.csv"),
        metric_catalog=pd.read_csv(PROCESSED_DIR / "metric_catalog.csv"),
        monthly=pd.read_csv(PROCESSED_DIR / f"kbo_player_monthly_records_{SEASON}.csv"),
        situations=pd.read_csv(PROCESSED_DIR / f"kbo_player_situation_records_{SEASON}.csv"),
    )


def build_catalog_lookup(catalog: pd.DataFrame) -> dict[str, dict[str, Any]]:
    return {row["metric_id"]: row.to_dict() for _, row in catalog.iterrows()}


def build_league_constants(metrics: pd.DataFrame) -> dict[str, float]:
    pivot = season_metric_pivot(metrics)
    if pivot.empty:
        return {}
    totals = {metric_id: pd.to_numeric(pivot[metric_id], errors="coerce").sum() for metric_id in pivot.columns}
    ip = totals.get("ip")
    if not ip:
        return {}
    league_era = safe_ratio(totals.get("pitcher_earned_runs"), ip, multiplier=9)
    fip_base = fip_without_constant(totals)
    constants = {}
    if league_era is not None:
        constants["league_era"] = league_era
    if league_era is not None and fip_base is not None:
        constants["fip_constant"] = league_era - fip_base
    return constants


def season_metric_pivot(metrics: pd.DataFrame) -> pd.DataFrame:
    league = metrics[
        (metrics["period_type"].eq("season"))
        & (metrics["period_value"].astype(str).eq(str(SEASON)))
        & (metrics["source_key"].isin(LEAGUE_SOURCE_KEYS))
        & (metrics["external_player_name"].notna())
    ].copy()
    if league.empty:
        return pd.DataFrame()

    return (
        league.sort_values(["external_player_name", "team", "metric_id", "source_key"])
        .drop_duplicates(["external_player_name", "team", "metric_id"])
        .pivot_table(
            index=["external_player_name", "team"],
            columns="metric_id",
            values="value",
            aggfunc="first",
        )
    )


def build_league_lookup(metrics: pd.DataFrame, catalog: pd.DataFrame, league_constants: dict[str, float]) -> dict[str, dict[str, Any]]:
    pivot = season_metric_pivot(metrics)
    if pivot.empty:
        return {}

    pivot = add_derived_metrics(pivot, league_constants)
    direction = catalog.set_index("metric_id")["rank_direction"].to_dict()
    lookup = {}
    for metric_id in pivot.columns:
        values = pd.to_numeric(pivot[metric_id], errors="coerce").dropna().tolist()
        if values:
            lookup[metric_id] = {"values": values, "direction": direction.get(metric_id, "desc")}
    return lookup


def build_player_payload(
    player: pd.Series,
    bundle: DataBundle,
    catalog: dict[str, dict[str, Any]],
    league_lookup: dict[str, dict[str, Any]],
    league_constants: dict[str, float],
) -> dict[str, Any]:
    player_id = player["player_id"]
    player_type = player["player_type"]
    metric_df = bundle.metrics[bundle.metrics["player_id"].eq(player_id)].copy()
    current = current_metric_values(metric_df, league_constants)
    seasons = build_season_values(metric_df, league_constants)
    months = build_season_month_values(metric_df, current, league_constants)
    situations = bundle.situations[bundle.situations["player_id"].eq(player_id)].copy()

    rep_metrics = HITTER_REP_METRICS if player_type == "hitter" else PITCHER_REP_METRICS
    chart_metrics = HITTER_CHART_METRICS if player_type == "hitter" else PITCHER_CHART_METRICS
    current = ensure_derived(current, league_constants)

    return {
        "id": player_id,
        "name": player["player_name"],
        "type": player_type,
        "team": TEAM_DISPLAY.get(player["team"], player["team"]),
        "teamShort": player.get("search_team", ""),
        "position": ROLE_LABEL.get(player.get("role_group", ""), POSITION_LABEL.get(player.get("position_group", ""), "")),
        "positionGroup": ROLE_LABEL.get(player.get("role_group", ""), POSITION_LABEL.get(player.get("position_group", ""), "")),
        "roleGroup": player.get("role_group", ""),
        "profileCode": f"ID {int(player['kbo_player_id'])}" if pd.notna(player.get("kbo_player_id")) else "KBO",
        "kboPlayerId": int(player["kbo_player_id"]) if pd.notna(player.get("kbo_player_id")) else None,
        "kboDetailUrl": player.get("kbo_detail_url", ""),
        "dataBadge": f"KBO 공식 기록 · {collection_date(metric_df)} 수집",
        "summary": build_summary(player, current),
        "metrics": build_metric_cards(rep_metrics, current, catalog, league_lookup),
        "league": build_league_items(rep_metrics, current, catalog, league_lookup),
        "leagueContext": "KBO 공식 공개 기록 기반 · 수집된 리그 표본 기준",
        "detailContext": "KBO 선수 상세 월별·상황별 기록 기준",
        "chartMetrics": [{"key": key, "label": label} for key, label in chart_metrics],
        "seasons": build_chart_rows(seasons, chart_metrics),
        "months": build_chart_rows(months, chart_metrics),
        "tables": build_tables(player_type, seasons, current, catalog),
        "servantGroups": build_detail_groups(player, current, situations, catalog),
        "insights": build_summary_insights(player, current, seasons, months),
        "detailInsights": build_detail_insights(player, current, situations),
        "dataNeeds": build_data_needs(player_type),
    }


def current_metric_values(metric_df: pd.DataFrame, league_constants: dict[str, float]) -> dict[str, float | None]:
    current = {}
    season_rows = metric_df[
        metric_df["period_type"].eq("season") & metric_df["period_value"].astype(str).eq(str(SEASON))
    ].copy()
    if season_rows.empty:
        return current
    season_rows["priority"] = season_rows["source_key"].map(CURRENT_SOURCE_PRIORITY).fillna(9)
    season_rows = season_rows.sort_values(["metric_id", "priority", "source_key"])
    for metric_id, rows in season_rows.groupby("metric_id"):
        current[metric_id] = first_number(rows["value"].tolist())
    return ensure_derived(current, league_constants)


def build_season_values(metric_df: pd.DataFrame, league_constants: dict[str, float]) -> list[dict[str, Any]]:
    season_rows = metric_df[
        metric_df["period_type"].eq("season")
        & metric_df["source_key"].eq("player_detail_total")
        & metric_df["period_value"].astype(str).str.fullmatch(r"\d{4}", na=False)
    ].copy()
    rows = []
    for period_value, group in season_rows.groupby("period_value"):
        values = metric_group_to_dict(group)
        values = ensure_derived(values, league_constants)
        values["season"] = int(period_value)
        values["label"] = str(period_value)
        rows.append(values)
    return sorted(rows, key=lambda item: item["season"], reverse=True)


def build_season_month_values(
    metric_df: pd.DataFrame,
    current: dict[str, Any],
    league_constants: dict[str, float],
) -> list[dict[str, Any]]:
    monthly = metric_df[metric_df["period_type"].eq("month")].copy()
    month_values = {
        period: ensure_derived(metric_group_to_dict(group), league_constants)
        for period, group in monthly.groupby("period_value")
    }

    months = []
    for month in range(1, 13):
        year = SEASON
        period = f"{year}-{month:02d}"
        values = month_values.get(period, {})
        row = {"periodValue": period, "label": f"{str(year)[-2:]}.{month:02d}", "hasData": bool(values)}
        row.update(values)
        months.append(row)

    if not any(row["hasData"] for row in months):
        row = {"periodValue": str(SEASON), "label": str(SEASON), "hasData": True}
        row.update(current)
        return [row]

    first_data_index = next(index for index, row in enumerate(months) if row["hasData"])
    last_data_index = len(months) - 1 - next(index for index, row in enumerate(reversed(months)) if row["hasData"])
    return months[first_data_index : last_data_index + 1]


def build_chart_rows(rows: list[dict[str, Any]], chart_metrics: list[tuple[str, str]]) -> list[dict[str, Any]]:
    keys = [key for key, _label in chart_metrics]
    output = []
    for row in rows:
        item = {key: row.get(key) for key in keys}
        item.update({key: row.get(key) for key in ["season", "label", "periodValue", "hasData"] if key in row})
        output.append(item)
    return output


def metric_group_to_dict(group: pd.DataFrame) -> dict[str, float | None]:
    values = {}
    for metric_id, rows in group.groupby("metric_id"):
        values[metric_id] = first_number(rows["value"].tolist())
    return values


def ensure_derived(values: dict[str, Any], league_constants: dict[str, float] | None = None) -> dict[str, Any]:
    league_constants = league_constants or {}
    values = dict(values)
    if values.get("ops") is None and values.get("obp") is not None and values.get("slg") is not None:
        values["ops"] = values["obp"] + values["slg"]
    if values.get("hitter_bb_k") is None:
        values["hitter_bb_k"] = safe_ratio(values.get("hitter_bb"), values.get("hitter_so"))
    if values.get("hitter_bb_pct") is None:
        values["hitter_bb_pct"] = safe_ratio(values.get("hitter_bb"), values.get("pa"), multiplier=100)
    if values.get("hitter_k_pct") is None:
        values["hitter_k_pct"] = safe_ratio(values.get("hitter_so"), values.get("pa"), multiplier=100)
    if values.get("hr_pa") is None:
        values["hr_pa"] = safe_ratio(values.get("home_runs"), values.get("pa"), multiplier=100)
    if values.get("babip") is None:
        values["babip"] = hitter_babip(values)
    if values.get("pitcher_k_bb") is None:
        values["pitcher_k_bb"] = safe_ratio(values.get("pitcher_strikeouts"), values.get("pitcher_walks"))
    if values.get("pitcher_k_pct") is None:
        values["pitcher_k_pct"] = safe_ratio(values.get("pitcher_strikeouts"), values.get("total_batters_faced"), multiplier=100)
    if values.get("pitcher_bb_pct") is None:
        values["pitcher_bb_pct"] = safe_ratio(values.get("pitcher_walks"), values.get("total_batters_faced"), multiplier=100)
    if values.get("k_minus_bb_pct") is None:
        values["k_minus_bb_pct"] = subtract_numbers(values.get("pitcher_k_pct"), values.get("pitcher_bb_pct"))
    if values.get("sb_pct") is None:
        attempts = none_to_zero(values.get("sb")) + none_to_zero(values.get("cs"))
        values["sb_pct"] = safe_ratio(values.get("sb"), attempts, multiplier=100)
    if values.get("k9") is None:
        values["k9"] = safe_ratio(values.get("pitcher_strikeouts"), values.get("ip"), multiplier=9)
    if values.get("bb9") is None:
        values["bb9"] = safe_ratio(values.get("pitcher_walks"), values.get("ip"), multiplier=9)
    if values.get("h9") is None:
        values["h9"] = safe_ratio(values.get("pitcher_hits_allowed"), values.get("ip"), multiplier=9)
    if values.get("hr9") is None:
        values["hr9"] = safe_ratio(values.get("pitcher_home_runs_allowed"), values.get("ip"), multiplier=9)
    if values.get("fip") is None:
        fip_base = fip_without_constant(values)
        if fip_base is not None and league_constants.get("fip_constant") is not None:
            values["fip"] = fip_base + league_constants["fip_constant"]
    if values.get("babip_allowed") is None:
        values["babip_allowed"] = pitcher_babip_allowed(values)
    if values.get("lob_pct") is None:
        values["lob_pct"] = lob_pct(values)
    if values.get("opponent_ops") is None:
        values["opponent_ops"] = opponent_ops(values)
    if values.get("ip_per_start") is None:
        values["ip_per_start"] = safe_ratio(values.get("ip"), values.get("games_started"))
    return values


def add_derived_metrics(pivot: pd.DataFrame, league_constants: dict[str, float]) -> pd.DataFrame:
    pivot = pivot.copy()
    if {"hitter_bb", "hitter_so"}.issubset(pivot.columns):
        pivot["hitter_bb_k"] = pivot["hitter_bb"] / pivot["hitter_so"].replace(0, pd.NA)
    if {"hitter_bb", "pa"}.issubset(pivot.columns):
        pivot["hitter_bb_pct"] = pivot["hitter_bb"] / pivot["pa"].replace(0, pd.NA) * 100
    if {"hitter_so", "pa"}.issubset(pivot.columns):
        pivot["hitter_k_pct"] = pivot["hitter_so"] / pivot["pa"].replace(0, pd.NA) * 100
    if {"home_runs", "pa"}.issubset(pivot.columns):
        pivot["hr_pa"] = pivot["home_runs"] / pivot["pa"].replace(0, pd.NA) * 100
    if {"hits", "home_runs", "ab", "hitter_so", "sacrifice_flies"}.issubset(pivot.columns):
        denominator = pivot["ab"] - pivot["hitter_so"] - pivot["home_runs"] + pivot["sacrifice_flies"]
        pivot["babip"] = (pivot["hits"] - pivot["home_runs"]) / denominator.replace(0, pd.NA)
    if {"pitcher_strikeouts", "pitcher_walks"}.issubset(pivot.columns):
        pivot["pitcher_k_bb"] = pivot["pitcher_strikeouts"] / pivot["pitcher_walks"].replace(0, pd.NA)
    if {"pitcher_strikeouts", "total_batters_faced"}.issubset(pivot.columns):
        pivot["pitcher_k_pct"] = pivot["pitcher_strikeouts"] / pivot["total_batters_faced"].replace(0, pd.NA) * 100
    if {"pitcher_walks", "total_batters_faced"}.issubset(pivot.columns):
        pivot["pitcher_bb_pct"] = pivot["pitcher_walks"] / pivot["total_batters_faced"].replace(0, pd.NA) * 100
    if {"pitcher_k_pct", "pitcher_bb_pct"}.issubset(pivot.columns):
        pivot["k_minus_bb_pct"] = pivot["pitcher_k_pct"] - pivot["pitcher_bb_pct"]
    if {"pitcher_hits_allowed", "ip"}.issubset(pivot.columns):
        pivot["h9"] = pivot["pitcher_hits_allowed"] / pivot["ip"].replace(0, pd.NA) * 9
    if {"pitcher_home_runs_allowed", "ip"}.issubset(pivot.columns):
        pivot["hr9"] = pivot["pitcher_home_runs_allowed"] / pivot["ip"].replace(0, pd.NA) * 9
    if {"pitcher_home_runs_allowed", "pitcher_walks", "pitcher_hbp_allowed", "pitcher_strikeouts", "ip"}.issubset(pivot.columns):
        fip_base = (
            13 * pivot["pitcher_home_runs_allowed"]
            + 3 * (pivot["pitcher_walks"] + pivot["pitcher_hbp_allowed"])
            - 2 * pivot["pitcher_strikeouts"]
        ) / pivot["ip"].replace(0, pd.NA)
        if league_constants.get("fip_constant") is not None:
            pivot["fip"] = fip_base + league_constants["fip_constant"]
    if {"pitcher_hits_allowed", "pitcher_home_runs_allowed", "total_batters_faced", "pitcher_walks", "pitcher_hbp_allowed", "pitcher_sac_allowed", "pitcher_strikeouts"}.issubset(pivot.columns):
        denominator = (
            pivot["total_batters_faced"]
            - pivot["pitcher_walks"]
            - pivot["pitcher_hbp_allowed"]
            - pivot["pitcher_sac_allowed"]
            - pivot["pitcher_strikeouts"]
            - pivot["pitcher_home_runs_allowed"]
        )
        pivot["babip_allowed"] = (pivot["pitcher_hits_allowed"] - pivot["pitcher_home_runs_allowed"]) / denominator.replace(0, pd.NA)
    if {"pitcher_hits_allowed", "pitcher_walks", "pitcher_hbp_allowed", "pitcher_runs", "pitcher_home_runs_allowed"}.issubset(pivot.columns):
        denominator = pivot["pitcher_hits_allowed"] + pivot["pitcher_walks"] + pivot["pitcher_hbp_allowed"] - 1.4 * pivot["pitcher_home_runs_allowed"]
        pivot["lob_pct"] = (pivot["pitcher_hits_allowed"] + pivot["pitcher_walks"] + pivot["pitcher_hbp_allowed"] - pivot["pitcher_runs"]) / denominator.replace(0, pd.NA) * 100
    if {
        "pitcher_hits_allowed",
        "doubles_allowed",
        "triples_allowed",
        "pitcher_home_runs_allowed",
        "pitcher_walks",
        "pitcher_hbp_allowed",
        "pitcher_sac_allowed",
        "pitcher_sf_allowed",
        "total_batters_faced",
    }.issubset(pivot.columns):
        at_bats = (
            pivot["total_batters_faced"]
            - pivot["pitcher_walks"]
            - pivot["pitcher_hbp_allowed"]
            - pivot["pitcher_sac_allowed"]
            - pivot["pitcher_sf_allowed"]
        )
        total_bases = pivot["pitcher_hits_allowed"] + pivot["doubles_allowed"] + 2 * pivot["triples_allowed"] + 3 * pivot["pitcher_home_runs_allowed"]
        opponent_obp = (
            pivot["pitcher_hits_allowed"]
            + pivot["pitcher_walks"]
            + pivot["pitcher_hbp_allowed"]
        ) / (at_bats + pivot["pitcher_walks"] + pivot["pitcher_hbp_allowed"] + pivot["pitcher_sf_allowed"]).replace(0, pd.NA)
        opponent_slg = total_bases / at_bats.replace(0, pd.NA)
        pivot["opponent_ops"] = opponent_obp + opponent_slg
    if {"ip", "games_started"}.issubset(pivot.columns):
        pivot["ip_per_start"] = pivot["ip"] / pivot["games_started"].replace(0, pd.NA)
    return pivot


def build_metric_cards(
    metric_ids: list[str],
    current: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
    league_lookup: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    cards = []
    for metric_id in metric_ids:
        info = catalog.get(metric_id, {})
        top = top_percent(current.get(metric_id), metric_id, league_lookup)
        cards.append(
            {
                "metricId": metric_id,
                "label": metric_label(metric_id, info),
                "value": format_metric(metric_id, current.get(metric_id)),
                "note": f"상위 {top}%" if top is not None else "공식 기록",
            }
        )
    return cards


def build_league_items(
    metric_ids: list[str],
    current: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
    league_lookup: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    items = []
    for metric_id in metric_ids:
        top = top_percent(current.get(metric_id), metric_id, league_lookup)
        score = None if top is None else max(4, min(100, 101 - top))
        items.append(
            {
                "metricId": metric_id,
                "label": metric_label(metric_id, catalog.get(metric_id, {})),
                "value": score,
                "rankLabel": f"상위 {top}%" if top is not None else "비교 준비중",
                "rawValue": format_metric(metric_id, current.get(metric_id)),
            }
        )
    return items


def top_percent(value: Any, metric_id: str, league_lookup: dict[str, dict[str, Any]]) -> int | None:
    if value is None or metric_id not in league_lookup:
        return None
    values = [item for item in league_lookup[metric_id]["values"] if item is not None]
    if len(values) < 5:
        return None
    direction = league_lookup[metric_id].get("direction", "desc")
    if direction == "asc":
        better_count = sum(item < value for item in values)
    else:
        better_count = sum(item > value for item in values)
    return int(max(1, min(100, round((better_count + 1) / len(values) * 100))))


def build_tables(
    player_type: str,
    seasons: list[dict[str, Any]],
    current: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if not seasons:
        seasons = [{"season": SEASON, **current}]
    if player_type == "hitter":
        return {
            "basic": table_for_metrics(seasons, HITTER_BASIC_TABLE, catalog),
            "advanced": table_for_metrics(seasons, HITTER_ADVANCED_TABLE, catalog),
            "value": table_for_metrics(seasons, HITTER_VALUE_TABLE + ["war"], catalog),
        }
    return {
        "basic": table_for_metrics(seasons, PITCHER_BASIC_TABLE, catalog),
        "advanced": table_for_metrics(seasons, PITCHER_ADVANCED_TABLE, catalog),
        "value": table_for_metrics(seasons, PITCHER_VALUE_TABLE + ["war"], catalog),
    }


def table_for_metrics(rows: list[dict[str, Any]], metric_ids: list[str], catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    headers = ["시즌"] + [metric_label(metric_id, catalog.get(metric_id, {})) for metric_id in metric_ids]
    body = []
    for row in rows:
        body.append([row.get("season", row.get("label", ""))] + [format_metric(metric_id, row.get(metric_id)) for metric_id in metric_ids])
    return {"headers": headers, "rows": body}


def build_detail_groups(
    player: pd.Series,
    current: dict[str, Any],
    situations: pd.DataFrame,
    catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if player["player_type"] == "hitter":
        return [
            detail_group("타격 결과", ["avg", "obp", "slg", "ops", "iso"], current, catalog),
            detail_group("타석 접근", ["hitter_bb_pct", "hitter_k_pct", "hitter_bb_k", "pitches_per_pa"], current, catalog),
            detail_group("장타·인플레이 대체 지표", ["extra_base_hits", "hr_pa", "babip", "ground_air_ratio"], current, catalog),
            detail_group("주루", ["sb", "cs", "sb_pct", "out_on_base"], current, catalog),
            detail_group("수비", ["errors", "fielding_pct", "putouts", "assists"], current, catalog),
            situation_group("상황별", player["player_type"], situations),
        ]
    return [
        detail_group("실점 통제", ["era", "fip", "whip", "opponent_avg", "opponent_ops"], current, catalog),
        detail_group("구위 결과", ["pitcher_k_pct", "k_minus_bb_pct", "k9", "h9", "hr9"], current, catalog),
        detail_group("인플레이·잔루", ["babip_allowed", "lob_pct", "pitcher_go_ao", "pitcher_gdp"], current, catalog),
        detail_group("역할", ["games_pitched", "games_started", "ip", "ip_per_start", "saves"], current, catalog),
        detail_group("제구", ["pitcher_bb_pct", "bb9", "wild_pitches", "balks"], current, catalog),
        situation_group("상황별", player["player_type"], situations),
    ]


def detail_group(title: str, metric_ids: list[str], current: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": title,
        "items": [
            {
                "label": metric_label(metric_id, catalog.get(metric_id, {})),
                "value": format_metric(metric_id, current.get(metric_id)),
                "note": detail_metric_note(metric_id, current.get(metric_id)),
            }
            for metric_id in metric_ids
        ],
    }


def detail_metric_note(metric_id: str, value: Any) -> str:
    if value is None:
        return "미수집"
    if metric_id in DERIVED_METRIC_IDS:
        return "공식 기록 기반 계산"
    return "KBO 공식 기록"


def situation_group(title: str, player_type: str, situations: pd.DataFrame) -> dict[str, Any]:
    items = []
    if situations.empty:
        return {"title": title, "items": [{"label": "상황별", "value": "미수집", "note": "공식 상세 기록 없음"}]}

    for group_name in ["주자상황별", "볼카운트별", "이닝별", "타순별", "투수유형별"]:
        subset = situations[situations["situation_group"].eq(group_name)].copy()
        if subset.empty:
            continue
        metric_column = "AVG" if "AVG" in subset.columns else None
        if not metric_column:
            continue
        subset[metric_column] = pd.to_numeric(subset[metric_column], errors="coerce")
        subset = subset.dropna(subset=[metric_column])
        if subset.empty:
            continue
        if player_type == "pitcher":
            row = subset.sort_values(metric_column, ascending=True).iloc[0]
            note = "피안타율 최저"
        else:
            row = subset.sort_values(metric_column, ascending=False).iloc[0]
            note = "타율 최고"
        items.append(
            {
                "label": group_name,
                "value": f"{row.get('situation_value', '')} {format_metric('avg', row[metric_column])}",
                "note": note,
            }
        )
        if len(items) == 4:
            break

    return {"title": title, "items": items or [{"label": "상황별", "value": "미수집", "note": "공식 상세 기록 없음"}]}


def build_summary(player: pd.Series, current: dict[str, Any]) -> str:
    name = player["player_name"]
    if player["player_type"] == "hitter":
        return (
            f"{name}의 현재 공식 기록은 OPS {format_metric('ops', current.get('ops'))}, "
            f"타율 {format_metric('avg', current.get('avg'))}, 출루율 {format_metric('obp', current.get('obp'))}입니다. "
            "타격 결과와 함께 주루·수비 기록을 같이 보도록 연결했습니다."
        )
    return (
        f"{name}의 현재 공식 기록은 ERA {format_metric('era', current.get('era'))}, "
        f"WHIP {format_metric('whip', current.get('whip'))}, 이닝 {format_metric('ip', current.get('ip'))}입니다. "
        "투구 결과와 월별·상황별 흐름을 함께 보도록 연결했습니다."
    )


def build_summary_insights(
    player: pd.Series,
    current: dict[str, Any],
    seasons: list[dict[str, Any]],
    months: list[dict[str, Any]],
) -> list[str]:
    name = player["player_name"]
    player_type = player["player_type"]
    key = "ops" if player_type == "hitter" else "era"
    latest_months = [row for row in months if row.get("hasData") and row.get(key) is not None]
    season_delta = compare_current_previous(seasons, key, lower_is_better=player_type == "pitcher")
    month_delta = compare_last_two(latest_months, key, lower_is_better=player_type == "pitcher")
    if player_type == "hitter":
        return [
            f"{name}은 대표 지표 기준으로 OPS {format_metric('ops', current.get('ops'))}를 기록 중입니다.",
            season_delta or "연도별 기록은 KBO 상세 통산 표 기준으로 정리했습니다.",
            month_delta or "월별 합계는 KBO 일자별 기록의 각 월 합계 행을 사용했습니다.",
        ]
    return [
        f"{name}은 대표 지표 기준으로 ERA {format_metric('era', current.get('era'))}, K/BB {format_metric('pitcher_k_bb', current.get('pitcher_k_bb'))}를 기록 중입니다.",
        season_delta or "연도별 기록은 KBO 상세 통산 표 기준으로 정리했습니다.",
        month_delta or "월별 합계는 KBO 일자별 기록의 각 월 합계 행을 사용했습니다.",
    ]


def build_detail_insights(player: pd.Series, current: dict[str, Any], situations: pd.DataFrame) -> list[str]:
    name = player["player_name"]
    if player["player_type"] == "hitter":
        situation_text = describe_situation(situations, "hitter")
        return [
            f"{name}의 상세 화면은 KBO 공식 월별 합계와 상황별 타격 기록을 기준으로 구성했습니다.",
            situation_text,
            "타구속도, 하드힛, wRC+, WAR는 현재 공식 수집 범위에 없어 표시하지 않고, 추후 허가된 데이터로 보강합니다.",
        ]
    situation_text = describe_situation(situations, "pitcher")
    return [
        f"{name}의 상세 화면은 KBO 공식 월별 합계와 상황별 피안타 기록을 기준으로 구성했습니다.",
        situation_text,
        "구종, 무브먼트, 릴리스, 팔각도는 현재 공식 수집 범위에 없어 표시하지 않고, 추후 PTS/ABS 라이선스 데이터로 보강합니다.",
    ]


def describe_situation(situations: pd.DataFrame, player_type: str) -> str:
    subset = situations[situations["situation_group"].eq("주자상황별")].copy()
    if subset.empty or "AVG" not in subset.columns:
        return "상황별 기록은 원본 CSV에 보관했으며, 추가 해석 지표는 다음 단계에서 넓힙니다."
    subset["AVG"] = pd.to_numeric(subset["AVG"], errors="coerce")
    subset = subset.dropna(subset=["AVG"])
    if subset.empty:
        return "상황별 기록은 원본 CSV에 보관했으며, 추가 해석 지표는 다음 단계에서 넓힙니다."
    if player_type == "pitcher":
        row = subset.sort_values("AVG", ascending=True).iloc[0]
        return f"주자상황별 피안타율은 {row.get('situation_value')} 구간에서 {format_metric('avg', row['AVG'])}로 가장 낮습니다."
    row = subset.sort_values("AVG", ascending=False).iloc[0]
    return f"주자상황별 타율은 {row.get('situation_value')} 구간에서 {format_metric('avg', row['AVG'])}로 가장 높습니다."


def compare_current_previous(seasons: list[dict[str, Any]], metric_id: str, lower_is_better: bool) -> str:
    current = next((row for row in seasons if row.get("season") == SEASON and row.get(metric_id) is not None), None)
    previous = next((row for row in seasons if row.get("season") == SEASON - 1 and row.get(metric_id) is not None), None)
    if not current or not previous:
        return ""
    delta = current[metric_id] - previous[metric_id]
    improved = delta < 0 if lower_is_better else delta > 0
    direction = "개선" if improved else "하락"
    return f"전년 대비 {metric_label(metric_id, {})}는 {format_delta(metric_id, delta)} 변했고, 방향은 {direction}입니다."


def compare_last_two(months: list[dict[str, Any]], metric_id: str, lower_is_better: bool) -> str:
    if len(months) < 2:
        return ""
    previous, current = months[-2], months[-1]
    delta = current[metric_id] - previous[metric_id]
    improved = delta < 0 if lower_is_better else delta > 0
    direction = "개선" if improved else "하락"
    return f"최근 월별 흐름은 {previous['label']} 대비 {current['label']}에 {format_delta(metric_id, delta)} 변화했고, 방향은 {direction}입니다."


def build_data_needs(player_type: str) -> list[str]:
    if player_type == "hitter":
        return [
            "WAR, wRC+, RAA는 공식 기록실에 없어 자동 수집하지 않음",
            "타구속도, 하드힛, 배럴은 허가된 트래킹 데이터 필요",
            "수비 범위와 송구 지표는 공식/라이선스 데이터 확인 필요",
        ]
    return [
        "구종, 구속, 무브먼트, 릴리스는 허가된 PTS/ABS 데이터 필요",
        "팔각도와 익스텐션은 공식/라이선스 데이터 확인 필요",
        "WAR, ERA+, RAA는 공식 기록실에 없어 자동 수집하지 않음",
    ]


def metric_label(metric_id: str, info: dict[str, Any]) -> str:
    fallback = {
        "hitter_bb_k": "볼삼비",
        "pitcher_k_bb": "K/BB",
        "k9": "K/9",
        "bb9": "BB/9",
        "h9": "H/9",
        "hr9": "HR/9",
        "hr_pa": "HR/PA",
        "k_minus_bb_pct": "K-BB%",
        "opponent_ops": "상대 OPS",
        "ip_per_start": "IP/GS",
        "war": "WAR",
    }
    return fallback.get(metric_id) or str(info.get("metric_name_kr") or info.get("metric_name_en") or metric_id)


def format_metric(metric_id: str, value: Any) -> str:
    value = clean_number(value)
    if value is None:
        if metric_id == "war":
            return "공식 미제공"
        return "미수집"
    if metric_id in {"avg", "obp", "slg", "ops", "iso", "gpa", "risp_avg", "opponent_avg", "fielding_pct", "babip", "babip_allowed", "opponent_ops"}:
        return f"{value:.3f}".replace("0.", ".")
    if metric_id in {"era", "whip", "hitter_bb_k", "pitcher_k_bb", "k9", "bb9", "h9", "hr9", "fip", "pitches_per_pa", "ip_per_start"}:
        return f"{value:.2f}"
    if metric_id in {"ip", "defense_innings"}:
        return f"{value:.1f}"
    if metric_id.endswith("_pct") or metric_id in {"sb_pct", "catcher_cs_pct", "hr_pa"}:
        return f"{value:.1f}%"
    return f"{int(round(value))}" if abs(value - round(value)) < 0.00001 else f"{value:.1f}"


def format_delta(metric_id: str, delta: float) -> str:
    sign = "+" if delta > 0 else ""
    if metric_id in {"avg", "obp", "slg", "ops"}:
        return f"{sign}{delta:.3f}".replace("0.", ".").replace("-0.", "-.")
    return f"{sign}{delta:.2f}"


def first_number(values: list[Any]) -> float | None:
    for value in values:
        number = clean_number(value)
        if number is not None:
            return number
    return None


def clean_number(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_ratio(numerator: Any, denominator: Any, multiplier: float = 1) -> float | None:
    numerator = clean_number(numerator)
    denominator = clean_number(denominator)
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator * multiplier


def subtract_numbers(left: Any, right: Any) -> float | None:
    left = clean_number(left)
    right = clean_number(right)
    if left is None or right is None:
        return None
    return left - right


def hitter_babip(values: dict[str, Any]) -> float | None:
    numerator = subtract_numbers(values.get("hits"), values.get("home_runs"))
    denominator = (
        none_to_zero(values.get("ab"))
        - none_to_zero(values.get("hitter_so"))
        - none_to_zero(values.get("home_runs"))
        + none_to_zero(values.get("sacrifice_flies"))
    )
    return safe_ratio(numerator, denominator)


def pitcher_babip_allowed(values: dict[str, Any]) -> float | None:
    numerator = subtract_numbers(values.get("pitcher_hits_allowed"), values.get("pitcher_home_runs_allowed"))
    denominator = (
        none_to_zero(values.get("total_batters_faced"))
        - none_to_zero(values.get("pitcher_walks"))
        - none_to_zero(values.get("pitcher_hbp_allowed"))
        - none_to_zero(values.get("pitcher_sac_allowed"))
        - none_to_zero(values.get("pitcher_strikeouts"))
        - none_to_zero(values.get("pitcher_home_runs_allowed"))
    )
    return safe_ratio(numerator, denominator)


def fip_without_constant(values: dict[str, Any]) -> float | None:
    home_runs = clean_number(values.get("pitcher_home_runs_allowed"))
    walks = clean_number(values.get("pitcher_walks"))
    hbp = clean_number(values.get("pitcher_hbp_allowed"))
    strikeouts = clean_number(values.get("pitcher_strikeouts"))
    innings = clean_number(values.get("ip"))
    if None in {home_runs, walks, hbp, strikeouts, innings} or innings <= 0:
        return None
    return (13 * home_runs + 3 * (walks + hbp) - 2 * strikeouts) / innings


def lob_pct(values: dict[str, Any]) -> float | None:
    hits = clean_number(values.get("pitcher_hits_allowed"))
    walks = clean_number(values.get("pitcher_walks"))
    hbp = clean_number(values.get("pitcher_hbp_allowed"))
    runs = clean_number(values.get("pitcher_runs"))
    home_runs = clean_number(values.get("pitcher_home_runs_allowed"))
    if None in {hits, walks, hbp, runs, home_runs}:
        return None
    denominator = hits + walks + hbp - 1.4 * home_runs
    return safe_ratio(hits + walks + hbp - runs, denominator, multiplier=100)


def opponent_ops(values: dict[str, Any]) -> float | None:
    hits = clean_number(values.get("pitcher_hits_allowed"))
    doubles = clean_number(values.get("doubles_allowed"))
    triples = clean_number(values.get("triples_allowed"))
    home_runs = clean_number(values.get("pitcher_home_runs_allowed"))
    walks = clean_number(values.get("pitcher_walks"))
    hbp = clean_number(values.get("pitcher_hbp_allowed"))
    sacrifices = clean_number(values.get("pitcher_sac_allowed"))
    sacrifice_flies = clean_number(values.get("pitcher_sf_allowed"))
    total_batters = clean_number(values.get("total_batters_faced"))
    if None in {hits, doubles, triples, home_runs, walks, hbp, sacrifices, sacrifice_flies, total_batters}:
        return None
    at_bats = total_batters - walks - hbp - sacrifices - sacrifice_flies
    total_bases = hits + doubles + 2 * triples + 3 * home_runs
    obp = safe_ratio(hits + walks + hbp, at_bats + walks + hbp + sacrifice_flies)
    slg = safe_ratio(total_bases, at_bats)
    if obp is None or slg is None:
        return None
    return obp + slg


def none_to_zero(value: Any) -> float:
    number = clean_number(value)
    return 0 if number is None else number


def collection_date(metric_df: pd.DataFrame) -> str:
    if metric_df.empty or "collected_at" not in metric_df:
        return ""
    value = str(metric_df["collected_at"].dropna().iloc[0])
    return value.split("T")[0]


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


if __name__ == "__main__":
    main()
