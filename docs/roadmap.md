# ValoCheck — Roadmap

## Phase 1: Foundation (DONE)
- [x] Flask app + 5 blueprints
- [x] Henrik API client with rate limiting + SQLite cache
- [x] Player profile: rank, K/D, win rate, HS%, ACS, DMG/round
- [x] MMR history area chart (tracker.gg style)
- [x] Win/loss donut chart
- [x] Player banner with card art + sub-navigation tabs
- [x] Leaderboard: 500 players x 4 regions
- [x] Crosshair builder with canvas preview + code export
- [x] 20 pro player crosshair presets
- [x] Agent insights with real scraped meta data (pick/win/K/D/ACS)
- [x] Tips & guides page (9 tips by rank)
- [x] Content pages: 29 agents + 21 maps
- [x] Dark theme CSS (Russo One + Chakra Petch)
- [x] SEO: OG tags, JSON-LD, sitemap (1795 URLs), robots.txt
- [x] systemd + nginx + Cloudflare-ready
- [x] 66 tests (pytest)
- [x] Healthcheck cron + nightly refresh cron
- [x] Favicon PNG set + OG image

## Phase 2: Pro Features (Week 2)

### Day 1-2: Core UX
- [ ] Match detail page — full 10-player scoreboard, round-by-round
- [ ] Search autocomplete — AJAX suggestions from leaderboard data
- [ ] Mobile navigation — hamburger menu, responsive tabs
- [ ] Fix any remaining UI/layout issues

### Day 3: Unique Features
- [ ] Player comparison — side-by-side stats for 2 players
- [ ] Season/Act filter on player page
- [ ] Map-specific win rates per player
- [ ] More match data (20 matches instead of 10)

### Day 4: SEO + Analytics
- [ ] Umami analytics (self-hosted, privacy-friendly)
- [ ] Google Search Console setup
- [ ] Enhanced JSON-LD on all pages
- [ ] Image lazy loading + performance audit
- [ ] Cache-Control headers optimization

### Day 5: Domain + Production
- [ ] Buy domain (valocheck.gg or valocheck.com)
- [ ] Cloudflare DNS + SSL (Full mode)
- [ ] nginx production hardening
- [ ] Submit sitemap to Google
- [ ] Submit sitemap to Bing

### Day 6-7: Growth
- [ ] Expand scraper: 200+ players for better Insights data
- [ ] Dynamic OG images per player (PIL-generated)
- [ ] Blog/news section for SEO content
- [ ] Social sharing optimization
- [ ] Performance load testing

## Phase 3: Scale (Month 2+)
- [ ] Google AdSense integration
- [ ] More regions in leaderboard (BR, LATAM)
- [ ] Weapon stats (if Henrik API supports)
- [ ] Premier tournament tracking
- [ ] User accounts (Riot OAuth2 — requires Riot dev approval)
- [ ] "My Stats" dashboard for authenticated users
- [ ] Email alerts for rank changes
- [ ] API for third-party access
- [ ] Consider second game (CS2 or Apex Legends)

## Technical Debt
- [ ] Replace CSS cache buster (?v=N) with content hash
- [ ] Add rate limiting to our own API endpoints
- [ ] Database migrations system
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Error monitoring (Sentry)
- [ ] CDN for static assets
