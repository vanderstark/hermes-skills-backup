# Session-specific SSL certbot/nginx pattern — nginx + certbot + Let's Encrypt

## The canonical nginx + certbot pattern for a Laravel monolith

## Setup (Ubuntu 24.04)

```bash
sudo apt install -y nginx python3-certbot-nginx

# Create only a port-80 vhost (NO listen 443 block, NO return 301)
sudo tee /etc/nginx/sites-available/ccc.example.com <<EOF
server {
    listen 80;
    server_name ccc.example.com;
    root /var/www/ccc-laravel-monolith/public;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_intercept_errors on;
    }
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    location ~ /\. {
        deny all;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ccc.example.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Certbot creates the 443 block and redirect automatically
sudo certbot --nginx -d ccc.example.com --redirect --no-eff-email --agree-tos

# Enable auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Verify
sudo certbot certificates
```

## Pitfalls

### Pitfall 1: "nginx -t fails — /etc/letsencrypt/live/ccc.example.com/fullchain.pem not found"
**Cause**: Pre-creating a `listen 443 ssl` block with cert paths before Certbot generates the cert.
**Fix**: Never pre-create a 443 block. Let `certbot --nginx` handle it.

### Pitfall 2: "HTTP 403 on /well-known/acme-challenge"
**Cause**: Manual `return 301` at server level on port 80 redirects the ACME challenge path to HTTPS.
**Fix**: Don't add `return 301` at server level. Certbot `--redirect` adds it in the right place (between `listen 443 ssl` and the server block).

### Pitfall 3: "certbot — no certificate for domain"
**Cause**: DNS A/AAAA record not pointing to server IP, or firewall blocking port 80.
**Fix**: Verify DNS with `dig ccc.example.com +short`. Ensure port 80 is open in firewall.

## Auto-renewal

```bash
# Check timer status
sudo systemctl status certbot.timer
# Expected: Active (running), 2x/day

# Test renewal (simulate 3-month expiry)
sudo certbot renew --dry-run

# Force-renewal on a specific date
sudo certbot renew --deploy-hook "systemctl reload nginx"
```

## Verification

```bash
# Check certificate expiry
sudo certbot certificates

# Check HTTPS endpoint
curl -I https://ccc.example.com

# Check SSL config
sudo openssl s_client -connect ccc.example.com:443 -servername ccc.example.com </dev/null 2>/dev/null | openssl x509 -noout -text | grep "Subject:"

# Verify HTTP→HTTPS redirect
curl -I http://ccc.example.com
# Should return: HTTP/1.1 301 Moved Permanently
# Location: https://ccc.example.com/
```

## Related Skills

- `deployment-patterns` — general deployment workflow patterns
- `docker-development` — Dockerfile/compose for SSL services
- `webapp-delivery` — shipping the production config