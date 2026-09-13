---
name: ecc-continuous-learning-v2
description: Use to observe patterns and log skill improvements.
---

# Continuous Learning v2 — Pembelajaran Berbasis Observasi

## Kapan Digunakan
- Aktif secara pasif di setiap sesi task-oriented (multi-step, pakai banyak tools)
- Saat user memberikan koreksi terhadap pendekatan yang diambil
- Saat menemukan pola berulang yang bisa dijadikan skill/procedure baru
- Review mingguan untuk mengevaluasi observasi yang terkumpul

## Prinsip Kerja

1. **Observasi Pasif**: Selama sesi berjalan, catat mental (bukan log setiap kali) hal-hal berikut:
   - Koreksi user terhadap pendekatan/asumsi yang saya buat
   - Pola tugas yang berulang tapi belum ada skill-nya
   - Keputusan metodologi yang signifikan (bukan preferensi kecil)

2. **Kriteria Layak Dicatat**:
   - ✅ Koreksi berulang (bukan sekali-pakai)
   - ✅ Pola yang akan muncul lagi di sesi mendatang
   - ✅ Kesalahan tool/skill yang bisa diperbaiki di source
   - ❌ Preferensi yang sudah tertangkap di memory
   - ❌ Bug tool sesaat yang tidak terkait metodologi

3. **Log Observasi** (integrasi dengan Task Observer existing di AGENTS.md):
   - Baca `/opt/data/skill-observations/log.md`
   - Append observasi baru dengan format standar (`Status: OPEN`)
   - Di akhir sesi, ringkas observasi per skill — jangan tawarkan "apply now" berulang

4. **Review Berkala**: Cron mingguan (Senin 09:00 WIB) mereview semua observasi OPEN dan menentukan aksi (patch skill, buat skill baru, atau close sebagai tidak relevan).

## Format Observasi
```markdown
### Observation NNN: [Judul singkat]
**Status:** OPEN
**Date:** YYYY-MM-DD
**Session context:** [konteks tugas]
**Skill:** [nama skill terkait]
**Issue:** [gejala spesifik]
**Suggested improvement:** [perubahan konkret]
**Principle:** [generalisasi/pelajaran]
```

## Integrasi dengan Task Observer
Skill ini melengkapi `task-observer` yang sudah aktif via AGENTS.md — `continuous-learning-v2` berfokus pada pola perilaku/insting jangka panjang, sedangkan `task-observer` fokus pada perbaikan skill teknis spesifik per sesi.

## Pitfalls
- Jangan over-log — hanya catat yang benar-benar actionable dan berulang
- Jangan ganggu alur kerja user dengan interupsi "mau saya perbaiki sekarang?" — defer ke review mingguan
