# 🔬 Research & AI LabOps: OSINT & R&D Excellence

**Ditulis:** 24 Agustus 2026  
**Kategori:** Research & AI LabOps  
**Target User:** Bos (Academy AI/OSINT Lab, 170-server DC)  
**Bahasa:** Indonesian (Bahasa Indonesia)

---

## 🎯 Ringkasan

Skill **Research & AI LabOps** dirancang untuk mentransformasi Lab OSINT Bos menjadi pusat riset dan publikasi teknis yang mandiri. Fokus utama:
- Pengambilan literatur ilmiah otomatis (arXiv)
- Sintesis bukti dari berbagai sumber (Semantic Scholar)
- Penulisan naskah teknis/paper standar internasional
- Alur kerja publikasi lab (Tech Blog/White Paper)

**Hasil Akhir:** Lab Bos mampu memproduksi konten edukasi dan riset berkualitas tinggi yang mendukung operasional Polri dan pengembangan drone.

---

## 📚 Skill Roadmap: 3 Lapis Pembelajaran

### Tier 1: Dasar (Focus Sesi Ini)
- ✅ `research/arxiv` — Search & retrieve academic papers via REST API
- ✅ `research/research-paper-writing` — Draft ML papers (design → submit)
- ✅ `research/blogwatcher` — Monitor tech blogs & RSS feeds

### Tier 2: Intermediate (Lanjutan)
- 🔷 `research/deep-research` — Multi-source investigation (Firecrawl/Exa)
- 🔷 `research/litreview` — Academic literature orientation & synthesis
- 🔷 `research/syllabus` — Curated learning lists for academy training

### Tier 3: Advanced (Scientific Mastery)
- 🟦 `scientific-writing` — Draft/audit scientific manuscripts
- 🟦 `scientific-critical-thinking` — Evaluate claims & evidence quality
- 🟦 `scientific-visualization` — Publication-ready data visualization

---

## 🔧 Core Workflow: Research Excellence

### Fase 1: Penemuan & Monitoring (Discovery)
```bash
# 1. Monitor tren terbaru via tech blogs
blogwatcher-cli list

# 2. Cari paper spesifik di arXiv (contoh: "LLM for OSINT")
python3 scripts/search_arxiv.py "LLM OSINT cybersecurity" --max 10 --sort date
```
**Tools:** `arxiv`, `blogwatcher`

### Fase 2: Analisis Dampak & Referensi
```bash
# Cek seberapa berpengaruh paper tersebut (citation count) via Semantic Scholar
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount,influentialCitationCount"
```
**Tools:** `arxiv` (Semantic Scholar integration)

### Fase 3: Sintesis & Ekstraksi Data
```bash
# Ekstrak konten full paper (PDF → Markdown)
web_extract(urls=["https://arxiv.org/pdf/ID"])
```
**Tools:** `ocr-and-documents`, `markitdown-converter`

### Fase 4: Drafting & Penulisan (Writing)
```bash
# Mulai drafting paper menggunakan struktur standar (Abstract, Method, Results)
load skill: research-paper-writing
# Gunakan bibtex otomatis dari arXiv metadata
```
**Tools:** `research-paper-writing`, `docx`, `powerpoint`

---

## 📋 Template: Lab White Paper / Tech Blog

```
[JUDUL LAPORAN TEKNIS LAB OSINT]

1. ABSTRAK (250 kata)
   - Masalah operasional yang dihadapi
   - Solusi teknologi yang diusulkan
   - Temuan utama

2. KONTEKS & LATAR BELAKANG
   - Tren teknologi global (referensi arXiv/blog)
   - Relevansi dengan tugas pokok Polri

3. METODOLOGI RISET
   - Sumber data (OSINT tools, datasets)
   - Model AI yang digunakan (referensi HuggingFace)

4. HASIL ANALISIS & EKSPERIMEN
   - Data visual (charts/tables)
   - Performa model/sistem

5. REKOMENDASI STRATEGIS
   - Langkah implementasi di lapangan
   - Mitigasi risiko

6. REFERENSI (BibTeX style)
```

---

## 🎬 Use Cases (Real-World Lab Context)

### Skenario 1: Monitoring Teknologi Drone Terbaru
Bos ingin tim lab selalu update dengan teknologi navigasi drone:
1. Setup `blogwatcher` untuk monitor feed dari DJI, Skydio, dan lab robotics universitas.
2. Tiap Senin, cari paper terbaru di arXiv category `cs.RO` (Robotics).
3. Buat digest mingguan: "Top 3 Teknologi Navigasi Drone Minggu Ini".

### Skenario 2: Pengembangan Modul Training Academy
Membuat kurikulum OSINT berbasis AI untuk penyidik baru:
1. Gunakan `research/syllabus` untuk memetakan topik dari dasar ke expert.
2. Cari paper "State of the art OSINT techniques 2026" di arXiv.
3. Generate slide presentasi otomatis menggunakan `productivity/powerpoint`.

### Skenario 3: Penulisan White Paper Publikasi Polri
Menghasilkan publikasi internal tentang "Pemanfaatan LLM untuk Analisis Intelkam":
1. Riset literatur menggunakan `research/arxiv` + `Semantic Scholar`.
2. Analisis data internal di lab 170-server.
3. Draft paper menggunakan `research-paper-writing`.

---

## 💡 Key Insights & Pitfalls

### ✅ Best Practices
- **Version Tracking:** Selalu simpan arXiv ID versi spesifik (v1, v2) untuk mencegah "citation drift".
- **BibTeX Workflow:** Gunakan script otomasi untuk generate BibTeX, jangan tulis manual.
- **Cross-Validation:** Bandingkan temuan di paper dengan "real-world blog posts" via `blogwatcher`.

### ⚠️ Pitfalls (Hindari!)
- **Relying on Abstract Only:** Kadang kesimpulan di abstrak terlalu optimis; selalu baca bagian "Results" dan "Limitations".
- **Outdated Data:** Paper AI berumur >2 tahun seringkali sudah *obsolete*; prioritaskan publikasi 6-12 bulan terakhir.
- **Ignore Withdrawn Papers:** Selalu cek status paper di arXiv sebelum menjadikannya referensi utama.

---

**Status:** Ready to Learn (Tier 1 - Dasar)  
**Estimated Time to Mastery:** 4 minggu @ 5 jam/minggu  
**Next Milestone:** Tier 2 (Deep Research & Literature Synthesis)
