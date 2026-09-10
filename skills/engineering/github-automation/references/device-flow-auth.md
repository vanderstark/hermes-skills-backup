# GitHub CLI Device Flow Authentication

## Overview
Device flow allows authentication without storing tokens in chat or environment variables. The token is stored securely in `~/.config/gh/hosts.yml`.

## Step-by-Step Setup

```bash
gh auth login
```

### Interactive Prompts:
1. **Account:** `GitHub.com`
2. **Protocol:** `HTTPS`
3. **Authenticate Git:** `Yes`
4. **Method:** `Login with a web browser`

### Browser Step:
```
Copy code: XXXX-XXXX
Open: https://github.com/login/device
Paste code → Authorize
```

## Verification
```bash
gh auth status
# Output: ✓ Logged in as vanderstark (keyring)
#         ✓ Token: gho_************************************
#         ✓ Git operations protocol: https
```

## Token Storage Location
```
~/.config/gh/hosts.yml
```
- File permissions: 600 (owner read/write only)
- Contains: oauth_token, user, git_protocol
- Never committed to git

## Re-authentication
```bash
gh auth login  # Re-run if token expires or revoked
```

## Common Issues

| Issue | Fix |
|-------|-----|
| "Could not prompt for code" | Run in terminal with TTY (not background) |
| "Authentication failed" | Check network, try again |
| Token expired | `gh auth login` again |
| Multiple accounts | `gh auth switch` |