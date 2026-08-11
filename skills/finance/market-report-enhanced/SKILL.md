---
name: market-report-enhanced
description: Laporan market IDX/US/Crypto dengan Entry/SL/TP & support.
---

# Market Report Enhanced — Entry/SL/TP1-3 + Support Terkuat

Laporan analisis market harian lengkap: **Saham IDX + Saham US + Crypto**, masing-masing dilengkapi **level Entry, SL, TP1, TP2, TP3** dan **deteksi support terkuat** dari data swing high/low 1 tahun.

## Kapan skill ini digunakan

- User minta "analisis market" / "market hari ini" / "market report"
- Cron job analisis harian (pagi/sore/malam)
- User minta Entry/SL/TP atau support terkuat untuk saham/crypto

## Metodologi

### 1. Data Collection (Yahoo Finance + CoinGecko + Indodax)

**Step 1 — Cookie & Crumb (Yahoo)**
```bash
cd /tmp
curl -s -c yc.txt "https://fc.yahoo.com" -H "User-Agent: Mozilla/5.0" -o /dev/null
CRUMB=$(curl -s -b yc.txt "https://query2.finance.yahoo.com/v1/test/getcrumb" -H "User-Agent: Mozilla/5.0")
```

**Step 2 — IDX Universe (screener, loop offset 0,250,500,750)**
```bash
curl -s -b /tmp/yc.txt \
  "https://query2.finance.yahoo.com/v1/finance/screener?crumb=$CRUMB&lang=en-US&region=US&formatted=true" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/json" \
  -d '{"size":250,"offset":0,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","query":{"operator":"AND","operands":[{"operator":"EQ","operands":["region","id"]}]}}'
```

**Step 3 — Batch Quote Yahoo (max 100 simbol/call) — tambah fundamentals**
```bash
# Quote dasar + fundamentals ringkas
curl -s -b /tmp/yc.txt \
  "https://query2.finance.yahoo.com/v7/finance/quote?symbols=BBRI.JK,BMRI.JK,BBCA.JK,TLKM.JK,ICBP.JK,ASII.JK,UNVR.JK,BRPT.JK,SMGR.JK,ADRO.JK,AAPL,MSFT,NVDA,GOOGL,AMZN,META,TSLA,AMD,AVGO,JPM,BTC-USD,ETH-USD,SOL-USD,BNB-USD,XRP-USD,DOGE-USD&fields=symbol,shortName,regularMarketPrice,regularMarketChangePercent,fiftyTwoWeekLow,fiftyTwoWeekHigh,fiftyDayAverage,twoHundredDayAverage,regularMarketVolume,averageDailyVolume3Month,trailingPE,priceToBook,dividendYield,marketCap,averageAnalystRating&crumb=$CRUMB" \
  -H "User-Agent: Mozilla/5.0"
```

**Step 3b — Yahoo quoteSummary Fundamentals (per saham terpilih)**
```bash
# Panggil untuk setiap saham terpilih (bisa batch 10-20 simbol)
curl -s -b /tmp/yc.txt \
  "https://query2.finance.yahoo.com/v10/finance/quoteSummary/BBRI.JK?modules=defaultKeyStatistics,financialData,summaryDetail,calendarEvents&crumb=$CRUMB" \
  -H "User-Agent: Mozilla/5.0"
# Field kunci: forwardPE, pegRatio, profitMargins, returnOnEquity, revenueGrowth, earningsGrowth, dividendRate, payoutRatio, targetMeanPrice, numberOfAnalystOpinions
```

**Step 4 — Chart 1 Tahun + Weekly (per saham terpilih)**
```bash
# Daily 1y untuk indikator teknis
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/BBRI.JK?range=1y&interval=1d" -H "User-Agent: Mozilla/5.0"
# Weekly 2y untuk konfirmasi tren besar
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/BBRI.JK?range=2y&interval=1wk" -H "User-Agent: Mozilla/5.0"
```

**Step 4b — CoinGecko Cross-check Crypto (gratis, no API key)**
```bash
# Top 20 koin by market cap
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h,7d" \
  -H "User-Agent: Mozilla/5.0"
# Bandingkan harga Yahoo vs CoinGecko — flag kalau beda >2%, ambil rata-rata
```

**Step 4c — Indodax API Crypto IDR (harga & volume lokal asli)**
```bash
# Semua pair IDR
curl -s "https://indodax.com/api/tickers" -H "User-Agent: Mozilla/5.0"
# Pair spesifik
curl -s "https://indodax.com/api/btc_idr/ticker" -H "User-Agent: Mozilla/5.0"
# Field kunci: last, high, low, vol_idr, vol_btc, buy, sell, server_time
```

### 2. Indikator Teknis (Python stdlib only)

```python
def sma(c, n):
    return sum(c[-n:]) / n if len(c) >= n else None

def rsi(c, n=14):
    if len(c) < n + 1:
        return None
    gains = losses = 0
    for i in range(1, n + 1):
        ch = c[-n-1+i] - c[-n+i-1]
        if ch >= 0:
            gains += ch
        else:
            losses -= ch
    if losses == 0:
        return 100
    rs = (gains / n) / (losses / n)
    return 100 - 100 / (1 + rs)

def macd(c):
    if len(c) < 26:
        return None
    e12 = [c[0]]; e26 = [c[0]]
    for p in c[1:]:
        e12.append(e12[-1] + 0.1818 * (p - e12[-1]))
        e26.append(e26[-1] + 0.074 * (p - e26[-1]))
    return e12[-1] - e26[-1]
```

**Tambah — On-Balance Volume (OBV)** — konfirmasi volume mengiringi pergerakan harga:
```python
def obv(closes, volumes):
    """OBV: volume kumulatif — naik saat close naik, turun saat close turun.
    Tren OBV searah harga = penguatan sehat; divergen (harga naik, OBV flat/turun) = sinyal lemah."""
    if not closes or len(closes) != len(volumes):
        return None
    value = 0.0; series = [0.0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]: value += volumes[i]
        elif closes[i] < closes[i-1]: value -= volumes[i]
        series.append(value)
    return series
```
Interpretasi OBV:
- **OBV naik & harga naik** → kuat (volume mengkonfirmasi breakout) — ✅ layak masuk
- **OBV flat/turun tapi harga naik** → divergensi bearish — ⚠️ jangan kejar, waspadai reversal
- **OBV naik tapi harga turun** → akumulasi (bullish), tunggu konfirmasi

**Tambahan — Multi-Timeframe (Weekly) untuk konfirmasi tren besar:**
```bash
# Ambil chart weekly 2y SEKALIGUS dengan daily. E.g.:
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/BBRI.JK?range=2y&interval=1wk" -H "User-Agent: Mozilla/5.0"
# Hitung SMA20/50 weekly + RSI14 weekly untuk memastikan setup daily sejalan dgn tren mingguan.
```
- **Harga daily > SMA20/50/200 DAN weekly > SMA20/50/200** → setup terkuat (trend align)
- **Daily bullish tapi weekly bearish** → rebound jangka pendek saja, risiko tinggi

**Fundamentals (dari quoteSummary) — tambahkan ke skor & catatan:**
- `forwardPE` (valuasi forward), `pegRatio` (harga-pertumbuhan), `profitMargins`, `returnOnEquity`, `revenueGrowth`, `earningsGrowth` (pertumbuhan QoQ)
- `targetMeanPrice` + `numberOfAnalystOpinions` → konsensus analis
- Prefer saham dengan **ROE tinggi + revenue/earnings growth positif + margin sehat** — bukan cuma murah di P/E
- Tambahkan bobot valuasi/th Fundamental ke skor ranking jika data tersedia

### 3. Deteksi Support/Resistance Terkuat (v4 — CRUCIAL)

Gunakan **swing high/low clustering** dari data 1 tahun dengan **multi-window** (3/5/8) & **touch count**:

```python
def swing_levels(highs, lows, window=5):
    """Find swing highs/lows with multiple window sizes for robust detection."""
    if len(highs) < 2*window+1: return [], []
    piv_l, piv_h = [], []
    for w in [3, 5, 8]:
        if len(highs) < 2*w+1: continue
        for i in range(w, len(lows)-w):
            if lows[i] == min(lows[i-w:i+w+1]): piv_l.append(lows[i])
        for i in range(w, len(highs)-w):
            if highs[i] == max(highs[i-w:i+w+1]): piv_h.append(highs[i])
    return list(set(piv_l)), list(set(piv_h))

def cluster(levels, tol_pct=0.025):
    """Cluster nearby levels with 2.5% tolerance. Returns (levels, touch_count)."""
    if not levels: return [], []
    levels = sorted(levels)
    groups = [[levels[0]]]
    for lv in levels[1:]:
        if abs(lv - groups[-1][-1]) / groups[-1][-1] <= tol_pct:
            groups[-1].append(lv)
        else:
            groups.append([lv])
    scored = sorted(groups, key=lambda g: -len(g))
    return [round(sum(g)/len(g), 2) for g in scored], [len(g) for g in scored]

def strongest_support(levels, touches, px):
    """Find strongest support below current price (most touches)."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        if lvl < px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt

def strongest_resistance(levels, touches, px):
    """Find strongest resistance above current price (most touches)."""
    best_lvl, best_cnt = None, 0
    for lvl, cnt in zip(levels, touches):
        if lvl > px and cnt > best_cnt:
            best_lvl, best_cnt = lvl, cnt
    return best_lvl, best_cnt
```

**Menentukan S.KUAT-1, S.KUAT-2, R.KUAT-1, R.KUAT-2:**
- **S.KUAT-1** = support **terdekat di bawah** harga saat ini (nearest support)
- **S.KUAT-2** = support **kedua** terdekat di bawah
- **R.KUAT-1** = resistance **terdekat di atas** harga saat ini (nearest resistance)
- **R.KUAT-2** = resistance **kedua** terdekat di atas
- **Strongest Support** = support dengan touch count tertinggi di bawah harga (bisa beda dari S.KUAT-1)
- **Strongest Resistance** = resistance dengan touch count tertinggi di atas harga (bisa beda dari R.KUAT-1)

### 4. Ranking & Pemilihan

**Skor komponen (0-100):**
| Faktor | Bobot | Kondisi Skor Tinggi |
|--------|-------|---------------------|
| vs SMA20 | 15% | Harga > SMA20 |
| vs SMA50 | 15% | Harga > SMA50 |
| vs SMA200 | 10% | Harga > SMA200 |
| RSI14 | 10% | 40-65 (momentum sehat) |
| MACD | 5% | Positif / naik |
| OBV | 15% | OBV naik + harga naik (konfirmasi volume) |
| Weekly trend | 10% | Weekly SMA20/50 > 0 (tren besar searah) |
| 52w Low gap | 5% | < 30% |
| Volume | 5% | > avg volume 3M |
| Fundamentals | 5% | ROE tinggi, revenue/earnings growth positif |

**Catatan scoring:**
- OBV & weekly trend nilainya **baru ditambahkan** — berperan besar karena konfirmasi volume & tren besar.
- Kalau data fundamental/OBV tidak tersedia untuk satu saham, bobot komponen itu dibagi rata ke komponen yang ada (jangan buang).
- **Ambil 10 terbaik IDX, 5-7 US, 3-5 crypto.**

### 5. Level Entry/SL/TP1/TP2/TP3

| Level | Metode |
|-------|--------|
| **Entry** | Zona antara S1 dan harga saat ini |
| **SL** | Di bawah S1 — **WAJIB** |
| **TP1** | R1 (resistance terdekat) |
| **TP2** | R2 (resistance kedua) |
| **TP3** | R2 berikutnya / 52-week high |

**Risk/reward minimum 1:2** — jika RR < 1:2, skip atau tunggu pullback.

### 6. Format Laporan (v4)

Setiap saham/crypto ditampilkan dalam **5 baris kompak** dengan urutan tetap:
1. **Nama — Score (%change)**
2. **🛡️ SL** | **🎯 TP1** | **TP2** | **TP3**
3. **✅ Entry** (zona)
4. **🔵 S.KUAT-1** | **🔵 S.KUAT-2** | **🔴 R.KUAT-1** | **🔴 R.KUAT-2**
5. **💰 HARGA SEKARANG** | **RR**

```
📊 REPORT MARKET — [Tanggal WIB]
Sentimen: [risk-on/risk-off/mixed]
IHSG: [harga] ([%]) | USD/IDR: [kurs]

## 🇮🇩 SAHAM IDX — TOP 10
  1. [TICKER] — Score [N] ([+%])
     🛡️ SL: [harga]  |  🎯 TP1: [harga]  |  TP2: [harga]  |  TP3: [harga]
     ✅ Entry: [zona rendah] – [zona tinggi]
     🔵 S.KUAT-1: [harga]  |  🔵 S.KUAT-2: [harga]  |  🔴 R.KUAT-1: [harga]  |  🔴 R.KUAT-2: [harga]
     💰 HARGA SEKARANG: [harga]  |  RR 1:[N]

## 🇺🇸 SAHAM US — TOP 7
  [format sama]

## 🪙 CRYPTO — TOP 5
  [format sama — harga USD rata-rata Yahoo+CoinGecko + Indodax IDR]

💡 Kiat: [insight singkat — best setup, overbought warnings, OBV/weekly-confirmed picks]
⚠️ Disclaimer: Analisa teknikal, BUKAN nasihat investasi.
```

*Catatan Crypto:*
- Harga USD memakai **rata-rata Yahoo + CoinGecko**; flag ⚠️ jika beda >2%.
- **Harga IDR & volume lokal dari Indodax** (bukan konversi).
- Volume IDR Indodax yang tinggi = permintaan pasar lokal kuat.

## Pitfalls Penting

1. **RSI14 = 100** → pastikan data chart ≥ 20 bar, gunakan `range=1y` untuk SMA200 akurat.
2. **Entry = zona, bukan harga tunggal** misal "7.000-7.150".
3. **SL selalu di bawah support kuat**.
4. **Hindari saham RSI > 80** — sudah overbought.
5. **Crypto lebih volatile** — lebarkan SL/TP ±5-10% vs ±3-5% saham.
6. **Selalu sertakan disclaimer** — bukan nasihat investasi personal.
7. **Front-load reminder di cron prompt** — "LAPORAN HARUS 3 BAGIAN: IDX, US, Crypto!"
8. **Yahoo quoteSummary butuh cookie+crumb** — tanpa cookie akan dapat `Unauthorized` / `Invalid Crumb`. Selalu gunakan cookie dari Step 1.
9. **Num field fundamentals = dict `{"raw": ..., "fmt": ...}`** — selalu ambil `.raw`, bukan dict-nya.
10. **CoinGecko beda dengan Yahoo >2%** — bukan error, tapi likuiditas/listing; laporkan 🔄 & tampilkan rata-rata, jangan merah satu-satunya.
11. **Indodax ticker** — respons: `{"tickers": {"btc_idr": {...}}}` — akses `data["tickers"]["btc_idr"]`, bukan langsung `data["btc_idr"]`.
12. **OBV butuh pasangan close+volume** — pastikan panjang array sama; jika tidak, injak `None`.
13. **Weekly chart `1wk` butuh range `2y`** — jangan pakai `range=1y&interval=1wk` (data tidak cukup untuk hitung SMA20/50 weekly yang stabil).

## Cron Job Integration

1. Prompt dimulai: *"Laporan ini MUST mencakup TIGA bagian: IDX, US, Crypto."*
2. **Pin model/provider**: `cronjob action=update job_id=<id> model=hermes provider=custom`
3. Setelah update, **baca kembali** `/opt/data/cron/jobs.json` untuk verifikasi.
4. Jangan paste truncated prompt — gunakan `read_file` dulu, lalu `write_file` ke `/tmp/scratch`, baru paste.