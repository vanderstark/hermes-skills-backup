---
name: hacking-labs-docker-ctf
description: "Use when creating Docker CTF hacking challenge labs."
---

# 🐳 Docker-Based Hacking Challenge Labs (CTF/Competition-Ready)

**Reusable framework for creating hands-on cybersecurity challenge labs in Docker.**

---

## 📌 When to Use This Skill

- Building **vulnerable app labs** for CTF competitions or training
- Creating **challenge collections** (LAB-001, LAB-002, etc.) with consistent structure
- Deploying **interactive hacking exercises** (SQL injection, XSS, command injection, etc.)
- Needing **reproducible, isolated environments** for security testing
- Authoring **step-by-step solution documentation** with multiple difficulty levels

---

## 🎯 Core Pattern (Reusable Template)

Each lab follows this structure:

```
hacking-lab-lab00X-<vulnerability-type>/
├── Dockerfile              (Flask/vulnerable app container)
├── app.py                  (100-150 lines: vulnerable code + endpoints)
├── docker-compose.yml      (Service orchestration on unique port)
├── requirements.txt        (Python deps: Flask, Werkzeug)
├── README.md              (Comprehensive deployment + solution guide)
└── templates/
    └── index.html         (300-400 lines: interactive frontend UI)
```

---

## 📋 Checklist: Create New Lab

### 1️⃣ Plan the Vulnerability
- [ ] Choose CWE type (SQL Injection, XSS, Command Injection, etc.)
- [ ] Assign lab number (LAB-001, LAB-002, ...)
- [ ] Set difficulty (Easy, Medium, Hard, Expert)
- [ ] Estimate solve time (15-45 min)
- [ ] Define objective (extract data, bypass auth, execute code, etc.)
- [ ] Determine flag format: `HACKING_LAB{extracted_value}`

### 2️⃣ Build Vulnerable App (`app.py`)
- [ ] 80-150 lines, Flask-based
- [ ] Initialize Flask + session setup
- [ ] Main endpoint (`/`) → return `index.html`
- [ ] Vulnerable endpoint (POST/GET) with **unguarded input** (key!)
- [ ] Secondary endpoint (`/data` or `/admin`) with target data (flag)
- [ ] Health check endpoint (`/health`)
- [ ] Use **hardcoded secret data** for demo (password, token, etc.)
- [ ] Mark vulnerable lines: `# ⚠️ VULNERABLE - NOT FOR PRODUCTION`

### 3️⃣ Create Interactive Frontend (`templates/index.html`)
- [ ] 300-400 lines, dark cybersecurity theme
- [ ] Challenge info card (objective + hints)
- [ ] Input form (matches vulnerable endpoint)
- [ ] Real-time exploitation results display
- [ ] "Success" indicator when objective achieved
- [ ] Inline flag/data display after successful exploit

### 4️⃣ Containerize (Dockerfile + Compose)
- [ ] Use `FROM python:3.11-slim`
- [ ] Copy app + requirements, expose unique port
- [ ] Include HEALTHCHECK (curl `/health`)
- [ ] `docker-compose.yml` with port mapping `500X:500X`
- [ ] `requirements.txt`: Flask 3.0.0 + Werkzeug 3.0.0

### 5️⃣ Document (`README.md` 400-600 lines)
**Sections (critical for learner success):**
- Objective + Difficulty + Time estimate
- 3-Minute Quick Start (clone → `docker-compose up` → browse)
- Vulnerable code snippet (exact unsafe lines)
- **3+ Solution methods** (basic → intermediate → advanced)
- Expected results + flag extraction
- **Secure code fix** (how to remediate)
- Educational notes (real-world impact, OWASP/CWE refs, exploit chain)
- Troubleshooting (common errors)

### 6️⃣ GitHub Setup (Private Repos)
- [ ] **Naming:** `hacking-lab-lab00X-<type>` (e.g., `hacking-lab-lab001-sqli`)
- [ ] Create **PRIVATE** repo via GitHub API **from the very first push** — don't default to public and fix it later. Include `"private":true` in the initial `POST /user/repos` call every time.
- [ ] `git init && git add -A && git commit && git push -u origin main`
- [ ] If push fails with "Repository not found", the repo doesn't exist yet — create it via API first, THEN push (don't assume `git remote add` alone creates the remote repo).
- [ ] Verify files pushed: `git log --oneline`

### 7️⃣ Verify & Test
- [ ] Docker build: `docker-compose up -d`
- [ ] Health check: `docker-compose ps` (healthy status)
- [ ] Frontend loads: `curl http://localhost:500X`
- [ ] Vulnerable endpoint reachable
- [ ] Exploitation payload works (manual browser/curl test)
- [ ] Flag extracted + matches expected format

---

## 📚 Solution Documentation Pattern

**Each README MUST include 3+ solution methods** (escalating difficulty):

| Level | Method | Effort | Example (XSS) |
|-------|--------|--------|---------------|
| **Beginner** | Direct inject | 2 min | `<img src=x onerror="alert(1)">` |
| **Intermediate** | API extract | 10 min | Fetch `/session`, read JSON response |
| **Advanced** | Automated payload | 20 min | Obfuscated JS, exfiltrate data |

This ensures learners of all skill levels succeed.

---

## 🛠️ Port Convention

**Incremental ports for lab isolation:**

| Lab | Vulnerability | Port |
|-----|---------------|------|
| LAB-001 | SQL Injection | 5000 |
| LAB-002 | Reflected XSS | 5001 |
| LAB-003 | Command Injection | 5002 |
| LAB-004 | Path Traversal | 5003 |
| LAB-005 | Auth Bypass | 5004 |

**Rule:** `5000 + LAB_NUMBER` prevents port conflicts during parallel testing (LAB-001→5000, LAB-006→5005, LAB-015→5014, etc.)

---

## 🏭 Batch Generation (Multiple Labs in One Session)

When the user asks for a batch of labs at once (e.g. "buat 10 lab sekaligus"):

- **Do NOT dispatch `delegate_task` in parallel batches of 3+ for this.** Each generated lab needs ~6 files (app.py, Dockerfile, docker-compose.yml, requirements.txt, templates/index.html, README.md) which burns multiple LLM calls per subagent; running 3 subagents concurrently reliably trips provider rate limits (HTTP 429) and the whole batch comes back empty. Generate lab files directly in the main session with `write_file` calls instead — no LLM call is spent per file, only per your own turn.
- Writes to shared temp/scratch paths (e.g. `/tmp`) may be blocked by `HERMES_WRITE_SAFE_ROOT` sandboxing — write directly into the target repo directory under the allowed root instead of staging in `/tmp`.
- After every lab's files are written, immediately `git init && git add -A && git commit`, create the GitHub repo (private, see above), `git remote add origin` + `git push` — don't batch the pushes for later; push each lab as soon as its files are ready so partial progress survives interruptions.
- Keep a `todo` list with one item per lab number so progress is visible and resumable if the session is interrupted mid-batch.

---

## ⚠️ Critical Pitfalls

**DON'T:**
- Mix vulnerable + secure code in same app.py (confuses learners on what to fix)
- Forget HEALTHCHECK in Dockerfile (breaks `docker-compose ps` visibility)
- Use `debug=True` in production Flask mode (reveals stack traces, security risk)
- Hardcode secrets in Git (use `git push -f` to rewrite history if leaked)
- Skip solution walkthrough (defeats educational purpose)
- Omit secure code examples (learners won't know how to fix vulnerabilities)
- **Ship a lab without a complete README in the SAME turn you create the app files.** In one session, labs 3, 4, and 5 were created with thin/missing READMEs and the user had to separately ask, three times, to "fix the README with clear deploy and solve steps" for each one. The README (with 3-Minute Quick Start + full step-by-step solution + secure-code fix) is not an optional follow-up — write it as part of the initial lab delivery, every time, no exceptions.

**DO:**
- Mark vulnerable lines with `# ⚠️ VULNERABLE` comments
- Provide **inline secure fixes** in README
- Test locally before pushing
- Use consistent naming across all labs
- Document real-world impact (how this vulnerability led to breaches/losses)
- Keep repos **PRIVATE** until explicitly released for competition

---

## 📋 Roadmap for 5-Lab Series

Suggested progression for CTF competition (12-16 weeks):

| Lab | Vulnerability | Complexity | Timeline |
|-----|---------------|-----------|----------|
| LAB-001 | SQL Injection | Easy-Medium | 1-2 weeks |
| LAB-002 | Reflected XSS | Easy-Medium | 2-3 weeks |
| LAB-003 | Command Injection | Medium | 2-3 weeks |
| LAB-004 | Path Traversal | Medium-Hard | 3 weeks |
| LAB-005 | Auth Bypass | Hard | 3-4 weeks |

---

## 🔐 Legal & Security Notes

**Required for each lab:**
- Disclaimer: "For educational purposes only"
- Warning: "Do not use against systems you do not own"
- Reference UU ITE compliance (Indonesia) or equivalent jurisdiction
- Use only **demo hardcoded data** (never real credentials)
- Include OWASP Top 10 + CWE reference links

---

## 🧪 Quick Verification Script

```bash
#!/bin/bash
# Verify lab deployment
docker-compose up -d
sleep 5
curl -s http://localhost:500X/health | grep -q '"status":"ok"' && echo "✅ Health OK" || echo "❌ Health failed"
curl -s http://localhost:500X/ | grep -q "OBJECTIVE\|Challenge" && echo "✅ Frontend OK" || echo "❌ Frontend failed"
```

---

## 📖 Session Examples

- **LAB-001 SQLi** (`hacking-lab-lab001-sqli`): Login bypass + password extraction via `' OR '1'='1`
- **LAB-002 XSS** (`hacking-lab-lab002-xss`): Session token theft via `<img onerror=...>` payload

---

## 🔗 Related Skills

- `docker-development` — Docker for regular (non-vulnerable) apps
- `cybersecurity-500-soal` — Theory/ABCD questions (complements hands-on labs)

---

**Version:** 1.0  
**Status:** Production-Ready  
**Last Updated:** 17 Agustus 2026
