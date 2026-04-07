"""Tests for API routes."""


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
