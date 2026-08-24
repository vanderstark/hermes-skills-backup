---
name: "github-skills-discovery"
title: "GitHub Skills Discovery & Installation"
description: "Use when bulk-installing skills from GitHub."
---

# GitHub Skills Discovery & Installation

**Trigger:** When you need to expand the Hermes skill library by searching GitHub for:
- Skill repos matching specific categories (marketing, CX, finance, etc.)
- Plugin bundles (GTM agents, composio skills, etc.)
- Integration packs (MCP servers, marketplace providers)
- When users request "install skill pack" or equivalent

**Outcome:** Batch-installed skills in `/opt/data/skills/<name>/`, verified locally, documented inventory, and GitHub backup of installation manifest.

---

## Workflow

### Phase 1: Search & Discover

```bash
# Search pattern: category + "skills" + language filters
curl -s "https://api.github.com/search/repositories?q=<category>+skills+language:python&sort=stars&per_page=5"

# Extract: full_name, stargazers_count, description
# Filter: relevance, maturity (stars > 5 preferred), recent updates
```

**Categories to search (examples):**
- `sales+marketing` → GTM/sales automation
- `customer-experience` / `customer-success` → CS automation
- `financial-advisor` → fintech skills
- `education+training` → curriculum/learning
- `design+creative` → UI/brand/animation
- `research+analysis` → market/academic

**Red flags:**
- Last update > 2 years ago (likely abandoned)
- Stars = 0 (unproven)
- No clear SKILL.md or manifest
- Incompatible license (GPL; prefer MIT/Apache2)

### Phase 2: Install Locally

```bash
cd /opt/data/skills
git clone --depth=1 https://github.com/<owner>/<repo>.git <local-name>
# Use friendly name, not raw repo name (e.g., 'gtm-agents' not 'gtmagents/gtm-agents')
```

**Handle timeouts:**
- Clone with `--depth=1` (latest commit only, faster)
- If clone timeout persists → repo is huge or rate-limited; skip or manual install later
- Log: which repos timed out for retry

**Verify:**
```bash
ls /opt/data/skills/<name>/
# Check for: README.md, SKILL.md, plugin.json, or manifest files
```

### Phase 3: Create Inventory Document

Build `INSTALLED-SKILLS.md` with:
```markdown
# Installation Date & Motivation
- Date installed
- Source (GitHub search query)
- Target (what gap this fills)

## Newly Installed Skills (Today)
- `<name>` — Description, key counts (agents, plugins, skills)

## Category Coverage (N/13 Complete)
| # | Kategori | Status | Skills Installed |
|---|----------|--------|------------------|
| 1 | CATEGORY | ✅ | count + skills |

## Installation Summary by Date
### <Date>
- ✅ skill-name (category)
```

### Phase 4: Backup to GitHub

```bash
cd /opt/data/hermes-skills-backup
git add INSTALLED-SKILLS.md SKILLS-DIRECTORY.md
git commit -m "Add/update skills inventory: <N> skills installed, <X>/<Y> categories complete (<skill-names>)"
git push origin main
```

**Document format:**
- One line per installed skill in commit message
- Inventory markdown for future reference
- Category matrix for at-a-glance coverage

---

## Pitfalls

1. **Confusing skill repos with plugin repos**
   - Skill repo: contains `SKILL.md` + references/scripts (Hermes native)
   - Plugin repo: contains `.claude-plugin/` (Claude marketplace format)
   - Some do both (claude-skills-pack); both are installable

2. **Clone timeout = abandon**
   - Repos >100MB or rate-limited by GitHub will timeout
   - Don't treat as "repo is broken" — try `--depth=1` or manual clone later
   - Log attempt; move on to next candidate

3. **Duplicate installations**
   - Check `ls /opt/data/skills/` before cloning
   - Avoid cloning same repo under different names
   - If already installed, log status and skip

4. **No verification of content**
   - Don't assume a 500-star repo is usable for Hermes
   - Check: does it have SKILL.md? Is LICENSE MIT/Apache? Is it abandoned?
   - If "looks good but no guarantees," note in inventory

5. **Forgetting to commit to GitHub**
   - Inventory lives in local `/opt/data/skills/` only until pushed
   - Always push backup to `vanderstark/hermes-skills-backup` (or equivalent)
   - Future sessions can't reference installed skills if not documented

---

## Success Signals

✅ `git clone` completed (repo in `/opt/data/skills/`)  
✅ `README.md` or `SKILL.md` exists in cloned directory  
✅ Category coverage matrix updated (N/13 shows progress)  
✅ GitHub push succeeded (commit visible on main branch)  
✅ Inventory markdown clear (future sessions can reference)  

---

## Manual Push Fallback (when `shell` / `terminal` tools fail)

Jika tools `shell` atau `terminal` tidak berfungsi (seperti di sesi ini), gunakan pendekatan manual dengan **satu perintah** yang bisa user jalankan:

```bash
cd /path/to/repo && \
git branch -m main && \
git remote set-url origin https://<TOKEN>@github.com/<owner>/<repo>.git && \
git add . && \
git commit -m "feat: <message>" --allow-empty && \
git push -u origin main --force && \
rm -f /tmp/gh_token_file && \
echo "✅ PUSH KE GITHUB BERHASIL"
```

**Catatan:**
- Simpan token di `/tmp/gh_token_file` dengan `chmod 600`
- Hapus token setelah push (`rm -f /tmp/gh_token_file`)
- Gunakan `--allow-empty` jika tidak ada perubahan file
- `--force` untuk overwrite history (aman untuk template baru)

### Template Manual Push Script

Simpan sebagai `scripts/manual-push.sh` di repo skill:

```bash
#!/bin/bash
# manual-push.sh — Fallback push when Hermes tools unavailable
set -euo pipefail
REPO_PATH="${1:-/opt/data/ai-clone}"
TOKEN_FILE="${2:-/tmp/gh_token_file}"
GH_USER="${3:-vanderstark}"
GH_REPO="${4:-polri-llm-v4-clone}"

if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "❌ Token file not found: $TOKEN_FILE"
    echo "Buat: echo 'ghp_xxx' > $TOKEN_FILE && chmod 600 $TOKEN_FILE"
    exit 1
fi

TOKEN=$(cat "$TOKEN_FILE" | tr -d '\n')
REMOTE_URL="https://${TOKEN}@github.com/${GH_USER}/${GH_REPO}.git"

cd "$REPO_PATH"
git branch -m main 2>/dev/null || true
git remote set-url origin "$REMOTE_URL"
git add .
git commit -m "feat: automated push from fallback script" --allow-empty
git push -u origin main --force

# Cleanup
rm -f "$TOKEN_FILE"
echo "✅ PUSH KE GITHUB BERHASIL: https://github.com/${GH_USER}/${GH_REPO}"
```

**Usage:**
```bash
chmod +x scripts/manual-push.sh
./scripts/manual-push.sh /opt/data/ai-clone /tmp/gh_token_file vanderstark polri-llm-v4-clone
```

---

## Related Skills

- `hermes-agent` — Configure Hermes, load skills from GitHub
- `skill-creator` — When creating a NEW skill from scratch (not bulk-install)
