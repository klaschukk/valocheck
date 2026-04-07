"""Tests for static files."""
import os


class TestStaticFiles:
    def test_css_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/css/app.css")

    def test_favicon_svg_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/favicon.svg")

    def test_favicon_32_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/img/favicon-32x32.png")

    def test_og_image_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/img/og.png")

    def test_webmanifest_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/site.webmanifest")

    def test_agents_json_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/data/agents.json")

    def test_maps_json_exists(self):
        assert os.path.exists("/home/klaschuk/valocheck/app/static/data/maps.json")

    def test_agents_images_not_empty(self):
        agents_dir = "/home/klaschuk/valocheck/app/static/img/agents"
        assert len(os.listdir(agents_dir)) > 0

    def test_maps_images_not_empty(self):
        maps_dir = "/home/klaschuk/valocheck/app/static/img/maps"
        assert len(os.listdir(maps_dir)) > 0

    def test_css_has_root_vars(self):
        with open("/home/klaschuk/valocheck/app/static/css/app.css") as f:
            css = f.read()
        assert "--bg:" in css
        assert "--primary:" in css
        assert "--accent:" in css

    def test_css_no_important(self):
        with open("/home/klaschuk/valocheck/app/static/css/app.css") as f:
            css = f.read()
        assert "!important" not in css

    def test_webmanifest_valid_json(self):
        import json
        with open("/home/klaschuk/valocheck/app/static/site.webmanifest") as f:
            data = json.load(f)
        assert data["name"] == "ValoCheck"
