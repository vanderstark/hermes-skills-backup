# SSL Let's Encrypt via Certbot — Apache Docker variant (Ubuntu 24.04)

Pola terbukti membuat tutorial + script otomatis HTTPS untuk varian **Apache
sebagai reverse proxy di Docker** (CCC Laravel Docker: app php-fpm + db mysql
+ adminer). Dipicu: user minta "setup SSL Let's Encrypt via Certbot" untuk
app Docker yang mau memakai **Apache + mod_ssl** (bukan nginx-proxy).

Beda kunci vs varian nginx-proxy (lihat `ssl-letsencrypt-certbot.md`):

| Aspek | nginx-proxy (docker) | Apache (docker) — SESI INI |
|-------|---------------------|----------------------------|
| Terminasi SSL | `jwilder/nginx-proxy` | Apache 2.4 `mod_ssl` (`SSLEngine on`) |
| Certbot | `jrcs/letsencrypt-nginx-proxy-companion` (otomatis dari label) | **sidecar `certbot/certbot` + webroot** (`certbot certonly --webroot -w /var/www/certbot`) |
| Challenge path | otomatis oleh companion | `Alias /.well-known/acme-challenge/ /var/www/certbot/.well-known/acme-challenge/` + `<Directory>` `Require all granted` |
| Proxy ke app | `VIRTUAL_HOST`/`VIRTUAL_PORT` env | `mod_proxy_fcgi` → `fcgi://app:9000/...` (php-fpm) |
| HTTP→HTTPS | redirect otomatis companion | `<VirtualHost *:80>` + `RewriteCond %{HTTPS} off` + `RewriteRule ... [R=301,L]` |
| Auto-renewal | cron internal companion | sidecar loop `sleep 12h && certbot renew --webroot` (trap TERM) |

## Arsitektur target

```
Internet :80/:443 → apache container (debian:bookworm-slim + mod_ssl,
                    mod_proxy, mod_proxy_fcgi, mod_rewrite, mod_headers)
   ├─ *.php / semua → ProxyPassMatch fcgi://app:9000/var/www/html/public/$1
   └─ /.well-known/acme-challenge/ → /var/www/certbot (bind-mount, rw)
                       ↑ certbot sidecar menulis challenge di sini (webroot)
certbot sidecar: certbot/certbot, mount certs (ro) + webroot (rw) + renew (ro)
db (mysql:8.0) + adminer (8081) tidak berubah dari base compose.
```

Catatan: app Docker CCC pakai php-fpm di port **9000** (bukan 8000) —
verifikasi port internal dari Dockerfile/nginx.conf repo app SEBELUM menulis
ProxyPassMatch. Cek `EXPOSE` di Dockerfile app.

## Urutan yang TERBUKTI (script + tutorial)

1. **Cek port internal app** dari Dockerfile app (`EXPOSE 9000` untuk
   php-fpm; kalau app image hanya php-fpm, proxy fcgi ke `app:9000`).
2. Generate **dua file terpisah**:
   - `docker/apache/Dockerfile` — base `debian:bookworm-slim`, install
     `apache2 libapache2-mod-ssl libapache2-mod-proxy-html
     libapache2-mod-proxy-fcgi libapache2-mod-rewrite libapache2-mod-headers`,
     `a2enmod ssl proxy proxy_http proxy_fcgi rewrite headers`, mkdir
     webroot + docroot, `CMD ["apache2ctl", "-D", "FOREGROUND"]` (bukan
     `apache2ctl start` — itu daemonize dan container exit).
   - `docker/apache/vhost/ssl.conf` — `<VirtualHost *:80>` redirect +
     `<VirtualHost *:443>` SSLEngine on + cert paths
     `/etc/letsencrypt/live/$DOMAIN/{fullchain,privkey,chain}.pem` + HSTS/
     security headers + `ProxyPreserveHost on` + ProxyPassMatch fcgi +
     Alias well-known.
3. **Urutan boot certbot (jangan langsung up semua)**:
   a. Tulis vhost HTTP sementara (`temp-http.conf`) yang hanya serve webroot
      + Alias well-known — SSL vhost TIDAK bisa aktif sebelum cert ada
      (Apache gagal start kalau cert file belum ada).
      Backup `ssl.conf` → `ssl.conf.bak`, up hanya `apache` service.
   b. `docker compose -f docker-compose.ssl.yml run --rm certbot certonly
      --webroot -w /var/www/certbot --email $EMAIL --agree-tos
      --no-eff-email -d $DOMAIN --non-interactive`
   c. Restore `ssl.conf`, hapus `temp-http.conf`, `up -d` full stack.
4. Auto-renewal sidecar entrypoint (jangan `--force-renewal`):
   ```sh
   sh -c "trap '' TERM; while true; do sleep 12h & wait \$\$!; \
   certbot renew --webroot -w /var/www/certbot --deploy-hook 'apachectl graceful' \
   && echo 'renewed at $(date)'; done"
   ```
   Di heredoc, `$$` harus `\$\$` (escape untuk bash) dan `$(date)` boleh
   literal (diexpand saat run, bukan saat tulis).
5. Verifikasi: `curl -k https://$DOMAIN/` → 200/301; `echo | openssl
   s_client -connect $DOMAIN:443 -servername $DOMAIN | openssl x509 -noout
   -dates`; `docker compose -f docker-compose.ssl.yml ps`.

## Pitfall khusus Apache

- **`apache2ctl -D FOREGROUND`**, bukan `apache2ctl start`: container
  langsung exit kalau pakai `start` (daemonize).
- **cert file harus ada SEBELUM Apache start** — boot sequence temp-http →
  certonly → swap vhost. Jangan up Apache dengan SSL vhost tanpa cert.
- **Bind-mount certs read-only ke Apache** (`certs:/etc/letsencrypt:ro`),
  read-write hanya untuk certbot sidecar.
- **vhost mount ke `sites-enabled`** (bukan `sites-available` + a2ensite)
  — langsung aktif.
- **SSLCertificateChainFile** deprecated di Apache 2.4.8+ tapi masih umum
  dipakai; fullchain.pem sudah termasuk chain — boleh omit, tapi banyak
  tutorial tetap sertakan.
- `ProxyPassMatch ^/(.+\.php)$ fcgi://app:9000/...` — untuk Laravel cukup
  satu match php; sisanya biarkan `ProxyPass /` kalau app-nya http server,
  TAPI kalau app container = php-fpm MURNI (tanpa nginx), jangan
  `ProxyPass /` http — semua request harus lewat fcgi match + rewrite ke
  `index.php`.

## Struktur repo tutorial (varian Apache)

```
<app>-ssl-docker-apache/
├── README.md                  # overview + arsitektur + quick install + perbandingan 4 varian
├── TUTORIAL_SSL.md            # lengkap: Dockerfile, compose.ssl.yml, vhost, boot urutan, renewal, troubleshooting
└── scripts/
    └── setup-ssl.sh           # interaktif: cek root/docker/port, input domain+email,
                               # cek DNS, generate Dockerfile+vhost+compose, boot urutan certbot,
                               # up full stack, verifikasi HTTPS + expiry + adminer, simpan .domain-config
```

Script juga support subdomain adminer opsional (vhost terpisah +
`ProxyPass / http://adminer:8080/` + cert kedua).

## Checklist verifikasi

- `bash -n scripts/setup-ssl.sh` → 0 error
- Di TUTORIAL: sertakan tabel troubleshooting 8–10 kasus + bagian security
  hardening (UFW 80/443/22, HSTS preload, cipher suite)
- Penamaan repo konsisten antar varian: `-docker-nginx`, `-docker-apache`,
  `-monolith-nginx`, `-monolith-apache` — 4 repo TERPISAH (aturan user,
  jangan gabung)
