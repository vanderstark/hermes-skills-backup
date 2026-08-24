# 📊 Finance & Market Lanjutan: Octagon Financial Analyst

**Ditulis:** 24 Agustus 2026  
**Kategori:** Finance & Market Analysis (Lanjutan)  
**Target User:** Bos (Polri, 170-server DC, market trader)  
**Bahasa:** Indonesian (Bahasa Indonesia)

---

## 🎯 Ringkasan

Skill **Financial Analyst Master** adalah orkestrasi menyeluruh dari semua tools **Octagon MCP** untuk analisis ekuitas kelas institusional. Mencakup:
- Pengambilan data finansial (income statement, balance sheet, cash flow)
- Analisis pertumbuhan YoY (revenue, profit, FCF)
- Segmentasi produk & geografis
- Rating kesehatan keuangan (Altman Z-Score, Piotroski)
- Benchmarking ESG + peer comparison

**Target output:** Laporan equity research 6,000-10,000 kata (initiation of coverage), model valuasi, dan investasi thesis.

---

## 📚 Skill Roadmap: 3 Lapis Pembelajaran

### Tier 1: Dasar (Sudah Dikuasai)
- ✅ `financial-analyst` — Financial ratio analysis, DCF, budget forecasting
- ✅ `saas-metrics-coach` — SaaS health (ARR, churn, CAC, LTV)
- ✅ `stock-analysis` — Analisis stock dengan public data (free)

### Tier 2: Intermediate (Focus Sesi Ini)
- 🔷 `financial-analyst-master` — Full equity research orchestrator (Octagon MCP)
- 🔷 `financial-growth` — YoY revenue, profit, FCF growth metrics
- 🔷 `balance-sheet-growth` — Asset, liability, equity trends
- 🔷 `cash-flow-growth` — OCF, FCF, net cash flow growth
- 🔷 `analyst-estimates` — Consensus revenue & EPS projections
- 🔷 `financial-health-scores` — Altman Z-Score, Piotroski Score

### Tier 3: Advanced (Lanjutan)
- 🟦 `sec-analyst-master` — SEC filing deep-dive (10-K, 10-Q, 8-K)
- 🟦 `earnings-analyst-master` — Earnings call transcript analysis
- 🟦 `market-analyst-master` — Market index, sector, peer comparison

---

## 🔧 Core Workflow: Financial Analyst Master

### Phase 1: Pengumpulan Data
```
1. Ambil income statement (revenue, COGS, operating income, net income, EPS)
2. Ambil balance sheet (assets, liabilities, equity, net debt)
3. Ambil cash flow statement (OCF, capex, FCF)
4. Ambil analyst estimates (consensus revenue & EPS 1-3 tahun ke depan)
```

**Tools:** `stock-quote`, `income-statement`, `balance-sheet`, `cash-flow-statement`

### Phase 2: Analisis Pertumbuhan
```
1. YoY growth: Revenue, Gross Profit, Operating Income, Net Income, EPS
2. Growth balance sheet: Total Assets, Liabilities, Shareholders' Equity
3. Growth cash flow: OCF, FCF, net cash flow
4. Historical ratings: Altman Z-Score, Piotroski Score (untuk 5 tahun terakhir)
```

**Tools:** `financial-growth`, `balance-sheet-growth`, `cash-flow-growth`, `financial-health-scores`

### Phase 3: Segmentasi Bisnis
```
1. Revenue by product segment (berapa % dari masing-masing produk?)
2. Revenue by geography (exposure US, EU, APAC, emerging markets?)
```

**Tools:** `revenue-product-segmentation`, `revenue-geographic-segmentation`

### Phase 4: ESG & Sustainability
```
1. ESG ratings (MSCI, Sustainalytics scores)
2. ESG sector benchmark (dibanding kompetitor di industri yang sama)
```

**Tools:** `esg-ratings`, `esg-benchmark-comparison`

### Phase 5: Peer Comparison
```
Ulangi Phase 1-4 untuk 2-3 kompetitor utama
Buat comparison table untuk:
- Growth rates (revenue, profit, FCF)
- Margins (gross, operating, net)
- Multiples (P/E, EV/EBITDA)
- Financial health scores
```

### Phase 6: Laporan & Valuasi
```
1. Buat investment thesis (3 bullet points)
2. Valuation: multiples vs. peer median
3. Risk analysis (top 5 risks ranked by impact)
4. Target price & upside calculation
```

---

## 📋 Template: Financial Analyst Report (6,000-10,000 kata)

```
INITIATION OF COVERAGE REPORT

1. EXECUTIVE SUMMARY & SNAPSHOT (500 words)
   - Current price | Target price | Implied upside (%)
   - Rating (Outperform/In Line/Underperform)
   - Factor profile percentile (Growth, Returns, Multiple, Quality)
   - 12-month price chart [placeholder]

2. INVESTMENT THESIS (500 words)
   - 3-bullet "Why now" positioning
   - One-liner: "[COMPANY] is positioned to [specific outcome] because [reason]"

3. INVESTMENT POSITIVES (1,000-1,500 words)
   - Ranked drivers of upside, each dengan quantitative support
   - E.g., "Revenue CAGR 15% → 20% (vs. 10% peer avg) → expand EV/Sales 3.0x to 3.5x"

4. COMPETITIVE & PEER ANALYSIS (800-1,000 words)
   - Table: company vs. 2-3 peers on revenue growth, margins, multiples, ratings
   - Relative strengths/weaknesses

5. ESTIMATES & OPERATING MODEL (1,000 words)
   - 3-year forward model: Revenue, EBITDA margin, FCF
   - Base case, bear case, bull case sensitivities

6. VALUATION (800-1,000 words)
   - Primary: multiples (EV/EBITDA, P/E) vs. peer median
   - Cross-check: peer multiples imply target price $X
   - Re-rating catalysts over 12-month view

7. KEY RISKS (800 words)
   - Top 5 risks ranked by probability × impact
   - Financial sensitivity: "If [risk], then [financial impact]"
   - E.g., "If churn rises 2%, FCF falls 15%"

8. ESG ASSESSMENT (500-700 words)
   - MSCI rating | Sustainalytics risk rating | Peer comparison
   - Material ESG factors (e.g., Board diversity, carbon footprint for energy stock)

9. APPENDIX
   - Extended financials (10-year historical)
   - Detailed model assumptions
   - Methodology & data sources
```

---

## 🎬 Use Cases (Real-World Polri Context)

### Skenario 1: Due Diligence untuk Investment Unit
Bos ingin audit finansial **perusahaan telekomunikasi Indonesia** sebelum Polri berinvestasi di subsidiary mereka:
1. Ambil 5-tahun financial data (PT TELKOM)
2. Analisis revenue growth: apakah sustainable? (mengapa turun/naik?)
3. Cash flow check: apakah ada red flag (burn rate, debt default risk)?
4. Peer comparison: bagaimana performa vs. Indosat, XL Axiata?
5. Output: 10-halaman report dgn recommendation "Go/No-Go invest?"

### Skenario 2: Market Timing untuk Trading
Bos ingin tau apakah saham IDX index sudah "mahal" atau "murah":
1. Ambil valuation multiples (P/E, EV/EBITDA) untuk top 20 saham IDX
2. Bandingkan ke historical median + peer average
3. Identifikasi "oversold" (harga rendah vs. growth) vs. "overbought"
4. Output: Buy/Sell signal untuk portfolio positioning

### Skenario 3: Financial Health Check (170-Server Cost Analysis)
Bos ingin tau apakah **vendor infrastruktur** (misal Nutanix, Pure Storage) financially healthy untuk jangka panjang:
1. Check Altman Z-Score (bankruptcy risk?)
2. Check cash flow trend: masih invest di R&D atau sudah decline?
3. Check guidance vs. actual (management credible?)
4. Output: Risk assessment "Safe jangka panjang?" vs. "Ada warning sign?"

---

## 💡 Key Insights & Pitfalls

### ✅ Best Practices

| Aspek | Best Practice |
|-------|---------------|
| **Data Collection** | Always retrieve 5-year historical (minimal). Lebih banyak = lebih akurat trend. |
| **Growth Analysis** | Bandingkan YoY growth ke 3-year CAGR vs. peer average. Identifikasi inflection points. |
| **Valuation** | Never trust single method. Always use 2-3 methods (multiples, DCF, peer comps). |
| **Risk Ranking** | Rank by `probability × impact`, bukan "gut feel". Quantify financial sensitivity. |
| **Peer Selection** | Pilih comparable peers (sama industri, ukuran, geography exposure). Jangan bandingkan bank ke tech. |

### ⚠️ Pitfalls (Hindari!)

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Terpaku satu metrik (e.g., revenue growth) | Miss profitability trap atau margin compression. | Always analyze profit margin trend + cash conversion. |
| Ignore ESG red flags | Regulatory risk (e.g., carbon tax) bisa crater valuasi. | Integrate ESG sebagai integral risk assessment. |
| Forecasting tanpa sensitivity | Model useless saat asumsi berubah. | Build bear/base/bull case untuk setiap key assumption. |
| Tidak cross-validate | Cherry-pick data untuk suit thesis. | Use multiple skills (financial-growth, balance-sheet, cash-flow) untuk confirm. |
| Miss cash flow red flags | Company bs earnings tapi negative FCF = distress signal. | Always check: "Apakah earnings converted to cash?" |

---

## 🎓 Learning Path (4 Minggu)

### Minggu 1: Data Collection & Financial Statements
- [ ] Load skill: `financial-analyst-master`
- [ ] Practice Phase 1: retrieve income statement + balance sheet untuk 3 stocks
- [ ] Understand setiap metric (Revenue, COGS, Operating Income, EPS, Net Debt)
- [ ] **Deliverable:** Snapshot table untuk AAPL, MSFT, GOOG

### Minggu 2: Growth Analysis
- [ ] Load skills: `financial-growth`, `balance-sheet-growth`, `cash-flow-growth`
- [ ] Analyze YoY trends: identify inflection points, margin changes
- [ ] Practice: "Apakah revenue growth sustainable?"
- [ ] **Deliverable:** Growth analysis untuk 5-tahun terakhir (IDX top 5 stocks)

### Minggu 3: Segmentation & Peer Comparison
- [ ] Load skills: `revenue-product-segmentation`, `esg-ratings`
- [ ] Understand business mix (mana segment paling profitable?)
- [ ] Peer benchmarking (tabel perbandingan 5 metrics vs. 3 peers)
- [ ] **Deliverable:** Competitive positioning memo (1-2 halaman)

### Minggu 4: Report & Valuation
- [ ] Buat laporan equity research lengkap (6,000+ kata)
- [ ] Include: thesis, positives, risks, valuation, recommendation
- [ ] Target price calculation: multiples method + DCF method
- [ ] **Deliverable:** Full equity research report (initiation of coverage)

---

## 📖 References & Learning Resources

### Official Docs
- Octagon MCP: https://docs.octagon.ai/
- SEC EDGAR (10-K, 10-Q filings): https://www.sec.gov/cgi-bin/browse-edgar

### Bookmarks (Recommended)
- Goldman Sachs equity research (sample format)
- Morningstar financial metrics glossary
- MSCI ESG rating methodology

### Related Skills
- `sec-analyst-master` — untuk deep-dive SEC filings
- `earnings-analyst-master` — untuk earnings call nuances
- `financial-health-scores` — untuk bankruptcy risk assessment
- `railpath-finance-toolkit` — untuk portfolio risk analytics

---

## 🔗 Integration dengan Hermes Infrastructure

### Octagon MCP Setup (Prasyarat)
Octagon MCP harus sudah configured di Hermes agent (Cursor/Claude Desktop/Windsurf). Verify:
```bash
# Check Octagon config
cat ~/.cursor/mcp_config.json | grep -A 5 octagon
# Should show: "octagon-mcp" enabled dengan API key
```

### Workflow dalam Hermes
1. Load skill `financial-analyst-master`
2. Query MCP tools via skill shortcuts
3. Data otomatis tersimpan di memory untuk cross-session reference
4. Export reports → GitHub repo `vanderstark/market-analysis-reports`

---

## ✨ Success Criteria

Bos dinyatakan **mastered** skill ini ketika bisa:
- [ ] Buat equity research report lengkap (thesis → valuation → risks) dalam 2 jam
- [ ] Identify financial red flags (cash burn, margin compression, debt risk) in 10 menit
- [ ] Rank peers objectively (comparison table) untuk 5 stocks
- [ ] Calculate target price using 2+ methods (multiples + DCF)
- [ ] Defend recommendation dengan quantitative evidence (bukan "gut feel")

---

**Status:** Ready to Learn (Tier 2 - Intermediate)  
**Estimated Time to Mastery:** 4 minggu @ 5 jam/minggu  
**Next Milestone:** Tier 3 (SEC Filing Deep-Dive + Earnings Analysis)
