# Indodax (Indonesian crypto exchange) market data

For crypto price/volume questions framed around the Indonesian market
("pasar di Indodax", "harga BTC di Indodax", prices in IDR terms local
traders actually see) prefer Indodax's own public API over Yahoo Finance
`-USD` tickers — it gives IDR-denominated prices (which include the local
exchange premium vs global USD price) and real IDR trading volume, which
is what the user actually cares about when asking about "pasar rame" /
"lagi ramai apa".

## Endpoint

Single unauthenticated GET, no API key, no crumb dance needed:

```bash
curl -s "https://indodax.com/api/summaries" -H "User-Agent: Mozilla/5.0" -o /tmp/indodax.json
```

Returns `{"tickers": {"<pair>_idr": {...}, ...}}` for ~500 pairs. Per-pair fields used:

- `last`, `high` (24h), `low` (24h) — all IDR, as strings (cast to float)
- `buy` / `sell` — current top bid/ask
- `vol_idr` — 24h volume in IDR (use this to rank "which coins are busiest today")
- `vol_<coin>` — 24h volume in the coin's own unit (e.g. `vol_btc`)

Ticker keys are lowercase `<symbol>_idr`, e.g. `btc_idr`, `eth_idr`, `dot_idr`.

## Useful derived metrics (stdlib Python, no pandas needed)

```python
last, high, low = float(t['last']), float(t['high']), float(t['low'])
range_pos_pct = (last - low) / (high - low) * 100 if high != low else 50   # 0=at 24h low, 100=at 24h high
momentum_from_low_pct = (last - low) / low * 100 if low > 0 else 0         # how far it's run off the 24h floor
```

- Rank by `vol_idr` descending to answer "which coins are the busiest / most
  ramai today" — USDT and BTC usually dominate; watch for volume among
  smaller-cap tokens as it signals rotation/pump activity.
- `momentum_from_low_pct` well above ~20-30% on a low-cap/low-liquidity pair
  is a pump signal — flag it explicitly as high-risk/volatile rather than a
  clean buy signal (e.g. seen: a token up +103% off its 24h low on modest
  volume — call that out as a pump, not a trend).
- `range_pos_pct` near 100 = trading at/near 24h high (momentum, but closer
  to local resistance); near 0 = at/near 24h low.

## Pitfalls

- Indodax prices run at a premium to global USD*USDIDR conversion because
  of local liquidity — don't be surprised if it doesn't match Yahoo's
  `BTC-USD` * USDIDR exactly; that's expected, not a data error.
- `vol_idr` field name is literal — some smaller pairs report 0 or missing
  volume; guard with `.get('vol_idr', 0)`.
- This endpoint has no historical/candle data — for RSI/MACD/SMA on a coin,
  still fall back to Yahoo's `-USD` chart endpoint (see
  `live-market-data-yahoo.md`) and only use Indodax for current
  price/volume/range snapshot in IDR terms.
