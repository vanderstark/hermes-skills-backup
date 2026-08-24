---
name: market-report-formatting
description: Use when formatting market reports with RAPI tables.
---

# Market Report Formatting (RAPI)

Use when generating market analysis reports. Applies RAPI (Readable, Accurate, Prioritized, Indexed) markdown table structure with HOT PICKS tier separation for immediate visual scanning.

## Triggers
- Market daily/weekly analysis with 10+ stocks/cryptos
- Need to emphasize top 3 picks over full list
- Format must work in Telegram (mobile-friendly markdown)
- User preference for **clean, not wordy** output

## Key Principles (User Preference)

**User dislikes:** Acak-acakan, hard-to-read fixed-width tables, all picks equal importance, verbose explanations.

**User wants:** RAPI format — markdown tables, HOT PICKS sorted by Risk-Reward (RR), emoji action signals, clear S/R columns.

## RAPI Table Structure

### HOT PICKS (Top 3 by RR)

```markdown
### ⭐ HOT PICKS

| # | Kode | Skor | Harga | Beli di | SL | TP1 | TP2 | RR | Action |
|---|------|------|-------|---------|----|----- |----- |----|--------|
| **1** | **ESSA** | 62 | 655 | 650–657 | 624 | 719 | 742 | **5.7** ⭐⭐ | **🔥 BUY** |
| **2** | **MDKA** | 58 | 2,900 | 2,617–2,669 | 2,514 | 2,928 | 3,097 | **5.0** ⭐⭐ | **🔥 BUY** |
| **3** | **PGEO** | 55 | 1,095 | 1,084–1,095 | 1,042 | 1,181 | 1,294 | **2.2** ⭐ | **🔥 BUY** |
```

### Star Rating Rule
- **⭐⭐** = RR ≥ 3.0 (very high reward-risk)
- **⭐** = RR ≥ 2.0 (good reward)
- (no star) = RR < 2.0 (neutral, still buyable)

### STANDARD PICKS (4–10)

```markdown
### STANDARD PICKS

| # | Kode | Skor | Harga | Entry | SL | TP1 | Sup.Kuat | Res.Kuat |
|---|------|------|-------|--------|----|----- |----------|----------|
| 4 | BBNI | 54 | 3,630 | 3,518–3,557 | 3,379 | 3,637 | 3,483 | 3,637 |
```

## Column Definitions

| Column | Format | Meaning |
|--------|--------|---------|
| # | 1-10 | Rank by composite score |
| Kode | SYMBOL or **SYMBOL** | Bold = HOT PICK |
| Skor | 0-100 | Composite score (fundamental+technical) |
| Harga | Current price (IDR/$) | Live fetched |
| Entry / Beli di | Price range | Where to buy (low–high entry) |
| SL | Stop loss price | Risk point |
| TP1 / TP | Target profit 1 | Conservative target |
| TP2 | Target profit 2 | Aggressive target |
| RR | Risk:Reward ratio | `(TP1 - Entry) / (Entry - SL)` |
| Sup.Kuat | Support (strongest) | Clustered SR level |
| Res.Kuat | Resistance (strongest) | Clustered SR level |
| Action | Text emoji | 🔥 BUY / HOLD / SELL |

## Report Header

```markdown
📊 MARKET REPORT — [Date/Time]
Sentimen: 🟢 RISK-ON / 🔴 RISK-OFF
IHSG: [price] ([change]%)
USD/IDR: [price] ([change]%)
Macro Score: [score]/100 | Sentiment Score: [score]/100
```

## Footer

```markdown
✅ Generated in [time]s (cache + live fetch + fundamentals)
```

## Pitfalls

- **No star ratings:** If RR < 2.0 for all, don't add stars arbitrarily. Keep them sparse.
- **Too many HOT PICKS:** Limit to 3 max (or 4 if RR > 3.0). Beyond that = dilutes signal.
- **Inconsistent decimals:** Use 2 decimals for USD, 0 for IDX/Crypto.
- **Missing action emoji:** Always include 🔥 for HOT PICKS, regular text for Standard.
- **Markdown rendering:** Telegram & GitHub both support these tables. Test on mobile before shipping.
- **Entry range too wide:** >3% spread = ambiguous entry. Tighten clustering or re-check SR.

## Execution Checklist

- [ ] Sort HOT PICKS by RR descending (highest first)
- [ ] Add star ratings ⭐ based on RR ≥ 2.0/3.0
- [ ] Bold symbols in HOT PICKS tier only
- [ ] Use 🔥 emoji for all HOT PICKS rows
- [ ] Include Sentimen, IHSG, USD/IDR in header
- [ ] Use markdown table format (NOT fixed-width)
- [ ] Test rendering on Telegram
- [ ] Footer: generation time + data freshness note

## Related

- `market-analysis-grid-tuning` — Tune weights to produce better HOT PICKS