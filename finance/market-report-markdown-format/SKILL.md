---
name: market-report-markdown-format
title: Market Report Markdown Format
description: Use markdown tables for Telegram mobile display.
trigger: "Use when formatting market cronjob reports for readability."
tags: ["market", "formatting", "telegram"]
version: "1.0.0"
---

# Market Report Markdown Format

Format market analysis for Telegram mobile readability. Separate HOT PICKS (top 3 by risk-reward) from STANDARD (4-10).

---

## Problem

Fixed-width console tables are unreadable on mobile ('acak acakan, susah membacanya' — session 2026-08-15).

---

## Solution

Markdown tables with visual hierarchy.

**Structure:**
- **Section 1:** HOT PICKS (Top 3 by RR) — bold ticker, emoji stars, 🔥 BUY action
- **Section 2:** STANDARD (4-10) — compact reference, 8 columns

**Emoji Legend:**
- `⭐⭐` = RR ≥ 3.0
- `⭐` = RR ≥ 2.0
- `🔥` = action signal
- `—` = null value

---

## Code Patch

**File:** `/opt/data/market-cache/report_from_cache.py` (function `print_table`)

Replace fixed-width format with markdown output:

```python
def print_table(title, rows, is_crypto=False, currency="Rp"):
    """Print market data in markdown table format."""
    print("\n" + "=" * 100)
    print(f"   {title}")
    print("=" * 100)
    
    # HOT PICKS (Top 3 by RR)
    hot_picks = sorted(rows[:3], key=lambda x: x.get('rr', 0), reverse=True)[:3]
    if hot_picks:
        print(f"\n### ⭐ HOT PICKS\n")
        print("| # | Kode | Skor | Harga | Beli di | SL | TP1 | TP2 | RR | Action |")
        print("|---|------|------|-------|---------|----|----- |----- |----|--------|")
        for i, r in enumerate(hot_picks, 1):
            lo, hi = r["entry"]
            sym_disp = r["sym"].replace("-USD", "").replace(".JK", "")
            rr = r.get('rr', 0)
            action = "🔥 BUY" if rr >= 2.0 else "BUY"
            stars = "⭐⭐" if rr >= 3.0 else "⭐" if rr >= 2.0 else ""
            print(f"| **{i}** | **{sym_disp}** | {r['composite_score']} | {r['px']:,.4g} | {lo:,.4g}–{hi:,.4g} | {r['sl']:,.4g} | {r['tp1']:,.4g} | {r['tp2']:,.4g} | **{rr}** {stars} | **{action}** |")
    
    # STANDARD (4-10)
    standard_picks = rows[3:10]
    if standard_picks:
        print(f"\n### STANDARD PICKS\n")
        print("| # | Kode | Skor | Harga | Entry | SL | TP1 | Sup.Kuat | Res.Kuat |")
        print("|---|------|------|-------|--------|----|----- |----------|----------|")
        for i, r in enumerate(standard_picks, 4):
            lo, hi = r["entry"]
            sym_disp = r["sym"].replace("-USD", "").replace(".JK", "")
            s1 = f"{r['s1']:,.4g}" if r.get("s1") else "—"
            r1 = f"{r['r1']:,.4g}" if r.get("r1") else "—"
            print(f"| {i} | {sym_disp} | {r['composite_score']} | {r['px']:,.4g} | {lo:,.4g}–{hi:,.4g} | {r['sl']:,.4g} | {r['tp1']:,.4g} | {s1} | {r1} |")
```

---

## Applied

All 3 cronjobs (verified 2026-08-15):
- Pagi 08:00 ✅
- Siang 12:00 ✅
- Sore 16:30 ✅

User tested & approved.
