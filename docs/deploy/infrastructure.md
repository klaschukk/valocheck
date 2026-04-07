# Infrastructure — ValoCheck

## Server

- Host: same server as prevozni.com (montiko)
- User: klaschuk
- Path: `/home/klaschuk/valocheck/`

## systemd Service

File: `/etc/systemd/system/valocheck.service`

```ini
[Unit]
Description=ValoCheck Valorant Stats
After=network.target

[Service]
User=klaschuk
WorkingDirectory=/home/klaschuk/valocheck
Environment=PATH=/home/klaschuk/valocheck/venv/bin
Environment=FLASK_ENV=production
ExecStart=/home/klaschuk/valocheck/venv/bin/gunicorn -w 2 --timeout 30 -b 127.0.0.1:5001 run:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Commands:
```bash
sudo systemctl daemon-reload
sudo systemctl enable valocheck
sudo systemctl start valocheck
sudo systemctl status valocheck
sudo journalctl -u valocheck -f
```

## nginx

File: `/etc/nginx/conf.d/valocheck.conf`

```nginx
server {
    listen 80;
    server_name valocheck.gg www.valocheck.gg;

    location /static/ {
        alias /home/klaschuk/valocheck/app/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

IMPORTANT: Do NOT touch `/etc/nginx/conf.d/transit.conf` (prevozni.com on port 5000).

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Cloudflare

- DNS: A record `valocheck.gg` -> server IP (proxied)
- SSL: Full mode
- Caching: standard

## Cron Jobs

```cron
# Leaderboard update every 6 hours
0 */6 * * * /home/klaschuk/valocheck/venv/bin/python3 /home/klaschuk/valocheck/scripts/fetch_leaderboard.py
```

## Ports

| Service | Port |
|---------|------|
| ValoCheck | 5001 |
| Prevozni (transit) | 5000 |

## Deployment

```bash
cd /home/klaschuk/valocheck
git pull
sudo systemctl restart valocheck
```
