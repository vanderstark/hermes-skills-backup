---
name: candidate-background-check
description: "Legit background check for candidates/partners, public data."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [background-check, hr, due-diligence, osint, hiring, compliance]
    related_skills: [legal-research-education, deep-research, scrapegraph-ai-scraping]
---

# Candidate / Business Partner Background Check (Public Data Only)

Structured workflow for legitimate background checks on job candidates or
prospective business partners, using only publicly available information.
This is NOT a surveillance/OSINT-hacking skill — it's a hiring/due-diligence
research aid bounded by legality and ethics.

## Hard boundary — read first, every time

- **Public sources only.** LinkedIn public profile, public social media,
  company registries (AHU Online / OSS for Indonesian entities), published
  news, academic/professional publications, publicly listed court records
  where legally accessible. Never: hacking accounts, buying leaked/breached
  data, scraping private/locked profiles, deploying spyware/stalkerware,
  or accessing any system requiring credentials that aren't the subject's
  own voluntary disclosure to you.
- **No real-time location tracking** of a person — this is about
  professional/reputational history, not surveillance.
- **UU PDP (Indonesia's Personal Data Protection Law) applies** once data
  is collected — the requester must have a lawful basis to process it
  (e.g. legitimate hiring interest), must not over-collect beyond what's
  job-relevant, and must handle/store it responsibly (not share it beyond
  the hiring decision, delete when no longer needed).
- **Best practice: disclose to the subject** that a background check is
  being conducted, even where not strictly legally mandated for the
  specific data type — flag this to the user as a recommendation, don't
  silently skip it.
- **Don't discriminate on protected characteristics.** Findings about
  religion, ethnicity, political affiliation, health, sexual orientation,
  or similar surfaced incidentally during research should NOT be reported
  or factored into a hiring recommendation — flag if such info is
  encountered so the user can consciously exclude it from decision-making,
  per Indonesian labor law (UU Ketenagakerjaan) non-discrimination
  principles.
- **Never present unverified inference as fact.** A same-name match on
  social media isn't confirmed identity — note confidence level, don't
  assert certainty from partial matches.

## When to use this skill

- User wants to verify a job candidate's stated background (education,
  work history, professional reputation) before making a hiring decision
- User wants basic due diligence on a prospective business partner/vendor
  (company legitimacy, public reputation, red flags in news coverage)
- Do NOT use for: monitoring a current employee's personal life, checking
  up on an ex/personal relationship, or any use case where the "candidate"
  framing is a pretext for personal surveillance — ask directly if the
  framing seems off and decline the personal-surveillance version.

## Workflow

### 1. Scope the check

Confirm with the user:
- Full name + any distinguishing detail (employer, city, LinkedIn URL if
  known) to disambiguate common names
- What's actually job-relevant: education verification? employment
  history? professional reputation/red flags? company legitimacy (for
  business partners)?
- Whether the subject has been/will be informed (recommend disclosure)

### 2. Identity verification (education & employment claims)

- Cross-check claimed employer/role against LinkedIn public profile,
  company website team pages, press releases mentioning the person
- For Indonesian entities: verify company legitimacy via AHU Online
  (ahu.go.id) for legal entity status, or OSS (oss.go.id) for business
  licensing — flag if a claimed employer doesn't appear to be a
  registered legal entity
- Note discrepancies plainly (e.g. "candidate states Senior Manager at
  X 2020-2023; LinkedIn shows Manager at X 2021-2023 — gap/title
  mismatch worth asking about directly") rather than concluding dishonesty
  outright — there can be legitimate explanations (promotion timing,
  LinkedIn not updated, etc.)

### 3. Professional reputation research

- Search for the person's name + relevant context (industry, employer)
  via web search / `mcp_exa_web_search_exa` (has a `category:people`
  filter) / `mcp_firecrawl_search`
- Look for: published work, conference talks, professional
  awards/recognition, news coverage (positive or negative), public
  disciplinary records if in a regulated profession (e.g. licensed
  professions with public registries)
- Distinguish confirmed-same-person hits from ambiguous same-name hits —
  common Indonesian names will produce false positives; require at least
  one corroborating detail (employer, photo match via LinkedIn, city)
  before attributing a finding to the specific candidate

### 4. Business partner / vendor due diligence (if applicable)

- Legal entity status and registration (AHU Online / OSS)
- News coverage — search for the company name + terms like "sengketa",
  "gugatan", "pailit", "penipuan" to surface any public legal/reputational
  issues
- Basic financial health signals if publicly available (annual report,
  news on funding/layoffs/expansion)
- Website/domain age and legitimacy signals (very new domain + big
  claims is a mild red flag worth noting, not a conclusion)

### 5. Compile findings — structured, hedged, sourced

Report format:

```
## Background Check Summary: [Name/Company]

**Scope:** [what was checked] | **Sources checked:** [list]
**Confidence:** High/Medium/Low (based on corroboration quality)

### Verified
- [Claim] — confirmed via [source], [date accessed]

### Discrepancies / Worth Asking About
- [Claimed X, found Y — not necessarily dishonest, ask directly]

### Not Found / Inconclusive
- [What couldn't be verified from public sources, and why]

### Flagged for User Awareness (not for decision-making)
- [Any protected-characteristic info encountered incidentally —
  explicitly note this should NOT factor into the hiring decision]

### Recommendation
- [Suggest follow-up questions for interview, or reference checks with
  named professional references — NOT a final hire/no-hire verdict,
  that stays with the user]
```

Always end with: "Ini rangkuman dari data publik yang bisa diverifikasi;
keputusan akhir tetap di tangan Bos berdasarkan proses rekrutmen/due
diligence lengkap (termasuk referensi langsung & wawancara)."

## Pitfalls

- Common name collisions — Indonesian names especially (many "Ahmad
  Fauzi"s, "Siti Nurhaliza"s, etc.) — don't attribute findings without
  corroboration.
- Don't over-collect — if the user only needs employment verification,
  don't go digging into personal social media / family / political
  views just because it's technically public.
- LinkedIn scraping at scale can violate ToS — for a single-candidate
  check, manual browser lookup is fine; don't build an automated bulk
  LinkedIn scraper on top of this skill.
- Company registry lookups (AHU/OSS) are official government sources —
  prefer them over third-party aggregator sites for legal entity status,
  which can be stale or inaccurate.

## Related Skills

- `legal-research-education` — if UU PDP compliance questions come up
- `deep-research` / `scrapegraph-ai-scraping` — broader web research tooling
- MCP tools: `mcp_exa_web_search_exa` (has people category), `mcp_firecrawl_search`
