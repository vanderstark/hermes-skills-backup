# 🔄 Hermes Skills & Plugins Backup — Restore Sekali Panggil

> **Satu repo GitHub = seluruh skill, plugin, dan konfigurasi Hermes Bos.**
> Install ulang Hermes? Cukup clone repo ini & jalankan `install.sh` — semua kembali tanpa ribet mencari link satu per satu.

---

## 🚀 Cara Restore (Setelah Install Hermes Baru)

### Cara 1 — Langsung dari GitHub (paling mudah)

```bash
git clone https://github.com/vanderstark/hermes-skills-backup.git
cd hermes-skills-backup
bash install.sh --from-github
```

### Cara 2 — Dari folder lokal

```bash
bash install.sh
```

### Opsi tambahan

| Flag | Fungsi |
|---|---|
| `--from-github` | Clone langsung dari GitHub lalu restore |
| `--skill-only` | Restore skill saja (skip plugins) |
| `--dry-run` | Simulasi — cek apa yang akan di-restore tanpa menulis |

---

## 📦 Isi Repo

```
hermes-skills-backup/
├── install.sh          ← 🚀 script restore otomatis (sekali jalan)
├── README.md           ← ← dokumen ini
├── AGENTS.md           ← project rules + aktivasi Task Observer
└── skills/             ← 📁 SEMUA skill (1884 SKILL.md, 114MB)
    ├── autonomous-ai-agents/
    ├── creative/
    ├── finance/
    ├── productivity/
    ├── science/
    ├── security/
    ├── software-development/
    └── ... (23 kategori)
└── plugins/            ← 📁 SEMUA plugin (74 file, 716KB)
```

---

## 🧠 Cara Kerja `install.sh`
56|56|

## 📚 Materi Pembelajaran Terbaru (Ditambahkan 24 Agustus 2026)

Berikut adalah materi pembelajaran yang telah disinkronisasi ke repo ini:

### 1. API Security & Penetration Testing
- **File:** `observations/notes/API_SECURITY_PENTEST_LANJUTAN.md`
- **Level:** Intermediates → Advanced (8–10 minggu)
- **Topik:** OWASP API Top 10, JWT/OAuth bypass, BOLA/IDOR/BFLA, GraphQL DoS, Rate Limit bypass, CI/CD integration
- **Deliverable:** `API_PENTEST_REPORT_FINAL.pdf` + 10 Sigma finding documents
- **Skill Asli:** `security/api-security`, `security/pentest-tools`, `security/reverse-skill/api-security`

### 2. Machine Learning Operations (Advanced)
- **File:** `observations/notes/MLOPS_ADVANCED_LANJUTAN.md`
- **Level:** Intermediates → Advanced (10–12 minggu)
- **Topik:** lm-eval-harness benchmarking, W&B experiment tracking, hyperparameter sweeps, model registry, CI/CD MLOps, vLLM deployment, speculative decoding
- **Deliverable:** `model-benchmark-report.pdf` + `sweep-report-indobert.pdf` + Indo-LLaMA-7B QA model
- **Skill Asli:** `mlops/evaluation/evaluating-llms-harness`, `mlops/evaluation/weights-and-biases`, `mlops/inference/serving-llms-vllm`

### 3. Threat Hunting & Detection Engineering
- **File:** `observations/notes/THREAT_HUNTING_LANJUTAN.md`
- **Level:** Intermediates → Advanced (8–10 minggu)
- **Topik:** ATT&CK mapping, hypothesis-driven hunting, Sigma/YARA rule engineering, SIEM query design, Atomic Red Team verification, detection pipeline
- **Deliverable:** `sigma-rules-pack-indonesian-polri.yaml` + `threat-hunt-exercise-report.pdf` + Wazuh dashboard
- **Skill Asli:** `security/reverse-skill/threat-hunting`, `malware-analysis`, `security/pentest-tools`

---

## 🧠 Cara Kerja `install.sh`
57|1. **Deteksi** `HERMES_HOME` (default `~/`)
58|2. **Restore** `skills/` → `$HERMES_HOME/skills/`
59|3. **Restore** `plugins/` → `$HERMES_HOME/plugins/`
60|4. **Restore** `AGENTS.md` → `$HERMES_HOME/AGENTS.md` (aktivasi Task Observer)
61|
62|---
63|
64|## 📝 Skill Terbaru Ditambahkan (24 Agustus 2026)
65|
66|- **Research & AI LabOps (OSINT & R&D)**
67|- **Machine Learning Ops (MLOps) GPU Server**
68|

6. **Verifikasi** jumlah SKILL.md & file plugin

> ⚠️ Folder yang sudah ada **tidak dihapus** — di-backup dulu dengan nama `skills.bak-<tanggal>`. Aman.

---

## 🤔 Kenapa Repo Ini Ada?

Bos tidak ingin **ribet mencari link skill satu per satu** saat install ulang Hermes. Dengan repo ini:

- ✅ **1 repo = semua skill + plugin + rules**
- ✅ **1 perintah** = restore lengkap
- ✅ Task Observer, custom skills (rocketpy, scrapegraph-ai, dsb), dan semua bundled skill tersimpan
- ✅ Tanpa `.venv` / video / file besar → efisien (34MB terkompresi)

---

## 🔄 Update Backup (Saat Ada Skill Baru)

Setelah Hermes menambah/mengubah skill, update repo:

```bash
# Dari folder repo backup:
rsync -a --exclude='.venv' --exclude='.git' --exclude='__pycache__' \
  --exclude='.curator_backups' --exclude='*.mp4' --exclude='*.tar.gz' \
  /opt/data/skills/ skills/
cp /opt/data/AGENTS.md AGENTS.md
git add -A
git commit -m "update: sinkronisasi skill $(date +%F)"
git push
```

---

## ❓ FAQ

**Q: Apa bedanya dengan `hermes skills install`?**
A: `hermes skills install` butuh link per repo. Repo ini **satu untuk semua** — tinggal restore, semua langsung aktif.

**Q: Apakah .venv ikut?**
A: **Tidak.** Python environment (`.venv`) dibuat ulang via `uv` — restore hanya file skill/prosedur, bukan binary.

**Q: Apakah ada secret/token di repo ini?**
A: **Tidak.** Semua `.env`, `.pem`, `.key` di-exclude. Skill berisi prosedur & instruksi, bukan kredensial.

**Q: Ukuran repo gede nggak?**
A: Skills ~114MB (34MB terkompresi) — nyaman untuk GitHub (limit file 100MB, repo recommend <1GB).

---

## 📋 Lisensi & Atribusi

- Skills adalah konten open-source milik komunitas (masing-masing punya lisensi sendiri, mis. Task Observer CC BY 4.0)
- Repo ini hanya **backup pribadi** pengguna vanderstark — bukan redistribusi komersial
- Attribusi tetap milik masing-masing author skill

Dibuat dengan ❤️ oleh Hermes untuk Bos. 🙏