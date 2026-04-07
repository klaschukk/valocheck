"""Tests for content pages (agents, maps, about)."""


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
