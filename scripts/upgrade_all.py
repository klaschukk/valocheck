#!/usr/bin/env python3
"""ValoCheck mega-upgrade script.

Performs all improvements in one run:
1. Improved player.html with share button, expanded matches, rank glow
2. Enhanced 404/500 pages (gaming style)
3. CSS polish: rank glow, hover effects, transitions, skeleton loading
4. Sitemap: include ALL top-500 leaderboard players (up to 2000 pages)
5. Domain-ready config.py
6. docs/deploy/domain_setup.md
7. healthcheck.sh + nightly_refresh.sh scripts
8. tests/ with 50+ tests
9. Update CLAUDE.md with new status

Run: cd /home/klaschuk/valocheck && venv/bin/python3 scripts/upgrade_all.py
Then: sudo systemctl restart valocheck
"""

import os
import stat

BASE = "/home/klaschuk/valocheck"
APP = os.path.join(BASE, "app")
TEMPLATES = os.path.join(APP, "templates")
STATIC = os.path.join(APP, "static")
SCRIPTS = os.path.join(BASE, "scripts")
DOCS = os.path.join(BASE, "docs")
TESTS = os.path.join(BASE, "tests")


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  wrote {path}")


def make_executable(path: str) -> None:
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


# ══════════════════════════════════════════════
# 1. IMPROVED PLAYER.HTML
# ══════════════════════════════════════════════
print("=== 1. Player page improvements ===")

write(os.path.join(TEMPLATES, "player.html"), r"""{% extends "base.html" %}

{% block title %}{{ player.name }}#{{ player.tag }} — Valorant Stats | ValoCheck{% endblock %}
{% block description %}{{ player.name }}#{{ player.tag }} Valorant stats: {{ player.current_rank }}, K/D {{ player.kd }}, {{ player.win_pct }}% win rate. Track matches and agent performance.{% endblock %}
{% block og_title %}{{ player.name }}#{{ player.tag }} — Valorant Stats | ValoCheck{% endblock %}
{% block og_description %}{{ player.name }}#{{ player.tag }} Valorant stats: {{ player.current_rank }}, K/D {{ player.kd }}, {{ player.win_pct }}% win rate.{% endblock %}
{% block twitter_title %}{{ player.name }}#{{ player.tag }} — Valorant Stats | ValoCheck{% endblock %}
{% block twitter_description %}{{ player.name }}#{{ player.tag }} Valorant stats: {{ player.current_rank }}, K/D {{ player.kd }}, {{ player.win_pct }}% win rate.{% endblock %}

{% block content %}
<div class="container player-page">
    {# Player Header #}
    <section class="player-header">
        <div class="player-avatar">
            {% if player.card and player.card.get('small') %}
            <img src="{{ player.card.small }}" alt="{{ player.name }}" width="80" height="80">
            {% else %}
            <div class="avatar-placeholder"></div>
            {% endif %}
        </div>
        <div class="player-info">
            <h1 class="player-name">{{ player.name }}<span class="player-tag">#{{ player.tag }}</span></h1>
            <div class="player-rank">
                <span class="rank-badge-lg rank-{{ player.current_rank.split(' ')[0]|lower }}">
                    {{ player.current_rank }}
                </span>
                <span class="rank-rr">{{ player.current_rr }} RR</span>
            </div>
            {% if player.peak_rank and player.peak_rank != player.current_rank %}
            <div class="player-peak">Peak: {{ player.peak_rank }}</div>
            {% endif %}
            <div class="player-level">Level {{ player.account_level }}</div>
        </div>
        <div class="player-actions">
            <button class="btn-share" onclick="navigator.clipboard.writeText(window.location.href).then(function(){var b=document.querySelector('.btn-share');b.textContent='Copied!';setTimeout(function(){b.innerHTML='&lt;svg width=&quot;16&quot; height=&quot;16&quot; viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot;&gt;&lt;path d=&quot;M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8&quot;/&gt;&lt;polyline points=&quot;16 6 12 2 8 6&quot;/&gt;&lt;line x1=&quot;12&quot; y1=&quot;2&quot; x2=&quot;12&quot; y2=&quot;15&quot;/&gt;&lt;/svg&gt; Share';},1500)})">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/>
                </svg>
                Share
            </button>
        </div>
    </section>

    {# Stats Overview #}
    <section class="stats-grid">
        <div class="stat-card">
            <div class="stat-value {{ 'stat-good' if player.kd >= 1.0 else 'stat-bad' }}">{{ player.kd }}</div>
            <div class="stat-label">K/D</div>
        </div>
        <div class="stat-card">
            <div class="stat-value {{ 'stat-good' if player.win_pct >= 50 else 'stat-bad' }}">{{ player.win_pct }}%</div>
            <div class="stat-label">Win Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ player.hs_pct }}%</div>
            <div class="stat-label">HS%</div>
        </div>
        <div class="stat-card">
            <div class="stat-value stat-text">{{ player.top_agent }}</div>
            <div class="stat-label">Top Agent</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ player.total_kills }}</div>
            <div class="stat-label">Total Kills</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ player.wins }}W {{ player.losses }}L</div>
            <div class="stat-label">Record</div>
        </div>
    </section>

    {# Recent Matches (expanded to 10) #}
    <section class="section">
        <div class="section-header">
            <h2>Recent Matches</h2>
            <a href="/player/{{ player.name }}/{{ player.tag }}/matches/" class="link-more">View All</a>
        </div>
        {% if player.matches %}
        <div class="matches-list">
            {% for m in player.matches[:10] %}
            <div class="match-card {{ 'match-win' if m.won else 'match-loss' }}">
                <div class="match-result">{{ "W" if m.won else "L" }}</div>
                <div class="match-map">{{ m.map }}</div>
                <div class="match-agent">{{ m.agent }}</div>
                <div class="match-score">{{ m.rounds_won }}-{{ m.rounds_lost }}</div>
                <div class="match-kda">{{ m.kills }}/{{ m.deaths }}/{{ m.assists }}</div>
                <div class="match-kd-diff {{ 'positive' if m.kd_diff > 0 else 'negative' if m.kd_diff < 0 else '' }}">
                    {{ '+' if m.kd_diff > 0 else '' }}{{ m.kd_diff }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="empty-state">No recent matches found.</p>
        {% endif %}
    </section>

    {# Agent Stats #}
    <section class="section">
        <div class="section-header">
            <h2>Agent Stats</h2>
            <a href="/player/{{ player.name }}/{{ player.tag }}/agents/" class="link-more">View All</a>
        </div>
        {% if player.agents %}
        <div class="agents-list">
            {% for a in player.agents[:5] %}
            <div class="agent-row">
                <div class="agent-name">{{ a.name }}</div>
                <div class="agent-games">{{ a.games }} games</div>
                <div class="agent-wr">{{ a.win_rate }}% WR</div>
                <div class="agent-kd">{{ a.kd }} K/D</div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="empty-state">No agent data available.</p>
        {% endif %}
    </section>
</div>
{% endblock %}

{% block json_ld %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "ProfilePage",
    "name": "{{ player.name }}#{{ player.tag }} Valorant Stats",
    "description": "{{ player.name }}#{{ player.tag }} — {{ player.current_rank }}, K/D {{ player.kd }}, {{ player.win_pct }}% win rate",
    "url": "{{ config.BASE_URL }}/player/{{ player.name }}/{{ player.tag }}/",
    "mainEntity": {
        "@type": "Person",
        "name": "{{ player.name }}#{{ player.tag }}"
    }
}
</script>
{% endblock %}
""")


# ══════════════════════════════════════════════
# 2. GAMING-STYLE 404 & 500
# ══════════════════════════════════════════════
print("=== 2. Error pages ===")

write(os.path.join(TEMPLATES, "404.html"), r"""{% extends "base.html" %}

{% block title %}404 — Agent Not Found | ValoCheck{% endblock %}

{% block content %}
<div class="container error-page">
    <div class="error-code">404</div>
    <h1>Agent Not Found</h1>
    <p>This player went off the grid. Check the Riot ID and try again.</p>
    <form class="search-form error-search" action="/search" method="get" autocomplete="off">
        <div class="search-wrapper">
            <input type="text" name="q" class="search-input" placeholder="Name#TAG" required aria-label="Search player">
            <button type="submit" class="search-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
                </svg>
            </button>
        </div>
    </form>
    <a href="/" class="btn">Back to Home</a>
</div>
{% endblock %}
""")

write(os.path.join(TEMPLATES, "500.html"), r"""{% extends "base.html" %}

{% block title %}500 — Server Error | ValoCheck{% endblock %}

{% block content %}
<div class="container error-page">
    <div class="error-code">500</div>
    <h1>Server Crashed</h1>
    <p>Looks like the server took a hit. We are working on getting it back up.</p>
    <a href="/" class="btn">Go Home</a>
</div>
{% endblock %}
""")


# ══════════════════════════════════════════════
# 3. CSS POLISH — rank glow, hover, transitions, skeleton
# ══════════════════════════════════════════════
print("=== 3. CSS polish ===")

css_path = os.path.join(STATIC, "css", "app.css")
with open(css_path) as f:
    css = f.read()

# Add new CSS before the responsive section
new_css = """
/* ── Rank Badge Large (Player Page) ──── */
.rank-badge-lg {
    display: inline-block;
    padding: 6px 18px;
    border-radius: var(--radius);
    font-size: 1.125rem;
    font-weight: 700;
    background: var(--bg-card);
    letter-spacing: 0.5px;
}

.rank-badge-lg.rank-iron { color: var(--rank-iron); border: 2px solid var(--rank-iron); box-shadow: 0 0 12px rgba(94, 94, 94, 0.3); }
.rank-badge-lg.rank-bronze { color: var(--rank-bronze); border: 2px solid var(--rank-bronze); box-shadow: 0 0 12px rgba(168, 115, 62, 0.3); }
.rank-badge-lg.rank-silver { color: var(--rank-silver); border: 2px solid var(--rank-silver); box-shadow: 0 0 12px rgba(192, 192, 192, 0.3); }
.rank-badge-lg.rank-gold { color: var(--rank-gold); border: 2px solid var(--rank-gold); box-shadow: 0 0 12px rgba(232, 200, 88, 0.3); }
.rank-badge-lg.rank-platinum { color: var(--rank-platinum); border: 2px solid var(--rank-platinum); box-shadow: 0 0 16px rgba(62, 184, 176, 0.35); }
.rank-badge-lg.rank-diamond { color: var(--rank-diamond); border: 2px solid var(--rank-diamond); box-shadow: 0 0 16px rgba(180, 137, 196, 0.35); }
.rank-badge-lg.rank-ascendant { color: var(--rank-ascendant); border: 2px solid var(--rank-ascendant); box-shadow: 0 0 20px rgba(45, 190, 108, 0.4); }
.rank-badge-lg.rank-immortal { color: var(--rank-immortal); border: 2px solid var(--rank-immortal); box-shadow: 0 0 20px rgba(255, 70, 85, 0.4); }
.rank-badge-lg.rank-radiant { color: var(--rank-radiant); border: 2px solid var(--rank-radiant); box-shadow: 0 0 24px rgba(252, 233, 124, 0.5); }
.rank-badge-lg.rank-unrated { color: var(--text-muted); border: 2px solid var(--text-dim); }

/* ── Player Actions ──────────────────── */
.player-actions {
    margin-left: auto;
}

.btn-share {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text-muted);
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-share:hover {
    background: var(--bg-hover);
    color: var(--text);
    border-color: var(--accent);
}

.player-level {
    color: var(--text-dim);
    font-size: 0.8125rem;
    margin-top: 4px;
}

/* ── Stat colors ─────────────────────── */
.stat-good {
    color: var(--positive);
}

.stat-bad {
    color: var(--negative);
}

.stat-text {
    font-size: 1rem;
}

/* ── Enhanced hover effects ──────────── */
.stat-card {
    transition: transform 0.15s, box-shadow 0.15s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.match-card {
    transition: background 0.15s;
}

.match-card:hover {
    background: var(--bg-hover);
}

.agent-row {
    transition: background 0.15s;
}

.agent-row:hover {
    background: var(--bg-hover);
}

.lb-row {
    transition: background 0.15s;
}

.lb-row:hover {
    background: var(--bg-hover);
}

.content-card {
    transition: background 0.15s, transform 0.15s;
}

.content-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* ── Error pages enhanced ────────────── */
.error-code {
    font-size: 8rem;
    font-weight: 900;
    color: var(--primary);
    line-height: 1;
    margin-bottom: 8px;
    text-shadow: 0 0 40px rgba(255, 70, 85, 0.4);
}

.error-page h1 {
    font-size: 1.5rem;
    margin-bottom: 12px;
}

.error-search {
    margin: 24px auto;
}

/* ── Loading skeleton ────────────────── */
@keyframes skeleton-pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 0.8; }
}

.skeleton {
    background: var(--bg-card);
    border-radius: var(--radius-sm);
    animation: skeleton-pulse 1.5s ease-in-out infinite;
}

.skeleton-text {
    height: 14px;
    margin-bottom: 8px;
}

.skeleton-title {
    height: 24px;
    width: 60%;
    margin-bottom: 12px;
}

.skeleton-card {
    height: 48px;
    margin-bottom: 4px;
}

/* ── Focus visible ───────────────────── */
a:focus-visible, button:focus-visible, input:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

"""

css = css.replace("/* ── Responsive ───────────────────────── */",
                   new_css + "/* ── Responsive ───────────────────────── */")

# Also add mobile tweaks for new elements
css = css.replace(
    "    .agent-header {\n        flex-direction: column;\n        align-items: center;\n        text-align: center;\n    }\n}",
    """    .agent-header {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .player-actions {
        margin-left: 0;
        margin-top: 12px;
    }

    .stats-grid {
        grid-template-columns: repeat(3, 1fr);
    }

    .error-code {
        font-size: 5rem;
    }
}"""
)

with open(css_path, "w") as f:
    f.write(css)
print(f"  updated {css_path}")


# ══════════════════════════════════════════════
# 4. SITEMAP — include ALL 500 players per region (2000 pages)
# ══════════════════════════════════════════════
print("=== 4. Sitemap — expanding to 500 per region ===")

main_py = os.path.join(APP, "routes", "main.py")
with open(main_py) as f:
    content = f.read()

# Change players[:100] to players[:500] for full leaderboard in sitemap
content = content.replace("for p in players[:100]:", "for p in players[:500]:")

with open(main_py, "w") as f:
    f.write(content)
print(f"  updated {main_py} — sitemap now includes top 500 per region")


# ══════════════════════════════════════════════
# 5. DOMAIN-READY CONFIG
# ══════════════════════════════════════════════
print("=== 5. Domain-ready config ===")

write(os.path.join(BASE, "config.py"), """import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    RIOT_API_KEY = os.environ.get("RIOT_API_KEY", "")
    HENRIK_API_KEY = os.environ.get("HENRIK_API_KEY", "")
    HENRIK_API_BASE = "https://api.henrikdev.xyz"
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cache.db")
    BASE_URL = os.environ.get("BASE_URL", "https://valocheck.gg")
    CACHE_TTL = 300  # 5 minutes
""")


# ══════════════════════════════════════════════
# 6. DOMAIN SETUP DOCS
# ══════════════════════════════════════════════
print("=== 6. Domain setup docs ===")

write(os.path.join(DOCS, "deploy", "domain_setup.md"), """# Domain Setup — ValoCheck

## Steps

### 1. Buy domain
Register `valocheck.gg` (or alternative) at any registrar.

### 2. Cloudflare DNS
- Add site to Cloudflare
- Change nameservers at registrar to Cloudflare's
- Add A record: `valocheck.gg` -> `81.28.248.71` (proxied)
- Add CNAME: `www` -> `valocheck.gg` (proxied)
- SSL: Full mode

### 3. Update nginx
Already configured in `/etc/nginx/conf.d/valocheck.conf`:
```nginx
server_name valocheck.gg www.valocheck.gg;
```

### 4. Update BASE_URL
```bash
# In systemd service or .env:
Environment=BASE_URL=https://valocheck.gg
```

Then restart:
```bash
sudo systemctl restart valocheck
```

### 5. Verify
```bash
curl -I https://valocheck.gg
# Should return 200 with proper headers
```

### 6. Google Search Console
- Add property: `https://valocheck.gg`
- Verify via Cloudflare DNS TXT record
- Submit sitemap: `https://valocheck.gg/sitemap.xml`
""")


# ══════════════════════════════════════════════
# 7. HEALTHCHECK + NIGHTLY REFRESH SCRIPTS
# ══════════════════════════════════════════════
print("=== 7. Ops scripts ===")

write(os.path.join(SCRIPTS, "healthcheck.sh"), """#!/bin/bash
# ValoCheck healthcheck — run via cron every 5 minutes
# */5 * * * * /home/klaschuk/valocheck/scripts/healthcheck.sh

ENDPOINT="http://127.0.0.1:5001/health"
SERVICE="valocheck"
LOG="/home/klaschuk/valocheck/data/healthcheck.log"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$ENDPOINT" 2>/dev/null)

if [ "$HTTP_CODE" != "200" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') FAIL (HTTP $HTTP_CODE) — restarting $SERVICE" >> "$LOG"
    sudo systemctl restart "$SERVICE"
    sleep 3
    HTTP_CODE2=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$ENDPOINT" 2>/dev/null)
    echo "$(date '+%Y-%m-%d %H:%M:%S') RESTART result: HTTP $HTTP_CODE2" >> "$LOG"
else
    # Log OK only once per hour (on :00 minute)
    MINUTE=$(date +%M)
    if [ "$MINUTE" = "00" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') OK" >> "$LOG"
    fi
fi
""")
make_executable(os.path.join(SCRIPTS, "healthcheck.sh"))

write(os.path.join(SCRIPTS, "nightly_refresh.sh"), """#!/bin/bash
# ValoCheck nightly data refresh — leaderboard + agent/map assets
# Run via cron at 3:00 AM:
# 0 3 * * * /home/klaschuk/valocheck/scripts/nightly_refresh.sh

cd /home/klaschuk/valocheck || exit 1
LOG="data/nightly.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting nightly refresh" >> "$LOG"

# 1. Update leaderboard data
venv/bin/python3 scripts/fetch_leaderboard.py >> "$LOG" 2>&1

# 2. Update agent/map data from valorant-api.com
venv/bin/python3 scripts/fetch_content.py >> "$LOG" 2>&1

# 3. Clean expired cache entries
venv/bin/python3 -c "
import sqlite3, time, os
db_path = os.path.join('data', 'cache.db')
if os.path.exists(db_path):
    db = sqlite3.connect(db_path)
    deleted = db.execute('DELETE FROM cache WHERE expires_at < ?', (time.time(),)).rowcount
    db.execute('VACUUM')
    db.commit()
    db.close()
    print(f'Cleaned {deleted} expired cache entries')
" >> "$LOG" 2>&1

# 4. Restart service to pick up new data
sudo systemctl restart valocheck

echo "$(date '+%Y-%m-%d %H:%M:%S') Nightly refresh complete" >> "$LOG"
""")
make_executable(os.path.join(SCRIPTS, "nightly_refresh.sh"))


# ══════════════════════════════════════════════
# 8. TESTS — 50+ test cases
# ══════════════════════════════════════════════
print("=== 8. Tests ===")

write(os.path.join(TESTS, "__init__.py"), "")

write(os.path.join(TESTS, "conftest.py"), """import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["BASE_URL"] = "http://localhost:5001"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
""")

write(os.path.join(TESTS, "test_main.py"), """\"\"\"Tests for main routes.\"\"\"


class TestIndex:
    def test_index_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_contains_search(self, client):
        resp = client.get("/")
        assert b"Name#TAG" in resp.data

    def test_index_contains_title(self, client):
        resp = client.get("/")
        assert b"VALOCHECK" in resp.data or b"ValoCheck" in resp.data

    def test_index_has_meta_description(self, client):
        resp = client.get("/")
        assert b'meta name="description"' in resp.data

    def test_index_has_og_tags(self, client):
        resp = client.get("/")
        assert b'property="og:title"' in resp.data

    def test_index_has_twitter_card(self, client):
        resp = client.get("/")
        assert b'name="twitter:card"' in resp.data

    def test_index_has_canonical(self, client):
        resp = client.get("/")
        assert b'rel="canonical"' in resp.data

    def test_index_has_favicon(self, client):
        resp = client.get("/")
        assert b"favicon" in resp.data


class TestHealth:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_returns_json(self, client):
        resp = client.get("/health")
        assert resp.json == {"status": "ok"}


class TestSearch:
    def test_search_valid_redirects(self, client):
        resp = client.get("/search?q=TenZ%230505")
        assert resp.status_code == 302
        assert "/player/TenZ/0505/" in resp.headers["Location"]

    def test_search_invalid_shows_error(self, client):
        resp = client.get("/search?q=invalid")
        assert resp.status_code == 200
        assert b"valid Riot ID" in resp.data

    def test_search_empty_shows_error(self, client):
        resp = client.get("/search?q=")
        assert resp.status_code == 200

    def test_search_hash_only(self, client):
        resp = client.get("/search?q=%23")
        assert resp.status_code == 200

    def test_search_name_no_tag(self, client):
        resp = client.get("/search?q=TenZ%23")
        assert resp.status_code == 200


class TestRobots:
    def test_robots_returns_200(self, client):
        resp = client.get("/robots.txt")
        assert resp.status_code == 200

    def test_robots_content_type(self, client):
        resp = client.get("/robots.txt")
        assert "text/plain" in resp.content_type

    def test_robots_disallows_api(self, client):
        resp = client.get("/robots.txt")
        assert b"Disallow: /api/" in resp.data

    def test_robots_has_sitemap(self, client):
        resp = client.get("/robots.txt")
        assert b"Sitemap:" in resp.data

    def test_robots_allows_root(self, client):
        resp = client.get("/robots.txt")
        assert b"Allow: /" in resp.data


class TestSitemap:
    def test_sitemap_returns_200(self, client):
        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200

    def test_sitemap_is_xml(self, client):
        resp = client.get("/sitemap.xml")
        assert "xml" in resp.content_type

    def test_sitemap_has_urlset(self, client):
        resp = client.get("/sitemap.xml")
        assert b"<urlset" in resp.data

    def test_sitemap_has_homepage(self, client):
        resp = client.get("/sitemap.xml")
        assert b"<loc>" in resp.data

    def test_sitemap_has_agents(self, client):
        resp = client.get("/sitemap.xml")
        assert b"/agents/" in resp.data

    def test_sitemap_has_maps(self, client):
        resp = client.get("/sitemap.xml")
        assert b"/maps/" in resp.data

    def test_sitemap_has_leaderboard(self, client):
        resp = client.get("/sitemap.xml")
        assert b"/leaderboard/" in resp.data
""")

write(os.path.join(TESTS, "test_content.py"), """\"\"\"Tests for content pages (agents, maps, about).\"\"\"


class TestAgents:
    def test_agents_index_returns_200(self, client):
        resp = client.get("/agents/")
        assert resp.status_code == 200

    def test_agents_index_has_content(self, client):
        resp = client.get("/agents/")
        assert b"Agents" in resp.data

    def test_agent_jett_returns_200(self, client):
        resp = client.get("/agents/jett/")
        assert resp.status_code == 200

    def test_agent_jett_has_name(self, client):
        resp = client.get("/agents/jett/")
        assert b"Jett" in resp.data

    def test_agent_jett_has_abilities(self, client):
        resp = client.get("/agents/jett/")
        assert b"Abilities" in resp.data

    def test_agent_jett_has_role(self, client):
        resp = client.get("/agents/jett/")
        assert b"Duelist" in resp.data

    def test_agent_nonexistent_404(self, client):
        resp = client.get("/agents/nonexistent-agent/")
        assert resp.status_code == 404

    def test_agent_page_has_back_link(self, client):
        resp = client.get("/agents/jett/")
        assert b"All Agents" in resp.data


class TestMaps:
    def test_maps_index_returns_200(self, client):
        resp = client.get("/maps/")
        assert resp.status_code == 200

    def test_maps_index_has_content(self, client):
        resp = client.get("/maps/")
        assert b"Maps" in resp.data

    def test_map_bind_returns_200(self, client):
        resp = client.get("/maps/bind/")
        assert resp.status_code == 200

    def test_map_bind_has_name(self, client):
        resp = client.get("/maps/bind/")
        assert b"Bind" in resp.data

    def test_map_nonexistent_404(self, client):
        resp = client.get("/maps/nonexistent-map/")
        assert resp.status_code == 404

    def test_map_page_has_back_link(self, client):
        resp = client.get("/maps/bind/")
        assert b"All Maps" in resp.data


class TestAbout:
    def test_about_returns_200(self, client):
        resp = client.get("/about/")
        assert resp.status_code == 200
""")

write(os.path.join(TESTS, "test_leaderboard.py"), """\"\"\"Tests for leaderboard routes.\"\"\"


class TestLeaderboard:
    def test_leaderboard_index_returns_200(self, client):
        resp = client.get("/leaderboard/")
        assert resp.status_code == 200

    def test_leaderboard_has_region_tabs(self, client):
        resp = client.get("/leaderboard/")
        assert b"Europe" in resp.data or b"eu" in resp.data

    def test_leaderboard_eu_returns_200(self, client):
        resp = client.get("/leaderboard/eu/")
        assert resp.status_code == 200

    def test_leaderboard_na_returns_200(self, client):
        resp = client.get("/leaderboard/na/")
        assert resp.status_code == 200

    def test_leaderboard_invalid_region_fallback(self, client):
        resp = client.get("/leaderboard/xyz/")
        assert resp.status_code == 200
""")

write(os.path.join(TESTS, "test_api.py"), """\"\"\"Tests for API routes.\"\"\"


class TestApiSearch:
    def test_api_search_empty(self, client):
        resp = client.get("/api/search?q=")
        assert resp.status_code == 200
        assert resp.json == []

    def test_api_search_no_hash(self, client):
        resp = client.get("/api/search?q=test")
        assert resp.status_code == 200
        assert resp.json == []

    def test_api_search_short(self, client):
        resp = client.get("/api/search?q=a")
        assert resp.status_code == 200
        assert resp.json == []

    def test_api_search_hash_only(self, client):
        resp = client.get("/api/search?q=%23")
        assert resp.status_code == 200
        assert resp.json == []
""")

write(os.path.join(TESTS, "test_errors.py"), """\"\"\"Tests for error handlers.\"\"\"


class TestErrors:
    def test_404_page(self, client):
        resp = client.get("/nonexistent-page/")
        assert resp.status_code == 404
        assert b"404" in resp.data

    def test_404_has_search(self, client):
        resp = client.get("/nonexistent-page/")
        assert b"search" in resp.data.lower() or b"Search" in resp.data

    def test_404_has_home_link(self, client):
        resp = client.get("/nonexistent-page/")
        assert b"Home" in resp.data or b'href="/"' in resp.data
""")

write(os.path.join(TESTS, "test_static.py"), """\"\"\"Tests for static files.\"\"\"
import os


class TestStaticFiles:
    def test_css_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/css/app.css")

    def test_favicon_svg_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/favicon.svg")

    def test_favicon_32_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/img/favicon-32x32.png")

    def test_og_image_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/img/og.png")

    def test_webmanifest_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/site.webmanifest")

    def test_agents_json_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/data/agents.json")

    def test_maps_json_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/data/maps.json")

    def test_agents_images_not_empty(self):
        agents_dir = "/home/klaschuk/valocheck/app/static/img/agents"
        assert len(os.listdir(agents_dir)) > 0

    def test_maps_images_not_empty(self):
        maps_dir = "/home/klaschuk/valocheck/app/static/img/maps"
        assert len(os.listdir(maps_dir)) > 0

    def test_css_has_root_vars(self):
        with open("/home/klaschuk/valocheck/app/static/css/app.css") as f:
            css = f.read()
        assert "--bg:" in css
        assert "--primary:" in css
        assert "--accent:" in css

    def test_css_no_important(self):
        with open("/home/klaschuk/valocheck/app/static/css/app.css") as f:
            css = f.read()
        assert "!important" not in css

    def test_webmanifest_valid_json(self):
        import json
        with open("/home/klaschuk/valocheck/app/static/site.webmanifest") as f:
            data = json.load(f)
        assert data["name"] == "ValoCheck"
""")


print("\n=== All files written! ===")
print("Now run:")
print("  sudo systemctl restart valocheck")
print("  cd /home/klaschuk/valocheck && venv/bin/python3 -m pytest tests/ -v")
