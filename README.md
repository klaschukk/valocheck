# ValoCheck

Fast, lightweight Valorant stat checker. Track any player's rank, K/D, win rate, and match history.

## Features

- **Player Profiles** — search any player by Riot ID (Name#TAG), see rank, K/D, win rate, headshot %, top agents, recent matches
- **Leaderboards** — top 500 players per region (EU, NA, AP, KR), updated every 6 hours
- **Agent Pages** — all Valorant agents with abilities, roles, and icons
- **Map Pages** — all Valorant maps with previews
- **Mobile-First** — dark gaming theme, responsive design, fast load times
- **SEO-Optimized** — OG tags, JSON-LD, dynamic sitemap, programmatic player pages

## Tech Stack

- **Backend:** Flask (Python 3.12)
- **Database:** SQLite (player/match cache)
- **API:** Henrik Dev API (unofficial Valorant API) + valorant-api.com (assets)
- **Server:** Gunicorn + nginx + Cloudflare
- **Frontend:** Jinja2 templates, single CSS file, no JS frameworks

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/valocheck.git
cd valocheck
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Optional: set API key for higher rate limits
export HENRIK_API_KEY=your_key_here

# Run dev server
python3 run.py
# Open http://localhost:5001
```

## API Sources

| API | Usage | Auth |
|-----|-------|------|
| [Henrik Dev API](https://api.henrikdev.xyz) | Player stats, MMR, matches, leaderboards | Optional key (30 req/min free) |
| [Valorant API](https://valorant-api.com) | Agent/map assets (icons, previews) | None required |

## Project Structure

```
valocheck/
├── app/                  # Flask application
│   ├── routes/           # Blueprints (main, player, leaderboard, content, api)
│   ├── templates/        # Jinja2 templates (14 + 2 partials)
│   ├── static/           # CSS, images, favicon
│   ├── riot_api.py       # Henrik API client
│   └── db.py             # SQLite cache layer
├── scripts/              # Cron jobs (leaderboard fetcher)
├── data/                 # Cache DB + leaderboard JSON
├── docs/                 # Project documentation
├── config.py             # App configuration
└── run.py                # Dev server entry point
```

## License

Not affiliated with Riot Games. Valorant is a registered trademark of Riot Games, Inc.
