---
name: github-bulk-repo-publishing
description: "Publish N generated artifacts as N separate GitHub repos."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, bulk, automation, api, curl, token-hygiene, repo-per-variant]
    related_skills: [github-repo-management, github-auth, docker-development]
---

# GitHub Bulk Repo Publishing

Use when a task produces **multiple independent local folders that each
need their own separate GitHub repo** — not one repo with subfolders.
Common trigger: "make N different variants of X and put EACH one in its
own repo" (e.g. one repo per Docker Compose combination, one repo per
config preset, one repo per environment). This is distinct from
`github-repo-management`'s single-repo create/clone/fork flows — the
value here is the *loop*, the *verification per iteration*, and the
*token hygiene discipline* across a batch of API calls.

## When `gh` isn't installed

Check first: `command -v gh`. If missing (`gh: command not found`) and no
`GITHUB_TOKEN`/git-credential-helper is already configured, the user will
need to supply a Personal Access Token directly. Expect it to arrive
**in the chat**, which means it will sit in plaintext conversation
history — that's a platform fact, not something to fix retroactively.
What IS controllable is covered in "Token hygiene" below.

## Core loop

```bash
export GH_TOKEN="<token>"   # shell-local only; never write to a committed file/script

GH_USER="<github-username>"

for dir in path/to/variant-*/ ; do
  name=$(basename "$dir")

  # 1. Create the repo via API — capture status + body to verify success
  status=$(curl -s -o /tmp/repo_resp.json -w "%{http_code}" \
    -X POST -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"${name}\",\"description\":\"...\",\"private\":false,\"auto_init\":false}")
  if [ "$status" != "201" ]; then
    echo "[CREATE_FAILED] ${name}: $(cat /tmp/repo_resp.json)"
    continue
  fi

  # 2. Init + commit + push from the local folder — subshell so `cd` doesn't leak
  (
    cd "$dir" \
    && git init -q \
    && git config user.name "${GH_USER}" \
    && git config user.email "${GH_USER}@users.noreply.github.com" \
    && git add -A \
    && git commit -q -m "Initial commit: ${name}" \
    && git branch -M main \
    && git remote add origin "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${name}.git" \
    && git push -u origin main \
    && git remote set-url origin "https://github.com/${GH_USER}/${name}.git"
  ) && echo "[OK] ${name}" || echo "[PUSH_FAILED] ${name}"
done

unset GH_TOKEN
```

For scripted/batch generation (not one-off), write this as a Python
`subprocess` driver instead of raw bash when the folder list itself was
also generated programmatically (e.g. a matrix of `{webserver} x
{version}` combinations) — keeps repo-name derivation and the
create+push logic in one reviewable script instead of interpolated shell.
See `scripts/bulk_create_repos.py` for a reusable driver.

## Verify, don't trust exit codes alone

A `git push` returning success doesn't guarantee the expected files
landed (empty commit, wrong branch, `.gitignore` silently excluding
everything). After the loop, spot-check at least 2-3 repos:

```bash
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/${GH_USER}/${name}/contents/" \
  | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
```

Report the verified count back to the user ("22/22 repos confirmed via
API"), not just "push succeeded."

## Token hygiene (do every time, not just once per session)

- Never write the token into a committed file, generator script, or
  memory entry — treat it as shell-session-scoped only.
- `git remote set-url origin <token-free-url>` **immediately after each
  push**, not batched at the end — if the loop is interrupted partway,
  fewer local remotes are left holding the token.
- `unset GH_TOKEN` and `rm -f` any temp response files once the batch's
  results are verified.
- If the token was pasted in chat, remind the user to revoke/rotate it
  at https://github.com/settings/tokens once the task is done — and
  **repeat this reminder every time the same token gets reused** across
  multiple asks in one session (e.g. "make repo A" ... later "now also
  publish B" ... later "also C") rather than assuming one mention earlier
  in the conversation covers all of them. Each reuse is a fresh exposure.

## Naming and scoping the repos

Before looping, confirm with the user whether they want:
- **one repo per variant** (this skill's use case) — e.g. `nginx-php8.3-laravel`, `apache-php8.3-laravel`, ...
- **one umbrella repo with subfolders** — simpler, less repo-sprawl, better for related variants meant to be browsed together

Don't assume — this is a real fork in the deliverable shape and asking
once up front avoids redoing the whole batch under the other model
(this happened in practice: an umbrella repo was built first, then the
user asked for the same content split into per-variant repos instead).

## Related Skills

- `github-repo-management` — single-repo create/clone/fork/release flows this skill's loop is built from
- `github-auth` — token/gh setup if authentication itself isn't configured yet
- `docker-development` — if the artifacts being published are Docker templates specifically
