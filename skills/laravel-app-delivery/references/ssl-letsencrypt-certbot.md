# SSL Let's Encrypt via Certbot — 4 Varian (Docker/Monolith × Nginx/Apache) (Ubuntu 24.04)

Pola terbukti membuat tutorial + script otomatis HTTPS untuk empat varian
repo Laravel (Docker × Apache/Nginx, Monolith × Nginx/Apache), di-push ke
4 repo GitHub TERPISAH (`<app>-ssl-docker-nginx`, `<app>-ssl-docker-apache`,
`<app>-ssl-monolith-nginx`, `<app>-ssl-monolith-apache`, PUBLIC).
Dipicu: user minta "tutorial SSL Let's Encrypt" untuk aplikasi yang sudah
punya 2 varian repo, PLUS permintaan terpisah "nginx DAN apache semua repo
yang berbeda".

## Arsitektur per varian

| Varian | Terminasi SSL | Certbot | Auto-renewal |
|--------|--------------|---------|--------------|
| Docker Nginx | `jwilder/nginx-proxy:alpine` container (port 80/443) | `jrcs/letsencrypt-nginx-proxy-companion` sidecar | cron internal certbot container (12 jam) |
| Docker Apache | `debian:bookworm-slim` + Apache mod_ssl + mod_proxy_fcgi (port 80/443) | certbot sidecar **webroot** (`certbot certonly --webroot -w /var/www/certbot`) | sidecar loop `while true; sleep 12h && certbot renew --webroot` | 

Detail urutan boot + vhost template + Dockerfile custom: lihat
`references/ssl-letsencrypt-certbot-apache-docker.md`.
| Monolith Nginx | Nginx native (Ubuntu) | `python3-certbot-nginx` (plugin --nginx) | `certbot.timer` systemd (2x/hari) |
| Monolith Apache | Apache 2.4 native (Ubuntu) | `python3-certbot-apache` (plugin --apache) | `certbot.timer` systemd (2x/hari) |

## Docker: docker-compose.ssl.yml (override file)

Jangan edit docker-compose.yml utama — buat FILE OVERRIDE
`docker-compose.ssl.yml`, deploy dengan
`docker compose -f docker-compose.yml -f docker-compose.ssl.yml up -d --build`.

- Service `nginx-proxy`: mount `/var/run/docker.sock`, port 80+443, label
  `com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy=true`.
- Service `certbot`: env `NGINX_PROXY_CONTAINER=ccc-nginx-proxy` +
  `DEFAULT_EMAIL`; mount sock + certs/vhost.d/html dirs (rw untuk certbot,
  ro untuk proxy).
- Service `app`: env `VIRTUAL_HOST`, `VIRTUAL_PORT=8000` (port INTERNAL app),
  `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL`, `APP_URL=https://...`,
  `FORCE_HTTPS=true`. HAPUS expose port 8080 dari base compose (proxy yang
  handle). Subdomain adminer = service kedua dengan
  `VIRTUAL_HOST=adminer.$DOMAIN`.
- Folder `docker/certs`, `docker/vhost.d`, `docker/html` dibuat dulu
  (auto-generated isi, jangan commit).
- Verifikasi: `docker compose logs -f certbot` cari "Certificate obtained";
  `curl -sI https://$DOMAIN`.

## Monolith: certbot --nginx

- `sudo apt install -y certbot python3-certbot-nginx`
- Nginx vhost (sites-available/ccc): server_name, root `$APP/public`,
  fastcgi_pass `unix:/var/run/php/php8.3-fpm.sock`, block `location ~
  /\\.(?!well-known).* { deny all; }` — WAJIB biarkan well-known terbuka
  untuk ACME challenge.
- Jalankan: `sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos
  --no-eff-email --redirect --hsts --keep-until-expiring`
- Auto-renewal TIDAK perlu cron manual — Ubuntu 24.04 buat `certbot.timer`
  otomatis. Verifikasi: `systemctl list-timers | grep certbot` + `sudo
  certbot renew --dry-run`.
- Update `.env` Laravel: `APP_URL=https://...`, `FORCE_HTTPS=true`,
  `SESSION_SECURE_COOKIE=true` lalu `php artisan config:clear`.

## Monolith: certbot --apache

- `sudo apt install -y certbot python3-certbot-apache`
- Aktifkan modul Apache yang dibutuhkan:
  `sudo a2enmod ssl proxy proxy_fcgi rewrite headers deflate expires http2`
- Apache VirtualHost (sites-available/ccc.conf): Port 80 (redirect ke 443) +
  Port 443 (SSLEngine on, DocumentRoot, ProxyPassMatch fcgi://127.0.0.1:9000/
  `$APP/public` untuk PHP, SSLCertificateFile/KeyFile path Let's Encrypt).
  Header security (X-Frame-Options, HSTS), gzip (mod_deflate), cache static.
  JANGAN lupa `AllowOverride All` di Directory public/ untuk Laravel.
- Jalankan: `sudo certbot --apache -d $DOMAIN --email $EMAIL --agree-tos
  --no-eff-email --redirect --hsts --keep-until-expiring`
- Auto-renewal: `certbot.timer` systemd (sama seperti Nginx). Verifikasi:
  `sudo certbot renew --dry-run`.
- Update `.env` Laravel sama seperti Nginx monolith.

## Docker: Apache + certbot (webroot)

- Base: `debian:bookworm-slim` container, install `apache2 certbot openssl`
  di entrypoint atau Dockerfile.
- Modul Apache wajib: `ssl rewrite proxy proxy_fcgi headers deflate`
- VirtualHost 80: redirect ke 443 + Alias /.well-known/acme-challenge/
  ke `/var/www/html/.well-known/acme-challenge/` (untuk webroot).
- VirtualHost 443: SSLEngine on, SSLCertificateFile/KeyFile
  `/etc/letsencrypt/live/$DOMAIN/fullchain.pem` dan privkey.pem,
  SetHandler proxy:fcgi://app:9000 (php-fpm di container app), security
  headers, cache.
- Certbot di host (bukan di container — lebih simpel): 
  `sudo certbot certonly --webroot -w /var/www/ccc-laravel-docker/app/public
  -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email`
  lalu restart apache container, atau certbot inside container via docker
  exec (lebih kompleks).
- Auto-renewal: certbot di host pakai cron `0 */12 * * * certbot renew
  --quiet && docker compose restart apache` — manual setup.

## Script otomatis (scripts/setup-ssl-{docker,monolith}.sh)

Pola script interaktif yang terbukti lulus `bash -n`:
1. `set -euo pipefail` + warna output + fungsi info/ok/warn/err.
2. Cek `[[ $EUID -ne 0 ]]` → minta sudo.
3. `read -rp` untuk domain + email (+ path app utk monolith).
4. Cek DNS SEBELUM certbot: `SERVER_IP=$(curl -4 -s ifconfig.me)`,
   `DOMAIN_IP=$(dig +short "$DOMAIN")` — kalau beda, warn + konfirmasi
   lanjut (certbot bakal gagal kalau DNS belum diarahkan).
5. Docker: heredoc generate `docker-compose.ssl.yml` (variabel domain/email
   di-escape: `\${DB_PASSWORD}` supaya tidak diexpand saat tulis file);
   loop tunggu cert (10s x 18 = 3 menit, cek `ls /etc/nginx/certs/*.pem |
   grep private_key` di container).
6. Monolith: heredoc tulis `/etc/nginx/sites-available/ccc` — ESCAPE `$uri`,
   `$query_string`, `$document_root` sebagai `\$uri` dst. (kalau tidak,
   bash expand jadi kosong saat tulis file!).
7. Akhiri: curl -sI verifikasi + print ringkasan (URL, email, renewal, link
   SSL Labs).

Pitfall heredoc: di dalam `cat > file <<EOF`, semua `$` variabel nginx
(`$uri`, `$host`) harus `\\$` atau hasilnya string kosong; sebaliknya
variabel bash yang mau di-embed (domain) biarkan polos. Variabel yang mau
di-embed nanti oleh docker-compose env pakai `\\${VAR}`.

Apache heredoc extra: `$` di `$APP_PATH`, `\\.php$`, `\${APACHE_LOG_DIR}`
harus di-escape `\\$`; direktif `ProxyPassMatch fcgi://...` dan
`<FilesMatch \\.php$>` sensitif terhadap escape (lihat template di
TUTORIAL_SSL.md varian apache).

## Struktur repo tutorial (terpisah dari app)

```
<app>-ssl-docker-nginx/          # Satu repo PER VARIAN (user aturan: terpisah)
├── README.md                  # quick install + perbandingan varian
├── TUTORIAL_SSL.md            # lengkap: arsitektur, config, .env, verifikasi, troubleshooting
└── scripts/
    └── setup-ssl.sh           # chmod +x, bash -n verified
```

Empat repo serupa: `<app>-ssl-docker-nginx`, `<app>-ssl-docker-apache`,
`<app>-ssl-monolith-nginx`, `<app>-ssl-monolith-apache`.

Cara pakai di README: `curl -sSL
https://raw.githubusercontent.com/user/<app>-ssl-<variant>/main/scripts/setup-ssl.sh
-o setup-ssl.sh && sudo ./setup-ssl.sh`

Batch 4 repo dengan `delegate_task`: kirim 3 task subagent paralel (masing-
masing bikin 1 folder + 3 file), kerjakan repo ke-4 sendiri di sesi utama
(karena `max_concurrent_children = 3`). Setelah subagent selesai: cek
`find` tiap folder, LENGKAPI file yang belum ditulis subagent (biasanya
TUTORIAL/script baru dibuat setelah README), `bash -n` semua script.
Jangan ulangi heritage — verifikasi isi folder pasca-delegasi.

## Checklist verifikasi

- `bash -n scripts/setup-ssl.sh` (4×) → 0 error
- GitHub API `GET /repos/user/<app>-ssl-<varian>` → exists (kalau NOT_FOUND,
  create dulu — lihat pitfall create-repo di SKILL.md)
- `git push` pakai token pattern (pitfall 24 di SKILL.md)
- curl API contents/ → file lengkap + commit sha benar
- Kalau API balas `Bad credentials` di tengah batch → cek `GET /user`
  (200 = token OK, retry; 401 = token invalid, minta token baru ke user)
