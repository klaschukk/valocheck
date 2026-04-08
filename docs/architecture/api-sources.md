# API Sources

## Henrik Dev API (PRIMARY)
Base: `https://api.henrikdev.xyz`
Key: `HENRIK_API_KEY` env var, set in systemd override
Rate: 30 req/min (Standard), 90 req/min (Enhanced — apply for upgrade)

### Endpoints Used
- `GET /valorant/v1/account/{name}/{tag}` — account info (name, tag, level, card)
- `GET /valorant/v2/mmr/{region}/{name}/{tag}` — current rank, RR, peak rank
- `GET /valorant/v1/mmr-history/{region}/{name}/{tag}` — RR history (last 20)
- `GET /valorant/v3/matches/{region}/{name}/{tag}?filter={mode}&size={n}` — match history
- `GET /valorant/v2/leaderboard/{region}?start={n}&size={n}` — leaderboard (returns all players per region)

### Rate Limiting
Client-side: 2s minimum interval between requests.
On 429: wait 10s + retry once (in scraper scripts).

## Riot Games API (PREPARED, NOT ACTIVE)
Client: `app/riot_direct.py`
Status: Dev key expires every 24h. Production key requires OAuth (RSO) for Valorant.
Plan: Apply for production key, implement RSO sign-in for Phase 3.

## Valorant API (ASSETS)
Base: `https://valorant-api.com`
No key required. Free.

- `GET /v1/agents?isPlayableCharacter=true` — all agents with abilities, icons
- `GET /v1/maps` — all maps with splash images, callouts

Scraped on deploy + nightly refresh. Data stored in `app/static/data/agents.json` and `maps.json`.
