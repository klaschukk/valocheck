import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    RIOT_API_KEY = os.environ.get("RIOT_API_KEY", "")
    HENRIK_API_KEY = os.environ.get("HENRIK_API_KEY", "")
    HENRIK_API_BASE = "https://api.henrikdev.xyz"
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cache.db")
    BASE_URL = os.environ.get("BASE_URL", "https://valocheck.gg")
    CACHE_TTL = 300  # 5 minutes
