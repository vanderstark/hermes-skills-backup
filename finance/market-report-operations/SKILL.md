---
name: "market-report-operations"
title: "Market Report Operations"
description: "Run/fix daily IDX-US-crypto market report cronjobs."
trigger: "Market report cronjob failures, format complaints, cache rebuilds, or daily report delivery."
tags: ["market", "cronjob", "reporting", "cache", "formatting"]
version: "1.0.0"
---

# 📊 Market Report Operations

End-to-end market report management: cronjob orchestration, cache operations, dependency fixes, and RAPI formatting standards.

---

## 🔧 Critical Fixes

### Fix 1: Missing yfinance Dependency

**Error:** `ModuleNotFoundError: No module named 'yfinance'`

**Root Cause:** Virtual environment at `/opt/data/market-cache/.venv` missing packages.

**Solution:**
```bash
cd /opt/data/market-cache
source .venv/bin/activate
pip install yfinance pandas numpy requests beautifulsoup4
```

**Verify:** `python3 build_cache.py` completes without ModuleNotFoundError.

---

### Fix 2: Script Path Mismatch

**Error:** `Script not found: /opt/data/scripts/market_report_from_cache.sh`

**Root Cause:** Cronjob resolves `script:` relative to `/opt/data/scripts/`, but scripts live in `~/.hermes/scripts/`.

**Solution:**
```bash
cp ~/.hermes/scripts/market_*.sh /opt/data/scripts/
chmod +x /opt/data/scripts/market_*.sh
```

**Verify:** `ls -la /opt/data/scripts/market_*` shows both .sh files.

---

## 📊 Format Standard — USER PREFERENCE (CRITICAL)

**User complaint (2026-08-15):** "tulisannya acak acakan, saya agak susah membacanya" — raw script stdout (fixed-width columns) is unreadable on Telegram.

**Rule:** NEVER paste raw `report_from_cache.py` stdout to the user. ALWAYS reformat into Markdown tables with priority tiers.

### Structure Template

```
📊 MARKET REPORT [DAY] — [TIME] WIB

🎯 MARKET OVERVIEW
| Metric | Value | Status |
|--------|-------|--------|
| IHSG | 6,402 | ✅ +1.59% |
| USD/IDR | 17,820 | ⚠️ -0.24% |
| Sentimen | RISK-ON 🟢 | Bullish |

🇮🇩 SAHAM IDX — TOP 10
### ⭐ HOT PICKS (RR > 2.5)
| # | Kode | Skor | Harga | Entry | SL | TP1 | RR | Action |
|---|------|------|-------|-------|----|----- |-----|--------|
| 1 | **ISAT** | 52 | 2,540 | 2,156-2,199 | 2,071 | 2,667 | **6.0** | **BUY SIGNAL** |

### STANDARD PICKS
| # | Kode | Skor | Harga | Entry | SL | TP1 | Sup.Kuat | Res.Kuat |

🇺🇸 SAHAM US — TOP 10   (same structure, HOT PICKS RR > 2.0)
🪙 CRYPTO — TOP 10      (same structure, HOT PICKS RR > 1.5)

📌 SUMMARY & ACTION POINTS
### PRIORITY 1 (Highest R:R)
- **ISAT (IDX)** RR 6.0 → Entry 2,156-2,199
- **WFC (US)** RR 4.2 → Entry $81.11-$82.72
### PRIORITY 2 (Good R:R)
### PRIORITY 3 (Crypto plays)

⚠️ Risk Management
- Always use SL · Scale in, don't all-in · Monitor S/R real-time
```

### Format Rules (NON-NEGOTIABLE)

1. **Emoji section headers:** 🎯 🇮🇩 🇺🇸 🪙 📌 ⭐ ⚠️ — instant visual scanning
2. **Markdown tables ONLY** — never fixed-width/ASCII column walls
3. **Hot Picks split out first** (thresholds: IDX RR>2.5, US RR>2.0, Crypto RR>1.5)
4. **Action column** in Hot Picks (BUY SIGNAL / HOLD / CAUTION)
5. **Summary tier AFTER tables** — Priority 1/2/3 ranked, one line each
6. **No verbose prose** — the user reads tables, not paragraphs

---

## 🕐 Cronjob Schedule

| Time WIB | Job ID | Script |
|----------|--------|--------|
| **08:00** Pagi | `424a9eaa0d37` | market_report_from_cache.sh |
| **12:00** Siang | `ee88975eeb0a` | market_report_from_cache.sh |
| **15:45** Sore | `ea6cc26cc7a5` | market_report_from_cache.sh |
| **02:00** Cache nightly | `e65f96616df9` | market_cache_build.sh |
| **15:00** Cache afternoon | `a2a47181ab20` | market_cache_build.sh |
| **11:00** Cache noon | `1163ae6f2b4a` | market_cache_build.sh |

> **Schedule change (2026-08-15):** Sore report moved from 16:30→15:45; Cache-afternoon moved from 15:30→15:00. Cache builds run 45-60 min before reports so fresh parquet data is available when the report cron fires.

### Daily Timeline (WIB)

```
02:00  → Nightly cache build (full universe refresh)
08:00  → Morning report → Telegram
11:00  → Noon cache build
12:00  → Siang report → Telegram
15:00  → Afternoon cache build
15:45  → Sore report → Telegram
```

### Manual Execution

```bash
cronjob_ide action=run job_id=424a9eaa0d37   # rerun pagi
cronjob_ide action=list                       # check last_status of all
```

**Note:** After a failed cronjob is fixed, rerun it manually and reformat the output for the user — don't wait for the next scheduled tick.

---

## 💾 Cache System

**Parquet files:** `/opt/data/market-cache/cache/`
- `idx_ohlc.parquet` (IDX ~45 symbols)
- `us_ohlc.parquet` (US ~503 symbols)
- `crypto_ohlc.parquet` (Crypto ~70 symbols)

**Rebuild:**
```bash
cd /opt/data/market-cache && source .venv/bin/activate && python3 build_cache.py
```
Success looks like: `✅ Done in 117.3s — IDX 45/45, US 503/503, Crypto 70/100`

**Pitfall:** `report_from_cache.py` can exceed a 30s terminal timeout during fundamentals fetch. Use `timeout 120 python3 report_from_cache.py` or a 120s+ tool timeout.

**Pitfall:** Delisted crypto symbols (TAO, UNI, APT, PEPE, etc.) log "possibly delisted" warnings — harmless, the builder skips them. Only worry if the final saved count drops sharply.

---

## ✅ Pre-Report Checklist

- [ ] Scripts exist: `/opt/data/scripts/market_*.sh`
- [ ] Venv deps installed: `pip list | grep yfinance`
- [ ] Cache fresh: `ls -la /opt/data/market-cache/cache/*.parquet`
- [ ] All 3 sections present (IDX/US/Crypto)
- [ ] Reformatted into Markdown tables — NOT raw stdout
- [ ] Hot Picks split from Standard Picks
- [ ] Priority 1/2/3 summary + risk reminders at the end
