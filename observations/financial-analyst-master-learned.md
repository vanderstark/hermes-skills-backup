# Learning Observation: Financial Analyst Master (Octagon MCP)

**Skill:** `finance/octagon/financial-analyst-master`
**Date:** 2026-08-24
**Learner:** Hermes Agent (for Bos - Polri)
**Status:** ACTIVE LEARNING

---

## 🔍 Skill Overview

This skill orchestrates a comprehensive suite of sub-skills from the **Octagon MCP** financial intelligence toolkit. It enables full equity research analysis modeled on institutional sell-side reports (e.g., Goldman Sachs), tailored for automated due diligence using public market data APIs.

The persona is an **Equity Research Analyst** producing decision-ready reports for hedge fund portfolio managers.

---

## 🧠 Conceptual Understanding

### Core Philosophy
This isn't just data retrieval—it's a **structured equity research workflow** designed around the question:
> "Why is this company undervalued or overvalued relative to its peers?"

It forces the analyst to:
1. Gather foundational financial data
2. Identify historical trends and growth trajectories
3. Understand business mix (product/geography)
4. Incorporate ESG positioning
5. Compare against competitors quantitatively
6. Synthesize everything into a valuation story

### Prerequisites for Production
- Octagon MCP must be configured in the AI agent environment
- Access to live financial databases (via Octagon API credentials)
- Understanding of financial metrics (P/E, EV/EBITDA, DCF scoring, etc.)

---

## 🧭 Workflow Deep Dive (Phase-by-Phase)

Each phase corresponds to a set of concrete `skill_view` calls or Octagon tool invocations:

### Phase 1 – Data Collection (`references/workflow-overview.md`)
```markdown
# Phase 1 Commands (Template):
Retrieve real-time income statement data for <TICKER>
Retrieve detailed balance sheet data for <TICKER>
Retrieve cash flow statement data for <TICKER>
Retrieve analyst Revenue and EPS estimates for <TICKER>
Retrieve Altman Z-Score and Piotroski Score for <TICKER>
```

**Key Insight:** This phase establishes the factual foundation. Every subsequent judgment must tie back to these numbers.

### Phase 2 – Growth & Trend Analysis
```bash
# YoY Growth Queries:
Retrieve year-over-year growth in key income-statement items for <TICKER>
Retrieve YoY growth in Total Assets, Liabilities, Equity for <TICKER>
Retrieve YoY growth in Operating Cash Flow and Free Cash Flow for <TICKER>
Retrieve historical financial ratings and key metric scores for <TICKER>
```

**Key Insight:** Trends reveal trajectory. A company growing revenue but declining margins signals competitive pressure.

### Phase 3 – Segmentation & Positioning
```bash
Retrieve revenue breakdown by product segment for <TICKER>
Retrieve revenue breakdown by geographic segment for <TICKER>
```

**Key Insight:** Diversification risk analysis—if 80% comes from one product region, that’s concentration risk.

### Phase 4 – ESG & Sustainability
```bash
Retrieve ESG ratings and scores for <TICKER>
Retrieve ESG benchmark comparison metrics for the Technology sector for FY2024
```

**Key Insight:** ESG is now part of valuation modeling—high ESG = lower cost of capital in many models.

### Phase 5 – Peer Comparison
Repeat Phases 1–4 for 2–3 direct competitors:
```bash
Retrieve year-over-year growth in key income-statement items for AMD
Retrieve year-over-year growth in key income-statement items for INTC
```

### Phase 6 – Report Generation

Final deliverable follows this structure:
- Executive Summary & Snapshot *(target price, upside %, rating)*
- Investment Thesis *(3-bullet "why now")*
- Positives *(ranked with quant support)*
- Peer Comparison *(table format)*
- Estimates & Assumptions *(base/bear/bull scenarios)*
- Valuation *(multiples cross-check)*
- Key Risks *(ranked by probability x impact)*
- ESG Assessment
- Appendix *(detailed models, methodology)*

---

## 💡 Practical Takeaways

| Concept | Application |
|--------|-------------|
| Sourcing Hierarchy | Always prioritize company filings (10-K, earnings calls) before third-party data |
| “DATA NEEDED” Tagging | Explicitly mark missing data so follow-up research is actionable |
| Factor Profile | Growth / Returns / Multiple / Integrated percentile summary gives quick health pulse |
| Cross-Validate | Use multiple skills to confirm findings (e.g., analyst estimates + health scores) |

---

## 🧪 Example Output Template

```markdown
# Initiation of Coverage: [COMPANY NAME] ([TICKER])
**Rating:** Buy / Hold / Sell  
**Target Price:** $XXX (+xx% upside)  
**Sector:** [Sector]  
**Date:** [YYYY-MM-DD]

## Executive Summary
[Brief overview combining price target, key thesis, factor profile]

## Investment Thesis
• [Driver #1 - backed by data]
• [Driver #2 - backed by data]
• [Driver #3 - backed by data]

## Peer Comparison Table
| Company | P/E | EV/EBITDA | Revenue Growth | ROE |
|--------|-----|-----------|----------------|-----|
| [TICKER] | xx.x | xx.x | xx% | xx% |
| [PEER1] | xx.x | xx.x | xx% | xx% |

## Valuation Cross-Check
- DCF-derived value: $XXX
- Peer median multiple: $XXX
- Implied re-rating catalyst: [description]

## Key Risks
1. **[Risk #1]** — Probability: High, Impact: Medium → Sensitivity: -$0.50/share
2. **[Risk #2]** — Probability: Low, Impact: High → Sensitivity: -$1.20/share

## ESG Snapshot
- MSCI Rating: AA
- Carbon Intensity: xx tonnes/$M revenue
- vs. Sector Average: Above / Below
```

---

## 🛠️ Integration Ideas (for Bos's Infrastructure)

Can integrate this workflow into:
- Daily/Weekly automated equity scan across portfolio holdings
- Pre-trade due diligence pipeline for new investments
- Integration with internal BI dashboards showing real-time factor profiles
- Alerting system when key financial ratios breach thresholds

---

## 📌 Next Steps After Learning

✅ Understand the six-phase workflow  
✅ Memorize key financial metrics referenced by each sub-skill  
✅ Build reusable Python wrapper to automate report generation from CLI  
✅ Test on sample ticker (e.g., NVDA or TSLA)  

---

*Observation logged by Task Observer protocol.*
