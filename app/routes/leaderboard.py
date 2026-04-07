import json
import os

from flask import Blueprint, current_app, render_template

from app.riot_api import REGIONS, henrik_api

leaderboard_bp = Blueprint("leaderboard", __name__)


def _load_leaderboard(region: str) -> list[dict]:
    """Load cached leaderboard from JSON file, fallback to live API."""
    lb_dir = os.path.join(os.path.dirname(current_app.root_path), "data", "leaderboard")
    fpath = os.path.join(lb_dir, f"{region}.json")
    if os.path.exists(fpath):
        try:
            with open(fpath) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return henrik_api.get_leaderboard(region, size=100) or []


@leaderboard_bp.route("/leaderboard/")
def index():
    return render_template("leaderboard.html", regions=REGIONS, region=None, players=[])


@leaderboard_bp.route("/leaderboard/<region>/")
def region(region: str):
    if region not in REGIONS:
        region = "eu"
    players = _load_leaderboard(region)
    return render_template("leaderboard.html", regions=REGIONS, region=region, players=players)
