# Database Tuning Repository Template

Struktur standar untuk setiap repo tuning database.

## Minimal File Structure

```
<db-name>-tuning-monolith/
├── README.md                          # Quick start + overview
├── scripts/
│   └── <db>_tuning.sh                # Main tuning script
├── docs/
│   ├── INSTALLATION.md                # Prerequisites + setup
│   ├── USAGE.md                       # Run script + verify
│   └── TROUBLESHOOTING.md             # Errors + solutions
├── LICENSE                            # MIT License
├── .gitignore                         # Exclude logs/backups
└── (optional) config/
    └── <db>.example.conf              # Config template
```

## README.md Template

```markdown
# [Database] Tuning - Monolith

**Script otomatis untuk optimasi [Database] di server Ubuntu 22.04/24.04**

## ✨ Fitur

- ✅ Memory optimization
- ✅ Connection pooling
- ✅ Auto backup + rollback
- ✅ Verification checks

## 🚀 3 Langkah Cepat

### 1️⃣ Clone
\`\`\`bash
git clone https://github.com/vanderstark/<db>-tuning-monolith.git
cd <db>-tuning-monolith
\`\`\`

### 2️⃣ Run
\`\`\`bash
sudo bash scripts/<db>_tuning.sh
\`\`\`

### 3️⃣ Verify
\`\`\`bash
# Check result
# ...command...
\`\`\`

## 📊 Results

| Parameter | Before | After |
|-----------|--------|-------|
| ... | ... | ... |

## 📚 Documentation

- [INSTALLATION.md](./docs/INSTALLATION.md)
- [USAGE.md](./docs/USAGE.md)  
- [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

## License

MIT License
```

## docs/INSTALLATION.md Template

```markdown
# INSTALLATION.md — Setup [Database] Tuning

## ✅ Prerequisites

\`\`\`bash
# Check version
[db] --version
lsb_release -a
free -h
nproc
\`\`\`

Minimal: Ubuntu 22.04/24.04, [DB] version X+, 2GB RAM+, root/sudo

## 🚀 Installation Steps

### Step 1: Install [Database]
\`\`\`bash
sudo apt update
sudo apt install -y [db]
\`\`\`

### Step 2: Verify Running
\`\`\`bash
sudo systemctl status [db]
\`\`\`

### Step 3: Clone Repo
\`\`\`bash
git clone https://github.com/vanderstark/<db>-tuning-monolith.git
cd <db>-tuning-monolith
chmod +x scripts/<db>_tuning.sh
\`\`\`

### Step 4: Pre-Tuning Check

\`\`\`bash
# Check current parameters
# ...command...
\`\`\`

Lanjut ke **[USAGE.md](./USAGE.md)**!
```

## docs/USAGE.md Template

```markdown
# USAGE.md — Cara Menjalankan

## 🎯 3 Langkah Eksekusi

### Step 1: Run Script
\`\`\`bash
cd <db-name>-tuning-monolith
sudo bash scripts/<db>_tuning.sh
\`\`\`

Output:
\`\`\`
==> [Database Tuning] Starting...
==> Backup created: ...
==> Tuning complete!
\`\`\`

### Step 2: Verify Results
\`\`\`bash
# Check parameter X
\`\`\`

### Step 3: Monitor
\`\`\`bash
# Watch status
# ...command...
\`\`\`

## ⚙️ Opsi Konfigurasi

Edit script line XXX:
\`\`\`bash
PARAM=value
\`\`\`

## 🔄 Rollback

\`\`\`bash
sudo cp /var/backups/<db>_tuning/DATE/config /etc/<db>/
sudo systemctl restart <db>
\`\`\`

Lihat [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) untuk detail.
```

## docs/TROUBLESHOOTING.md Template

```markdown
# TROUBLESHOOTING.md — Error & Solusi

## ❌ Error: "Script not found"

**Solusi:** Check permissions & path

## ❌ Error: "[DB] failed to start"

**Penyebab:** Config syntax error
**Solusi:** Restore backup

## ✅ Normal Warnings

- Warning X: expected behavior
- Notice Y: OK

**Cek `/var/log/<db>_tuning.log` untuk detail.** 🔧
```

## Script Template Skeleton

```bash
#!/usr/bin/env bash
#
# <db>_tuning.sh — [Database] Performance Tuning
# Target: Ubuntu 22.04/24.04 + [DB Version]
# Usage: sudo bash <db>_tuning.sh
#
set -euo pipefail

BACKUP_DIR="/var/backups/<db>_tuning/$(date +%Y%m%d_%H%M%S)"
LOG="/var/log/<db>_tuning.log"

echo "==> [<DB> Tuning] Starting $(date)" | tee -a "$LOG"

# ---- Preflight ----
[[ $EUID -eq 0 ]] || { echo "ERROR: Run with sudo"; exit 1; }
command -v <db> >/dev/null 2>&1 || { echo "ERROR: <DB> not found"; exit 1; }

mkdir -p "$BACKUP_DIR"
# Backup config here
echo "==> Backup created: $BACKUP_DIR" | tee -a "$LOG"

# ---- Detect Hardware ----
CPU_CORES=$(nproc)
TOTAL_MEM_MB=$(($(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024))
echo "==> CPU=$CPU_CORES Mem=${TOTAL_MEM_MB}MB" | tee -a "$LOG"

# ---- Tuning ----
# Write optimized config here

# ---- Kernel Tuning ----
# sysctl adjustments here

# ---- Restart ----
systemctl restart <db> && echo "==> <DB> restarted" | tee -a "$LOG"

# ---- Verification ----
sleep 2
if systemctl is-active --quiet <db>; then
  echo "==> <DB> is running ✅" | tee -a "$LOG"
else
  echo "ERROR: <DB> failed to start" | tee -a "$LOG"
  exit 1
fi

echo "==> COMPLETE!" | tee -a "$LOG"
```

---

**Gunakan template ini sebagai starting point untuk setiap repo tuning database baru.**
