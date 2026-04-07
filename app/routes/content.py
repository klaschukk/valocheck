import json
import os

from flask import Blueprint, abort, current_app, render_template

content_bp = Blueprint("content", __name__)

_agents_cache: list[dict] | None = None
_maps_cache: list[dict] | None = None


def _get_agents() -> list[dict]:
    global _agents_cache
    if _agents_cache is not None:
        return _agents_cache
    path = os.path.join(current_app.root_path, "static", "data", "agents.json")
    if os.path.exists(path):
        with open(path) as f:
            _agents_cache = json.load(f)
    else:
        _agents_cache = []
    return _agents_cache


def _get_maps() -> list[dict]:
    global _maps_cache
    if _maps_cache is not None:
        return _maps_cache
    path = os.path.join(current_app.root_path, "static", "data", "maps.json")
    if os.path.exists(path):
        with open(path) as f:
            _maps_cache = json.load(f)
    else:
        _maps_cache = []
    return _maps_cache


@content_bp.route("/about/")
def about():
    return render_template("about.html")


@content_bp.route("/agents/")
def agents_index():
    agents = _get_agents()
    return render_template("agents_index.html", agents=agents)


@content_bp.route("/agents/<slug>/")
def agent_detail(slug: str):
    agents = _get_agents()
    agent = next((a for a in agents if a["slug"] == slug), None)
    if not agent:
        abort(404)
    return render_template("agent.html", agent=agent)


@content_bp.route("/maps/")
def maps_index():
    maps = _get_maps()
    return render_template("maps_index.html", maps=maps)


@content_bp.route("/maps/<slug>/")
def map_detail(slug: str):
    maps = _get_maps()
    m = next((m for m in maps if m["slug"] == slug), None)
    if not m:
        abort(404)
    return render_template("map.html", map=m)
