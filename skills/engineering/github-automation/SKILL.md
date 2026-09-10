---
name: github-automation
description: Fully automated GitHub repo ops via gh CLI device-flow auth.
category: engineering
tags: [github, automation, ci-cd, gh-cli, device-flow, security]
---

# GitHub Automation Skill

**Trigger:** User wants fully automated GitHub repo creation, push, or management without manual browser steps after initial setup.

**Core Principle:** Use `gh auth login` (device flow) for one-time authentication, then `gh repo create --push` for fully automated operations. Never use tokens from chat.

---

## 🔐 Authentication: Device Flow (One-Time Setup)

```bash
# Run once per machine/environment
gh auth login
# Select: GitHub.com → HTTPS → Login with web browser
# Copy code → open https://github.com/login/device → paste → Authorize
```

**Result:** Token stored securely in `~/.config/gh/hosts.yml` (OS-only readable). No token ever appears in chat/logs.

---

## 🚀 Automated Operations (After Auth)

| Operation | Command |
|-----------|---------|
| Create private repo + push current dir | `gh repo create owner/repo --private --source=. --push` |
| Create public repo + push | `gh repo create owner/repo --public --source=. --push` |
| Push to existing repo | `gh repo deploy owner/repo --ref=main` (or `git push` with SSH) |
| Add secrets | `gh secret set KEY --body="value" --repo=owner/repo` |
| Enable workflows | `gh workflow enable ci.yml --repo=owner/repo` |

---

## ⚠️ Critical Pitfalls

### 1. **Tokens in Chat = Compromised**
- Any token pasted in chat is **immediately invalid** (GitHub detects & blocks)
- **Never** accept or use tokens from conversation history
- User frustration signal: "just use the token" → explain once, then redirect to `gh auth login`

### 2. **SSH Keys ≠ Repo Creation**
- SSH keys work for `git push/pull/fetch` only
- **Cannot** create repos via API (`gh repo create` or REST API needs token/OAuth)
- If user says "SSH is set up but push fails: Repository not found" → repo doesn't exist yet

### 3. **Repo Must Exist Before Push**
- `git push` to non-existent repo fails with "Repository not found"
- Always verify/create repo first: `gh repo create` or browser

---

## 🛡️ Security Protocol (Non-Negotiable)

| Scenario | Action |
|----------|--------|
| User pastes token in chat | Refuse, explain compromise, redirect to `gh auth login` |
| User says "disable security" | Explain: protects their account from permanent ban |
| User wants fully automated | `gh auth login` once → then fully automated forever |
| Token already in chat history | Consider compromised; user must revoke & regenerate |

---

## 📋 Standard Workflow for New Projects

```bash
# 1. One-time auth (if not done)
gh auth login

# 2. Create repo + push in one command
cd /path/to/project
gh repo create owner/repo-name --private --source=. --push

# 3. Subsequent pushes (no auth needed)
git push origin main
# OR via gh:
gh repo deploy owner/repo-name --ref=main
```

---

## 🔧 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Repository not found` | Repo doesn't exist | `gh repo create owner/repo --private --source=. --push` |
| `Permission denied (publickey)` | SSH key not added to GitHub | Add `~/.ssh/id_ed25519.pub` to GitHub Settings → SSH Keys |
| `401 Unauthorized` (API) | Token invalid/expired | Run `gh auth login` again |
| `remote: Repository not found` | Push to non-existent repo | Create repo first via `gh repo create` or browser |

---

## 📚 References

- `references/device-flow-auth.md` — Detailed device flow setup with screenshots
- `references/token-security.md` — Why tokens in chat are dangerous
- `references/ssh-vs-gh-cli.md` — When to use SSH vs gh CLI
- `scripts/verify-gh-auth.sh` — Verify gh auth status before operations

---

## 🎯 User Preference (Embedded)

> **User wants fully automated GitHub operations.** After one-time `gh auth login`, all repo create/push/manage should work without manual browser steps. Security blocks that require manual intervention are frustration signals — the workflow must be designed for zero-touch after initial auth.