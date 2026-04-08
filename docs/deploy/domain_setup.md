# Domain Setup — ValoCheck

## Steps

### 1. Buy domain
Register `valocheck.gg` (or alternative) at any registrar.

### 2. Cloudflare DNS
- Add site to Cloudflare
- Change nameservers at registrar to Cloudflare's
- Add A record: `valocheck.gg` -> `YOUR_SERVER_IP` (proxied)
- Add CNAME: `www` -> `valocheck.gg` (proxied)
- SSL: Full mode

### 3. Update nginx
Already configured in `/etc/nginx/conf.d/valocheck.conf`:
```nginx
server_name valocheck.gg www.valocheck.gg;
```

### 4. Update BASE_URL
```bash
# In systemd service or .env:
Environment=BASE_URL=https://valocheck.gg
```

Then restart:
```bash
sudo systemctl restart valocheck
```

### 5. Verify
```bash
curl -I https://valocheck.gg
# Should return 200 with proper headers
```

### 6. Google Search Console
- Add property: `https://valocheck.gg`
- Verify via Cloudflare DNS TXT record
- Submit sitemap: `https://valocheck.gg/sitemap.xml`
