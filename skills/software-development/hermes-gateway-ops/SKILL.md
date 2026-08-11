---
name: hermes-gateway-ops
description: "Fix self-hosted Hermes gateway errors and restarts."
version: 1.0.0
author: JARVIS
license: MIT
metadata:
  hermes:
    tags: [hermes, gateway, telegram, troubleshooting, fallback-provider, self-hosted]
    related_skills: [hermes-agent]
---

# Hermes Gateway Ops (this user's self-hosted deployment)

Operating notes for diagnosing and fixing gateway/model-provider issues on this
user's (Eko/"Bos") self-hosted Hermes instance. Complements the bundled
`hermes-agent` skill (which is protected/read-only) — this skill holds the
deployment-specific facts and the exact recovery playbook that skill doesn't cover.

## Deployment facts (this instance)

- `HERMES_HOME=/opt/data` (not default `~/.hermes`). Config at `/opt/data/config.yaml`,
  logs at `/opt/data/logs/{gateway,agent,errors}.log`.
- Runs in Docker under s6 (`s6-supervise gateway-default`). The gateway process is
  `hermes gateway run --replace`.
- Model: custom OpenAI-compatible proxy, primary at `http://192.168.147.179:20128/v1`
  (`cc/claude-sonnet-5`). A second proxy exists at `http://9router:20128/v1` — use its
  `cc/*` models for fallback; its `gh/*` models 403 ("not licensed to use Copilot").
  Always `curl .../v1/chat/completions` to smoke-test a candidate fallback model before
  wiring it in — don't assume every model in `/v1/models` is actually usable.
- Telegram gateway is allowlisted for user "eko kurnia" (chat id 6544373047) — already
  working, don't assume unauthorized-user issues by default.

## Diagnosing a Telegram/gateway "no reply" or "Empty response from model" error

1. Read `/opt/data/logs/agent.log` (NOT gateway.log — gateway.log only shows
   request/response summaries; agent.log has the actual API-call-by-call trace
   including retry counts and provider error bodies). Search near the timestamp
   the user reported.
2. Common shapes seen:
   - `Empty response (no content or reasoning) — retry N/3` then `attempting fallback`
     → primary model returned nothing (often triggered by very long session context,
     e.g. 100k+ tokens / 100+ turns — the fix is `/reset` in the chat, not a provider fix).
   - `Fallback activated` immediately followed by an HTTP error (e.g. 403 "not licensed")
     → the fallback entry itself is misconfigured; fix the fallback chain (below).
3. Cross-check the provider is actually reachable:
   `curl -s -m 10 -o /dev/null -w "HTTP %{http_code}\n" <base_url>/models -H "Authorization: Bearer $ENV_VAR"`

## Configuring a fallback provider (non-interactive)

`hermes fallback add` requires a real TTY (curses picker) — it cannot run via
`terminal()`/piped stdin, even with `pty=true` in this environment. Do NOT waste
turns retrying it. Instead write the chain directly through the same helpers the
CLI uses, which keeps validation/format identical to what `hermes fallback list`
expects:

```python
from hermes_cli.config import load_config, save_config
from hermes_cli.fallback_cmd import _read_chain, _write_chain

cfg = load_config()
chain = _read_chain(cfg)
chain.append({
    "provider": "custom",
    "model": "cc/claude-sonnet-5",          # verify with a curl smoke test first
    "base_url": "http://9router:20128/v1",
    "api_key_env": "HERMES_CUSTOM_9ROUTER_20128_API_KEY",
})
_write_chain(cfg, chain)
save_config(cfg)
```
Run via `execute_code`/`terminal -c` with `sys.path.insert(0, '/opt/hermes')` first.
Verify with `hermes fallback list` afterward. Changes to `config.yaml` require a
gateway restart to take effect on the live Telegram session (see below).

## Restarting the gateway — MUST be from outside this session

If the current agent session is itself running inside the gateway process
(`HERMES_GATEWAY_SESSION=1` in env — check before attempting), any `kill`/restart
of the gateway PID is blocked by the runtime: SIGTERM would propagate to this
session's own child processes before the restart could complete, so the safety
guard refuses it outright. Do not spend turns trying to work around this from
within the session (backgrounding, detaching, `setsid`, etc. do not help — the
block is structural, not a shell technicality).

Correct flow:
1. Make the config change (see above) — this persists to disk immediately, no
   restart needed for that step.
2. Tell the user to run `hermes gateway restart` (or `kill -TERM $(pgrep -f
   "hermes gateway run")` — s6 auto-revives it) from a **separate terminal/SSH
   session**, not from inside this chat.
3. After the user confirms, verify from here: `tail -N /opt/data/logs/gateway.log`
   should show a fresh `Starting Hermes Gateway...` / `✓ telegram connected` block
   with a recent timestamp.

## Checking what models a custom provider actually has

Before wiring a new model alias (e.g. user asks "add model X"), verify it exists on
the target provider first — `config.yaml`'s `custom_providers[].models` list is a
cache written at setup time and goes stale; the live provider may have more or
fewer models than what's listed there. Query the source of truth directly:

```bash
source /opt/data/.env 2>/dev/null   # loads HERMES_CUSTOM_<HOST>_<PORT>_API_KEY vars
curl -s http://9router:20128/v1/models \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_20128_API_KEY" \
  | python3 -c "import json,sys; print('\n'.join(m['id'] for m in json.load(sys.stdin)['data']))"
```

Grep/filter the id list for the requested name (case-insensitive substring match —
users often say a codename like "deepseek v4" that may not match the provider's
exact model id). If it's not there, tell the user plainly it's not available on
that provider yet rather than guessing at an id and wiring a broken alias.

### Polling for a model to appear later (no_agent cron pattern)

If the user wants to be notified when a model becomes available rather than
checking again themselves, create a `no_agent=true` cron job whose `script` runs
the same curl+filter above and only `print`s when the target model id is found.
`no_agent` jobs stay silent on empty stdout and don't burn LLM tokens per tick —
this is the right tool for "watch for X to show up" style requests, not a normal
agent-driven job. Example schedule: daily (`0 9 * * *`) is enough for model
rollout cadence; don't over-poll a slow-changing resource.

## User says a cron-delivered report "never arrived"

Before re-running the job or assuming delivery is broken, check server-side
whether it actually sent:

1. `cronjob action=list` — check `last_run_at` / `last_status` for that job.
   `last_status: ok` means the run completed without error, but says nothing
   about delivery.
2. Grep `agent.log` for the job's ID with a delivery-specific pattern:
   ```
   grep "<job_id>.*deliver" /opt/data/logs/agent.log
   ```
   A line like `Job '<job_id>': delivered to telegram:<chat_id> via live
   adapter` confirms the platform adapter accepted the message — the report
   was sent from Hermes' side.
3. Also check `errors.log` around that timestamp for a delivery-layer
   failure (rate limit, auth, network) that wouldn't show in agent.log.
4. If both agent.log shows "delivered" and errors.log is clean, the message
   left the system successfully — the likely explanation is it's further up
   in the chat history (scrolled past) or a missed notification, not a
   pipeline failure. Tell the user this plainly instead of silently
   re-running the job; offer to re-run only if they still want the content
   surfaced again, not as an automatic recovery action.

## Adding MCP servers on this deployment (`hermes mcp add`)

The `hermes` wrapper at `/opt/hermes/hermes` can fail to even start with
`ModuleNotFoundError: No module named 'dotenv'` (a broken/incomplete venv
install, not a missing MCP feature). Workaround: invoke the CLI module
directly through the same venv's Python instead of the broken wrapper:

```bash
HERMES_HOME=/opt/data /opt/hermes/.venv/bin/python3 -m hermes_cli.main mcp <subcommand> ...
```

This works identically to `hermes mcp ...` — same subcommands (`add`,
`list`, `test`, `remove`, `catalog`). Always pass `HERMES_HOME=/opt/data`
(this deployment's non-default home) so the CLI reads/writes the right
`config.yaml`.

`hermes mcp add <name> --command <cmd> --args ...` prompts interactively
with `Enable all N tools? [Y/n/select]:` — this blocks in a non-TTY
`terminal()` call unless piped:

```bash
echo "Y" | HERMES_HOME=/opt/data /opt/hermes/.venv/bin/python3 -m hermes_cli.main \
  mcp add firecrawl --command npx --args -y firecrawl-mcp
```

A successful run prints `✓ Saved '<name>' to /opt/data/config.yaml (N/N
tools enabled)`. Verify anytime with `mcp list` (shows configured servers
+ enabled tool counts) or `mcp test <name>` (live reconnect + tool
discovery, useful to confirm a server still works after a config change).
Newly added MCP tools only appear in **new** sessions — the current
session's tool list is fixed at conversation start, so tell the user a
`/new` session is needed before the added tools (e.g. `firecrawl_search`,
`web_search_exa`) become callable.

Two research-oriented MCP servers run in **keyless/free mode** out of the
box — no signup, no API key, just rate-limited by IP — useful whenever a
skill (e.g. `deep-research`) calls for firecrawl/exa but no key is
configured:
- `firecrawl-mcp` (npx package `firecrawl-mcp`): `firecrawl_scrape` and
  `firecrawl_search` work keyless; other tools (crawl, monitor, agent,
  research_*) need a `FIRECRAWL_API_KEY` from firecrawl.dev.
- `exa-mcp-server` (npx package `exa-mcp-server`): connects keyless with a
  reduced 2-tool set (`web_search_exa`, `web_fetch_exa`) instead of its
  full tool catalog, which needs `EXA_API_KEY`.

## Session-too-long empty responses

If `agent.log` shows the primary model failing only after the session has grown
very large (check `in=` token count in the `API call` log line — six figures is a
red flag), the fix is not a provider/fallback change: recommend the user send
`/reset` in that Telegram chat to start a fresh session. Do this instead of (or in
addition to) fallback wiring when the token count signal is present.

## Checking token/usage stats ("berapa % token terpakai hari ini")

`hermes insights --days N` gives an aggregate summary (input/output tokens,
tool calls, sessions) but **only reflects sessions that have already been
finalized/checkpointed to the DB** — the currently-live session (e.g. the
Telegram chat the user is asking from right now) is usually NOT included,
because its usage hasn't been flushed yet. Don't present the insights total
as "today's total" without this caveat.

```bash
HERMES_HOME=/opt/data /opt/hermes/.venv/bin/python3 -m hermes_cli.main insights --days 1
```

For a more granular/manual check (e.g. per-cron-job breakdown), query
`session_model_usage` directly in `/opt/data/state.db`:

```bash
HERMES_HOME=/opt/data /opt/hermes/.venv/bin/python3 -c "
import sqlite3
conn = sqlite3.connect('/opt/data/state.db')
cur = conn.cursor()
cur.execute(\"SELECT session_id, input_tokens, output_tokens FROM session_model_usage WHERE session_id LIKE '%_20260804_%'\")
for row in cur.fetchall():
    print(row)
"
```

The `sessions` table (not `session_model_usage`) has per-session
`input_tokens`/`output_tokens`/`message_count` columns keyed by `id` and
`source` (e.g. `source='telegram'`) — useful for finding the live session's
row, but note its counters are **cumulative since the session was last
`/reset`**, not scoped to a calendar day. A long-lived Telegram session that
hasn't been `/reset` in days will show a token count spanning its entire
lifetime, not "today" — flag this distinction explicitly to the user rather
than presenting a multi-day cumulative number as a daily figure.

There is no live, mid-session "% of context window used right now" figure
available from outside the running process — the model's context window
size (`model.context_length`, defaults to 256,000 for this deployment's
custom provider per the `agent.log` probe-down messages) can be stated, but
computing "how full is it right now" isn't possible via the state DB;
recommend periodic `/reset` if the user wants cleaner day-by-day tracking
instead of trying to compute a live percentage.
