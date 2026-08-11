---
name: indonesian-taxation
description: "Indonesian tax calc: PPh, PPN, e-Faktur \u2014 education only."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tax, pajak, indonesia, pph, ppn, akuntansi, keuangan]
    related_skills: [legal-research-education, financial-analyst, business-investment-advisor]
---

# Perpajakan Indonesia (Edukasi & Kalkulasi Umum)

Membantu penjelasan konsep, kalkulasi, dan simulasi perpajakan Indonesia
(PPh, PPN, e-Faktur, SPT) untuk keperluan edukasi, estimasi bisnis, dan
pemahaman umum. **Bukan pengganti konsultan pajak bersertifikat (Kuasa
Pajak/Konsultan Pajak resmi)** dan tidak menghasilkan dokumen pajak yang
mengikat secara hukum.

## Batasan Keras — Baca Dulu, Selalu

- **Bukan nasihat pajak resmi.** Setiap perhitungan/penjelasan harus
  ditutup dengan disclaimer: "Ini simulasi/edukasi umum, bukan nasihat
  pajak resmi — untuk kepatuhan pajak yang mengikat (SPT, sengketa pajak,
  audit), konsultasikan dengan konsultan pajak bersertifikat (memiliki
  Sertifikat Konsultan Pajak/kuasa resmi Ditjen Pajak)."
- **Tarif & aturan pajak sering berubah** (via UU HPP, PMK, PER Dirjen
  Pajak) — tarif yang dipakai di sini adalah tarif umum yang berlaku
  luas per pengetahuan terkini, tapi HARUS diverifikasi ke sumber resmi
  (pajak.go.id) untuk kasus yang akan benar-benar dilaporkan/dibayarkan,
  terutama untuk transaksi bernilai besar atau tanggal transaksi lampau/
  masa depan yang mungkin beda rezim aturan.
- **Tidak menggantikan e-Filing/e-Faktur resmi.** Bisa jelaskan
  prosedurnya, tidak bisa submit SPT/faktur pajak sungguhan atas nama
  user — itu tetap lewat portal resmi DJP (djponline.pajak.go.id) atau
  aplikasi e-Faktur resmi.
- **Objek pajak spesifik/kompleks perlu profesional** — restrukturisasi
  bisnis, sengketa pajak, tax planning agresif, transaksi lintas negara
  (transfer pricing) ada di luar cakupan skill ini.

## Kapan Skill Ini Dipakai

- User minta hitung PPN/PPh dari suatu harga/transaksi
- User tanya konsep pajak (apa itu PKP, DPP, bedanya PPh final vs tidak final)
- User minta simulasi dampak pajak terhadap harga jual/margin bisnis
- User tanya alur umum e-Faktur atau pelaporan SPT
- BUKAN untuk: mengisi/submit SPT sungguhan, memberi nasihat tax planning
  yang mengurangi kewajiban pajak secara agresif, atau menjustifikasi
  penghindaran pajak ilegal (tax evasion)

## Konsep Dasar yang Perlu Diketahui

### DPP (Dasar Pengenaan Pajak)
Nilai transaksi SEBELUM PPN — dasar perhitungan pajak. Kalau harga sudah
"termasuk PPN", DPP dihitung mundur:
```
DPP = Harga Termasuk PPN / (1 + tarif PPN)
PPN = Harga Termasuk PPN - DPP
```
Kalau harga BELUM termasuk PPN:
```
PPN = DPP x tarif PPN
Harga Termasuk PPN = DPP + PPN
```

### PPN (Pajak Pertambahan Nilai)
- Tarif umum saat ini: **11%** (naik dari 10% sejak April 2022 via UU HPP;
  sempat direncanakan naik ke 12% untuk barang mewah tertentu mulai 2025
  — verifikasi tarif berlaku saat transaksi ke pajak.go.id, terutama
  untuk kategori barang mewah vs umum yang bisa beda tarif)
- Dikenakan pada penyerahan Barang Kena Pajak (BKP)/Jasa Kena Pajak (JKP)
  oleh Pengusaha Kena Pajak (PKP)
- PKP wajib membuat **Faktur Pajak** (kini via e-Faktur) untuk tiap
  transaksi kena PPN

### PPh (Pajak Penghasilan) — Jenis yang Sering Relevan untuk Bisnis
| Jenis | Objek | Tarif Umum | Sifat |
|---|---|---|---|
| PPh Pasal 21 | Gaji/penghasilan karyawan | Progresif (5%-35%, tergantung lapisan penghasilan kena pajak) | Dipotong pemberi kerja |
| PPh Pasal 22 | Pembelian oleh bendahara pemerintah/BUMN, impor, penjualan barang mewah tertentu | Umumnya 1,5% (bervariasi per jenis transaksi) | Dipungut pihak pemungut, jadi kredit pajak |
| PPh Pasal 23 | Dividen, bunga, royalti, sewa, jasa tertentu antar wajib pajak dalam negeri | 2% atau 15% tergantung objek | Dipotong pihak pembayar |
| PPh Pasal 25 | Angsuran pajak tahun berjalan | Dihitung dari SPT tahun sebelumnya | Dibayar sendiri per bulan |
| PPh Final UMKM (PP 55/2022) | Omzet UMKM ≤ Rp4,8 miliar/tahun | 0,5% dari omzet | Final, dibayar sendiri |
| PPh Badan | Laba bersih fiskal badan usaha | 22% (umum), ada insentif untuk UMKM tertentu | Dilaporkan tahunan (SPT Tahunan Badan) |

**PENTING:** PPh Pasal 22 dan Pasal 23 adalah **pajak dipotong/dipungut
di muka** — bukan biaya final, melainkan **kredit pajak** yang nanti
diperhitungkan saat lapor SPT Tahunan (bisa mengurangi PPh terutang akhir
tahun, atau lebih bayar/kurang bayar).

### PKP (Pengusaha Kena Pajak)
Pengusaha yang wajib memungut PPN karena omzetnya melebihi batas
(umumnya Rp4,8 miliar/tahun) — vendor non-PKP tidak memungut PPN dan
tidak menerbitkan Faktur Pajak.

## Workflow Kalkulasi

### 1. Klarifikasi dulu sebelum hitung
Tanyakan/pastikan:
- Harga yang diberikan itu **sudah termasuk PPN atau belum**? (paling
  sering jadi sumber salah hitung — lihat pitfall di bawah)
- Jenis PPh apa yang relevan (22/23/final UMKM/badan)?
- Basis perhitungan PPh: dari **harga jual (DPP)** atau dari **laba**?
  (PPh Pasal 22/23 dari DPP; PPh Badan dari laba fiskal)

### 2. Hitung dengan Python (execute_code/terminal), bukan mental math
Selalu gunakan kalkulasi terprogram untuk angka yang akan dipakai user
secara resmi — hindari salah hitung manual, terutama untuk perhitungan
berlapis (DPP mundur, dikali quantity besar, dll).

### 3. Sajikan hasil dengan breakdown jelas + disclaimer
Format tabel per komponen (DPP, PPN, PPh, dll), jangan cuma angka akhir
— supaya user bisa verifikasi tiap langkah.

## Alur Umum e-Faktur & SPT (Edukasi, Bukan Eksekusi)

### e-Faktur
1. PKP mendaftar sertifikat elektronik di KPP terdaftar
2. Install aplikasi e-Faktur Desktop/Client resmi dari DJP, atau pakai
   e-Faktur Web/Host-to-Host
3. Input transaksi penjualan kena PPN → generate Faktur Pajak elektronik
   (nomor seri diambil otomatis dari sistem DJP)
4. Faktur Pajak jadi bukti pungutan PPN yang sah, dilaporkan di SPT Masa PPN

### SPT (Surat Pemberitahuan)
- **SPT Masa** — dilaporkan bulanan (PPh 21/23/25, PPN) via djponline.pajak.go.id
- **SPT Tahunan** — dilaporkan setahun sekali (PPh Orang Pribadi/Badan),
  rekonsiliasi seluruh pajak yang sudah dipotong/dipungut sepanjang tahun

Untuk submit sungguhan, arahkan user ke djponline.pajak.go.id atau
aplikasi e-Faktur resmi — skill ini tidak melakukan submission.

## Pitfalls (Kesalahan Umum yang Harus Dihindari)

- **Salah asumsi harga termasuk/belum termasuk PPN** — ini kesalahan
  paling sering. Selalu klarifikasi eksplisit ke user sebelum menghitung,
  jangan asumsikan sepihak. Kalau ambigu, tawarkan kedua skenario.
- **PPh dihitung dari harga TERMASUK PPN** — salah. PPh Pasal 22/23
  seharusnya dihitung dari **DPP** (harga sebelum PPN), bukan dari harga
  final yang sudah termasuk PPN.
- **Mengira PPh Pasal 22/23 sebagai biaya final** — salah. Itu kredit
  pajak, bukan pengurang laba permanen (walau untuk simulasi cash flow
  jangka pendek, wajar dianggap sebagai potongan sementara).
- **Tarif pajak dikutip dari ingatan tanpa verifikasi tanggal** — tarif
  PPN pernah 10% → 11% → berpotensi berubah lagi. Selalu sebutkan
  "tarif per pengetahuan terkini, verifikasi ke pajak.go.id untuk
  transaksi riil", terutama kalau user menyebut tanggal transaksi
  spesifik yang jauh dari hari ini.
- **Generalisasi PKP vs non-PKP** — jangan asumsikan vendor otomatis PKP
  kalau tidak dikonfirmasi; vendor kecil/UMKM sering non-PKP dan tidak
  memungut PPN sama sekali.

## Related Skills

- `legal-research-education` — kerangka disclaimer & batasan non-binding
  yang sama diterapkan di sini
- `financial-analyst` — untuk analisa dampak pajak terhadap valuasi/
  proyeksi keuangan yang lebih luas
- `business-investment-advisor` — untuk keputusan investasi yang
  mempertimbangkan implikasi pajak
