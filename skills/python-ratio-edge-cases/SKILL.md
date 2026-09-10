---
name: python-ratio-edge-cases
description: Use when Python divides ratios involving market prices.
---

# Python Ratio & Division Edge Cases

Use when writing Python code that divides by values derived from market prices, financial data, or any numeric dataset that may contain zeros or near-zero values. Covers ZeroDivisionError in clustering, SR computation, and percentage calculations.

## Triggers
- `ZeroDivisionError: float division by zero` in clustering/pivots
- SR (support/resistance) grouping with zero-price tokens (stablecoins)
- Percentage change calculations on flat prices
- Any `x / y` where `y` comes from user/market data

## The Pattern

### WRONG (ZeroDivisionError)
```python
def cluster(levels, tol_pct=0.025):
    levels = sorted(levels)
    groups = [[levels[0]]]
    for lv in levels[1:]:
        if abs(lv - groups[-1][-1]) / groups[-1][-1] <= tol_pct:  # BUG: groups[-1][-1] = 0
            groups[-1].append(lv)
        else:
            groups.append([lv])
```

### CORRECT
```python
def cluster(levels, tol_pct=0.025):
    levels = sorted(levels)
    groups = [[levels[0]]]
    for lv in levels[1:]:
        prev_lvl = groups[-1][-1]
        if prev_lvl == 0:
            groups.append([lv])
            continue
        if abs(lv - prev_lvl) / abs(prev_lvl) <= tol_pct:
            groups[-1].append(lv)
        else:
            groups.append([lv])
```

## Key Rules

1. **Guard `prev == 0`** before any division involving data-derived values
2. **Use `abs(prev_lvl)`** — negative prices can appear in some financial contexts (oil futures)
3. **Check after `append` not before** — the first element in a group can be zero
4. **Consider zero as a separate cluster** — don't merge 0 with a non-zero group

## Common Hit Points in Market Analysis

| Location | Bug Trigger | Fix |
|----------|-------------|-----|
| SR clustering (`cluster()`) | Stablecoin at $0.9999 vs $1.0000 | Guard `prev == 0` |
| % change calc (`pct = (new-old)/old`) | Old price = 0 (IPO, delisting) | Guard `old == 0` |
| RSI normalization | All flat prices → denominator = 0 | Return 50 (neutral) |
| Volatility ratio | Single data point → std = 0 | Return 0 (no vol) |
| Fibonacci retracement | ATH = 0 (new listing) | Skip SR calc |

## Related

- `market-analysis-grid-tuning` — Tuning SR tolerance parameter
- `market-report-formatting` — Displaying SR levels in reports