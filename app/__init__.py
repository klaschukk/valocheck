from flask import Flask, render_template

from config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.db import init_db
    init_db(app)

    from app.routes.main import main_bp
    from app.routes.player import player_bp
    from app.routes.leaderboard import leaderboard_bp
    from app.routes.content import content_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    return app
