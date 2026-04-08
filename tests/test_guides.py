"""Tests for SEO guide pages."""


class TestGuides:
    def test_best_agents_returns_200(self, client):
        resp = client.get("/guides/best-agents/")
        assert resp.status_code == 200

    def test_best_agents_has_content(self, client):
        resp = client.get("/guides/best-agents/")
        assert b"S-Tier" in resp.data or b"Best Agent" in resp.data

    def test_best_agents_has_json_ld(self, client):
        resp = client.get("/guides/best-agents/")
        assert b"application/ld+json" in resp.data

    def test_rank_distribution_returns_200(self, client):
        resp = client.get("/guides/rank-distribution/")
        assert resp.status_code == 200

    def test_rank_distribution_has_chart(self, client):
        resp = client.get("/guides/rank-distribution/")
        assert b"rank-dist" in resp.data

    def test_rank_distribution_has_all_ranks(self, client):
        resp = client.get("/guides/rank-distribution/")
        assert b"Iron" in resp.data
        assert b"Radiant" in resp.data

    def test_crosshair_settings_returns_200(self, client):
        resp = client.get("/guides/crosshair-settings/")
        assert resp.status_code == 200

    def test_crosshair_settings_has_codes(self, client):
        resp = client.get("/guides/crosshair-settings/")
        assert b"0;P;" in resp.data

    def test_how_to_rank_up_returns_200(self, client):
        resp = client.get("/guides/how-to-rank-up/")
        assert resp.status_code == 200

    def test_how_to_rank_up_has_sections(self, client):
        resp = client.get("/guides/how-to-rank-up/")
        assert b"Fundamentals" in resp.data
        assert b"Economy" in resp.data

    def test_tips_links_to_guides(self, client):
        resp = client.get("/tips/")
        assert b"/guides/" in resp.data
