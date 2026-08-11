# Multi-asset recurring screening reports (cron) — IDX + US equities + Crypto

When a user wants a recurring (e.g. 3x/day) automated "best support-level
picks" report spanning multiple asset classes (Indonesian IDX stocks, US
stocks, and crypto), extend one cron job prompt per session rather than
building separate jobs per asset class — the user wants ONE report with
multiple sections, not multiple messages.

## Screening pattern (same shape per asset class, different universe)

1. **Universe**: pull symbols via Yahoo Finance screener
   (`query2.finance.yahoo.com/v1/finance/screener`, POST, region filter
   `id` for IDX / `us` for US equities) or a hardcoded liquid watchlist
   for crypto (Yahoo ticker suffix `-USD`: BTC-USD, ETH-USD, BNB-USD,
   SOL-USD, XRP-USD, ADA-USD, DOGE-USD, AVAX-USD, DOT-USD, LINK-USD,
   TRX-USD, ATOM-USD, NEAR-USD, LTC-USD). Crypto quote/chart calls
   usually don't need the cookie+crumb dance that IDX/US quote/fundamentals
   calls require — try without first.
2. **Quote batch**: `/v7/finance/quote` with up to 100 symbols per call,
   requesting `regularMarketPrice, fiftyTwoWeekLow, fiftyTwoWeekHigh,
   fiftyDayAverage, twoHundredDayAverage, averageDailyVolume3Month,
   trailingPE, marketCap, averageAnalystRating, regularMarketChangePercent`.
3. **Filter thresholds differ per asset class** — don't reuse IDX
   thresholds for US or crypto:
   - IDX: price >= 100 IDR, avg 3M volume >= 3,000,000, market cap >= 1T
     IDR, analyst rating contains "Buy", trailing PE 0-30.
   - US: price >= $5, avg 3M volume >= 1,000,000, market cap >= $10B,
     analyst rating contains "Buy", trailing PE 0-40.
   - Crypto: no PE/rating filter (doesn't apply) — just rank by
     proximity to 52w low + MA200, and widen SL/TP distance since
     crypto is materially more volatile than equities.
4. **Ranking/selection**: for all three, rank candidates by combined
   closeness of price to 52-week low AND to SMA200 — that's the shared
   "near strongest support" heuristic the user wants. Take top 3-5 per
   asset class.
5. **Per-pick technicals**: `/v8/finance/chart/<SYMBOL>?range=1y&interval=1d`
   → compute RSI14, MACD, SMA20/50/200, swing low over 20/60 days with
   stdlib Python (see `references/live-market-data-yahoo.md`).
6. **Entry/SL/TP1/TP2**: derive from swing highs/lows, SMA levels, and
   52-week range — always include these four numbers per pick, that's
   the deliverable the user actually wants, not just raw indicator values.
7. **Report shape**: one title, then one section per asset class in a
   consistent format (name, price, why-near-support, RSI, PE/marketcap,
   rating if applicable, Entry/SL/TP1/TP2), one favorite pick flagged per
   section, and a closing disclaimer that this is public-data analysis,
   not personalized investment advice.

## Troubleshooting: user says a scheduled report "didn't arrive"

Before re-running the job or assuming delivery failed, check the logs — don't
just trust the user's "I didn't get it" at face value, and don't blindly
trigger a re-run first either. `cronjob action=list` shows `last_run_at` /
`last_status`, which confirms the job fired, but not whether delivery
succeeded. Grep the agent log for the specific run:

```
search_files(pattern="cron_<job_id>_<run_timestamp>.*(deliver|Deliver)",
             file_glob="agent.log", path="<hermes_home>/logs")
```

A line like `delivered to telegram:<chat_id> via live adapter` confirms the
message was sent — the user likely just missed it in scrollback/notifications.
Also check `errors.log` for the same time window in case delivery silently
failed. Only after confirming via logs that nothing was sent should you
re-trigger with `cronjob action=run` — if logs show successful delivery,
tell the user to check their client instead of re-running (a redundant
re-run doubles the report for no reason if the first one actually landed).

## Extending an existing cron job to add an asset class

Read the job's current `prompt` in full (`cronjob action=list` only
returns a truncated `prompt_preview` — get the full text from
`/opt/data/cron/jobs.json` or by tracking what you last set), then call
`cronjob action=update` with the SAME `job_id`, appending a new numbered
step block for the new asset class plus a note to add its report
section — don't replace the existing IDX/US content, and don't create a
second job for the same schedule. Repeat once per existing recurring job
(e.g. once each for Pagi/Sore/Malam) so all three keep the same coverage.

Practical append workflow that avoids terminal quoting hell for a ~7-8k
character prompt: write the addendum text to a scratch file with
`write_file`, read the job's current full prompt from
`/opt/data/cron/jobs.json` via `read_file`, concatenate in a `terminal`
Python heredoc (`python3 << 'EOF' ... EOF`) into a `/tmp/new_prompts_*.json`
map of `{job_id: new_prompt}`, sanity-check the merged length/tail with
`read_file`, then paste each job's final prompt into a `cronjob
action=update` call per job_id. `execute_code` is blocked for touching
`/opt/data/cron/jobs.json` directly under cron-mode approval policy — do
the file surgery in scratch `/tmp` files via `terminal`/`read_file`/
`write_file` and let `cronjob action=update` be the only mutator of the
actual job record.

## Cross-validating crypto prices across sources (no paid API key)

When the user wants crypto price data to be more accurate/robust than a
single source, add a same-shape cross-check step against a second free
API rather than switching sources — CoinGecko's public markets endpoint
needs no API key and no auth dance:

```
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h,7d" -H "User-Agent: Mozilla/5.0"
```

Pattern for a report/cron step: fetch the same top coins from both
CoinMarketCap (if already integrated) and CoinGecko, flag a note if the
two prices differ by more than ~2% (usually reflects listing/liquidity
differences rather than an error), and average the two for the number
actually shown in the report. For Indonesian-market questions keep using
Indodax as the IDR-native source (see `references/indodax-crypto-data.md`)
and treat CoinMarketCap+CoinGecko as the USD/global cross-check layer, not
a replacement for Indodax's local pricing.

This "add a second free source and average/flag-divergence" pattern
generalizes beyond crypto — the same idea applies if the user later asks
for a second stock-data source alongside Yahoo Finance (e.g. Finnhub,
Alpha Vantage, Twelve Data) — those require a free API key signup (a
one-time human step, not something the agent can complete unattended),
so surface that requirement plainly rather than promising integration is
already done.

## Critical pitfall: never paste a truncated placeholder into a cron job prompt

When updating a job's prompt via `cronjob action=update`, the full prompt
string you pass IS what gets stored verbatim — there is no server-side
"resolve this placeholder" step. If you read the old prompt back through
something that truncates long output (a `cronjob action=list` preview, or
your own summary text showing `"...[truncated]"`) and then paste that
truncated text as the new prompt, the literal string `[truncated]` gets
saved as part of the job's actual instructions, silently destroying every
step after the cut point. This happened for real: a job that used to
screen IDX + US + Crypto got reduced to ~200 chars of just the IDX
opening sentence, and every subsequent run only produced an IDX section —
no error, no warning, just quietly incomplete output for multiple days
until the user asked "why is only IDX showing up tonight?".

Rule: before calling `cronjob action=update`, always read the CURRENT
FULL prompt with `read_file` on `/opt/data/cron/jobs.json` (or from a
`/tmp` scratch file you wrote it to earlier in the same session) and
verify the tail of that string is real content, not an ellipsis or a
truncation marker, before concatenating an addendum and pasting the
result into the update call. Sanity-check length: if the "full" prompt
you're about to submit is suspiciously short relative to what the job
used to do, stop and re-fetch instead of submitting it.

## Pitfall: agent stops after the first section despite a complete multi-section prompt

Even with a fully intact prompt, a long numbered multi-section prompt
(IDX steps 1-7, then US steps 8-10, then Crypto steps 11-13) can cause
the executing agent to write a "final" report after finishing only the
first section and never continue to the later steps — it treats the
first section's own wrap-up instruction ("Tutup dengan disclaimer...",
"Response akhir kamu adalah laporan itu sendiri...") as if it means the
whole task is done. Symptom: a recurring report that used to cover
multiple asset classes silently regresses to covering only the first one,
with `last_status: ok` in `cronjob action=list` (the job ran fine, it
just did less than instructed) — don't assume "ok" status means the full
prompt was followed; read the actual delivered report content via
`session_search` on the cron run's session id.

Mitigation: prepend an explicit, impossible-to-miss instruction at the
very top of the prompt (before step 1) stating how many sections the
final report MUST contain and that finishing an early section is NOT
completion — e.g. "Laporan ini HARUS mencakup TIGA bagian: IDX, US,
Crypto — jangan anggap tugas selesai setelah IDX saja; ikuti SEMUA langkah
bernomor sampai selesai." This front-loaded reminder measurably reduces
the early-stop failure mode for cron jobs with 10+ numbered steps.
