# GitHub API Repo Creation

## Create New Repository
```bash
TOKEN="ghp_xxx"
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"repo-name","description":"Description","private":false,"auto_init":false}'
```

## HTTP Status Codes
- `201` — Created successfully
- `422` — Validation failed (name exists, invalid chars)
- `401` — Authentication failed (token invalid/expired)

## Token Storage Security
```
echo "ghp_xxx" > /tmp/gh_token_file
chmod 600 /tmp/gh_token_file
# Use in git push:
git remote set-url origin https://$(cat /tmp/gh_token_file)@github.com/user/repo.git
# After push:
rm -f /tmp/gh_token_file
```

## Alternative via Python
```python
import subprocess
token = open('/tmp/gh_token_file').read().strip()
remote = f"https://{token}@github.com/user/repo.git"
subprocess.run(['git', 'remote', 'set-url', 'origin', remote])
```
