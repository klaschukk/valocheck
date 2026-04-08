# ValoCheck Documentation

How to use: CLAUDE.md is the compact index (~80 lines). Detailed info lives here in docs/.
AI reads CLAUDE.md every session, then opens specific docs files only when needed.

## Structure

```
docs/
├── README.md                    — this file
├── architecture/
│   ├── overview.md              — stack, project structure, file tree
│   ├── database.md              — SQLite schema, cache, players table
│   └── api-sources.md           — Henrik API, Riot API, valorant-api.com
├── features/
│   ├── player.md                — player profile, stats, MMR chart, banner
│   ├── leaderboard.md           — regions, scraper, cron
│   ├── crosshairs.md            — builder, pro presets, canvas
│   ├── insights.md              — agent meta, scraper, role filter
│   ├── search.md                — autocomplete, player cache DB
│   └── content.md               — agents, maps, tips, about, compare
├── deploy/
│   ├── infrastructure.md        — systemd, nginx, Cloudflare, ports
│   └── domain_setup.md          — domain purchase, DNS, SSL
├── design/
│   └── design_system.md         — colors, typography, components
├── seo/
│   └── strategy.md              — programmatic SEO, sitemap, JSON-LD
├── progress/
│   └── status.md                — what's done, what's next, phase tracker
├── monetization.md              — AdSense analysis, breakeven, timeline
└── roadmap.md                   — full Phase 1-3 feature roadmap
```

## How this saves AI resources

Before: CLAUDE.md = ~170 lines loaded every session.
After: CLAUDE.md = ~80 lines (key context + link table). AI reads only the docs files relevant to the current task.

Example savings:
- Task "fix crosshair builder" → AI reads CLAUDE.md (80 lines) + docs/features/crosshairs.md = ~150 lines instead of 170+
- Task "deploy domain" → CLAUDE.md + docs/deploy/domain_setup.md = ~120 lines
- Task "new feature" → CLAUDE.md + docs/progress/status.md + docs/roadmap.md = ~160 lines
