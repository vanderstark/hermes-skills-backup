# Screening an entire market/exchange (not just one ticker)

When the user asks to scan/screen a whole exchange or index (e.g. "cari
saham IDX yang bagus dan di support kuat", "screen semua saham 900-an") —
don't try to hit `/v8/finance/chart/<TICKER>` one by one for hundreds of
tickers first. Get the universe + batch fundamentals in two cheap calls,
then only pull daily price history for the shortlist that survives
filtering.

## Step 1 — Get the full ticker universe via the screener endpoint

Needs the same cookie+crumb dance as quoteSummary (see
`live-market-data-yahoo.md`). Region codes: `id` = Indonesia (IDX),
`us` = USA, etc. Paginate with `size`/`offset` (max size 250 per call).

```bash
curl -s -c /tmp/yc.txt "https://fc.yahoo.com" -H "User-Agent: Mozilla/5.0" -o /dev/null
CRUMB=$(curl -s -b /tmp/yc.txt "https://query2.finance.yahoo.com/v1/test/getcrumb" -H "User-Agent: Mozilla/5.0")

curl -s -b /tmp/yc.txt -H "User-Agent: Mozilla/5.0" -H "Content-Type: application/json" \
  -X POST -d '{"size":250,"offset":0,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","query":{"operator":"AND","operands":[{"operator":"EQ","operands":["region","id"]}]}}' \
  "https://query2.finance.yahoo.com/v1/finance/screener?crumb=$CRUMB&lang=en-US&region=US&formatted=true"
```

Response: `finance.result[0].total` (e.g. 839 for IDX) and `.quotes[]`
with `symbol`. Loop `offset += 250` until `offset >= total`.

## Step 2 — Batch fundamentals via `/v7/finance/quote` (up to ~100 symbols/call)

This is the key shortcut — one call returns price, 52w range, MAs, PE,
dividend yield, market cap, and analyst rating for up to ~100 tickers at
once, so screening 800+ names only costs ~9 HTTP calls, not 800.

```bash
CRUMB=$(curl -s -b /tmp/yc.txt "https://query2.finance.yahoo.com/v1/test/getcrumb" -H "User-Agent: Mozilla/5.0")
FIELDS="symbol,shortName,regularMarketPrice,fiftyTwoWeekLow,fiftyTwoWeekHigh,fiftyDayAverage,twoHundredDayAverage,regularMarketVolume,averageDailyVolume3Month,trailingPE,priceToBook,dividendYield,marketCap,averageAnalystRating,regularMarketChangePercent"
curl -s -b /tmp/yc.txt -H "User-Agent: Mozilla/5.0" \
  "https://query2.finance.yahoo.com/v7/finance/quote?symbols=SYM1,SYM2,...&fields=$FIELDS&crumb=$CRUMB"
```

Sleep ~0.8s between chunks to avoid rate limiting. Do this loop in
`execute_code` (Python + subprocess), not one-tool-call-per-chunk in the
main turn — keeps ~9 screener calls out of the visible conversation.

## Step 3 — Filter in Python before doing anything expensive

Typical useful filters for "good stock at support" style screens:
- Liquidity: `averageDailyVolume3Month` above a floor (e.g. 1-3M shares)
- Size: `marketCap` above a floor to exclude micro-caps/gorengan
- Quality: `averageAnalystRating` contains "Buy", `trailingPE` in a sane
  range (0 < PE ≤ 30)
- Support proximity: `(price - fiftyTwoWeekLow) / fiftyTwoWeekLow` small,
  or price close to `twoHundredDayAverage`/`fiftyDayAverage` from above
  (trading near a moving-average support level, not just an all-time low)

Only for the surviving shortlist (5-10 names), pull full 1y daily closes
via `/v8/finance/chart/<TICKER>` (see main reference) to compute RSI14,
MACD, and real swing-low support levels (min of last 20/60/120-day lows)
for entry/SL/TP — the screener endpoint's 52w low is too coarse for that.

## Pitfalls

- `query1.finance.yahoo.com/v8/finance/chart` sometimes returns HTTP 429
  on a single unauthenticated hit if called too soon after a screener
  batch — space it out, and prefer the batched `/v7/finance/quote` for the
  wide scan, reserving `/v8/finance/chart` for the final shortlist only.
- The screener endpoint uses `query2` and needs the crumb; the chart
  endpoint uses `query1`/`query2` and does NOT need a crumb. Don't mix
  them up.
- IDX/exchange listings for "all stocks" via idx.co.id are behind
  Cloudflare (returns "Just a moment..." challenge page to curl) — don't
  waste calls on it; the Yahoo screener has the full universe already.

## Combining multiple markets in one report (e.g. IDX + US)

When a report needs to screen more than one exchange (e.g. a daily IDX
watchlist plus a US large-cap section), run the same 3-step pipeline once
per region and give each region its own filter thresholds — don't reuse
IDX-scale thresholds for a market with different price/liquidity norms.
Example thresholds that worked well:

| Filter              | IDX (region `id`)     | US (region `us`)        |
|----------------------|------------------------|--------------------------|
| Min price            | 100 IDR                | 5 USD                    |
| Min avg 3M volume    | 3,000,000 shares       | 1,000,000 shares         |
| Min market cap       | 1T IDR                 | 10B USD                  |
| Analyst rating       | contains "Buy"         | contains "Buy"           |
| Trailing PE range    | 0–30                   | 0–40                     |

If the full `region=us` screener pagination is too slow/heavy for a
scheduled job, fall back to running `/v7/finance/quote` +
`/v8/finance/chart` directly against a fixed large-cap liquid watchlist
(e.g. AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM, V, XOM) instead of
paginating the full screener — same filter/sort/report logic, just a
pre-seeded universe instead of a scanned one. This keeps a multi-market
recurring report (e.g. a cron job) reliable without needing the full
800+ symbol scan for every region every run.
