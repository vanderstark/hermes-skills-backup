# Pipeline Comparison: Production vs Experimental

---

## market_report_fast.py (PRODUCTION — Use for Daily Reports)

| Aspect | Status |
|---|---|
| **Path** | `/opt/data/.hermes/scripts/market_report_fast.py` |
| **Use case** | Daily 3x cron reports (08:00/16:30/20:00 WIB) |
| **Output** | Canonical 5-line format per asset |
| **S/R Method** | Touch-count clusters (multi-window [3,5,8] + 2.5% tolerance) |
| **S.KUAT / R.KUAT** | ✅ Strongest touch-count levels |
| **Entry Zone** | ✅ `S1*1.01` to `min(S1*1.03, px*0.98)` |
| **TP3** | ✅ Fibonacci extension `r2 + (r2-r1)*0.618` |
| **Cross-check CoinGecko** | ✅ Live crypto USD |
| **Cross-check Indodax** | ✅ Live crypto IDR |
| **IHSG & USD/IDR** | ✅ Live |
| **Overbought filter** | ✅ RSI>72 |
| **OBV trend** | ✅ 20-bar + 5-bar |
| **Format** | Markdown table + emoji, Telegram-ready |
| **Runtime** | ~12s |

---

## iidx-predict (EXPERIMENTAL — R&D Only)

| Aspect | Status |
|---|---|
| **Path** | `/opt/data/iidx-predict/` |
| **Use case** | Research: backtesting, divergence scanner, pattern recognition |
| **Output** | JSON + PNG charts + signal score (-100..+100) |
| **S/R Method** | Classic pivot points + Fibonacci retracement |
| **S.KUAT / R.KUAT** | ❌ Not implemented (only pivot-based S1/S2/R1/R2) |
| **Entry Zone** | ❌ Not implemented (uses current price as entry) |
| **TP3** | ❌ Not implemented (only TP1/TP2) |
| **Cross-check CoinGecko** | ✅ Implemented in cross_check.py |
| **Cross-check Indodax** | ✅ Implemented in cross_check.py |
| **IHSG & USD/IDR** | ⚠️ Via Yahoo only (`^JKSE`, `IDR=X`) |
| **Overbought filter** | ⚠️ Signal score penalizes RSI>70 but not in ranking |
| **OBV trend** | ✅ OBV in advanced_ta.py |
| **Format** | JSON + detailed per-asset fields |
| **Runtime** | ~30-40s |

---

## When to Use Which

| User Request | Use |
|---|---|
| "analisa market", "keluarkan analisa", "market hari ini", "market report" | **market_report_fast.py** |
| "backtest", "divergence scanner", "pattern recognition", "signal score", "chart PNG" | **iidx-predict** |
| "coba bandingin hasil", "R&D", "experiment" | **iidx-predict** (but verify with market_report_fast.py first) |

---

## Key Difference: S.KUAT/R.KUAT

**Production (market_report_fast.py):**
- Swing high/low dengan multiple windows [3,5,8]
- Cluster tolerance 2.5%
- `cluster()` returns `(levels, touch_counts)`
- **S.KUAT = level dengan touch TERBANYAK di bawah harga**
- **R.KUAT = level dengan touch TERBANYAK di atas harga**

**Experimental (iidx-predict):**
- Classic pivot point formula: `(H+L+C)/3`
- S1=2P-H, R1=2P-L, S2=P-(R1-S1), R2=P+(R1-S1)
- Fibonacci retracement dari swing high/low
- Tidak ada touch-count → tidak bisa identifikasi level "kuat" vs "lemah"

> Inilah sebab user keluh "Lho mana area entry dan support kuat kok tidak ada" saat saya pakai iidx-predict.