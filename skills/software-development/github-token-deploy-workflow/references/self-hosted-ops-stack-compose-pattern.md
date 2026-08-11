# Self-Hosted Ops Tool Stack — Docker Compose Repo Pattern

Repeated pattern used across several sessions for deploying self-hosted
monitoring/ITSM/IPAM tools (Zabbix, LibreNMS, NetBox, GLPI, and similar
multi-container apps with DB + web + background workers) via Docker
Compose. Use this as the starting shape whenever a user asks for
"docker compose for X and put it on GitHub" for this class of app.

## Repo Shape

```
tool-docker-compose/
├── docker-compose.yml
├── .env.example        # placeholder creds, safe to commit
├── generate-env.sh      # copies .env.example -> .env, fills random secrets
└── README.md            # setup wizard steps, default creds, backup/update commands
```

## generate-env.sh Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail
cp .env.example .env
PASS="$(openssl rand -base64 24 | tr -d '=+/' | cut -c1-24)"
sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=${PASS}/" .env
# repeat sed per secret (SECRET_KEY, REDIS_PASSWORD, SUPERUSER_PASSWORD, etc.)
```

This avoids ever hand-typing/hardcoding a password into a file that
might get committed, and gives every deployment unique credentials by
default. For Django-style apps (NetBox) also generate a long
`SECRET_KEY`; for API-driven apps also generate an API token
(`openssl rand -hex 20`).

## Compose Conventions to Repeat

- All app/web ports bind `127.0.0.1:PORT:PORT` — never `0.0.0.0` by
  default; note in README that a reverse proxy + TLS is required for
  any external access.
- `networks: { <db-network>: { internal: true } }` for the DB tier so
  it's unreachable outside the compose network.
- `depends_on: <db>: condition: service_healthy` + a real `healthcheck:`
  on the DB (using the image's own healthcheck tool, e.g.
  `healthcheck.sh --connect --innodb_initialized` for MariaDB,
  `pg_isready` for Postgres, `mysqladmin ping` for MySQL) before
  app/worker containers start — not just "container started".
- Pin image tags (`postgres:16-alpine`, not `:latest`).
- `logging: { driver: json-file, options: { max-size: 10m, max-file: 3 } }`
  on every service to cap disk growth.
- Split Redis into separate task-queue vs cache instances when the
  upstream app recommends it (NetBox does) — don't share one Redis
  container for both roles if the docs say not to.
- Background job / worker containers get their own service definition
  (rqworker, dispatcher, housekeeping, etc.) rather than trying to run
  everything in the main web container.

## Exception: Tools That Need a Pre-Setup Step Before `docker compose up`

Most tools in this class follow `.env.example` + `generate-env.sh` +
`docker compose up` with zero extra steps (Zabbix, LibreNMS, NetBox,
GLPI all auto-migrate/auto-configure on first boot). **Wazuh does not**
— its Docker stack requires TLS certs and per-component config files
(`opensearch.yml`, `internal_users.yml`, `wazuh_manager.conf`) that must
exist before the first `docker compose up`, because Indexer/Manager/
Dashboard talk to each other over mandatory TLS from the first boot.

Pattern for this exception: ship a `setup.sh` that runs *before*
`generate-env.sh`/`docker compose up`, which:
1. Downloads the official `config/` tree + `generate-indexer-certs.yml`
   from the upstream project's own Docker repo (e.g.
   `github.com/wazuh/wazuh-docker` tag matching the image version) —
   don't hand-write these files, they're detailed and version-specific
   enough that a typo silently breaks TLS handshake with no clear error.
2. Runs the upstream's own cert-generator container
   (`docker compose -f generate-indexer-certs.yml run --rm generator`)
   to produce the actual cert/key pairs into `config/`.
3. Only after that succeeds does the normal `.env` + `docker compose up`
   flow apply.

Document in the README that one default credential (here, the Indexer
admin password) is **tied to a static bcrypt hash shipped in the
downloaded config**, so changing it isn't a simple `.env` edit — it
needs regenerating the hash via the image's own hash tool and editing
the YAML, while other passwords (API, Dashboard) remain freely
editable via `.env` alone. Call out which category each credential
falls into so the user doesn't try the wrong (broken) method.

Before writing this kind of `setup.sh`, actually fetch and inspect the
upstream repo's real directory layout (`curl -sL <tag>.tar.gz | tar -tz`
or a scratch clone) rather than assuming the layout from memory —
volume names and mount paths in these upstream composes shift slightly
between versions (e.g. a `filebeat_etc`/`filebeat_var` volume pair that
is easy to omit if drafting the compose from recall alone).

## Verify Third-Party Images Actually Exist Before Drafting the Compose

Don't write a `docker-compose.yml` service around an image name recalled
from memory/guessed convention (e.g. `<author>/<tool>-agent`) without
checking it's real first — invented image names look plausible but
silently don't exist. Verify via the Docker Hub API before committing
the name to the compose file:

```bash
curl -s "https://hub.docker.com/v2/repositories/<namespace>/<image>/" \
  | python3 -c "
import json,sys
d = json.load(sys.stdin)
if d.get('message') == 'object not found':
    print('NOT FOUND')
else:
    print('name:', d.get('name'), '| pulls:', d.get('pull_count'))
"
```

If the guessed image doesn't exist, don't substitute another guess —
either drop that service from the compose (documenting in the README
that the piece is handled natively instead, e.g. "NRPE agent installs
on the target host directly, not as a container — see the bare-metal
repo's `install-nrpe-agent.sh`") or find a real, high-pull-count image
and re-verify it the same way. Also worth double-checking the *env var
surface* of a real image via its Docker Hub overview page before
assuming password/config knobs exist — some maintained images (e.g.
`jasonrivers/nagios`) have no env var for setting the admin password at
container start at all.

## Exception: Images With No Password Env Var at Container Start

Some images (e.g. `jasonrivers/nagios`) ship a **fixed default
credential** (not a placeholder driven by env var) that can only be
changed by running the image's own credential tool *inside the running
container* after `docker compose up`, not via `.env`. Pattern for this:

1. `docker-compose.yml`/`generate-env.sh` for this tool do NOT attempt
   to inject a password via environment — say so explicitly in the
   script's own output so the user isn't left thinking the default
   credential was already replaced.
2. Ship a separate `change-<thing>-password.sh` that:
   - Checks the target container is actually running
     (`docker ps --format '{{.Names}}' | grep -q '^<name>$'`)
   - Runs the image's built-in credential-change tool via `docker exec`
     (e.g. `htpasswd -b <path> <user> <new-password>`)
   - Restarts the in-container service (or the whole container) so the
     change takes effect
   - Prints the new password once, with a note that it won't be shown
     again
3. README explicitly separates "credentials settable via `.env`" from
   "credentials requiring this post-start script" so the user doesn't
   try the wrong (silently ineffective) method for either.

## Variant: Deliberately Disabling a Stack's Default TLS/Auth

When a user explicitly asks for a "no SSL" revision of a stack that
enables TLS/auth by default (e.g. Wazuh Indexer's security plugin),
don't just delete cert volume mounts and hope — the upstream images
usually have one explicit config flag that turns the whole security
layer off cleanly (e.g. OpenSearch/Wazuh Indexer:
`plugins.security.disabled: true` in `opensearch.yml`, which disables
both TLS *and* password enforcement together, not just TLS alone). Find
and use that flag rather than partially stripping SSL-only settings,
and:
- Update every inter-service URL from `https://` to `http://` (Manager
  →Indexer, Dashboard→Indexer) to match — a stale `https://` pointing at
  a plaintext endpoint fails silently confusing.
- Strip the corresponding `<ssl>`/`ssl.*` config blocks that reference
  now-nonexistent cert files, not just leave them dangling.
- Put a loud, first-thing-in-the-README security warning stating that
  disabling the flag usually removes auth entirely (not just
  encryption) — a user asking for "no SSL" is very often thinking
  "skip the cert hassle" and not "also make the datastore
  passwordless", so this must be surfaced explicitly, not buried.
- Prompt for interactive confirmation in the setup script itself before
  applying the change (`read -rp "... Lanjutkan? (y/N)"`), since this is
  a meaningfully different security posture from the default.

## Variant: Personal Learning/CTF Lab Compose (Vulnerable-by-Design Targets)

When a user asks for "pentest/hacking tools" without a specific
authorized target, don't refuse outright and don't build offensive
tooling aimed at a real system — first `clarify` what they actually
mean (own asset / authorized client engagement / learning-CTF), then
route "learning" answers to a **local practice lab**, not raw attacker
tooling with no target. Compose shape for this:

- One service per vulnerable-by-design target (DVWA, OWASP Juice Shop,
  WebGoat, Metasploitable2 — all long-standing, intentionally-vulnerable
  community images) plus one attacker/tools box (`kalilinux/kali-rolling`
  with `nmap`/`sqlmap`/`nikto`/`gobuster`/`hydra` installed via the
  container's `command:` on first boot).
- Every port bound to `127.0.0.1` only, same as the ops-tool pattern
  above — a CTF lab is even more important to keep off any public
  interface than a monitoring stack.
- Ship a `start-lab.sh` (not a bare `docker compose up` in the README)
  that prints an explicit scope/legality warning and requires a
  `y/N` confirmation before starting — the boundary between "practice
  against these bundled targets" and "practice against anything else"
  needs to be stated up front, not assumed understood.
- README states the boundary explicitly: fine to attack the bundled
  targets, not fine to reuse the same techniques against systems the
  user doesn't own/have written authorization for. State this once,
  plainly, near the top — don't bury it in a wall of legal text.
- Verify every target/tool image against the Docker Hub API before
  drafting the compose (same technique as above) — this class of repo
  gets copy-pasted from memory/blog posts more than most, and stale or
  renamed image names are common.

## Variant: Competition/Community Platforms (Not Monitoring/ITSM)

The same repo shape (`.env.example` + `generate-env.sh` +
`docker-compose.yml` with DB + cache + app tiers, `internal: true`
network for the DB, healthchecks, pinned tags) applies just as well to
non-infra self-hosted platforms — e.g. **CTFd** (CTF competition
hosting: challenges, scoreboard, teams). Don't assume this pattern is
monitoring/ITSM-specific; the deciding factor is "multi-container app
with DB + web + optional cache/worker tiers", not the app's domain.
For CTFd specifically: pull the compose shape (network names, env var
list, volume mounts) straight from the upstream project's own
`docker-compose.yml` in its GitHub repo (`raw.githubusercontent.com/<org>/<repo>/master/docker-compose.yml`)
rather than reconstructing it from memory — same reasoning as the Wazuh
cert-generator step above: these files encode non-obvious details (e.g.
CTFd's `internal` network name, the `permissions` init container for
volume ownership) that are easy to omit when drafting from recall.

## Verify Bare-Metal Download URLs and Repos the Same Way (Not Just Docker Images)

The "verify before drafting" discipline above applies just as hard to
the **bare-metal/monolith sibling repo** of these stacks (source
tarballs, vendor APT repos) — don't embed a version-pinned download URL
from memory without confirming it resolves:

```bash
curl -sI "https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.5.7.tar.gz" | head -3
curl -s "https://apt.grafana.com/dists/stable/Release" | head -10   # repo metadata, not just the GPG key URL
```

A `200 OK` on the tarball/repo-metadata URL is the same kind of cheap,
mandatory check as the Docker Hub API lookup — do it before finalizing
the install script, not after a user reports it's broken.

## Verify Vendor HTTP APIs Before Automating Against Them (Not Just Existence — Also Deprecation Status)

When a setup script calls a tool's own HTTP API to configure something
post-install (e.g. Grafana's Alerting Provisioning API to create a
Telegram contact point), check the *official docs page* for that
endpoint before writing the script — vendors mark endpoints
"deprecated" while keeping them fully functional (old behavior
continues to work, but docs steer new integrations elsewhere and the
endpoint could be removed in a future release without much notice).
Two concrete things to check, not just "does the endpoint exist":
1. Is it flagged deprecated in the docs? If so, note the risk plainly
   in a script comment near the call, don't silently assume it's stable
   forever.
2. What are the exact required field names for the payload (e.g.
   Telegram contact point needs `bottoken`/`chatid`, not
   `bot_token`/`chat_id`) — pull these from the docs page for that
   specific integration type, not the generic top-level API reference,
   because field-naming conventions vary per-integration within the
   same API.

**Pattern for resilience**: when automating against an endpoint with
deprecation risk, make the script try the API call first, then on
non-2xx response print the exact manual Web UI steps (menu path, field
names, values already filled in from what the user typed) as a
fallback — rather than just failing with a raw error. This way the
script still saves the user typing when the API works, and doesn't
strand them with just an HTTP error code when it doesn't:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST ... )
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "202" ]]; then
    echo "  Created via API."
else
    echo "  API call failed (HTTP ${HTTP_CODE}) — follow these manual steps instead:"
    echo "  1. Open <url>, go to <menu path>"
    echo "  2. Field X: <value already collected from the user>"
    # ...
fi
```

## Exception: Tools With No CLI Database Init — Web Installer Wizard Is Mandatory

Some classic PHP-era apps (RackTables is the concrete case) ship **no
`init.sql`/CLI path** to set up the database at all — the *only*
supported way to create the schema and write the app's DB-credentials
file is a **web installer wizard** (`install.php` or similar) that must
be completed by loading the app in a browser after the container/host
is up. Don't assume every app has a scriptable init path — actually
download and grep the source tree for `init.sql`/`schema.sql` before
writing a script that tries to `mysql < some.sql`:

```bash
curl -sL "<source-tarball-url>" -o /tmp/check.tar.gz
mkdir -p /tmp/check && tar -xzf /tmp/check.tar.gz -C /tmp/check --strip-components=1
find /tmp/check -iname "*.sql" -o -iname "secret*"
grep -rn "path_to_secret_php\|not_already_installed" /tmp/check --include=*.php | head
```

If no CLI init path exists, the install script's job changes: prepare
every prerequisite (packages, DB user+empty schema, writable secret
file placeholder, vhost, permissions) and stop there — the last mile is
manual via browser. Make this explicit in both the script's final
output and the README:
- Print the exact DB host/name/user/password to paste into the wizard
  form (note: inside Docker the DB host is the **compose service name**,
  e.g. `db`, not `localhost` — call this out, it's the #1 way this step
  fails for users copying bare-metal instructions into the Docker repo).
- State the file-permission tightening step required *after* the wizard
  finishes (wizard needs the secret file world-writable to create it;
  lock it back down, e.g. `chmod 440`, once done — leaving it loose is
  a real vulnerability, not just tidiness).
- In the Docker variant, persist the secret file's directory in a named
  volume so `docker compose up -d --build` on a rebuild does **not**
  re-trigger the wizard.

## Exception: No Maintained Docker Image Exists At All — Build a Custom Dockerfile

Before assuming a community image is usable, check its own last-updated
date via the Docker Hub API (`d.get('last_updated')`, same call used to
confirm existence) — a repo can exist, have a real pull count, and still
be **too stale to use safely** (RackTables: highest-pull community image
was last pushed in 2015). Don't default to the highest-pull-count result
without also reading that date.

When nothing current exists, build a **minimal custom Dockerfile from an
official, actively-maintained base image** rather than either (a) using
the stale image anyway or (b) giving up on a Docker variant:
- Base on the official language/runtime image (`php:8.1-apache`, not a
  random community PHP+Apache bundle) — its own tags page shows it's
  still receiving updates.
- Pull the app's *source tarball* inside the Dockerfile the same way the
  monolith install script does (`curl` the versioned GitHub release
  tag), so the Docker and bare-metal repos install the identical
  upstream version and both benefit from the same version-pin discipline.
- Parameterize the version as a `ARG` (e.g. `ARG APP_VERSION=0.22.0`) so
  bumping versions later is a one-line change, not a Dockerfile rewrite.
- When the sandbox has no working `dockerd` to build-test the Dockerfile
  directly, validate by secondary evidence instead of skipping
  validation entirely: confirm the base image tag exists and is current
  (Docker Hub tags API), confirm every `apt-get install` package name
  resolves for the target Debian/Ubuntu release
  (`packages.ubuntu.com/<codename>/<pkg>` or Debian equivalent), and
  confirm any helper binary referenced from the base image (e.g.
  `healthcheck.sh` inside `mariadb:10.11`) actually exists by checking
  that upstream image's own GitHub repo/Dockerfile contents via the
  GitHub Contents API rather than assuming it ships one.
- State plainly in the README which Docker Hub images were checked and
  rejected as too old, so a future maintainer doesn't "helpfully"
  swap back to the stale community image.

## GitHub Releases API for Bare-Metal Binary/Tarball Versions

For monolith installs that download a versioned release tarball
(Prometheus, Node Exporter, RackTables source, etc.), resolve the
current version via the GitHub Releases/Tags API rather than
hand-typing a version number from memory — memory drifts stale fast for
fast-moving projects:

```bash
curl -s "https://api.github.com/repos/<org>/<repo>/releases/latest" \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('tag_name'))"
# if a project doesn't publish GitHub Releases (tag-only), use:
curl -s "https://api.github.com/repos/<org>/<repo>/tags" \
  | python3 -c "import json,sys; [print(t['name']) for t in json.load(sys.stdin)[:5]]"
```

Then still separately confirm the actual asset/tarball URL resolves
(the version string existing as a tag doesn't guarantee the exact
filename pattern you're constructing matches the real release asset).

## README Must Always Document

1. Default login/superuser credentials **and an explicit instruction to
   rotate them** (many of these tools — GLPI especially — ship
   universally-known default creds like `glpi`/`glpi`).
2. First-run setup wizard steps if the app doesn't auto-migrate (GLPI
   shows a browser wizard; Zabbix/NetBox auto-migrate on first boot —
   note the difference so the user isn't confused when one behaves
   differently from another).
3. Backup command (`pg_dump`/`mysqldump` invocation via `docker compose
   exec <db-service> ...`).
4. Update procedure (`docker compose pull && docker compose up -d`,
   plus "back up the DB before a major version bump").
5. What this tool is *for* relative to the other tools already deployed
   in the same infra stack (monitoring vs IPAM vs asset/ticketing) —
   helps the user pick the right tool for a given task later without
   re-asking.

## Variant: Repackaging/Translating a Third-Party GitHub Project (Not Deploying a Known App)

When the user wants a whole third-party project (not a well-known infra
tool) mirrored into their own GitHub with translated docs — e.g.
"buatkan tutorial Bahasa Indonesia untuk `<github-url>` lalu upload" —
this is a redistribution question, not just a docs-writing one. Handle
it in this order:

1. **Check the source repo's license before copying anything**, via the
   GitHub API, not by eyeballing the file list:
   ```bash
   curl -s "https://api.github.com/repos/<org>/<repo>" \
     | python3 -c "import json,sys; print(json.load(sys.stdin).get('license'))"
   ```
   `null` means **no LICENSE file exists** → the repo is
   all-rights-reserved by default; the owner has not granted
   redistribution rights in writing, regardless of how open the project
   feels in spirit (public repo, security-community tool, etc.).
2. **If the license is `null` (or restrictive), stop and `clarify` with
   the user before copying source files** — don't default to "docs-only
   wrapper" or "full copy" on your own. Offer the real tradeoff plainly:
   keep it as a live-download wrapper (fetches the current upstream file
   at runtime, nothing of theirs stored in your repo, zero redistribution
   risk) vs. copy the actual files into the new repo (user accepts the
   licensing risk explicitly). Do whichever the user picks — this is a
   legal-risk decision for the user to own, not one to make unilaterally
   in either direction.
3. **Live-download wrapper pattern** (the default-safe option): a small
   script that always re-fetches the current file from
   `raw.githubusercontent.com/<org>/<repo>/<branch>/<path>` right before
   running it, rather than vendoring a static copy — this sidesteps the
   license question for the executable entirely (nothing of the third
   party's code lives in your repo) and keeps the user automatically on
   the latest upstream version. Wrap it with your own translated
   menu/prompts/warnings printed before invoking the fetched script.
4. **If the user opts to copy files anyway** (their call, their risk),
   put them in a clearly-separated subfolder (e.g. `asli/` /
   `vendor/` / `upstream/`), and write an explicit "Attribution &
   License" section in the README: name the true copyright holder,
   link the source repo, state plainly that no LICENSE file exists
   there so the copied content is technically all-rights-reserved, and
   say "do not redistribute this subfolder separately." Don't bury this
   in a casual "credits" footnote — it needs to be a clearly-headed
   section a future reader can't miss.
5. **Inspect what's actually being copied before pushing it**, especially
   for security-tooling repos — sample/test data folders in these repos
   sometimes contain named real-world exploit or malware captures (e.g.
   a NIDS-testing repo shipping `.pcap` captures literally named after
   EternalBlue/DoublePulsar or a ransomware campaign). This data is
   inert (packet captures, not executables) and typically fine for a
   security-education repo, but document what it is and where it came
   from in the README rather than silently including unlabeled files a
   future reader might mistake for something else or flag as suspicious.

