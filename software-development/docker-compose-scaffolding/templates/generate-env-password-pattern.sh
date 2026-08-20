#!/usr/bin/env bash
#
# generate-env.sh (reusable skeleton)
#
# Adapt the sed targets below to the specific stack's .env.example keys.
# Pattern used consistently across Zabbix/NetBox/GLPI/Wazuh Docker Compose
# generators: copy .env.example -> .env, overwrite password/secret fields
# with openssl-rand-derived random values, print generated superuser
# credentials once (not recoverable after — user must capture now).
#
set -euo pipefail

if [ -f .env ]; then
    read -rp ".env sudah ada. Timpa? (y/N): " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 0
fi

cp .env.example .env

# Alphanumeric password, 20-24 chars — safe for shell/YAML/sed interpolation
DB_PASSWORD="$(openssl rand -base64 24 | tr -d '=+/' | cut -c1-24)"
API_PASSWORD="$(openssl rand -base64 24 | tr -d '=+/' | cut -c1-24)"
# For fields requiring mixed-case + digit + symbol (some stacks enforce
# password complexity), append a fixed suffix guaranteeing all classes:
# SUPERUSER_PASSWORD="$(openssl rand -base64 18 | tr -d '=+/' | cut -c1-18)Aa1!"

# Django/Rails-style long secret keys (50+ random chars, no shell metachars)
SECRET_KEY="$(openssl rand -base64 64 | tr -d '=+/\n' | cut -c1-50)"

# Repeat one sed line per .env key that needs a generated value:
sed -i "s#^DB_PASSWORD=.*#DB_PASSWORD=${DB_PASSWORD}#" .env
sed -i "s#^API_PASSWORD=.*#API_PASSWORD=${API_PASSWORD}#" .env
sed -i "s#^SECRET_KEY=.*#SECRET_KEY=${SECRET_KEY}#" .env

echo ""
echo "════════════════════════════════════════════════════════"
echo "  .env berhasil dibuat dengan kredensial random"
echo "════════════════════════════════════════════════════════"
echo ""
echo "  CATAT kredensial yang relevan sekarang — tidak akan"
echo "  ditampilkan ulang oleh script ini. Kredensial lengkap"
echo "  juga tersimpan di file .env (jaga kerahasiaannya)."
echo ""
echo "════════════════════════════════════════════════════════"

# Notes for adapting this skeleton:
# - If the stack has a password tied to a static bcrypt hash shipped in a
#   config file (e.g. Wazuh Indexer's internal_users.yml), do NOT randomize
#   that specific field here — generating a random value that no longer
#   matches the pre-baked hash will break auth. Document the manual
#   hash-regeneration procedure in the stack's own README instead, and only
#   randomize the OTHER passwords (API/dashboard) that aren't hash-locked.
# - hex tokens (API tokens, etc.) commonly want: openssl rand -hex 20
