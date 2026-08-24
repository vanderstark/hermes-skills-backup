---
name: osint-toolkit-installation
title: OSINT Toolkit Installation & Setup
trigger: Use when installing open-source OSINT tools (Sherlock, theHarvester, SpiderFoot, Shodan, Exiftool) for authorized research. Legal public sources only.
description: Install 5+ open-source OSINT tools legally.
---

## 🔍 OSINT Toolkit Installation & Setup

**Scope:** Installing & verifying open-source OSINT tools for authorized research, investigations, or training labs. Legal public-source collection only (no dark web, no unauthorized access).

---

## Quick Reference

| Tool | Type | Install |
|------|------|---------|
| **Sherlock** | Username search | `pip install sherlock-project` |
| **theHarvester** | Email/subdomain | `git clone --depth=1 https://github.com/laramies/theHarvester.git && cd theHarvester && pip install -r requirements.txt` |
| **SpiderFoot** | Reconnaissance | `git clone --depth=1 https://github.com/smicallef/spiderfoot.git && cd spiderfoot && pip install -r requirements.txt` |
| **Shodan CLI** | Internet search | `pip install shodan` |
| **Exiftool** | Metadata extract | `pip install exiftool` |

---

## Installation Steps (Linear Order)

### 1. **Create Directory**
```bash
mkdir -p /opt/data/osint && cd /opt/data/osint
```

### 2. **Install pip-based Tools**
```bash
pip install sherlock-project shodan exiftool
```

**Pitfall:** Use `pip3` if `pip` not found.

### 3. **Clone Git Tools (use --depth=1 to avoid timeout)**
```bash
cd /opt/data/osint

# theHarvester
git clone --depth=1 https://github.com/laramies/theHarvester.git
cd theHarvester && pip install -r requirements.txt && cd ..

# SpiderFoot
git clone --depth=1 https://github.com/smicallef/spiderfoot.git
cd spiderfoot && pip install -r requirements.txt && cd ..
```

**Pitfall:** `git clone` hangs 45+ seconds = timeout. Always use `--depth=1`.

### 4. **Verify with Script**
Create `osint-verify.sh`:

```bash
#!/bin/bash
sherlock --version && echo "[OK] Sherlock" || echo "[FAIL] Sherlock"
shodan --version && echo "[OK] Shodan" || echo "[FAIL] Shodan"
cd /opt/data/osint/theHarvester && python3 theHarvester.py -h >/dev/null 2>&1 && echo "[OK] theHarvester" || echo "[FAIL] theHarvester"
cd /opt/data/osint/spiderfoot && python3 sf.py -m sfp_dns -t test.com >/dev/null 2>&1 && echo "[OK] SpiderFoot" || echo "[FAIL] SpiderFoot"
exiftool -v >/dev/null 2>&1 && echo "[OK] Exiftool" || echo "[FAIL] Exiftool"
```

Run: `bash osint-verify.sh`

---

## Legal Boundaries

### ✅ Authorized Use
- Written permission + security research
- Institution-approved academic
- Law enforcement with warrant
- Bug bounty (within scope)
- Public source collection

### ❌ Prohibited
- UU ITE Pasal 30 violations (Indonesia)
- Unauthorized data access
- Doxxing, stalking, harassment
- Dark web sources
- Credential misuse

---

## Pitfalls & Fixes

| Issue | Fix |
|-------|-----|
| `pip not found` | Use `pip3` or `python3 -m pip` |
| `git clone` hangs | Always use `--depth=1` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in cloned dir |
| Script permission denied | `chmod +x osint-verify.sh` |
| Sherlock fails username | Try common username (john.doe, admin, test) |
| theHarvester needs API | Check `theHarvester --help` for API configuration |

---

## Usage

```bash
# Sherlock username search
sherlock username123

# theHarvester email harvest
cd /opt/data/osint/theHarvester
python3 theHarvester.py -d example.com -b google

# SpiderFoot recon
cd /opt/data/osint/spiderfoot
python3 sf.py -m sfp_dns -t example.com

# Shodan internet search
shodan search "apache"
```

---

## Git Deploy

```bash
cp osint-verify.sh /opt/data/hermes-skills-backup/
cd /opt/data/hermes-skills-backup
git add osint-verify.sh
git commit -m "Add OSINT Toolkit: 5 tools + verification"
git push origin main
```
