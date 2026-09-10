# SSH Keys vs GitHub CLI (gh)

## Quick Comparison

| Capability | SSH Keys | gh CLI (Device Flow) |
|------------|----------|----------------------|
| `git clone` | ✅ | ✅ (via HTTPS) |
| `git push` | ✅ | ✅ (via HTTPS) |
| `git pull` | ✅ | ✅ (via HTTPS) |
| **Create repo** | ❌ | ✅ `gh repo create` |
| **Delete repo** | ❌ | ✅ `gh repo delete` |
| **Manage secrets** | ❌ | ✅ `gh secret set` |
| **Manage workflows** | ❌ | ✅ `gh workflow enable` |
| **Create PR** | ❌ | ✅ `gh pr create` |
| **Manage issues** | ❌ | ✅ `gh issue create` |
| **API access** | ❌ | ✅ `gh api` |

## When to Use Each

### SSH Keys
- Daily `git push/pull/fetch` operations
- CI/CD runners that only need git operations
- When you want passwordless git without browser auth

### gh CLI (Device Flow)
- **Creating new repositories** (the #1 use case here)
- Managing repo settings, secrets, workflows
- Any GitHub API operation
- Full automation after one-time `gh auth login`

## The Critical Insight from This Session

**User had SSH key set up but couldn't push because repo didn't exist.**

```bash
# SSH works for this:
git push origin main
# But ONLY if repo already exists!

# gh CLI does BOTH:
gh repo create owner/repo --private --source=. --push
# Creates repo AND pushes in one command
```

## Setup Both (Recommended)

```bash
# 1. SSH for daily git ops
ssh-keygen -t ed25519 -C "your-email"
# Add ~/.ssh/id_ed25519.pub to GitHub Settings → SSH Keys

# 2. gh CLI for automation
gh auth login  # One-time device flow
```

## Then Use Appropriately

```bash
# New project - fully automated:
cd my-project
gh repo create owner/my-project --private --source=. --push

# Daily work - git with SSH:
git push origin main

# Need to add secret:
gh secret set AWS_KEY --body="xxx" --repo=owner/my-project
```