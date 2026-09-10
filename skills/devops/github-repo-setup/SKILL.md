---
name: github-repo-setup
description: Create GitHub repos with README and push content.
---
Use when you need to create a new GitHub repository (public or private), initialize it with a README, and push initial content. This skill covers the full workflow: repo creation via API, local init, commit, push, and setting visibility.

## Steps

1. **Prepare content locally** (e.g., write README.md, script files).
2. **Create repository via GitHub API** (using a personal access token):
   ```bash
   curl -s -X POST -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \
     https://api.github.com/user/repos \
     -d '{"name":"<repo-name>","description":"<description>","private":true}'
   ```
   Replace `<repo-name>`, `<description>`, and set `"private":true` or `false` as needed.
3. **Initialize local git repository**:
   ```bash
   git init -q -b main
   git add <files>
   git commit -q -m "initial: add <description>"
   ```
4. **Add remote and push**:
   ```bash
   git remote add origin https://$TOKEN@github.com/<username>/<repo-name>.git
   git push -u origin main
   # Remove token from remote URL for security:
   git remote set-url origin https://github.com/<username>/<repo-name>.git
   unset GITHUB_TOKEN
   ```
5. **Verify**:
   - Check that the repo is public/private as intended.
   - Ensure README appears on GitHub.

## Pitfalls

- **Never hardcode tokens in scripts** – always use environment variable and unset after use.
- **Always reset the remote URL** after pushing to avoid leaking the token in `git remote -v`.
- **Ensure the repo name is unique** under your account; otherwise the API will return 422.
- **If the repo already exists**, you cannot recreate it; instead, push to the existing repo or delete it first (if allowed).
- **Remember to set the correct visibility** (`private`: true/false) at creation; changing it later requires a PATCH request.

### ⚠️ Critical: `gh repo create` Does NOT Set Up Local Git

**Problem:** `gh repo create <name>` creates the remote repo but does NOT initialize or configure your local git repository. After running `gh repo create`, your local directory may still have no `.git/` folder, or the remote may point to the wrong repo.

**Symptoms:**
- `git push` fails with "src refspec main does not match any"
- `git remote -v` shows the wrong repository URL
- User says "the repo is empty on GitHub" after you claim it's pushed

**Fix — Always do this after `gh repo create`:**
```bash
# 1. Verify what gh actually created
gh repo view --web  # opens browser to confirm repo exists

# 2. If local .git is missing or wrong, re-init:
rm -rf .git
git init
git remote add origin https://github.com/<username>/<repo-name>.git

# 3. Add, commit, and force-push if needed
git add .
git commit -m "initial commit"
git push -u origin main --force
```

**Verification step — ALWAYS confirm after push:**
```bash
# Check that files actually made it to GitHub
git ls-remote origin | head -5
# Or visit the URL in a browser to visually confirm
```

**User frustration handling:** If the user says "it's not on GitHub", do NOT argue. Immediately:
1. Run `git remote -v` to check the remote URL
2. Run `git log --oneline` to check local commits
3. If mismatched, re-init and force-push
4. Confirm by visiting the GitHub URL

## References

- GitHub API documentation: https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user
- GitHub CLI alternative: `gh repo create <name> --private --push --description "<desc>"`

## Example

See the `pushup-counter` repository created in this session: https://github.com/vanderstark/pushup-counter (private).