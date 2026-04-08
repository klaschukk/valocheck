import json
import os

from flask import Blueprint, current_app, jsonify, request

from app.riot_api import henrik_api

api_bp = Blueprint("api", __name__)


@api_bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if "#" not in q or len(q) < 3:
        return jsonify([])
    parts = q.split("#", 1)
    name, tag = parts[0].strip(), parts[1].strip()
    if not name or not tag:
        return jsonify([])
    account = henrik_api.get_account(name, tag)
    if account:
        return jsonify([{"name": account.get("name"), "tag": account.get("tag")}])
    return jsonify([])


@api_bp.route("/autocomplete")
def autocomplete():
    """Search players DB + leaderboard for autocomplete."""
    from app.db import search_players

    q = request.args.get("q", "").strip().lower()
    if len(q) < 2:
        return jsonify([])

    results: list[dict] = []
    seen: set[str] = set()

    # 1. Search our players DB first (includes anyone ever looked up)
    try:
        db_results = search_players(q, limit=8)
        for p in db_results:
            key = f"{p['name']}#{p['tag']}".lower()
            if key not in seen:
                seen.add(key)
                results.append({
                    "name": p["name"],
                    "tag": p["tag"],
                    "rank": p.get("rank", ""),
                    "rr": "",
                    "region": (p.get("region") or "").upper(),
                })
    except Exception:
        pass

    if len(results) >= 8:
        return jsonify(results[:8])

    # 2. Search leaderboard JSON files
    lb_dir = os.path.join(os.path.dirname(current_app.root_path), "data", "leaderboard")
    if os.path.isdir(lb_dir):
        for fname in os.listdir(lb_dir):
            if not fname.endswith(".json"):
                continue
            region = fname.replace(".json", "")
            try:
                with open(os.path.join(lb_dir, fname)) as f:
                    players = json.load(f)
                for p in players:
                    name = p.get("name", "")
                    tag = p.get("tag", "")
                    if name and q in name.lower():
                        key = f"{name}#{tag}".lower()
                        if key not in seen:
                            seen.add(key)
                            results.append({
                                "name": name,
                                "tag": tag,
                                "rank": f"#{p.get('rank', 0)}",
                                "rr": f"{p.get('rr', 0)} RR",
                                "region": region.upper(),
                            })
                            if len(results) >= 8:
                                return jsonify(results)
            except (json.JSONDecodeError, OSError):
                continue

    return jsonify(results)
