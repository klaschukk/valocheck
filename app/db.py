import json
import sqlite3
import time
from typing import Any

from flask import Flask, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        from flask import current_app
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
    return g.db


def init_db(app: Flask) -> None:
    with app.app_context():
        db = sqlite3.connect(app.config["DB_PATH"])
        db.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                expires_at REAL NOT NULL
            )
        """)
        db.commit()
        db.close()

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()


def cache_get(key: str) -> Any | None:
    db = get_db()
    row = db.execute("SELECT value, expires_at FROM cache WHERE key = ?", (key,)).fetchone()
    if row and row["expires_at"] > time.time():
        return json.loads(row["value"])
    if row:
        db.execute("DELETE FROM cache WHERE key = ?", (key,))
        db.commit()
    return None


def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
        (key, json.dumps(value), time.time() + ttl),
    )
    db.commit()
