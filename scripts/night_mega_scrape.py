#!/usr/bin/env python3
"""ValoCheck Mega Night Scraper — builds own player database.

Does NOT use Henrik API. Uses:
1. Riot API (dev key) — account lookup, 20 req/sec
2. valorant-api.com — agents, maps, seasons (free, no limits)
3. Local leaderboard data — 2000 players already scraped

What it does:
- Loads all 2000 leaderboard players
- Looks up each via Riot API → gets PUUID
- Saves to our SQLite players table
- Refreshes all agent/map/season data
- Cleans expired cache
- Reports stats

Time: ~5 minutes for 2000 players (Riot API = 20 req/sec)
Run: RIOT_API_KEY=xxx venv/bin/python3 scripts/night_mega_scrape.py
"""

import json
import logging
import os
import sqlite3
import sys
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "data", "cache.db")
STATIC = os.path.join(BASE, "app", "static")

RIOT_KEY = os.environ.get("RIOT_API_KEY", "")
RIOT_RATE = 0.06  # 20 req/sec = 50ms between requests, use 60ms for safety

# Region routing for Riot Account API
ROUTING = {
    "eu": "europe",
    "na": "americas",
    "ap": "asia",
    "kr": "asia",
    "br": "americas",
    "latam": "americas",
}

session = requests.Session()
last_riot_req = 0.0
stats = {"looked_up": 0, "saved": 0, "errors": 0, "cached": 0}


def riot_get(url: str) -> dict | None:
    """Rate-limited Riot API request."""
    global last_riot_req
    if not RIOT_KEY:
        return None
    elapsed = time.time() - last_riot_req
    if elapsed < RIOT_RATE:
        time.sleep(RIOT_RATE - elapsed)
    last_riot_req = time.time()
    try:
        resp = session.get(url, headers={"X-Riot-Token": RIOT_KEY}, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429:
            retry = int(resp.headers.get("Retry-After", 5))
            logger.warning("Riot rate limited, waiting %ds", retry)
            time.sleep(retry)
            resp = session.get(url, headers={"X-Riot-Token": RIOT_KEY}, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        if resp.status_code == 401:
            logger.error("Riot API key expired!")
            return None
        return None
    except Exception as e:
        logger.error("Riot error: %s", e)
        return None


def init_db(db: sqlite3.Connection) -> None:
    """Ensure tables exist."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS players (
            name TEXT NOT NULL,
            tag TEXT NOT NULL,
            region TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            puuid TEXT DEFAULT '',
            last_seen REAL NOT NULL,
            PRIMARY KEY (name, tag)
        )
    """)
    # Add puuid column if missing (migration)
    try:
        db.execute("ALTER TABLE players ADD COLUMN puuid TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass  # Column already exists
    db.execute("CREATE INDEX IF NOT EXISTS idx_players_name ON players(name COLLATE NOCASE)")
    db.commit()


def save_player(db: sqlite3.Connection, name: str, tag: str, region: str = "",
                rank: str = "", puuid: str = "") -> None:
    db.execute(
        "INSERT OR REPLACE INTO players (name, tag, region, rank, puuid, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
        (name, tag, region, rank, puuid, time.time()),
    )


def load_leaderboard_players() -> list[dict]:
    """Load all players from leaderboard JSON files."""
    lb_dir = os.path.join(BASE, "data", "leaderboard")
    players = []
    seen = set()
    for region in ["eu", "na", "ap", "kr"]:
        fpath = os.path.join(lb_dir, f"{region}.json")
        if not os.path.exists(fpath):
            continue
        try:
            with open(fpath) as f:
                data = json.load(f)
            for p in data:
                name = p.get("name", "")
                tag = p.get("tag", "")
                if name and tag:
                    key = f"{name}#{tag}".lower()
                    if key not in seen:
                        seen.add(key)
                        players.append({
                            "name": name,
                            "tag": tag,
                            "region": region,
                            "rank": f"#{p.get('rank', 0)}",
                            "rr": p.get("rr", 0),
                        })
        except (json.JSONDecodeError, OSError):
            continue
    return players


def phase1_riot_lookup(db: sqlite3.Connection, players: list[dict]) -> None:
    """Phase 1: Look up all players via Riot API to get PUUIDs."""
    if not RIOT_KEY:
        logger.warning("No RIOT_API_KEY, skipping Riot lookups")
        return

    logger.info("Phase 1: Riot API lookup for %d players...", len(players))
    for i, p in enumerate(players):
        name, tag, region = p["name"], p["tag"], p["region"]
        routing = ROUTING.get(region, "europe")

        # Check if already in DB with PUUID
        row = db.execute("SELECT puuid FROM players WHERE name = ? AND tag = ?", (name, tag)).fetchone()
        if row and row[0]:
            stats["cached"] += 1
            if (i + 1) % 200 == 0:
                logger.info("  [%d/%d] %d new, %d cached, %d errors",
                            i + 1, len(players), stats["saved"], stats["cached"], stats["errors"])
            continue

        url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
        data = riot_get(url)
        stats["looked_up"] += 1

        if data and "puuid" in data:
            save_player(db, data.get("gameName", name), data.get("tagLine", tag),
                       region, p.get("rank", ""), data["puuid"])
            stats["saved"] += 1
        else:
            # Save without PUUID
            save_player(db, name, tag, region, p.get("rank", ""), "")
            stats["errors"] += 1

        if (i + 1) % 100 == 0:
            db.commit()
            logger.info("  [%d/%d] %d new, %d cached, %d errors",
                        i + 1, len(players), stats["saved"], stats["cached"], stats["errors"])

    db.commit()
    logger.info("Phase 1 done: %d looked up, %d saved, %d cached, %d errors",
                stats["looked_up"], stats["saved"], stats["cached"], stats["errors"])


def phase2_refresh_assets() -> None:
    """Phase 2: Refresh agent/map/season data from valorant-api.com."""
    logger.info("Phase 2: Refreshing assets from valorant-api.com...")

    # Agents
    try:
        resp = session.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true", timeout=15)
        resp.raise_for_status()
        agents = []
        for a in resp.json().get("data", []):
            name = a.get("displayName", "")
            slug = name.lower().replace("/", "-").replace("'", "").replace(" ", "-")
            if not slug:
                continue
            role = a.get("role") or {}
            abilities = []
            for ab in a.get("abilities", []):
                abilities.append({
                    "slot": ab.get("slot", ""),
                    "name": ab.get("displayName", ""),
                    "description": ab.get("description", ""),
                })
            agents.append({
                "uuid": a.get("uuid", ""),
                "name": name,
                "slug": slug,
                "description": a.get("description", ""),
                "role": role.get("displayName", ""),
                "abilities": abilities,
                "icon": f"/static/img/agents/{slug}.png",
            })

            # Download icon
            icon_url = a.get("displayIcon", "")
            icon_path = os.path.join(STATIC, "img", "agents", f"{slug}.png")
            if icon_url and not os.path.exists(icon_path):
                try:
                    img = session.get(icon_url, timeout=10)
                    img.raise_for_status()
                    os.makedirs(os.path.dirname(icon_path), exist_ok=True)
                    with open(icon_path, "wb") as f:
                        f.write(img.content)
                except Exception:
                    pass

        agents.sort(key=lambda x: x["name"])
        with open(os.path.join(STATIC, "data", "agents.json"), "w") as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)
        logger.info("  Saved %d agents", len(agents))
    except Exception as e:
        logger.error("  Agents error: %s", e)

    # Maps
    try:
        resp = session.get("https://valorant-api.com/v1/maps", timeout=15)
        resp.raise_for_status()
        maps = []
        for m in resp.json().get("data", []):
            name = m.get("displayName", "")
            slug = name.lower().replace(" ", "-").replace("'", "")
            if not slug or slug == "the-range":
                continue
            splash_url = m.get("splash", "") or m.get("listViewIcon", "")
            splash_path = os.path.join(STATIC, "img", "maps", f"{slug}.png")
            if splash_url and not os.path.exists(splash_path):
                try:
                    img = session.get(splash_url, timeout=10)
                    img.raise_for_status()
                    os.makedirs(os.path.dirname(splash_path), exist_ok=True)
                    with open(splash_path, "wb") as f:
                        f.write(img.content)
                except Exception:
                    pass

            callouts = []
            for c in m.get("callouts") or []:
                callouts.append({
                    "region": c.get("regionName", ""),
                    "super_region": c.get("superRegionName", ""),
                })
            maps.append({
                "uuid": m.get("uuid", ""),
                "name": name,
                "slug": slug,
                "coordinates": m.get("coordinates", ""),
                "splash": f"/static/img/maps/{slug}.png",
                "callouts": callouts,
            })
        maps.sort(key=lambda x: x["name"])
        with open(os.path.join(STATIC, "data", "maps.json"), "w") as f:
            json.dump(maps, f, ensure_ascii=False, indent=2)
        logger.info("  Saved %d maps", len(maps))
    except Exception as e:
        logger.error("  Maps error: %s", e)

    # Seasons
    try:
        resp = session.get("https://valorant-api.com/v1/seasons", timeout=15)
        resp.raise_for_status()
        seasons = []
        for s in resp.json().get("data", []):
            seasons.append({
                "uuid": s.get("uuid", ""),
                "name": s.get("displayName", ""),
                "type": s.get("type", ""),
                "start": s.get("startTime", ""),
                "end": s.get("endTime", ""),
                "parent": s.get("parentUuid", ""),
            })
        with open(os.path.join(STATIC, "data", "seasons.json"), "w") as f:
            json.dump(seasons, f, indent=2)
        logger.info("  Saved %d seasons", len(seasons))
    except Exception as e:
        logger.error("  Seasons error: %s", e)


def phase3_clean_cache(db: sqlite3.Connection) -> None:
    """Phase 3: Clean expired cache entries."""
    logger.info("Phase 3: Cleaning cache...")
    try:
        deleted = db.execute("DELETE FROM cache WHERE expires_at < ?", (time.time(),)).rowcount
        db.execute("VACUUM")
        db.commit()
        logger.info("  Cleaned %d expired entries", deleted)
    except Exception as e:
        logger.error("  Cache clean error: %s", e)


def phase4_report(db: sqlite3.Connection) -> None:
    """Phase 4: Generate report."""
    total_players = db.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    with_puuid = db.execute("SELECT COUNT(*) FROM players WHERE puuid != ''").fetchone()[0]
    cache_size = db.execute("SELECT COUNT(*) FROM cache").fetchone()[0]

    logger.info("=" * 50)
    logger.info("NIGHT SCRAPE REPORT")
    logger.info("=" * 50)
    logger.info("Players in DB:     %d", total_players)
    logger.info("With PUUID:        %d", with_puuid)
    logger.info("Cache entries:     %d", cache_size)
    logger.info("Riot lookups:      %d", stats["looked_up"])
    logger.info("New saves:         %d", stats["saved"])
    logger.info("Already cached:    %d", stats["cached"])
    logger.info("Errors:            %d", stats["errors"])
    logger.info("=" * 50)

    # Save report to file
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_players": total_players,
        "with_puuid": with_puuid,
        "cache_entries": cache_size,
        "riot_lookups": stats["looked_up"],
        "new_saves": stats["saved"],
        "errors": stats["errors"],
    }
    report_path = os.path.join(BASE, "data", "scrape_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)


def main():
    logger.info("ValoCheck Night Mega Scraper starting...")
    logger.info("Riot API key: %s", "present" if RIOT_KEY else "MISSING")

    # Init DB
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    init_db(db)

    # Load leaderboard players
    players = load_leaderboard_players()
    logger.info("Loaded %d players from leaderboard files", len(players))

    # Phase 1: Riot API lookups
    phase1_riot_lookup(db, players)

    # Phase 2: Refresh assets
    phase2_refresh_assets()

    # Phase 3: Clean cache
    phase3_clean_cache(db)

    # Phase 4: Report
    phase4_report(db)

    db.close()
    logger.info("Done!")


if __name__ == "__main__":
    main()
