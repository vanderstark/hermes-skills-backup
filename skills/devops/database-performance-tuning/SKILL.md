---
name: database-performance-tuning
description: "Auto-tune MySQL/PostgreSQL/MongoDB/Redis databases."
trigger: "optimize database performance, scale connections, reduce latency, tune memory buffers, prepare for production load"
category: devops
author: Jarvis (Hermes Agent)
version: "1.0"
---

# Database Performance Tuning

End-to-end methodology for auto-tuning relational (MySQL, PostgreSQL) and NoSQL (MongoDB, Redis) databases. Generates **monolith scripts** (for host) and **Docker variants** — each database engine gets its own repo pair.

## When to Use

- Optimize MySQL/MariaDB `innodb_buffer_pool_size`, `max_connections`, query cache
- Tune PostgreSQL `shared_buffers`, `effective_cache_size`, `work_mem`
- Configure MongoDB WiredTiger cache, profiling, index usage
- Set Redis `maxmemory`, eviction policy, persistence
- Production-ready: auto-scale params based on CPU/RAM hardware
- Multi-engine environments: separate repo per database (not monolithic)

## Core Pattern

### Repo Structure (Monolith + Docker)

One database = two repos:
```
vanderstark/<db>-tuning-monolith/         ← Host-based script + tutorial
vanderstark/<db>-tuning-docker/           ← Docker image + compose
```

Each is **independent** — no cross-repo dependencies, self-contained scripts, self-contained docs.

### Monolith Repo Layout

```
<db>-tuning-monolith/
├── README.md                     ← Feature summary + before/after table
├── scripts/<db>_tuning.sh       ← Bash script (hardware auto-detect + tune)
├── docs/
│   ├── INSTALLATION.md          ← OS setup, verify DB installed & running
│   ├── USAGE.md                 ← 3-step execution, verify results, monitor
│   └── TROUBLESHOOTING.md       ← Error → cause → fix mapping
├── configs/<db>/                ← Optional template configs
├── LICENSE (MIT)
└── .gitignore
```

### Docker Repo Layout

```
<db>-tuning-docker/
├── README.md
├── Dockerfile                    ← Build image + run tuning
├── docker-compose.yml           ← Service + resource limits + volumes
├── docs/
│   ├── DOCKER_BUILD.md
│   └── DEPLOYMENT.md
├── LICENSE
└── .gitignore
```

## Workflow

### Phase 1: Monolith Script

**Auto-detection:**
```bash
CPU_CORES=$(nproc)
RAM_GB=$(free -h | grep Mem | awk '{print $2}')
BUFFER_POOL_MB=$(( (RAM_MB * 70) / 100 ))    # 70% of RAM
MAX_CONNECTIONS=$(( CPU_CORES * 50 ))        # 50× cores (min 200)
```

**Core actions:**
1. Detect hardware (CPU, RAM, disk)
2. Calculate optimal params (buffer pool 70% RAM, max conn × CPU factor)
3. Backup old config to `/var/backups/<db>_tuning/YYYYMMDD_HHMMSS/`
4. Write new config + kernel tuning (`sysctl`, `ulimits`)
5. Validate syntax (e.g., `mysqld --help`, `nginx -t`)
6. Restart service + verify connection
7. Log results to `/var/log/<db>_tuning.log`
8. Rollback on error (restore from backup)

**Tutorial structure (immutable across all DBs):**
- `INSTALLATION.md` — "Do I have the binary? Can I connect?"
- `USAGE.md` — "Run script → Verify params changed → Monitor performance"
- `TROUBLESHOOTING.md` — "Error X means Y, do Z"
- `README.md` — Feature list, before/after metrics table, quick-start checklist

### Phase 2: Docker Variant

1. **Dockerfile** — Base image + install binary + COPY tuning script + RUN script (at build or start)
2. **docker-compose.yml** — Service + resource limits (CPU, memory) + volume mounts (config, data) + health check
3. **Docs** — DOCKER_BUILD.md (build steps), DEPLOYMENT.md (run examples, scale)

## Expected Results

Example MySQL (8 CPU, 16GB RAM):

| Parameter | Before | After | Lift |
|-----------|--------|-------|------|
| Buffer Pool | 128M | 11GB | 86× |
| Max Connections | 151 | 400 | 2.6× |
| Query Cache | Off | 256M | On |
| Sort Buffer | 256K | 4M | 16× |

**Performance** — Read 30-50% faster, write 20-30% faster, handle 3-5× more connections.

## Implementation Checklist

### Monolith Script

- [ ] Bash with `set -euo pipefail`
- [ ] Root check: `[[ $EUID -eq 0 ]]`
- [ ] Binary check: `command -v <binary>`
- [ ] Hardware detect: `nproc`, `grep MemTotal /proc/meminfo`
- [ ] Clamp buffer pool: min 256M, max RAM - 2GB
- [ ] Backup config to dated `/var/backups/` dir
- [ ] Write new config (append to existing or create `/etc/conf.d/99-tuning.cnf`)
- [ ] Apply kernel tuning: `/etc/sysctl.d/99-<db>-tuning.conf`
- [ ] Raise ulimits: `/etc/security/limits.d/99-<db>.conf`
- [ ] Validate syntax (database-specific check)
- [ ] Restart service + sleep 2s + verify connection
- [ ] Log all steps to `/var/log/<db>_tuning.log`
- [ ] On error: rollback from backup, exit 1

### Docs (Standard Pattern)

**INSTALLATION.md:**
1. Verify binary installed: `<db> --version`
2. Verify running: `systemctl status <db>`
3. Clone repo
4. Check script executable: `chmod +x scripts/<db>_tuning.sh`

**USAGE.md:**
1. Run: `sudo bash scripts/<db>_tuning.sh`
2. Verify: `<db> -e "SHOW VARIABLES LIKE 'buffer_pool%';"` (or equivalent)
3. Monitor: `tail -f /var/log/<db>_tuning.log`

Expected output log (show full sample in docs).

**TROUBLESHOOTING.md:**
- Map each error: "Connection refused" → MySQL not running → `sudo systemctl start mysql`
- Params not changing → Config not loaded → Check config path, restart, verify
- Buffer pool too large → RAM exhausted → Rollback, re-run script with lower percentage

**README.md:**
- Feature list (what script does)
- Before/after table (metrics)
- 3-step checklist (install, run, verify)

### Docker

- [ ] Dockerfile: `FROM ubuntu:24.04` + install + COPY tuning.sh + RUN/CMD
- [ ] Expose ports (3306 for MySQL, 5432 for PostgreSQL, etc.)
- [ ] Health check (SQL query: `mysql -e "SELECT 1"`)
- [ ] docker-compose: `cpus`, `memory` limits, volume mounts, restart policy
- [ ] docs/DOCKER_BUILD.md — build command, image size
- [ ] docs/DEPLOYMENT.md — run single + scale + monitor examples

## Pitfalls

⚠️ **Auto-detection machine-dependent.** Log calculated values before restart. Show Bos the numbers so he can override if needed (e.g., "detected 16GB but I only want to use 4GB").

⚠️ **Buffer pool oversizing crashes the container.** Always clamp to `(RAM_MB - 2048)` to leave headroom. Default to 70%, not 100%.

⚠️ **Restart = downtime.** For production, warn in docs. Consider offline migration (dump → reload) instead of in-place restart.

⚠️ **Config paths vary widely.** MySQL: `/etc/mysql/my.cnf` vs `/etc/mysql/conf.d/`. PostgreSQL: `/etc/postgresql/X/main/postgresql.conf`. MongoDB: `/etc/mongod.conf`. Don't hardcode; verify per OS/version.

⚠️ **Kernel tuning persists.** `sysctl -w` is temporary (survives until next reboot). `/etc/sysctl.d/` is permanent. Script should use both for testing + persistence.

⚠️ **Slow query log path inconsistent.** Check `SHOW VARIABLES LIKE 'slow_query_log_file'` first, don't assume default path.

⚠️ **One repo per database.** Do NOT create one mega-repo with all DBs. Each database gets its own monolith repo + Docker repo. Rationale: independence, clarity, reusability.

## References

Linked from skill:
- `references/hardware-calc.md` — Formulas for buffer pool, max conn
- `references/error-mapping.md` — Collated error → fix from all TROUBLESHOOTING docs
- `references/docker-resource-limits.md` — Memory/CPU tuning for containers
- `templates/Dockerfile.mysql` — Starter template
- `templates/docker-compose.example.yml` — Starter compose file
- `scripts/hardware-detect.sh` — Reusable detection logic

## Live Examples

See production repos:
- `vanderstark/mysql-tuning-monolith` — MySQL working example
- (PostgreSQL, MongoDB, Redis follow same pattern)

---

**Usage path:**
1. Load this skill when starting a new `<db>-tuning-monolith` repo
2. Copy template layout
3. Customize script for target database (MySQL vs PostgreSQL vs MongoDB vs Redis)
4. Follow checklist — don't skip docs or backup
5. Test: run script, verify params, rollback check
6. Create Docker variant using Phase 2 pattern
7. Push each repo separately to GitHub

Ready to automate database tuning! 🚀