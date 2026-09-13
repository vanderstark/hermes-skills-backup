---
name: claude-mem-make-plan
description: Use when planning phased implementation.
---

# Make Plan — Rencana Implementasi Bertahap

## Kapan Digunakan
- User meminta rencana implementasi untuk fitur/proyek besar
- User butuh roadmap pengembangan multi-fase
- Tugas kompleks yang perlu dipecah menjadi langkah dapat dikelola
- Sebelum eksekusi proyek besar (setup infrastruktur, migrasi sistem, dll)

## Langkah Kerja

1. **Klarifikasi Goal**: Pastikan paham target akhir dan batasan (constraints) sebelum menulis rencana.
2. **Breakdown Fase**: Bagi pekerjaan menjadi fase logis (Phase 1, 2, 3...) dengan goal spesifik per fase.
3. **Detail Task**: Setiap fase punya daftar task konkret, actionable, dan dapat diverifikasi.
4. **Dependencies**: Catat urutan ketergantungan antar fase/task.
5. **Risk & Edge Cases**: Identifikasi potensi masalah dan mitigasi.
6. **Deliverables**: Definisikan output nyata per fase (file, dokumen, deployment).

## Format Output

```markdown
# Rencana: [Nama Proyek/Fitur]

## Fase 1: [Nama Fase]
**Goal:** [1-2 kalimat tujuan fase ini]

Tasks:
- [ ] Task konkret 1
- [ ] Task konkret 2

**Deliverable:** [Output nyata]
**Dependency:** [Apa yang harus siap dulu]

## Fase 2: [Nama Fase]
...

## Risiko & Mitigasi
- Risiko: [deskripsi] → Mitigasi: [langkah]
```

## Pitfalls
- Jangan buat fase terlalu besar (>1 minggu kerja) — pecah lagi jika perlu
- Selalu sertakan cara verifikasi/testing per fase
- Untuk proyek Bos (170-server DC, drone dev, dll), pertimbangkan dependency infrastruktur eksisting
