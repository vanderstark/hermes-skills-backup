# Uptime Kuma Monitoring Stack (Dual-Repo Pattern)

**Dual-repo deploy shape validated in session:** separate repos for Docker vs Monolith, each with complete agent deployment guide for 170-server datacenter.

## Repos Created
- `uptime-kuma-docker` — Docker Compose (louislam/uptime-kuma:1)
- `uptime-kuma-monolith` — Native Node.js + systemd on Ubuntu 24.04

## Key Pattern: Push-Based Agent (vs Prometheus Pull)

Uptime Kuma uses **push-based monitoring**: each target server runs a lightweight agent that POSTs heartbeat to Uptime Kuma push endpoint. If heartbeat stops → server marked DOWN.

### Agent Architecture
```
Server Pusat (Uptime Kuma :3001)
       │
  push heartbeat ──► Server Target (10.0.x.x)
                        │
                        └── systemd service: uptime-kuma-pushbeat
                            └── script: /opt/uptime-kuma-agent/pushbeat.sh (loop curl every 60s)
```

### Agent Files (in each repo)
```
agents/
  └── pushbeat.service          # systemd unit (deployed to /etc/systemd/system/)
scripts/
  ├── install-agent.sh          # Install agent on ONE target server (via SSH)
  ├── deploy-agent.sh           # Bulk deploy to N servers (reads servers.txt)
  ├── pushbeat.sh               # Heartbeat script (embedded in install-agent.sh)
  └── servers.txt.example       # Template: list of target IPs
```

### Deployment Workflow (User Validated)

**Step 1 — Create Push Monitor in UI:**
```
Uptime Kuma UI → Add Monitor → Type: "Push" → Save
→ Copy Push URL: http://10.0.0.5:3001/api/push/xxxxx?status=up&msg=OK&ping=
```

**Step 2 — Single Server (via SSH from central):**
```bash
ssh root@10.0.1.10 "bash -s" < scripts/install-agent.sh "http://10.0.0.5:3001/api/push/xxxxx?..."
```

**Step 3 — Bulk (170 servers):**
```bash
cp scripts/servers.txt.example scripts/servers.txt
nano scripts/servers.txt   # fill IPs
chmod +x scripts/deploy-agent.sh
./scripts/deploy-agent.sh "http://10.0.0.5:3001/api/push/xxxxx?..." --bulk scripts/servers.txt
```

> ⚠️ **Critical**: Each server needs UNIQUE Push URL (1 monitor = 1 URL). For 170 servers, create 170 Push monitors via API first, then map IP→URL in deploy script.

### Push Monitor Creation via API (Automation)
```bash
for i in $(seq 1 170); do
  curl -s -X POST "http://localhost:3001/api/v1/projects/0/monitors" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <API_KEY>" \
    -d "{\"name\": \"Server-$i\", \"type\": \"push\", \"interval\": 60}"
done
```

### Repo Structure (Dual-Tutorial Convention)
Each repo contains BOTH tutorial formats (user requirement):
- `README.md` — Quick Start: 🅰️ Otomatis (script) + 🅱️ Manual (step-by-step)
- `TUTORIAL.md` — Full manual guide (10-11 numbered langkah) + agent deployment section
- `scripts/setup-uptime-kuma.sh` — Install central Uptime Kuma (Docker or native)
- `scripts/install-agent.sh` — Agent installer for target servers
- `scripts/deploy-agent.sh` — Bulk SSH deploy
- `agents/pushbeat.service` — systemd unit template

### Naming Convention (User Enforced)
- NO app prefix in repo names: `uptime-kuma-docker` NOT `ccc-uptime-kuma-docker`
- Separate repos per install method (Docker vs Monolith)
- Generic stack names only

### Troubleshooting Table (Included in TUTORIAL.md)
| Gejala | Penyebab & Solusi |
|--------|-------------------|
| Monitor **Pending** | Agent belum kirim heartbeat → cek `journalctl -u uptime-kuma-pushbeat` |
| Monitor **DOWN** tapi server hidup | Push URL salah/expired, firewall blokir outbound ke 3001 |
| `curl: (7) Failed to connect` | Server pusat tidak reachable dari target — cek network/firewall |
| Agent jalan tapi UI tidak update | Push URL invalid (monitor dihapus di UI) → buat ulang monitor |

### Sync with Prometheus Stack (Reference)
Both monitoring stacks (Prometheus+Grafana pull + Uptime Kuma push) deployed in same session for 170-server datacenter:
- Prometheus repos: `prometheus-grafana-docker`, `prometheus-grafana-monolith`
- Uptime Kuma repos: `uptime-kuma-docker`, `uptime-kuma-monolith`
- Shared pattern: dual-repo, agent deployment scripts, file_sd_configs for dynamic targets

### Related Templates
- `templates/zeek-monitoring-stack.md` — behavioral network analysis
- `templates/tpot-honeypot-stack.md` — honeypot early warning
- `references/prometheus-grafana-monitoring.md` — Prometheus pull-based pattern