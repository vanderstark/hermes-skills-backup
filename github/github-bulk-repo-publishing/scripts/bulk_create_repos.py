#!/usr/bin/env python3
"""
Bulk-create GitHub repos from local folders, one repo per folder.

Reusable driver for the pattern in SKILL.md: given a base directory
containing N independently-deployable folders, create N GitHub repos
(one per folder name) and push each folder's contents as that repo's
initial commit.

Usage:
    export GH_TOKEN="<personal access token>"
    python3 bulk_create_repos.py <base_local_dir> <github_username> [--private]

Each subdirectory of <base_local_dir> becomes one repo named after the
subdirectory. Verifies each push via the GitHub contents API before
reporting success.
"""
import subprocess
import json
import os
import sys
import time
import urllib.request
import urllib.error


def gh_api(token, method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "bulk-repo-publisher",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <base_local_dir> <github_username> [--private]")
        sys.exit(1)

    base_dir = sys.argv[1]
    gh_user = sys.argv[2]
    private = "--private" in sys.argv[3:]

    token = os.environ.get("GH_TOKEN")
    if not token:
        print("ERROR: set GH_TOKEN in the environment first.")
        sys.exit(1)

    folders = sorted(
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    )
    if not folders:
        print(f"No subdirectories found under {base_dir}")
        sys.exit(1)

    print(f"Found {len(folders)} folders to publish as separate repos.\n")

    results = []
    for name in folders:
        local_path = os.path.join(base_dir, name)

        status, resp = gh_api(token, "POST", "/user/repos", {
            "name": name,
            "description": f"Generated: {name.replace('-', ' ')}",
            "private": private,
            "auto_init": False,
        })
        if status != 201:
            results.append((name, "CREATE_FAILED", resp.get("message", str(resp))))
            continue

        try:
            subprocess.run(["git", "init", "-q"], cwd=local_path, check=True)
            subprocess.run(["git", "config", "user.name", gh_user], cwd=local_path, check=True)
            subprocess.run(["git", "config", "user.email", f"{gh_user}@users.noreply.github.com"], cwd=local_path, check=True)
            subprocess.run(["git", "add", "-A"], cwd=local_path, check=True)
            subprocess.run(["git", "commit", "-q", "-m", f"Initial commit: {name}"], cwd=local_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=local_path, check=True)
            remote_url = f"https://{gh_user}:{token}@github.com/{gh_user}/{name}.git"
            subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=local_path, check=True)
            push = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=local_path,
                                   capture_output=True, text=True)
            if push.returncode != 0:
                results.append((name, "PUSH_FAILED", push.stderr[-300:]))
                continue
            # strip token from remote immediately
            subprocess.run(["git", "remote", "set-url", "origin", f"https://github.com/{gh_user}/{name}.git"], cwd=local_path, check=True)

            # verify via API that files actually landed
            vstatus, vresp = gh_api(token, "GET", f"/repos/{gh_user}/{name}/contents/")
            if vstatus == 200 and isinstance(vresp, list) and len(vresp) > 0:
                results.append((name, "OK", f"https://github.com/{gh_user}/{name} ({len(vresp)} items)"))
            else:
                results.append((name, "PUSHED_BUT_EMPTY", "verify failed — check manually"))
        except subprocess.CalledProcessError as e:
            results.append((name, "GIT_ERROR", str(e)))

        time.sleep(1)  # avoid API rate-limit bursts

    print(f"\n=== SUMMARY: {len(results)} repos processed ===\n")
    ok = sum(1 for r in results if r[1] == "OK")
    print(f"Success: {ok} / {len(results)}\n")
    for name, status, info in results:
        print(f"[{status}] {name} -> {info}")


if __name__ == "__main__":
    main()
