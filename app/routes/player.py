from flask import Blueprint, abort, render_template, request

from app.riot_api import get_player_profile, henrik_api

player_bp = Blueprint("player", __name__)


@player_bp.route("/player/<name>/<tag>/")
def profile(name: str, tag: str):
    player = get_player_profile(name, tag)
    if not player:
        abort(404)
    return render_template("player.html", player=player)


@player_bp.route("/player/<name>/<tag>/matches/")
def matches(name: str, tag: str):
    player = get_player_profile(name, tag)
    if not player:
        abort(404)
    return render_template("matches.html", player=player)


@player_bp.route("/player/<name>/<tag>/agents/")
def agents(name: str, tag: str):
    player = get_player_profile(name, tag)
    if not player:
        abort(404)
    return render_template("agents.html", player=player)


@player_bp.route("/compare/")
def compare():
    """Compare two players side by side."""
    p1_name = request.args.get("p1", "").strip()
    p1_tag = request.args.get("t1", "").strip()
    p2_name = request.args.get("p2", "").strip()
    p2_tag = request.args.get("t2", "").strip()

    player1 = None
    player2 = None

    if p1_name and p1_tag:
        player1 = get_player_profile(p1_name, p1_tag)
    if p2_name and p2_tag:
        player2 = get_player_profile(p2_name, p2_tag)

    return render_template("compare.html", player1=player1, player2=player2,
                         p1_name=p1_name, p1_tag=p1_tag, p2_name=p2_name, p2_tag=p2_tag)


@player_bp.route("/match/<match_id>/")
def match_detail(match_id: str):
    """Full match scoreboard with all 10 players."""
    # Fetch match data directly — try cached first
    from app.db import cache_get, cache_set
    import json

    cache_key = f"match:{match_id}"
    match_data = cache_get(cache_key)

    if not match_data:
        # Need to find this match — search through recent player matches
        # For now, return 404 if not cached
        abort(404)

    return render_template("match_detail.html", match=match_data)
