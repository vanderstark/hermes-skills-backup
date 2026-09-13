# Prometheus + Grafana Monitoring Stack Reference

**Class:** Metrics monitoring stack (NOT log aggregation / NOT security NSM)

**Repos pattern:** Docker Compose (`prometheus-grafana-docker`) vs. Monolith systemd (`prometheus-grafana-monolith`) — split per install method, generic name (no app-brand prefix).

## When This Applies

- User wants to monitor server resource metrics (CPU/RAM/disk/network)
- User wants per-container metrics (Docker hosts)
- User has a multi-server fleet (datacenter) and wants central monitoring
- User wants a dashboard UI (Grafana) backed by Prometheus TSDB

## Docker Stack Shape (prometheus-grafana-docker)

### docker-compose.yml
```yaml
services:
  prometheus:
    image: prom/prometheus:v2.53.0
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks: [monitoring]

  grafana:
    image: grafana/grafana-enterprise:11.1.0
    ports: ["3000:3000"]
    volumes:
      - grafana_data:/var/lib/grafana
      - ./provisioning:/etc/grafana/provisioning:ro
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-admin123}
    networks: [monitoring]
    depends_on: [prometheus]

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.50.0
    ports: ["8080:8080"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker/:ro
    networks: [monitoring]

  node-exporter:
    image: prom/node-exporter:v1.8.2
    ports: ["9100:9100"]
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - "--path.procfs=/host/proc"
      - "--path.sysfs=/host/sys"
      - "--path.rootfs=/rootfs"
      - "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)"
    networks: [monitoring]

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    name: monitoring
    driver: bridge
```

### Key Docker decisions
- Network name `monitoring` can be left implicit (docker compose auto-creates it) — don't pre-create with `docker network create` unless you deliberately want it to survive `docker compose down`.
- In Docker, Prometheus scrape targets use **service names** (`node-exporter:9100`), never `localhost`.
- `node-exporter` needs `pid: host` and `command` path overrides for correct host proc/sys visibility from inside the container.

## Monolith Stack Shape (prometheus-grafana-monolith)

### Install sequence (native Ubuntu 24.04)
1. Create system users: `sudo useradd -r -s /sbin/nologin prometheus`
2. Download Prometheus binary tar.gz from GitHub releases → extract → `/opt/prometheus`
3. Symlink binaries: `sudo ln -s /opt/prometheus/prometheus /usr/local/bin/prometheus`
4. Create dirs: `/etc/prometheus/{consoles,console_libraries,rules}`, `/var/lib/prometheus`
5. Copy config: `sudo cp prometheus.yml /etc/prometheus/prometheus.yml` (the *repo's* config, not the tarball's example)
6. Write systemd unit to `/etc/systemd/system/prometheus.service`:
```ini
[Unit]
Description=Prometheus Monitoring
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file /etc/prometheus/prometheus.yml \
  --storage.tsdb.path /var/lib/prometheus/ \
  --web.console.libraries /etc/prometheus/console_libraries \
  --web.console.templates /etc/prometheus/consoles \
  --storage.tsdb.retention.time=30d \
  --web.enable-lifecycle

[Install]
WantedBy=multi-user.target
```
7. Node Exporter: download binary → `/usr/local/bin/` → own systemd service on port 9100
8. Grafana: install via **official APT repo** (`packages.grafana.com/oss/deb`) — simpler than binary tarball
9. Start: `sudo systemctl enable --now prometheus grafana-server node_exporter`

### Key monolith decisions
- In monolith, Prometheus scrape targets use `localhost` (same host), unlike Docker's service names.
- `--web.enable-lifecycle` flag allows `curl -X POST http://localhost:9090/-/reload` to reload config without a full restart.
- Node Exporter running natively on the host needs NO `--path.procfs`/`--path.sysfs` overrides (those exist only to work around Docker's mount namespace) — plain `ExecStart=/usr/local/bin/node_exporter` is correct.

## Multi-Server Farm Pattern (large datacenter, e.g. 170-server case)

### Architecture
```
   Central Server
   ┌────────────────────────────────────┐
   │  Prometheus + Grafana              │
   │  scrapes each target's :9100      │
   └──────────────┬──────────────────┘
                  │ scrape (HTTP)
   ┌──────────────┴──────────────────┐
   │  N Server Targets                │
   │  each runs: node_exporter:9100  │
   └───────────────────────────────┘
```

### Two approaches to target config

**A. static_configs (simple, needs a Prometheus restart on change)**
```yaml
scrape_configs:
  - job_name: "server-farm"
    static_configs:
      - targets:
          - "10.0.1.10:9100"
          - "10.0.1.11:9100"
          # ... rest of the fleet
```

**B. file_sd_configs (recommended for large/churning fleets — no restart needed)**
```yaml
scrape_configs:
  - job_name: "server-farm"
    file_sd_configs:
      - files:
          - "/etc/prometheus/targets/*.json"
        refresh_interval: 30s
```
File `/etc/prometheus/targets/servers.json`:
```json
[
  {
    "targets": ["10.0.1.10:9100", "10.0.1.11:9100"],
    "labels": { "environment": "production", "site": "site-a" }
  }
]
```
→ Reload after editing the JSON: `sudo systemctl reload prometheus` or `curl -X POST http://localhost:9090/-/reload`

### Per-target Node Exporter deployment (server target side)
Node Exporter is lightweight (~20MB RAM). Deploy via systemd (monolith target) or a single Docker container:
```bash
docker run -d --name node-exporter --restart unless-stopped \
  -p 9100:9100 \
  -v /proc:/host/proc:ro -v /sys:/host/sys:ro -v /:/rootfs:ro \
  prom/node-exporter:v1.8.2 \
  --path.procfs=/host/proc --path.sysfs=/host/sys --path.rootfs=/rootfs \
  --collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)
```
For large fleets (dozens to hundreds of hosts), prefer Ansible over a raw SSH loop for idempotency and error handling — don't build one ad hoc unless the user asks for it explicitly.

## Dashboard Import IDs

| ID  | Name                          | Use case                |
|-----|-------------------------------|-------------------------|
| 1860| Node Exporter Full            | Host CPU/Mem/Disk/Net   |
| 179 | Docker Monitoring             | Per-container metrics   |
| 3662| Prometheus 2.0 Overview       | Prometheus self-health  |

Import via: Grafana UI → Dashboards → New → Import → enter ID → pick "Prometheus" datasource.

## Grafana Provisioning (Docker — auto-wire datasource + dashboard on first boot)

`provisioning/datasources/datasource.yml`:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
```

`provisioning/dashboards/dashboard-provider.yml`:
```yaml
apiVersion: 1
providers:
  - name: "default"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards
```

Dashboard JSON files placed in `dashboards/` and mounted at `/var/lib/grafana/dashboards/` appear automatically in Grafana's dashboard list — no manual import needed on subsequent boots.

## Security Notes (Monolith + Multi-server)

- **Firewall (server target side):** restrict `:9100` to the monitoring server's IP only:
  ```bash
  sudo ufw allow proto tcp from <monitoring-server-ip> to any port 9100
  sudo ufw deny 9100
  ```
- **Firewall (central server):** never expose `:9090`/`:3000` to the internet directly — put behind a reverse proxy with TLS (see the SSL tutorial repos in this same skill's `templates/` for the Nginx/Apache + Let's Encrypt pattern).
- **Grafana:** change the `admin` password on first login; keep `GF_USERS_ALLOW_SIGN_UP=false`.
- **Prometheus:** has no auth by default. If exposed via reverse proxy, add basic auth or an IP allowlist at the proxy layer.

## Sync Verification Recipe (local ↔ GitHub)

Don't trust `git push`'s exit code alone as proof the content landed — confirm via the API:
```bash
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(curl -s "https://api.github.com/repos/<user>/<repo>/commits/main" | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
echo "Local:  $LOCAL_SHA"
echo "Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" = "$REMOTE_SHA" ] && echo "In sync" || echo "MISMATCH"
```
Also spot-check the file tree via the Contents API to catch a "successful but empty/wrong" push:
```bash
curl -s "https://api.github.com/repos/<user>/<repo>/contents/" | python3 -c "
import json,sys
for item in json.load(sys.stdin):
    print(f'  {item[\"type\"]:5} {item[\"name\"]}')
"
```
This SHA-diff pattern generalizes beyond monitoring stacks — use it any time a push needs positive confirmation rather than assumed success, especially after a batch of commits across multiple repos in the same session.

## Related: Companion Stack (Push-Based Uptime Kuma)

Prometheus+Grafana is **pull-based** (central scraper → target agents). Its push-based companion — **Uptime Kuma** (each target sends heartbeat to a central server) — uses a parallel dual-repo pattern (`uptime-kuma-docker` + `uptime-kuma-monolith`) with its own agent deployment workflow. See `references/uptime-kuma-monitoring.md` for the full push-based agent deployment guide (systemd `uptime-kuma-pushbeat.service`, `install-agent.sh`/`deploy-agent.sh`, bulk deploy to 170 targets via SSH, Push URL management, and troubleshooting table).
