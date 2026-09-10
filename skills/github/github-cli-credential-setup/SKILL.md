---
name: github-cli-credential-setup
category: github
description: Fix git push failures with gh CLI authentication.
---

## github-cli-credential-setup

Use this skill when `git push` fails with authentication errors like "Username for 'https://github.com': No such device or address" even though `gh auth status` shows the user is logged in.

### Problem:
Git cannot authenticate to GitHub using the token stored by `gh auth login`. The credential helper needs to be configured.

### Solution:

Run the following commands:

```bash
gh auth setup-git
```

This configures the local Git credential helper to use the authentication token stored by `gh auth login`.

### Verification:

After running the setup, verify by pushing again:

```bash
git push origin main
```

### Alternative Manual Fix (if `gh auth setup-git` fails):

1.  **Set credential helper globally:**
    ```bash
    git config --global credential.helper store
    ```
2.  **Manually set credentials (less secure):**
    ```bash
    git config --global credential.username <your-github-username>
    git config --global credential.helper store
    ```
    Then run `git push` and enter your token as the password when prompted.

### Pitfalls:
*   **Token Scope:** Ensure your PAT (Personal Access Token) has the required scopes (`repo`, `workflow` for push/deploy).
*   **Token Expiration:** Check if your token has expired (GitHub tokens may have an expiration date).

