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

### Done
- [x] Flask app + 5 blueprints (main, player, leaderboard, content, api)
- [x] Henrik API client with rate limiting + SQLite cache
- [x] Player profile: rank, K/D, win rate, HS%, ACS, DMG/round, K/round, KAD
- [x] Player banner with wide card art + sub-navigation tabs (Overview/Matches/Agents)
- [x] MMR history area chart (tracker.gg style, gradient fill, gain/loss dots)
- [x] Win/loss donut chart (SVG)
- [x] Extended stats grid (kills, deaths, assists, rounds, top agent)
- [x] Leaderboard: top 500 x 4 regions (eu, na, ap, kr), cron every 6h
- [x] Crosshair builder: canvas preview, 8 colors, sliders, code export
- [x] 20 pro player crosshair presets database
- [x] Agent insights: real scraped meta (pick rate, win rate, K/D, ACS)
- [x] Tips & guides page (9 tips by rank difficulty)
- [x] Content pages: 29 agents + 21 maps (valorant-api.com)
- [x] Rich homepage: hero + top players + agents grid + maps grid + features
- [x] Dark theme CSS: Russo One + Chakra Petch, Valorant HUD style
- [x] SEO: OG tags, JSON-LD, sitemap (1795 URLs), robots.txt
- [x] systemd + nginx + Cloudflare-ready
- [x] Favicon PNG set (32, 180, 192, 512) + OG image + webmanifest
- [x] 66 tests (pytest), all passing
- [x] Healthcheck cron (*/5 min), nightly refresh cron (3:00 AM)
- [x] Scrapers: leaderboard, agent meta, pro crosshairs, content assets
- [x] GitHub + GitLab repos

### Next (Phase 2)
- [ ] Match detail page (full 10-player scoreboard)
- [ ] Search autocomplete (AJAX)
- [ ] Mobile hamburger menu
- [ ] Player comparison (side-by-side)
- [ ] Season/Act filter
- [ ] Umami analytics
- [ ] Domain + Cloudflare SSL
- [ ] Google AdSense (after 1000+ visits/day)

## Docs

- `docs/roadmap.md` — full feature roadmap (Phase 1-3)
- `docs/monetization.md` — AdSense analysis, breakeven, timeline
- `docs/api/riot_api.md` — Henrik/Riot API documentation
- `docs/seo/strategy.md` — programmatic SEO strategy
- `docs/design/design_system.md` — colors, typography, components
- `docs/deploy/infrastructure.md` — systemd, nginx, Cloudflare
- `docs/deploy/domain_setup.md` — domain purchase + setup guide
