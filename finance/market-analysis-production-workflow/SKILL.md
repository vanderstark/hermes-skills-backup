---
name: market-analysis-production-workflow
description: Run IDX/US/Crypto analysis — use market_report_fast.py.
---

# Market Analysis Production Workflow

**Governing skill:** `daily-market-report-cron` (hub-installed, defines canonical format & rules)  
**Production script:** `/opt/data/.hermes/scripts/market_report_fast.py` (v4, no_agent, ~12s)  
**Cron schedule:** 3x/day (08:00/16:30/20:00 WIB) via cronjob tool

---

## ⚡ Critical Rule — ALWAYS USE PRODUCTION SCRIPT

When user asks for market analysis ("analisa market", "keluarkan analisa", "market hari ini"), **jalanin `market_report_fast.py` langsung**. JANGAN pakai pipeline eksperimental (`iidx-predict`) yang belum punya fitur lengkap.

> **Lesson learned (2026-08-13):** User koreksi "Lho mana area entry dan support kuat kok tidak ada" — karena saya pakai `iidx-predict` (pivot-based S/R, tanpa Entry Zone, tanpa S.KUAT touch-count) padahal script produksi sudah punya semua fitur yang diminta.

---

## ✅ Production Script Features (market_report_fast.py v4)

| Fitur | Status | Detail |
|---|---|---|
| **Entry Zone** | ✅ | `S1 × 1.01–1.02` sampai `min(S1×1.03, px×0.98)` |
| **S.KUAT / R.KUAT** | ✅ | Berdasar **touch-count** (multi-window [3,5,8] + cluster 2.5%), bukan pivot biasa |
| **TP3 Fibonacci** | ✅ | `r2 + (r2-r1)*0.618` (bukan hardcode) |
| **Cross-check CoinGecko** | ✅ | Harga crypto USD live |
| **Cross-check Indodax** | ✅ | Harga crypto IDR lokal |
| **IHSG & USD/IDR live** | ✅ | Yahoo `^JKSE` + `IDR=X` + exchangerate.host fallback |
| **Format output kanonis** | ✅ | 5 baris per aset: SL → TP1/TP2/TP3 → Entry → S.KUAT-1/2 → R.KUAT-1/2 → Harga Sekarang → RR |
| **Overbought filter** | ✅ | RSI>72 difilter dari ranking |
| **OBV trend** | ✅ | 20-bar + 5-bar (medium+short), bukan 5-bar saja |

---

## 🚫 Jangan Pakai Pipeline Eksperimental

`/opt/data/iidx-predict/` — pipeline baru (yfinance → pivot/Fib → chart → JSON)  
**Kelebihan:** modular, chart PNG, signal score -100..+100, JSON terstruktur  
**Kekurangan (belum ada):** Entry Zone, S.KUAT/R.KUAT touch-count, TP3 Fibonacci, format tabel kanonis, cross-check Indodax/IHSG terintegrasi di output

> Gunakan `iidx-predict` HANYA untuk R&D (backtesting engine, divergence scanner, pattern recognition) — bukan untuk laporan harian user.

---

## 🔧 Cron Integration Pattern

```bash
# Wrapper script di ~/.hermes/scripts/market_report_run.sh
cd /opt/data && python3 .hermes/scripts/market_report_fast.py
```

Cronjob via `cronjob` tool: `no_agent=true`, `deliver=telegram`, `model=hermes provider=custom` (pin agar tidak unpinned).

---

## 📋 Format Output Kanonis (WAJIB)

```
  {i}. {SYM} — Score {score} ({chg:+.2f}%)
     🛡️ SL: {sl}  |  🎯 TP1: {tp1}  |  TP2: {tp2}  |  TP3: {tp3}
     ✅ Entry: {e_low} – {e_high}
     🔵 S.KUAT-1: {s1}  |  🔵 S.KUAT-2: {s2}  |  🔴 R.KUAT-1: {r1}  |  🔴 R.KUAT-2: {r2}
     💰 HARGA SEKARANG: {px}  |  RR 1:{rr}
```

Urutan kolom **tidak boleh diubah**: SL, TP1, TP2, TP3, Entry, S.KUAT-1, S.KUAT-2, R.KUAT-1, R.KUAT-2, Harga Sekarang.

---

## 📌 Watchlist Composition (FIXED LIST — bukan dinamis)

Watchlist adalah **hardcoded list** di source script, BUKAN hasil scan likuiditas otomatis dari bursa. Total **27 simbol discan**, ranking Top 10/7/5 by score ditampilkan:

| Kategori | Jumlah discan | Ditampilkan |
|---|---|---|
| IDX | 10 (BBRI, BMRI, BBCA, TLKM, ICBP, ASII, UNVR, BRPT, SMGR, ADRO) | Top 10 |
| US | 10 (AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, AMD, AVGO, JPM) | Top 7 |
| Crypto | 7 (BTC, ETH, SOL, BNB, XRP, DOGE, ADA) | Top 5 |

Kalau user tanya "apakah ini scan otomatis likuiditas tertinggi?" → jawab jujur: **tidak**, ini watchlist blue-chip/big-cap tetap yang dipilih manual (mirip likuiditas tinggi tapi bukan hasil filter algoritmik). Untuk scan lebih luas lihat `references/full-market-scan-feasibility.md`.

---

## 🐛 Pitfalls (dari iterasi nyata)

1. **OBV trend jangan 5 bar** — pakai 20-bar + 5-bar
2. **Entry zone jangan "S1 sampai harga"** — terlalu lebar
3. **Filter overbought RSI>72** di scoring
4. **TP3 jangan hardcode** — pakai Fibonacci extension
5. **RR crypto sering < 1:1** (SL 5%) — wajar, laporkan apa adanya
6. **`datetime.utcnow()` deprecated** — pakai `datetime.now(timezone.utc)`
7. **Cek harga "sekarang" terakhir** — user bandingin dengan ticker live
8. **Setelah edit script, SELALU jalankan** `python3 .hermes/scripts/market_report_fast.py` untuk verifikasi
9. **Setelah pindah cron ke production script, HAPUS cron duplikat/lama** — pernah ada 3 cronjob `iidx-predict-0800/1630/2000` nganggur bersamaan dengan 3 cronjob produksi `market_report_fast.py` karena cron lama tidak dihapus saat migrasi. Selalu `cronjob(action='list')` dulu untuk cek duplikasi sebelum & sesudah menambah job baru.
10. **Full-market scan (900 saham IDX) BELUM diimplementasikan** — hanya estimasi feasibility (lihat `references/full-market-scan-feasibility.md`). Jangan klaim sudah bisa scan semua 900 saham; watchlist saat ini tetap 27 simbol fixed.

---

## 📁 Related Files

- Production script: `/opt/data/.hermes/scripts/market_report_fast.py`
- Governing skill (hub): `daily-market-report-cron` (defines canon format & rules)
- Experimental pipeline: `/opt/data/iidx-predict/` (R&D only)
- Cron wrapper: `~/.hermes/scripts/market_report_run.sh`

---

## 🔗 Cross-Reference

- See `daily-market-report-cron` skill for authoritative format specification
- See `task-observer` skill for session monitoring protocol