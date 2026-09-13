# CCC SSL Tutorial — File Structure Template

Template for a CCC (Akademi Kepolisian) SSL setup tutorial repository
(Let's Encrypt + Certbot + native web server on Ubuntu 24.04).

## File layout

```
ccc-ssl-monolith-nginx/
├── README.md
├── TUTORIAL_SSL.md
└── scripts/
    └── setup-ssl.sh
```

## File responsibilities

### README.md
- Title: `# 🔐 CCC SSL Tutorial — Monolith + Nginx`
- One-line description of what this repo covers
- Isi (contents) table: file → purpose
- Quick install command block (curl + chmod + sudo run)
- Ringkasan table: Web Server, Certbot, Auto-Renewal, PHP Handler, SSL Termination, Cocok untuk
- Repo terkait table (links to sibling repos)
- Lisensi: `CC BY 4.0`
- Footer: `© 2026 CCC SSL Tutorial — Akademi Kepolisian`

### TUTORIAL_SSL.md
- `# 🔐 CCC SSL Tutorial — Monolith + Nginx`
- Persyaratan section (Ubuntu 24.04, domain, root/sudo, PHP 8.2-FPM, Nginx)
- Quick Start section (apt install → vhost → certbot --nginx → timer → verify)
- Langkah-Langkah section (numbered, detailed commands with explanations)
  1. Install packages
  2. Create vhost
  3. Enable vhost
  4. Run certbot --nginx
  5. Enable certbot.timer
  6. Verify
- Troubleshooting table (HTTP-01 failure, nginx -t, PHP-FPM socket, certificate not yet valid)
- Catatan penting section
- Sumber referensi table

### scripts/setup-ssl.sh
- `#!/usr/bin/env bash` shebang
- Header comment describing purpose, workflow steps, usage, important notes
- `set -euo pipefail`
- Color variables (RED, GREEN, YELLOW, NC) for info/warn/error output
- `read_prompt()` function for interactive input with defaults
- `validate_domain()` function with regex
- Step blocks:
  1. Read input (domain, email, app_path)
  2. apt-get update + install nginx, python3-certbot-nginx
  3. Write port-80 vhost (NO 443 block, NO return 301)
  4. Enable vhost, disable default, nginx -t, restart nginx
  5. Run `certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --redirect --no-eff-email`
  6. systemctl enable certbot.timer
  7. Print summary + verification commands
- `exit 0` at end
- chmod +x on install

## Variants

| Variant | Web Server | Certbot Package |
|---------|-----------|-----------------|
| `ccc-ssl-monolith-nginx` | Nginx | `python3-certbot-nginx` |
| `ccc-ssl-monolith-apache` | Apache | `python3-certbot-apache` |
| `ccc-ssl-docker-nginx` | Nginx (container) | `certbot/certbot` |

## Checklist (before commit)

- [ ] Script passes `bash -n` syntax check
- [ ] Script is executable (`chmod +x`)
- [ ] `bash -n` passes
- [ ] README Quick Install URLs point to the correct repo
- [ ] Ringkasan table PHP Handler socket path is version-correct
- [ ] Tutorial troubleshooting mentions DNS propagation timing (40-60s)
- [ ] License footer matches `© 2026 CCC SSL Tutorial — Akademi Kepolisian`