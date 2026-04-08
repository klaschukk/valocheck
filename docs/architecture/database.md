# Database — SQLite

Path: `data/cache.db` (gitignored)
Mode: WAL (Write-Ahead Logging)

## Tables

### cache
General-purpose key-value cache with TTL.

| Column | Type | Description |
|--------|------|-------------|
| key | TEXT PK | Cache key (e.g. `henrik:/valorant/v1/account/...`) |
| value | TEXT | JSON-serialized data |
| expires_at | REAL | Unix timestamp when entry expires |

TTL defaults: 300s (player data), 120s (matches), 3600s (leaderboard), 86400s (match detail).

### players
Known players database for autocomplete. Grows as users search for players.

| Column | Type | Description |
|--------|------|-------------|
| name | TEXT PK | Player name |
| tag | TEXT PK | Player tag |
| region | TEXT | Region (eu, na, ap, kr) |
| rank | TEXT | Last known rank |
| last_seen | REAL | Unix timestamp of last lookup |

Index: `idx_players_name` on `name COLLATE NOCASE` for fast autocomplete search.

## Functions (app/db.py)

- `cache_get(key)` — get cached value if not expired
- `cache_set(key, value, ttl)` — set cache entry
- `save_player(name, tag, region, rank)` — upsert player for autocomplete
- `search_players(query, limit)` — search players by name LIKE %query%
