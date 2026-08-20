#!/usr/bin/env bash
# smoke-test: run against a live server to verify all SSL setup steps
# Usage: bash scripts/test_ssl_setup.sh <domain> <email> <app_path>

set -euo pipefail

DOMAIN="${1:-}"
EMAIL="${2:-}"
APP_PATH="${3:-/var/www/ccc-laravel-monolith}"

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Usage: $0 <domain> <email> [app_path]"
    exit 1
fi

DOMAIN_LOW=$(echo "$DOMAIN" | tr '[:upper:]' '[:lower:]')

echo "==> Testing SSL setup for $DOMAIN"

# 1. Check Nginx vhost exists and is port-80 only
echo "==> Checking vhost..."
VHOST="/etc/nginx/sites-available/${DOMAIN_LOW}"
if [ ! -f "$VHOST" ]; then
    echo "FAIL: vhost not found at $VHOST"
    exit 1
fi

if grep -q "listen 443 ssl" "$VHOST"; then
    echo "FAIL: vhost contains manual listen 443 ssl block (should be added by certbot)"
    exit 1
fi

if grep -q "return 301" "$VHOST"; then
    echo "FAIL: vhost contains manual return 301 (breaks HTTP-01 challenge)"
    exit 1
fi
echo "PASS: vhost is port-80 only, no manual 443 or redirect"

# 2. Check Nginx config valid
echo "==> Testing nginx config..."
if ! sudo nginx -t >/dev/null 2>&1; then
    echo "FAIL: nginx -t failed"
    exit 1
fi
echo "PASS: nginx -t"

# 3. Check certbot certificates exist
echo "==> Checking certbot certificates..."
if ! sudo certbot certificates | grep -q "$DOMAIN"; then
    echo "FAIL: certbot doesn't show certificate for $DOMAIN"
    exit 1
fi
echo "PASS: certbot certificate found"

# 4. Check certbot timer active
echo "==> Checking certbot timer..."
if ! sudo systemctl is-active certbot.timer >/dev/null 2>&1; then
    echo "FAIL: certbot.timer not active"
    exit 1
fi
echo "PASS: certbot.timer active"

# 5. Check HTTPS endpoint
echo "==> Testing HTTPS endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" --max-time 10)
if [ "$HTTP_CODE" != "200" ]; then
    echo "FAIL: HTTPS returned $HTTP_CODE (expected 200)"
    exit 1
fi
echo "PASS: HTTPS returns 200"

# 6. Check HTTP→HTTPS redirect
echo "==> Testing HTTP→HTTPS redirect..."
REDIRECT_LOCATION=$(curl -s -I "http://$DOMAIN" --max-time 10 | grep -i "^location:" | head -1)
if ! echo "$REDIRECT_LOCATION" | grep -q "https://$DOMAIN"; then
    echo "FAIL: HTTP redirect missing or wrong: $REDIRECT_LOCATION"
    exit 1
fi
echo "PASS: HTTP redirects to HTTPS"

# 7. Check cert expiry > 30 days
echo "==> Checking certificate expiry..."
EXPIRY=$(sudo certbot certificates | grep -A5 "$DOMAIN" | grep "Expiry Date:" | head -1 | sed 's/.*Expiry Date: //')
if [ -z "$EXPIRY" ]; then
    echo "WARN: Could not parse expiry date"
else
    EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
    NOW_EPOCH=$(date +%s)
    DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
    if [ "$DAYS_LEFT" -lt 30 ]; then
        echo "WARN: Certificate expires in $DAYS_LEFT days"
    else
        echo "PASS: Certificate valid for $DAYS_LEFT days"
    fi
fi

echo ""
echo "All checks passed! ✓"
exit 0