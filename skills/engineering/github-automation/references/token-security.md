# Why Tokens in Chat Are Dangerous

## The Problem
When a GitHub Personal Access Token (PAT) appears in conversation history:

1. **GitHub Scans for Leaked Tokens** - Automated systems detect tokens in public/private logs
2. **Immediate Revocation** - GitHub invalidates the token within minutes
3. **Account Risk** - Repeated leaks can trigger account restrictions

## What "In Chat" Means
- Any message you send to this AI containing `ghp_...` or `gho_...` or `github_pat_...`
- The token is now in the conversation transcript
- Even if deleted from visible chat, it's in the session history

## Visual Detection
```
Token pattern: ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (40 chars)
              gho_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (40 chars)
              github_pat_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (80+ chars)
```

## What Happens When Used
```bash
# This WILL fail if token was ever in chat:
git push https://ghp_XXXX@github.com/user/repo.git
# Error: remote: Invalid username or password
# fatal: Authentication failed
```

## Correct Alternatives

| Method | Security | Use Case |
|--------|----------|----------|
| `gh auth login` (device flow) | ✅ Secure | All automated operations |
| SSH Keys | ✅ Secure | Git push/pull only |
| Environment variable (set locally) | ⚠️ Temporary | One-off scripts only |
| GitHub Actions secrets | ✅ Secure | CI/CD pipelines |

## User Frustration Signal
> "Just use the token I gave you"

**Response:** The token is already compromised. Run `gh auth login` once, then everything works automatically forever.

## Prevention
1. Never paste tokens in chat
2. Use `gh auth login` for automation
3. Store tokens in password manager (Bitwarden, 1Password, KeePass)
4. Revoke immediately if accidentally pasted