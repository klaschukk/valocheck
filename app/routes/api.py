from flask import Blueprint, jsonify, request

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
