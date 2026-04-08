"""Direct Riot Games API client.

Uses official Riot API endpoints instead of Henrik wrapper.
Rate limit: 20 req/sec (Development), 500 req/10sec (Production).

Endpoints:
- Account: https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}
- Matches: https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}
- Match detail: https://{region}.api.riotgames.com/val/match/v1/matches/{matchId}
- Leaderboard: https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{actId}
- MMR: Uses Henrik API as fallback (Riot doesn't expose MMR directly)

Region routing:
- Account API: americas, europe, asia (routing values)
- Val API: eu, na, ap, kr, br, latam (platform)
"""

import logging
import time
from typing import Any

import requests
from flask import current_app

from app.db import cache_get, cache_set

logger = logging.getLogger(__name__)

# Riot ID region -> Account API routing
ACCOUNT_ROUTING = {
    "eu": "europe",
    "na": "americas",
    "ap": "asia",
    "kr": "asia",
    "br": "americas",
    "latam": "americas",
}

# Riot val platform routing
VAL_PLATFORM = {
    "eu": "eu",
    "na": "na",
    "ap": "ap",
    "kr": "kr",
    "br": "br",
    "latam": "latam",
}


class RiotAPI:
    """Direct Riot Games API client."""

    def __init__(self):
        self.session = requests.Session()
        self._last_request = 0.0
        self._min_interval = 0.1  # 20 req/sec for dev key

    def _get_key(self) -> str:
        return current_app.config.get("RIOT_API_KEY", "")

    def _rate_limit(self) -> None:
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()

    def _request(self, url: str, cache_key: str = "", cache_ttl: int = 300) -> dict | list | None:
        if cache_key:
            cached = cache_get(cache_key)
            if cached is not None:
                return cached

        key = self._get_key()
        if not key:
            return None

        self._rate_limit()
        try:
            resp = self.session.get(url, headers={"X-Riot-Token": key}, timeout=10)
            if resp.status_code == 404:
                return None
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 5))
                logger.warning("Riot API rate limited, waiting %ds", retry_after)
                time.sleep(retry_after)
                resp = self.session.get(url, headers={"X-Riot-Token": key}, timeout=10)
            if resp.status_code == 401:
                logger.error("Riot API key expired or invalid")
                return None
            resp.raise_for_status()
            data = resp.json()
            if cache_key:
                cache_set(cache_key, data, ttl=cache_ttl)
            return data
        except requests.RequestException as e:
            logger.error("Riot API error: %s — %s", url, e)
            return None

    def get_account(self, name: str, tag: str, region: str = "eu") -> dict | None:
        """Get account by Riot ID (name#tag)."""
        routing = ACCOUNT_ROUTING.get(region, "europe")
        url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
        return self._request(url, cache_key=f"riot:account:{name}:{tag}", cache_ttl=3600)

    def get_matchlist(self, puuid: str, region: str = "eu") -> list | None:
        """Get match IDs for a player."""
        platform = VAL_PLATFORM.get(region, "eu")
        url = f"https://{platform}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
        return self._request(url, cache_key=f"riot:matchlist:{puuid}", cache_ttl=120)

    def get_match(self, match_id: str, region: str = "eu") -> dict | None:
        """Get full match details."""
        platform = VAL_PLATFORM.get(region, "eu")
        url = f"https://{platform}.api.riotgames.com/val/match/v1/matches/{match_id}"
        return self._request(url, cache_key=f"riot:match:{match_id}", cache_ttl=86400)

    def get_leaderboard(self, act_id: str, region: str = "eu", size: int = 200, start: int = 0) -> dict | None:
        """Get ranked leaderboard for an act."""
        platform = VAL_PLATFORM.get(region, "eu")
        url = f"https://{platform}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}?size={size}&startIndex={start}"
        return self._request(url, cache_key=f"riot:lb:{region}:{act_id}:{start}", cache_ttl=3600)


riot_api = RiotAPI()
