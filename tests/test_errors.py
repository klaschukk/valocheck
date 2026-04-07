"""Tests for error handlers."""


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
