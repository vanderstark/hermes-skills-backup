---
name: daily-market-report-cron
description: Daily IDX/US/Crypto report with compact Entry/SL/TP table.
---

# Daily Market Report (IDX + US + Crypto) — Compact Table Format

Menghasilkan laporan analisa market harian (pagi/sore/malam, cron 08:00/16:30/20:00 WIB) dengan **format tabel kompak** yang sudah disetujui user (Eko/Bos) setelah ~4 iterasi koreksi legibility. Gunakan script `market_report_fast.py` (no_agent, ~12 detik) — JANGAN generate lewat LLM manual (lama & inkonsisten).

## Trigger

- "market hari ini bagaimana", "analisa market", "keluarkan analisa lagi"
- User mengeluh hasil analisa "salah semua" / "susah membaca" → langsung cek script, bukan asal rombak format

## Kanon Format Output (WAJIB — urutan persis, 5 baris per aset)

```
  {i}. {SYM} — Score {score} ({chg:+.2f}%)
     🛡️ SL: {sl}  |  🎯 TP1: {tp1}  |  TP2: {tp2}  |  TP3: {tp3}
     ✅ Entry: {e_low} – {e_high}
     🔵 S.KUAT-1: {s1}  |  🔵 S.KUAT-2: {s2}  |  🔴 R.KUAT-1: {r1}  |  🔴 R.KUAT-2: {r2}
     💰 HARGA SEKARANG: {px}  |  RR 1:{rr}
```

**Urutan kolom yang user minta (jangan diubah):** SL, TP1, TP2, Entry, Support Kuat-1, Support Kuat-2, Resistance Kuat-1, Resistance Kuat-2, Harga Sekarang. Semua aset (IDX, US, Crypto) WAJIB format sama. Sertakan TP3 di baris SL/TP. Ikuti juga ringkasan tabel markdown per kategori (IDX top5, US top5, Crypto top5) + "Best Setup" + "Hari Ini Skip" (overbought).

**JANGAN** tampilkan blok verbose per aset (SMA20/SMA50/RSI/OBV/Weekly/alasan per baris terpisah) — user protes "susah membaca". Simpan detail itu untuk bagian insights saja.

## Level S/R: Kekuatan = JUMLAH TOUCH

- Swing high/low pakai **multiple windows [3,5,8]** + cluster tolerance **2.5%** → lebih presisi dari single window 5 + 3%.
- `cluster()` mengembalikan `(levels, touch_counts)` — touch count = ukuran cluster.
- **S1/R1 = terdekat di bawah/atas harga; S.KUAT/R.KUAT (untuk insight) = level dengan touch TERBANYAK** di bawah/atas harga.
- Support dengan touch tinggi + jarak < 8% = entry primer. Touch tinggi + jarak > 20% = magnet jangka panjang (TP3/invest).
- SL = S1 × (1 − buffer): buffer 3% saham, 5% crypto.

## Pitfalls (dari iterasi nyata)

1. **OBV trend jangan 5 bar** — pakai 20 bar + 5 bar (medium+short) untuk akurasi; OBV 5 bar sering salah arah.
2. **Entry zone jangan "S1 sampai harga"** — terlalu lebar. Entry = S1 × (1+1-2%) sampai min(S1×1.03, px×0.98); crypto buffer 2%.
3. **Filter overbought RSI>70** di scoring — saham overbought (RSI 81+) tetap masuk ranking kalau tidak difilter.
4. **TP3 jangan hardcode** — pakai Fibonacci extension: `r2 + (r2-r1)*0.618`.
5. **RR crypto sering < 1:1** (SL lebar 5%) — wajar, laporkan; jangan paksa RR ≥ 1:2 untuk crypto.
6. **`datetime.utcnow()` deprecated** — pakai `datetime.now(timezone.utc)`.
7. **Cek harga "sekarang" terakhir** — user membandingkan dengan ticker live-nya; kalau beda drastis, indikator/timestamp-nya yang salah, bukan cuma angka.
8. **Setelah edit script, SELALU jalankan** `python3 .hermes/scripts/market_report_fast.py` untuk verifikasi output — jangan klaim fix tanpa run.

## Script

`/opt/data/.hermes/scripts/market_report_fast.py` — v4, no_agent cron job (~12s). Data: Yahoo Finance (chart 1y daily + 2y weekly), CoinGecko cross-check crypto, Indodax IDR prices, IHSG & USD/IDR.

## Cron Integration

- 3 job harian (Pagi/Sore/Malam) → prompt harus self-contained 3-bagian (IDX, US, Crypto), pin `model=hermes provider=custom`.
- Setelah model/config drift, job gagal "unpinned — Skipped to prevent spend" → re-pin via `cronjob update job_id=<id> model=hermes provider=custom`.
- Baca FULL prompt dari `/opt/data/cron/jobs.json` sebelum update — jangan paste truncated.

## Bahasa & Nada

Indonesian, hormat tone, "Bos", ~3x 🙏🙏🙏 per reply. Tabel markdown rapi (bukan prose panjang).
