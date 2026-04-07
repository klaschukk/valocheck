#!/bin/bash
# ValoCheck healthcheck — run via cron every 5 minutes
# */5 * * * * /home/klaschuk/valocheck/scripts/healthcheck.sh

ENDPOINT="http://127.0.0.1:5001/health"
SERVICE="valocheck"
LOG="/home/klaschuk/valocheck/data/healthcheck.log"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$ENDPOINT" 2>/dev/null)

if [ "$HTTP_CODE" != "200" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') FAIL (HTTP $HTTP_CODE) — restarting $SERVICE" >> "$LOG"
    sudo systemctl restart "$SERVICE"
    sleep 3
    HTTP_CODE2=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$ENDPOINT" 2>/dev/null)
    echo "$(date '+%Y-%m-%d %H:%M:%S') RESTART result: HTTP $HTTP_CODE2" >> "$LOG"
else
    # Log OK only once per hour (on :00 minute)
    MINUTE=$(date +%M)
    if [ "$MINUTE" = "00" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') OK" >> "$LOG"
    fi
fi
