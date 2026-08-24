# README Section Template — Backup, Restore & Monitoring

Drop this into the project's **single root README.md**, just above the security/keamanan section.
Replace `<project>` and paths as needed. Keep Indonesian if the user's docs are Indonesian.

---

## 🗃️ Backup, Restore & Monitoring Otomatis

Semua script ada di folder `backups/scripts/`.

### 1. Backup Database (Otomatis Harian 02:00 WIB)
```bash
# Jalankan manual
./backups/scripts/backup-db.sh

# Atau pasang cron (butuh sudo)
./backups/scripts/setup-cron.sh
```
- Output: `backups/db_<project>_YYYYMMDD_HHMMSS.sql.gz`
- Retensi: backup >14 hari otomatis dihapus
- Verifikasi: integritas gzip dicek sebelum disimpan

### 2. Restore Database
```bash
./backups/scripts/restore-db.sh backups/db_<project>_20260820_020000.sql.gz
```
⚠️ Restore menimpa seluruh data. Konfirmasi dengan mengetik `YA`.

### 3. Health Check (Tiap 15 Menit)
```bash
./backups/scripts/healthcheck.sh
```
Mengecek: container up/down, HTTP app, MySQL ping, Redis ping, disk usage. Log di `backups/health.log`.

### Cron Schedule (setelah `setup-cron.sh`)
| Waktu | Job |
|-------|-----|
| 02:00 WIB | Backup DB |
| */15 menit | Health check |
| Senin 03:00 | Rotasi log lama |

---

## Notes for the agent

- Insert with `patch` mode=replace, anchoring on the existing `## 🔐 ...Keamanan` heading so the new section lands directly above it.
- Do NOT create `backups/README.md` — the user explicitly does not want multiple READMEs ("jangan ada 2 bikin pusing"). One root README, subsections only.
- After patching, commit and push in a single terminal call, then delete any token file.
