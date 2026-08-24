---
name: tuning-repo-publishing
description: Build & publish tuning scripts as separate GitHub repos.
---

# Tuning Script Repo Publishing

**Use when:** User asks for performance tuning scripts (web servers, databases) + wants each as a separate GitHub repo + beginner tutorial for each.

**Behavior:** Create repo per komponen (1 MySQL repo, 1 PostgreSQL repo, etc.). Each repo has auto-tuning script, kernel+limit settings, complete tutorial (INSTALLATION/USAGE/TROUBLESHOOTING), and lives at `vanderstark/<komponen>-tuning-<variant>` on GitHub.

---

## User Preferences (vanderstark)

- **1 komponen = 1 repo** — not one mega-repo with multiple databases. User correction: "1 data base 1 repo".
- **Sequence: monolith first, then Docker variants** — user specified order, not parallel.
- Chat style JARVIS: open "Yes, Bos." + greeting English (Good morning/afternoon/evening/night, Bos) + body Bahasa Indonesia.

---

## Repo Naming

```
<komponen>-tuning-monolith  # e.g. mysql-tuning-monolith
<komponen>-tuning-docker    # e.g. mysql-tuning-docker
```

**Historical:** Apache/Nginx tuning + Docker done (4 repos). MySQL/PostgreSQL/MongoDB/Redis monolith done (4 repos). Docker DB variants pending.

---

## File Structure Per Repo

```
README.md                          # Badges, 3-langkah cepat, feature table (before/after tuning)
scripts/<komponen>_tuning.sh       # Auto-tuning bash script
docs/INSTALLATION.md               # Setup <software> + pre-check
docs/USAGE.md                      # Run, verify, monitoring, rollback
docs/TROUBLESHOOTING.md            # Common errors + solutions
LICENSE                            # MIT "Copyright (c) 2026 Eko Kurnia (vanderstark)"
.gitignore                         # *.conf.bak, *.conf.old, /var/backups/, /var/log/, .env, *.pem, *.key
```

---

## Script Pattern (Bash, `set -euo pipefail`)

1. **Preflight checks:**
   - `[[ $EUID -eq 0 ]]` — require root
   - `command -v <binary>` — software installed?

2. **Auto-backup config** BEFORE any edit:
   ```bash
   BACKUP_DIR="/var/backups/<db>_tuning/$(date +%Y%m%d_%H%M%S)"
   mkdir -p "$BACKUP_DIR"
   cp <config_files> "$BACKUP_DIR/"
   ```

3. **Detect hardware** (CPU, RAM):
   ```bash
   CPU_CORES=$(nproc)
   TOTAL_MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
   TOTAL_MEM_MB=$((TOTAL_MEM_KB / 1024))
   ```

4. **Calculate tuning values** — see `references/db-tuning-parameters.md` for % per database.

5. **Write config** (either new `.conf.d/` file or update main config).

6. **Kernel tuning** → `/etc/sysctl.d/99-<x>-tuning.conf` + `sysctl --system`.

7. **Ulimit tuning** → `/etc/security/limits.d/99-<x>.conf`.

8. **Restart service**:
   ```bash
   systemctl restart <service>
   sleep 2-3
   ```

9. **Verify** (wait a bit, then test):
   - MySQL: `mysql -e "SELECT 1;"`
   - PostgreSQL: `sudo -u postgres psql -c "SHOW shared_buffers;"`
   - MongoDB: `mongosh --eval "db.serverStatus().wiredTiger.cache"`
   - Redis: `redis-cli PING`

10. **Rollback on failure** (restore backup, restart, exit 1).

11. **Log output** → `/var/log/<x>_tuning.log` with timestamps.

---

## GitHub Publish Workflow (Token)

**Critical order** (user ran into errors when reordered):

```bash
# 1. Commit FIRST (else: "src refspec main does not match any")
cd /opt/data/<repo>
git add . && git commit -m "Initial: <Komponen> tuning script..."
git branch -M main

# 2. Create repo via GitHub API (else: "Repository not found" on push)
curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"<repo>","private":false,"description":"<DB> tuning script..."}'

# 3. Push with token in URL
git push https://oauth2:$TOKEN@github.com/vanderstark/<repo>.git main
```

### Token Handling
- Store: `/tmp/gh_token_file` chmod 600
- Delete after all pushes: `rm /tmp/gh_token_file`
- User must revoke token later: `github.com/settings/tokens`

### Repo Description Template
```
<DatabaseName> tuning script for Ubuntu - Auto-optimize <feature1>, <feature2>, <feature3>
```
E.g. "MySQL tuning script for Ubuntu - Auto-optimize buffer pool, connections, kernel parameters"

---

## Pitfalls & Workarounds

| Error | Cause | Fix |
|-------|-------|-----|
| `src refspec main does not match any` | No commits yet, or branch name wrong | Commit first, `git branch -M main`, THEN push |
| `Repository not found` (on push) | Repo not created in GitHub yet | Use GitHub API curl to create repo FIRST |
| `could not read Username for 'https://github.com'` | URL missing token creds | Use `https://oauth2:$TOKEN@github.com/...` |
| Security scan flags PAT | Token visible in command | Explain repo & ask user approval before running |
| Approval timeout (long combined command) | Too many operations chained | Split: commit, then create-repo curl, then push |

---

## Tutorial Content (Each `docs/` file)

### INSTALLATION.md
- Minimal requirements (OS version, software version, RAM, root/sudo)
- Install commands (apt-get / brew / yum)
- Verify installed: version checks, status checks
- Pre-tuning check: hardware (`free -h`, `nproc`), current config

### USAGE.md
- 3 steps: clone → run script → verify
- Script output example (expected log output)
- Verification commands per database (show config changed)
- Monitoring (real-time stats commands)
- Rollback procedure

### TROUBLESHOOTING.md
- Common errors & solutions (alphabetical)
- Check logs path
- Tuning tips (if slow still, if memory high, if connections maxed)

### README.md
- Top: badges (database name + Ubuntu version)
- Bullet list of features (✅ each setting tuned)
- Quick 3-step summary (clone, run, verify)
- Example before/after table (tuning results)
- Saftey features (auto-backup, rollback, validation)
- Requirements checklist
- Link to docs

---

## 🆕 Extended Patterns (2026-08-15)

### Cronjob Config Repository Pattern

Similar to DB tuning repos, cronjob configurations can be versioned & deployed:

1. **Export settings** → JSON (cronjob-settings.json)
2. **Create private repo** → `vanderstark/hermes-config-schedule` (private)
3. **Deploy via GitHub API** → curl POST to create repo, then push

```bash
# Export live cronjob config
cronjob action=list  # → capture all 7 jobs

# Create repo (private)
curl -X POST -H "Authorization: token $TOKEN" \
  -d '{"name":"hermes-config-schedule","private":true,"description":"Hermes cronjob schedule backup"}' \
  https://api.github.com/user/repos

# Commit & push
cd /opt/data/hermes-config-export
git init && git add . && git commit -m "Cronjob config: 7 jobs"
git branch -M main
git push https://oauth2:$TOKEN@github.com/vanderstark/hermes-config-schedule.git main
```

**Key difference from DB tuning:** Private repo (config may contain sensitive paths/schedule), not public tutorial.

### Drone Development Skill from GitHub Search

When user wants a new skill from GitHub resources:

1. **Search GitHub** → Find 3+ relevant repos
2. **Create comprehensive skill** → Combine into one umbrella (e.g., `drone-development`)
3. **Structure:** SKILL.md + references/ + templates/ + scripts/
4. **Push to skills backup** → `vanderstark/hermes-skills-backup` (existing repo)

This demonstrates the skill-authoring workflow: search → combine → structure → deploy.

---

## References

See `references/db-tuning-parameters.md` for:
- MySQL: buffer pool %, max_connections, query_cache, slow log threshold
- PostgreSQL: shared_buffers %, effective_cache_size %, work_mem sizing, autovacuum
- MongoDB: WiredTiger cache %, max connections, compression, oplog size
- Redis: maxmemory %, eviction policy, AOF vs RDB, max clients
- Web servers (Apache/Nginx): worker processes, keep-alive, buffer sizes

