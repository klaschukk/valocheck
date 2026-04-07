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


@content_bp.route("/insights/")
def insights():
    agents = _get_agents()
    # Load real agent meta if available
    meta_path = os.path.join(current_app.root_path, "static", "data", "agent_meta.json")
    agent_meta = []
    if os.path.exists(meta_path):
        try:
            with open(meta_path) as f:
                agent_meta = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    # Merge meta with agent info (icons, roles)
    agents_by_name = {a["name"]: a for a in agents}
    for m in agent_meta:
        agent_info = agents_by_name.get(m["agent"], {})
        m["icon"] = agent_info.get("icon", "")
        m["role"] = agent_info.get("role", "")
        m["slug"] = agent_info.get("slug", "")
    return render_template("insights.html", agents=agents, agent_meta=agent_meta)


@content_bp.route("/crosshairs/")
def crosshairs():
    pro_path = os.path.join(current_app.root_path, "static", "data", "pro_crosshairs.json")
    pro_crosshairs = []
    if os.path.exists(pro_path):
        try:
            with open(pro_path) as f:
                pro_crosshairs = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return render_template("crosshairs.html", pro_crosshairs=pro_crosshairs)


@content_bp.route("/tips/")
def tips():
    return render_template("tips.html")


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
