"""SEO tests — titles, descriptions, JSON-LD, OG tags, canonical, sitemap."""

import json
import re

import pytest

# All pages that should have proper SEO
_SEO_PAGES = [
    "/",
    "/agents/",
    "/agents/jett/",
    "/maps/",
    "/maps/bind/",
    "/leaderboard/",
    "/leaderboard/eu/",
    "/insights/",
    "/crosshairs/",
    "/tips/",
    "/compare/",
    "/seasons/",
    "/about/",
    "/guides/best-agents/",
    "/guides/rank-distribution/",
    "/guides/crosshair-settings/",
    "/guides/how-to-rank-up/",
    "/guides/weapons/",
    "/guides/maps/",
]


# ── Title ──

@pytest.mark.parametrize("url", _SEO_PAGES)
def test_title_exists(client, url):
    html = client.get(url).data.decode()
    m = re.search(r"<title>(.*?)</title>", html)
    assert m, f"No <title> on {url}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_title_length(client, url):
    html = client.get(url).data.decode()
    m = re.search(r"<title>(.*?)</title>", html)
    title = m.group(1).strip()
    assert 10 <= len(title) <= 80, f"Title length {len(title)} on {url}: {title}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_title_has_valocheck(client, url):
    html = client.get(url).data.decode()
    title = re.search(r"<title>(.*?)</title>", html).group(1)
    assert "ValoCheck" in title or "Valo" in title, f"No brand in title: {title}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_title_no_none(client, url):
    html = client.get(url).data.decode()
    title = re.search(r"<title>(.*?)</title>", html).group(1)
    assert "None" not in title, f"None in title: {title}"


# ── Meta description ──

@pytest.mark.parametrize("url", _SEO_PAGES)
def test_description_exists(client, url):
    html = client.get(url).data.decode()
    m = re.search(r'name="description"\s+content="([^"]*)"', html)
    assert m, f"No meta description on {url}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_description_length(client, url):
    html = client.get(url).data.decode()
    m = re.search(r'name="description"\s+content="([^"]*)"', html)
    desc = m.group(1).strip()
    assert 30 <= len(desc) <= 300, f"Description length {len(desc)} on {url}"


# ── Canonical ──

@pytest.mark.parametrize("url", _SEO_PAGES)
def test_has_canonical(client, url):
    html = client.get(url).data.decode()
    assert 'rel="canonical"' in html, f"No canonical on {url}"


# ── OG tags ──

@pytest.mark.parametrize("url", _SEO_PAGES)
def test_og_title(client, url):
    html = client.get(url).data.decode()
    assert 'property="og:title"' in html, f"No og:title on {url}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_og_description(client, url):
    html = client.get(url).data.decode()
    assert 'property="og:description"' in html, f"No og:description on {url}"


@pytest.mark.parametrize("url", _SEO_PAGES)
def test_twitter_card(client, url):
    html = client.get(url).data.decode()
    assert 'name="twitter:card"' in html, f"No twitter:card on {url}"


# ── JSON-LD on key pages ──

def test_homepage_json_ld(client):
    html = client.get("/").data.decode()
    assert "application/ld+json" in html
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert m
    data = json.loads(m.group(1))
    assert data["@type"] == "WebSite"


def test_agent_json_ld(client):
    html = client.get("/agents/jett/").data.decode()
    assert "application/ld+json" in html
    assert "BreadcrumbList" in html


def test_leaderboard_json_ld(client):
    html = client.get("/leaderboard/eu/").data.decode()
    assert "application/ld+json" in html
    assert "ItemList" in html


def test_guide_json_ld(client):
    html = client.get("/guides/how-to-rank-up/").data.decode()
    assert "application/ld+json" in html
    assert "Article" in html


# ── Sitemap ──

def test_sitemap_returns_xml(client):
    resp = client.get("/sitemap.xml")
    assert resp.status_code == 200
    assert "xml" in resp.content_type


def test_sitemap_url_count(client):
    xml = client.get("/sitemap.xml").data.decode()
    count = xml.count("<url>")
    assert count >= 50, f"Sitemap has only {count} URLs"


def test_sitemap_has_agents(client):
    xml = client.get("/sitemap.xml").data.decode()
    assert "/agents/jett/" in xml


def test_sitemap_has_maps(client):
    xml = client.get("/sitemap.xml").data.decode()
    assert "/maps/" in xml


def test_sitemap_has_guides(client):
    xml = client.get("/sitemap.xml").data.decode()
    assert "/guides/best-agents/" in xml
    assert "/guides/weapons/" in xml


def test_sitemap_consistent_base(client):
    xml = client.get("/sitemap.xml").data.decode()
    urls = re.findall(r"<loc>([^<]+)</loc>", xml)
    bases = set()
    for u in urls[:20]:
        base = u.split("/", 3)[:3]
        bases.add("/".join(base))
    assert len(bases) == 1, f"Mixed bases: {bases}"


# ── Robots ──

def test_robots_txt(client):
    resp = client.get("/robots.txt")
    assert resp.status_code == 200
    assert b"Sitemap:" in resp.data
    assert b"Disallow: /api/" in resp.data


# ── Lang attribute ──

@pytest.mark.parametrize("url", ["/", "/agents/jett/"])
def test_html_lang(client, url):
    html = client.get(url).data.decode()
    assert 'lang="en"' in html
