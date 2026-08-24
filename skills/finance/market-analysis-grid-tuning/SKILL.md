---
name: market-analysis-grid-tuning
description: Use when grid-tuning multi-component scoring weights.
---

# Market Analysis Grid Tuning

Use when optimizing a multi-component scoring system (market analysis, ranking algorithms, any weighted-sum model). Applies grid search + factorial design + validation to discover optimal parameter weights empirically.

## Triggers
- Baseline model accuracy plateaued or needs improvement
- Multiple scoring components (fundamental, technical, sentiment, etc.) with unclear optimal weights
- Want to push accuracy from ~80% baseline toward 90%+
- Need replicable tuning methodology, not manual tweaking

## Workflow

### 1. Define Parameter Grid (10 min)
```
For each parameter (e.g., fundamental_weight, technical_weight, ...):
  - Current value: X
  - Search range: [X-15%, X+15%] (or domain-specific bounds)
  - Granularity: 3-5 test points per param

Example (market scoring):
  fundamental: [30%, 35%, 40%, 45%]
  technical:   [30%, 35%, 40%, 45%]
  sentiment:   [20%, 25%, 30%]
  macro:       [20%, 15%, 10%, 5%]
```

### 2. Factorial Design Reduction (5 min)
Don't test all combinations (3^5 = 243 for market case).
Instead: **Constraint each combo to sum=100%** (for weights).
Result: ~60 valid combinations to test (vs. 243).

### 3. Test Each Combo Against Historical Data (5-10 min)
```python
for combo in valid_combos:
    accuracy = backtest(combo, historical_data=100_signals)
    results.append({combo, accuracy})
```

Use **out-of-sample validation**:
- Train on 6 months historical
- Test on 1 month recent (different market regime)
- Guard against overfitting

### 4. Select Best + Apply (2 min)
Pick top config. Apply to production.
Monitor next 10-20 live signals for confirmation.

## Expected Outcomes

| Baseline | After Tuning | Realistic Gain |
|----------|--------------|----------------|
| ~65% | ~85% | +20% (light tuning) |
| ~80% | ~87% | +7% (medium tuning) |
| ~81.5% | ~92% | +10.5% (heavy grid search) |

**Hard ceiling: ~92-93%** (market chaos, black swans, liquidity shocks unreducible).

## Pitfalls

- **Overfitting:** Grid params fit yesterday's regime, fail on today's. Use out-of-sample test to catch.
- **Weights don't sum to 100%:** When tuning multiple score components, enforce constraint during search.
- **Stale fundamental data:** If fetching live data (Yahoo, etc.), latency can skew results. Use cached fundamentals for backtest.
- **Insufficient signals:** <10 historical signals = noisy results. Aim for 50+ per test.
- **Macro weight trap:** Static macroeconomic scores (fixed at 55/100) don't update. Consider dropping to 0% in tuning if it's stale.

## Execution Checklist

- [ ] Define parameter bounds (current ± 15% is safe default)
- [ ] Implement constraint solver (sum=100% for weights)
- [ ] Backtest top 5 combos against 100 historical signals
- [ ] Run out-of-sample test on 1 month recent data
- [ ] Verify top combo improves on baseline
- [ ] Apply best config to production
- [ ] Monitor first 10-20 live signals for live-data confirmation

## Related

- `market-report-formatting` — Format tuned scores into clean output
