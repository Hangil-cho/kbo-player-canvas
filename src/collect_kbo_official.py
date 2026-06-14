"""
Collect public KBO official record tables and normalize them to metric rows.

This collector deliberately uses only public KBO official pages. It does not
crawl Statiz, Naver Sports, login-gated live commentary, video, or undocumented
commercial feeds.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from http.cookiejar import CookieJar
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin
from urllib.request import HTTPCookieProcessor, Request, build_opener

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SEASON = 2026
BASE_URL = "https://www.koreabaseball.com"
PLAYER_SEARCH_URL = urljoin(BASE_URL, "/Player/Search.aspx")
USER_AGENT = "Mozilla/5.0 (compatible; KBO Player Canvas research prototype)"
SOURCE_NAME = "kbo_official"
LEAGUE_QUALITY_FLAG = "public_leaderboard_page"
DETAIL_QUALITY_FLAG = "public_player_detail_page"
KBO_FIELD_PREFIX = "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$"
REQUEST_DELAY_SECONDS = 0.15

IDENTIFIER_COLUMNS = {
    "순위",
    "선수명",
    "팀명",
    "POS",
    "구분",
    "연도",
    "일자",
    "상대",
    "결과",
}


@dataclass(frozen=True)
class SourcePage:
    key: str
    category: str
    url: str
    period_type: str = "season"
    max_pages: int = 12


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

TEAM_SEARCH_CODE = {
    "kt": "KT",
    "samsung": "SS",
    "ssg": "SK",
    "nc": "NC",
    "lotte": "LT",
    "kia": "HT",
    "hanwha": "HH",
}

POSITION_SEARCH_CODE = {
    "pitcher": "1",
    "catcher": "2",
    "infielder": "3,4,5,6",
    "outfielder": "7,8,9",
}


HITTER_DETAIL_METRIC_MAP = {
    "AVG": "avg",
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
    "SB": "sb",
    "CS": "cs",
    "SAC": "sacrifice_hits",
    "SF": "sacrifice_flies",
    "BB": "hitter_bb",
    "IBB": "hitter_ibb",
    "HBP": "hitter_hbp",
    "SO": "hitter_so",
    "GDP": "hitter_gdp",
    "SLG": "slg",
    "OBP": "obp",
    "OPS": "ops",
    "E": "errors",
    "SB%": "sb_pct",
    "MH": "multi_hit",
    "RISP": "risp_avg",
    "PH-BA": "pinch_hit_avg",
    "AVG1": "avg",
}

PITCHER_DETAIL_METRIC_MAP = {
    "ERA": "era",
    "G": "games_pitched",
    "CG": "complete_games",
    "SHO": "shutouts",
    "W": "pitcher_wins",
    "L": "pitcher_losses",
    "SV": "saves",
    "HLD": "holds",
    "WPCT": "pitcher_win_pct",
    "TBF": "total_batters_faced",
    "NP": "pitch_count",
    "IP": "ip",
    "H": "pitcher_hits_allowed",
    "2B": "doubles_allowed",
    "3B": "triples_allowed",
    "HR": "pitcher_home_runs_allowed",
    "SAC": "pitcher_sac_allowed",
    "SF": "pitcher_sf_allowed",
    "BB": "pitcher_walks",
    "IBB": "intentional_walks_allowed",
    "HBP": "pitcher_hbp_allowed",
    "SO": "pitcher_strikeouts",
    "WP": "wild_pitches",
    "BK": "balks",
    "R": "pitcher_runs",
    "ER": "pitcher_earned_runs",
    "BSV": "blown_saves",
    "WHIP": "whip",
    "AVG": "opponent_avg",
    "QS": "qs",
    "ERA1": "era",
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
    opener = build_kbo_opener()
    players = load_players()
    metric_ids = load_metric_ids()

    source_frames = []
    inventory_frames = []
    metric_frames = []

    for source in SOURCE_PAGES:
        frames = read_paginated_source(source, opener)
        if not frames:
            continue
        source_frame = pd.concat(frames, ignore_index=True, sort=False)
        source_frame.insert(0, "source_key", source.key)
        source_frame.insert(1, "source_category", source.category)
        source_frame.insert(2, "source_url", source.url)
        source_frame.insert(3, "season", SEASON)
        source_frame.insert(4, "collected_at", collected_at)

        raw_path = RAW_DIR / f"kbo_{source.key}_{SEASON}.csv"
        source_frame.to_csv(raw_path, index=False, encoding="utf-8-sig")
        source_frames.append(source_frame)

        inventory_frames.append(build_column_inventory(source, source_frame, metric_ids))
        metric_frames.append(build_metric_values(source, source_frame, players, collected_at, metric_ids))

        page_count = source_frame["source_page"].nunique() if "source_page" in source_frame.columns else 1
        print(f"saved {raw_path.relative_to(PROJECT_ROOT)} rows={len(source_frame)} pages={page_count}")

    combined = pd.concat(source_frames, ignore_index=True, sort=False) if source_frames else pd.DataFrame()
    combined_path = RAW_DIR / f"kbo_official_combined_{SEASON}.csv"
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")
    print(f"saved {combined_path.relative_to(PROJECT_ROOT)} rows={len(combined)}")

    player_directory = discover_player_directory(players, opener, collected_at)
    directory_path = PROCESSED_DIR / f"kbo_player_directory_{SEASON}.csv"
    player_directory.to_csv(directory_path, index=False, encoding="utf-8-sig")
    print(f"saved {directory_path.relative_to(PROJECT_ROOT)} rows={len(player_directory)}")

    detail_outputs = collect_player_detail_pages(player_directory, opener, collected_at, metric_ids)
    metric_frames.extend(detail_outputs["metric_frames"])

    save_optional_frame(detail_outputs["profile_rows"], PROCESSED_DIR / f"kbo_player_profiles_{SEASON}.csv")
    save_optional_frame(detail_outputs["raw_detail_rows"], RAW_DIR / f"kbo_player_detail_tables_{SEASON}.csv")
    save_optional_frame(detail_outputs["monthly_rows"], PROCESSED_DIR / f"kbo_player_monthly_records_{SEASON}.csv")
    save_optional_frame(detail_outputs["situation_rows"], PROCESSED_DIR / f"kbo_player_situation_records_{SEASON}.csv")

    column_inventory = pd.concat(inventory_frames, ignore_index=True, sort=False) if inventory_frames else pd.DataFrame()
    inventory_path = PROCESSED_DIR / f"kbo_official_column_inventory_{SEASON}.csv"
    column_inventory.to_csv(inventory_path, index=False, encoding="utf-8-sig")
    print(f"saved {inventory_path.relative_to(PROJECT_ROOT)} rows={len(column_inventory)}")

    all_metric_values = pd.concat(metric_frames, ignore_index=True, sort=False) if metric_frames else pd.DataFrame()
    all_metric_values_path = PROCESSED_DIR / f"kbo_official_metric_values_{SEASON}.csv"
    all_metric_values.to_csv(all_metric_values_path, index=False, encoding="utf-8-sig")
    print(f"saved {all_metric_values_path.relative_to(PROJECT_ROOT)} rows={len(all_metric_values)}")

    if all_metric_values.empty or "player_id" not in all_metric_values.columns:
        target_metric_values = pd.DataFrame()
    else:
        target_metric_values = all_metric_values[all_metric_values["player_id"].astype(str).ne("")].copy()
    target_metric_values_path = PROCESSED_DIR / "player_metric_values.csv"
    target_metric_values.to_csv(target_metric_values_path, index=False, encoding="utf-8-sig")
    print(f"saved {target_metric_values_path.relative_to(PROJECT_ROOT)} rows={len(target_metric_values)}")

    snapshot = build_target_snapshot(combined, player_directory)
    snapshot_path = PROCESSED_DIR / f"kbo_target_players_snapshot_{SEASON}.csv"
    snapshot.to_csv(snapshot_path, index=False, encoding="utf-8-sig")
    print(f"saved {snapshot_path.relative_to(PROJECT_ROOT)} rows={len(snapshot)}")

    missing = build_missing_report(snapshot, target_metric_values, player_directory)
    missing_path = PROCESSED_DIR / f"kbo_target_players_missing_{SEASON}.csv"
    missing.to_csv(missing_path, index=False, encoding="utf-8-sig")
    print(f"saved {missing_path.relative_to(PROJECT_ROOT)} rows={len(missing)}")


def build_kbo_opener():
    return build_opener(HTTPCookieProcessor(CookieJar()))


def load_players() -> pd.DataFrame:
    path = PROCESSED_DIR / "players_master.csv"
    players = pd.read_csv(path, dtype=str).fillna("")
    players["kbo_team_abbr"] = players["team"].map(TEAM_ABBR).fillna(players["team"])
    return players


def load_metric_ids() -> set[str]:
    path = PROCESSED_DIR / "metric_catalog.csv"
    catalog = pd.read_csv(path, dtype=str)
    return set(catalog["metric_id"].dropna().astype(str))


def fetch_html(opener, url: str, data: dict[str, Any] | None = None, referer: str | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if referer:
        headers["Referer"] = referer
    body = None
    if data is not None:
        body = urlencode({k: "" if v is None else v for k, v in data.items()}).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = Request(url, data=body, headers=headers)
    with opener.open(request, timeout=30) as response:
        content = response.read()
    time.sleep(REQUEST_DELAY_SECONDS)
    return content.decode("utf-8", errors="ignore")


def read_paginated_source(source: SourcePage, opener) -> list[pd.DataFrame]:
    html = fetch_html(opener, source.url)
    first = read_record_table_from_html(html)
    if first is None:
        print(f"warning: no record table found for {source.key}")
        return []

    frames = [attach_page_number(first, 1)]
    max_page = min(parse_max_page(html), source.max_pages)

    for page_number in range(2, max_page + 1):
        page_html = fetch_postback_page(opener, source.url, html, page_number)
        if not page_html or is_kbo_error_page(page_html):
            print(f"warning: {source.key} page {page_number} pagination failed; keeping available pages")
            break
        table = read_record_table_from_html(page_html)
        if table is None:
            print(f"warning: {source.key} page {page_number} had no readable record table")
            break
        frames.append(attach_page_number(table, page_number))
        html = page_html

    return frames


def fetch_postback_page(opener, url: str, html: str, page_number: int) -> str | None:
    payload = extract_form_payload(html)
    if not payload:
        return None
    payload["__EVENTTARGET"] = f"{KBO_FIELD_PREFIX}ucPager$btnNo{page_number}"
    payload["__EVENTARGUMENT"] = ""
    payload[f"{KBO_FIELD_PREFIX}hfPage"] = str(page_number)
    return fetch_html(opener, url, payload, referer=url)


def extract_form_payload(html: str) -> dict[str, str]:
    payload: dict[str, str] = {}
    for tag in re.findall(r"<input\b[^>]*>", html, flags=re.IGNORECASE):
        name = get_attr(tag, "name")
        if not name:
            continue
        input_type = get_attr(tag, "type").lower()
        if input_type in {"submit", "button", "image"}:
            continue
        payload[name] = unescape(get_attr(tag, "value"))

    for tag, inner in re.findall(r"(<select\b[^>]*>)(.*?)</select>", html, flags=re.IGNORECASE | re.DOTALL):
        name = get_attr(tag, "name")
        if not name:
            continue
        options = re.findall(r"<option\b([^>]*)>(.*?)</option>", inner, flags=re.IGNORECASE | re.DOTALL)
        selected_value = ""
        first_value = ""
        for option_tag, _label in options:
            value = unescape(get_attr(option_tag, "value"))
            if first_value == "":
                first_value = value
            if "selected" in option_tag.lower():
                selected_value = value
                break
        payload[name] = selected_value if selected_value != "" else first_value
    return payload


def get_attr(tag: str, attr_name: str) -> str:
    match = re.search(rf'\b{re.escape(attr_name)}=["\']([^"\']*)["\']', tag, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def read_record_table_from_html(html: str) -> pd.DataFrame | None:
    for table in read_html_tables(html):
        columns = {str(column).strip() for column in table.columns}
        if {"선수명", "팀명"}.issubset(columns):
            return normalize_columns(table)
    return None


def read_html_tables(html: str) -> list[pd.DataFrame]:
    try:
        tables = pd.read_html(StringIO(html))
    except ValueError:
        return []
    return [normalize_columns(table) for table in tables]


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def attach_page_number(frame: pd.DataFrame, page_number: int) -> pd.DataFrame:
    frame = frame.copy()
    frame["source_page"] = page_number
    return frame


def parse_max_page(html: str) -> int:
    page_numbers = []
    for match in re.finditer(r"ucPager_btnNo(\d+)", html):
        page_numbers.append(int(match.group(1)))
    return max(page_numbers) if page_numbers else 1


def is_kbo_error_page(html: str) -> bool:
    lower = html.lower()
    return "errorbox" in lower or "<title>에러" in html


def discover_player_directory(players: pd.DataFrame, opener, collected_at: str) -> pd.DataFrame:
    rows = []
    for _, player in players.iterrows():
        player_dict = player.to_dict()
        candidate = search_player(player_dict, opener)
        rows.append(
            {
                **{column: player_dict.get(column, "") for column in players.columns if column != "kbo_team_abbr"},
                "kbo_player_id": candidate.get("kbo_player_id", ""),
                "kbo_detail_url": candidate.get("kbo_detail_url", ""),
                "kbo_detail_type": candidate.get("kbo_detail_type", ""),
                "search_team": candidate.get("team", ""),
                "search_position": candidate.get("position", ""),
                "search_birth_date": candidate.get("birth_date", ""),
                "search_source": "kbo_player_search" if candidate else "",
                "collected_at": collected_at,
            }
        )
    return pd.DataFrame(rows)


def search_player(player: dict[str, str], opener) -> dict[str, str]:
    team_code = TEAM_SEARCH_CODE.get(player.get("team_id", ""), "")
    position_code = POSITION_SEARCH_CODE.get(player.get("position_group", ""), "")
    search_attempts = [
        (team_code, position_code),
        (team_code, ""),
        ("", position_code),
        ("", ""),
    ]
    for team, position in search_attempts:
        html = fetch_html(opener, PLAYER_SEARCH_URL)
        payload = extract_form_payload(html)
        payload.update(
            {
                f"{KBO_FIELD_PREFIX}ddlTeam": team,
                f"{KBO_FIELD_PREFIX}ddlPosition": position,
                f"{KBO_FIELD_PREFIX}txtSearchPlayerName": player["player_name"],
                f"{KBO_FIELD_PREFIX}btnSearch": "검색",
                f"{KBO_FIELD_PREFIX}hfPage": "1",
            }
        )
        result_html = fetch_html(opener, PLAYER_SEARCH_URL, payload, referer=PLAYER_SEARCH_URL)
        candidates = parse_player_search_results(result_html)
        match = choose_player_candidate(player, candidates)
        if match:
            return match
    return {}


def parse_player_search_results(html: str) -> list[dict[str, str]]:
    rows = []
    for row_html in re.findall(r"<tr\b[^>]*>(.*?)</tr>", html, flags=re.IGNORECASE | re.DOTALL):
        if "playerId=" not in row_html:
            continue
        href_match = re.search(r"href=['\"]([^'\"]*playerId=([0-9]+)[^'\"]*)['\"]", row_html)
        if not href_match:
            continue
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", row_html, flags=re.IGNORECASE | re.DOTALL)
        values = [strip_tags(cell) for cell in cells]
        detail_url = urljoin(BASE_URL, href_match.group(1))
        detail_type = "pitcher" if "PitcherDetail" in detail_url else "hitter"
        rows.append(
            {
                "kbo_player_id": href_match.group(2),
                "kbo_detail_url": detail_url,
                "kbo_detail_type": detail_type,
                "number": values[0] if len(values) > 0 else "",
                "player_name": values[1] if len(values) > 1 else "",
                "team": values[2] if len(values) > 2 else "",
                "position": values[3] if len(values) > 3 else "",
                "birth_date": values[4] if len(values) > 4 else "",
                "body": values[5] if len(values) > 5 else "",
                "school": values[6] if len(values) > 6 else "",
            }
        )
    return rows


def choose_player_candidate(player: dict[str, str], candidates: list[dict[str, str]]) -> dict[str, str]:
    if not candidates:
        return {}
    exact_name = [candidate for candidate in candidates if candidate.get("player_name") == player["player_name"]]
    if not exact_name:
        exact_name = candidates
    team_abbr = player.get("kbo_team_abbr") or TEAM_ABBR.get(player.get("team", ""), "")
    same_team = [candidate for candidate in exact_name if not team_abbr or candidate.get("team") == team_abbr]
    if same_team:
        return same_team[0]
    return exact_name[0]


def strip_tags(html_fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_fragment)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def collect_player_detail_pages(
    player_directory: pd.DataFrame,
    opener,
    collected_at: str,
    metric_ids: set[str],
) -> dict[str, Any]:
    profile_rows = []
    raw_detail_rows = []
    monthly_rows = []
    situation_rows = []
    metric_frames = []

    for _, player in player_directory.iterrows():
        kbo_player_id = str(player.get("kbo_player_id", "")).strip()
        if not kbo_player_id:
            print(f"warning: no KBO player id for {player.get('player_name')}")
            continue
        player_type = "pitcher" if player.get("player_type") == "pitcher" else "hitter"

        page_tables: dict[str, list[pd.DataFrame]] = {}
        page_htmls: dict[str, str] = {}
        for page_type in ["Basic", "Total", "Daily", "Game", "Situation"]:
            url = build_detail_url(player_type, page_type, kbo_player_id)
            html = fetch_html(opener, url)
            page_htmls[page_type] = html
            tables = read_html_tables(html)
            page_tables[page_type] = tables
            raw_detail_rows.extend(build_raw_detail_rows(player, kbo_player_id, player_type, page_type, url, tables))

        profile = extract_player_profile(page_htmls.get("Basic", ""))
        profile_rows.append(
            {
                "player_id": player.get("player_id", ""),
                "player_name": player.get("player_name", ""),
                "kbo_player_id": kbo_player_id,
                "kbo_detail_url": build_detail_url(player_type, "Basic", kbo_player_id),
                "player_type": player_type,
                "collected_at": collected_at,
                **profile,
            }
        )

        metric_frames.append(
            build_player_basic_metric_values(player, kbo_player_id, page_tables.get("Basic", []), collected_at, metric_ids)
        )
        metric_frames.append(
            build_player_total_metric_values(player, kbo_player_id, page_tables.get("Total", []), collected_at, metric_ids)
        )

        player_monthly = build_monthly_rows(player, kbo_player_id, page_tables.get("Daily", []), collected_at)
        monthly_rows.extend(player_monthly)
        metric_frames.append(build_monthly_metric_values(player, kbo_player_id, player_monthly, collected_at, metric_ids))

        section_titles = extract_section_titles(page_htmls.get("Situation", ""))
        player_situations = build_situation_rows(
            player,
            kbo_player_id,
            page_tables.get("Situation", []),
            section_titles,
            collected_at,
        )
        situation_rows.extend(player_situations)
        metric_frames.append(
            build_situation_metric_values(player, kbo_player_id, player_situations, collected_at, metric_ids)
        )

        print(f"collected detail pages for {player.get('player_name')} ({kbo_player_id})")

    return {
        "profile_rows": pd.DataFrame(profile_rows),
        "raw_detail_rows": pd.DataFrame(raw_detail_rows),
        "monthly_rows": pd.DataFrame(monthly_rows),
        "situation_rows": pd.DataFrame(situation_rows),
        "metric_frames": [frame for frame in metric_frames if frame is not None and not frame.empty],
    }


def build_detail_url(player_type: str, page_type: str, kbo_player_id: str) -> str:
    detail_dir = "PitcherDetail" if player_type == "pitcher" else "HitterDetail"
    return urljoin(BASE_URL, f"/Record/Player/{detail_dir}/{page_type}.aspx?playerId={kbo_player_id}")


def extract_player_profile(html: str) -> dict[str, str]:
    profile = {}
    for label, value in re.findall(r"<li>\s*([^:<]+):\s*(.*?)</li>", html, flags=re.IGNORECASE | re.DOTALL):
        key = strip_tags(label)
        if key:
            profile[key] = strip_tags(value)
    return profile


def build_raw_detail_rows(
    player: pd.Series,
    kbo_player_id: str,
    player_type: str,
    page_type: str,
    url: str,
    tables: list[pd.DataFrame],
) -> list[dict[str, Any]]:
    rows = []
    for table_index, table in enumerate(tables):
        for row_index, row in table.iterrows():
            rows.append(
                {
                    "player_id": player.get("player_id", ""),
                    "player_name": player.get("player_name", ""),
                    "kbo_player_id": kbo_player_id,
                    "player_type": player_type,
                    "detail_page_type": page_type,
                    "source_url": url,
                    "table_index": table_index,
                    "row_index": row_index,
                    **row.to_dict(),
                }
            )
    return rows


def build_player_basic_metric_values(
    player: pd.Series,
    kbo_player_id: str,
    tables: list[pd.DataFrame],
    collected_at: str,
    metric_ids: set[str],
) -> pd.DataFrame:
    if not tables:
        return pd.DataFrame()
    source_columns = {}
    for table in tables[:2]:
        if table.empty:
            continue
        for column, value in table.iloc[0].to_dict().items():
            source_columns[str(column)] = value

    mapping = detail_mapping_for_player(player)
    rows = metric_rows_from_record(
        player=player,
        kbo_player_id=kbo_player_id,
        record=source_columns,
        mapping=mapping,
        metric_ids=metric_ids,
        source_key="player_detail_basic",
        source_column_prefix="",
        source_url=build_detail_url(player.get("player_type", ""), "Basic", kbo_player_id),
        period_type="season",
        period_value=str(SEASON),
        collected_at=collected_at,
        quality_flag=DETAIL_QUALITY_FLAG,
    )
    return pd.DataFrame(rows)


def build_player_total_metric_values(
    player: pd.Series,
    kbo_player_id: str,
    tables: list[pd.DataFrame],
    collected_at: str,
    metric_ids: set[str],
) -> pd.DataFrame:
    if not tables:
        return pd.DataFrame()
    mapping = detail_mapping_for_player(player)
    rows = []
    for _, record in tables[0].iterrows():
        year = clean_text(record.get("연도", ""))
        if not year:
            continue
        period_type = "career" if year == "통산" else "season"
        period_value = "career" if year == "통산" else year
        rows.extend(
            metric_rows_from_record(
                player=player,
                kbo_player_id=kbo_player_id,
                record=record.to_dict(),
                mapping=mapping,
                metric_ids=metric_ids,
                source_key="player_detail_total",
                source_column_prefix="",
                source_url=build_detail_url(player.get("player_type", ""), "Total", kbo_player_id),
                period_type=period_type,
                period_value=period_value,
                collected_at=collected_at,
                quality_flag=DETAIL_QUALITY_FLAG,
            )
        )
    return pd.DataFrame(rows)


def build_monthly_rows(
    player: pd.Series,
    kbo_player_id: str,
    tables: list[pd.DataFrame],
    collected_at: str,
) -> list[dict[str, Any]]:
    rows = []
    for table_index, table in enumerate(tables):
        if table.empty:
            continue
        month_label = str(table.columns[0]).strip()
        month_number = parse_month_number(month_label)
        for row_index, row in table.iterrows():
            first_value = clean_text(row.iloc[0] if len(row) else "")
            opponent = clean_text(row.get("상대", ""))
            is_summary = first_value == "합계" or opponent == "합계"
            row_type = "monthly_summary" if is_summary else "game"
            period_value = f"{SEASON}-{month_number:02d}" if month_number else month_label
            rows.append(
                {
                    "player_id": player.get("player_id", ""),
                    "player_name": player.get("player_name", ""),
                    "kbo_player_id": kbo_player_id,
                    "player_type": player.get("player_type", ""),
                    "period_type": "month" if is_summary else "game_date",
                    "period_value": period_value if is_summary else f"{SEASON}.{first_value}",
                    "month": month_label,
                    "row_type": row_type,
                    "table_index": table_index,
                    "row_index": row_index,
                    "source_url": build_detail_url(player.get("player_type", ""), "Daily", kbo_player_id),
                    "collected_at": collected_at,
                    **row.to_dict(),
                }
            )
    return rows


def build_monthly_metric_values(
    player: pd.Series,
    kbo_player_id: str,
    monthly_rows: list[dict[str, Any]],
    collected_at: str,
    metric_ids: set[str],
) -> pd.DataFrame:
    mapping = detail_mapping_for_player(player)
    rows = []
    for record in monthly_rows:
        if record.get("row_type") != "monthly_summary":
            continue
        rows.extend(
            metric_rows_from_record(
                player=player,
                kbo_player_id=kbo_player_id,
                record=record,
                mapping=mapping,
                metric_ids=metric_ids,
                source_key="player_detail_daily_month",
                source_column_prefix="",
                source_url=record.get("source_url", ""),
                period_type="month",
                period_value=record.get("period_value", ""),
                collected_at=collected_at,
                quality_flag=DETAIL_QUALITY_FLAG,
            )
        )
    return pd.DataFrame(rows)


def build_situation_rows(
    player: pd.Series,
    kbo_player_id: str,
    tables: list[pd.DataFrame],
    section_titles: list[str],
    collected_at: str,
) -> list[dict[str, Any]]:
    rows = []
    for table_index, table in enumerate(tables):
        if table.empty:
            continue
        situation_group = section_titles[table_index] if table_index < len(section_titles) else f"table_{table_index}"
        for row_index, row in table.iterrows():
            situation_value = clean_text(row.get("구분", row.iloc[0] if len(row) else ""))
            rows.append(
                {
                    "player_id": player.get("player_id", ""),
                    "player_name": player.get("player_name", ""),
                    "kbo_player_id": kbo_player_id,
                    "player_type": player.get("player_type", ""),
                    "period_type": "situation",
                    "period_value": f"{situation_group}|{situation_value}",
                    "situation_group": situation_group,
                    "situation_value": situation_value,
                    "table_index": table_index,
                    "row_index": row_index,
                    "source_url": build_detail_url(player.get("player_type", ""), "Situation", kbo_player_id),
                    "collected_at": collected_at,
                    **row.to_dict(),
                }
            )
    return rows


def build_situation_metric_values(
    player: pd.Series,
    kbo_player_id: str,
    situation_rows: list[dict[str, Any]],
    collected_at: str,
    metric_ids: set[str],
) -> pd.DataFrame:
    mapping = detail_mapping_for_player(player)
    rows = []
    for record in situation_rows:
        rows.extend(
            metric_rows_from_record(
                player=player,
                kbo_player_id=kbo_player_id,
                record=record,
                mapping=mapping,
                metric_ids=metric_ids,
                source_key="player_detail_situation",
                source_column_prefix="",
                source_url=record.get("source_url", ""),
                period_type="situation",
                period_value=record.get("period_value", ""),
                collected_at=collected_at,
                quality_flag=DETAIL_QUALITY_FLAG,
            )
        )
    return pd.DataFrame(rows)


def extract_section_titles(html: str) -> list[str]:
    titles = []
    for match in re.findall(r"<h5[^>]*>(.*?)</h5>", html, flags=re.IGNORECASE | re.DOTALL):
        title = strip_tags(match)
        if title:
            titles.append(title)
    return titles


def parse_month_number(month_label: str) -> int | None:
    match = re.search(r"(\d{1,2})월", str(month_label))
    return int(match.group(1)) if match else None


def detail_mapping_for_player(player: pd.Series | dict[str, Any]) -> dict[str, str]:
    player_type = player.get("player_type", "")
    return PITCHER_DETAIL_METRIC_MAP if player_type == "pitcher" else HITTER_DETAIL_METRIC_MAP


def metric_rows_from_record(
    player: pd.Series | dict[str, Any],
    kbo_player_id: str,
    record: dict[str, Any],
    mapping: dict[str, str],
    metric_ids: set[str],
    source_key: str,
    source_column_prefix: str,
    source_url: str,
    period_type: str,
    period_value: str,
    collected_at: str,
    quality_flag: str,
) -> list[dict[str, Any]]:
    rows = []
    sample_size = sample_size_for(player_metric_category(player), record)
    team = (
        clean_text(record.get("팀명", ""))
        or clean_text(player.get("search_team", ""))
        or TEAM_ABBR.get(player.get("team", ""), "")
    )
    for source_column, metric_id in mapping.items():
        if metric_id not in metric_ids or source_column not in record:
            continue
        rows.append(
            {
                "player_id": player.get("player_id", ""),
                "external_player_name": player.get("player_name", ""),
                "kbo_player_id": kbo_player_id,
                "season": SEASON,
                "period_type": period_type,
                "period_value": period_value,
                "team": team,
                "role_group": player.get("role_group", ""),
                "position_group": player.get("position_group", ""),
                "source_position": "",
                "metric_id": metric_id,
                "value": parse_number(record.get(source_column, "")),
                "sample_size": sample_size,
                "source": SOURCE_NAME,
                "source_key": source_key,
                "source_column": f"{source_column_prefix}{source_column}",
                "source_url": source_url,
                "source_rank": None,
                "quality_flag": quality_flag,
                "collected_at": collected_at,
            }
        )
    return rows


def player_metric_category(player: pd.Series | dict[str, Any]) -> str:
    return "pitching" if player.get("player_type", "") == "pitcher" else "batting"


def save_optional_frame(frame: pd.DataFrame, path: Path) -> None:
    if frame is None or frame.empty:
        frame = pd.DataFrame()
    frame.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"saved {path.relative_to(PROJECT_ROOT)} rows={len(frame)}")


def build_column_inventory(source: SourcePage, frame: pd.DataFrame, metric_ids: set[str]) -> pd.DataFrame:
    rows = []
    mapping = SOURCE_METRIC_MAP.get(source.key, {})
    for column in frame.columns:
        if column in {"source_key", "source_category", "source_url", "season", "collected_at", "source_page"}:
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
                "is_identifier": column in IDENTIFIER_COLUMNS,
                "notes": "identifier_or_context" if column in IDENTIFIER_COLUMNS else "",
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
                    "kbo_player_id": "",
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
                    "quality_flag": LEAGUE_QUALITY_FLAG,
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


def sample_size_for(category: str, record: pd.Series | dict[str, Any]) -> float | None:
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
    if text in {"", "-", "--", "nan"}:
        return None

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


def build_target_snapshot(combined: pd.DataFrame, player_directory: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, player in player_directory.iterrows():
        name = player["player_name"]
        team_abbr = player.get("kbo_team_abbr", "") or TEAM_ABBR.get(player.get("team", ""), "")
        matches = pd.DataFrame()
        if not combined.empty and "선수명" in combined.columns:
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
                    "kbo_player_id": player.get("kbo_player_id", ""),
                    "source_key": "player_detail" if player.get("kbo_player_id", "") else "",
                    "matched": bool(player.get("kbo_player_id", "")),
                    "note": "filled by player detail page" if player.get("kbo_player_id", "") else "not found",
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
                    "kbo_player_id": player.get("kbo_player_id", ""),
                    "source_key": row.get("source_key", ""),
                    "source_category": row.get("source_category", ""),
                    "matched": True,
                    "note": "",
                }
            )
    return pd.DataFrame(rows)


def build_missing_report(
    snapshot: pd.DataFrame,
    target_metric_values: pd.DataFrame,
    player_directory: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for _, player in player_directory.iterrows():
        player_rows = snapshot[snapshot["player_id"].eq(player["player_id"])]
        matched_sources = sorted(
            player_rows[player_rows["matched"].eq(True)]["source_key"].dropna().astype(str).unique()
        )
        metric_count = 0
        period_types = ""
        if not target_metric_values.empty:
            metric_rows = target_metric_values[target_metric_values["player_id"].eq(player["player_id"])]
            metric_count = len(metric_rows)
            period_types = ", ".join(sorted(metric_rows["period_type"].dropna().astype(str).unique()))
        rows.append(
            {
                "player_id": player["player_id"],
                "player_name": player["player_name"],
                "team": player["team"],
                "role_group": player["role_group"],
                "kbo_player_id": player.get("kbo_player_id", ""),
                "matched_source_count": len(matched_sources),
                "matched_sources": ", ".join(matched_sources),
                "metric_row_count": metric_count,
                "period_types": period_types,
                "needs_follow_up": metric_count == 0,
                "recommended_next_step": "" if metric_count else "check player search result manually",
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    main()
