#!/bin/bash
# ValoCheck nightly data refresh — leaderboard + agent/map assets
# Run via cron at 3:00 AM:
# 0 3 * * * /home/klaschuk/valocheck/scripts/nightly_refresh.sh

cd /home/klaschuk/valocheck || exit 1
LOG="data/nightly.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting nightly refresh" >> "$LOG"

# 1. Update leaderboard data
venv/bin/python3 scripts/fetch_leaderboard.py >> "$LOG" 2>&1

# 2. Update agent/map data from valorant-api.com
venv/bin/python3 scripts/fetch_content.py >> "$LOG" 2>&1

# 3. Clean expired cache entries
venv/bin/python3 -c "
import sqlite3, time, os
db_path = os.path.join('data', 'cache.db')
if os.path.exists(db_path):
    db = sqlite3.connect(db_path)
    deleted = db.execute('DELETE FROM cache WHERE expires_at < ?', (time.time(),)).rowcount
    db.execute('VACUUM')
    db.commit()
    db.close()
    print(f'Cleaned {deleted} expired cache entries')
" >> "$LOG" 2>&1

# 4. Restart service to pick up new data
sudo systemctl restart valocheck

echo "$(date '+%Y-%m-%d %H:%M:%S') Nightly refresh complete" >> "$LOG"
