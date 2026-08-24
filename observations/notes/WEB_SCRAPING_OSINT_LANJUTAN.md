# 🕸️ Web Scraping OSINT: Materi Lanjutan untuk Bos

**Skill dasar:** `scrapegraph-ai-scraping` (ScrapegraphAI — LLM-Powered Web Scraping, MIT license)
**Kategori:** Data Mining / OSINT / Automation
**Target:** Lab OSINT polsek/academy — monitoring & pengumpulan data intelijen

---

## 🎯 Ringkasan Skill

ScrapegraphAI adalah library Python yang pakai LLM untuk memahami struktur halaman web dan ekstrak data sesuai prompt bahasa natural — **tanpa CSS selector atau XPath manual**. Cocok untuk situs yang strukturnya berantakan/berubah-ubah, atau saat mau dibangun pipeline scraping yang tahan terhadap redesign website.

**Kapan pakai skill ini:**
- Mau ekstrak data dari halaman web dan cukup deskripsikan APA yang mau diambil (bukan cara/selector)
- Struktur HTML target tidak konsisten antar halaman
- Bangun pipeline data-collection berulang (monitoring harga, agregasi berita, tracking kompetitor/aktivitas) di banyak situs berbeda tanpa maintenance selector satu-satu

**Kapan JANGAN pakai (lebih baik pakai `requests`/`curl` langsung):**
- Struktur halaman sederhana & stabil (misal endpoint JSON)
- Scraping skala besar (100+ halaman) — LLM call per halaman jadi mahal & lambat

---

## 🔧 Instalasi

```bash
pip install scrapegraphai
playwright install   # wajib untuk situs JS-heavy / headless mode
```

---

## ⚙️ Konfigurasi Inti (pakai model Hermes sendiri, tanpa API key terpisah)

```python
import os
from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "api_key": os.environ["HERMES_CUSTOM_..._API_KEY"],  # cek /opt/data/.env untuk nama var yang tepat
        "model": "openai/cc/claude-sonnet-5",   # prefix "openai/" wajib meski bukan OpenAI asli
        "base_url": "http://<host>:<port>/v1",
    },
    "verbose": True,
    "headless": True,   # set False untuk debug visual
}

smart_scraper_graph = SmartScraperGraph(
    prompt="Extract nama pelaku, lokasi, dan tanggal kejadian",
    source="https://contoh-sumber-berita.com/artikel",
    config=graph_config,
)

result = smart_scraper_graph.run()
print(result)   # {"content": {"nama": ..., "lokasi": ..., "tanggal": ...}}
```

---

## 📊 Jenis Graph yang Tersedia

| Graph Class | Kegunaan |
|---|---|
| `SmartScraperGraph` | Satu halaman, satu prompt → ekstraksi terstruktur |
| `SmartScraperMultiGraph` | Prompt sama untuk banyak URL sekaligus (efisien untuk monitoring multi-sumber) |
| `SearchGraph` | Search web dulu (via search API), lalu scrape+ekstrak dari hasil teratas |
| `ScriptCreatorGraph` | Generate script Python scraping yang bisa dipakai ulang (hemat biaya untuk cron job berulang) |

### Contoh Multi-Sumber (untuk monitoring OSINT banyak situs)

```python
from scrapegraphai.graphs import SmartScraperMultiGraph

multi_graph = SmartScraperMultiGraph(
    prompt="Extract judul berita, tanggal, dan ringkasan terkait keamanan siber",
    source=[
        "https://sumber1.com/berita-terbaru",
        "https://sumber2.com/kategori/kriminal",
    ],
    config=graph_config,
)
result = multi_graph.run()
```

---

## 🎯 Use Case untuk Lab OSINT Polri

1. **Monitoring media/forum** — pantau pemberitaan terkait kasus/isu tertentu secara otomatis (Intelkam).
2. **Tracking aktivitas online** — kumpulkan data publik terkait pola/tren kejahatan siber (Reskrim).
3. **Agregasi data sosial** — kumpulkan sentimen publik terkait program Binmas/Sabhara.
4. **Pipeline berulang (cron)** — pakai `ScriptCreatorGraph` untuk generate script tanpa LLM call berulang, cocok dijadwalkan harian via `cronjob`.

---

## ⚠️ Pitfalls Penting

- **Situs JS-heavy:** `headless: True` pakai Playwright — wajib `playwright install` dulu, kalau lupa fetch gagal diam-diam/timeout.
- **Rate limit & etika:** tetap scraping biasa — hormati `robots.txt`, ToS situs, rate limiting, JANGAN kumpulkan PII tanpa dasar hukum yang sah (penting untuk konteks Polri!).
- **Prefix model:** wajib pakai prefix `openai/` di nama model custom, walau backend bukan OpenAI asli.
- **Biaya untuk skala besar:** tiap scrape = minimal 1 LLM call per halaman. Untuk 100+ halaman, pertimbangkan `ScriptCreatorGraph` biar generate script non-LLM yang reusable.
- **IP internal di base_url:** wajar kalau security scanner flag base_url IP internal (192.168.x.x) — ini endpoint Hermes internal, bukan exposure asli.

---

## 🔗 Related Skills

- `exploratory-data-analysis` — profiling & cleaning data hasil scraping
- `scikit-learn` — clustering/pattern-mining dari dataset hasil scraping (misal: pola modus kejahatan)
- `polars` — ETL cepat kalau hasil scraping datanya besar (tabular)

---

**Status:** Siap dipakai untuk lab OSINT
**Next Step:** Setup `pip install scrapegraphai` + `playwright install`, lalu uji coba SmartScraperGraph di 1 sumber dulu sebelum scale-up ke multi-sumber
