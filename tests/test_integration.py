"""Integration tests — cross-page links, data consistency, navigation."""

import re

import pytest


# ── Navigation consistency ──

_PAGES_WITH_NAV = ["/", "/agents/", "/leaderboard/", "/guides/", "/crosshairs/"]


@pytest.mark.parametrize("url", _PAGES_WITH_NAV)
def test_header_nav_links(client, url):
    html = client.get(url).data.decode()
    assert "/leaderboard/" in html
    assert "/agents/" in html
    assert "/maps/" in html
    assert "/crosshairs/" in html
    assert "/guides/" in html


@pytest.mark.parametrize("url", _PAGES_WITH_NAV)
def test_footer_exists(client, url):
    html = client.get(url).data.decode()
    assert "site-footer" in html


@pytest.mark.parametrize("url", _PAGES_WITH_NAV)
def test_logo_links_home(client, url):
    html = client.get(url).data.decode()
    assert 'href="/"' in html
    assert "VALO" in html


# ── Agent pages consistency ──

def test_agents_index_has_cards(client):
    resp = client.get("/agents/")
    html = resp.data.decode()
    # Should have at least 20 agent cards
    count = html.count("content-card")
    assert count >= 20, f"Only {count} agent cards"


def test_agent_detail_has_abilities(client):
    resp = client.get("/agents/jett/")
    html = resp.data.decode()
    assert "ability-card-v2" in html or "ability-v2" in html


def test_agent_links_back_to_index(client):
    html = client.get("/agents/jett/").data.decode()
    assert "/agents/" in html


# ── Map pages consistency ──

def test_maps_index_has_cards(client):
    html = client.get("/maps/").data.decode()
    count = html.count("map-card")
    assert count >= 10, f"Only {count} map cards"


def test_map_detail_has_name(client):
    html = client.get("/maps/bind/").data.decode()
    assert "Bind" in html


# ── Leaderboard consistency ──

def test_leaderboard_index_has_regions(client):
    html = client.get("/leaderboard/").data.decode()
    assert "region-tab" in html
    assert "Europe" in html or "eu" in html.lower()


def test_leaderboard_eu_has_rows(client):
    html = client.get("/leaderboard/eu/").data.decode()
    count = html.count("lb-row")
    assert count >= 10, f"Only {count} leaderboard rows"


def test_leaderboard_players_link_to_profiles(client):
    html = client.get("/leaderboard/eu/").data.decode()
    assert "/player/" in html


# ── Insights consistency ──

def test_insights_has_agent_rows(client):
    html = client.get("/insights/").data.decode()
    count = html.count("insights-row")
    assert count >= 10, f"Only {count} insight rows"


def test_insights_has_role_filters(client):
    html = client.get("/insights/").data.decode()
    assert "Duelist" in html
    assert "Controller" in html


# ── Tips page links ──

def test_tips_links_to_guides(client):
    html = client.get("/tips/").data.decode()
    assert "/guides/how-to-rank-up/" in html
    assert "/guides/best-agents/" in html
    assert "/guides/weapons/" in html


# ── Search flow ──

def test_search_with_valid_id_redirects(client):
    resp = client.get("/search?q=TenZ%230505")
    assert resp.status_code == 302
    assert "/player/TenZ/0505/" in resp.headers["Location"]


def test_search_without_hash_shows_error(client):
    resp = client.get("/search?q=somename")
    assert resp.status_code == 200
    assert b"valid Riot ID" in resp.data


# ── Homepage content ──

def test_homepage_has_search(client):
    html = client.get("/").data.decode()
    assert "search-input" in html


def test_homepage_has_top_players(client):
    html = client.get("/").data.decode()
    assert "home-lb" in html


def test_homepage_has_agents(client):
    html = client.get("/").data.decode()
    assert "home-agent" in html


def test_homepage_has_guides(client):
    html = client.get("/").data.decode()
    assert "/guides/" in html


# ── Cross-links ──

def test_agent_detail_has_insights_data(client):
    """Agent pages should have role info."""
    html = client.get("/agents/sage/").data.decode()
    assert "Sentinel" in html


def test_crosshairs_has_pro_presets(client):
    html = client.get("/crosshairs/").data.decode()
    assert "xh-pro" in html


def test_compare_page_has_form(client):
    html = client.get("/compare/").data.decode()
    assert "Player 1" in html
    assert "Player 2" in html


def test_seasons_page_has_timeline(client):
    html = client.get("/seasons/").data.decode()
    assert "season-row" in html or "Current Season" in html
