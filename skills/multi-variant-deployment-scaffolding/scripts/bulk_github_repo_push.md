# Bulk GitHub Repo Creation + Push Loop

Reference pattern for pushing many local folders as separate GitHub
repos in one pass. Validated working for 22 repos in a single run
(no `gh` CLI required — pure `curl` + `git`).

```bash
export GH_TOKEN="<token>"
GH_USER="<username>"

for dir in /path/to/variants/*/; do
  repo_name=$(basename "$dir")

  # 1. Create the repo via API — check status before proceeding
  status=$(curl -s -o /tmp/repo_resp.json -w "%{http_code}" \
    -X POST -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"$repo_name\",\"private\":false,\"auto_init\":false}")
  [ "$status" = "201" ] || { echo "FAILED create: $repo_name (status $status)"; continue; }

  # 2. git init + commit + push (token only lives in remote URL transiently)
  ( cd "$dir" \
    && git init -q \
    && git config user.name "$GH_USER" \
    && git config user.email "${GH_USER}@users.noreply.github.com" \
    && git add -A \
    && git commit -q -m "Initial commit: $repo_name" \
    && git branch -M main \
    && git remote add origin "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${repo_name}.git" \
    && git push -u origin main \
    && git remote set-url origin "https://github.com/${GH_USER}/${repo_name}.git" )  # strip token immediately after push
done

unset GH_TOKEN
rm -f /tmp/repo_resp.json
```

## Post-run verification (don't skip)

Spot-check at least 2-3 repos via the Contents API to confirm files
actually landed, rather than trusting loop exit codes alone:

```bash
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/$GH_USER/$repo_name/contents/" \
  | python3 -c "import json,sys; [print(i['type'],i['name']) for i in json.load(sys.stdin)]"
```

## Token hygiene checklist

- Strip token from git remote URL immediately after each push (shown
  above) — don't leave it sitting in `.git/config`.
- `unset GH_TOKEN` and delete any temp files holding raw API responses
  once the batch finishes.
- If the user pasted the token as plain chat text (common when there's
  no secrets vault available), treat it as burned regardless of technical
  validity — tell them to revoke/rotate it at
  https://github.com/settings/tokens once the task is done. If the
  conversation reuses the same token across multiple asks (e.g. terminal
  session state reset and the user re-pasted it), repeat the reminder
  each time rather than assuming one mention covered it.
