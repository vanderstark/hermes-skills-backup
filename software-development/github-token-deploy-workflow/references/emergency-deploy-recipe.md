---
title: Emergency Deploy Recipe (Tools Failed)
description: "Satu blok perintah tunggal untuk user jalankan saat semua tools agent gagal."
---

# Emergency Deploy Recipe

Gunakan ini hanya bila **semua tools agent** (`terminal`, `execute_code`, `write_file`, `shell`) mengalami error teknis internal dan tidak bisa dieksekusi.

## Langkah 1: Buat Repository di GitHub (via browser)

Buka [https://github.com/new](https://github.com/new), lalu isi:
- **Repository name**: `police-llm-gateway-laravel`
- **Description**: "Polri LLM Gateway Laravel v1.8 (Dockerized, 14 Fitur)"
- **Public / Private**: sesuai keinginan
- Klik **Create repository** (jangan inisialisasi dengan README)

## Langkah 2: Salin & Jalankan Perintah di Terminal Anda

Ganti `YOUR_NEW_TOKEN` di bawah dengan **Personal Access Token (PAT)** Anda.

```bash
# 1. Pastikan semua file ada di folder project Laravel
cd /opt/data/polri-llm-gateway-laravel
ls -la Dockerfile docker-compose.yml app/Models/ApiKey.php app/Http/Controllers/LlmProviderController.php database/migrations/2024_01_01_000005_create_api_keys_table.php README.md

# 2. Inisialisasi ulang Git
rm -rf .git && git init

# 3. Konfigurasi identitas
git config user.email "vanderstark@users.noreply.github.com"
git config user.name "vanderstark"

# 4. Tambahkan semua file
git add .

# 5. Commit
git commit -m "chore: complete Laravel port with Docker Compose, Dockerfile, README, 14 features"

# 6. Push ke GitHub (PAKE TOKEN BARU)
git push https://YOUR_NEW_TOKEN@github.com/vanderstark/police-llm-gateway-laravel.git main -f

# 7. Hapus token dari file temp
rm -f /tmp/gh_token_file
```

## Langkah 3: Verifikasi di GitHub

1. Buka [https://github.com/vanderstark/police-llm-gateway-laravel](https://github.com/vanderstark/police-llm-gateway-laravel)
2. Pastikan `README.md`, `docker-compose.yml`, `Dockerfile`, dan seluruh folder `app/`, `database/`, `routes/` ada.
3. Jika ada file hilang → beri tahu agent, kami akan `write_file` ulang.

## Catatan Keamanan

- Jangan pernah paste `YOUR_NEW_TOKEN = "ghp_xxx"` langsung ke chat — ketik di terminal, jalankan, lalu hapus.
- Setelah selesai, **revoke token** di [https://github.com/settings/tokens](https://github.com/settings/tokens) untuk keamanan.