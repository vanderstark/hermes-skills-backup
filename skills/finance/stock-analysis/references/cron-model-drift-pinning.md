# Cron Job Model Drift & Pinning — Operational Reference

## The Problem

When the global Hermes model config changes (e.g. `cc/claude-sonnet-5` → `hermes` alias), existing cron jobs with `model: null` / `provider: null` (unpinned) silently fail at runtime with:

```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (model 'cc/claude-sonnet-5' -> 'hermes'), and this job is unpinned. No inference call was made. To run on the new config, pin it explicitly: `cronjob action=update job_id=... provider=<provider> model=<model>` (or pin the original values to keep them).
```

Jobs show `last_status: error` and `executed: true, execution_success: false`.

## Root Cause

Cron jobs capture a `model_snapshot` / `provider_snapshot` at creation time. If the global config changes and the job isn't explicitly pinned, the scheduler refuses to run it to prevent silent model changes (which could alter behavior/cost).

## Fix: Pin Jobs to Current Config

**Preferred (API):**
```bash
cronjob action=update job_id=<id> model=hermes provider=custom
```
But `cronjob action=update` requires a non-empty `prompt` or `skills` change — just passing `model`/`provider` returns `"No updates provided."`

**Workaround (combined):**
```bash
cronjob action=update job_id=<id> prompt="<FULL_CURRENT_PROMPT>" model=hermes provider=custom
```

**Direct file edit (risky — see below):**
Edit `/opt/data/cron/jobs.json`, set `model` and `provider` (and `model_snapshot`/`provider_snapshot`) on each job object, then save.

## ⚠️ Critical Risk: Direct jobs.json Edit Can Drop Jobs

In this session, manually rewriting `/opt/data/cron/jobs.json` to add `model: hermes, provider: custom` to the three analysis jobs **silently dropped the 4th job** (the `no_agent: true` DeepSeek V4 checker script job) because the JSON written didn't include it.

**Rule:** Never edit `/opt/data/cron/jobs.json` directly for model pinning. Use the `cronjob action=update` API with the FULL prompt — it atomically updates only the target job.

If the API refuses (e.g. "No updates provided"), the workaround is:
1. `cronjob action=list` to get job IDs
2. `read_file /opt/data/cron/jobs.json` to get full prompt for each
3. `cronjob action=update job_id=... prompt="<FULL_PROMPT>" model=hermes provider=custom` for each job

## Prevention: Pin at Creation Time

When creating new recurring analysis jobs, explicitly include:
- `model: "hermes"` (or current active model alias)
- `provider: "custom"`
- `model_snapshot: "hermes"`
- `provider_snapshot: "custom"`

This avoids the drift error entirely if the global config changes later.

## Verification After Pinning

After updating:
1. `cronjob action=run job_id=<id>` — should show `execution_success: true`
2. Check `last_run_at` updates and `last_status: ok`
3. Confirm delivery via `search_files(pattern="cron_<job_id>_<timestamp>.*deliver", file_glob="agent.log")`

## Note on Model Aliases

The `hermes` model alias maps to the active provider chain (currently custom proxy → cc/claude-sonnet-5, fallback → 9router). Pinning to the alias (`hermes`) is correct — it follows the active config. Pinning to a specific model ID (`cc/claude-sonnet-5`) would break if the proxy target changes.