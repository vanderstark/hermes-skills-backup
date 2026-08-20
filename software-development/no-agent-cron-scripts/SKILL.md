---
name: no-agent-cron-scripts
description: Convert slow LLM cron jobs to fast no_agent Python scripts.
---

# No-Agent Cron Scripts (Fast Scheduled Automation)

## When to use
- A recurring cron job is slow (minutes–hours) because the LLM agent does dozens of sequential tool calls (fetch → compute → fetch) with reasoning between each.
- The job is mostly deterministic: fetch from known endpoints + compute + print a fixed-format report. If a human could script it in ~30 lines, it should be a script.
- You want zero token cost and consistent output for a scheduled report/watchdog.

Signs it is LLM-bound: user complains "loading-nya lama", the run produces no output file, or a job that is only a few HTTP calls takes >>1 minute.

## Steps

1. **Write a standalone Python script** — stdlib only (`urllib.request`, `json`, `time`, `datetime`). The cron environment may lack pip packages (no numpy/pandas/requests). SMA/RSI/MACD/OBV all fit in plain loops.
2. **Save under `$HERMES_HOME/.hermes/scripts/`** — e.g. HERMES_HOME=/opt/data → `/opt/data/.hermes/scripts/<name>.py`. NOTE: `/opt/hermes/scripts` (image dir) is read-only; use the home-relative path.
3. **Attach to the job** with a RELATIVE filename only:
   ```
   cronjob update job_id=<id> script=<filename.py> no_agent=true
   ```
   Absolute/home-relative paths are REJECTED: "Script path must be relative to ~/.hermes/scripts/".
4. **Verify**: `cronjob list` shows no_agent=true + script, or inspect `$HERMES_HOME/cron/jobs.json` (no_agent flag = 1).
5. **Test manually** before the schedule fires: run the script by hand and confirm stdout has the full report. Non-empty stdout is delivered verbatim to the chat; empty stdout = silent run (watchdog pattern).
6. The old LLM prompt can stay on the job as documentation — with no_agent=true it is ignored.

## Pitfalls
- `cronjob update` with ONLY model/provider (no prompt/script/name) → `{"error": "No updates provided."}`. Always include at least one other field.
- Writing files that contain backticks / `$VAR` via shell heredoc or `python3 -c "..."` mangles content: `$(...)` gets command-substituted, `$JWT_SECRET` becomes empty/hash, backticks execute. Use the `write_file` tool (safe root) then `cp`, or a QUOTED heredoc `<<'EOF'`.
- Compute timezone in the script yourself: `datetime.now(timezone.utc).timestamp() + 7*3600` for WIB — the cron env may not have host TZ.
- Throttle per-symbol HTTP calls (`time.sleep(0.15)`) to avoid Yahoo/CoinGecko rate limits.
- After model/config drift a job fails 'unpinned — Skipped to prevent spend' — re-pin: `cronjob update job_id=<id> model=hermes provider=custom`.

## Worked example
The user's daily market report (3 jobs: 08:00/16:30/20:00 WIB) was converted from a 4k-char LLM prompt that stalled for minutes → a ~13 second stdlib Python script (`market_report_fast.py`). The script fetches Yahoo screener (~839 IDX tickers + US + crypto), calculates SMA/RSI/MACD/OBV, detects support/resistance from 1-year swing clusters, cross-checks crypto via CoinGecko + Indodax IDR, and prints fixed-width tables with Entry/SL/TP1-3. Skeleton reusable pattern: `analyze_symbol()` → 1y daily + 2y weekly chart → indicators → cluster levels → rank → print.

Template: `templates/market_report_fast.py` — the full working script. Copy, adjust symbol lists, redeploy.

## User communication (Eko/Bos)
- Output in Indonesian, address as "Bos", hormat (respectful) tone with ~3x respect expressions per reply.
- Emoji: use exactly **three 🙏🙏🙏 in a row** per message (not one, not scattered) — user corrected this explicitly multiple times, "1x 🙏 kurang".
- Full report = IDX + US + Crypto in ONE message — never stop after IDX.
