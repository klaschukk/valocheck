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
    """Search leaderboard data for player name autocomplete."""
    q = request.args.get("q", "").strip().lower()
    if len(q) < 2:
        return jsonify([])

    results: list[dict] = []
    lb_dir = os.path.join(os.path.dirname(current_app.root_path), "data", "leaderboard")
    if not os.path.isdir(lb_dir):
        return jsonify([])

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
                    results.append({
                        "name": name,
                        "tag": tag,
                        "rank": p.get("rank", 0),
                        "rr": p.get("rr", 0),
                        "region": region.upper(),
                    })
                    if len(results) >= 8:
                        return jsonify(results)
        except (json.JSONDecodeError, OSError):
            continue

    return jsonify(results)
