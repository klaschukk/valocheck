#!/usr/bin/env python3
"""Generate pro player crosshair database.

Since crosshair data isn't available via API, this script creates
a curated database of known pro player crosshairs from community sources.

Saves to: app/static/data/pro_crosshairs.json

Time estimate: instant (static data, no API calls)
Run: venv/bin/python3 scripts/scrape_pro_crosshairs.py
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Curated pro crosshair database
# Sources: prosettings.net, vlr.gg, community wikis
PRO_CROSSHAIRS = [
    {"player": "TenZ", "team": "Sentinels", "region": "NA", "code": "0;P;c;5;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Cyan", "style": "Small + Clean"},
    {"player": "Aspas", "team": "LOUD", "region": "BR", "code": "0;P;c;1;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Classic"},
    {"player": "yay", "team": "Cloud9", "region": "NA", "code": "0;P;c;5;h;0;d;1;0l;3;0o;2;0a;1;0f;0;1b;0", "color": "White", "style": "Dot + Lines"},
    {"player": "Derke", "team": "Fnatic", "region": "EU", "code": "0;P;c;1;h;0;d;1;0l;6;0o;3;0a;1;0f;0;1b;0", "color": "Green", "style": "Wide + Dot"},
    {"player": "Demon1", "team": "Evil Geniuses", "region": "NA", "code": "0;P;c;3;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Yellow", "style": "Medium"},
    {"player": "Chronicle", "team": "FUT", "region": "EU", "code": "0;P;c;4;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Red", "style": "Standard"},
    {"player": "cNed", "team": "Natus Vincere", "region": "EU", "code": "0;P;c;1;h;0;0l;4;0o;1;0a;1;0f;0;1b;0", "color": "Green", "style": "Tight"},
    {"player": "Suygetsu", "team": "Natus Vincere", "region": "EU", "code": "0;P;c;5;h;0;0l;5;0o;2;0a;1;0f;0;1b;0", "color": "White", "style": "Long Lines"},
    {"player": "Marved", "team": "Sentinels", "region": "NA", "code": "0;P;c;1;h;0;d;1;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Dot + Classic"},
    {"player": "FNS", "team": "Sentinels", "region": "NA", "code": "0;P;c;5;h;0;0l;3;0o;3;0a;1;0f;0;1b;0", "color": "White", "style": "Small Gap"},
    {"player": "Less", "team": "LOUD", "region": "BR", "code": "0;P;c;1;h;0;0l;5;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Standard+"},
    {"player": "Alfa", "team": "KRU", "region": "LATAM", "code": "0;P;c;5;h;0;d;1;0a;1;0f;0;1b;0", "color": "White", "style": "Dot Only"},
    {"player": "Boaster", "team": "Fnatic", "region": "EU", "code": "0;P;c;1;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Classic"},
    {"player": "nAts", "team": "BBL Esports", "region": "EU", "code": "0;P;c;5;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "White", "style": "Clean"},
    {"player": "Zekken", "team": "Sentinels", "region": "NA", "code": "0;P;c;5;h;0;0l;3;0o;2;0a;1;0f;0;1b;0", "color": "Cyan", "style": "Compact"},
    {"player": "Leo", "team": "Fnatic", "region": "EU", "code": "0;P;c;1;h;0;d;1;0l;3;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Dot + Small"},
    {"player": "Johnqt", "team": "Sentinels", "region": "NA", "code": "0;P;c;3;h;0;0l;4;0o;1;0a;1;0f;0;1b;0", "color": "Yellow", "style": "Tight Gap"},
    {"player": "Zyppan", "team": "Fnatic", "region": "EU", "code": "0;P;c;4;h;0;0l;5;0o;2;0a;1;0f;0;1b;0", "color": "Red", "style": "Long Red"},
    {"player": "Sayf", "team": "Team Liquid", "region": "EU", "code": "0;P;c;5;h;0;0l;4;0o;2;0a;1;0f;0;1b;0", "color": "White", "style": "Standard White"},
    {"player": "ScreaM", "team": "Karmine Corp", "region": "EU", "code": "0;P;c;1;h;0;d;1;0l;2;0o;2;0a;1;0f;0;1b;0", "color": "Green", "style": "Dot + Tiny Lines"},
]

out_path = os.path.join(BASE, "app", "static", "data", "pro_crosshairs.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as f:
    json.dump(PRO_CROSSHAIRS, f, ensure_ascii=False, indent=2)

print(f"Saved {len(PRO_CROSSHAIRS)} pro crosshairs to {out_path}")
