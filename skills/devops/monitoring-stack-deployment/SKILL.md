---
name: monitoring-stack-deployment
description: "Deploy Prometheus/Loki/Netdata monitoring to 170 servers."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [monitoring, logging, prometheus, loki, netdata, uptime-kuma, docker, monolith, deployment, 170-server, datacenter, devops]
    related_skills: [github-token-deploy-workflow, webapp-delivery, monitoring-setup, deployment-guide]
---

# Monitoring Stack Deployment (Datacenter/Multi-Server Monitoring Infra)

## Purpose

Class-level workflow for scaffolding, deploying, and syncing **multi-repo monitoring infrastructure** to GitHub, covering both Docker and monolith installs, with **agent deployment guides** for scaling to **170+ servers**.

## When to Use

- User wants to deploy monitoring stacks (Prometheus/Grafana, Loki, Netdata, Uptime Kuma) in both Docker and native/monolith variants
- User needs consistent tutorial structure across all monitoring repos (Bahasa Indonesia guides with English commands)
- User requests agent deployment instructions for scaling monitoring to a server farm
- User wants to deploy to GitHub with clean naming (no app-brand prefixes like "ccc-")

## Repository Structure Convention

Each monitoring tool gets **2 separate repos** (Docker + monolith):

```
tool-{docker|monolith}/
├── README.md                  # Overview + quick start (2 paths)
├── TUTORIAL.md                # Full tutorial (otomatis + manual)
├── docker-compose.yml         # [docker variant only]
├── *.service                  # [monolith variant only] systemd units
├── provisioning/              # [docker variant only] (datasources, dashboards)
├── agents/                    # [uptime-kuma, netdata] systemd unit templates
├── dashboards/                # Grafana JSON dashboards
├── scripts/
│   ├── setup-*.sh             # 🅰️ Install stack on server pusat
│   ├── install-agent.sh       # 🅱️ Install agent on 1 target server
│   ├── deploy-bulk.sh         # Deploy agent to N servers via SSH
│   └── servers.txt.example    # Template IP list
```

## Tutorial Convention (Mandatory Per User Request)

Each `TUTORIAL.md` MUST contain **both paths**:
1. **🅰️ Otomatis (Script)** — single command execution
2. **🅱️ Manual (Step-by-step)** — 10-11 numbered `langkah` (instructions)

**Language rule**: Section titles in Bahasa Indonesia; all commands/code blocks in English (shell commands). This is a hard user preference.

## Agent Deployment Patterns (Tool-Specific)

| Tool | Agent | Method |
|------|-------|--------|
| Prometheus | Node Exporter | Pull-based via SSH deploy script |
| Loki | Promtail | Push-based agent (systemd) + SSH bulk deploy |
| Netdata | Child Netdata | Streaming (parent-child) via API key + SSH bulk deploy |
| Uptime Kuma | Pushbeat.sh | HTTP heartbeat (curl loop) via systemd service |

## GitHub Push Workflow

Follow [github-token-deploy-workflow](software-development/github-token-deploy-workflow/SKILL.md).
Repo names: **generic + variant** (e.g., `netdata-docker`, `loki-logging-monolith`).
User rejected app-brand prefixes like "ccc-" — always use clean names.

## Token Security (Critical)

PAT was reused inline across many commands. Write token to temp file **ONCE** then reference via `$(cat /tmp/gh_token_file)`. **Alert user to revoke token immediately** after repeated exposure.

## Sync & Verification

- Verify files via Contents API (not push exit status)
- `bash -n scripts/*.sh` — Check Bash syntax
- YAML parse for `docker-compose.yml` & config files
- Spot-check 2-3 repos — enough to catch systematic failure

## Pitfalls

- **`git init` may create `master`**: if `git push -u origin main` fails with "src refspec", run `git branch -m master main` first.
- **Push before repo exists**: CREATE via API FIRST, then push — else "repository does not exist".
- **`cp -r src/.* dest/` pulls source `.git`**: after glob-copy, `rm -rf dest/.git` then fresh init.
- **Token inline triggers scanner**: causes approval timeout. Use temp-file pattern.
- **`set -euo pipefail` + trap referencing unset vars**: init `TMP_DIR=""` at top.