import json
import os

from flask import Blueprint, Response, current_app, redirect, render_template, request, url_for

main_bp = Blueprint("main", __name__)

AGENTS_LIST: list[dict] | None = None
MAPS_LIST: list[dict] | None = None


def _load_agents() -> list[dict]:
    global AGENTS_LIST
    if AGENTS_LIST is not None:
        return AGENTS_LIST
    path = os.path.join(current_app.root_path, "static", "data", "agents.json")
    if os.path.exists(path):
        with open(path) as f:
            AGENTS_LIST = json.load(f)
    else:
        AGENTS_LIST = []
    return AGENTS_LIST


def _load_maps() -> list[dict]:
    global MAPS_LIST
    if MAPS_LIST is not None:
        return MAPS_LIST
    path = os.path.join(current_app.root_path, "static", "data", "maps.json")
    if os.path.exists(path):
        with open(path) as f:
            MAPS_LIST = json.load(f)
    else:
        MAPS_LIST = []
    return MAPS_LIST


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if "#" in query:
        parts = query.split("#", 1)
        name = parts[0].strip()
        tag = parts[1].strip()
        if name and tag:
            return redirect(url_for("player.profile", name=name, tag=tag))
    return render_template("index.html", error="Enter a valid Riot ID (Name#TAG)")


@main_bp.route("/health")
def health():
    return {"status": "ok"}


@main_bp.route("/robots.txt")
def robots():
    base = current_app.config.get("BASE_URL", "https://valocheck.gg")
    content = f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {base}/sitemap.xml\n"
    return Response(content, mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap():
    base = current_app.config.get("BASE_URL", "https://valocheck.gg")
    urls: list[dict[str, str]] = []

    # Static pages
    static_pages = [
        ("/", "daily", "1.0"),
        ("/agents/", "weekly", "0.8"),
        ("/maps/", "weekly", "0.8"),
        ("/leaderboard/", "daily", "0.9"),
        ("/about/", "monthly", "0.3"),
    ]
    for path, freq, priority in static_pages:
        urls.append({"loc": f"{base}{path}", "changefreq": freq, "priority": priority})

    # Leaderboard regions
    for region in ["eu", "na", "ap", "kr", "br", "latam"]:
        urls.append({"loc": f"{base}/leaderboard/{region}/", "changefreq": "daily", "priority": "0.8"})

    # Agents
    agents = _load_agents()
    for agent in agents:
        slug = agent.get("slug", "")
        if slug:
            urls.append({"loc": f"{base}/agents/{slug}/", "changefreq": "monthly", "priority": "0.6"})

    # Maps
    maps = _load_maps()
    for m in maps:
        slug = m.get("slug", "")
        if slug:
            urls.append({"loc": f"{base}/maps/{slug}/", "changefreq": "monthly", "priority": "0.6"})

    # Top players from leaderboard files
    lb_dir = os.path.join(os.path.dirname(current_app.root_path), "data", "leaderboard")
    if os.path.isdir(lb_dir):
        seen: set[str] = set()
        for fname in os.listdir(lb_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(lb_dir, fname)
            try:
                with open(fpath) as f:
                    players = json.load(f)
                for p in players[:100]:
                    name = p.get("name") or p.get("gameName", "")
                    tag = p.get("tag") or p.get("tagLine", "")
                    if name and tag:
                        key = f"{name}/{tag}"
                        if key not in seen:
                            seen.add(key)
                            urls.append({
                                "loc": f"{base}/player/{name}/{tag}/",
                                "changefreq": "daily",
                                "priority": "0.5",
                            })
            except (json.JSONDecodeError, OSError):
                continue

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        xml_parts.append("  <url>")
        xml_parts.append(f"    <loc>{u['loc']}</loc>")
        xml_parts.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_parts.append(f"    <priority>{u['priority']}</priority>")
        xml_parts.append("  </url>")
    xml_parts.append("</urlset>")

    return Response("\n".join(xml_parts), mimetype="application/xml")
