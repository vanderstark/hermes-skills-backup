---
name: skill-learning-backup-workflow
description: Learn skills then push notes to GitHub backup repo.
---

# Skill Learning → GitHub Backup Workflow

Class of task: user names one or more skills to learn/study, then expects
the resulting artifacts (notes, examples, checklists) pushed to a personal
GitHub backup repo, autonomously. Typical phrasing: "pelajari skill X, Y, Z
terus upload ke github <url>".

## User preference (hard rule, not optional)

This operator ("Bos") has repeatedly stated: **autonomous action over
descriptions**. When the request is "pelajari X, terus upload ke github":

- Do NOT reply with a "rencana materi belajar" / study-plan list and stop
  there waiting for confirmation. That is a narration-only turn and is a
  direct violation of the standing preference.
- Go straight to: (1) load the named skills via `skill_view`, (2) write
  the condensed learning artifact directly to files in the target repo,
  (3) commit, (4) push, (5) report back tersely with what was pushed
  (commit hash / files) — not what you're about to do.
- If genuinely blocked (e.g. divergent branch, missing token), say so in
  one line and take the corrective action yourself before asking — don't
  stop at "berikut rencana saya" and wait.
- Format: RAPI markdown tables, Indonesian language, address user as
  "Bos", 3x 🙏 per message. This skill exists to make sure that standing
  preference actually gets applied during learn+push tasks specifically,
  since it has been violated in this class of task before.

## Artifact shape

Don't paste long explanations into the chat. Write the material as files
under the target backup repo, e.g.:

```
<repo>/notes/<skill-name>-learned.md         # condensed cheat-sheet
<repo>/observations/<skill-name>-session.md  # optional session findings
```

Each `notes/<skill-name>-learned.md` should be short (condensed knowledge,
not a mirror of the source skill) — trigger conditions, the core workflow
in bullet steps, and any pitfalls found while testing it.

## GitHub token handling in the Hermes sandbox

**Do not write the token to `/tmp/...`.** File writes are sandboxed by
`HERMES_WRITE_SAFE_ROOT` (typically `/opt/data`); a write outside that root
is denied with `"Write denied: '...' is outside HERMES_WRITE_SAFE_ROOT"`.
This is a durable sandbox rule, not a one-off environment issue — it will
recur every session.

**Working procedure (proven this session):**

```bash
export GITHUB_TOKEN="<token>"
git -C <repo_path> remote set-url origin "https://${GITHUB_TOKEN}@github.com/<owner>/<repo>.git"
git -C <repo_path> push origin main
unset GITHUB_TOKEN
```

- Embed the token directly in the remote URL via env var interpolation —
  no file write needed at all.
- After the push, `unset GITHUB_TOKEN` and remind the user to revoke the
  token at github.com/settings/tokens (per this operator's standing
  security procedure — never keep a PAT alive longer than the push).
- If a project's own `AGENTS.md` specifies a token-file procedure (e.g.
  `/tmp/gh_token_file` chmod 600), that predates the sandbox root
  restriction and will fail the same way — use the env var method above
  instead, and note the discrepancy to the user once.

## Divergent branch handling

Before pushing, always `git fetch origin` and compare `HEAD` to
`origin/<branch>`. If diverged (local behind remote), do **not** force-push.
Resolve with `git pull --rebase origin <branch>` first, verify
`git status` is clean, then push. Never overwrite remote history silently
— remote commits may include security-relevant changes (e.g. removed
sensitive docs) that must not be lost.

## Pitfalls observed

- Replying with a bulleted "study plan" (topics to cover, checkboxes) and
  ending the turn there is NOT progress on this task type — it reads as
  stalling to this operator. Either the files exist and are pushed, or
  the task isn't done.
- Don't ask "mau saya mulai yang mana dulu?" when the user already said
  "pelajari semua" (all of them) — that's already the answer, proceed.
- `skill_view` with a bare skill name is ambiguous when several installed
  collections share that name (e.g. `research`, `ai-security`). Pass the
  full categorized path (`ecc/deep-research`,
  `finance/octagon/financial-analyst-master`) instead.
