"""
Collect public KBO official record tables and normalize them to metric rows.

This collector deliberately uses only public KBO official record pages for now.
It does not crawl Statiz, Naver Sports, login-gated live commentary, video, or
undocumented commercial feeds.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SEASON = 2026
USER_AGENT = "Mozilla/5.0 (compatible; KBO Player Canvas research prototype)"
SOURCE_NAME = "kbo_official"
QUALITY_FLAG = "public_leaderboard_page_only"


@dataclass(frozen=True)
class SourcePage:
    key: str
    category: str
    url: str
    period_type: str = "season"


SOURCE_PAGES = [
    SourcePage("hitter_basic1", "batting", "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx"),
    SourcePage("hitter_basic2", "batting", "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic2.aspx"),
    SourcePage("hitter_detail1", "batting", "https://www.koreabaseball.com/Record/Player/HitterBasic/Detail1.aspx"),
    SourcePage("pitcher_basic1", "pitching", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx"),
    SourcePage("pitcher_basic2", "pitching", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic2.aspx"),
    SourcePage("pitcher_detail1", "pitching", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Detail1.aspx"),
    SourcePage("defense_basic", "defense", "https://www.koreabaseball.com/Record/Player/Defense/Basic.aspx"),
    SourcePage("runner_basic", "running", "https://www.koreabaseball.com/Record/Player/Runner/Basic.aspx"),
]

TEAM_ABBR = {
    "kt wiz": "KT",
    "삼성 라이온즈": "삼성",
    "SSG 랜더스": "SSG",
    "NC 다이노스": "NC",
    "롯데 자이언츠": "롯데",
    "KIA 타이거즈": "KIA",
    "한화 이글스": "한화",
}

SOURCE_METRIC_MAP = {
    "hitter_basic1": {
        "G": "hitter_games",
        "PA": "pa",
        "AB": "ab",
        "R": "runs",
        "H": "hits",
        "2B": "doubles",
        "3B": "triples",
        "HR": "home_runs",
        "TB": "total_bases",
        "RBI": "rbi",
        "SAC": "sacrifice_hits",
        "SF": "sacrifice_flies",
        "AVG": "avg",
    },
    "hitter_basic2": {
        "AVG": "avg",
        "BB": "hitter_bb",
        "IBB": "hitter_ibb",
        "HBP": "hitter_hbp",
        "SO": "hitter_so",
        "GDP": "hitter_gdp",
        "SLG": "slg",
        "OBP": "obp",
        "OPS": "ops",
        "MH": "multi_hit",
        "RISP": "risp_avg",
        "PH-BA": "pinch_hit_avg",
    },
    "hitter_detail1": {
        "AVG": "avg",
        "XBH": "extra_base_hits",
        "GO": "ground_outs",
        "AO": "air_outs",
        "GO/AO": "ground_air_ratio",
        "GW RBI": "game_winning_rbi",
        "BB/K": "hitter_bb_k",
        "P/PA": "pitches_per_pa",
        "ISOP": "iso",
        "XR": "xr",
        "GPA": "gpa",
    },
    "pitcher_basic1": {
        "ERA": "era",
        "G": "games_pitched",
        "W": "pitcher_wins",
        "L": "pitcher_losses",
        "SV": "saves",
        "HLD": "holds",
        "WPCT": "pitcher_win_pct",
        "IP": "ip",
        "H": "pitcher_hits_allowed",
        "HR": "pitcher_home_runs_allowed",
        "BB": "pitcher_walks",
        "HBP": "pitcher_hbp_allowed",
        "SO": "pitcher_strikeouts",
        "R": "pitcher_runs",
        "ER": "pitcher_earned_runs",
        "WHIP": "whip",
    },
    "pitcher_basic2": {
        "ERA": "era",
        "CG": "complete_games",
        "SHO": "shutouts",
        "QS": "qs",
        "BSV": "blown_saves",
        "TBF": "total_batters_faced",
        "NP": "pitch_count",
        "AVG": "opponent_avg",
        "2B": "doubles_allowed",
        "3B": "triples_allowed",
        "SAC": "pitcher_sac_allowed",
        "SF": "pitcher_sf_allowed",
        "IBB": "intentional_walks_allowed",
        "WP": "wild_pitches",
        "BK": "balks",
    },
    "pitcher_detail1": {
        "ERA": "era",
        "GS": "games_started",
        "Wgs": "starter_wins",
        "Wgr": "relief_wins",
        "GF": "games_finished",
        "SVO": "save_opportunities",
        "TS": "relief_touch_success",
        "GDP": "pitcher_gdp",
        "GO": "pitcher_go",
        "AO": "pitcher_ao",
        "GO/AO": "pitcher_go_ao",
    },
    "defense_basic": {
        "G": "defense_games",
        "GS": "defense_starts",
        "IP": "defense_innings",
        "E": "errors",
        "PKO": "pickoffs",
        "PO": "putouts",
        "A": "assists",
        "DP": "double_plays",
        "FPCT": "fielding_pct",
        "PB": "passed_balls",
        "SB": "stolen_bases_allowed",
        "CS": "caught_stealing_allowed",
        "CS%": "catcher_cs_pct",
    },
    "runner_basic": {
        "G": "runner_games",
        "SBA": "steal_attempts",
        "SB": "sb",
        "CS": "cs",
        "SB%": "sb_pct",
        "OOB": "out_on_base",
        "PKO": "pickoff_outs",
    },
}


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    collected_at = datetime.now().isoformat(timespec="seconds")
    players = load_players()
    metric_ids = load_metric_ids()

    source_frames = []
    inventory_frames = []
    metric_frames = []

    for source in SOURCE_PAGES:
        frame = read_first_table(source.url)
        frame.insert(0, "source_key", source.key)
        frame.insert(1, "source_category", source.category)
        frame.insert(2, "source_url", source.url)
        frame.insert(3, "season", SEASON)
        frame.insert(4, "collected_at", collected_at)

        raw_path = RAW_DIR / f"kbo_{source.key}_{SEASON}.csv"
        frame.to_csv(raw_path, index=False, encoding="utf-8-sig")
        source_frames.append(frame)

        inventory_frames.append(build_column_inventory(source, frame, metric_ids))
        metric_frames.append(build_metric_values(source, frame, players, collected_at, metric_ids))

        print(f"saved {raw_path.relative_to(PROJECT_ROOT)} rows={len(frame)} cols={len(frame.columns)}")

    combined = pd.concat(source_frames, ignore_index=True, sort=False)
    combined_path = RAW_DIR / f"kbo_official_combined_{SEASON}.csv"
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")
    print(f"saved {combined_path.relative_to(PROJECT_ROOT)} rows={len(combined)}")

    column_inventory = pd.concat(inventory_frames, ignore_index=True, sort=False)
    inventory_path = PROCESSED_DIR / f"kbo_official_column_inventory_{SEASON}.csv"
    column_inventory.to_csv(inventory_path, index=False, encoding="utf-8-sig")
    print(f"saved {inventory_path.relative_to(PROJECT_ROOT)} rows={len(column_inventory)}")

    all_metric_values = pd.concat(metric_frames, ignore_index=True, sort=False)
    all_metric_values_path = PROCESSED_DIR / f"kbo_official_metric_values_{SEASON}.csv"
    all_metric_values.to_csv(all_metric_values_path, index=False, encoding="utf-8-sig")
    print(f"saved {all_metric_values_path.relative_to(PROJECT_ROOT)} rows={len(all_metric_values)}")

    target_metric_values = all_metric_values[all_metric_values["player_id"].astype(str).ne("")].copy()
    target_metric_values_path = PROCESSED_DIR / "player_metric_values.csv"
    target_metric_values.to_csv(target_metric_values_path, index=False, encoding="utf-8-sig")
    print(f"saved {target_metric_values_path.relative_to(PROJECT_ROOT)} rows={len(target_metric_values)}")

    snapshot = build_target_snapshot(combined, players)
    snapshot_path = PROCESSED_DIR / f"kbo_target_players_snapshot_{SEASON}.csv"
    snapshot.to_csv(snapshot_path, index=False, encoding="utf-8-sig")
    print(f"saved {snapshot_path.relative_to(PROJECT_ROOT)} rows={len(snapshot)}")

    missing = build_missing_report(snapshot, players)
    missing_path = PROCESSED_DIR / f"kbo_target_players_missing_{SEASON}.csv"
    missing.to_csv(missing_path, index=False, encoding="utf-8-sig")
    print(f"saved {missing_path.relative_to(PROJECT_ROOT)} rows={len(missing)}")


def load_players() -> pd.DataFrame:
    path = PROCESSED_DIR / "players_master.csv"
    players = pd.read_csv(path, dtype=str).fillna("")
    players["kbo_team_abbr"] = players["team"].map(TEAM_ABBR).fillna(players["team"])
    return players


def load_metric_ids() -> set[str]:
    path = PROCESSED_DIR / "metric_catalog.csv"
    catalog = pd.read_csv(path, dtype=str)
    return set(catalog["metric_id"].dropna().astype(str))


def read_first_table(url: str) -> pd.DataFrame:
    storage_options = {"User-Agent": USER_AGENT}
    tables = pd.read_html(url, encoding="utf-8", storage_options=storage_options)
    if not tables:
        raise RuntimeError(f"No HTML table found: {url}")
    frame = tables[0].copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def build_column_inventory(source: SourcePage, frame: pd.DataFrame, metric_ids: set[str]) -> pd.DataFrame:
    rows = []
    mapping = SOURCE_METRIC_MAP.get(source.key, {})
    for column in frame.columns:
        if column in {"source_key", "source_category", "source_url", "season", "collected_at"}:
            continue
        metric_id = mapping.get(str(column), "")
        rows.append(
            {
                "source_key": source.key,
                "source_category": source.category,
                "source_url": source.url,
                "column_name": column,
                "mapped_metric_id": metric_id,
                "in_metric_catalog": bool(metric_id and metric_id in metric_ids),
                "is_identifier": column in {"순위", "선수명", "팀명", "POS"},
                "notes": "identifier_or_context" if column in {"순위", "선수명", "팀명", "POS"} else "",
            }
        )
    return pd.DataFrame(rows)


def build_metric_values(
    source: SourcePage,
    frame: pd.DataFrame,
    players: pd.DataFrame,
    collected_at: str,
    metric_ids: set[str],
) -> pd.DataFrame:
    rows = []
    mapping = SOURCE_METRIC_MAP.get(source.key, {})
    source_position = "POS" if "POS" in frame.columns else None

    for _, record in frame.iterrows():
        player_name = clean_text(record.get("선수명", ""))
        team = clean_text(record.get("팀명", ""))
        player = find_player(players, player_name, team)
        sample_size = sample_size_for(source.category, record)
        rank = parse_number(record.get("순위", ""))

        for source_column, metric_id in mapping.items():
            if metric_id not in metric_ids or source_column not in frame.columns:
                continue
            value = parse_number(record.get(source_column, ""))
            rows.append(
                {
                    "player_id": player.get("player_id", ""),
                    "external_player_name": player_name,
                    "season": SEASON,
                    "period_type": source.period_type,
                    "period_value": str(SEASON),
                    "team": team,
                    "role_group": player.get("role_group", inferred_role(source.category)),
                    "position_group": player.get("position_group", inferred_position_group(source.category)),
                    "source_position": clean_text(record.get(source_position, "")) if source_position else "",
                    "metric_id": metric_id,
                    "value": value,
                    "sample_size": sample_size,
                    "source": SOURCE_NAME,
                    "source_key": source.key,
                    "source_column": source_column,
                    "source_url": source.url,
                    "source_rank": rank,
                    "quality_flag": QUALITY_FLAG,
                    "collected_at": collected_at,
                }
            )
    return pd.DataFrame(rows)


def find_player(players: pd.DataFrame, player_name: str, team: str) -> dict[str, str]:
    if not player_name:
        return {}
    matches = players[players["player_name"].astype(str).eq(player_name)]
    if team and not matches.empty:
        same_team = matches[matches["kbo_team_abbr"].astype(str).eq(team)]
        if not same_team.empty:
            matches = same_team
    if matches.empty:
        return {}
    return matches.iloc[0].to_dict()


def sample_size_for(category: str, record: pd.Series) -> float | None:
    if category == "batting":
        return parse_number(record.get("PA", record.get("AB", "")))
    if category == "pitching":
        return parse_number(record.get("IP", record.get("TBF", "")))
    if category == "defense":
        return parse_number(record.get("IP", record.get("G", "")))
    if category == "running":
        return parse_number(record.get("SBA", record.get("G", "")))
    return None


def inferred_role(category: str) -> str:
    if category == "pitching":
        return "pitcher"
    return ""


def inferred_position_group(category: str) -> str:
    if category == "batting":
        return "hitter"
    if category == "pitching":
        return "pitcher"
    return category


def parse_number(value: Any) -> float | None:
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = clean_text(value).replace(",", "")
    if text in {"", "-", "--"}:
        return None

    # KBO innings can appear as "33 1/3" or "33.1" depending on table parsing.
    if " " in text and "/" in text:
        whole, fraction = text.split(" ", 1)
        numerator, denominator = fraction.split("/", 1)
        return float(whole) + float(numerator) / float(denominator)

    if "/" in text and text.count("/") == 1:
        numerator, denominator = text.split("/", 1)
        return float(numerator) / float(denominator)

    try:
        return float(text)
    except ValueError:
        return None


def clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def build_target_snapshot(combined: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, player in players.iterrows():
        name = player["player_name"]
        team_abbr = player["kbo_team_abbr"]
        matches = combined[combined["선수명"].astype(str).eq(name)].copy()
        if "팀명" in matches.columns:
            same_team = matches["팀명"].astype(str).eq(team_abbr)
            matches = matches[same_team | ~matches["팀명"].notna()]
        if matches.empty:
            rows.append(
                {
                    "player_id": player["player_id"],
                    "player_name": name,
                    "team": player["team"],
                    "role_group": player["role_group"],
                    "source_key": "",
                    "matched": False,
                    "note": "KBO official public leaderboard pages did not include this player",
                }
            )
            continue
        for _, row in matches.iterrows():
            rows.append(
                {
                    "player_id": player["player_id"],
                    "player_name": name,
                    "team": player["team"],
                    "role_group": player["role_group"],
                    "source_key": row.get("source_key", ""),
                    "source_category": row.get("source_category", ""),
                    "matched": True,
                    "note": "",
                }
            )
    return pd.DataFrame(rows)


def build_missing_report(snapshot: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, player in players.iterrows():
        player_rows = snapshot[snapshot["player_id"].eq(player["player_id"])]
        matched_sources = sorted(
            player_rows[player_rows["matched"].eq(True)]["source_key"].dropna().astype(str).unique()
        )
        rows.append(
            {
                "player_id": player["player_id"],
                "player_name": player["player_name"],
                "team": player["team"],
                "role_group": player["role_group"],
                "matched_source_count": len(matched_sources),
                "matched_sources": ", ".join(matched_sources),
                "needs_follow_up": len(matched_sources) == 0,
                "recommended_next_step": (
                    "check player detail pages or wait for qualified leaderboard inclusion"
                    if len(matched_sources) == 0
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    main()
