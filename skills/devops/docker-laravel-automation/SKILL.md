---
name: "docker-laravel-automation"
description: "Backup, health-check & cron ops for Dockerized Laravel apps."
version: 1.0.0
author: "Hermes Agent"
license: "MIT"
tags:
  - devops
  - docker
  - laravel
  - backup
  - monitoring
  - automation
---

# Docker Laravel Automation

Reusable backup, restore, and health-monitoring scripts for Laravel applications deployed via Docker Compose. Built from the Polri LLM Gateway production rollout.

## When to use
User asks to add backup/restore/monitoring/cron automation to a Dockerized Laravel (or similar PHP/Docker Compose) app.

## Script set (copy into `backups/scripts/` of the target repo)

1. **backup-db.sh** — mysqldump inside the DB container, gzip, integrity-check the archive, rotate backups older than `RETENTION_DAYS` (default 14), log to `backups/backup.log`. Use `--single-transaction --quick --routines --triggers --events`.
2. **restore-db.sh** — takes a `.sql.gz` path, verifies gzip integrity, requires typed `YA` confirmation before overwriting the DB, then pipes into `docker exec -i <mysql_container> mysql`.
3. **healthcheck.sh** — checks each container in a list is `docker ps`-visible, curls the app URL for 200/302, `mysqladmin ping`, `redis-cli ping`, and disk usage (warns >85%). Exit 0 = healthy, 1 = any failure. Alerts to `backups/health.log`.
4. **setup-cron.sh** — writes `/etc/cron.d/<project>` with: daily 02:00 backup, health check every 15 min, weekly log rotation. Requires sudo; prints the crontab it wrote.

## Configuration (top of each script)
```bash
DB_CONTAINER="<project>-mysql"   # must match docker-compose container_name exactly
DB_NAME="<project>_db"
DB_USER="root"
DB_PASS="<from .env / docker-compose>"
RETENTION_DAYS=14
APP_URL="http://localhost:8000"
```
Container names MUST match `container_name:` in docker-compose.yml exactly — the #1 source of false "container DOWN" alarms.

## Standard layout
```
project/
└── backups/
    ├── scripts/{backup-db.sh, restore-db.sh, healthcheck.sh, setup-cron.sh}
    ├── backup.log
    └── health.log
```
After writing scripts, always `chmod +x backups/scripts/*.sh`.

## README integration
Append a "Backup, Restore & Monitoring" section to the project's SINGLE root README.md — see `references/readme-section-template.md`. Never create a second README per subsystem; users find split docs confusing and will ask you to merge them.

## Pitfalls
- **Docker daemon unreachable in sandboxed environments**: healthcheck reports all containers DOWN with "Cannot connect to the Docker daemon". Environment limitation, not a script bug — validate logic (exit codes, log format) instead of rewriting the script.
- gzip-verify BEFORE touching the live DB; corrupt archives silently truncate restores.
- Use `write_file` for multi-line bash scripts, not heredoc-in-terminal — heredocs with `$` and backticks get mangled.
- Never inline a GitHub PAT in the push command; use a token file and delete it after push.

## References
- `references/readme-section-template.md` — drop-in Markdown section documenting backup/restore/health commands and the cron schedule table.
