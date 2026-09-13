---
name: gh-cli-workflow
description: "Use gh CLI for all GitHub ops. Override token workflows."
version: 1.0.0
author: Bos (Polri)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [github, gh-cli, workflow, git, security]
---

# GitHub CLI Workflow

**Use when** user explicitly prefers `gh` CLI for ALL GitHub operations: repo creation, push, PR, secrets, CI/CD. This overrides token-based workflows.

## 🔐 Authentication First

```bash
gh auth status
# If needed: gh auth login
```

## 🔧 Repository Operations

```bash
gh repo create OWNER/REPO --description "desc" --public
git clone https://github.com/OWNER/REPO.git
gh auth setup-git
```

## 🚀 Push Workflow (Bos Pattern)

```bash
git add .
git commit -m "feat: description"
git push -u origin main
```

## ⚠️ SECURITY - Bos Preferences

1. **NEVER embed tokens in git URLs**
2. **NEVER create token files in /tmp**
3. **NEVER commit .env or secret files**
4. **REVOKE tokens after push**
5. **Prefer SSH when possible**

## 📝 Bos Project Pattern

1. `gh auth status` (verify login)
2. `gh auth setup-git`
3. Clone/use local repo
4. Edit files
5. `git add .` → `git commit` → `git push -u origin main`
6. Close: "Terima Kasih"
7. Remind to revoke tokens if used