# Pulse Monitoring — Deployment + Advisory Notes (v6.x)

Deployed 2026-08-09 as two repos: `vanderstark/pulse-docker` and
`vanderstark/pulse-monolith`. Pulse = self-hosted infra monitoring
(Proxmox VE/PBS/PMG, Docker/Podman, Kubernetes, TrueNAS, Linux/Win/macOS
agents, vSphere early-access) with an "AI Patrol" that runs scheduled
rounds over state+history to surface silent failures (failed backups,
restart loops, unhealthy containers, clock drift).

## Key facts (verify-again-if-stale)

- Upstream: `github.com/rcourtman/Pulse` — **MIT license (Community
  edition)**, written in Go (single binary) + SolidJS/TS frontend.
- Port: **7655**. Docker image: `rcourtman/pulse` (multi-arch
  amd64/arm64).
- Editions: **Community (free, MIT, 7-day history)** / Relay (paid:
  remote web access, mobile pairing, push) / Pro (paid: Patrol
  investigation, governed fixes, 90-day history, RBAC, audit) / MSP.
  Core self-hosted monitoring is NOT gated by monitored-system count.
- First-run auth is a **bootstrap token** (secure by default): generate
  via `docker exec pulse /app/pulse bootstrap-token`,
  `sudo pulse bootstrap-token`, or `pct exec <ctid> -- /usr/local/bin/pulse
  bootstrap-token` (LXC path must be absolute). Paste the printed token
  into the web UI, then Quick Security Setup wizard creates admin + API
  token. v6 stores an encrypted JSON snapshot in `.bootstrap_token` —
  never paste the raw file contents.
- Release assets: `pulse-<tag>-linux-amd64.tar.gz` (~150 MB) extracts to
  `./bin/pulse` (+ `bin/pulse-agent-*`, `scripts/`). The official
  `install.sh` (signed, verify with sshsig before running) is the
  server installer; agent installs are served by the running server at
  `Settings → Infrastructure → Install on a host` (`/install.sh` on the
  Pulse host) — do NOT use the GitHub server installer for agents.
- Manual systemd unit (validated):
  ```
  [Service]
  Type=simple
  ExecStart=/usr/local/bin/pulse
  Restart=always
  RestartSec=10
  Environment=PULSE_DATA_DIR=/etc/pulse
  ```
  Data dir `/etc/pulse`. Docker path mounts `/data` volume; set
  `PULSE_DEPLOYMENT_METHOD=docker_compose`. Optional auto-login env:
  `PULSE_AUTH_USER`/`PULSE_AUTH_PASS` (auto-hashed at startup).
- Docker host monitoring uses the **unified agent** on the host — the
  Pulse server container does NOT need `/var/run/docker.sock` (safer).

## Deploy shape used (matches the split-repo rule)

- `pulse-docker`: `docker-compose.yml` (image `rcourtman/pulse:${PULSE_VERSION:-v6.1.2}`,
  port `${PULSE_PORT:-7655}:7655`, volume `pulse_data:/data`) + `.env.example`
  (PULSE_VERSION, PULSE_PORT) + README tutorial.
- `pulse-monolith`: `install.sh` (downloads the versioned release
  tarball from GitHub Releases via `PULSE_VERSION`, `install -m 0755
  bin/pulse /usr/local/bin/pulse`, writes the systemd unit above) +
  `uninstall.sh` + `pulse.service` + README tutorial.
- READMEs are full tutorials in Indonesian: install → bootstrap token →
  add monitored hosts (Proxmox API token / unified agent / Docker
  socket) → manage service → update → uninstall → troubleshooting.
- Resolve the current version with the GitHub Releases API
  (`/releases/latest` → `tag_name`) and confirm the exact asset URL
  pattern resolves before finalizing install.sh. Docker image existence
  via Hub API (`hub.docker.com/v2/repositories/rcourtman/pulse/tags`).

## Advisory context (AKPOL infra — user runs 170-server datacenter + police academy lab)

User compared **Pulse vs Zabbix**; recommended split:
- **Pulse** = operational dashboard for Proxmox VE/PBS/PMG + Docker
  (CCC, AI lab) — native integrations, AI Patrol, easy deploy.
- **Zabbix** = enterprise backbone for physical hosts (SNMP/IPMI/BMC),
  switches/routers, compliance/audit, retention, 1000+ templates.
Because Pulse lacks SNMP/IPMI and Zabbix lacks AI patrol, both together
cover the gap; neither alone does.

**Proxmox Backup Server (PBS)** questions resolved:
- PBS software is **free, AGPLv3** — all features (dedup, compression,
  incremental, encryption, verify) work on the `pbs-no-subscription`
  repo. Subscription (~€225-960/yr, `pbs-enterprise` repo) buys support
  + enterprise repo, not features.
- Placement for a 2-physical-server AKPOL buy: **no third server
  needed** — Server A = Proxmox VE compute (CCC, AI/OSINT lab), Server B
  = Proxmox VE + LXC-PBS (backup target + staging). Physical separation
  of data vs backup is what matters, not container-vs-bare-metal PBS.
  Honest caveat to state: both in the same room = 3-2-1 rule is really
  2-2-0 — add a cheap off-site layer (encrypted USB / cloud Restic) for
  critical data only.