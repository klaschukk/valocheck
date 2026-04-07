"""Tests for leaderboard routes."""


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
