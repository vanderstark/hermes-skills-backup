# Adminer (Docker) + phpMyAdmin (Monolith) — Setup Otomatis

Ditambahkan atas permintaan user: "install adminer untuk yang docker, dan
phpmyadmin untuk yang monolith". Keduanya TERBUKTI (push berhasil), jadi
jangan hapus dari varian repo.

## Docker variant → Adminer

`docker-compose.yml` tambah service:

```yaml
  adminer:
    image: adminer:4.8.1
    container_name: ccc-adminer
    restart: unless-stopped
    ports:
      - "8081:8080"
    environment:
      ADMINER_DESIGN: "price"
      ADMINER_DEFAULT_SERVER: "db"    # hostname MySQL service
    depends_on:
      db:
        condition: service_healthy
    networks:
      - ccc-net
```

- Akses: `http://localhost:8081`
- Login: Server=`db`, User=`ccc_user`, Pass=`secret` (atau `${DB_PASSWORD}`)
- Root: `root` / `${DB_ROOT_PASSWORD:-rootpass}`

README Docker: tambah blok "Database Manager — Adminer" setelah login default.

## Monolith variant → phpMyAdmin

Di `deploy-mono.sh` langkah [6/6] setelah install nginx:

```bash
export DEBIAN_FRONTEND=noninteractive
PMA_PASS="${PMA_DB_PASSWORD:-secret}"
debconf-set-selections <<EOF
phpmyadmin phpmyadmin/dbconfig-install boolean true
phpmyadmin phpmyadmin/app-password-confirm password ${PMA_PASS}
phpmyadmin phpmyadmin/mysql/admin-pass password ${PMA_PASS}
phpmyadmin phpmyadmin/mysql/app-pass password ${PMA_PASS}
phpmyadmin phpmyadmin/reconfigure-webserver multiselect
EOF
apt-get install -y -qq phpmyadmin
```

**PENTING**: `apt-get install phpmyadmin` TANPA preseed adalah interaktif
(debconf prompt) dan menggantung di script → selalu preseed dulu.

Nginx vhost terpisah (port 8082) di `/etc/nginx/sites-available/phpmyadmin`:

```nginx
server {
    listen 8082;
    server_name _;
    root /usr/share/phpmyadmin;
    index index.php;
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

- Akses: `http://<IP_SERVER>:8082`
- Login: User=`root` / Pass sesuai preseed (default `secret`)
- Aktifkan: `ln -s` ke sites-enabled + `nginx -t && systemctl reload nginx`
- README Monolith: tambah langkah 7 "Database Manager — phpMyAdmin" + baris
  akses `:8082` di daftar URL.

## Port map (konsisten antar varian)

| Layanan | Docker | Monolith |
|---|---|---|
| App utama | :8080 | :80 (nginx) / :8000 (artisan) |
| DB manager | :8081 (Adminer) | :8082 (phpMyAdmin) |

## Verifikasi

- Bash: `bash -n deploy-mono.sh`
- YAML: `python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))"`
  (fallback tanpa pyyaml: baca key top-level `version/services/volumes/networks`)