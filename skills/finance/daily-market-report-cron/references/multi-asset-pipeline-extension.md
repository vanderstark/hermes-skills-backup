# Multi-Asset Pipeline Extension Recipe

**Context**: The original `daily-market-report-cron` script focused on IDX stocks only.
This session extended it to handle **three asset classes** in a single pipeline run:
- Indonesian stocks (^JKSE, BBCA.JK, BBRI.JK, etc.)
- US stocks (^GSPC, AAPL, MSFT, NVDA, TSLA, etc.)
- Crypto (BTC-USD, ETH-USD, SOL-USD, etc.)

## Extension Pattern (Reusable)

### 1. Abstract Symbol Lists by Asset Class

```python
# In pipeline config — NEVER a flat list
SYMBOLS_INDO = ['^JKSE', 'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 'BBNI.JK', 'UNVR.JK']
SYMBOLS_US = ['^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'AMZN', 'META']
SYMBOLS_CRYPTO = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'DOGE-USD']
DEFAULT_SYMBOLS = SYMBOLS_INDO + SYMBOLS_US + SYMBOLS_CRYPTO
```

**Why**: Future edits (add/remove symbols) are surgical. No risk of breaking other asset classes.

### 2. Isolate Output Per Asset Class

- Output file naming: `iidx_predict_<DATE>.json` → consider `iidx_predict_indo_<DATE>.json`, `iidx_predict_us_<DATE>.json`, `iidx_predict_crypto_<DATE>.json`
- Chart directories: `charts/indo/`, `charts/us/`, `charts/crypto/`
- This avoids 100+ files in one folder.

### 3. Handle Symbol Format Variance

Yahoo Finance uses different ticker formats per exchange:
- Indonesian stocks: `BBCA.JK`, `BBRI.JK` (suffix `.JK`)
- US stocks: `AAPL`, `MSFT` (no suffix)
- US indices: `^GSPC`, `^IXIC` (prefix `^`)
- Crypto: `BTC-USD`, `ETH-USD` (suffix `-USD`)

**Wrap fetch functions** so they accept raw symbol strings and normalize internally:

```python
def fetch_yahoo_ohlc(ticker: str, period: str = '15d', interval: str = '1d') -> pd.DataFrame:
    # Normalize common cases
    ticker = ticker.strip().upper()
    # Already handles .JK, ^, -USD via yfinance directly
    # But add exchange detection if needed later
    ...
```

### 4. Schedule Separately Per Domain

**Do NOT reuse the same cronjob ID** across asset classes. Each gets:
- Own cronjob ID (`iidx-predict-indo`, `iidx-predict-us`, `iidx-predict-crypto`)
- Own schedule (can overlap or stagger)
- Own Telegram delivery target if user wants separate channels

### 5. Reuse Core Analysis Logic

The `generate_sr_levels()`, `plot_candles_with_sr()`, `classify_recommendation()` functions work **unchanged** across all three asset classes because:
- Pivot/Fib math is exchange-agnostic
- Candlestick plotting is data-structure agnostic
- Recommendation rules are price-level relative (not absolute)

### 6. Session Workflow (What We Did)

```bash
# 1. Edit pipeline config (symbol arrays)
# 2. Run full pipeline: python3 src/pipeline/iidx_predict_pipeline.py
# 3. Verify output JSON + charts/
# 4. Create cronjob via Hermes for 16:30 WIB delivery
# 5. Test manual run via bash script
```

## Pitfalls Encountered

| Issue | Fix |
|-------|-----|
| yfinance returns MultiIndex columns for single ticker | `df.columns = df.columns.get_level_values(0)` |
| yfinance returns tuple on error/no-data | Check `isinstance(df, tuple)` before `.columns` access |
| `^JKSE` (IHSG) delisted from Yahoo | Use `^JKSE` as proxy; confirm data source periodically |
| Cronjob script must be in `~/.hermes/scripts/` | Copy wrapper script there, use filename only in cronjob |

## Related Files Created This Session

- `/opt/data/iidx-predict/src/pipeline/iidx_predict_pipeline.py` — extended with multi-asset symbol arrays
- `/opt/data/iidx-predict/scripts/run_pipeline.sh` — wrapper for cron
- `~/.hermes/scripts/iidx_predict_run.sh` — Hermes cronjob entry point
- 3 cronjobs: `iidx-predict-0800`, `iidx-predict-1630`, `iidx-predict-2000`

## For Future: Adding a 4th Asset Class (e.g., Forex)

1. Add `SYMBOLS_FOREX = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'USDIDR=X']`
2. Extend `DEFAULT_SYMBOLS = ... + SYMBOLS_FOREX`
3. Create `charts/forex/`, `output/forex_*.json` isolation
4. Add cronjob `iidx-predict-forex` if needed separate schedule
5. Verify yfinance supports the symbols (most forex pairs use `=X` suffix)