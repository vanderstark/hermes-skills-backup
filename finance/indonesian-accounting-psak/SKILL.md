---
name: indonesian-accounting-psak
description: "Indonesian accounting (PSAK): journal, laporan keuangan."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [akuntansi, accounting, psak, pembukuan, laporan-keuangan, indonesia]
    related_skills: [indonesian-taxation, financial-analyst, legal-research-education]
---

# Akuntansi Indonesia (PSAK) — Edukasi & Penyusunan Dasar

Membantu penjurnalan, penyusunan laporan keuangan dasar, dan penjelasan
konsep akuntansi berdasarkan **PSAK (Pernyataan Standar Akuntansi
Keuangan)** yang berlaku di Indonesia — termasuk PSAK umum dan **SAK EMKM**
(untuk UMKM) sebagai standar yang lebih sederhana.

**Bukan pengganti akuntan publik bersertifikat (CPA/CA) atau auditor**
untuk laporan keuangan yang akan diaudit, dilaporkan ke OJK/BEI, atau
dipakai untuk keperluan legal/perpajakan resmi bernilai tinggi.

## Batasan Keras — Baca Dulu, Selalu

- **Bukan opini akuntan resmi.** Laporan keuangan yang disusun di sini
  adalah draft kerja/edukasi — untuk laporan yang akan diaudit, dipakai
  investor, bank, atau pelaporan resmi (OJK, pajak), harus direview
  akuntan publik/auditor bersertifikat.
- **PSAK terus diperbarui** (adopsi konvergensi IFRS berkelanjutan oleh
  DSAK-IAI) — rujukan standar spesifik (nomor PSAK, tanggal efektif)
  harus diverifikasi ke situs resmi IAI (iaiglobal.or.id) untuk
  penerapan yang mengikat, terutama untuk entitas dengan akuntabilitas
  publik yang tunduk PSAK penuh (bukan SAK EMKM/SAK ETAP).
- **Pilih standar yang tepat sesuai jenis entitas:**
  - **SAK EMKM** — untuk UMKM (Usaha Mikro Kecil Menengah), paling sederhana
  - **SAK ETAP** — untuk entitas tanpa akuntabilitas publik signifikan
  - **PSAK penuh** — untuk entitas dengan akuntabilitas publik (Tbk, BUMN, dll)

  Salah pilih standar = laporan keuangan tidak sesuai kebutuhan entitas.
  Selalu klarifikasi jenis/skala entitas dulu.
- **Tidak menggantikan software akuntansi resmi** untuk pembukuan
  produksi berkelanjutan (Accurate, Jurnal.id, Zahir, SAP, dll) — skill
  ini untuk penjurnalan ad-hoc, edukasi, dan draft laporan, bukan sistem
  pembukuan harian perusahaan.

## Kapan Skill Ini Dipakai

- User minta bantu membuat jurnal (debit/kredit) untuk transaksi tertentu
- User minta susun draft Laporan Laba Rugi, Neraca, atau Laporan Arus Kas
- User tanya konsep akuntansi (akrual vs kas, aset lancar vs tetap,
  depresiasi, dll)
- User minta hitung rasio keuangan dasar dari laporan yang ada
- BUKAN untuk: menyusun laporan keuangan yang akan diaudit/dilaporkan
  resmi tanpa review akuntan, atau manipulasi angka untuk menyembunyikan
  kondisi keuangan sebenarnya (window dressing/fraud)

## Konsep Dasar Akuntansi

### Persamaan Akuntansi Dasar
```
Aset = Liabilitas + Ekuitas
```

### Prinsip Debit-Kredit
| Akun | Bertambah (Debit/Kredit) | Berkurang |
|---|---|---|
| Aset | Debit | Kredit |
| Liabilitas (Kewajiban) | Kredit | Debit |
| Ekuitas (Modal) | Kredit | Debit |
| Pendapatan | Kredit | Debit |
| Beban | Debit | Kredit |

### Basis Akuntansi
- **Basis Akrual** — transaksi dicatat saat terjadi, bukan saat kas
  berpindah tangan (standar PSAK umum mensyaratkan ini)
- **Basis Kas** — dicatat saat kas benar-benar diterima/dikeluarkan
  (lebih sederhana, kadang dipakai UMKM kecil meski SAK EMKM tetap
  mendorong akrual untuk item material)

### Siklus Akuntansi (Ringkas)
1. Identifikasi & analisis transaksi (bukti transaksi: nota, invoice, dll)
2. Jurnal Umum (mencatat debit-kredit tiap transaksi kronologis)
3. Posting ke Buku Besar (per akun)
4. Neraca Saldo (trial balance) — cek total debit = total kredit
5. Jurnal Penyesuaian (akrual, depresiasi, dll di akhir periode)
6. Neraca Saldo Setelah Penyesuaian
7. Laporan Keuangan (Laba Rugi, Neraca, Arus Kas, Perubahan Ekuitas)
8. Jurnal Penutup (menutup akun nominal ke akun Laba Ditahan)

## Laporan Keuangan Utama (PSAK 1 — Penyajian Laporan Keuangan)

Set lengkap laporan keuangan (PSAK 1) terdiri dari:
1. **Laporan Posisi Keuangan (Neraca)** — Aset, Liabilitas, Ekuitas per tanggal tertentu
2. **Laporan Laba Rugi dan Penghasilan Komprehensif Lain** — kinerja per periode
3. **Laporan Perubahan Ekuitas** — mutasi modal/laba ditahan per periode
4. **Laporan Arus Kas** — aktivitas operasi, investasi, pendanaan
5. **Catatan atas Laporan Keuangan (CaLK)** — kebijakan akuntansi & rincian pos

### Format Ringkas Laporan Laba Rugi
```
Pendapatan                          xxx
Beban Pokok Penjualan (HPP)        (xxx)
────────────────────────────────────────
Laba Kotor                          xxx
Beban Operasional                  (xxx)
────────────────────────────────────────
Laba Usaha (EBIT)                   xxx
Beban/Pendapatan Non-Operasional    xxx
────────────────────────────────────────
Laba Sebelum Pajak (EBT)            xxx
Beban Pajak Penghasilan            (xxx)
────────────────────────────────────────
Laba Bersih                         xxx
```

### Format Ringkas Neraca
```
ASET                          LIABILITAS & EKUITAS
Aset Lancar          xxx      Liabilitas Jangka Pendek    xxx
  Kas                xxx      Liabilitas Jangka Panjang   xxx
  Piutang            xxx      ─────────────────────────────
  Persediaan         xxx      Total Liabilitas            xxx
Aset Tetap            xxx      Ekuitas                     xxx
  (dikurangi                  ─────────────────────────────
   akumulasi depresiasi)      Total Liabilitas + Ekuitas   xxx
─────────────────────
Total Aset             xxx     (harus SAMA dengan Total Liabilitas+Ekuitas)
```

## Beberapa PSAK Kunci yang Sering Relevan

| PSAK | Topik | Catatan |
|---|---|---|
| PSAK 1 | Penyajian Laporan Keuangan | Struktur dasar laporan |
| PSAK 2 | Laporan Arus Kas | Metode langsung vs tidak langsung |
| PSAK 14 | Persediaan | Metode FIFO, rata-rata tertimbang (LIFO tidak diizinkan) |
| PSAK 16 | Aset Tetap | Depresiasi, model biaya vs revaluasi |
| PSAK 23 | Pendapatan | Kini banyak mengacu PSAK 72 (adopsi IFRS 15) untuk kontrak pelanggan |
| PSAK 46 | Pajak Penghasilan | Pajak tangguhan (deferred tax) |
| PSAK 72 | Pendapatan dari Kontrak dengan Pelanggan | 5-step model (adopsi IFRS 15) |
| PSAK 73 | Sewa | Hampir semua sewa dicatat sebagai aset & liabilitas (adopsi IFRS 16) |

*(Verifikasi nomor & isi PSAK terkini ke iaiglobal.or.id — DSAK-IAI
terus menerbitkan amandemen/PSAK baru.)*

## Workflow Bantu Penjurnalan

### 1. Identifikasi transaksi
Tanyakan: jenis transaksi (penjualan/pembelian/pembayaran/penerimaan/
penyesuaian), tanggal, nominal, akun yang terlibat.

### 2. Tentukan akun debit & kredit
Terapkan aturan debit-kredit di atas. Contoh pola umum:

**Penjualan tunai:**
```
(D) Kas                      xxx
    (K) Pendapatan Penjualan     xxx
```

**Penjualan kredit (piutang):**
```
(D) Piutang Usaha             xxx
    (K) Pendapatan Penjualan     xxx
```

**Pembelian barang dagang tunai:**
```
(D) Persediaan                xxx
    (K) Kas                      xxx
```

**Pembayaran beban (misal sewa):**
```
(D) Beban Sewa                xxx
    (K) Kas                      xxx
```

**Depresiasi aset tetap (jurnal penyesuaian):**
```
(D) Beban Depresiasi          xxx
    (K) Akumulasi Depresiasi     xxx
```

### 3. Cek keseimbangan
Total debit HARUS SAMA DENGAN total kredit di tiap entri jurnal — kalau
tidak seimbang, ada kesalahan yang harus ditelusuri sebelum lanjut.

### 4. Gunakan Python untuk laporan multi-transaksi
Untuk menyusun laporan dari banyak transaksi, gunakan `terminal`/
`execute_code` dengan struktur data (list/dict) per transaksi, jangan
hitung manual satu-satu untuk data besar — risiko salah hitung tinggi.

## Rasio Keuangan Dasar (untuk analisis cepat)

| Rasio | Formula | Interpretasi |
|---|---|---|
| Current Ratio | Aset Lancar / Liabilitas Lancar | Likuiditas jangka pendek (>1 = sehat) |
| Debt to Equity Ratio | Total Liabilitas / Total Ekuitas | Struktur modal, leverage |
| Net Profit Margin | Laba Bersih / Pendapatan | Efisiensi profitabilitas |
| Return on Assets (ROA) | Laba Bersih / Total Aset | Efisiensi penggunaan aset |
| Return on Equity (ROE) | Laba Bersih / Total Ekuitas | Return bagi pemilik modal |

Untuk analisis rasio lebih mendalam & valuasi, lihat skill
`financial-analyst`.

## Pitfalls

- **Salah pilih standar** (PSAK penuh vs SAK ETAP vs SAK EMKM) — dampak
  besar ke kompleksitas pengungkapan yang wajib. Selalu tanya skala
  entitas dulu.
- **Lupa jurnal penyesuaian** — banyak entri terlewat kalau langsung
  loncat dari transaksi harian ke laporan tanpa proses penyesuaian akhir
  periode (akrual, depresiasi, persediaan akhir, dll).
- **Tidak cek keseimbangan neraca** — Total Aset harus SELALU sama
  dengan Total Liabilitas + Ekuitas; kalau tidak, ada kesalahan
  penjurnalan yang harus ditelusuri sebelum menyajikan hasil ke user.
- **Mencampur basis kas & akrual** tanpa disadari — konsisten pakai satu
  basis sepanjang periode pelaporan.
- **Mengklaim laporan "sudah sesuai PSAK"** tanpa qualifier — selalu
  sebut ini "draft berdasarkan prinsip PSAK umum", karena kepatuhan
  PSAK penuh butuh pengungkapan CaLK detail yang di luar cakupan
  simulasi cepat.

## Related Skills

- `indonesian-taxation` — pajak yang terkait dengan pos akuntansi (PPh
  Badan dari laba fiskal, PPN dari transaksi penjualan/pembelian)
- `financial-analyst` — analisis rasio & valuasi lebih lanjut dari
  laporan yang sudah disusun
- `legal-research-education` — kerangka disclaimer non-binding yang sama
