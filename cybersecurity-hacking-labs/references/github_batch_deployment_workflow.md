# GitHub Batch Deployment Workflow for 20+ Hacking Labs

This document captures the end-to-end workflow for deploying 20+ lab repositories to GitHub, learned during LAB-049 through LAB-068 deployment.

---

## Complete Workflow

### Phase 1: Prepare All Lab Directories Locally
```
hacking-lab-docker/
├── lab-049-ssrf/
├── lab-050-xxe/
├── ...
├── lab-068-sri-bypass/
```
Each directory must contain ALL files before Git operations:
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `app.py`
- `templates/index.html` (if applicable)
- `README.md`

### Phase 2: Create GitHub Repositories (API)
```bash
# Create all repos first, then push
# This avoids rate limiting and 503 errors during push

curl -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $GH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"hacking-lab-labXXX-vulnname","description":"LAB-XXX: Vulnerability Name Challenge","private":true}'

# Do this for all 20 labs with sleep 2 between calls
```

### Phase 3: Initialize Git & Push (Per Lab)
```bash
# CRITICAL: git init inside EACH lab directory, not parent!
for lab in lab-049-ssrf lab-050-xxe ... lab-068-sri-bypass; do
  cd /opt/data/hacking-lab-docker/$lab
  
  # Initialize
  git init
  git config user.email "hermes@localhost"
  git config user.name "Hermes Agent"
  git checkout -b main
  
  # Add all files (including README!)
  git add -A
  git commit -m "feat: LAB-XXX Vulnerability Name Challenge"
  
  # Set remote (CONSISTENT naming!)
  # Pattern: hacking-lab-labXXX-vulnname (NO dash before XXX)
  git remote add origin "https://$GH_TOKEN@github.com/vanderstark/hacking-lab-labXXX-vulnname.git"
  
  # Push
  git push -u origin main
done
```

---

## Critical Rules (Learned from Failures)

### Rule 1: Write → Commit → Push = SAME STEP
- `write_file` only writes to local disk
- It does NOT commit or push
- After ANY file write (especially README), immediately:
  ```bash
  git add <file> && git commit -m "..." && git push origin main
  ```
- Verify with `git status --short` across ALL lab dirs before declaring "done"

### Rule 2: Consistent Repo Naming
- ✅ CORRECT: `hacking-lab-lab060-http-request-smuggling` (no dash before 060)
- ❌ WRONG: `hacking-lab-lab-060-http-request-smuggling` (dash before 060)
- Use EXACT SAME convention for:
  1. GitHub API repo creation
  2. `git remote add/set-url`
  3. Any documentation/reference

### Rule 3: Git Filesystem Boundary
- Each lab = separate git repo
- `git init` INSIDE lab directory
- NOT in parent directory (`hacking-lab-docker/`)
- Otherwise git sees everything as one repo

### Rule 4: Token Hygiene
- Never log actual token values
- Mask in output: `ghp_***` or `***`
- Revoke token after batch deployment
- Use separate token for this specific task

### Rule 5: Verify Push Success
```bash
# Check each lab after push
for lab in lab-049-ssrf ... lab-068-sri-bypass; do
  echo "=== $lab ==="
  git -C "$lab" log --oneline -1
  git -C "$lab" ls-remote --heads origin main
done
```

---

## Troubleshooting Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `remote: Repository not found` | Wrong repo name in remote URL | `git remote -v` then `git remote set-url origin <correct-url>` |
| `fatal: not a git repository` | Forgot `git init` | Run `git init` in lab dir |
| `nothing added to commit` | File not tracked | `git add <file>` before commit |
| `up to date` but no README on GitHub | File committed but not pushed | `git push origin main` |
| GitHub API 503/rate limit | Too many parallel calls | Create repos sequentially with `sleep 2` |

---

## Batch Verification Script
```bash
#!/bin/bash
# Run this AFTER all pushes to verify everything is on GitHub

BASE="https://api.github.com/repos/vanderstark"
LABS=(
  "lab049-ssrf" "lab050-xxe" "lab051-ssti" "lab052-jwt-algo-confusion"
  "lab053-cors-misconfiguration" "lab054-dom-xss" "lab055-race-condition"
  "lab056-file-upload-bypass" "lab057-coupon-stacking" "lab058-api-versioning"
  "lab059-insecure-deserialization" "lab060-http-request-smuggling"
  "lab061-web-cache-deception" "lab062-oauth-pkce-bypass"
  "lab063-graphql-batching-dos" "lab064-websocket-hijacking"
  "lab065-idor-uuid" "lab066-csp-bypass"
  "lab067-template-injection-freemarker" "lab068-sri-bypass"
)

for lab in "${LABS[@]}"; do
  echo -n "Checking $lab... "
  curl -s -H "Authorization: token $GH_TOKEN" \
    "$BASE/hacking-lab-$lab/contents/README.md" | grep -q '"name": "README.md"' \
    && echo "✅ README found" || echo "❌ README MISSING"
done
```

---

## Checklist Before Declaring "Done"

- [ ] All 20 labs have `README.md` file locally
- [ ] All 20 labs have `git init` + at least one commit
- [ ] All 20 repos created on GitHub (verify via API)
- [ ] All 20 repos pushed (verify with `git log --oneline -1` + `git ls-remote`)
- [ ] `git status --short` returns empty for all 20 labs
- [ ] Token revoked/regenerated
- [ ] User notified of any failures

---

## Port Assignment Reference (LAB-049 to LAB-068)

| Lab | Port |
|-----|------|
| 049 SSRF | 5048 |
| 050 XXE | 5049 |
| 051 SSTI | 5050 |
| 052 JWT Algo | 5051 |
| 053 CORS | 5052 |
| 054 DOM XSS | 5053 |
| 055 Race | 5055 |
| 056 File Upload | 5056 |
| 057 Coupon | 5057 |
| 058 API Version | 5058 |
| 059 Deserialization | 5059 |
| 060 Request Smuggling | 5060 |
| 061 Cache Deception | 5061 |
| 062 OAuth PKCE | 5062 |
| 063 GraphQL DoS | 5063 |
| 064 WebSocket | 5064 |
| 065 IDOR UUID | 5065 |
| 066 CSP | 5066 |
| 067 Freemarker | 5067 |
| 068 SRI | 5068 |

---

## Key Lesson

**"Local file existence ≠ GitHub deployment"**

The user asked "tolong di github nya juga di update dong" after a batch where:
- 11 of 13 READMEs were written locally (via `write_file`)
- But only 2 were committed + pushed
- The rest sat as untracked files (`?? README.md`)

**Root cause:** Treating "write file" and "deploy to GitHub" as separate steps with a gap between them. They must be atomic — write → commit → push in one continuous operation per file.

**For future:** After every `write_file` to a lab directory that's already a git repo, immediately execute the commit + push sequence. Never assume "I'll push later" — later becomes never, and the user has to ask.