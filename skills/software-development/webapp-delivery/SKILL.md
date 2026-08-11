---
name: webapp-delivery
description: "Ship FastAPI+frontend web apps to GitHub with tutorial."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [fastapi, webapp, delivery, github, docker, dashboard, tutorial]
    related_skills: [docker-compose-scaffolding, github-token-deploy-workflow, docker-development]
---

# Web App Delivery (FastAPI + vanilla JS frontend → Docker → GitHub + tutorial)

Class of work: the user (datacenter admin / police-academy AI lab) asks for a
**custom application** ("buat aplikasi seperti X", "buatkan DSS simulasi",
"command center") and then wants it pushed to **their GitHub** with a
**complete Bahasa Indonesia tutorial README**. Examples seen: OSINT War Room
clone → Crisis Command Center (disaster/conflict decision-support app).

Distinct from `docker-compose-scaffolding` (infra/stack compose generation) and
`github-token-deploy-workflow` (the push mechanics — reuse that skill's PAT
pattern; this skill covers what to BUILD and how to VERIFY it).

## When to use

- User asks to build an app/dashboard/simulator and ship it to GitHub with a tutorial
- App is self-contained: one container serving both API and static frontend
- User's lab/datacenter context (police academy, OSINT), Bahasa Indonesia UI + README

## Proven architecture (single container, no build step)

- **Backend**: FastAPI + Pydantic v2, package layout:
  `backend/{main.py, api/, models/, services/}`. Pure-Python compute (impact
  models, allocators, decision engines) lives in `services/`; request/response
  schemas in `models/`; routers in `api/`. Environment-validated Pydantic
  `Enum` values are ASCII English (`earthquake/flood/conflict`); Indonesian
  display labels are a frontend concern.
- **Frontend**: no bundler — static `frontend/index.html` + `css/` + `js/`
  (api.js / map.js / ui.js / main.js), served by FastAPI:
  ```python
  app.include_router(sim.router, prefix="/api/v1")
  app.mount("/", StaticFiles(directory="frontend", html=True))  # MUST be last
  ```
  Mounting static files last is critical — mount before routers and it shadows
  every API route.
- **JS**: plain `<script src>` tags do NOT support ES module `export`/`import`.
  A stray `export {}` in api.js throws "Unexpected export" in browser. Use
  namespace objects (`const API = {...}`) or IIFEs.
- **Docker**: `python:3.12-slim`, `COPY backend/ frontend/`, uvicorn CMD on
  0.0.0.0:8000, curl HEALTHCHECK. Keep `GET /api/health` separate from `/api/status`.
- **Maps**: Leaflet + dark CARTO tiles — initially via CDN; **for offline/LAN use**
  (see section below), self-host all assets + tile cache.

## Offline / LAN deployment (posko darurat, bencana, perang)

When the user asks "kalau internet mati, apa masih jalan?" — the answer is "hampir 100%",
but only if prepared beforehand. Proven pattern from `vanderstark/crisis-command-center`:

1. **Self-host CDN assets** — download Leaflet 1.9.4 (leaflet.js + leaflet.css +
   marker images) + Font Awesome 6.5.1 (all.min.css + webfonts) into
   `frontend/assets/leaflet/` and `frontend/assets/fontawesome/`. Change `<link>`
   and `<script>` tags to relative paths. Verify zero CDN refs:
   ```bash
   grep -c "unpkg.com\|cdnjs.cloudflare.com" frontend/index.html  # → must be 0
   ```
2. **Offline map tiles** — ship `download-tiles.py` (deg2num slippy-map math, area
   bounding boxes for Indonesia/Natuna/Papua/Java/Timor, zoom 3-12 with per-zoom
   tile-count cap ~6000). Users run it locally to cache priority areas. Keep the
   script durable; tile files may be gitignored if huge.
3. **Auto-switch tile layer** — in `map.js`:
   ```js
   window.addEventListener('online',  () => swapTiles('online'));
   window.addEventListener('offline', () => swapTiles('offline'));
   ```
   plus `navigator.onLine` check at init. `swapTiles()` calls `tileLayer.setUrl()`.
4. **LAN access** — `docker-compose.yml` must bind `0.0.0.0:${PORT}:8000` (not just
   `8000:8000`). uvicorn dev: `--host 0.0.0.0`. Test via the server's LAN IP, not 127.0.0.1.
5. **Warn user** that LAN access is unauthenticated by default; offer simple login
   or IP allowlist as a follow-up task.

## Workflow (the parts that catch bugs)

1. **Write code module-by-module**, running `python3 -m py_compile` on every
   backend file after writing:
   ```bash
   python3 -m py_compile backend/main.py backend/api/*.py backend/models/*.py backend/services/*.py
   ```
2. **Live test, don't trust compile**: py_compile only catches syntax. Boot the
   real server and curl the endpoints before claiming success:
   ```bash
   uv venv /tmp/app-venv -q && uv pip install --python /tmp/app-venv/bin/python -q -r requirements.txt
   # terminal(background=true, notify=false): /tmp/app-venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8123
   curl -s http://127.0.0.1:8123/api/health
   curl -s -X POST http://127.0.0.1:8123/api/v1/simulate -H 'Content-Type: application/json' -d '{...}'
   ```
   Test at least one request PER scenario/endpoint. A 422 Pydantic validation
   error is JSON with a `detail` array — read it raw (`head -c 600`) when the
   parse fails; don't assume the whole API is broken. Kill the server via
   `process action=kill` after tests.
3. **Verify static serving too**: `curl -s -o /dev/null -w "%{http_code}"` for
   index.html + each css/js file.
4. Then write the README + push per `github-token-deploy-workflow`.

## Pitfalls (hit this session, will bite again)

- **Pydantic Enum wire format**: the `str, Enum` accepts whatever VALUES are
  defined. Frontend JS sends ASCII English — define the VALUES as those exact
  strings. Localized values (`gempa_bumi`, `banjir`, `konflik`) in the schema
  produce HTTP 422 `Input should be 'gempa_bumi', 'banjir'...`.
- **Slider/range inputs**: display live value in a `<span>` via an `input`
  event listener; don't rely on the browser default (some browsers show no
  value at all without custom JS).
- **`git init` may create branch `master`**: if `git push -u origin main`
  says "src refspec main does not match any", run `git branch -m master main`
  first.
- **Push without token in URL fails with "could not read Username ... No such
  device or address"** — not a hung prompt. Set tokenized URL
  (`https://<user>:<TOKEN>@github.com/...`) right before push, strip right
  after (`git remote set-url origin <clean>`).
- **New scenario types (maritime/air) must use the SAME dispatch pattern** —
  `_impact_dispatch()` in simulation.py needs the new enum values to map to
  `ImpactModel.maritime()` / `.air()` methods, AND resource_allocator must
  pass the new params (`maritime_threat`, `enemy_units`, `air_threat`,
  `enemy_aircraft`) — missing any → `KeyError` at runtime, not at compile.
  Test each new type with a curl call before committing.
- **Preset scenarios** (dropdown on frontend) auto-fill many fields but the
  backend `SimulateRequest` must have `Optional` defaults for ALL maritime/air
  params so a `conflict`-only payload doesn't fail Pydantic validation — and
  vice versa: maritime/air payloads must NOT require earthquake_* fields.
- **Frontend JS must not use ES-module `export`** — if you switch the JS files
  to use `export {}`, the browser throws "Unexpected export" (the `<script src>` tags
  have no `type="module"`). Keep namespace objects (`const API = {...}`) or IIFEs.
- **Foreground terminal rejects `&` backgrounding for servers** — use
  `terminal(background=true)` + follow-up calls.
- **Impact model return variable mismatch**: when adding a new scenario type, the
  `combined()` method returned `affected` but the caller unpacked `total_affected`.
  py_compile won't catch this — only a live curl test does. Pattern: always test
  each new `disaster_type` value via live POST before committing. The error surfaces
  as `"Gagal memproses simulasi: name 'X' is not defined"` at the API level.
- **Walrus operator in return tuple**: a line like
  `esc = a * b * (1 + x / 10 * 0.5 if (x := y) else 1)` looks clever but fails
  with NameError on the default branch when the variable isn't pre-bound. Keep
  pre-binding explicit: `cap_mult = cap_mult_val or 1.0`.
- **Historical data as frontend dropdown**: when adding a JSON dataset (e.g. 45 wars)
  that the user picks from, (a) add a `GET /api/v1/<resource>` endpoint serving the
  data, (b) add `fetch<Resource>()` to `api.js`, (c) populate `<select>` on load,
  (d) on `change`, auto-fill form fields + center map. This pattern reuses across
  any "pick from database → auto-fill form" UX — not specific to wars.
- **Combined/multi-matra dispatch**: adding a `combined` type that invokes multiple
  single-matra methods simultaneously requires: (a) `combined` in the `DisasterType`
  enum, (b) a `combined()` method in the impact model that calls conflict+maritime+air
  internally, (c) `resource_allocator` conditional blocks for each sub-matra,
  (d) `decision_engine` accepts `combined=True` flag to emit cross-matra coordination
  actions (Kogabwilhan), (e) `_impact_dispatch()` in simulation.py maps the new type.
  All five sites must be updated — missing any one produces a runtime error.

- **Adding many disaster types (26+ bencana Indonesia) — 5-site update + smoke
  test**: when the user gives a full disaster list (tsunami, letusan gunung api,
  tanah longsor, angin puting beliung, kekeringan, kebakaran hutan/gedung/
  permukiman, wabah, pandemi, terrorisme, demo, ...), the enum grows to ~30
  values. Update ALL sites: (1) `schemas.py` enum + Optional request params with
  defaults, (2) `impact_model.py` — one method per type (reuse a `_generic()`
  helper for types without unique physics: `severity` drives affected/deaths/
  damaged; unique formulas for tsunami wave-height, volcano VEI tables, forest
  fire area×fuel×wind, pandemic mortality), (3) `_impact_dispatch()` dict,
  (4) `resource_allocator` block, (5) `decision_engine` template. Frontend too:
  `<select>` options + per-type param sections + `buildPayload()` branches.
  **Smoke-test every enum value**: write `tests/test_all_types.py` that loops
  ALL disaster types with a minimal payload and asserts HTTP 200 + sensible
  numbers — 31/31 PASS before committing. py_compile alone NEVER catches a
  missing dispatch/allocator/engine branch. Keep it as a permanent test file.
- **Port change across dual repos (Docker + Monolith)**: user asks \"ganti port
  8000 → X\". Update in BOTH repos, not one:
  - Docker repo: `Dockerfile` (EXPOSE + CMD + HEALTHCHECK), `docker-compose.yml`
    (`${APP_PORT:-X}:X` host AND container side must match CMD), `backend/main.py`
    CORS origins, `.env.example`, `README.md` all refs.
  - Monolith repo: `installer/*.service` (ExecStart + Environment), `installer/install.sh`
    (port + printed URLs), `backend/main.py` CORS, `.env.example`, `README.md`.
  Use `sed -i 's/8000/X/g'` per file set, then `grep -rn 8000` must return nothing.
  Nasty trap: a careless sed on compose can produce
  `"0.0.0.0:${APP_PORT:-X}":X"` (broken quote / bad YAML) — re-run the YAML
  parser after every compose edit. Verify with live uvicorn on the new port
  (health + simulate + static) and confirm the OLD port no longer serves.
- **Two-repo sync discipline (Docker vs Monolith)**: new features live in ONE
  source dir, then sync to sibling:
  ```bash
  for d in backend frontend tests; do rm -rf "$MONO/$d" && cp -r "$SRC/$d" "$MONO/$d"; done
  ```
  Then strip monolith-only exclusions: `rm -rf "$MONO/backend/__pycache__"`
  and `"$MONO/frontend/assets/tiles"/[0-9]*` (keep `.gitkeep` — gitignore has
  `frontend/assets/tiles/*` + `!frontend/assets/tiles/.gitkeep`). Never copy
  Dockerfile/docker-compose into monolith. IDENTICAL commit message for both
  pushes makes verification (`git log` vs GitHub API) trivial. Check
  `git status --short` on both before push.

## README (tutorial) standards — user expects ALL of these

- Indonesian (Bahasa), full TOC, BOTH install paths (Docker = primary, venv =
  dev), "Cara Pakai" with 2-3 concrete named scenarios, project structure tree,
  API endpoint + example curl + sample JSON response, formulas/domain-logic
  section, limitations/roadmap table, MIT license line. **The user reads the
  formulas** — document model math, not just usage.

## Verification before declaring done

- `docker compose` YAML check (see docker-compose-scaffolding for the uv-venv
  fallback when pyyaml is absent)
- py_compile all green
- live uvicorn: health + each scenario endpoint + static files all 200
- GitHub push + Contents API listing per github-token-deploy-workflow
- `.env.example` placeholder-only, `.gitignore` excludes `.env` — grep the
  pushed raw files for real secrets before telling the user it's clean

## References

- `references/disaster-dss-domain-model.md` — empirical formulas + resource
  ratios for the disaster/conflict decision-support app (MMI curves,
  depth-damage curves, escalation factors, SPHERE/BNPB ratios, MILITER maritime/air
  ratios, preset skenario Indonesia). Reuse for "berapa pasukan/bantuan/tindakan"
  questions or Phase 2 ML work. Now covers the full 26-bencana+5-operasi set:
  generic severity model, tsunami wave-height tiers, volcano VEI 0-8 table,
  forest-fire area×fuel×wind, kebakaran/wabah/sosial decision templates.
- `templates/simulate-request-example.json` — example payload for the
  `POST /api/v1/simulate` endpoint (earthquake).
- `scripts/test_all_disaster_types.py` — smoke-test that POSTs every
  DisasterType enum value (31 types) with a minimal payload against a live
  server and reports OK/FAIL per type. Run after ANY change to schemas /
  impact_model / dispatch / allocator / engine — py_compile never catches a
  missing branch.

## Related Skills

- `github-token-deploy-workflow` — PAT push mechanics + security hygiene
- `docker-compose-scaffolding` — compose validation, upstream-repo verification, generate-env.sh
- `docker-development` — Dockerfile best practices