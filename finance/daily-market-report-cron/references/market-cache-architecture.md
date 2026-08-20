# Market Cache Architecture (Sesi Ini — August 2026)

Arsitektur baru untuk laporan market hbr/tidak blokir konsumsi token LLM:

## Build Cache Layer (`build_cache.py`)

- **Waktu**: 02:00 WIB (nightly) + 15:30 WIB (afternoon refresh)
- **Fungsi**: Download OHLC 1 tahun untuk 648 simbol
  - IDX: 45 LQ45 (via Yahoo Finance yfinance)
  - US: 503 S&P 500 (via Yahoo Finance yfinance)
  - Crypto: 70 top (via Yahoo Finance yfinance)
- **Cross-check**: CoinGecko API + Indodax API (harga IDR)
- **Indeks tambahan**: `^JKSE` (IHSG) + `USDIDR=X` (USD/IDR)
- **Output**: `cache/idx_ohlc.parquet`, `cache/us_ohlc.parquet`, `cache/crypto_ohlc.parquet`, `_meta.json`
- **Waktu eksekusi**: ~90-100 detik (butuh koneksi internet, rate-limit handling)

## Report from Cache Layer (`report_from_cache.py`)

- **Waktu**: 08:00 WIB (pagi) + 16:30 WIB (sore)
- **Fungsi**: Generate laporan dari cache (tidak butuh internet)
- **Analisis teknikal**: SMA 20/50/200, RSI 14, MACD, OBV, swing levels clustering, S/R touch-count
- **Live fetch**: IHSG/USD/IDR, CoinGecko cross-check, Indodax IDR prices (runtime)
- **Output**: Top 10 IDX / Top 10 US / Top 10 Crypto dalam tabel markdown kompak
- **Waktu generate**: ~3-5 detik (hanya baca file lokal + 4 API call ringan)
- **Format kolom**: S.KUAT 1/2, R.KUAT 1/2 (touch-count), Entry Zone, SL, TP1/TP2/TP3, RR ratio

## Cron Schedule (6 Jobs)

| Job | Jadwal WIB | Fungsi |
|---|---|---|
| market-cache-build-nightly | 02:00 | Download cache utama (malam hari) |
| market-cache-build-afternoon | 15:30 | Refresh cache sore (post-close IDX) |
| Analisa Pagi | 08:00 | Laporan pagi dari cache <6 jam |
| Analisa Sore | 16:30 | Laporan sore dari cache <1 jam (paling fresh) |
| [20:00 dihapus] | — | — |

## Hybrid Data Arsitektur

```
            +----------------------+
            |  cache/ parquet files|
            +----------+-----------+
                       |
                       v
    build_cache.py   report_from_cache.py  (3-5s)
    (90s, internet)     (cache + 4 live fetch)
                       |
                       v
            +----------+-----------+
            | Header sentimen      |
            | IHSG, USD/IDR        |
            +----------------------+
```

## Keuntungan

- Laporan siang/malam pakai data paling fresh (hanya 1 jam "basi" dari build 15:30)
- Backup kalau build malam 02:00 gagal/rate-limit
- Cepat: <5 detik vs 12 detik script monolith
- Tidak butuh koneksi internet saat generate laporan (hanya 4 API call ringan)
- Output lengkap: S.KUAT 1/2 & R.KUAT 1/2 (touch-count clustering, 2.5% tol)

## Reference

- `/opt/data/market-cache/build_cache.py` — downloader cache
- `/opt/data/market-cache/report_from_cache.py` — generator laporan dari cache (sudah hybrid live fetch)
- `/opt/data/market-cache/scripts/` — wrapper shell scripts