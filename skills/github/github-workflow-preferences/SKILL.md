---
name: github-workflow-preferences
description: "Enforces gh CLI usage and user-specific auth patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Workflow, Preferences, gh-cli, Authentication]
    related_skills: [github-auth, github-repo-management, github-pr-workflow]
---

# GitHub Workflow Preferences for Hermes Agent

This skill encodes the specific GitHub workflow preferences of the user (Bos) to ensure the agent follows their preferred patterns.

## Core Principle: gh CLI First, Always

**User Preference:** "User explicitly prefers using `gh` CLI for ALL GitHub operations: repo create, push, sync, release, secrets, workflows."

**Decision Rule:** When `gh` is installed (regardless of authentication status), ALWAYS use `gh` commands. Never fall back to git-only or curl-based methods when `gh` is available.

## Authentication Workflow

When working with GitHub repositories:

1. **Check for gh availability:**
   ```bash
   gh --version 2>/dev/null || echo "gh not installed"
   ```

2. **If gh is installed (PREFERRED PATH):**
   - Check auth status: `gh auth status`
   - If not authenticated: 
     * Interactive: `gh auth login`
     * Headless: `echo "<TOKEN>" | gh auth login --with-token`
   - Always run: `gh auth setup-git` (configures git credentials for underlying git operations)
   - Proceed with ALL GitHub operations using `gh` subcommands

3. **Only if gh is NOT installed:**
   - Fall back to git-only authentication methods (HTTPS with PAT or SSH)
   - Use curl for API calls when needed

## Specific Workflow Patterns Enforced

### Repository Creation

**Preferred (gh):**
```bash
gh repo create my-new-project --public --clone
```

### Pushing Changes

**Always use gh repo sync or gh push when possible:**
```bash
# After making changes locally
gh repo sync  # Preferred
# OR
 git push  # Only if gh not available
```

### File Operations

**Never embed tokens in URLs:**
- ❌ DO NOT use: `https://<token>@github.com/user/repo.git`
- ✅ ALWAYS use: `gh auth setup-git` then standard git/gh operations

### Token Handling

**Never create token files in /tmp:**
- Tokens should only exist briefly in memory when piping to gh auth
- Never write tokens to disk unless using git's credential helper store
- Immediately revoke PAT after push operations when user provides temporary token

## Verification Steps

After any GitHub operation sequence, verify:

1. `gh auth status` shows authenticated
2. `git config --global credential.helper` is set (store or cache)
3. No token remnants in shell history or temporary files

## Common Corrections from User

Based on session observations:

- ❌ **WRONG:** Creating token files in /tmp for authentication
- ✅ **CORRECT:** Using `echo "<TOKEN>" | gh auth login --with-token` for headless auth

- ❌ **WRONG:** Embedding tokens in git remote URLs
- ✅ **CORRECT:** Using `gh auth setup-git` to configure credentials properly

- ❌ **WRONG:** Using git-only methods when gh is available
- ✅ **CORRECT:** Always preferring gh CLI for GitHub operations

- ❌ **WRONG:** Using `git push https://$(gh auth token)@github.com/...` without verifying token expiry
- ✅ **CORRECT:** Using `gh auth status` first, then `$(gh auth token)` only for the current session push, and revoking immediately after

- ❌ **WRONG:** Leaving PAT tokens in chat history or session memory
- ✅ **CORRECT:** Immediately revoke PAT after push operations when user provides temporary token; never store tokens in chat history

- ❌ **WRONG:** Using direct git commands for repo creation when gh CLI is available
- ✅ **CORRECT:** Using `gh repo create` for all repository creation operations

- ❌ **WRONG:** Pushing code without first checking repo contents via `gh api /repos/owner/repo/contents`
- ✅ **CORRECT:** Always verify repo contents before and after push operations, especially when user reports files that don't appear locally

- ❌ **WRONG:** Assuming all files from historical context are present in the current working directory
- ✅ **CORRECT:** Always verify file existence locally with `ls -la` or `gh api` before assuming file presence, especially after context compaction

- ❌ **WRONG:** Using `git rm` without first confirming file existence in the working tree
- ✅ **CORRECT:** Use `gh api /repos/owner/repo/contents/path` to verify file exists in remote before attempting local operations

- ❌ **WRONG:** Moving files between directories without verifying both source and destination states
- ✅ **CORRECT:** Use `gh api` to verify file states at both source and destination before/after move operations (e.g., README.md move from subfolder to root)

## References

- See `github-auth` skill for detailed authentication methods
- See `github-repo-management` for repository operations
- User preference: Always use gh when available, never embed tokens, never create token files in /tmp
