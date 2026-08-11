---
name: stock-analysis
description: Analyze a stock using free public market data (no paid API).
metadata:
  version: "1.0.0"
---

# Stock Analysis (Free Data Sources)

Produce a technical + fundamental writeup for any publicly traded ticker
when no paid market-data MCP (Octagon, Bloomberg, etc.) is connected. This
is the default path — reach for it before telling the user a paid
integration is required.

## When to use this skill

Load it whenever the user asks to analyze, evaluate, or get an opinion on
a specific stock ticker or company ("analyze BBRI", "how's AAPL doing",
"is this stock a buy") and no dedicated market-data MCP/tool is already
wired up in the session.

Also load it when the user asks to **screen/scan an entire market or
index** for opportunities ("cari saham bagus di IDX yang lagi support
kuat", "screen semua saham") — do NOT decline this as impractical or
silently narrow it to a small index without asking first. See
`references/market-wide-screening-yahoo.md` for the batched-quote pattern
that makes scanning 800+ tickers cheap (a handful of `/v7/finance/quote`
batch calls instead of one `/v8/finance/chart` call per ticker).

## Data source: Yahoo Finance (unauthenticated + lightly-authenticated)

See `references/live-market-data-yahoo.md` for the full recipe: price
history endpoint (no auth), the fundamentals endpoint (needs a session
cookie + crumb — Yahoo returns "Invalid Crumb" without it, the reference
has the two-step curl fix), and stdlib-only Python for SMA/RSI/MACD/EMA
so no numpy/pandas dependency is required.

Works across exchanges by ticker suffix (`.JK` Jakarta, `.L` London, no
suffix for US, etc.) — same pattern, not Indonesia-specific. Crypto tickers
use the `-USD` suffix (BTC-USD, ETH-USD, etc.) on the same endpoints.

For crypto priced in Indonesian Rupiah / "harga di Indodax" / "pasar
Indodax lagi ramai apa" style questions, use Indodax's own public API
instead — it's unauthenticated, IDR-native (includes the local exchange
premium), and carries real local trading volume, which is what the user
actually means by "ramai". See `references/indodax-crypto-data.md` for the
endpoint, fields, and derived momentum/range metrics. Still fall back to
Yahoo's chart endpoint for RSI/MACD/SMA history — Indodax has no candle
data.

## Recurring multi-asset screening reports (cron jobs)

When the user wants a recurring job (e.g. 3x/day) that screens IDX stocks,
US stocks, and/or crypto together and recommends picks near their
strongest support level with concrete Entry/SL/TP1/TP2 levels, see
`references/multi-asset-recurring-screening-cron.md` for the full
per-asset-class filter thresholds, ranking heuristic, and the pattern for
extending an existing cron job's prompt (append a new section, don't spin
up a duplicate job for the same schedule).

## Cron job model drift & pinning (operational)

When the global Hermes model config changes (e.g. `cc/claude-sonnet-5` →
`hermes`), existing unpinned cron jobs fail with a "config drifted" error.
See `references/cron-model-drift-pinning.md` for the fix pattern, the
direct-file-edit risk (silently drops other jobs), and prevention by
pinning at creation time (`model: "hermes", provider: "custom"`).

## Report shape

1. Current price, 52-week range, market cap
2. Technical table (RSI14, MACD, price vs SMA20/50/200, 1M/3M/1Y % change)
   with a one-line plain-language read of the pattern
3. Fundamentals table (P/E trailing+forward, P/B, ROE/ROA, margins,
   dividend yield + payout ratio, revenue/earnings growth)
4. Analyst consensus (recommendation, mean/high/low target price, analyst
   count) if available from the fundamentals payload
5. Plain-language bull points and risk points, not just raw numbers
6. Explicit disclaimer that this is public-data analysis, not personalized
   investment advice — the call depends on the user's own risk profile and
   horizon

## Pitfalls

- Don't stop at price data alone — a "stock analysis" request implies both
  technical and fundamental context; fetch both endpoints.
- The fundamentals endpoint fails silently-ish with a JSON error body
  (`{"finance":{"result":null,"error":{"code":"Unauthorized",...}}}`) —
  check for that shape before assuming the module keys are missing.
- Numeric fields in `quoteSummary` responses are usually wrapped as
  `{"raw": ..., "fmt": "..."}` — always pull `.raw`, not the dict itself.
