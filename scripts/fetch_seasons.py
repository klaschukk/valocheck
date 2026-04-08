#!/usr/bin/env python3
"""Fetch current season/act info from valorant-api.com.

Saves to: app/static/data/seasons.json
Run: venv/bin/python3 scripts/fetch_seasons.py
"""

import json
import os

import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "app", "static", "data", "seasons.json")

resp = requests.get("https://valorant-api.com/v1/seasons", timeout=15)
resp.raise_for_status()
raw = resp.json().get("data", [])

seasons = []
for s in raw:
    seasons.append({
        "uuid": s.get("uuid", ""),
        "name": s.get("displayName", ""),
        "type": s.get("type", ""),
        "start": s.get("startTime", ""),
        "end": s.get("endTime", ""),
        "parent": s.get("parentUuid", ""),
    })

with open(OUT, "w") as f:
    json.dump(seasons, f, indent=2)

print(f"Saved {len(seasons)} seasons to {OUT}")
