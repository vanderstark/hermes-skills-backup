# GitHub Search Queries by Category

This reference maps the 13 "123 Claude Skills" categories to GitHub search queries for bulk-installing skill packs.

## Search Template

```
https://api.github.com/search/repositories?q=<QUERY>+skills+language:python+language:javascript&sort=stars&per_page=5
```

## By Category

### 1. 123 SKILLS (Framework)
**Query:** `engineering+framework+copilot`  
**Keywords:** spec, plan, build, audit, e2e, ship, debug  
**Examples:** claude-skills-pack, gstack  

### 2. ADS & PERFORMANCE
**Query:** `ads+performance+marketing`  
**Keywords:** Google Ads, Facebook Ads, analytics, ROI, performance-max  
**Examples:** gtm-agents, performance-max-claude-skills  

### 3. CONTENT CREATION
**Query:** `content+creation+writing`  
**Keywords:** copywriting, scripts, articles, email, social  
**Examples:** awesome-claude-skills/content-research-writer  

### 4. SALES & MARKETING
**Query:** `sales+marketing+gtm`  
**Keywords:** prospecting, pipeline, campaign, cold-email, funnel  
**Examples:** gtm-agents (203 agents), OneWave-AI/claude-skills  

### 5. BUSINESS OPERATIONS
**Query:** `business+operations+automation`  
**Keywords:** workflows, process, document, compliance, scheduling  
**Examples:** existing ECC ops suite  

### 6. FINANCE & PLANNING
**Query:** `finance+advisor+planning`  
**Keywords:** portfolio, accounting, tax, crypto, valuation  
**Examples:** personal-finance-advisor, octagon-finance  

### 7. CUSTOMER EXPERIENCE
**Query:** `customer-experience+cs+automation`  
**Keywords:** churn, NPS, retention, support, satisfaction  
**Examples:** customer-success-skills, support-machine  

### 8. PRODUCT DEVELOPMENT
**Query:** `product+development+lifecycle`  
**Keywords:** validation, roadmap, prioritization, launch  
**Examples:** product-lens, artifact-builder  

### 9. EDUCATION & TRAINING
**Query:** `education+training+curriculum`  
**Keywords:** course, LMS, assessment, onboarding, learning  
**Examples:** ai-agent-camp, edu-role-play  

### 10. DESIGN & CREATIVE
**Query:** `design+creative+ui+brand`  
**Keywords:** UI/UX, branding, animation, design-system  
**Examples:** 40+ design skills (existing)  

### 11. RESEARCH & ANALYSIS
**Query:** `research+analysis+market`  
**Keywords:** competitive, academic, papers, data, intelligence  
**Examples:** arxiv-skill, biomedical-research-analyst  

### 12. PERSONAL PRODUCTIVITY
**Query:** `productivity+note+organization`  
**Keywords:** notes, task, calendar, project, automation  
**Examples:** obsidian-skills, notion-skills  

### 13. GROWTH & SCALING
**Query:** `growth+scaling+orchestrator`  
**Keywords:** ABM, nurture, launch, PLG, expansion  
**Examples:** gtm-agents orchestrators  

---

## Success Indicators

**Good repos to install:**
- Stars > 10 (has proven community interest)
- Updated within last 6 months (actively maintained)
- Contains SKILL.md or .claude-plugin/ manifest
- License: MIT, Apache2, or similar (NOT GPL)
- Clear README with examples

**Skip these:**
- Stars = 0-3 (unproven)
- Last update > 1 year (stale)
- No manifest or docs (unclear structure)
- GPL license (viral; avoid)
- Description is vague or template-only

---

## Real Examples from This Session (Aug 15, 2026)

Installed today (13/13 categories complete):
- `claude-skills-pack` (12 eng skills)
- `gtm-agents` (67 plugins, 203 agents)
- `personal-finance` (10 fintech)
- `customer-success` (CS automation)

Final GitHub backup: `vanderstark/hermes-skills-backup`  
Documentation: `INSTALLED-SKILLS.md`, `SKILLS-DIRECTORY.md`
