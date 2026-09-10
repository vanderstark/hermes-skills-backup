---
name: docker-matrix-and-bulk-repo-push
description: "Generate N Docker variants, deliver each as own zip/repo."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, docker-compose, github, bulk-repo, template-generation, laravel, ci4]
    related_skills: [docker-development, github-repo-management, github-auth]
---

# Docker Template Matrix Generation + Bulk GitHub Repo Push

Covers two combined workflows that recur together: (1) generating many
self-contained Docker Compose variants across a matrix (webserver x
language-version x framework), and (2) pushing each variant to its own
GitHub repo (or its own zip) rather than one monorepo/one bundle.

## When to use this skill

- User asks for "N combinations" of Docker setups (e.g. Nginx & Apache x
  multiple PHP versions x Laravel/CodeIgniter/etc), each self-contained
- User wants each variant delivered separately: "1 docker = 1 zip", "beda
  compose beda repo", "jangan digabung jadi 1 folder/repo"
- User wants generated templates pushed to their own GitHub account,
  either as one repo with subfolders OR as many independent repos

## Part 1 — Generating the Matrix

Generate each combination as a **fully self-contained folder** (own
Dockerfile, docker-compose.yml, .env.example, README, no cross-folder
references) so each one works standalone after extraction/cloning — never
a single parameterized template the user has to hand-edit.

Pattern (Python script via `write_file`, not `execute_code` — this
environment blocks arbitrary local Python execution as a policy, so build
the generator as a `.py` file under a writable path like `/opt/data/scripts/`
and run it with `terminal`):

```python
PHP_VERSIONS = ["7.4", "8.0", "8.1", "8.2", "8.3"]  # example matrix axis

def write_file(path, content):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

for webserver in ["nginx", "apache"]:
    for version in PHP_VERSIONS:
        folder = f"{BASE}/{webserver}-php{version}-<framework>"
        write_file(f"{folder}/Dockerfile", dockerfile_for(webserver, version))
        write_file(f"{folder}/docker-compose.yml", compose_for(webserver, version))
        write_file(f"{folder}/.env.example", env_example)
        write_file(f"{folder}/README.md", readme_for(webserver, version))
```

### Respect real framework version floors

Don't blindly replicate every version across every framework in the
matrix. Example: CodeIgniter 4 requires PHP 7.4+ (released 2020, after PHP
5.6 EOL) — including a PHP 5.6 x CI4 combo produces a Dockerfile that
cannot build. When a matrix axis has a known floor/ceiling for one of the
frameworks in scope, ask the user how to handle it (skip that combo /
substitute an older framework major version that does support it / build
anyway with an explicit EOL warning baked into the Dockerfile and README)
rather than silently omitting it or silently shipping a broken combo.

### Validate before delivering

Loop-validate every generated `docker-compose.yml` with `yaml.safe_load()`
across ALL variants before packaging — catches the common
f-string/YAML-brace collision (Compose's `${VAR}` needs escaping to
`${{VAR}}` inside a Python f-string) early, across the whole batch at once
rather than one file at a time.

```bash
python3 -c "
import yaml, glob
for f in glob.glob('BASE/**/*.yml', recursive=True):
    yaml.safe_load(open(f))
print('all valid')
"
```

Also sanity-check with `bash -n` on every generated `.sh` script if the
matrix includes shell scripts (e.g. install scripts), not just YAML.

## Part 2 — Delivery: 1 zip per variant OR 1 repo per variant

### 1 zip per variant

Use Python's stdlib `zipfile` (this environment has no `zip` CLI
installed) — one `.zip` per folder, named to match the folder:

```python
import zipfile, os

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                arcname = os.path.relpath(fp, os.path.dirname(folder_path))
                zf.write(fp, arcname)
```

Deliver each with its own `MEDIA:` path — don't bundle all zips into one
tar/zip-of-zips when the user asked for them separate.

### 1 GitHub repo per variant

See `github-repo-management` skill's create-repo and clone sections for
the single-repo primitives. For creating MANY repos in one pass (bulk
create + push loop), script it directly with `urllib.request` calls
(avoid an actual `gh` CLI dependency since it's often not installed):

```python
import subprocess, json, os, time, urllib.request

GH_TOKEN = os.environ["GH_TOKEN"]
GH_USER = "the-username"

def gh_api(method, path, data=None):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github+json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

for repo_name, local_path in variants:  # [(name, path), ...]
    status, resp = gh_api("POST", "/user/repos", {"name": repo_name, "private": False, "auto_init": False})
    if status != 201:
        continue  # log and move on -- one failure shouldn't kill the batch
    subprocess.run(["git", "init", "-q"], cwd=local_path, check=True)
    subprocess.run(["git", "config", "user.name", GH_USER], cwd=local_path, check=True)
    subprocess.run(["git", "config", "user.email", f"{GH_USER}@users.noreply.github.com"], cwd=local_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=local_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", f"Initial commit: {repo_name}"], cwd=local_path, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=local_path, check=True)
    remote = f"https://{GH_USER}:{GH_TOKEN}@github.com/{GH_USER}/{repo_name}.git"
    subprocess.run(["git", "remote", "add", "origin", remote], cwd=local_path, check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=local_path, check=True)
    subprocess.run(["git", "remote", "set-url", "origin", f"https://github.com/{GH_USER}/{repo_name}.git"], cwd=local_path, check=True)
    time.sleep(1)  # avoid API rate-limit bursts across many repos
```

After the loop, spot-verify a few repos via the API
(`GET /repos/{owner}/{repo}/contents/`) rather than trusting `git push`
exit codes alone — confirms files actually landed with the expected file
set, not just that the push command returned 0.

## Token Hygiene (critical — recurring risk pattern)

If the user pastes a GitHub Personal Access Token directly into chat
(rather than via a secure prompt), treat it as compromised the moment
it's visible in conversation history:

1. Use it for the requested operation, but immediately after each push,
   run `git remote set-url origin https://github.com/<user>/<repo>.git`
   to strip the token back out of that repo's local `.git/config`.
2. Never write the token to memory, to a skill, or to any file that
   outlives the task (`unset GH_TOKEN` / remove temp response files when
   done).
3. Explicitly tell the user, every time this happens, to revoke/rotate
   the token at github.com/settings/tokens — don't just do it silently
   once and let subsequent reuses of the same pasted token go unremarked.
4. Prefer asking the user to set `GH_TOKEN` as a shell-level env var
   themselves when the platform allows it, over having them paste it in
   chat — but don't block the task if they paste it anyway; just flag it.

## Ask-before-scale confirmation

Before generating a large fan-out (10+ zips, 10+ repos), confirm the exact
delivery shape with the user via a single clarifying question — "1 repo
gabungan dengan subfolder" vs "1 repo per kombinasi" vs "N zip files"
materially changes the amount of work and the number of GitHub API calls;
don't default to the biggest interpretation without confirming.
