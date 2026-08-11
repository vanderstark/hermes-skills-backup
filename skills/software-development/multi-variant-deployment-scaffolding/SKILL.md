---
name: multi-variant-deployment-scaffolding
description: "Generate/publish many parametrized deploy template variants."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, scaffolding, templates, github, bulk-generation, deployment]
    related_skills: [docker-development, github-repo-management]
---

# Multi-Variant Deployment Scaffolding

Covers two related, recurring tasks: (1) generating N parametrized
variants of a deployment template (e.g. "every combination of webserver ×
language version"), and (2) publishing each variant — either as
subfolders in one repo, or as N separate one-repo-per-variant GitHub
repos — reliably at scale (10-25+ variants in one pass).

## When to use this skill

- User asks for "all combinations of X and Y" as deployable
  artifacts — e.g. Nginx/Apache × PHP 5.6-8.3, or any webserver ×
  language-version × framework matrix
- User wants each variant packaged separately (individual ZIPs, or
  individual GitHub repos) rather than one big bundle
- User wants a tutorial/install-script matrix that varies by only a few
  parameters (e.g. monolith vs distributed architecture, per-component
  install scripts)

## Core Technique: Generator Script, Not Hand-Written Files

Never hand-write N nearly-identical Dockerfiles/compose files/scripts one
at a time in separate tool calls — write ONE Python generator script with
small per-variant functions, loop over the parameter matrix, and write
each file inside the script. This is dramatically faster, less
error-prone, and trivially auditable (validate all outputs in one pass
afterward).

Pattern:

```python
import os

VERSIONS = ["5.6", "7.4", "8.0", "8.1", "8.2", "8.3"]  # or whatever axis
WEBSERVERS = ["nginx", "apache"]

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def dockerfile_for(webserver, version):
    # branch on version/webserver-specific quirks HERE, not by duplicating
    # whole files — e.g. EOL versions need a warning comment, non-alpine
    # base images for versions with no alpine variant, etc.
    ...
    return content

for webserver in WEBSERVERS:
    for version in VERSIONS:
        d = f"{BASE}/{webserver}-{version}"
        write_file(f"{d}/Dockerfile", dockerfile_for(webserver, version))
        write_file(f"{d}/docker-compose.yml", compose_for(webserver, version))
        write_file(f"{d}/README.md", readme_for(webserver, version))
```

Run this via `terminal` (as a saved `.py` file — `execute_code` blocks
subprocess-heavy generation, and cron-mode sessions block it entirely),
never inline heredocs per file.

### Handle Version/Combo-Specific Quirks Explicitly, Don't Silently Uniform Them

Real per-version differences matter and get missed if you templatize too
aggressively:
- Some language versions only ship non-alpine base images (e.g. very old
  PHP versions lack an alpine variant — check before assuming
  `<lang>:X-alpine` exists for every version in your matrix)
- EOL/unsupported versions should carry an explicit warning comment in
  the generated Dockerfile/README, not be presented identically to
  actively-supported versions
- A newer framework version may not support the oldest language version
  in your matrix at all (e.g. a framework requiring PHP 7.4+ cannot
  honestly get a PHP 5.6 variant) — flag this to the user and drop that
  cell from the matrix rather than generating something that will fail
  to build; don't fabricate a working combination that doesn't exist

## Validate Every Generated File Before Delivering

After generation, mechanically validate ALL outputs in one pass — don't
eyeball a sample:

```bash
python3 -c "
import yaml, glob
errors = []
for f in glob.glob('BASE_DIR/**/*.yml', recursive=True):
    try:
        yaml.safe_load(open(f))
    except Exception as e:
        errors.append((f, str(e)))
print('OK' if not errors else errors)
"
```

For zipped/bulk-packaged variants, also verify each archive contains the
expected file set (not just that the archive exists):

```python
import zipfile, glob
for zp in glob.glob('*.zip'):
    with zipfile.ZipFile(zp) as zf:
        names = zf.namelist()
        base = names[0].split('/')[0]
        required = [f'{base}/Dockerfile', f'{base}/docker-compose.yml']
        missing = [r for r in required if r not in names]
        if missing: print(zp, 'MISSING', missing)
```

`zipfile` (Python stdlib) is a reliable substitute when the `zip` CLI
isn't installed on the box — no need to apt-install anything.

## Publishing: One Repo Per Variant vs Subfolders in One Repo

Ask the user explicitly which they want before generating anything —
these are not equivalent and re-doing 20+ repos after generating one
combined repo wastes a full round-trip:

- **One combined repo, subfolders per variant** — simpler, one clone
  gets everything, easier to keep a single shared README/CI. Default
  choice when not specified.
- **One repo per variant** — needed when variants are meant to be
  cloned/used fully independently, or the user explicitly asks for
  "different repo for each". Loop repo-create-via-API + git-init + push
  per folder; validated to work reliably for 20+ repos in one pass. See
  `scripts/bulk_github_repo_push.md` for the exact loop pattern and the
  token-hygiene practices that go with it (strip token from remote URL
  immediately after push, unset from shell, remind user to revoke a
  token that appeared in chat plaintext).

## Pre-Generation Verification — Never Assume Install Mechanics, Fetch Them

Before writing a single install script/Dockerfile line for a
service/tool you haven't personally verified this session, spend 2-3
tool calls confirming the *actual* mechanics — assumptions about how a
tool installs are wrong often enough to be the default risk, not the
edge case:

- **APT/download URLs**: `curl -sI <url>` for a 200, or hit the
  provider's release API (`api.github.com/repos/<org>/<repo>/releases/latest`
  or `/tags`) to confirm the version string you're about to hardcode
  still exists and is current.
- **Docker images**: check `https://hub.docker.com/v2/repositories/<ns>/<img>/`
  before writing `image: foo/bar:latest` into a compose file — a
  plausible-sounding image name can 404 (`"message": "object not
  found"`), or exist but be dead (checked one this session with
  514k pulls last updated in **2015** — pull count alone doesn't mean
  current/safe). If no actively-maintained official image exists,
  **build a custom Dockerfile from an official base image** (e.g.
  `php:8.1-apache` + fetch the tool's source at build time) rather than
  using a stale community image or fabricating one.
- **Non-trivial installers**: for any tool where you're about to write
  "run this SQL file" / "here's the config format" from memory,
  actually download and grep the tool's real source first
  (`curl -sL <tarball> | tar -xz`, then `find`/`grep` the extracted
  tree). This caught a real case: an assumed `init.sql` + manual
  `secret.php` for RackTables didn't exist at all — the real installer
  is a **web wizard** (`install.php`) that generates config
  interactively; the script had to be rewritten to prep prerequisites
  and hand off to the wizard instead of trying to script around it.
  Same discipline applies to CLI flags, env var names, and directory
  layouts for CrowdSec/Suricata/Grafana Alerting API etc. — fetch the
  vendor's current docs page (via browser tool, not memory) and quote
  real command output, don't paraphrase from training data.
- Docker daemon may not be available in the execution sandbox to
  actually build/test a Dockerfile — when so, substitute verification
  with checking base-image tags exist, apt package names resolve for
  the target Debian/Ubuntu codename, and any embedded scripts
  py_compile/bash -n clean, and say so explicitly rather than claiming
  the build was tested.

## Copying Third-Party Assets Into a Repo (No LICENSE Present)

When a user asks to also upload/mirror another project's actual code or
binary assets (not just write a docs/tutorial *about* it), check the
source repo's license first: `curl -s
"https://api.github.com/repos/<org>/<repo>" | python3 -c "...print(d['license'])"`.
If `license` is `null`, the repo is default all-rights-reserved —
flag this explicitly to the user with a clarifying question (copy
anyway at their own risk / skip and keep docs-only / recommend a real
fork instead of manual copy) before writing any files. If the user
says proceed anyway, still add a clear Attribution/License section in
the new repo's README naming the original owner, linking the source
repo, and stating the copied folder is not separately licensed —
this is the minimum diligence, not a substitute for the user's own
legal judgement.

## Pitfalls

- Don't assume `execute_code` is available for the generator script —
  it commonly gets blocked ("runs arbitrary local Python... blocked").
  Write the generator to a `.py` file with `write_file` and run it via
  `terminal(command="python3 /path/to/generator.py")` instead.
- `write_file` / sandbox tools are often restricted to a safe-root
  directory (e.g. only under a specific data dir) — writing the
  generator script itself to `/tmp` can be denied even though the
  *generated output* under the safe root is fine. Put the generator
  script itself under the same safe root as its output.
- When a framework has a real minimum-version requirement that excludes
  part of the requested matrix (e.g. "PHP 5-8" but framework needs
  7.4+), surface this as a clarifying question with concrete options
  (skip the unsupported version / substitute an older framework version
  / include anyway with a big warning) rather than silently picking one.

## Related Skills

- `docker-development` — Dockerfile/compose best practices (multi-stage
  builds, non-root user, healthchecks) that the generator functions
  should follow for each variant
- `github-repo-management` — full GitHub API reference (auth, repo
  create/fork, releases); this skill's `scripts/` file supplements it
  with the specific bulk-loop pattern for many-repos-at-once

## Non-Docker Variant: Bare-Metal Service Install Tutorials

The same "generate N parametrized variants, validate, publish" workflow
applies to **bare-metal install tutorials** (a self-hosted service like
Zabbix/LibreNMS deployed via a shell script + README, not Docker) — the
variant axis here is usually **architecture** (monolith vs distributed) or
**component role** (database-server / app-server / per-site proxy), each
shipped as its own `install-*.sh` + shared `README.md`.

Conventions that held up well across repeated requests for this kind of
tutorial in one session (Zabbix monolith, Zabbix distributed w/
proxy-per-site, LibreNMS):

- **Generate strong random credentials in-script**, never hardcode a
  password: `PASS="$(openssl rand -base64 18 | tr -d '=+/' | cut -c1-20)"`
- **Write generated credentials to a root-only file** (`chmod 600`) and
  print its path in the final summary — never print the raw password to
  stdout/logs where it could be scraped later.
- **Idempotency checks before heavy operations** — e.g. before importing
  a large SQL schema, check whether the target DB is already populated
  (`SELECT COUNT(*) FROM information_schema.tables WHERE ...`) and skip
  if so, so the script can be safely re-run without corrupting an
  existing install.
- **`set -euo pipefail` + a `log()`/`err()` helper** at the top of every
  script for consistent colored progress output and fail-fast behavior.
- **UFW detection, not blind `ufw allow`**: check
  `ufw status | grep -q "Status: active"` before opening any port, so the
  script doesn't silently no-op (or error) on hosts without UFW.
- **Distributed/multi-component variants need cross-references in the
  README** — e.g. "run install-database-server.sh first, note the
  IP/credentials it prints, then pass them interactively to
  install-server-distributed.sh" — a numbered "install order" section
  with copy-pasteable example commands per component is what makes a
  multi-script variant actually usable versus just N unrelated scripts.
- **End every script with a clearly bordered summary block** (access
  URL, default login, and the literal next-step command) — this is what
  the user actually reads first; don't bury it in the middle of install
  log output.
- Always run `bash -n <script>.sh` on every generated script before
  delivering/pushing (cheap syntax check, catches unclosed quotes/heredocs
  immediately) — same discipline as the `yaml.safe_load()` pass for
  compose files.

## Deploying the Same Service Two Ways (Bare-Metal Script vs Docker Compose)

When a user first asks for a bare-metal install tutorial for a service,
then later asks for "the same thing but Docker Compose" (a real recurring
pattern), treat them as **separate deliverables that should reference each
other**, not a replacement:

- Reuse the same env var names / defaults across both (DB name, admin
  user, ports) so the user isn't relearning the service's shape twice.
- The Docker version should prefer the vendor's **official pre-built
  image** (e.g. `zabbix/zabbix-server-mysql`, `librenms/librenms`) over
  reinventing a custom Dockerfile that reimplements bare-metal
  installation steps in a container — official images already encode
  correct entrypoint/migration logic (e.g. Zabbix's image auto-imports
  the DB schema on first boot; a bare-metal script does the same thing
  manually via `zcat ... | mysql ...`). Don't duplicate that logic in a
  Dockerfile; just consume the image and pass config via environment
  variables per that image's documented contract.
- Multi-process services with a "web + background worker" split (e.g.
  LibreNMS: web UI vs dispatcher/poller vs SNMP-trap-receiver) are often
  shipped by the vendor as **one image, multiple services differentiated
  by env var flags** (LibreNMS uses `SIDECAR_DISPATCHER=true` /
  `SIDECAR_SNMPTRAPD=true` on the same `librenms/librenms` image rather
  than separate images) — check the vendor's official Docker docs for
  this pattern before assuming you need N different images for N roles.
- Cross-link the README of each version to the other (bare-metal README
  mentions "see also X for the Docker Compose version" and vice versa)
  since the user is likely to want to reference the sibling repo later.
