# 🛠️ DevOps & Infrastructure Lanjutan: Monitoring & Tuning untuk 170-Server DC

**Ditulis:** 24 Agustus 2026  
**Kategori:** DevOps & Infrastructure (Lanjutan)  
**Target User:** Bos (170-server datacenter + polsek/academy AI/OSINT lab)  
**Bahasa:** Indonesian (Bahasa Indonesia)

---

## 🎯 Ringkasan

Skill lanjutan ini fokus pada **observability infrastruktur skala besar** — mendeteksi masalah sebelum jadi insiden, tuning performa database/aplikasi, dan otomasi operasional untuk datacenter 170 server.

**Konteks operasional:** Dengan 170 server + lab AI/OSINT, Bos butuh sistem monitoring yang **scalable**, **self-hosted** (sesuai preferensi open-source), dan **automated alerting** agar tidak perlu cek manual satu-per-satu.

---

## 📚 Skill Roadmap: 3 Lapis Pembelajaran

### Tier 1: Dasar (Sudah Dikuasai)
- ✅ `docker-laravel-automation` — Backup, health-check & cron ops Laravel apps
- ✅ `github-multi-repo-automation` — Push otomatis multi-repo

### Tier 2: Intermediate (Focus Sesi Ini)
- 🔷 `monitoring-stack-deployment` — Deploy Prometheus/Loki/Netdata ke 170 server
- 🔷 `database-performance-tuning` — Auto-tune MySQL/PostgreSQL/MongoDB/Redis
- 🔷 `datacenter-ops` — RAID sizing, UPS/NUT, DC monitoring
- 🔷 `security-ai-observer` — Wiring DeepHat AI analysis ke Loki cron alerts
- 🔷 `tuning-repo-publishing` — Publish tuning scripts sebagai GitHub repos terpisah

### Tier 3: Advanced (Lanjutan)
- 🟦 `implementing-endpoint-detection-with-wazuh` — SIEM/XDR untuk 170 server
- 🟦 `implementing-syslog-centralization-with-rsyslog` — Centralized logging dengan TLS
- 🟦 `configuring-network-segmentation-with-vlans` — Network segmentation datacenter

---

## 🔧 Core Workflow: Monitoring Stack Deployment

### Fase 1: Arsitektur Monitoring (2 Repo per Tool: Docker + Monolith)
```
Struktur repo per tool monitoring:
tool-{docker|monolith}/
├── README.md              # Overview + quick start
├── TUTORIAL.md            # Tutorial lengkap (🅰️ Otomatis + 🅱️ Manual)
├── docker-compose.yml     # [docker variant]
├── *.service              # [monolith variant] systemd units
├── provisioning/          # datasources, dashboards
├── agents/                # systemd unit templates untuk 170 server
├── dashboards/            # Grafana JSON dashboards
└── scripts/
    ├── setup-*.sh          # Install stack di server pusat
    ├── install-agent.sh    # Install agent di 1 target server
    └── deploy-bulk.sh      # Deploy agent ke N server via SSH
```

### Fase 2: Stack Selection (Berdasarkan Kebutuhan)

| Tool | Fungsi | Agent | Cocok Untuk |
|------|--------|-------|--------------|
| **Prometheus** | Metrics collection & alerting | Node Exporter | CPU/RAM/Disk metrics real-time |
| **Loki** | Log aggregation | Promtail | Centralized logging, search |
| **Netdata** | Real-time performance monitoring | Child Netdata (streaming) | Per-second granular metrics |
| **Uptime Kuma** | Uptime/availability monitoring | Pushbeat.sh (heartbeat) | Service availability check |

### Fase 3: Deployment ke 170 Server (Bulk Deploy Pattern)
```bash
# Server pusat: setup monitoring stack (Prometheus/Loki/Grafana)
./scripts/setup-monitoring-stack.sh

# Agent deployment ke seluruh 170 server via SSH loop
./scripts/deploy-bulk.sh servers.txt
# servers.txt berisi 170 IP address, satu per baris

# Verifikasi: cek berapa agent yang online
curl -s http://prometheus-server:9090/api/v1/targets | jq '.data.activeTargets | length'
```

### Fase 4: Dashboard & Alerting
```
1. Import Grafana dashboard JSON (dari dashboards/ folder)
2. Setup alert rules: CPU >90%, Disk >85%, service down >5 menit
3. Integrasi notifikasi: Telegram bot (untuk Bos), email, Slack (opsional)
4. Buat dashboard summary: "170-server health at a glance"
```

---

## 🔧 Core Workflow: Database Performance Tuning

### Fase 1: Baseline Assessment
```
1. Identifikasi jenis database (MySQL/PostgreSQL/MongoDB/Redis)
2. Ambil baseline metrics: query latency, connection pool usage, cache hit ratio
3. Identifikasi slow query log (queries >1 detik)
```

### Fase 2: Auto-Tuning berdasarkan Workload
```
MySQL:
- innodb_buffer_pool_size = 70-80% dari total RAM (untuk dedicated DB server)
- max_connections berdasarkan concurrent app instances
- slow_query_log ON untuk identifikasi bottleneck

PostgreSQL:
- shared_buffers = 25% dari total RAM
- effective_cache_size = 50-75% dari total RAM
- work_mem tuning berdasarkan concurrent query complexity

MongoDB:
- WiredTiger cache size tuning
- Index optimization (explain() analysis)

Redis:
- maxmemory-policy sesuai use case (LRU untuk cache, noeviction untuk queue)
- Persistence tuning (RDB vs AOF trade-off)
```

### Fase 3: Verifikasi & Monitoring Berkelanjutan
```
1. Re-benchmark setelah tuning (before/after comparison)
2. Setup continuous monitoring untuk detect regression
3. Dokumentasikan perubahan config + rationale
```

---

## 🔧 Core Workflow: Datacenter Ops (170-Server Context)

### Fase 1: RAID & Storage Sizing
```
- RAID 10: untuk database server (butuh IOPS tinggi + redundancy)
- RAID 6: untuk bulk storage/backup server (butuh kapasitas + fault tolerance 2 disk)
- Hot-spare disk: minimal 1 per storage pool untuk auto-rebuild
```

### Fase 2: UPS/NUT (Network UPS Tools) Monitoring
```
1. Setup NUT server di UPS utama
2. Deploy NUT client di seluruh server yang terhubung UPS yang sama
3. Automated graceful shutdown saat battery <20%
4. Alert Telegram saat power outage terdeteksi
```

### Fase 3: Datacenter Health Dashboard
```
Metrics wajib di-monitor untuk 170-server DC:
- Suhu ruangan (ambient temperature) — cegah overheat
- Kelembaban (humidity) — cegah kondensasi/corrosion
- Power consumption per rack (kWh)
- UPS battery status & estimasi runtime
- Network switch utilization per rack
```

---

## 🎬 Use Cases (Real-World Konteks 170-Server DC)

### Skenario 1: Deteksi Dini Server Down
Bos butuh tahu kalau ada server mati/unreachable SEBELUM dilaporkan user:
1. Deploy Uptime Kuma dengan heartbeat check tiap 60 detik ke 170 server
2. Alert otomatis ke Telegram Bos jika 1 server down >5 menit
3. Dashboard summary: "168/170 server online" real-time

### Skenario 2: Database Bottleneck di Aplikasi Laravel
Bos melihat aplikasi CI4/Laravel jadi lambat saat traffic tinggi:
1. Cek slow query log — identifikasi query mana yang bottleneck
2. Tuning `innodb_buffer_pool_size` berdasarkan available RAM
3. Add index untuk query yang sering dijalankan tanpa index
4. Re-benchmark: response time turun dari 2s → 200ms

### Skenario 3: AI-Powered Security Alerting untuk Lab OSINT
Academy AI/OSINT lab butuh monitoring keamanan otomatis:
1. Setup Loki untuk centralize semua log dari 170 server
2. Wiring DeepHat AI untuk analisis log pattern (anomaly detection)
3. Cron job tiap 15 menit: scan log baru, flag suspicious pattern
4. Alert Telegram jika terdeteksi brute-force attempt atau unusual access pattern

### Skenario 4: Capacity Planning untuk Ekspansi DC
Bos ingin tahu kapan perlu tambah server baru:
1. Monitor trend CPU/RAM/Disk utilization 3 bulan terakhir (Prometheus historical data)
2. Proyeksi growth rate berdasarkan trend
3. Rekomendasi: "Dalam 4 bulan, disk utilization akan mencapai 90% — sarankan tambah storage"

---

## 💡 Key Insights & Pitfalls

### ✅ Best Practices

| Aspek | Best Practice |
|-------|---------------|
| **Repo Naming** | Generic + variant (`netdata-docker`, `loki-logging-monolith`) — hindari brand prefix seperti "ccc-" |
| **Bulk Deployment** | Selalu test di 1-3 server dulu sebelum deploy ke seluruh 170 server |
| **Token Security** | Write token ke temp file SEKALI, reference via `$(cat /tmp/gh_token_file)` — revoke setelah selesai |
| **Dokumentasi Ganda** | TUTORIAL.md WAJIB punya 2 jalur: 🅰️ Otomatis (script) + 🅱️ Manual (step-by-step) |
| **Verifikasi via API** | Verify push via Contents API, bukan hanya exit status command |
| **Alert Fatigue** | Set threshold yang masuk akal (CPU >90% selama 5 menit, bukan spike sesaat) — hindari alert spam |

### ⚠️ Pitfalls (Hindari!)

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `git init` bikin branch `master` | Push gagal dgn "src refspec main does not match" | `git branch -m master main` sebelum push |
| Push sebelum repo dibuat di GitHub | Error "repository does not exist" | CREATE via API dulu, BARU push |
| `cp -r src/.* dest/` ikut narik `.git` | Corrupt git history di destination | `rm -rf dest/.git` lalu fresh `git init` |
| Token inline di command | Trigger GitHub secret scanner, approval timeout | Gunakan temp-file pattern (`/tmp/gh_token_file`) |
| `set -euo pipefail` + trap unset var | Script crash saat cleanup | Inisialisasi `TMP_DIR=""` di awal script |
| Tuning DB tanpa baseline | Tidak bisa ukur improvement, bisa jadi regression | SELALU benchmark before/after tuning |
| Monitoring tanpa alerting | Masalah baru diketahui setelah user komplain | Setup proactive alerting, bukan cuma dashboard pasif |

---

## 🎓 Learning Path (5 Minggu)

### Minggu 1: Monitoring Stack Fundamentals
- [ ] Load skill: `monitoring-stack-deployment`
- [ ] Deploy Prometheus + Grafana di server pusat (test environment dulu)
- [ ] Setup Node Exporter di 3-5 server sebagai pilot
- [ ] **Deliverable:** Dashboard basic (CPU/RAM/Disk) untuk 5 server

### Minggu 2: Log Aggregation & Centralization
- [ ] Load skill: `monitoring-stack-deployment` (Loki variant)
- [ ] Deploy Loki + Promtail agent ke pilot servers
- [ ] Setup log search dashboard di Grafana
- [ ] **Deliverable:** Centralized log search untuk 5 server (proof of concept)

### Minggu 3: Bulk Deployment ke 170 Server
- [ ] Buat `servers.txt` dengan 170 IP address
- [ ] Test `deploy-bulk.sh` untuk deploy agent ke batch kecil (10 server) dulu
- [ ] Full rollout ke seluruh 170 server
- [ ] **Deliverable:** Monitoring coverage 170/170 server + alert Telegram integration

### Minggu 4: Database Performance Tuning
- [ ] Load skill: `database-performance-tuning`
- [ ] Baseline assessment untuk DB production (MySQL/PostgreSQL)
- [ ] Terapkan tuning parameter sesuai workload
- [ ] **Deliverable:** Before/after benchmark report

### Minggu 5: Datacenter Ops & AI Security Observer
- [ ] Load skills: `datacenter-ops`, `security-ai-observer`
- [ ] Setup UPS/NUT monitoring untuk graceful shutdown
- [ ] Wiring DeepHat AI ke Loki cron alerts untuk anomaly detection
- [ ] **Deliverable:** Full DC health dashboard + AI-powered alert pipeline

---

## 📖 References & Learning Resources

### Official Docs
- Prometheus: https://prometheus.io/docs/
- Grafana Loki: https://grafana.com/docs/loki/
- Netdata: https://learn.netdata.cloud/
- Uptime Kuma: https://github.com/louislam/uptime-kuma
- NUT (Network UPS Tools): https://networkupstools.org/docs/

### Related Skills (Sudah Ada di Library)
- `devops/database-performance-tuning` — Auto-tune database
- `devops/datacenter-ops` — RAID, UPS/NUT, DC monitoring
- `devops/docker-laravel-automation` — Backup & health-check
- `devops/security-ai-observer` — AI-powered log analysis
- `devops/tuning-repo-publishing` — Publish tuning scripts sebagai repo terpisah
- `github-token-deploy-workflow` — Token security untuk GitHub push

---

## ✨ Success Criteria

Bos dinyatakan **mastered** skill ini ketika bisa:
- [ ] Deploy monitoring stack (Prometheus/Loki/Netdata) ke server baru dalam <15 menit
- [ ] Bulk-deploy agent ke 170 server dalam 1 kali eksekusi script (tanpa manual per-server)
- [ ] Tuning database untuk improve query performance 2x+ dari baseline
- [ ] Setup automated alerting yang actionable (bukan alert fatigue)
- [ ] Buat capacity planning report berdasarkan trend data historis

---

**Status:** Ready to Learn (Tier 2 - Intermediate)  
**Estimated Time to Mastery:** 5 minggu @ 6-8 jam/minggu  
**Next Milestone:** Tier 3 (Wazuh SIEM + Centralized Syslog + Network Segmentation)
