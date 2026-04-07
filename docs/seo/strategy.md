# SEO Strategy — ValoCheck

## Approach: Programmatic SEO

Generate thousands of unique, indexable pages from API data.

## Page Types

### Player Profiles (unlimited)
- URL: `/player/{name}/{tag}/`
- Title: `{Name}#{Tag} Valorant Stats | ValoCheck`
- Unique content: rank, K/D, win rate, HS%, match history, agent breakdown
- JSON-LD: ProfilePage schema
- Indexed via internal links from leaderboard pages

### Leaderboard Pages (6 regions)
- URL: `/leaderboard/{region}/`
- Title: `{Region} Valorant Leaderboard | ValoCheck`
- 500 player links per region = 3000 internal links to player profiles
- Updated every 6 hours via cron

### Agent Pages (20+)
- URL: `/agents/{slug}/`
- Title: `{Agent} — Valorant Agent Guide | ValoCheck`
- Static content: abilities, role, description

### Map Pages (10+)
- URL: `/maps/{slug}/`
- Title: `{Map} — Valorant Map Guide | ValoCheck`
- Static content: preview image, callouts

## Technical SEO

### Meta Tags (base.html)
- `<html lang="en">` — site is in English
- `<meta name="description">` — unique per page via Jinja2 blocks
- `<meta property="og:title/description/image/url">` — Open Graph
- `<meta name="twitter:card" content="summary_large_image">`
- `<link rel="canonical">` — self-referencing canonical

### Structured Data
- Player pages: `ProfilePage` JSON-LD
- Breadcrumbs where applicable

### Sitemap
- Dynamic `/sitemap.xml` route
- Includes: static pages, all agents, all maps, leaderboard pages
- Top players from leaderboard (when available)

### Robots.txt
- Allow all except `/api/`
- Sitemap reference: `https://valocheck.gg/sitemap.xml`

## Link Building Strategy

- Leaderboard pages link to player profiles
- Agent/map pages provide evergreen content
- Player pages link to agent detail pages
- Internal linking creates crawl depth for search engines
