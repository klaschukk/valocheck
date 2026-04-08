# Project Status — April 2026

## Done (Phase 1)
- [x] Flask app + 5 blueprints (main, player, leaderboard, content, api)
- [x] Henrik API client with rate limiting + SQLite cache
- [x] Player profile: rank, K/D, win rate, HS%, ACS, DMG/round, KAD
- [x] Player banner with wide card art + sub-navigation tabs
- [x] MMR history area chart (gradient fill, gain/loss dots)
- [x] Win/loss donut chart (SVG)
- [x] Extended stats grid (kills, deaths, assists, rounds, top agent)
- [x] Match detail page (full 10-player scoreboard)
- [x] Player comparison (side-by-side, 9 stats with visual bars)
- [x] Search autocomplete from players DB + leaderboard
- [x] Leaderboard: top 500 x 4 regions, gold/silver/bronze medals
- [x] Crosshair builder: canvas preview, 8 colors, sliders, code export
- [x] 20 pro player crosshair presets with mini canvas previews
- [x] Agent insights: real scraped meta (pick rate, win rate, K/D, ACS)
- [x] Tips & guides page (9 tips by rank difficulty)
- [x] Content pages: 29 agents + 21 maps (valorant-api.com)
- [x] Rich homepage: hero + search + top players + agents + maps + features
- [x] Dark theme CSS: Russo One + Chakra Petch, Valorant HUD style
- [x] SEO: OG tags, JSON-LD, sitemap (1795 URLs), robots.txt
- [x] systemd + nginx + Cloudflare-ready
- [x] Favicon PNG set (32, 180, 192, 512) + OG image + webmanifest
- [x] 66 tests (pytest), all passing
- [x] Healthcheck cron (*/5 min), nightly refresh cron (3:00 AM)
- [x] Scrapers: leaderboard, agent meta, pro crosshairs, content assets
- [x] GitHub + GitLab repos
- [x] Mobile burger menu
- [x] Animated page transitions
- [x] Player cache DB (any searched player becomes findable)
- [x] Riot Games API client prepared (riot_direct.py)

## Next (Phase 2)
- [ ] Henrik Enhanced API key (90 req/min)
- [ ] Domain purchase (valocheck.gg) + Cloudflare SSL
- [ ] Umami analytics (self-hosted)
- [ ] Google Search Console + sitemap submit
- [ ] Season/Act filter on player page
- [ ] Dynamic OG images per player
- [ ] Expand scraper to 200+ matches for better Insights
- [ ] Performance: lazy loading, image optimization

## Future (Phase 3)
- [ ] Riot OAuth (RSO) + Production API key
- [ ] "My Stats" dashboard for authenticated users
- [ ] Google AdSense (after 1000+ visits/day)
- [ ] Blog/news section for SEO content
- [ ] Weapon stats (if available via API)
- [ ] Premier tournament tracking
