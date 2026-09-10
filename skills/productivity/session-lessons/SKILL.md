---
name: session-lessons
description: "Materi singkat dari session sekarang untuk agent selanjutnya"
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Session Lessons

Skill ini menyimpan **pelajaran cepat** atau **tips** yang muncul selama sesi ini. Tidak ada langkah detail, hanya poin utama untuk agent di sesi selanjutnya.

## Akhir September 2026 - Pendekatan Git & Skills

### 🔧 Git Push Workflow (GitHub)

- Jika ada perubahan kecil, gunakan:  
  ```bash
  git add -A && git commit --amend --no-edit && git push --force
  ```

- Untuk submodule conflict:
  ```bash
  git status --porcelain
  ```

### 🗂 Local Directory Setup

- Buat repo baru langsung di `/opt/data/` sebagai subfolder.  
  Contoh: `/opt/data/Shadow-Broker/`

- Jangan clone ke luar dulu kemudian pindah.

### 📦 Push Script Backup (bila rsync tidak tersedia)

```bash
cp -r /opt/data/skills/* ./skills/
git add .
git commit -m "..."  
git push origin main
```

### ⚠️ rsync tidak selalu tersedia

Jika `rsync` tidak ada atau `sudo` tidak tersedia, gunakan:

```bash
cp -r <source> <dest>
```