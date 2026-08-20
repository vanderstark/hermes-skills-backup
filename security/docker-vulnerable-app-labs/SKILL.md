---
name: docker-vulnerable-app-labs
trigger: Use when building Docker-containerized vulnerable apps for CTF/training.
description: Build intentionally-vulnerable Docker labs.
---

# 🔒 Docker Vulnerable App Labs

Create intentionally-vulnerable Docker apps for security training, CTF competitions, and hands-on learning.

---

## STANDARD STRUCTURE

Each lab follows this 5-file pattern:

```
lab-XXX-<vulnerability>/
├── app.py                    # Flask app with vulnerabilities
├── templates/index.html      # Interactive HTML frontend
├── Dockerfile                # Container image
├── docker-compose.yml        # Orchestration
├── requirements.txt          # Python dependencies
└── README.md                 # CRITICAL: Deploy + solution guide
```

---

## WORKFLOW (6 STEPS)

1. **Create Flask App** — Mark vulnerabilities with `⚠️ VULNERABLE`. Include flag inline. Add `/health` endpoint.
2. **Create HTML Frontend** — Dark theme, interactive form, auto-detect flags.
3. **Create Dockerfile** — Python 3.11-slim. Healthcheck. No debug mode.
4. **Create docker-compose.yml** — Single service. Unique port. Healthcheck.
5. **Create requirements.txt** — Flask, Werkzeug, + lab-specific deps.
6. **Create README.md** — Use full template from `references/readme-template.md`.

---

## README.MD STANDARD (13 SECTIONS - REQUIRED)

1. Header
2. About Challenge (metadata)
3. Learning Objectives (5-7)
4. QUICK DEPLOY GUIDE (3 min)
5. Credentials/Demo Data
6. STEP-BY-STEP SOLUTION (5+ steps)
7. Multiple Exploitation Methods (2-4 techniques)
8. Secure Code Examples (❌ vs. ✅)
9. Troubleshooting (7+ issues)
10. File Structure
11. Flag Details
12. Lab Series Status (table)
13. Footer (disclaimer)

**User preference (LAB-004/005):** This is the exact format you want. Use it for every lab.
**User preference (LAB-056-068):** Indonesian language, beginner-friendly 5-step format: Eksplorasi → Exploit → Verifikasi → Capture Flag → Submit. Must explain WHY exploits work, not just WHAT. Include ❌ VULNERABLE vs ✅ SECURE code comparison in README.

---

## PORT ASSIGNMENTS

Ports increment sequentially starting at 5000 (LAB-001) — each new lab = next free port.

| Lab | Port | Vulnerability | Lab | Port | Vulnerability |
|-----|------|----------------|-----|------|----------------|
| 001 | 5000 | SQL Injection | 011 | 5010 | API Key Exposure |
| 002 | 5001 | XSS Reflected | 012 | 5011 | SSTI (Jinja2 RCE) |
| 003 | 5002 | Command Injection | 013 | 5012 | CORS + CSRF Chain |
| 004 | 5003 | Path Traversal | 014 | 5013 | Weak Cryptography |
| 005 | 5004 | JWT Bypass | 015 | 5014 | Race Condition (TOCTOU) |
| 006 | 5005 | IDOR | 016 | 5015 | SSRF |
| 007 | 5006 | XXE Injection | 017 | 5016 | Stored XSS/HTML Injection |
| 008 | 5007 | CORS Misconfiguration | 018 | 5017 | Mass Assignment |
| 009 | 5008 | Insecure Deserialization | 019 | 5018 | NoSQL Injection |
| 010 | 5009 | Brute Force / No Rate Limit | 020 | 5019 | Open Redirect |
| 021 | 5020 | XXE Advanced (file read) | 026 | 5025 | LDAP Injection |
| 022 | 5021 | JWT Advanced (alg=none) | 027 | 5026 | File Upload RCE |
| 023 | 5022 | HTTP Header Injection (CRLF) | 028 | 5027 | Business Logic - Price Manipulation |
| 024 | 5023 | IDOR Advanced (predictable hash ID) | | | |
| 025 | 5024 | SSTI Advanced (filter bypass) | | | |

**Port rule:** next port = 5000 + (lab_number - 1). Always continue the sequence from the highest existing lab, don't reset.

---

## GITHUB WORKFLOW

1. `git init && git checkout -b main && git add -A && git commit -m "feat: LAB-### [Vulnerability] Challenge"` FIRST (before creating the remote repo) — this lets the commit succeed even if repo creation is slow/rate-limited.
2. Create private repo via API: `curl -X POST https://api.github.com/user/repos -d '{"name":"...","private":true}'`
3. `git remote add origin ...` then `git push -u origin main`
4. Naming: `hacking-lab-lab###-<slug>` (slug = short vulnerability name, e.g. `idor`, `ssti`, `open-redirect`)
5. Repo created with `"private":true` is already PRIVATE — no separate visibility-change step needed if set at creation.

**Pitfall:** if you `git remote add` + `git push` BEFORE the `curl -X POST .../repos` call finishes, push fails with "Repository not found" (repo doesn't exist yet). Always create the repo first, or push only after confirming `"full_name"` appeared in the create-repo response.

**GitHub API Rate Limit / 503 Handling (LAB-049-068 batch):**
- GitHub API sometimes returns 503 (unavailable) during repo creation
- Fix: Create all repos first via API with exponential backoff retry, then push sequentially
- Or: Push locally first, then create repo + push again when GitHub is available
- Never log the PAT token in terminal output — mask as `ghp_***`

---

## BATCH GENERATION (multiple labs in one session)

When the user asks for N more labs (e.g. "buat 5 soal lagi"), generate and push them **one at a time, sequentially, via write_file + terminal** — not via parallel subagent delegation. Delegating repetitive lab-file generation to `delegate_task` in batches hit provider rate limits (HTTP 429) repeatedly and wasted the whole batch; direct sequential execution in the main session is more reliable for this repetitive-but-simple file-generation pattern.

**Todo tool pitfall:** a single `todo` call listing all pending labs (10+ items with long descriptions) can exceed the stream size and time out. Keep todo updates small — a handful of short items — and update incrementally (mark done, add next batch) rather than writing the whole remaining roadmap in one call.

---

## PITFALLS & FIXES

| Pitfall | Fix |
|---------|-----|
| README too short | Use full template from `references/readme-template.md` |
| No solution steps | Provide 5+ steps: explore → identify → exploit → execute → flag |
| Single exploit method | Show Python, curl, online tools, manual |
| No troubleshooting | Add 7+ issues + solutions |
| Uncommented code | Mark each vuln with `⚠️ VULNERABLE` |
| No flag detection | Scan output for `FLAG_` pattern, show green box |
| Secrets too visible | Hide behind exploit — require genuine attack |
| Port conflicts | Assign unique ports sequentially |
| No healthcheck | Add HEALTHCHECK + `/health` endpoint |

---

## VERIFICATION CHECKLIST

- [ ] Dockerfile builds without errors
- [ ] `docker-compose up -d` starts successfully
- [ ] Health check passes
- [ ] Web UI loads at `http://localhost:PORT`
- [ ] Vulnerability is exploitable (test)
- [ ] Flag discoverable via exploit
- [ ] README has ALL 13 sections
- [ ] Secure code examples show FIX
- [ ] Troubleshooting covers 7+ scenarios
- [ ] Commit: `feat: LAB-### ...` format
- [ ] Repo set to PRIVATE
- [ ] Lab series status table updated

---

**Status:** Production-ready. Used for Polri cybersecurity academy + CTF competitions (Aug 2026+). 28/30 labs shipped as of Aug 2026 (LAB-001 through LAB-028), each in its own private GitHub repo `hacking-lab-lab###-<slug>`.

**Working pattern for "buat N soal lagi" requests:** deliver 3-5 labs per batch, sequentially, each fully self-contained: app.py → templates/index.html → requirements.txt → Dockerfile → docker-compose.yml → README.md → git init/commit → create GitHub repo via API → push. Confirm each push succeeded before starting the next lab. This has run reliably for 3 consecutive follow-up batches (5+5+3 labs) — keep repeating it verbatim for further "N soal lagi" asks, just continuing lab numbering/ports from the highest existing lab.
