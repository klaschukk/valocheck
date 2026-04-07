#!/usr/bin/env python3
"""Scrape agent meta stats from leaderboard players' matches.

Takes top players from leaderboard, fetches their recent matches,
and aggregates agent pick/win rates across all matches.

Saves to: app/static/data/agent_meta.json

Time estimate: ~5-10 minutes (fetches 50 players x ~2s rate limit)
Run: HENRIK_API_KEY=your_key venv/bin/python3 scripts/scrape_agent_meta.py
"""

import json
import logging
import os
import sys
import time
from collections import defaultdict

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_URL = "https://api.henrikdev.xyz"
API_KEY = os.environ.get("HENRIK_API_KEY", "")
RATE_LIMIT = 2.1  # seconds between requests

session = requests.Session()
if API_KEY:
    session.headers["Authorization"] = API_KEY
session.headers["Accept"] = "application/json"

last_req = 0.0


def api_get(path: str) -> dict | list | None:
    global last_req
    elapsed = time.time() - last_req
    if elapsed < RATE_LIMIT:
        time.sleep(RATE_LIMIT - elapsed)
    last_req = time.time()

    try:
        resp = session.get(f"{API_URL}{path}", timeout=15)
        if resp.status_code in (404, 429):
            return None
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", data)
    except Exception as e:
        logger.error("API error %s: %s", path, e)
        return None


def main():
    # Load top players from leaderboard
    lb_dir = os.path.join(BASE, "data", "leaderboard")
    players_to_check = []

    for region in ["eu", "na", "ap", "kr"]:
        fpath = os.path.join(lb_dir, f"{region}.json")
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            lb = json.load(f)
        # Take top 12 from each region with valid names
        count = 0
        for p in lb:
            name, tag = p.get("name", ""), p.get("tag", "")
            if name and tag and count < 12:
                players_to_check.append((name, tag, region))
                count += 1

    logger.info("Checking %d players across 4 regions", len(players_to_check))

    # Aggregate agent stats across all matches
    agent_data: dict[str, dict] = defaultdict(lambda: {
        "picks": 0, "wins": 0, "kills": 0, "deaths": 0,
        "assists": 0, "rounds": 0, "score": 0
    })
    total_matches = 0

    for i, (name, tag, region) in enumerate(players_to_check):
        logger.info("[%d/%d] Fetching matches for %s#%s (%s)",
                    i + 1, len(players_to_check), name, tag, region)

        matches = api_get(f"/valorant/v3/matches/{region}/{name}/{tag}?filter=competitive&size=5")
        if not matches or not isinstance(matches, list):
            continue

        for match in matches:
            all_players = match.get("players", {}).get("all_players", [])
            teams_data = match.get("teams", {})
            metadata = match.get("metadata", {})
            rounds_played = metadata.get("rounds_played", 0)

            for player in all_players:
                agent = player.get("character", "Unknown")
                if not agent or agent == "Unknown":
                    continue

                team = player.get("team", "").lower()
                won = False
                if team in teams_data:
                    won = teams_data[team].get("has_won", False)

                stats = player.get("stats", {})
                kills = stats.get("kills", 0)
                deaths = stats.get("deaths", 0)
                assists = stats.get("assists", 0)
                score = stats.get("score", 0)

                # Count rounds from team data
                match_rounds = 0
                if team in teams_data:
                    match_rounds = teams_data[team].get("rounds_won", 0) + teams_data[team].get("rounds_lost", 0)

                ad = agent_data[agent]
                ad["picks"] += 1
                if won:
                    ad["wins"] += 1
                ad["kills"] += kills
                ad["deaths"] += deaths
                ad["assists"] += assists
                ad["rounds"] += match_rounds
                ad["score"] += score

            total_matches += 1

    if not agent_data:
        logger.warning("No data collected!")
        return

    # Calculate rates
    total_picks = sum(a["picks"] for a in agent_data.values())
    result = []
    for agent, d in sorted(agent_data.items(), key=lambda x: x[1]["picks"], reverse=True):
        pick_rate = round(d["picks"] / max(total_picks, 1) * 100, 1)
        win_rate = round(d["wins"] / max(d["picks"], 1) * 100, 1)
        kd = round(d["kills"] / max(d["deaths"], 1), 2)
        acs = round(d["score"] / max(d["rounds"], 1))
        kill_pct = round(d["kills"] / max(d["rounds"], 1) * 100, 1)

        result.append({
            "agent": agent,
            "picks": d["picks"],
            "pick_rate": pick_rate,
            "win_rate": win_rate,
            "kd": kd,
            "acs": acs,
            "kill_pct": kill_pct,
            "total_kills": d["kills"],
            "total_deaths": d["deaths"],
        })

    out_path = os.path.join(BASE, "app", "static", "data", "agent_meta.json")
    with open(out_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("Done! %d agents from %d matches. Saved to %s", len(result), total_matches, out_path)


if __name__ == "__main__":
    main()
