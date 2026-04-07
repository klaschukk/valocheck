# CLAUDE.md — ValoCheck

## Overview

**ValoCheck** — fast, lightweight Valorant stat checker.
Player profiles, leaderboards, agent/map stats. Competitor to tracker.gg but 10x faster and cleaner.

- **URL:** https://valocheck.gg
- **Stack:** Flask + SQLite + Gunicorn + nginx + Cloudflare
- **Target:** programmatic SEO pages (player profiles, leaderboards, agent/map pages)

## Language

- Communication: **Russian**
- Code, commits, comments: **English**

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python 3.12) |
| DB | SQLite (player/match cache, WAL mode) |
| WSGI | Gunicorn (2 workers, port 5001) |
| Reverse proxy | nginx (Cloudflare-only access) |
| SSL | Cloudflare (Full mode) |
| Process | systemd (valocheck.service) |
| API | Henrik Dev API (unofficial, free) + Riot Games API |
| Assets | valorant-api.com (agents, maps, ranks) |

## URL Architecture

```
/                              — home (hero + search)
/search?q=Name%23TAG           — search redirect
/player/{name}/{tag}/          — player profile (rank, K/D, winrate, matches, agents)
/player/{name}/{tag}/matches/  — full match history
/player/{name}/{tag}/agents/   — agent breakdown
/leaderboard/                  — leaderboard index (region select)
/leaderboard/{region}/         — regional leaderboard (eu, na, ap, kr, br, latam)
/agents/                       — all agents index
/agents/{slug}/                — agent detail (abilities, role)
/maps/                         — all maps index
/maps/{slug}/                  — map detail (preview, callouts)
/about/                        — about page
/api/search?q=                 — player search API (JSON)
/sitemap.xml                   — dynamic sitemap
/robots.txt                    — robots
/health                        — healthcheck
```

## Project Structure

```
valocheck/
├── CLAUDE.md
├── README.md
├── config.py               ← Config (SECRET_KEY, API keys, DB_PATH, BASE_URL, CACHE_TTL)
├── run.py                   ← dev server (port 5001)
├── requirements.txt         ← Flask, requests, gunicorn
├── app/
│   ├── __init__.py          ← create_app(), blueprint registration, error handlers
│   ├── db.py                ← SQLite cache (cache_get, cache_set, WAL mode)
│   ├── riot_api.py          ← HenrikAPI client (rate limiting, caching, player profile)
│   ├── routes/
│   │   ├── main.py          ← /, /search, /health, /robots.txt, /sitemap.xml
│   │   ├── player.py        ← /player/{name}/{tag}/, /matches/, /agents/
│   │   ├── leaderboard.py   ← /leaderboard/, /leaderboard/{region}/
│   │   ├── content.py       ← /agents/, /agents/{slug}/, /maps/, /maps/{slug}/, /about/
│   │   └── api.py           ← /api/search
│   ├── templates/
│   │   ├── base.html        ← layout: head (OG, JSON-LD), header, main, footer
│   │   ├── _partials/       ← _header.html, _footer.html
│   │   ├── index.html, player.html, matches.html, agents.html
│   │   ├── leaderboard.html, agents_index.html, agent.html
│   │   ├── maps_index.html, map.html, about.html, 404.html, 500.html
│   │   └── 14 templates total
│   └── static/
│       ├── css/app.css      ← single CSS, dark theme, mobile-first (700+ lines)
│       ├── favicon.svg
│       ├── img/agents/      ← agent icons (from valorant-api.com)
│       ├── img/maps/        ← map previews (from valorant-api.com)
│       └── img/ranks/
├── scripts/
│   └── fetch_leaderboard.py ← cron: fetch top 500 per region (every 6h)
├── data/
│   ├── cache.db             ← SQLite cache (gitignored)
│   └── leaderboard/         ← JSON files per region (gitignored)
├── docs/
│   ├── api/riot_api.md
│   ├── seo/strategy.md
│   ├── design/design_system.md
│   └── deploy/infrastructure.md
├── tests/
└── venv/                    ← Python 3.12 virtualenv (gitignored)
```

## API Sources

### Henrik Dev API (https://api.henrikdev.xyz)
- `GET /valorant/v1/account/{name}/{tag}` — account info
- `GET /valorant/v2/mmr/{region}/{name}/{tag}` — current rank, RR, peak
- `GET /valorant/v1/mmr-history/{region}/{name}/{tag}` — MMR history
- `GET /valorant/v3/matches/{region}/{name}/{tag}?filter={mode}&size={n}` — matches
- `GET /valorant/v2/leaderboard/{region}?start={n}&size={n}` — leaderboard
- Rate limit: 30 req/min (free), 2s client-side interval

### Valorant API (https://valorant-api.com)
- `GET /v1/agents` — all agents (name, role, abilities, icons)
- `GET /v1/maps` — all maps (name, preview, minimap)
- Free, no key required

## Conventions

- Python: PEP 8, type hints, max 120 chars
- Templates: Jinja2, `{% include %}` for partials, `{% macro %}` for cards
- CSS: semantic variables, mobile-first, no !important, no inline styles
- Git: conventional commits (feat:, fix:, docs:, infra:)
- No emojis anywhere — use SVG icons + rank/agent images
- Communication: Russian. Code/commits: English.

## Commands

- Dev server: `python3 run.py` (port 5001)
- Production: `gunicorn -w 2 --timeout 30 -b 127.0.0.1:5001 run:app`
- Leaderboard update: `python3 scripts/fetch_leaderboard.py`
- Service: `sudo systemctl restart valocheck`

## Current Status (April 2026)

- [x] Flask app + 5 blueprints
- [x] Henrik API client with rate limiting + SQLite cache
- [x] Player profile page (rank, K/D, winrate, matches, agents)
- [x] Leaderboard page (6 regions)
- [x] Dark theme CSS (mobile-first)
- [x] 14 templates + 2 partials
- [x] systemd + nginx + Cloudflare
- [x] SEO: OG tags, JSON-LD, sitemap.xml, robots.txt
- [x] Leaderboard scraper (cron every 6h)
- [x] Content pages: agents + maps (valorant-api.com)
- [x] Favicon PNG set + webmanifest
- [ ] Umami analytics
- [ ] Google AdSense
