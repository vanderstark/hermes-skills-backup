# Pulling live stock data without a paid API (Yahoo Finance)

When the user asks to analyze a specific ticker (e.g. "analyze BBRI stock")
and no paid market-data MCP (Octagon, etc.) is connected, Yahoo Finance's
unauthenticated/lightly-authenticated endpoints are enough for a full
technical + fundamental writeup. Works for most exchanges, including
Jakarta (`.JK` suffix), by ticker symbol.

## 1. Price history (no auth needed)

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/<TICKER>?range=1y&interval=1d" \
  -H "User-Agent: Mozilla/5.0"
```

Returns `chart.result[0]` with `meta` (current price, 52w high/low, market
cap, previous close) and `indicators.quote[0]` arrays: `close`, `high`,
`low`, `volume`, aligned to the `timestamp` array. Use `range=1y` for a full
year of daily closes — enough for SMA20/50/200, RSI14, MACD, and 1M/3M/1Y
% change calculations in pure Python (no numpy/pandas needed, see below).

## 2. Fundamentals (quoteSummary — needs a crumb)

The `quoteSummary` endpoint returns `Unauthorized: Invalid Crumb` without a
session cookie + crumb token. Fetch both first, then pass the crumb:

```bash
# 1. Get a session cookie
curl -s -c /tmp/yc.txt "https://fc.yahoo.com" -H "User-Agent: Mozilla/5.0" -o /dev/null

# 2. Get a crumb using that cookie
CRUMB=$(curl -s -b /tmp/yc.txt "https://query2.finance.yahoo.com/v1/test/getcrumb" -H "User-Agent: Mozilla/5.0")

# 3. Query fundamentals with cookie + crumb
curl -s -b /tmp/yc.txt \
  "https://query2.finance.yahoo.com/v10/finance/quoteSummary/<TICKER>?modules=defaultKeyStatistics,financialData,summaryDetail,price,earningsTrend,balanceSheetHistory,incomeStatementHistory&crumb=$CRUMB" \
  -H "User-Agent: Mozilla/5.0"
```

Useful modules: `financialData` (ROE, ROA, margins, analyst target price,
recommendation, debt), `summaryDetail` (P/E, dividend yield, payout ratio,
52w range), `defaultKeyStatistics` (P/B, beta, EPS), `price` (name, market
cap, currency). Most numeric fields are `{"raw": <value>, "fmt": "..."}` —
extract `.raw`.

## 3. Technical indicators from raw closes (stdlib only)

```python
def sma(vals, n): return sum(vals[-n:]) / n

def rsi(vals, period=14):
    deltas = [vals[i]-vals[i-1] for i in range(1, len(vals))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain, avg_loss = sum(gains)/period, sum(losses)/period
    if avg_loss == 0: return 100
    return 100 - (100/(1 + avg_gain/avg_loss))

def ema(vals, n):
    k = 2/(n+1)
    e = vals[0]
    for v in vals[1:]: e = v*k + e*(1-k)
    return e
```

MACD = `ema(closes, 12) - ema(closes, 26)`. Compare last close against
SMA20/50/200 for trend positioning; RSI > 70 overbought, < 30 oversold.

## Full worked example (BBRI.JK, one session)

```python
import json
from hermes_tools import terminal

r = terminal("curl -s 'https://query1.finance.yahoo.com/v8/finance/chart/BBRI.JK?range=1y&interval=1d' -H 'User-Agent: Mozilla/5.0'")
data = json.loads(r['output'])
result = data['chart']['result'][0]
closes = [c for c in result['indicators']['quote'][0]['close'] if c is not None]
# ... sma/rsi/ema as above
```

This produced a correct, well-received report combining price action,
RSI/MACD/SMA positioning, P/E, P/B, ROE, dividend yield, and analyst
consensus — see report shape in SKILL.md.

This same pattern extends to any ticker/exchange Yahoo covers, not just
Indonesian stocks — swap the `.JK` suffix accordingly (`.L` London, no
suffix for US, etc.).
