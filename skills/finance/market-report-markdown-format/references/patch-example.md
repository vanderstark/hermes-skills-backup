# Patch Example: print_table() Function

**File:** `/opt/data/market-cache/report_from_cache.py` (line ~352)

## Old (Fixed-Width Console)

```python
def print_table(title, rows, is_crypto=False, currency="Rp"):
    print("\n" + "=" * 120)
    print(f"   {title}")
    print("=" * 120)
    # Fixed-width columns
    if is_crypto or currency == "$":
        print(f"  {'#':<2} {'Kode':<6} {'Skor':<5} {'Harga Sekarang':<10} {'Zona Beli':<16} ...")
        print("  " + "-" * 116)
        for i, r in enumerate(rows, 1):
            print(f"  {i:<2} {sym_disp:<6} ...")  # Unreadable on mobile
```

## New (Markdown Table)

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

## Output Comparison

### Before (Unreadable on Mobile)
```
  #  Kode   Skor  Harga Sekarang Zona Beli          Stop Loss  TP1        TP2      
  ------  -----  -------------- ------------------- --------- --------- ---------  
  1  MDKA   58         2,900    2,617–     2,669    2,514    2,928    3,097     
```

### After (Telegram-Friendly)
```markdown
### ⭐ HOT PICKS

| **1** | **MDKA** | 58 | 2,900 | 2,617–2,669 | 2,514 | 2,928 | 3,097 | **3.0** ⭐⭐ | **🔥 BUY** |

### STANDARD PICKS

| 4 | BBNI | 54 | 3,630 | 3,518–3,557 | 3,379 | 3,637 | 3,483 | 3,637 |
```

✅ Mobile wrap-friendly, emoji visual scan, bold emphasis for top picks.
