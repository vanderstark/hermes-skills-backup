# Feasibility: Full IDX Market Scan (900 saham)

**Status:** NOT IMPLEMENTED — hanya estimasi/benchmark, belum ada script produksi.

## Benchmark Terukur (2026-08-13)

Test `yf.download()` batch parallel (`threads=True`) untuk 30 simbol IDX:
- 30 simbol → 11.27s → ~376ms/simbol
- Ekstrapolasi 900 simbol (rate sama) → **~338 detik (±6 menit)** hanya untuk download OHLC
- Ditambah hitung indikator+S/R+score (~5ms/simbol × 900 ≈ 5 detik) + sorting + format laporan
- **Total estimasi: ±6–7 menit per eksekusi**

## Kendala Utama

1. **Rate-limit Yahoo Finance** — 900 request beruntun berisiko kena 429/block. Belum divalidasi apakah `yf.download()` batch menangani ini otomatis untuk skala 900.
2. **Margin waktu cron ketat** — 3 jadwal (08:00/16:30/20:00 WIB) hanya beda ±5 jam; 7 menit per run OK tapi tidak ada buffer kalau jaringan lambat.

## Arsitektur yang Direkomendasikan (belum dibangun)

Pola **cache + reader** (bukan live-scan tiap cron):
1. **Cron malam (mis. 02:00 WIB)** — job terpisah download & simpan seluruh 900 simbol ke file cache lokal (parquet/feather, bukan CSV — lebih kompak & cepat baca)
2. **Cron pagi/sore/malam (existing)** — baca cache lokal (instant, <10 detik), hitung indikator on-the-fly, ranking, kirim laporan Top 10

## Catatan

Estimasi di atas BELUM divalidasi dengan real full-scan 900 simbol (baru tes sampel 30). Sebelum mengklaim "sudah bisa scan semua IDX" ke user, implementasi + uji nyata full-scan wajib dilakukan dulu — jangan sajikan estimasi ini sebagai fitur yang sudah jalan.
