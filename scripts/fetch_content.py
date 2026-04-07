#!/usr/bin/env python3
"""Fetch agent and map data from valorant-api.com.

Saves:
  - app/static/data/agents.json
  - app/static/data/maps.json
  - app/static/img/agents/{slug}.png
  - app/static/img/maps/{slug}.png
"""

import json
import logging
import os
import re
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

session = requests.Session()


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = slug.replace("/", "-").replace("'", "")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def download_image(url: str, path: str) -> bool:
    if os.path.exists(path):
        return True
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        return True
    except requests.RequestException as e:
        logger.error("Failed to download %s: %s", url, e)
        return False


def fetch_agents() -> list[dict]:
    logger.info("Fetching agents...")
    resp = session.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true", timeout=15)
    resp.raise_for_status()
    raw = resp.json().get("data", [])

    img_dir = os.path.join(STATIC_DIR, "img", "agents")
    os.makedirs(img_dir, exist_ok=True)

    agents: list[dict] = []
    for a in raw:
        name = a.get("displayName", "")
        slug = slugify(name)
        if not slug:
            continue

        icon_url = a.get("displayIcon", "")
        if icon_url:
            download_image(icon_url, os.path.join(img_dir, f"{slug}.png"))

        role = a.get("role") or {}
        abilities = []
        for ab in a.get("abilities", []):
            abilities.append({
                "slot": ab.get("slot", ""),
                "name": ab.get("displayName", ""),
                "description": ab.get("description", ""),
            })

        agents.append({
            "uuid": a.get("uuid", ""),
            "name": name,
            "slug": slug,
            "description": a.get("description", ""),
            "role": role.get("displayName", ""),
            "role_icon": role.get("displayIcon", ""),
            "abilities": abilities,
            "icon": f"/static/img/agents/{slug}.png",
        })

    agents.sort(key=lambda x: x["name"])

    data_dir = os.path.join(STATIC_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "agents.json"), "w") as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d agents", len(agents))
    return agents


def fetch_maps() -> list[dict]:
    logger.info("Fetching maps...")
    resp = session.get("https://valorant-api.com/v1/maps", timeout=15)
    resp.raise_for_status()
    raw = resp.json().get("data", [])

    img_dir = os.path.join(STATIC_DIR, "img", "maps")
    os.makedirs(img_dir, exist_ok=True)

    maps: list[dict] = []
    for m in raw:
        name = m.get("displayName", "")
        slug = slugify(name)
        if not slug:
            continue

        # Skip "The Range" practice map
        if slug == "the-range":
            continue

        splash_url = m.get("splash", "") or m.get("listViewIcon", "")
        if splash_url:
            download_image(splash_url, os.path.join(img_dir, f"{slug}.png"))

        callouts = []
        for c in m.get("callouts") or []:
            callouts.append({
                "region": c.get("regionName", ""),
                "super_region": c.get("superRegionName", ""),
            })

        maps.append({
            "uuid": m.get("uuid", ""),
            "name": name,
            "slug": slug,
            "coordinates": m.get("coordinates", ""),
            "splash": f"/static/img/maps/{slug}.png",
            "callouts": callouts,
        })

    maps.sort(key=lambda x: x["name"])

    data_dir = os.path.join(STATIC_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "maps.json"), "w") as f:
        json.dump(maps, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d maps", len(maps))
    return maps


if __name__ == "__main__":
    fetch_agents()
    time.sleep(1)
    fetch_maps()
    logger.info("Done!")
