import logging
import time
from typing import Any

import requests
from flask import current_app

from app.db import cache_get, cache_set, save_player

logger = logging.getLogger(__name__)

REGIONS = {
    "eu": "Europe",
    "na": "North America",
    "ap": "Asia Pacific",
    "kr": "Korea",
    "br": "Brazil",
    "latam": "Latin America",
}

RANK_TIERS = [
    "Unrated", "Iron 1", "Iron 2", "Iron 3",
    "Bronze 1", "Bronze 2", "Bronze 3",
    "Silver 1", "Silver 2", "Silver 3",
    "Gold 1", "Gold 2", "Gold 3",
    "Platinum 1", "Platinum 2", "Platinum 3",
    "Diamond 1", "Diamond 2", "Diamond 3",
    "Ascendant 1", "Ascendant 2", "Ascendant 3",
    "Immortal 1", "Immortal 2", "Immortal 3",
    "Radiant",
]


class HenrikAPI:
    """Client for Henrik Dev Valorant API."""

    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz"
        self.session = requests.Session()
        self._last_request = 0.0
        self._min_interval = 2.0  # 30 req/min = 1 per 2 sec

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        key = current_app.config.get("HENRIK_API_KEY")
        if key:
            headers["Authorization"] = key
        return headers

    def _rate_limit(self) -> None:
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()

    def _get(self, path: str, cache_ttl: int = 300) -> dict[str, Any] | None:
        cache_key = f"henrik:{path}"
        cached = cache_get(cache_key)
        if cached is not None:
            return cached

        self._rate_limit()
        url = f"{self.base_url}{path}"
        try:
            resp = self.session.get(url, headers=self._headers(), timeout=10)
            if resp.status_code == 404:
                return None
            if resp.status_code == 429:
                logger.warning("Henrik API rate limited")
                return None
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == 200 or "data" in data:
                result = data.get("data", data)
                cache_set(cache_key, result, ttl=cache_ttl)
                return result
            return None
        except requests.RequestException as e:
            logger.error("Henrik API error: %s — %s", url, e)
            return None

    def get_account(self, name: str, tag: str) -> dict[str, Any] | None:
        return self._get(f"/valorant/v1/account/{name}/{tag}")

    def get_mmr(self, name: str, tag: str, region: str = "eu") -> dict[str, Any] | None:
        return self._get(f"/valorant/v2/mmr/{region}/{name}/{tag}")

    def get_mmr_history(self, name: str, tag: str, region: str = "eu") -> list[dict] | None:
        return self._get(f"/valorant/v1/mmr-history/{region}/{name}/{tag}")

    def get_matches(self, name: str, tag: str, region: str = "eu", mode: str = "competitive",
                    size: int = 10) -> list[dict] | None:
        return self._get(f"/valorant/v3/matches/{region}/{name}/{tag}?filter={mode}&size={size}", cache_ttl=120)

    def get_leaderboard(self, region: str = "eu", start: int = 0, size: int = 100) -> list[dict] | None:
        return self._get(f"/valorant/v2/leaderboard/{region}?start={start}&size={size}", cache_ttl=3600)


henrik_api = HenrikAPI()


def get_player_profile(name: str, tag: str) -> dict[str, Any] | None:
    """Fetch complete player profile: account + MMR + recent matches."""
    account = henrik_api.get_account(name, tag)
    if not account:
        return None

    # Try multiple regions for MMR
    mmr = None
    player_region = account.get("region", "eu") or "eu"
    for region in [player_region, "eu", "na", "ap", "kr"]:
        mmr = henrik_api.get_mmr(name, tag, region)
        if mmr:
            break

    matches_raw = henrik_api.get_matches(name, tag, player_region) or []

    # Fetch MMR history for rank graph
    mmr_history_raw = henrik_api.get_mmr_history(name, tag, player_region) or []
    mmr_history = []
    for h in mmr_history_raw[:20]:
        mmr_history.append({
            "rank": h.get("currenttierpatched", ""),
            "rr": h.get("ranking_in_tier", 0),
            "change": h.get("mmr_change_to_last_game", 0),
            "elo": h.get("elo", 0),
            "date": h.get("date_raw", 0),
        })

    # Process matches
    matches = []
    total_kills, total_deaths, total_assists = 0, 0, 0
    total_headshots, total_bodyshots, total_legshots = 0, 0, 0
    total_score, total_rounds, total_damage = 0, 0, 0
    total_first_bloods = 0
    wins, losses = 0, 0
    agent_stats: dict[str, dict] = {}
    map_stats: dict[str, dict] = {}

    for match in matches_raw:
        # Cache full match data for match detail page
        match_id = match.get("metadata", {}).get("matchid", "")
        if match_id:
            cache_set(f"match:{match_id}", match, ttl=86400)  # 24h

        metadata = match.get("metadata", {})
        players = match.get("players", {})
        all_players = players.get("all_players", [])

        # Find this player
        player_data = None
        for p in all_players:
            p_name = p.get("name", "").lower()
            p_tag = p.get("tag", "").lower()
            if p_name == name.lower() and p_tag == tag.lower():
                player_data = p
                break

        if not player_data:
            continue

        stats = player_data.get("stats", {})
        kills = stats.get("kills", 0)
        deaths = stats.get("deaths", 0)
        assists = stats.get("assists", 0)
        headshots = stats.get("headshots", 0)
        bodyshots = stats.get("bodyshots", 0)
        legshots = stats.get("legshots", 0)
        score = stats.get("score", 0)
        agent_name = player_data.get("character", "Unknown")
        team = player_data.get("team", "").lower()
        damage_made = player_data.get("damage_made", 0) or 0
        damage_received = player_data.get("damage_received", 0) or 0

        total_kills += kills
        total_deaths += deaths
        total_assists += assists
        total_headshots += headshots
        total_bodyshots += bodyshots
        total_legshots += legshots
        total_score += score
        total_damage += damage_made

        # Determine win/loss
        teams_data = match.get("teams", {})
        won = False
        if team in teams_data:
            won = teams_data[team].get("has_won", False)

        if won:
            wins += 1
        else:
            losses += 1

        # Map stats
        map_name = metadata.get("map", "Unknown")
        if map_name not in map_stats:
            map_stats[map_name] = {"games": 0, "wins": 0, "kills": 0, "deaths": 0}
        map_stats[map_name]["games"] += 1
        if won:
            map_stats[map_name]["wins"] += 1
        map_stats[map_name]["kills"] += kills
        map_stats[map_name]["deaths"] += deaths

        # Agent stats
        if agent_name not in agent_stats:
            agent_stats[agent_name] = {"games": 0, "wins": 0, "kills": 0, "deaths": 0, "assists": 0}
        agent_stats[agent_name]["games"] += 1
        if won:
            agent_stats[agent_name]["wins"] += 1
        agent_stats[agent_name]["kills"] += kills
        agent_stats[agent_name]["deaths"] += deaths
        agent_stats[agent_name]["assists"] += assists

        # Round scores
        rounds_won = 0
        rounds_lost = 0
        if team in teams_data:
            rounds_won = teams_data[team].get("rounds_won", 0)
            rounds_lost = teams_data[team].get("rounds_lost", 0)

        match_rounds = rounds_won + rounds_lost
        total_rounds += match_rounds
        match_acs = round(score / max(match_rounds, 1))

        matches.append({
            "map": metadata.get("map", "Unknown"),
            "mode": metadata.get("mode", ""),
            "agent": agent_name,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kd_diff": kills - deaths,
            "won": won,
            "rounds_won": rounds_won,
            "rounds_lost": rounds_lost,
            "acs": match_acs,
            "damage": damage_made,
            "started_at": metadata.get("game_start_patched", ""),
            "match_id": metadata.get("matchid", ""),
        })

    # Calculate aggregates
    total_games = wins + losses
    kd = round(total_kills / max(total_deaths, 1), 2)
    kad = round((total_kills + total_assists) / max(total_deaths, 1), 2)
    total_shots = total_headshots + total_bodyshots + total_legshots
    hs_pct = round(total_headshots / max(total_shots, 1) * 100, 1)
    win_pct = round(wins / max(total_games, 1) * 100, 1)
    acs = round(total_score / max(total_rounds, 1))
    dmg_per_round = round(total_damage / max(total_rounds, 1), 1)
    kills_per_round = round(total_kills / max(total_rounds, 1), 1)

    # Top agent
    top_agent = max(agent_stats, key=lambda a: agent_stats[a]["games"]) if agent_stats else "Unknown"

    # Process agent stats for display
    agents_display = []
    for agent, s in sorted(agent_stats.items(), key=lambda x: x[1]["games"], reverse=True):
        agents_display.append({
            "name": agent,
            "games": s["games"],
            "wins": s["wins"],
            "win_rate": round(s["wins"] / max(s["games"], 1) * 100, 1),
            "kd": round(s["kills"] / max(s["deaths"], 1), 2),
            "kills": s["kills"],
            "deaths": s["deaths"],
            "assists": s["assists"],
        })

    # MMR data
    current_rank = "Unrated"
    current_rr = 0
    peak_rank = "Unrated"
    rank_tier = 0
    if mmr:
        current_data = mmr.get("current_data", {})
        current_rank = current_data.get("currenttierpatched", "Unrated") or "Unrated"
        current_rr = current_data.get("ranking_in_tier", 0) or 0
        rank_tier = current_data.get("currenttier", 0) or 0
        highest = mmr.get("highest_rank", {})
        peak_rank = highest.get("patched_tier", current_rank) or current_rank

    # Save to players DB for autocomplete
    try:
        save_player(account.get("name", name), account.get("tag", tag), player_region, current_rank)
    except Exception:
        pass  # Don't fail profile load if DB write fails

    return {
        "name": account.get("name", name),
        "tag": account.get("tag", tag),
        "account_level": account.get("account_level", 0),
        "card": account.get("card", {}),
        "region": player_region,
        "current_rank": current_rank,
        "current_rr": current_rr,
        "rank_tier": rank_tier,
        "peak_rank": peak_rank,
        "kd": kd,
        "kad": kad,
        "win_pct": win_pct,
        "hs_pct": hs_pct,
        "acs": acs,
        "dmg_per_round": dmg_per_round,
        "kills_per_round": kills_per_round,
        "total_rounds": total_rounds,
        "top_agent": top_agent,
        "total_kills": total_kills,
        "total_deaths": total_deaths,
        "total_assists": total_assists,
        "wins": wins,
        "losses": losses,
        "total_headshots": total_headshots,
        "total_bodyshots": total_bodyshots,
        "total_legshots": total_legshots,
        "matches": matches,
        "agents": agents_display,
        "maps": [
            {
                "name": m,
                "games": s["games"],
                "wins": s["wins"],
                "win_rate": round(s["wins"] / max(s["games"], 1) * 100, 1),
                "kd": round(s["kills"] / max(s["deaths"], 1), 2),
            }
            for m, s in sorted(map_stats.items(), key=lambda x: x[1]["games"], reverse=True)
        ],
        "mmr_history": mmr_history,
    }
