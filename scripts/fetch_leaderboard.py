#!/usr/bin/env python3
"""Fetch top 500 leaderboard players per region from Henrik Dev API.

Saves JSON files to data/leaderboard/{region}.json.
Run via cron every 6 hours:
  0 */6 * * * /home/klaschuk/valocheck/venv/bin/python3 /home/klaschuk/valocheck/scripts/fetch_leaderboard.py
"""

import json
import logging
import os
import sys
import time

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.henrikdev.xyz"
REGIONS = ["eu", "na", "ap", "kr"]
PAGE_SIZE = 100
MAX_PLAYERS = 500
MIN_INTERVAL = 2.0  # seconds between requests

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "leaderboard")
API_KEY = os.environ.get("HENRIK_API_KEY", "")


def fetch_region(region: str) -> list[dict]:
    """Fetch top MAX_PLAYERS for a region, paginating in chunks of PAGE_SIZE."""
    players: list[dict] = []
    start = 0

    while start < MAX_PLAYERS:
        url = f"{BASE_URL}/valorant/v2/leaderboard/{region}?start={start}&size={PAGE_SIZE}"
        headers = {"Accept": "application/json"}
        if API_KEY:
            headers["Authorization"] = API_KEY

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 429:
                logger.warning("Rate limited on %s at offset %d, stopping", region, start)
                break
            resp.raise_for_status()
            data = resp.json()
            # v2 returns {"players": [...]} or {"data": [...]}
            if isinstance(data, dict):
                page = data.get("players") or data.get("data") or []
            else:
                page = data
            if not page or not isinstance(page, list):
                break

            for p in page:
                if len(players) >= MAX_PLAYERS:
                    break
                players.append({
                    "name": p.get("gameName", ""),
                    "tag": p.get("tagLine", ""),
                    "rank": p.get("leaderboardRank", 0),
                    "rr": p.get("rankedRating", 0),
                    "wins": p.get("numberOfWins", 0),
                })

            logger.info("  %s: fetched %d players", region, len(players))

            if len(page) < PAGE_SIZE:
                break
            start += PAGE_SIZE
            time.sleep(MIN_INTERVAL)

        except requests.RequestException as e:
            logger.error("Error fetching %s at offset %d: %s", region, start, e)
            break

    return players


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    total = 0

    for region in REGIONS:
        logger.info("Fetching leaderboard: %s", region)
        players = fetch_region(region)

        if not players:
            logger.warning("No data for %s, skipping", region)
            continue

        out_path = os.path.join(DATA_DIR, f"{region}.json")
        with open(out_path, "w") as f:
            json.dump(players, f, ensure_ascii=False)
        logger.info("Saved %d players to %s", len(players), out_path)
        total += len(players)
        time.sleep(MIN_INTERVAL)

    logger.info("Done. Total: %d players across %d regions", total, len(REGIONS))


if __name__ == "__main__":
    sys.exit(main() or 0)
