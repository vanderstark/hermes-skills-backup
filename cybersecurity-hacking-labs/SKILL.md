---
name: cybersecurity-hacking-labs
title: Cybersecurity Hacking Labs - Docker CTF Challenges
description: Build Docker-based hacking labs for CTF competitions.
trigger: Use when creating hands-on CTF challenges with vulnerable apps.
---

# 🔓 Cybersecurity Hacking Labs — Docker-Based Practical Challenges

Build production-ready hands-on hacking labs with vulnerable applications, interactive frontends, Docker deployment, and step-by-step exploitation guides.

---

## 🎯 When to Use This Skill

- ✅ Creating new CTF/hacking challenges (labs, exercises)
- ✅ Building vulnerable applications intentionally for learning
- ✅ Containerizing challenges with Docker + Docker Compose
- ✅ Writing deployment + exploitation guides
- ✅ Designing multi-lab series (LAB-001, LAB-002, etc.)

---

## 📋 Lab Directory Structure

```
hacking-lab-<name>/
├── Dockerfile                 # Minimal container
├── docker-compose.yml        # Port, volume, health checks
├── requirements.txt          # Dependencies
├── app.py (main app)         # Vulnerable application
├── templates/index.html      # Interactive frontend (if needed)
└── README.md                 # Deployment + solution guide
```

---

## 🔧 5-Phase Build Process

### Phase 1: Design & Plan
1. Define vulnerability (CWE identifier)
2. Set objective (what to extract/exploit)
3. Pick framework (Flask, Express, Spring)
4. Set difficulty (Easy/Medium/Hard)
5. Estimate time (30min to 2+ hours)

### Phase 2: Build Vulnerable App
- Start minimal (single file if possible)
- Comment why it's vulnerable
- Add debug output (SQL queries, request details)
- Pre-initialize database with test data
- Include `/health` endpoint returning `{"status":"ok"}`

### Phase 3: Frontend (Optional)
- Interactive UI for user input
- Visual feedback (success/error/flag display)
- Clear instructions + hints
- Semantic HTML

### Phase 4: Docker Configuration
- **Dockerfile:** Minimal image with HEALTHCHECK
- **docker-compose.yml:** Port mapping, restart policy, healthcheck
- Test locally: `docker-compose up -d`

### Phase 5: Comprehensive README (400+ lines)

Must include:
1. Objective & description
2. Quick Start (3-minute deployment)
3. Challenge details (vuln, difficulty, time)
4. Deployment guide (step-by-step)
5. Solution walkthrough (2+ methods) — **USER PREFERENCE: Indonesian, beginner-friendly 5-step format: Eksplorasi → Exploit → Verifikasi → Capture Flag → Submit. Must explain WHY exploits work, not just WHAT. Include ❌ VULNERABLE vs ✅ SECURE code comparison.**
6. Educational content (why vulnerable, secure fix)
7. Troubleshooting (common errors + fixes)

---

## 🔐 Security Considerations

- ✅ Scope vulnerability (one clear CWE per lab)
- ✅ Add comments explaining vulnerability
- ✅ Include secure fix examples
- ✅ Docker isolation (exploits can't escape)
- ✅ Healthchecks for reliable deployment
- ✅ Log interactions for debugging

---

## 📊 Naming & Organization

**Single lab:** `hacking-lab-<vuln-name>` (e.g., `hacking-lab-sqli`)

**Multi-lab series (production-ready, sequential numbering):**
```
hacking-labs-complete/
├── lab-001-sqli/
├── lab-002-xss/
├── lab-003-command-injection/
└── README.md
```

**Large-scale batch series (40+ labs, GitHub private repos):**
```
# GitHub repo naming: hacking-lab-lab<NNN>-<vuln-slug>
# Port assignment: sequential (5028-5068 for 20 labs)
# Example batch 049-068:
#   hacking-lab-lab049-ssrf (port 5048)
#   hacking-lab-lab050-xxe (port 5049)
#   ...
#   hacking-lab-lab068-sri-bypass (port 5068)
```

**Repo structure per lab:**
```
hacking-lab-labXXX-vulnname/
├── Dockerfile                 # Minimal, HEALTHCHECK
├── docker-compose.yml         # Port, restart, healthcheck
├── requirements.txt           # Dependencies
├── app.py                     # Vulnerable Flask app
├── templates/index.html       # Interactive frontend
├── README.md                  # 400+ lines: deploy + 2+ solutions + secure fix
└── .gitignore                 # .env, __pycache__, *.pyc
```

---

## ✅ Quality Checklist

- [ ] Runs via `docker-compose up -d` (no manual steps)
- [ ] Health endpoint responds within 5s
- [ ] Vulnerability is exploitable (manually tested)
- [ ] README: clear deployment + 2+ solutions
- [ ] Database pre-initialized
- [ ] Dockerfile minimal
- [ ] Educational comments in code
- [ ] Git repo committed + pushed

---

## 📚 Pitfalls & Fixes

| Pitfall | Fix |
|---------|-----|
| App crashes in Docker | Add HEALTHCHECK, test locally |
| Port conflicts | Override port in docker-compose.yml |
| Can't exploit | Provide 2+ exploitation methods |
| Vague README | Step-by-step format + actual commands |
| Difficulty mismatch | Test with target audience |
| Database not initialized | Auto-init in app.py |
| No success signal | Display flag on success |

**Large-batch pitfalls (20+ labs):**
| Pitfall | Fix |
|---------|-----|
| GitHub API rate limit / 503 | Retry with exponential backoff, create repos first then push |
| Git filesystem boundary | `git init` inside each lab dir, not parent |
| Token leaked in logs | Never log tokens; use `ghp_***` masking |
| Sequential port exhaustion | Plan ports upfront (e.g., 5028-5068), verify no conflicts |
| README drift across labs | Use template + auto-generate for consistency |
| **README written locally but never pushed** | `write_file` only touches disk — it does NOT commit or push. After writing/updating any README (or any file) in a lab dir, immediately run `git add <file> && git commit -m "..." && git push origin main` as part of the SAME step, not a later cleanup pass. Verify with `git status --short` across all lab dirs before telling the user "done" — an untracked or unpushed file means the work isn't actually live on GitHub yet, even though it exists locally. This caused a user to have to ask "update github juga dong" after a whole doc-fix batch because 11 of 13 READMEs were sitting uncommitted. |
| **Repo naming inconsistency breaks push** | Some repos were created/referenced as `hacking-lab-lab060-...` (no dash before number) and others as `hacking-lab-lab-060-...` (dash before number) for the same lab — causing `git push` to fail with "Repository not found" against the wrong URL. Pick ONE convention (`hacking-lab-lab<NNN>-<slug>`, no dash before the number) and use it consistently for repo creation AND `git remote add/set-url` — never assume the remote URL matches without checking `git remote -v` first when a push fails. |

---

## 🎯 Multi-Lab Roadmap (LAB-001 to LAB-068)

| Lab | Vulnerability | Difficulty | Time | Framework |
|-----|----------------|-----------|------|-----------|
| 001-028 | Original batch (XPath, Clickjacking, GraphQL, Prototype Pollution, ReDoS, etc.) | Easy-Hard | 15-45min | Flask |
| 029 | XPath Injection | Easy | 15min | Flask |
| 030 | Clickjacking | Easy | 15min | Flask |
| 031 | GraphQL Introspection | Medium | 20min | Flask |
| 032 | Prototype Pollution | Medium | 25min | Flask |
| 033 | ReDoS | Medium | 25min | Flask |
| 034 | Insecure Randomness | Easy | 15min | Flask |
| 035 | Host Header Injection | Medium | 20min | Flask |
| 036 | Session Fixation | Medium | 20min | Flask |
| 037 | Weak OTP | Easy | 15min | Flask |
| 038 | Zip Slip | Medium | 20min | Flask |
| 039 | SSI Injection | Medium | 20min | Flask |
| 040 | Second-Order SQLi | Medium | 25min | Flask |
| 041 | Unvalidated POST Redirect | Easy | 15min | Flask |
| 042 | Excessive Data Exposure | Easy | 15min | Flask |
| 043 | Broken Function Level AuthZ | Medium | 20min | Flask |
| 044 | Command Injection | Medium | 20min | Flask |
| 045 | localStorage + XSS | Medium | 25min | Flask |
| 046 | Cache Poisoning | Hard | 30min | Flask |
| 047 | Subdomain Takeover | Medium | 25min | Flask |
| 048 | Improper Rate Limiting | Easy | 15min | Flask |
| 049 | SSRF | Easy | 15min | Flask |
| 050 | XXE | Easy | 15min | Flask |
| 051 | SSTI (Jinja2 RCE) | Medium | 20min | Flask |
| 052 | JWT Algorithm Confusion | Medium | 20min | Flask |
| 053 | CORS Misconfiguration | Easy | 15min | Flask |
| 054 | DOM-based XSS | Easy | 15min | Flask |
| 055 | Race Condition (TOCTOU) | Medium | 20min | Flask |
| 056 | File Upload Bypass | Easy | 15min | Flask |
| 057 | Coupon Stacking (Business Logic) | Easy | 15min | Flask |
| 058 | API Versioning Bypass | Medium | 20min | Flask |
| 059 | Insecure Deserialization (Pickle) | Medium | 20min | Flask |
| 060 | HTTP Request Smuggling | Hard | 25min | Flask |
| 061 | Web Cache Deception | Medium | 20min | Flask |
| 062 | OAuth PKCE Bypass | Medium | 20min | Flask |
| 063 | GraphQL Batching DoS | Medium | 20min | Flask |
| 064 | WebSocket Hijacking | Medium | 20min | Flask |
| 065 | IDOR via UUID Enumeration | Easy | 15min | Flask |
| 066 | CSP Bypass | Medium | 20min | Flask |
| 067 | Freemarker Template Injection | Medium | 20min | Flask |
| 068 | SRI Bypass | Medium | 20min | Flask |

---

## 🚀 Fast Track (2 Hours per Lab)

1. 30min: Design + research
2. 30min: Build vulnerable app
3. 30min: Configure Docker
4. 30min: Write README

**Large-batch parallelization (20 labs):**
- Phase 1 (parallel): Write all `app.py` + templates (4-5 hours)
- Phase 2 (parallel): Docker + docker-compose + requirements (1 hour)
- Phase 3 (sequential): README generation using template (2-3 hours)
- Phase 4 (parallel): Git init + GitHub push (1-2 hours)

---

**Example:** github.com/vanderstark/hacking-lab-sqli  
**Status:** Production-Ready (68 labs complete)  
**Updated:** 17 Agustus 2026
