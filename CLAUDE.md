# CLAUDE.md — ValoCheck

## Overview
**ValoCheck** — fast Valorant stat checker. Player profiles, leaderboards, agent/map stats.
- **URL:** https://valocheck.gg (temp: http://81.28.248.71:5080/)
- **Stack:** Flask + SQLite + Gunicorn + nginx
- **API:** Henrik Dev API (primary) + valorant-api.com (assets)

## Language
- Communication: **Russian**
- Code, commits, comments: **English**

## Conventions
- Python: PEP 8, type hints, max 120 chars
- Templates: Jinja2, `{% include %}` for partials
- CSS: semantic variables, mobile-first, 0 !important, 0 inline styles
- Git: conventional commits (feat:, fix:, docs:, infra:)
- 0 emojis — use SVG icons + rank/agent images
- Fonts: Russo One (headings) + Chakra Petch (body)

## Commands
```bash
python3 run.py                    # dev server (port 5001)
sudo systemctl restart valocheck  # production restart
venv/bin/python3 -m pytest tests/ # run 66 tests
```

## Scrapers (run manually or via cron)
```bash
HENRIK_API_KEY=xxx venv/bin/python3 scripts/fetch_leaderboard.py   # 2 min
HENRIK_API_KEY=xxx venv/bin/python3 scripts/scrape_agent_meta.py   # 15 min
venv/bin/python3 scripts/fetch_content.py                          # 30 sec
venv/bin/python3 scripts/scrape_pro_crosshairs.py                  # instant
```

## Docs Index
Detailed docs in `docs/`. Read only what's needed for the current task.

| Doc | Contents |
|-----|----------|
| [docs/architecture/overview.md](docs/architecture/overview.md) | stack, project structure, URL map |
| [docs/architecture/database.md](docs/architecture/database.md) | SQLite schema (cache + players) |
| [docs/architecture/api-sources.md](docs/architecture/api-sources.md) | Henrik API, Riot API, valorant-api.com |
| [docs/features/player.md](docs/features/player.md) | player profile, banner, stats, MMR chart |
| [docs/features/crosshairs.md](docs/features/crosshairs.md) | builder, pro presets, canvas |
| [docs/features/search.md](docs/features/search.md) | autocomplete, player cache DB |
| [docs/deploy/infrastructure.md](docs/deploy/infrastructure.md) | systemd, nginx, Cloudflare, cron |
| [docs/deploy/domain_setup.md](docs/deploy/domain_setup.md) | domain purchase, DNS, SSL |
| [docs/design/design_system.md](docs/design/design_system.md) | colors, typography, components |
| [docs/seo/strategy.md](docs/seo/strategy.md) | programmatic SEO, sitemap, JSON-LD |
| [docs/progress/status.md](docs/progress/status.md) | what's done, what's next, phases |
| [docs/roadmap.md](docs/roadmap.md) | full Phase 1-3 feature roadmap |
| [docs/monetization.md](docs/monetization.md) | AdSense analysis, breakeven, timeline |

## Critical Notes
- Henrik API key in systemd override, NOT in code
- Rate limit: 30 req/min (Standard), 3s interval in scrapers
- Riot production key requires OAuth (RSO) — Phase 3
- CSS cache buster: `?v=N` in base.html, bump on CSS changes
- Leaderboard data: `data/leaderboard/{region}.json` (gitignored)
- Player cache DB grows as users search — feeds autocomplete
