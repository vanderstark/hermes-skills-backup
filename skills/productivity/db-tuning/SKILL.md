---
name: db-tuning
description: "Database tuning: 1 repo per DB, 3-doc format."
trigger: database tuning, optimize database, database performance
category: productivity
author: Hermes Agent
version: "1.0"
---

# Database Tuning — Methodology & Repo Pattern

Standardized approach to database performance tuning with Hermes Agent.

## 🎯 Core Pattern: 1 Repository Per Database

Each database gets its own GitHub repository to enable independent versioning, CI/CD, and clear ownership.

| Database | Monolith Repo | Docker Repo |
|----------|--------------|-------------|
| MySQL | `vanderstark/mysql-tuning-monolith` | *(Docker coming)* |
| PostgreSQL | `vanderstark/postgresql-tuning-monolith` | *(Docker coming)* |
| MongoDB | `vanderstark/mongodb-tuning-monolith` | *(Docker coming)* |
| Redis | *(In Progress)* | *(In Progress)* |

---

## 📖 Tutorial Standard: 3-Document Format

Every tuning repository MUST include exactly 3 documentation files:

1. **`README.md`** — Quick start, fitur overview, contoh hasil
2. **`docs/INSTALLATION.md`** — Setup & prasyarat checklist  
3. **`docs/USAGE.md`** — Eksekusi, verifikasi, opsi konfigurasi
4. **`docs/TROUBLESHOOTING.md`** — Error, solutions, rollback

---

## 🧩 Monolith vs Docker Split

### **Monolith** (`-monolith` suffix)
Direct OS tuning script. Best for: Host optimization.

```
mysql-tuning-monolith/
├── README.md
├── scripts/mysql_tuning.sh
├── docs/{INSTALLATION,USAGE,TROUBLESHOOTING}.md
├── LICENSE
└── .gitignore
```

### **Docker** (`-docker` suffix) — Coming
Docker image with tuning baked-in. Best for: Containerized deploys.

---

## ✅ Quality Standards

- [ ] 1 Repo per database (separate GitHub repos)
- [ ] 3-Doc format (README + 3 docs)
- [ ] Functional script (works standalone)
- [ ] Auto-backup before edit
- [ ] Verification after tuning
- [ ] Clear rollback procedure
- [ ] Public repo, MIT License
- [ ] Token safety (temp use, never stored)

---

## 🔐 Safety Requirements

✅ Auto backup: `/var/backups/<db>_tuning/DATE/`
✅ Config validation before restart
✅ Graceful rollback on error  
✅ Connectivity test after tuning
✅ Logging to `/var/log/<db>_tuning.log`
✅ Root/sudo only
✅ No secrets in code

---

## 📋 Repository Naming

```
<dbname>-tuning-[monolith|docker]
```

Example: `mysql-tuning-monolith`, `postgresql-tuning-docker`

---

## 📞 Related Skills

- `mysql-tuning-monolith` — MySQL
- `postgresql-tuning-monolith` — PostgreSQL  
- `mongodb-tuning-monolith` — MongoDB
- *(Redis, Elasticsearch coming)*

---

## 🎯 When to Use

User says "tune MySQL", "optimize database", "improve DB performance":
1. Identify database type
2. Choose monolith or Docker variant
3. Load skill: `skill_view mysql-tuning-monolith`
4. Follow 3-step execution: Clone → Run → Verify

---

**Principle:** 1 repo per database keeps concerns clear, versioning independent, CI/CD focused. 3-doc tutorial ensures reproducible, user-friendly deployments.