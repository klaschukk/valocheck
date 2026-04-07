from flask import Blueprint, abort, render_template

from app.riot_api import get_player_profile

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
