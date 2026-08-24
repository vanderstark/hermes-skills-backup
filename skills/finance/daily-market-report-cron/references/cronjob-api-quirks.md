# Cronjob API Quirks

## create
- Membuat job baru memerlukan `prompt` field meskipun pakai `no_agent=true` + `script=`.
- Tanpa prompt → error: `"create requires either prompt or at least one skill"`.
- Solusi: isi prompt placeholder minimal (`"Run market_cache_build.sh"`), delivery=`local`.

## patch
- **TIDAK ADA** action `patch`.
- Error: `"Unknown cron action 'patch'"`.

## update (ganti/patch)
- Pakai `cronjob(action='update', job_id=<id>, ...)`.
- Untuk no_agent job: set ulang `script`, `no_agent=true`, `enabled_toolsets`, `deliver`.
- Prompt dapat di-clear dengan string kosong `""` (jika no_agent) — tapi lebih aman tetap isi placeholder.

## Timeout
- Default 180 detik foreground.
- Job dengan live fetch banyak simbol (Top-N parallel) bisa melebihi → error.
- Solusi: naikkan `enabled_toolsets` (terminal + delegation) agar lebih fleksibel.

## Next Run Timing
- `next_run_at` selalu dihitung berdasarkan timezone WIB (UTC+7), bukan lokal server.
- Jangan konversi ke UTC secara manual — biarkan cronjob yang handle.
