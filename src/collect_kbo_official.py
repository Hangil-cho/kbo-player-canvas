"""
Collect KBO official record tables and save editable CSV files.

The first version intentionally focuses on stable public table pages from
koreabaseball.com. It saves source tables as raw CSV and a small processed
snapshot for the 10 target players used in the prototype.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SEASON = 2026
USER_AGENT = "Mozilla/5.0 (compatible; KBO Player Canvas research prototype)"

TARGET_PLAYERS = [
    {"player_name": "박영현", "team_hint": "KT", "role": "pitcher"},
    {"player_name": "소형준", "team_hint": "KT", "role": "pitcher"},
    {"player_name": "최원준", "team_hint": "KT", "role": "hitter"},
    {"player_name": "안현민", "team_hint": "KT", "role": "hitter"},
    {"player_name": "원태인", "team_hint": "삼성", "role": "pitcher"},
    {"player_name": "박성한", "team_hint": "SSG", "role": "hitter"},
    {"player_name": "김주원", "team_hint": "NC", "role": "hitter"},
    {"player_name": "김진욱", "team_hint": "롯데", "role": "pitcher"},
    {"player_name": "김도영", "team_hint": "KIA", "role": "hitter"},
    {"player_name": "심우준", "team_hint": "한화", "role": "hitter"},
]


@dataclass(frozen=True)
class SourcePage:
    key: str
    category: str
    url: str


SOURCE_PAGES = [
    SourcePage("hitter_basic1", "hitter", "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx"),
    SourcePage("hitter_basic2", "hitter", "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic2.aspx"),
    SourcePage("hitter_detail1", "hitter", "https://www.koreabaseball.com/Record/Player/HitterBasic/Detail1.aspx"),
    SourcePage("pitcher_basic1", "pitcher", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx"),
    SourcePage("pitcher_basic2", "pitcher", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic2.aspx"),
    SourcePage("pitcher_detail1", "pitcher", "https://www.koreabaseball.com/Record/Player/PitcherBasic/Detail1.aspx"),
    SourcePage("defense_basic", "defense", "https://www.koreabaseball.com/Record/Player/Defense/Basic.aspx"),
    SourcePage("runner_basic", "runner", "https://www.koreabaseball.com/Record/Player/Runner/Basic.aspx"),
]


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    collected = []
    for source in SOURCE_PAGES:
        frame = read_first_table(source.url)
        frame.insert(0, "source_key", source.key)
        frame.insert(1, "source_category", source.category)
        frame.insert(2, "source_url", source.url)
        frame.insert(3, "collected_at", datetime.now().isoformat(timespec="seconds"))
        raw_path = RAW_DIR / f"kbo_{source.key}_{SEASON}.csv"
        frame.to_csv(raw_path, index=False, encoding="utf-8-sig")
        collected.append(frame)
        print(f"saved {raw_path.relative_to(PROJECT_ROOT)} rows={len(frame)} cols={len(frame.columns)}")

    combined = pd.concat(collected, ignore_index=True, sort=False)
    combined_path = RAW_DIR / f"kbo_official_combined_{SEASON}.csv"
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")
    print(f"saved {combined_path.relative_to(PROJECT_ROOT)} rows={len(combined)}")

    snapshot = build_target_snapshot(combined, TARGET_PLAYERS)
    snapshot_path = PROCESSED_DIR / f"kbo_target_players_snapshot_{SEASON}.csv"
    snapshot.to_csv(snapshot_path, index=False, encoding="utf-8-sig")
    print(f"saved {snapshot_path.relative_to(PROJECT_ROOT)} rows={len(snapshot)}")

    missing = build_missing_report(snapshot, TARGET_PLAYERS)
    missing_path = PROCESSED_DIR / f"kbo_target_players_missing_{SEASON}.csv"
    missing.to_csv(missing_path, index=False, encoding="utf-8-sig")
    print(f"saved {missing_path.relative_to(PROJECT_ROOT)} rows={len(missing)}")


def read_first_table(url: str) -> pd.DataFrame:
    storage_options = {"User-Agent": USER_AGENT}
    tables = pd.read_html(url, encoding="utf-8", storage_options=storage_options)
    if not tables:
        raise RuntimeError(f"No HTML table found: {url}")
    frame = tables[0].copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def build_target_snapshot(combined: pd.DataFrame, targets: Iterable[dict[str, str]]) -> pd.DataFrame:
    rows = []
    for target in targets:
        name = target["player_name"]
        matches = combined[combined["선수명"].astype(str).eq(name)].copy()
        if "팀명" in matches.columns:
            same_team = matches["팀명"].astype(str).eq(target["team_hint"])
            matches = matches[same_team | ~matches["팀명"].notna()]
        if matches.empty:
            rows.append(
                {
                    "player_name": name,
                    "team_hint": target["team_hint"],
                    "role": target["role"],
                    "source_key": "",
                    "matched": False,
                    "note": "KBO official ranking/source first page에서 발견되지 않음",
                }
            )
            continue
        for _, row in matches.iterrows():
            item = {
                "player_name": name,
                "team_hint": target["team_hint"],
                "role": target["role"],
                "source_key": row.get("source_key", ""),
                "source_category": row.get("source_category", ""),
                "matched": True,
                "note": "",
            }
            for column in matches.columns:
                if column not in item and column not in {"source_url", "collected_at"}:
                    item[column] = row.get(column)
            rows.append(item)
    return pd.DataFrame(rows)


def build_missing_report(snapshot: pd.DataFrame, targets: Iterable[dict[str, str]]) -> pd.DataFrame:
    rows = []
    for target in targets:
        name = target["player_name"]
        player_rows = snapshot[snapshot["player_name"].eq(name)]
        matched_sources = sorted(player_rows[player_rows["matched"].eq(True)]["source_key"].dropna().astype(str).unique())
        rows.append(
            {
                "player_name": name,
                "team_hint": target["team_hint"],
                "role": target["role"],
                "matched_source_count": len(matched_sources),
                "matched_sources": ", ".join(matched_sources),
                "needs_follow_up": len(matched_sources) == 0,
                "recommended_next_step": "선수 상세 페이지 또는 Statiz에서 보강" if len(matched_sources) == 0 else "",
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    main()

