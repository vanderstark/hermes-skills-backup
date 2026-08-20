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

### Real-Time Harga Top-N (NEW — Sesi Ini)
Ditambahkan fetch harga **real-time** untuk Top-N (bukan hanya sentimen header):
```python
import concurrent.futures
def fetch_live_price(sym):
    """Ambil harga close terbaru dari Yahoo 5d chart untuk 1 simbol."""
    d = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=1d")
    if not d or not d.get("chart", {}).get("result"):
        return None, None
    q = d["chart"]["result"][0]["indicators"]["quote"][0]
    closes = [x for x in q["close"] if x is not None]
    if len(closes) < 2: return None, None
    return round(closes[-1], 4), round(closes[-2], 4)

# Ambil harga live secara paralel untuk Top-N per kategori (max_workers=10)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_live_price, r["sym"]): i for i, r in enumerate(top_list)}
    for fut in concurrent.futures.as_completed(futures):
        i = futures[fut]
        live_px, live_prev = fut.result()
        if live_px and top_list[i]["px"] > 0:
            top_list[i]["px"] = live_px
            if live_prev:
                top_list[i]["chg"] = round((live_px/live_prev - 1)*100, 2)
```
**Catatan**: Kolom **S.KUAT/R.KUAT/Entry/SL/TP** tetap dari cache (indikator teknikal berbasis histori 1 tahun, tidak perlu real-time). Hanya **Harga** & **% perubahan** yang di-override live.

**Bukti kerja**: test menunjukkan harga berbeda dari cache (ZEC $492.5→$485.7, XMR $403→$401.2, SOL $76.23→$75.46). Total waktu: ~8.4 detik (vs 3.5 detik tanpa live fetch).

## Cron Job Failure Investigation & Debugging Workflow (Sesi Agustus 2026)

### Gejala Failure
- `cronjob list` menunjukkan `last_status: error` (atau `status: failed`)
- `last_delivery_error: null` → error terjadi di **agent execution** (script/tool), bukan delivery channel
- `last_run_at: 2026-08-15T08:00:27` → job ada history, tapi crashed

### Diagnosis Checklist (Berurutan)

1. **Check cronjob list**
   ```bash
   cronjob(action='list')  # Lihat job_id, last_status, script name
   ```

2. **Isolate: Run script manual**
   ```bash
   cd /opt/data/market-cache
   source .venv/bin/activate
   python3 report_from_cache.py 2>&1 | head -50
   ```
   Jika manual sukses (output normal) → error hanya transient (rate-limit/time). Cron akan succeed next run.

3. **Common Cause: Missing Python Dependencies** ⚠️
   - Error: `ModuleNotFoundError: No module named 'yfinance'`
   - Reason: Virtual environment `.venv` exists tapi dependencies hilang (fresh clone, env corruption, migration)
   - **Fix**:
     ```bash
     cd /opt/data/market-cache && source .venv/bin/activate
     pip install yfinance pandas numpy beautifulsoup4 requests
     python3 report_from_cache.py  # Test manual
     ```
   - After fix: Cron job next run akan pakai dependency fresh.

4. **Jika manual gagal juga → debug lebih dalam**
   - Check venv path: `which python3` (harus dalam `.venv/bin/`)
   - Check import: `python3 -c "import yfinance; print(yfinance.__version__)"`
   - Cek koneksi: `curl -s 'https://query1.finance.yahoo.com/v8/finance/chart/BBRI.JK' | head -20`

### Solusi (Sesuai Error Type)

| Error | Solusi |
|-------|--------|
| `ModuleNotFoundError: yfinance` | `pip install yfinance pandas numpy` (dalam `.venv`) |
| `IndentationError` atau syntax | Edit script, `python3 -c "import ast; ast.parse(open('file.py').read())"` verify |
| Timeout (>180s) | Naikkan cronjob timeout via `cronjob update` atau edit script timeout |
| Rate-limit 429 | Transient, cron retry next run. Tambah `time.sleep(0.5)` antar request jika sering |
| No data / empty output | Cek cache files exist: `ls -lh /opt/data/market-cache/cache/*.parquet` |

### Best Practice: Keep `.venv` Pinned
Setelah fix dependency sekali, dokumentasi di session atau memory untuk future migration:
- `requirements.txt`: `yfinance==1.6.0`, `pandas==3.0.5`, dll
- Atau: `pip freeze > requirements.txt` → `pip install -r requirements.txt` di env baru

## Pitfalls (dari iterasi nyata)

1. **OBV trend jangan 5 bar** — pakai 20 bar + 5 bar (medium+short) untuk akurasi; OBV 5 bar sering salah arah.
2. **Entry zone jangan "S1 sampai harga"** — terlalu lebar. Entry = S1 × (1+1-2%) sampai min(S1×1.03, px×0.98); crypto buffer 2%.
3. **Filter overbought RSI>70** di scoring — saham overbought (RSI 81+) tetap masuk ranking kalau tidak difilter.
4. **TP3 jangan hardcode** — pakai Fibonacci extension: `r2 + (r2-r1)*0.618`.
5. **RR crypto sering < 1:1** (SL lebar 5%) — wajar, laporkan; jangan paksa RR ≥ 1:2 untuk crypto.
6. **`datetime.utcnow()` deprecated** — pakai `datetime.now(timezone.utc)`.
7. **Cek harga "sekarang" terakhir** — user membandingkan dengan ticker live-nya; kalau beda drastis, indikator/timestamp-nya yang salah, bukan cuma angka.
8. **Setelah edit script, SELALU jalankan** `python3 .hermes/scripts/market_report_fast.py` untuk verifikasi output — jangan klaim fix tanpa run.

## Sistem Cache & Generator Laporan (Arsitektur Baru)

Sesi ini membangun sistem cache dan generator laporan baru sebagai alternatif/modular terhadap script `market_report_fast.py` monolith:

### `build_cache.py` — Downloader Cache Malam
- Jalankan via cron `02:00 WIB` (job: `market-cache-build-nightly`)
- Download OHLC 1 tahun untuk 648 simbol (45 LQ45 IDX + 503 S&P500 US + 70 crypto top)
- Disimpan ke `market-cache/cache/` sebagai file parquet
- Butuh ~90-100 detik, butuh koneksi internet
- Output: `idx_ohlc.parquet`, `us_ohlc.parquet`, `crypto_ohlc.parquet` + `_meta.json`

### `report_from_cache.py` — Generator Laporan Cepat
- Jalankan via cron `08:00/16:30 WIB` (job: `Analisa Pagi/Sore`)
- Baca file parquet dari cache (tidak butuh internet)
- Generate Top 10 IDX / Top 10 US / Top 10 Crypto dalam 3-5 detik
- Output format: tabel markdown kompak dengan Entry Zone, S.Kuat (touch-count), SL, TP1/TP2/TP3, RR
- Script: `~/.hermes/scripts/market_report_from_cache.sh`

### Alur Data Baru
- **02:00 WIB** → `market_cache_build.sh` → refresh cache (data fresh pre-market)
- **08:00 WIB** → `market_report_from_cache.sh` → laporan pagi dari cache <6 jam
- **15:30 WIB** → `market_cache_build.sh` → refresh cache sore (data post-close IDX)
- **16:30 WIB** → `market_report_from_cache.sh` → laporan sore dari cache <1 jam (data paling fresh)

### Keuntungan
- Laporan siang/malam pakai data **paling fresh** (hanya 1 jam "basi" dari build 15:30)
- Backup kalau build malam 02:00 gagal/rate-limit
- Cepat: <5 detik vs 12 detik script monolith

## Composite Score (NEW — Sesi Ini)\n\n### Metodologi: Fundamental 30% + Teknikal 30% + Sentimen 20% + Makro 20%\n\n```python\n# Score breakdown per aset\ncomposite = round(fundamental_score * 0.30 + technical_score * 0.30 + sentiment_score * 0.20 + macro_score * 0.20)\n\n# Contoh output\n# ESSA — Composite 61 (T:82 F:50 S:50 M:55)\n# AWK — Composite 61 (T:83 F:50 S:50 M:55)\n```\n\n### Fundamental Score (`score_fundamental`) — 30% weight\nFetch PER, PB, market cap dari Yahoo Finance `quoteSummary` API:\n```python\ndef score_fundamental(fund):\n    score = 50\n    pe = fund.get(\"pe\")\n    pb = fund.get(\"pb\")\n    mkt_cap = fund.get(\"mkt_cap\")\n    if pe is not None:\n        if pe < 10: score += 20\n        elif pe < 15: score += 10\n        elif pe < 20: score += 0\n        elif pe < 30: score -= 10\n        else: score -= 20\n    if pb is not None:\n        if pb < 1: score += 10\n        elif pb < 2: score += 5\n        elif pb < 3: score += 0\n        else: score -= 10\n    if mkt_cap is not None and mkt_cap > 1_000_000_000: score += 5\n    return max(0, min(100, score))\n```\n\n### Parallel Fundamental Fetch untuk IDX + US (NEW)\n\nUntuk IDX (45 simbol `.JK`) dan US (502 simbol), fetch fundamental paralel via Yahoo `quoteSummary` endpoint:\n```python\n# IDX: tambahkan .JK suffix\nidx_yf_symbols = [s.replace(\".JK\", \"\") for s in idx_symbols]\nwith concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:\n    futs = {ex.submit(fetch_summary, s + \".JK\"): s for s in idx_yf_symbols}\n    for fut in concurrent.futures.as_completed(futs):\n        sym_key = futs[fut]\n        data = fut.result()\n        if data: fund_scores[sym_key] = score_fundamental(data)\n\n# US: pakai ticker asli (misalnya AWK, FERG — tidak perlu modifikasi)\nus_yf_symbols = list(set(us_df[\"symbol\"].tolist()))\nwith concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:\n    futs = {ex.submit(fetch_summary, s): s for s in us_yf_symbols}\n    for fut in concurrent.futures.as_completed(futs):\n        sym_key = futs[fut]\n        data = fut.result()\n        if data: fund_scores[sym_key] = score_fundamental(data)\n```\n\n`fetch_summary()` — Yahoo `quoteSummary` API:\n```python\ndef fetch_summary(sym):\n    url = f\"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=summaryDetail,defaultKeyStatistics,price\"\n    d = fetch_json(url)\n    res = d[\"quoteSummary\"][\"result\"][0]\n    summary = res.get(\"summaryDetail\", {})\n    stats = res.get(\"defaultKeyStatistics\", {})\n    price_data = res.get(\"price\", {}).get(\"result\", [{}])[0]\n    return {\n        \"px\": summary.get(\"previousClose\", {}).get(\"raw\") or price_data.get(\"regularMarketPrice\", {}).get(\"raw\"),\n        \"pe\": summary.get(\"trailingPE\", {}).get(\"raw\"),\n        \"pb\": stats.get(\"priceToBook\", {}).get(\"raw\"),\n        \"mkt_cap\": price_data.get(\"marketCap\", {}).get(\"raw\"),\n        \"beta\": stats.get(\"beta\", {}).get(\"raw\"),\n    }\n```\n\n### Runtime Impact\n- Fundamental fetch (557 saham paralel): +15–20 detik\n- **Total runtime laporan: ~20 detik** (vs 3.5 detik tanpa fundamental)\n- Tidak persisten antar cron run — fetch ulang tiap kali\n\n## Sentiment Score (NEW — Binary, Tidak Netral)\n\nSentiment sekarang **binary** — selalu RISK-ON atau RISK-OFF, tidak ada zona NEUTRAL lagi. User minta \"sentimen tolong di on kan\".\n```python\nihsg_chg = round((ihsg_px/ihsg_prev - 1)*100, 2)\nif ihsg_chg > 0: sent = \"🟢 RISK-ON\"\nelif ihsg_chg < 0: sent = \"🔴 RISK-OFF\"\n```\n\n### Pitfall: IndentationError setelah patch\nSaat mengubah logika sentimen (NEUTRAL → binary), patch pertama menghasilkan `IndentationError: unexpected indent` karena blok `if/elif` salah indent. **SELALU gunakan `python3 -c \"import ast; ast.parse(open('file.py').read())\"` untuk verifikasi syntax sebelum kirim ke user.**\n\n## Hybrid Live Fetch (Baru — Sesi Ini)
`report_from_cache.py` sekarang hybrid:
- **Analisis teknikal berat** (scan 600+ simbol SMA/RSI/MACD/OBV/SR) → dari **cache parquet** (~3 detik)
- **Live fetch saat runtime**:
  - `���� Fetching live data...` → IHSG & USD/IDR dari Yahoo
  - `���� Fetching CoinGecko cross-check...` → validasi harga crypto
  - `�������� Fetching Indodax IDR prices...` → harga crypto Rupiah
  - `���� Fetching IHSG & USD/IDR...` → sentimen header
  - `���� Fetching REAL-TIME harga untuk Top-N (30 simbol)...` → **NEW**: parallel fetch live price untuk Top 10 IDX + Top 10 US + Top 10 Crypto via Yahoo Finance chart endpoint (5d, 1d), override kolom `Harga` & `%chg` dengan data real-time
- Output header: Sentimen (RISK-ON/OFF **binary — no NEUTRAL**), IHSG, USD/IDR
- Crypto cross-check merge ke output tabel (diff CoinGecko + Indodax IDR)

### Format Output Baru — S.KUAT 1/2 & R.KUAT 1/2
```markdown
  1. ESSA — Score 82 (-7.04%)
     SL: 624  TP1: 719  TP2: 742  TP3: 756
     Entry: 650 – 657
     S.KUAT 1: 644  |  S.KUAT 2: 599
     R.KUAT 1: 719  |  R.KUAT 2: 742
     Harga: 660  |  RR 1:2.7
```
Kolom: S1, S2 (support terdekat & kedua di bawah), R1, R2 (resistance terdekat & kedua di atas). Jika tidak ada level kedua → tampil `-`.

### Format Tabel Final (Disetujui User — Kolom Fix)

Setelah beberapa iterasi (list bullet → markdown table → detail card), user akhirnya minta **tabel markdown rapi** dengan kolom urutan PERSIS ini (jangan diubah lagi tanpa diminta):

```
Kode | Harga Sekarang | Zona Beli | Stop Loss | TP1 | TP2 | Support Kuat 1 | Support Kuat 2 | Resisten Kuat 1 | Resisten Kuat 2 | Risk:Reward
```

- **Tidak perlu TP3** di tabel ringkas ini (beda dari kanon lama yang include TP3) — TP3 boleh tetap dihitung internal tapi tidak wajib ditampilkan jika user minta versi ringkas ini.
- Skor (composite atau technical) taruh di kolom awal sebelum Kode, bukan di akhir.
- Style breakdown seperti "Composite 61 (T:82 F:50 S:50 M:55)" itu OK untuk versi verbose/text-plain (output cron mentah), tapi saat presentasi ke user di chat, **sederhanakan ke tabel markdown murni** — jangan tampilkan breakdown huruf T/F/S/M inline, cukup kolom skor tunggal kalau user minta "mudah dibaca".
- User pernah bilang "kurang enak" pada format dengan emoji bullet + collapsible `<details>` — ternyata yang diinginkan justru tabel markdown polos, bukan card/emoji-heavy. Kalau ragu, default ke **tabel markdown polos** dulu, baru tambah dekorasi kalau diminta.

### Reference Files
- `/opt/data/market-cache/build_cache.py` — downloader cache
- `/opt/data/market-cache/report_from_cache.py` — generator laporan dari cache (sudah hybrid live fetch)
- `/opt/data/market-cache/scripts/` — wrapper shell scripts

Jika user minta kembali ke script monolith `market_report_fast.py`, gunakan cron lama (08:00/16:30/20:00 pakai `market_report_fast.py`) atau manual `python3 .hermes/scripts/market_report_fast.py` dari `/opt/data`.

## Script

`/opt/data/.hermes/scripts/market_report_fast.py` — v4, no_agent cron job (~12s). Data: Yahoo Finance (chart 1y daily + 2y weekly), CoinGecko cross-check crypto, Indodax IDR prices, IHSG & USD/IDR.

`~/.hermes/scripts/market_report_from_cache.sh` — generator laporan dari cache baru, ~3-5 detik.

`/opt/data/.hermes/scripts/market_report_fast.py` — v4, no_agent cron job (~12s). Data: Yahoo Finance (chart 1y daily + 2y weekly), CoinGecko cross-check crypto, Indodax IDR prices, IHSG & USD/IDR.

## Propagated Change Protocol (New — Agustus 2026)

**Signal:** User said _"tolong di terapkan dan update ke cronjob yang lain"_ after approving a format fix for one report.

This is the canonical pattern when user approves a change for **ONE** delivery channel (e.g., noon report) and asks to apply it **_everywhere_**:

1. **`Identify all affected cronjobs`** (via `cronjob list`) — usually 3 market reports + 3 cache builds + daily/weekly review.
2. **`Patch the shared script`** (e.g., `report_from_cache.py`, `build_cache.py`) — NOT per-cronjob config.
3. **`Sync to all script locations`**:
   - `/opt/data/market-cache/*.py` → `/opt/data/scripts/*.py` → `~/.hermes/scripts/*.sh` wrappers
4. **`Run every cronjob manually`** (via `cronjob action='run'`) — verify ✅ `last_status: ok` for each.
5. **`Commit changes to GitHub backup repo`** (`vanderstark/hermes-config-schedule`) with descriptive message.
6. **`Update this skill's SKILL.md`** with: new data window, new format, pitfalls encountered.
7. **Verify next scheduled run** (trigger manually at same WIB time or wait for cron).

### When to Apply This Protocol
- ✅ Format change (tabling, columns ordering, emoji style)
- ✅ Data window change (1y → 15y)
- ✅ Bug fix that affects output (e.g., ZeroDivisionError in cluster())
- ❌ One-off schedule tweaks (those are per-job edits only)

### Pitfall: Do NOT fix only one job
If you patch `report_from_cache.py` but only test via one cronjob `run`, the next day the OTHER two cronjobs (pagi/sore) still emit the old format until they pick up the same script file. Always re-run ALL report cronjobs after a shared-script change.

### Example: 15-Year Data Window Propagation (Case Study)
**User request:** _"diubah menjadi jangan 1 tahun tapi menjadi 15 tahun"_

1. Patched `build_cache.py`: `period="1y"` → `period="15y"` (3 call sites: idx, us, crypto)
2. Patched `report_from_cache.py`:
   - Added `📊 Data periode: **15 tahun plenus**` header line
   - Fixed `cluster()` ZeroDivisionError: `groups[-1][-1]==0` → use `prev_lvl = groups[-1][-1]; if prev_lvl == 0: groups.append([lv]); continue`
3. Synced scripts to `/opt/data/scripts/` and `~/.hermes/scripts/`
4. Ran all 3 cache builds + 3 report cronjobs → all ✅ ok
5. Committed to GitHub: _"Update: 15-year data window + cluster() fix + RAPI report format"_
6. THIS SKILL entry documents the change permanently.

## Building a Separate/Custom Pipeline (Different Codebase)

If the user asks for a standalone pipeline outside `market_report_fast.py` (e.g. a new project dir with its own S/R modules, chart generator, multi-asset symbol lists for IDX+US+Crypto), see `references/multi-asset-pipeline-extension.md` for the abstraction pattern: separate symbol arrays per asset class, isolated output dirs, ticker-format handling (`.JK`/`^`/`-USD`), and per-asset-class cronjob scheduling. Cronjob scripts must live in `~/.hermes/scripts/` (filename only, not absolute path) — creating one under a project dir and copying it there is the working pattern.

## Cron Integration

Jadwal final (7 jobs, per Agustus 2026 — 3x laporan + 3x build cache + 1x review):

| Job | WIB | Fungsi |
|---|---|---|
| market-cache-build-nightly | 02:00 | Build cache full universe |
| Analisa Pagi | 08:00 | Laporan dari cache malam |
| market-cache-build-noon | 11:00 | Refresh cache siang |
| Analisa Siang | 12:00 | Laporan dari cache siang (fresh) |
| market-cache-build-afternoon | 15:30 | Refresh cache sore |
| Analisa Sore | 16:30 | Laporan dari cache sore (paling fresh) |
| weekly-skill-review-task-observer | Senin 09:00 | Review skill (task-observer) |

- Tambah slot laporan baru = tambah build-cache SEBELUM waktu laporan (jangan laporan pakai cache basi >4 jam).
- Cronjob scripts hidup di `~/.hermes/scripts/` (filename only, bukan absolute path).
- Setelah model/config drift, job gagal "unpinned — Skipped to prevent spend" → re-pin via `cronjob update job_id=<id> model=hermes provider=custom`.
- Baca FULL prompt dari `/opt/data/cron/jobs.json` sebelum update — jangan paste truncated.

### Pitfall: cronjob tool API — tidak ada action 'patch'
`cronjob(action='patch', ...)` **tidak ada** — error "Unknown cron action 'patch'". Gunakan `action='update'` untuk edit job existing. Untuk job baru dengan `no_agent=true` + `script=...`, `action='create'` tetap **wajib** isi `prompt` (walau sebenarnya diabaikan saat `no_agent=true`) — kalau kosong, error "create requires either prompt or at least one skill". Isi prompt singkat placeholder seperti `"Run market_cache_build.sh"` untuk no_agent job yang delivery-nya `local` (tidak ada output ke chat).

## Format Tabel Final (Disetujui User — Kolom Fix)

Setelah beberapa iterasi (list bullet → markdown table → detail card), user akhirnya minta **tabel markdown rapi** dengan kolom urutan PERSIS ini (jangan diubah lagi tanpa diminta):

```
Kode | Harga Sekarang | Zona Beli | Stop Loss | TP1 | TP2 | Support Kuat 1 | Support Kuat 2 | Resisten Kuat 1 | Resisten Kuat 2 | Risk:Reward
```

- **Tidak perlu TP3** di tabel ringkas ini (beda dari kanon lama yang include TP3) — TP3 boleh tetap dihitung internal tapi tidak wajib ditampilkan jika user minta versi ringkas ini.
- Skor (composite atau technical) taruh di kolom awal sebelum Kode, bukan di akhir.
- Style breakdown seperti "Composite 61 (T:82 F:50 S:50 M:55)" itu OK untuk versi verbose/text-plain (output cron mentah), tapi saat presentasi ke user di chat, **sederhanakan ke tabel markdown murni** — jangan tampilkan breakdown huruf T/F/S/M inline, cukup kolom skor tunggal kalau user minta "mudah dibaca".
- User pernah bilang "kurang enak" pada format dengan emoji bullet + collapsible `<details>` — ternyata yang diinginkan justru tabel markdown polos, bukan card/emoji-heavy. Kalau ragu, default ke **tabel markdown polos** dulu, baru tambah dekorasi kalau diminta.

## Bahasa & Nada

Indonesian, hormat tone, "Bos", ~3x 🙏🙏🙏 per reply. Tabel markdown rapi (bukan prose panjang).
