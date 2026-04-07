"""Tests for main routes."""


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
