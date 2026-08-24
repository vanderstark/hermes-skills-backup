---
name: github-multi-repo-automation
description: Otomatisasi push multi-repo GitHub via API + token.
trigger: Gunakan ketika pengguna meminta otomatisasi deployment, push, update README, atau manajemen repository ke banyak repo GitHub secara bertahap.
version: 1.0
author: Hermes Agent
---
# 🎯 GitHub Multi-Repo Automation

## 📌 Trigger
Gunakan ketika pengguna meminta otomatisasi deployment, push, update README, atau manajemen repository ke banyak repo GitHub secara bertahap.

## 🧰 Komponen Utama
- GitHub API (REST) untuk membuat repository baru
- Git CLI untuk push otomatis ke banyak repo
- Token PAT yang disimpan aman di `/tmp/gh_token_file` (chmod 600)
- Script shell untuk orkestrasi otomatis
- Auto-redact token & cleanup otomatis setelah push selesai

## 🛠️ Cara Pakai
1. Buat token pribadi di https://github.com/settings/tokens/new (scope: `repo`)
2. Simpan ke file: `echo "TOKEN" > /tmp/gh_token_file && chmod 600 /tmp/gh_token_file`
3. Jalankan script push otomatis dari folder repositori
4. Script akan otomatis menghapus token setelah selesai untuk keamanan

## ⚠️ Pitfall Umum
- **Error: "remote: Repository not found"** → Token salah, kadaluarsa, atau tidak punya akses, atau **repo belum dibuat** (solusi: buat repo dulu via GitHub API atau gh CLI)
- **Error: "fatal: remote origin already exists"** → Hapus dulu dengan `git remote remove origin` atau gunakan `git remote set-url origin <url>`
- **Error: "Authentication failed"** → Pastikan scope token mencakup `repo`
- **File README duplikat** → Pastikan hanya ada satu file README di root repository
- **Tools `shell` tidak berfungsi** → Gunakan `terminal` dengan perintah eksplisit, bukan `shell` tool
- **Token terbongkar di output** → Selalu hapus dengan `rm -f /tmp/gh_token_file` setelah operasi selesai
- **File tidak terlihat di GitHub (browser)** → Branch lokal `master` tidak cocok dengan default branch repo (`main`). **Solusi:** Selalu rename branch lokal ke `main` sebelum push: `git branch -m main`
- **Push "Everything up-to-date" tapi file tidak ikut** → Pastikan branch yang dipakai adalah default branch repo. Jika tidak, rename dulu ke `main` atau gunakan `git push origin <existing-branch>`
- **Tool `write_file`/`terminal` gagal dengan "missing required field" atau "expected string, got NoneType"** → Gunakan `execute_code` + `hermes_tools.terminal/write_file` sebagai fallback yang stabil

## 🔄 Workflow Stabil untuk Push Otomatis (diperbarui dari sesi Polri LLM)

```bash
# 1. Simpan token ke file aman
echo "ghp_..." > /tmp/gh_token_file && chmod 600 /tmp/gh_token_file

# 2. Buat repo jika belum ada (via GitHub API)
TOKEN=$(cat /tmp/gh_token_file)
curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"NAMA_REPO","description":"DESKRIPSI","private":true,"auto_init":false}'

# 3. Push dari folder repo lokal
cd /path/to/repo
git branch -m main                          # WAJIB: hindari master/main mismatch
git remote set-url origin "https://$TOKEN@github.com/USER/REPO.git" 2>/dev/null || \
git remote add origin "https://$TOKEN@github.com/USER/REPO.git"
git add . && git commit -m "PESAN_COMMIT" --allow-empty
git push -u origin main --force

# 4. Hapus token untuk keamanan
rm -f /tmp/gh_token_file
```

## 📁 File Pendukung
- `scripts/push-to-github.sh` — Script push otomatis ke GitHub
- `references/error-handling.md` — Solusi untuk error umum GitHub push

## 📚 Referensi
- GitHub REST API: https://docs.github.com/en/rest
- GitHub CLI (alternatif): https://cli.github.com/manual/