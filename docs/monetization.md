# ValoCheck — Monetization Analysis

## Costs (Monthly)

| Item | Cost | Notes |
|------|------|-------|
| Server | ~50 EUR/mo | Shared with prevozni.com (split 50/50 of 100 EUR) |
| Domain | ~1 EUR/mo | ~10 EUR/year for .gg or .com |
| Claude subscription | 100 EUR/mo | Development tool, not ongoing operational cost |
| **Total operational** | **~51 EUR/mo** | Without Claude (one-time dev cost) |
| **Total with Claude** | **~151 EUR/mo** | During active development |

## Revenue Model: Google AdSense

### Traffic Estimates

Gaming/esports niche metrics:
- **RPM** (Revenue per 1000 pageviews): $2-5 for gaming sites
  - US/EU gaming traffic: $3-5 RPM
  - Global average: $2-3 RPM
  - Conservative estimate: **$2.50 RPM**

### Scenario Analysis

#### Scenario 1: Launch Month (Month 1)
- SEO pages indexed: ~2000 (player profiles from leaderboard)
- Organic traffic: ~100-300 visits/day (new site, low domain authority)
- Monthly pageviews: ~5,000-15,000
- **AdSense revenue: $12-37/mo (~10-35 EUR)**
- **Verdict: NOT profitable yet**

#### Scenario 2: Growth (Month 3-6)
- SEO pages indexed: ~5000+
- Google starts ranking player profiles + agent pages
- Organic traffic: ~1,000-3,000 visits/day
- Monthly pageviews: ~50,000-150,000
- **AdSense revenue: $125-375/mo (~115-345 EUR)**
- **Verdict: Covers operational costs (51 EUR), possibly profitable**

#### Scenario 3: Established (Month 6-12)
- Strong SEO presence for "player name valorant stats" queries
- Organic traffic: ~5,000-15,000 visits/day
- Monthly pageviews: ~200,000-600,000
- **AdSense revenue: $500-1,500/mo (~460-1,380 EUR)**
- **Verdict: Clearly profitable**

#### Scenario 4: Success (Year 2+)
- Competitive with smaller trackers
- 30,000-100,000 visits/day
- Monthly pageviews: 1,000,000-4,000,000
- **AdSense revenue: $2,500-10,000/mo (~2,300-9,200 EUR)**
- Premium features or sponsorships: additional revenue

### Breakeven Analysis

| Cost scenario | Monthly cost | Required pageviews | Required daily visits |
|---------------|-------------|-------------------|----------------------|
| Ops only (no Claude) | 51 EUR | ~22,000 | ~730 |
| With Claude dev | 151 EUR | ~65,000 | ~2,170 |

**To break even on operational costs: ~730 visits/day**
**To break even including Claude: ~2,170 visits/day**

### Is it realistic?

**YES, but not immediately.**

Key factors:
1. **Programmatic SEO is the main driver.** 2000 player profile pages = 2000 potential Google landing pages. Each top player's name is a search query.
2. **Long-tail keywords are our strength.** "TenZ valorant stats", "Aspas rank", "{player} valorant profile" — these queries have moderate volume but low competition from other small trackers.
3. **tracker.gg dominates** but they're bloated with ads, slow, and have a premium paywall. We're faster and cleaner — that's our advantage.
4. **Gaming niche has decent CPM** compared to general content.

### Timeline to Profitability

| Milestone | Timeline | Monthly revenue estimate |
|-----------|----------|------------------------|
| First AdSense payment ($100 threshold) | Month 3-4 | ~$30-50/mo |
| Covers server costs (51 EUR) | Month 4-6 | ~$60-80/mo |
| Covers all costs inc. Claude (151 EUR) | Month 6-9 | ~$170-200/mo |
| Meaningful income (500+ EUR) | Month 9-12 | ~$500-800/mo |

### Recommendations

1. **Don't add AdSense too early** — focus on getting Google to index pages first. Ads on low-traffic site hurt UX and SEO.
2. **Apply for AdSense when hitting 1000+ visits/day** (Google may reject sites with very low traffic).
3. **Ad placement matters:** one leaderboard ad + one in-content ad per page. Don't be tracker.gg with 5 ads per page.
4. **Consider alternatives to AdSense:**
   - Ezoic (lower threshold, better RPM for gaming)
   - Mediavine (requires 50K sessions/month)
   - Direct sponsorships from gaming brands
   - Premium features (ad-free, more data, API access)

### Conclusion

The project **can be profitable** within 4-6 months if SEO works well. Operational costs are very low (51 EUR/mo). The main investment is development time. At 2,000+ daily visits (achievable with 2000+ indexed pages), the site pays for itself. At 10,000+ daily visits, it becomes a meaningful income source.

**Risk factors:**
- Henrik API could change terms or go down
- Riot could launch their own stats platform
- Google algorithm changes could tank traffic
- Competition from established trackers

**Mitigation:**
- Multiple data sources (Henrik + direct Riot API)
- Focus on unique features (crosshair builder, clean UX)
- Build email list for direct traffic
- Social media presence (Reddit, Twitter/X)
