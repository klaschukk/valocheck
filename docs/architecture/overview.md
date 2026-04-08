# Architecture Overview

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python 3.12) |
| DB | SQLite (player/match cache, WAL mode) |
| WSGI | Gunicorn (2 workers, port 5001) |
| Reverse proxy | nginx (port 80 for domain, port 5080 for IP access) |
| SSL | Cloudflare (Full mode) — when domain is set up |
| Process | systemd (valocheck.service) |
| API | Henrik Dev API (primary) + Riot Games API (prepared) |
| Assets | valorant-api.com (agents, maps, ranks) |
| Fonts | Google Fonts: Russo One + Chakra Petch |

## Project Structure

```
valocheck/
├── CLAUDE.md                ← compact index (~80 lines)
├── README.md
├── config.py                ← Config (SECRET_KEY, API keys, DB_PATH, BASE_URL)
├── run.py                   ← dev server (port 5001)
├── requirements.txt
├── app/
│   ├── __init__.py          ← create_app(), blueprints, error handlers
│   ├── db.py                ← SQLite: cache + players table
│   ├── riot_api.py          ← Henrik API client + player profile builder
│   ├── riot_direct.py       ← Direct Riot API client (prepared, needs prod key)
│   ├── routes/
│   │   ├── main.py          ← /, /search, /health, /robots.txt, /sitemap.xml
│   │   ├── player.py        ← /player/, /compare/, /match/
│   │   ├── leaderboard.py   ← /leaderboard/
│   │   ├── content.py       ← /agents/, /maps/, /insights/, /crosshairs/, /tips/, /about/
│   │   └── api.py           ← /api/search, /api/autocomplete
│   ├── templates/           ← 17 Jinja2 templates + 2 partials
│   └── static/
│       ├── css/app.css      ← single CSS (~900 lines), Valorant HUD theme
│       ├── data/             ← agents.json, maps.json, agent_meta.json, pro_crosshairs.json
│       ├── img/              ← agents/, maps/, favicons, og.png
│       └── site.webmanifest
├── scripts/
│   ├── fetch_leaderboard.py ← cron: top 500 x 4 regions (every 6h)
│   ├── fetch_content.py     ← agents + maps from valorant-api.com
│   ├── scrape_agent_meta.py ← agent pick/win rates from top player matches
│   ├── scrape_pro_crosshairs.py ← 20 pro player crosshair presets
│   ├── healthcheck.sh       ← cron: */5 min, auto-restart
│   └── nightly_refresh.sh   ← cron: 3:00 AM, all scrapers + cache cleanup
├── data/
│   ├── cache.db             ← SQLite (gitignored)
│   └── leaderboard/         ← JSON per region (gitignored)
├── docs/                    ← detailed documentation (see docs/README.md)
├── tests/                   ← 66 pytest tests
└── .claude/
    └── settings.json        ← auto-allow permissions
```

## URL Architecture

```
/                              ← home (hero + search + top players + agents + maps)
/search?q=Name%23TAG           ← search redirect
/player/{name}/{tag}/          ← player profile (banner + stats + chart + matches)
/player/{name}/{tag}/matches/  ← full match history
/player/{name}/{tag}/agents/   ← agent breakdown
/match/{id}/                   ← match detail (10-player scoreboard)
/compare/                      ← player comparison (side-by-side)
/leaderboard/                  ← region select
/leaderboard/{region}/         ← regional leaderboard (eu, na, ap, kr, br, latam)
/agents/                       ← all agents grid
/agents/{slug}/                ← agent detail (abilities, role, sidebar)
/maps/                         ← all maps grid with splash previews
/maps/{slug}/                  ← map detail (splash, callouts)
/insights/                     ← agent meta (pick/win rates, role filter)
/crosshairs/                   ← crosshair builder + 20 pro presets
/tips/                         ← 9 gameplay tips by rank
/about/                        ← about page with stats sidebar
/api/search?q=                 ← player search API (JSON)
/api/autocomplete?q=           ← autocomplete from DB + leaderboard
/sitemap.xml                   ← dynamic sitemap (1795+ URLs)
/robots.txt                    ← robots
/health                        ← healthcheck
```
