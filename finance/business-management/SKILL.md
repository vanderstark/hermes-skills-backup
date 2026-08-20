---
name: business-management
description: "Business & org management: planning, teams, ops frameworks."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [management, manajemen, sdm, operasional, strategi, project-management]
    related_skills: [indonesian-accounting-psak, indonesian-taxation, business-investment-advisor, market-research-reports]
---

# Manajemen Bisnis & Organisasi

Membantu perencanaan strategis, manajemen operasional, manajemen SDM
dasar, dan manajemen proyek menggunakan kerangka kerja manajemen yang
umum dipakai — untuk membantu pengambilan keputusan bisnis/organisasi,
bukan pengganti konsultan manajemen bersertifikat untuk keputusan
strategis besar yang mengikat.

## Batasan

- **Bukan keputusan final** — kerangka kerja di sini membantu
  terstruktur berpikir, bukan menggantikan judgment pemilik bisnis/
  pimpinan organisasi yang tahu konteks penuh (budaya organisasi,
  hubungan personal, batasan riil).
- **Tidak menggantikan HR/hukum ketenagakerjaan untuk keputusan SDM
  berisiko hukum** — PHK, sengketa karyawan, kontrak kerja mengikat,
  tetap perlu konsultasi HR profesional/hukum ketenagakerjaan (lihat
  skill `legal-research-education` untuk edukasi dasar UU
  Ketenagakerjaan, tapi keputusan personel spesifik butuh profesional).
- **Kerangka kerja adalah alat bantu, bukan resep otomatis** — hasil
  analisis (SWOT, RACI, dll) harus divalidasi dengan konteks nyata
  organisasi user, bukan diterima mentah-mentah sebagai kebenaran.

## Kapan Skill Ini Dipakai

- User minta bantu susun rencana strategis/rencana kerja organisasi
- User minta analisis SWOT, RACI matrix, atau framework manajemen lain
- User tanya soal manajemen tim, delegasi tugas, atau struktur organisasi
- User minta bantu manajemen proyek (timeline, milestone, resource planning)
- User tanya konsep manajemen umum (kepemimpinan, pengambilan keputusan,
  manajemen perubahan)

## Kerangka Kerja Perencanaan Strategis

### SWOT Analysis
```
Strengths (Kekuatan)         Weaknesses (Kelemahan)
- Internal, positif           - Internal, negatif

Opportunities (Peluang)      Threats (Ancaman)
- Eksternal, positif          - Eksternal, negatif
```
Gunakan untuk assessment posisi organisasi sebelum menyusun strategi.

### SMART Goals
Tujuan/target harus:
- **S**pecific — jelas, tidak ambigu
- **M**easurable — bisa diukur (angka/indikator jelas)
- **A**chievable — realistis dicapai dengan sumber daya yang ada
- **R**elevant — sejalan dengan tujuan besar organisasi
- **T**ime-bound — ada batas waktu jelas

### Balanced Scorecard (untuk organisasi yang lebih matang)
4 perspektif yang diukur simultan:
1. **Finansial** — profitabilitas, revenue growth
2. **Pelanggan** — kepuasan, retensi, market share
3. **Proses Internal** — efisiensi operasional, kualitas
4. **Pembelajaran & Pertumbuhan** — kapabilitas SDM, inovasi, budaya

### Porter's Five Forces (analisis kompetitif)
1. Ancaman pendatang baru
2. Daya tawar pemasok
3. Daya tawar pembeli
4. Ancaman produk substitusi
5. Persaingan antar kompetitor eksisting

## Manajemen Operasional

### RACI Matrix (kejelasan peran dalam proyek/proses)
| Peran | Arti |
|---|---|
| **R**esponsible | Yang mengerjakan tugas |
| **A**ccountable | Yang bertanggung jawab atas hasil akhir (biasanya 1 orang) |
| **C**onsulted | Yang dimintai masukan sebelum keputusan |
| **I**nformed | Yang diberi tahu setelah keputusan/hasil |

### PDCA Cycle (perbaikan berkelanjutan)
```
Plan → Do → Check → Act → (kembali ke Plan)
```
Cocok untuk continuous improvement proses operasional.

### Analisis Root Cause — 5 Whys
Tanyakan "kenapa" berulang (biasanya 5x) untuk sampai ke akar masalah,
bukan berhenti di gejala permukaan.

## Manajemen Proyek

### Elemen Dasar Rencana Proyek
1. **Scope** — apa yang dikerjakan (dan yang TIDAK dikerjakan)
2. **Timeline** — milestone & deadline
3. **Resource** — SDM, budget, tools yang dibutuhkan
4. **Risk** — risiko yang mungkin muncul & mitigasinya
5. **Stakeholder** — siapa yang berkepentingan & perlu update

### Kanban vs Scrum vs Waterfall (kapan pakai yang mana)
| Metode | Cocok untuk |
|---|---|
| **Waterfall** | Proyek dengan requirement jelas & jarang berubah (misal: instalasi infrastruktur fisik seperti Zabbix/LibreNMS yang sudah dibuat) |
| **Kanban** | Alur kerja berkelanjutan, prioritas sering berubah (operasional harian, support ticket) |
| **Scrum** | Proyek pengembangan iteratif dengan tim tetap (software development, iterasi produk) |

## Manajemen SDM Dasar (Edukasi, Bukan Keputusan Personel)

### Siklus Manajemen Kinerja
1. Penetapan target (idealnya SMART) di awal periode
2. Coaching/feedback berkala (bukan cuma review tahunan)
3. Evaluasi kinerja periodik
4. Pengembangan (training, promosi, atau perbaikan)

### Model Kepemimpinan Situasional (Hersey-Blanchard)
Gaya kepemimpinan disesuaikan level kematangan/kompetensi anggota tim:
- **Telling** — untuk anggota baru/kompetensi rendah, arahan jelas
- **Selling** — motivasi & arahan seimbang
- **Participating** — kolaboratif, anggota sudah kompeten tapi butuh dukungan
- **Delegating** — anggota sudah kompeten & mandiri, minim pengawasan

## Workflow Bantu Perencanaan

### 1. Klarifikasi konteks dulu
Tanyakan: skala organisasi (kecil/menengah/besar), sektor (swasta/
pemerintah/nirlaba), horison waktu (jangka pendek/menengah/panjang),
dan masalah spesifik yang ingin dipecahkan.

### 2. Pilih kerangka kerja yang sesuai
Jangan paksakan 1 framework untuk semua kasus — SWOT untuk assessment
posisi, RACI untuk kejelasan peran proyek, Balanced Scorecard untuk
organisasi matang dengan multi-perspektif KPI, dst.

### 3. Sajikan hasil terstruktur, tapi tandai sebagai draft
Hasil analisis (SWOT, dll) disajikan sebagai starting point diskusi,
bukan keputusan final — dorong user untuk validasi dengan tim/data riil.

### 4. Untuk data kuantitatif (KPI, budget, dll), gunakan Python
Sama seperti skill akuntansi/pajak — hitung dengan `terminal`/
`execute_code`, jangan mental math untuk angka yang akan dipakai
sungguhan.

## Pitfalls

- **Framework generik tanpa konteks** — SWOT/RACI/dll hasilnya cuma
  sekuat data yang dimasukkan; jangan isi placeholder generik tanpa
  input spesifik dari user.
- **Mencampur keputusan strategis dengan keputusan personel berisiko
  hukum** — kalau pertanyaan sudah menyentuh PHK/sengketa karyawan
  spesifik, arahkan ke `legal-research-education` + rekomendasi
  konsultasi HR/hukum profesional, jangan beri "keputusan" langsung.
- **Overselling framework sebagai jaminan sukses** — semua kerangka
  kerja manajemen adalah alat bantu berpikir terstruktur, bukan formula
  ajaib; selalu framing sebagai "starting point untuk didiskusikan".

## Related Skills

- `indonesian-accounting-psak` — untuk data finansial pendukung keputusan manajemen
- `indonesian-taxation` — implikasi pajak dari keputusan bisnis
- `business-investment-advisor` — evaluasi investasi/capex spesifik
- `market-research-reports` — riset pasar untuk mendukung strategi
- `legal-research-education` — untuk aspek hukum ketenagakerjaan/kontrak
