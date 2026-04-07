# Henrik Dev API Documentation

## Base URL

```
https://api.henrikdev.xyz
```

## Authentication

Optional API key via `Authorization` header. Without key: 30 requests/minute.

## Endpoints Used

### Account
```
GET /valorant/v1/account/{name}/{tag}
```
Returns: name, tag, account_level, region, card (small/wide/large images).

### MMR (Rank)
```
GET /valorant/v2/mmr/{region}/{name}/{tag}
```
Returns: current_data (currenttier, currenttierpatched, ranking_in_tier, mmr_change_to_last_game), highest_rank.

Regions: `eu`, `na`, `ap`, `kr`, `br`, `latam`.

### MMR History
```
GET /valorant/v1/mmr-history/{region}/{name}/{tag}
```
Returns: array of MMR changes per match.

### Matches
```
GET /valorant/v3/matches/{region}/{name}/{tag}?filter={mode}&size={n}
```
Modes: `competitive`, `unrated`, `deathmatch`, `spikerush`.
Returns: metadata (map, mode, matchid, game_start_patched), players.all_players (name, tag, character, team, stats), teams (has_won, rounds_won, rounds_lost).

### Leaderboard
```
GET /valorant/v2/leaderboard/{region}?start={n}&size={n}
```
Returns: array of {gameName, tagLine, leaderboardRank, rankedRating, numberOfWins}.

## Rate Limiting

- Free tier: 30 requests/minute
- Client-side enforcement: 2-second minimum interval between requests
- SQLite cache layer: 5-minute TTL (default), 2-minute for matches, 1-hour for leaderboard

## Error Handling

- 404: player not found (return None)
- 429: rate limited (return None, log warning)
- Other errors: log and return None

## Valorant API (Assets)

```
https://valorant-api.com
```

No authentication required.

### Agents
```
GET /v1/agents?isPlayableCharacter=true
```
Returns: uuid, displayName, description, role (displayName, displayIcon), abilities (slot, displayName, description, displayIcon), displayIcon, fullPortrait.

### Maps
```
GET /v1/maps
```
Returns: uuid, displayName, listViewIcon, splash, displayIcon (minimap), coordinates, callouts (regionName, superRegionName, location).
