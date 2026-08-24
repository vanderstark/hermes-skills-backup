# Manual Push Fallback Reference

When tools `shell` / `terminal` fail, use this one-command approach:

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

**Template script** (`scripts/manual-push.sh`):
- Input: repo path, token file path, GitHub user, repo name
- Output: success message or error with token cleanup

**Security:**
- Never commit token to repo
- Delete token after push
- Token stored chmod 600 only