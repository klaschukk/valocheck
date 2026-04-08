"""Tests for new pages: crosshairs, insights, tips, compare, about."""


class TestCrosshairs:
    def test_crosshairs_returns_200(self, client):
        resp = client.get("/crosshairs/")
        assert resp.status_code == 200

    def test_crosshairs_has_canvas(self, client):
        resp = client.get("/crosshairs/")
        assert b"xhCanvas" in resp.data

    def test_crosshairs_has_pro_presets(self, client):
        resp = client.get("/crosshairs/")
        assert b"xh-pro" in resp.data

    def test_crosshairs_has_color_picker(self, client):
        resp = client.get("/crosshairs/")
        assert b"cPicker" in resp.data

    def test_crosshairs_has_copy_button(self, client):
        resp = client.get("/crosshairs/")
        assert b"Copy" in resp.data


class TestInsights:
    def test_insights_returns_200(self, client):
        resp = client.get("/insights/")
        assert resp.status_code == 200

    def test_insights_has_filters(self, client):
        resp = client.get("/insights/")
        assert b"Duelist" in resp.data

    def test_insights_has_agents(self, client):
        resp = client.get("/insights/")
        assert b"insights-row" in resp.data


class TestTips:
    def test_tips_returns_200(self, client):
        resp = client.get("/tips/")
        assert resp.status_code == 200

    def test_tips_has_cards(self, client):
        resp = client.get("/tips/")
        assert b"tip-card" in resp.data

    def test_tips_has_difficulty(self, client):
        resp = client.get("/tips/")
        assert b"Essential" in resp.data or b"Beginner" in resp.data


class TestCompare:
    def test_compare_returns_200(self, client):
        resp = client.get("/compare/")
        assert resp.status_code == 200

    def test_compare_has_form(self, client):
        resp = client.get("/compare/")
        assert b"compare-form" in resp.data or b"Player 1" in resp.data

    def test_compare_empty_no_crash(self, client):
        resp = client.get("/compare/?p1=fake&t1=000&p2=fake2&t2=000")
        assert resp.status_code == 200


class TestAbout:
    def test_about_has_features(self, client):
        resp = client.get("/about/")
        assert b"about-features" in resp.data or b"What is" in resp.data

    def test_about_has_stats_sidebar(self, client):
        resp = client.get("/about/")
        assert b"about-stat" in resp.data


class TestAutocomplete:
    def test_autocomplete_short_query(self, client):
        resp = client.get("/api/autocomplete?q=a")
        assert resp.status_code == 200
        assert resp.json == []

    def test_autocomplete_valid_query(self, client):
        resp = client.get("/api/autocomplete?q=TH")
        assert resp.status_code == 200
        assert isinstance(resp.json, list)


class TestMatchDetail:
    def test_match_nonexistent_404(self, client):
        resp = client.get("/match/fake-match-id/")
        assert resp.status_code == 404
