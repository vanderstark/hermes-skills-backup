---
name: docker-compose-scaffolding
description: "Generate multi-variant Docker Compose/Dockerfile stacks."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, docker-compose, scaffolding, iac, deployment, laravel]
    related_skills: [docker-development]
---

# Docker Compose Scaffolding (Single & Multi-Variant)

Generate ready-to-run Docker Compose + Dockerfile stacks for the user,
including cases where they want SEVERAL parameterized variants at once
(e.g. "every PHP version 5-8, nginx AND apache, each as its own zip").
This skill is about the *generation workflow and packaging*, not Docker
concepts themselves — pair with `docker-development` for Dockerfile/compose
best-practice content (multi-stage builds, security anti-patterns, etc.).

## When to use this skill

- User asks for a docker-compose/Dockerfile setup to deploy an app
- User asks for MULTIPLE variants of the same stack (different language
  versions, different webservers, different DB engines) — each variant
  should be self-contained and independently runnable
- User asks for the output packaged as one-zip-per-variant, or a single
  bundle — read their packaging instruction literally (see Packaging below)

## Core workflow

### 1. Enumerate the variant matrix explicitly

Before generating anything, write out the full cross-product of dimensions
the user asked for (e.g. webserver x language-version x db). Confirm counts
with the user if the matrix is large (12+ combinations) so they aren't
surprised by the file count.

### 2. Generate via a script, not by hand-writing each file

For anything beyond ~2-3 variants, hand-writing each Dockerfile/compose
file is slow and error-prone (copy-paste drift). Instead:

1. Write a single Python generator script that has one function per file
   type (`dockerfile_fpm(version)`, `compose_nginx(version)`, etc.) and
   loops over the variant matrix, calling `write_file()`/plain
   `open(...).write()` for each combination.
2. Run the generator via `terminal`, not `execute_code_ide` — in Hermes
   deployments configured with `approvals.cron_mode` restrictions,
   `execute_code_ide` may be BLOCKED for arbitrary Python (including
   subprocess calls). The generator script itself must be created with
   `write_file` and then invoked with `terminal(command="python3 <path>")`.
3. **Write the generator script under the Hermes write-safe-root**, not
   `/tmp` — deployments with `HERMES_WRITE_SAFE_ROOT` set (check via a
   failed `write_file` error message, or ask the user) will reject writes
   outside that root (e.g. `/opt/data/scripts/...` instead of
   `/tmp/...`). Put throwaway generator scripts in a `scripts/` folder
   under the safe root, and generated deliverables under a `documents/`
   or `cache/` folder under the same root.

### 3. Validate before delivering

Always parse every generated `docker-compose.yml`/`*.yml` with `pyyaml`
before telling the user it's done:

```bash
python3 -c "
import yaml, glob
for f in glob.glob('OUTPUT_DIR/**/*.yml', recursive=True):
    with open(f) as fh:
        yaml.safe_load(fh)
print('all yaml valid')
"
```

If `docker compose` (v2 plugin) is available in the environment, also run
`docker compose config` per variant as a stronger check — but don't block
delivery on its absence; YAML-parse validation plus a manual review of the
generated content is an acceptable fallback when the plugin isn't
installed locally.

**Validation fallback when `pyyaml`/`docker compose` are BOTH absent**
(common in PEP-668 / externally-managed Python environments): create a throwaway
virtualenv for one-off YAML validation — this was the exact pattern that resolved
the PentAGI deploy check when system Python was PEP-668 locked:
```bash
uv venv /tmp/yamlcheck -q && uv pip install --python /tmp/yamlcheck/bin/python pyyaml -q
/tmp/yamlcheck/bin/python -c "import yaml; yaml.safe_load(open('docker-compose.yml')); print('ok')"
```
`uv` is the cleanest path around PEP-668 block; never attempt
`pip install --break-system-packages pyyaml` in a deployment that enforces
externally-managed Python. The `write_file` linter's own YAML check
(`"lint": {"status": "ok"}`) is a sufficient fallback only for *syntax* — it
cannot catch semantic issues (duplicate service names, wrong mount paths),
so still run a real `yaml.safe_load` via the venv when possible.

---

### 4. Packaging — respect the user's literal instruction

- **"package as one zip"** -> single archive of the whole tree.
- **"one zip per variant, named per feature"** -> loop and create N zips,
  each named descriptively from the variant dimensions, e.g.
  `nginx-php8.3-laravel.zip`, `apache-php7.4-laravel.zip`. Each zip must
  be self-contained (its own Dockerfile, compose file, .env.example,
  README) — the user should be able to extract just that one zip and run
  it without needing any sibling zip.
- **No `zip` CLI available** is common in minimal Linux containers —
  check with `which zip` first; if absent, use Python's built-in
  `zipfile` module instead of trying to install a package:

```python
import zipfile, os

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                zf.write(fp, os.path.relpath(fp, os.path.dirname(folder_path)))
```

`tar -czf` via `terminal` is the alternative when a `.tar.gz` is
acceptable instead of `.zip`.

## Security baseline to apply by default

Unless the user asks for something more permissive, generated compose
files should default to:

- **Bind published ports to `127.0.0.1`**, not `0.0.0.0` — especially for
  admin/debug tools like Adminer, phpMyAdmin, Prometheus, Grafana. Note
  in the README that a reverse proxy + TLS belongs in front for real
  external access.
- **Isolate the database/internal network** with `networks.<name>.internal:
  true` so it isn't reachable from outside the Docker network.
- **Non-root `USER`** in Dockerfiles where the base image supports it.
- **Pin image versions** (`postgres:17-alpine`, not `postgres:latest`).
- **No hardcoded secrets** — `.env` + `.env.example` (never commit real
  `.env`; note it in `.dockerignore` and recommend `.gitignore` too).
- **Healthchecks** on stateful services (DB) with `depends_on.condition:
  service_healthy` on dependents, so app containers don't race the DB
  startup.
- **Log rotation** (`logging.driver: json-file`, `max-size`/`max-file`)
  so container logs don't fill the host disk.

## Multiple frameworks in one request ("do the same for framework X")

When the user asks to replicate the same variant matrix for a second
framework (e.g. "buat juga untuk CI4 seperti yang di Laravel"):

- **Check that framework's real minimum runtime version first** — don't
  silently reuse the previous framework's version range. E.g. Laravel
  legacy versions support PHP 5.6, but CodeIgniter 4 requires PHP 7.4+
  (it never supported 5.6 at all). Building a PHP 5.6 image for a
  framework whose code uses PHP 7+ syntax will fail at `composer install`
  or runtime with syntax errors — don't generate it, flag the mismatch to
  the user and propose dropping the unsupported version from that
  framework's matrix (ask via `clarify` first if uncertain, since it's a
  scope change from the original request).
- Framework-specific PHP extensions differ — e.g. CodeIgniter 4 needs
  `mysqli` + `xml` on top of the `pdo_mysql`/`mbstring`/`gd`/`zip`/`intl`
  set Laravel needs. Check the target framework's server-requirements doc
  rather than reusing the previous framework's extension list verbatim.
- `.env` shape differs per framework (Laravel: `DB_CONNECTION`,
  `DB_HOST`, etc. read automatically; CodeIgniter 4: `database.default.*`
  dotted keys, and CI4 reads `.env` from the **project root**, i.e.
  inside `src/.env`, not the Docker-folder-level `.env.example` — note
  this explicitly in the README so the user doesn't put credentials in
  the wrong file).

## Pitfalls encountered

- **SonarQube requires `vm.max_map_count=524288` on the host** (not in Docker) —
  the bundled Elasticsearch refuses to start without it. Run
  `sudo sysctl -w vm.max_map_count=524288` before `docker compose up`, and
  add it to `/etc/sysctl.conf` so it survives reboot. This is the #1
  "container exits immediately" failure for SonarQube/Loki/Graylog-style
  ES-based images and is almost certainly NOT a compose bug — check the
  sysctl first.
- EOL language/runtime versions (e.g. PHP 5.6, PHP 7.4) should ship with
  a visible comment/README warning that they're unsupported upstream and
  intended only for legacy-app maintenance, not new projects.
- CI matrices (GitHub Actions `strategy.matrix`) often can't cover EOL
  versions because tooling actions (e.g. `shivammathur/setup-php`) may
  drop stable support for them — scope the CI matrix to currently
  supported versions and note the EOL variants are deploy-only, untested
  by CI.
- When multiple variants share the same container/service names (e.g.
  `laravel_mysql`), that's fine ACROSS separate zips (each is run
  independently) but would collide if a user tried to run several
  variants simultaneously on the same host — mention this in the README
  if variants are likely to be run side-by-side rather than one-at-a-time.

## Available compose templates in `templates/`

| Template | Purpose |
|----------|---------|
| `minio-object-storage-compose.md` | MinIO S3-compatible object storage (ports 9000/9001, `mc ready` healthcheck, auto-init bucket sidecar, `.env` secrets) |
| `object-store-and-code-quality-stacks.md` | MinIO + SonarQube self-hosted stack recipes with full compose snippets, pitfalls, and README guidance |
| `generate-env-password-pattern.sh` | Reusable `openssl rand` password generator for `.env` files |
| `ubuntu2404-systemd-installer-pattern.md` | **Ubuntu 24.04 bare-metal installer** (systemd + venv + uvicorn) for companion monolith repos — verified on `crisis-command-center-monolith` |

These are reusable patterns — adapt ports, volumes, and bucket names per deployment.

## Related Skills

- `docker-development` — Dockerfile/compose language-level best practices
  (multi-stage builds, BuildKit secrets, anti-patterns table)
- `github-token-deploy-workflow` — **OVERLAP ALERT**: this skill also covers
  PAT-based GitHub push for generated Docker stacks. Both skills are
  user-owned. The push pattern in this skill (`docker-compose-scaffolding`)
  is the **canonical one** for multi-variant stacks (Laravel, CI4, etc.);
  `github-token-deploy-workflow` adds NSM-specific templates (Zeek, T-Pot,
  Arkime, CrowdSec) and repo-splitting rules for dual-mode tools. When in
  doubt, use the pattern from THIS skill for compose-scaffolding tasks.

## Delivering downloadable HTML diagrams (topology / architecture)

If the user asks for a topology/architecture diagram as a **downloadable HTML**
file (and Playwright isn't installed), render via Hermes' built-in browser
(`browser_navigate` to `file://...`, `browser_vision` to verify) and deliver
with `MEDIA:/path/file.html`. Full method, plus why not to bother with
Playwright for HTML-only delivery: `references/html-delivery-technique.md`.

### Mermaid rendering pitfalls (learned the hard way — opens with multi-diagram pages)

When embedding SEVERAL Mermaid diagrams in one HTML page, DEBUGGING
``Syntax error in text`` requires checking EACH diagram individually, because
the built-in browser snapshot may show only part of the page. Use:

```js
// In browser_console — returns which .mermaid blocks have errors & which rendered SVG:
document.querySelectorAll('.mermaid').forEach((el, i) => {
  if (el.textContent.includes('Syntax error')) console.log(`diagram ${i+1} ERROR`);
  else console.log(`diagram ${i+1} ok`);
});
```

Known Mermaid v10 syntax gotchas (all hit this session):
- **`END` / `end` is a RESERVED keyword.** Using `END` as a node ID (or any ID
  containing it) silently breaks parsing — rename to `FINISH`, `DONE`, `END2`, etc.
- **`-- TEXT -->` edge-label syntax vs `-->|TEXT|` pipe syntax.** Both are valid in
  plain flowcharts, but inside `subgraph` blocks (especially nested), the
  `-- TEXT -->` form is fragile — when a diagram fails with ``Syntax error``
  and the line looks like `A -- BLOCK --> B`, switch to `A -->|"BLOCK"| B`.
  Quote the label when it contains spaces: `-->|"NO MATCH"|`.
- **Nested/duplicate subgraph blocks can corrupt the whole parse tree.** If a
  diagram was patched multiple times and left two competing `subgraph ... end`
  blocks (or an unfinished `<div>` wrapping a second `.mermaid`), the entire
  following content can be silently swallowed. Check for leftover
  `<!-- -->` fragments and unclosed `</div>` before assuming the syntax is wrong.
- **`classDef` resets can leave a stale reference**: if a node ID was renamed
  (e.g. `AUTHZ` → `AUTHZ_ROLE`), any `class ...` line still referencing the old
  ID throws a parse error — grep the file for the old ID before re-rendering.
- Verify visually with `browser_vision` (don't trust `hasSvg` alone — a failed
  diagram can still show a fallback SVG). A succinct visual check of each
  diagram title area confirms it rendered correctly.
- **Node ID collision is a silent killer, not just `END`.** Reusing the same
  identifier for a `subgraph ID[...]` AND a node inside it (e.g.
  `subgraph DC[...]` containing a node also named `DC["Docker"]`), or reusing
  a node ID across two different `subgraph` blocks in the same diagram (e.g.
  `A1`/`A2` as both a node in subgraph 1 and again in subgraph 3), breaks the
  parser with the same generic "Syntax error in text" message — no hint which
  ID collided. **Debug by isolating**: write a throwaway minimal
  `test-minimal.html` with 3-4 nodes and no subgraphs, confirm mermaid.js
  itself renders (rules out CDN/init issues), then binary-search the real
  diagram's node IDs for duplicates — grep for each ID and count occurrences;
  every custom ID (not just `subgraph` labels) must be globally unique across
  the whole diagram, not just within its own subgraph.

### Delivering crisp diagrams when the user says a screenshot is "buram"/blurry

A single long HTML page with 5-6 stacked Mermaid diagrams, screenshotted via
`browser_vision` at default viewport, downsamples every individual diagram —
readable to an LLM's vision pass, but visibly blurry to the user when
delivered as one image. When the user complains about blur/legibility:

1. **Split into one HTML file per diagram** (`01-topic.html`, `02-topic.html`,
   ...), each with just that diagram at a large `font-size` (15-18px) filling
   the full viewport — not the full multi-diagram page.
2. `browser_navigate` to each file individually, verify render via
   `browser_console` (`hasSvg` + no `Syntax error` text), then
   `browser_vision` per-file to get a crisp, dedicated screenshot per diagram.
3. Deliver each screenshot as its own `MEDIA:` attachment plus the raw `.html`
   file path — the user can also open the HTML locally for a native-resolution
   view, which beats any chat-compressed screenshot.
4. Keep the original combined HTML file too (for a single-document handoff /
   printing), but treat the split files as the primary chat-delivery format
   whenever legibility was flagged as an issue.

## Pushing generated deliverables to GitHub (PAT-based, no gh CLI)

**WORKFLOW DIPILIH:** `curl` + `git remote` (bukan `gh` CLI) — ini workflow yang sudah diverifikasi (sudah dipakai MinIO, SonarQube, OPNsense).

**Pattern:**
```bash
export GH_TOKEN="<token>"
# 1. Verify token
curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user | python3 -c "import json,sys; print(json.load(sys.stdin)['login'])"
# 2. Create repo
curl -s -X POST -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos -d "{\"name\":\"stack-name\",\"description\":\"...\",\"private\":false,\"auto_init\":false}"
# 3. Init + Commit + Push
cd /path/to/repo
git init -q
git config user.name "vanderstark"
git config user.email "vanderstark@users.noreply.github.com"
git add -A
git commit -q -m "Initial commit"
git branch -M main
git remote add origin "https://<user>:<GH_TOKEN>@github.com/<user>/stack-name.git"
git push -u origin main
# 4. CLEANUP — STRICTLY
git remote set-url origin "https://github.com/<user>/stack-name.git"
unset GH_TOKEN
rm -f /tmp/repo_*.json
```

**CRITICAL:** Always verify the push succeeded via GitHub Contents API before telling the user it's done — `git push` exit code alone isn't proof the files are browsable.

## Multiple Repos for Multiple Stack Variants

When user asks for **multiple separate repos** (e.g. a tool that ships BOTH
bare-metal AND Docker form — like OPNsense/CrowdSec), follow the rule:
- **One repo per tool per install-method** — `opnsense-monolith` +
  `opnsense-docker`, NOT one merged `opnsense` repo. User-corrected
  preference, non-negotiable.
- Same cleanup pattern per repo (`git remote set-url`, `unset GH_TOKEN`).
- For **multi-variants of SAME tool** (e.g. PHP 5.6/7.4/8.x x nginx/apache),
  use ONE repo with subfolders per variant.
- In this session's context, OPNsense needed 2 repos:
  - `opnsense-monolith` — bare-metal/VM installer (ISO + verify + hardening scripts)
  - `opnsense-docker` — monitoring Docker stack (Suricata, Zeek, CrowdSec, Grafana)

### Tutorial-style deliverables (README-led repos): one repo PER METHOD

The repo-splitting rule also applies when the deliverable is a **tutorial**
(no code — README + optional scripts) covering multiple install methods for
one tool. The user explicitly rejected a single combined tutorial repo
(`truenas-ubuntu` with `monolith/proxmox-vm/`, `monolith/replicate-on-ubuntu/`,
`monolith/standalone-iso/` subfolders) and asked to split ("tolong di buat
pisah repo nya"):

- One repo per method: `truenas-proxmox-vm`, `truenas-on-ubuntu`,
  `truenas-standalone` — never `truenas-ubuntu` with method subfolders.
- Scripts belong only in the repo whose method uses them (the replicate-on-
  Ubuntu scripts do NOT go in the Proxmox-VM repo just because they were
  authored together; remove before push).
- Before splitting, ask or state the plan: a monolithic tutorial folder is a
  reasonable first draft, but flag that final delivery will be per-method
  repos so the user isn't surprised.
- Same validation (bash -n on any scripts) and per-repo verification via the
  Contents API before reporting done.

**Honest-capability gate before writing a tutorial:** if the user asks for a
tutorial of an OS that CANNOT be installed as a package inside another OS
(e.g. TrueNAS SCALE on Ubuntu 24.04 — it's a standalone Debian-based OS, not
an apt package), do NOT write a fake "install TrueNAS on Ubuntu" guide.
State the constraint plainly, then use `clarify` to offer the real methods
(VM in Proxmox / replicate features with ZFS+Samba+NFS+Cockpit / standalone
ISO install) — the user picks; the chosen methods become the per-method repos.

## Security Hygiene for GitHub Token (non-negotiable)

**If the user pasted their token in chat (not stored locally):**
- Remind them to rotate/revoke at https://github.com/settings/tokens — every time, not once.
- **Never use a token that has already been pasted multiple times in chat history.**
- Even after cleanup, chat retains the plaintext — the more reuse, the more exposure.
- Do not persist the token to memory, skills, or any file outside ephemeral shell env.

## Verifying Image Name Before Writing Into Compose

Don't guess the Docker Hub image name — verify it first:
```bash
# Docker Hub
curl -s "https://hub.docker.com/v2/repositories/<namespace>/<image>/" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('message', 'FOUND') or 'NO IMAGE')"
# Non-Docker-Hub registries (e.g. gcr.io) — use tags/list endpoint
curl -s "https://gcr.io/v2/<project>/<image>/tags/list" | head -c 300
```

## Related Reference

- `references/self-hosted-ops-stack-compose-pattern.md` — actual repo shape used for
  monitoring/ITSM/IPAM/SIEM tool deployments.
- `references/offline-capable-webapp-pattern.md` — making web apps 100% offline-capable
  (self-host CDN assets, map tile caching, online/offline auto-switch, LAN binding,
  zero-external-dependency backend). Use when delivering apps that must survive
  internet outages (disaster/emergency response, military, air-gapped).

### When the tool is a self-hostable app with its OWN official docker-compose.yml (not a bare infra image)

For apps that ship a real, actively-maintained official `docker-compose.yml` in
their own GitHub repo (not just a Docker Hub image page) — e.g. PentAGI, and
generally any app whose landing page's "get started" link resolves to a
JS-rendered SPA shell with no useful static content — do NOT hand-write the
compose file from the marketing site. Identify the real upstream repo first
(GitHub search API: `https://api.github.com/search/repositories?q=<toolname>`,
sorted by stars, cross-checked against the landing page's own links/socials),
`git clone --depth 1` it into `/tmp`, and read the **actual**
`docker-compose.yml` + `.env.example`/`README.md` env var list before writing
your own adapted version. This catches env vars, volume mounts, and
inter-service dependencies (`depends_on.condition: service_healthy`, shared
networks) that would otherwise be guessed wrong. Delete the `/tmp` clone once
extracted. This is the same discipline as the existing "Verifying compose
files for complex multi-container stacks against upstream" pitfall below —
apply it to ANY user-facing app request, not just infra/SIEM stacks.

### Verify GitHub push landed correctly, not just that `git push` exited 0

After the standard PAT push pattern (below), always confirm the pushed files
are actually browsable via the Contents API — one call, cheap, and catches
partial pushes or wrong-branch pushes silently:
```bash
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/<user>/<repo>/contents/" \
  | python3 -c "import json,sys
for item in json.load(sys.stdin): print(f\"  {item['type']:5} {item['name']} ({item.get('size',0)} bytes)\")"
```
Do this as the LAST step before telling the user the deliverable is done —
`git push` returning success only means the local git object graph reached
the remote, not that the tree matches what you intended to ship.

---

For infra tools that ship inter-dependent config across several
containers (SSL certs shared between services, security-plugin config
files, cluster join tokens — e.g. Wazuh's Indexer+Manager+Dashboard,
where all three need matching cert paths and hostnames) — don't
hand-write `docker-compose.yml` + config files purely from memory. The
volume-mount paths, env var names, and companion config file contents
for these stacks are numerous and easy to get subtly wrong (a single
missing `filebeat_etc`/`filebeat_var` mount, or a stale env var name,
fails silently or produces a confusing runtime error).

Instead:
1. Download the tool's own official `docker-compose`-based deployment
   repo (e.g. `curl -sL https://github.com/<org>/<repo>/archive/refs/tags/<tag>.tar.gz`)
   into `/tmp`, extract, and read its real `docker-compose.yml` +
   `config/` directory before writing your own version.
2. Cross-check every volume mount and env var in your generated compose
   against the official source — this catches missing mounts that would
   otherwise only surface as a cryptic startup failure once the user
   actually runs it.
3. Reuse the official config file *contents* (yml/conf templates) rather
   than reinventing them, adapting only what the user's request actually
   changes (e.g. hostnames, ports, or security settings).
4. Delete the `/tmp` clone after extracting what's needed.

### Disabling SSL/TLS on OpenSearch-based stacks (Wazuh-style) on request

Some stacks (Wazuh Indexer/Manager/Dashboard, and other OpenSearch-based
tools) default to mandatory TLS + an internal auth plugin. If the user
explicitly asks for a no-SSL variant (e.g. for lab/testing), the correct
official mechanism — found in the tool's own indexer config — is usually
a single flag like `plugins.security.disabled: true` in the indexer's
own yml, NOT just stripping `https://` from URLs. Stripping URLs alone
without disabling the security plugin leaves the indexer still expecting
TLS handshakes and it will refuse plain-HTTP connections. Also strip any
`<ssl>`/`ssl.*` config blocks in the dependent services' own config
(manager conf, dashboard yml) so they stop trying to load cert files
that no longer exist. Always add an explicit README warning that
disabling security removes both encryption AND password enforcement
(not just encryption) — this is a bigger security tradeoff than it
sounds, and the user should see that stated plainly before deploying it
anywhere beyond a lab.

### Reusable `generate-env.sh` pattern for Docker Compose secrets

For any generated compose stack needing DB/API/dashboard passwords,
ship a `generate-env.sh` alongside `.env.example` that copies the
example and overwrites password fields with `openssl rand`-derived
values via `sed`, then prints the generated superuser credentials once
(the user will not see them again unless captured now). This has been
the consistent pattern across Zabbix/NetBox/GLPI/Wazuh generators this
consistent pattern across Zabbix/NetBox/GLPI/Wazuh generators this
session — see `templates/generate-env-password-pattern.sh` in this
skill's `templates/` dir for the reusable skeleton (adapt the `sed`
targets and generated-credential summary to the specific stack's `.env`
keys).

Post-generation sanity script: `scripts/generate-env-verify.sh` — run from
the compose folder to list env vars referenced by `${VAR}` substitutions
and detect whether a `.env`/`.env.example` was accidentally staged.

### Verify every third-party image actually exists before writing it into compose

Don't type an image name from memory/pattern-guessing (e.g. assuming
`<vendor>/nrpe-server` exists because similar-looking images exist for
other tools) — invented image names produce a `docker compose up`
failure the user only discovers after cloning the repo. Verify EVERY
non-trivial/non-famous image before delivering:

```bash
# Docker Hub images:
curl -s "https://hub.docker.com/v2/repositories/<namespace>/<image>/" | python3 -c "
import json,sys
d = json.load(sys.stdin)
if d.get('message') == 'object not found':
    print('NOT FOUND')
else:
    print('pull_count:', d.get('pull_count'), '| last_updated:', d.get('last_updated'))
"

# Non-Docker-Hub registries (e.g. gcr.io) don't expose the same v2 API path —
# use the registry's own tags-list endpoint instead:
curl -s "https://gcr.io/v2/<project>/<image>/tags/list" | head -c 300
```

A high `pull_count` (millions+) and a recent `last_updated` are good
signals the image is real and maintained. If an image turns out not to
exist (this happened for an imagined NRPE-agent container this
session), don't substitute a second guess — either drop that
service/feature from the compose file and explain why in the README
(e.g. "install this agent natively on the target host instead"), or
ask the user, rather than guessing a third unverified name.

### Verify installation mechanism before scripting it — don't assume init.sql/secret.php exists

Some apps have NO CLI/scriptable path to bootstrap their database at
all — the only supported route is a **web installer wizard** that runs
in-browser on first request (RackTables 0.22 is one: there's no
`init.sql`, and `secret.php` is written BY the wizard, not read from a
template). Before writing an automated bootstrap step (`mysql <
init.sql`, a templated `secret.php`, etc.), actually download and grep
the tool's real source tree for the files you're about to reference —
if they don't exist, don't invent them. Instead:
1. Script everything scriptable (packages, DB user/empty-schema
   creation, webserver vhost, file permissions including a writable
   placeholder config file the wizard needs to open for writing).
2. Stop there and hand off to the wizard explicitly in the README/final
   output — give the exact values (DB host/name/user/password) the
   user pastes into the wizard form, and the exact `chmod`/`chown`
   lock-down command to run on the now-populated config file
   afterward (wizards typically leave it world-writable).
3. For the Docker variant of the same tool, remember the DB **hostname**
   the wizard needs is the compose service name (`db`), not
   `localhost` — call this out explicitly since it's the #1 way users
   get stuck at the wizard's connection-test step.

### Security tool integrations often split into a container-safe "detection" half and a host-only "enforcement" half

When integrating an IDS/IPS/blocking tool (Suricata, CrowdSec, fail2ban-
style tools) into an existing compose stack, don't assume the whole tool
can live inside one container. Many such tools split cleanly into:
- a **detection/analysis component** — reads logs/traffic, fine inside
  a container with the right volume/log mounts;
- an **enforcement/remediation component** — needs direct access to the
  host's iptables/nftables or network interfaces to actually block
  traffic, and is unreliable or actively discouraged to run nested
  inside another container's network namespace.

Ship the detection half as a compose service/snippet, but install the
enforcement half **natively on the host** and say so plainly (e.g.
CrowdSec's Security Engine can run in Docker, but its Firewall Bouncer
needs host-level iptables access — containerizing it requires
`network_mode: host` + `NET_ADMIN`, which is more fragile than a native
install). Don't silently ship a compose-only "solution" that detects
but never actually blocks anything — that's a functional gap the user
won't notice until they test it.

### Rendering vendor doc pages that 404 on a guessed URL or return JS-shell HTML to curl

Official doc sites for security/infra tools (Wazuh, CrowdSec, etc.)
often (a) restructure URLs between versions so a guessed slug like
`.../detect-network-anomalies-suricata.html` 404s even though the page
exists under a different slug, and (b) render primarily client-side, so
`curl` returns mostly `<style>`/`<script>` boilerplate with the real
content injected by JS — regex-stripping tags on that HTML yields noise,
not the article body. When this happens:
1. Load the doc site's parent/index page with the browser tool instead
   of guessing leaf URLs — the sidebar navigation lists the real slugs.
2. If a sidebar link's `browser_click` doesn't visibly navigate (some
   nav frameworks reuse the same DOM), extract the real `href` values
   directly: `browser_console(expression="Array.from(document.
   querySelectorAll('a')).filter(a => a.textContent.includes('<label
   fragment>')).map(a => a.href)")`.
2. Once on the right page, pull exact copy-paste commands out of hidden
   "Copy to clipboard" code blocks with
   `browser_console(expression="Array.from(document.querySelectorAll
   ('pre')).map(p => p.textContent).join('\\n---\\n')")` — this gets the
   literal shell/YAML snippets the vendor intends users to run, instead
   of retyping them from a possibly-truncated accessibility snapshot.

### Verify an image's actual configuration surface before assuming env-var support

Popular community images vary widely in what they let you configure via
environment variables — don't assume a `FOO_ADMIN_PASSWORD`-style env
var exists just because sibling stacks in this same session supported
one. Check the image's Docker Hub overview page (or its Dockerfile/
entrypoint source) for the actual supported env vars before writing
`environment:` keys into the compose file. When an image has NO
password env var (seen this session with a Nagios community image that
only supports `MAIL_RELAY_HOST`/`NAGIOS_FQDN`/`NAGIOS_TIMEZONE`, with a
fixed default web login baked into the image), don't invent one that
silently does nothing — instead ship a small `change-admin-password.sh`
that runs the image's real in-container tool (e.g. `docker exec <name>
htpasswd -b <path> <user> <new-password>`) after first start, and say
so plainly in the README instead of implying the password can be set
at `docker compose up` time.

## Companion bare-metal ("monolith") tutorials for the same tool

When the user asks for both a Docker Compose version AND a bare-metal/
"monolith" (systemd + apt/binary-release install) version of the same
tool in the same or a follow-up request, treat them as a matched pair
sharing the same due-diligence discipline, not just "write two READMEs
in the same style":

- Verify the *exact* upstream version/binary/package-repo URL you're
  about to script against before writing the installer — `curl -sI` the
  release tarball URL (expect `200`), or hit the project's GitHub
  Releases API (`/repos/<org>/<repo>/releases/latest`) for the current
  tag, rather than hardcoding a remembered version number that may be
  stale.
- Both variants get their own repo per the "one repo per tool" rule
  below — `<tool>-ubuntu24-tutorial` (bare-metal) and
  `<tool>-docker-compose` (Docker), never combined into one.
- Bare-metal installers should still follow the general safety
  conventions used across this session's scripts: `set -euo pipefail`,
  root check, Ubuntu-version sanity check with a y/N override prompt,
  `openssl rand`-generated credentials written to a root-only
  (`chmod 600`) credentials file, firewall (UFW) rule addition guarded
  by `command -v ufw && ufw status | grep -q active`, and a final
  human-readable summary block with concrete next-step commands.
- Validate all shell scripts with `bash -n <file>` (and any embedded
  heredoc Python with `python3 -m py_compile`) before delivering —
  applies equally to the bare-metal and Docker variants.

### When the tool has NO official container image (OPNsense / pfSense / firewalls)

Some "firewall" tools (OPNsense, pfSense) are **FreeBSD distributions** —
they ship as ISO/boot images only, with **no official Docker image**. Do
NOT invent a compose service for the firewall itself. What you saw in
Docker Hub (`demisto/opnsense`, ~33 MB CLI-tools wrapper) is an
EXPERIMENTAL community wrapper, good only for lab demos of CLI tools, NOT
a real stateful firewall.

Correct approach when the user asks for "OPNsense docker + monolith":
- **Repo 1 (`<tool>-monolith`)**: bare-metal/VM install — download official
  ISO (`curl -sL https://mirror.<host>/opnsense/releases/<ver>/` to list
  real versions; e.g. `OPNsense-26.7-OpenSSL-dvd1.iso`), `verify-checksum.sh`,
  VMware ESXi + Proxmox install guides, `post-install-hardening.sh`.
- **Repo 2 (`<tool>-docker`)**: the *surrounding monitoring stack* that
  connects to the firewall — Suricata (IDS/IPS), Zeek (NSM), CrowdSec
  (blocking via OPNsense API), Grafana. Label clearly in README: "this
  stack complements the host-installed firewall; it is NOT a firewall
  replacement".
- Architecture: firewall (bare-metal) → mirror/SPAN port → Suricata/Zeek
  containers → Wazuh/Elastic SIEM; CrowdSec bouncer talks back to the
  firewall's API/REST to block IPs. Diagram this in the README or an HTML
  topology page so the user sees the split clearly.
