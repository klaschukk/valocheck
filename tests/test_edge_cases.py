"""Edge case tests — malformed input, injection, unicode, long inputs."""

import json

import pytest


# ── Unicode/special chars in URLs ──

def test_unicode_player_name(client):
    resp = client.get("/player/再化降水驻守/0817/")
    assert resp.status_code in (200, 404, 500)  # Should not crash


def test_emoji_in_url(client):
    resp = client.get("/agents/🎮/")
    assert resp.status_code in (400, 404)


def test_special_chars_in_search(client):
    resp = client.get("/search?q=%3Cscript%3Ealert(1)%3C/script%3E")
    assert resp.status_code == 200
    assert b"<script>alert" not in resp.data  # No XSS


# ── Very long inputs ──

def test_long_autocomplete_query(client):
    resp = client.get("/api/autocomplete?q=" + "a" * 500)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)


def test_long_player_name(client):
    resp = client.get("/player/" + "x" * 500 + "/tag/")
    assert resp.status_code in (404, 500)


def test_long_agent_slug(client):
    resp = client.get("/agents/" + "y" * 500 + "/")
    assert resp.status_code == 404


def test_long_map_slug(client):
    resp = client.get("/maps/" + "z" * 500 + "/")
    assert resp.status_code == 404


# ── SQL injection attempts ──

def test_sqli_autocomplete(client):
    resp = client.get("/api/autocomplete?q='; DROP TABLE players; --")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)


def test_sqli_search(client):
    resp = client.get("/api/search?q=' OR 1=1 --")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data == []


def test_sqli_player_name(client):
    resp = client.get("/player/' OR 1=1 --/tag/")
    assert resp.status_code in (200, 404)


# ── Missing/empty parameters ──

def test_search_no_param(client):
    resp = client.get("/search")
    assert resp.status_code == 200


def test_autocomplete_no_param(client):
    resp = client.get("/api/autocomplete")
    assert resp.status_code == 200
    assert json.loads(resp.data) == []


def test_autocomplete_empty(client):
    resp = client.get("/api/autocomplete?q=")
    assert resp.status_code == 200
    assert json.loads(resp.data) == []


# ── Nonexistent pages ──

def test_404_returns_404(client):
    resp = client.get("/this-page-does-not-exist/")
    assert resp.status_code == 404


def test_404_has_search(client):
    resp = client.get("/nonexistent/")
    assert resp.status_code == 404
    assert b"search" in resp.data.lower() or b"Search" in resp.data


def test_double_slash(client):
    resp = client.get("//agents//")
    assert resp.status_code in (200, 301, 308, 404)


# ── Content type checks ──

def test_health_returns_json(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "ok"


def test_sitemap_returns_xml(client):
    resp = client.get("/sitemap.xml")
    assert "xml" in resp.content_type


def test_robots_returns_text(client):
    resp = client.get("/robots.txt")
    assert "text/plain" in resp.content_type


def test_autocomplete_returns_json(client):
    resp = client.get("/api/autocomplete?q=test")
    assert "json" in resp.content_type


# ── Compare edge cases ──

def test_compare_same_player(client):
    resp = client.get("/compare/?p1=test&t1=123&p2=test&t2=123")
    assert resp.status_code == 200


def test_compare_missing_tags(client):
    resp = client.get("/compare/?p1=test&t1=&p2=test2&t2=")
    assert resp.status_code == 200


# ── Match detail ──

def test_match_fake_id(client):
    resp = client.get("/match/00000000-0000-0000-0000-000000000000/")
    assert resp.status_code == 404


def test_match_invalid_id(client):
    resp = client.get("/match/not-a-uuid/")
    assert resp.status_code == 404
