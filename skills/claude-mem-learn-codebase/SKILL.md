---
name: claude-mem-learn-codebase
description: Use when priming/onboarding into an unfamiliar codebase.
---

# Learn Codebase — Priming Pemahaman Codebase

## Kapan Digunakan
- Onboarding ke proyek/repo baru
- Sebelum refactor besar pada sistem yang belum familiar
- User minta "pahami codebase ini" atau "analisa struktur project"
- Debug masalah di codebase yang belum pernah disentuh

## Langkah Kerja

1. **Struktur Direktori**: Gunakan `search_files(target='files')` untuk memetakan struktur folder utama.
2. **Entry Points**: Identifikasi file utama (main.py, index.js, app.py, dll) dan config (package.json, requirements.txt, composer.json).
3. **Baca Source Files**: Baca file-file kunci secara berurutan — mulai dari entry point, lalu ikuti import/dependency graph.
4. **Identifikasi Pola**: Catat pola arsitektur (MVC, layered, microservices), konvensi penamaan, dan struktur database.
5. **Dokumentasi Existing**: Cek README, AGENTS.md, CONTRIBUTING.md untuk konteks tambahan.
6. **Ringkasan**: Buat ringkasan arsitektur — komponen utama, alur data, titik integrasi eksternal.

## Format Output

```markdown
# Codebase Summary: [Nama Proyek]

## Stack
- Bahasa/Framework: ...
- Database: ...
- Deployment: ...

## Struktur Utama
- `/src` — ...
- `/config` — ...

## Alur Kerja Utama
1. Entry point → ...
2. ...

## Konvensi & Pola
- ...

## Area Perlu Perhatian
- [Technical debt/TODO/known issues]
```

## Pitfalls
- Jangan hanya baca 1-2 file lalu langsung asumsikan paham keseluruhan arsitektur
- Untuk proyek besar, prioritaskan file yang sering diubah (git log) atau entry point utama
- Selalu verifikasi asumsi dengan menjalankan test/build jika memungkinkan
