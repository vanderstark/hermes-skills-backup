---
name: skill-discovery-workflow
description: Use when finding or evaluating new skills for the user.
version: 1.0.0
author: Hermes Agent / Curator
license: MIT
platforms: [linux, macos, windows]
tags: [workflow, discovery, organization, meta-skill]
hermes:
  tags: [workflow, discovery, organization, meta-skill]
  related_skills: [task-observer, autonomous-ai-agents]
---

# Skill Discovery Workflow

Gunakan skill ini untuk metodologi eksplorasi skill baru di folder `skills/`, `plugins/`, atau marketplace external. Skill ini menggantikan pola pencarian yang tidak terstruktur.

## 🧭 Kapan Digunakan

Gunakan skill ini ketika:
- Membutuhkan skill baru untuk topik spesifik
- Ingin mengevaluasi skill yang sudah ada
- Sedang mengorganisasi koleksi skill berdasarkan domain
- Membutuhkan workflow consistency untuk pengembangan skill baru

## 🔍 Proses Discovery (4 Fase)

### Fase 1: Definisikan Domain Target
Tentukan kategori utama yang dicari:
- `research` / `science` — untuk riset akademik
- `mlops` — untuk machine learning operations
- `productivity` — untuk otomasi dokumen
- `security` — untuk cybersecurity
- `finance` — untuk analisis keuangan
- `software-development` — untuk coding/devops
- `creative` — untuk konten kreatif

### Fase 2: Gunakan skills_list untuk Scanning
```bash
# Cari semua skill di kategori tertentu
skills_list(category="research")
skills_list(category="mlops")
skills_list(category="productivity")

# Output berisi: name, description, tags, related_skills
```

### Fase 3: Gunakan skill_view untuk Evaluasi Mendalam
Untuk setiap skill yang dipertimbangkan:
```bash
# Baca SKILL.md lengkap
skill_view(name="research/arxiv")

# Baca file pendukung (references, scripts, templates)
skill_view(name="research/arxiv", file_path="references/usage.md")
```

**Metadata yang Perlu Dilihat:**
- `description` — apakah tepat dengan kebutuhan?
- `tags` — cocok untuk domain kita?
- `related_skills` — ada skill pendukung?
- `setup_needed` / `missing_required_commands` — perlu persiapan?

### Fase 4: Buat Catatan Evaluasi
Di `/opt/data/deliverables/hermes-skills-backup/observations/notes/[DOMAIN]_SKILL_BROWSING.md`

Format:
```markdown
# [DOMAIN] Skill Browsing - [Tanggal]

## Skills yang Ditemukan
- **skill-name** — deskripsi singkat + relevance score

## Skills yang Perlu Dipelajari
- **primary** — skill utama
- **secondary** — skill pendukung

## Insights & Pitfalls
### Best Practices
- ...

### Challenges
- ...
```

## 📋 Template Checklist Evaluasi

| Kriteria | Ya | Tidak | Keterangan |
|----------|-----|--------|------------|
| Cocok dengan use case Bos? |  |  |  |
| Memiliki dokumentasi lengkap? |  |  |  |
| Ada file pendukung (references/scripts)? |  |  |  |
| Butuh setup tambahan? |  |  |  |
| Ambuhan riwayat (historical) tersedia? |  |  |  |

## 🔄 Update Skill: Research & AI LabOps

### Skills yang Ditemukan di Kategori Research
| Skill | Deskripsi | Relevansi |
|-------|-----------|-----------|
| `research/arxiv` | Search arXiv papers via REST API | ⭐⭐⭐⭐⭐ Utama |
| `research/research-paper-writing` | Draft ML papers | ⭐⭐⭐⭐⭐ Utama |
| `research/blogwatcher` | Monitor tech blogs/RSS | ⭐⭐⭐⭐ Terkait OSINT |
| `research/ai-tool-system-prompts` | Leaked prompts from 30+ AI tools | ⭐⭐⭐ OSINT tooling |
| `research/polymarket` | Query Polymarket markets/prices | ⭐⭐ Meta-research |
| `research/papers` | Research paper discovery | ⭐⭐ Alternatif arXiv |

### Skills yang Ditemukan di Kategori MLOps
| Skill | Deskripsi | Relevansi |
|-------|-----------|-----------|
| `mlops/huggingface-hub` | HF CLI: search/download/upload | ⭐⭐⭐⭐⭐ Utama |
| `mlops/llama-cpp` | Local GGUF inference | ⭐⭐⭐⭐⭐ Utama |
| `mlops/serving-llms-vllm` | vLLM high-throughput serving | ⭐⭐⭐⭐ Lanjutan |
| `mlops/weights-and-biases` | ML experiment tracking | ⭐⭐⭐⭐ Utama |
| `mlops/evaluating-llms-harness` | LLM benchmark suite | ⭐⭐⭐ Lanjutan |

### Skills yang Ditemukan di Kategori Productivity
| Skill | Deskripsi | Relevansi |
|-------|-----------|-----------|
| `productivity/ocr-and-documents` | Extract text from PDFs/scans | ⭐⭐⭐⭐ Dokumen |
| `productivity/powerpoint` | Create/edit PPTXs | ⭐⭐⭐⭐ Presentasi |
| `productivity/docx` | Create/edit Word docs | ⭐⭐⭐⭐ Dokumen |
| `productivity/markitdown-converter` | Convert docs to markdown | ⭐⭐⭐ OSINT content |
| `productivity/notebooklm` | Browser automation/notebooks | ⭐⭐ R&D note-taking |
| `productivity/youtube-full` | YouTube transcript analysis | ⭐ Content research |

## ⚠️ Pitfalls yang Dihindari

1. **Jangan langsung pilih skill terbaru** — selalu evaluasi setup_needed dan dependencies
2. **Check version stability** — skill yang baru dirilis bisa belum stabil
3. **Verifikasi license compatibility** — pastikan cocok dengan kebutuhan Bos (MIT, Apache, dll)
4. **Jangan lupa backup token** — selalu hapus token GitHub setelah push

## 💡 Best Practices

1. **Version tracking:** Catat nomor versi skill yang dipilih untuk reproduksibilitas
2. **Cross-skill reference:** Cari skill yang memiliki `related_skills` untuk workflow lengkap
3. **Documentation check:** Pastikan ada `SKILL.md` + `references/` + `scripts/` (jika diperlukan)
4. **Task-aligned selection:** Pilih skill yang trigger condition-nya cocok dengan kebutuhan Bos

## 📦 Contoh Penggunaan

Untuk menggunakan skill yang sudah dipilih:
```bash
# Load skill yang dipilih
load skill: research/arxiv

# atau via CLI
hermes skill load research/arxiv

# Eksekusi workflow
python scripts/search_arxiv.py "transformer reinforcement learning"
```