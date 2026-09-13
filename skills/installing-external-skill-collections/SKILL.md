---
name: installing-external-skill-collections
description: Install skills into the library from a GitHub repo/URL.
---

# Installing External Skill Collections

Triggers: user gives a GitHub link (or similar) and asks to "install this skill" /
"install all the skills in this repo" / "add these skills to your library".

## Critical disambiguation: "install to Hermes" vs "push to GitHub"

When a user gives a GitHub URL and says "install this" / "masukkan ini" / "tambahkan
skill ini", confirm (or infer from phrasing) whether they mean:
- **Install into Hermes's local skill library** (`/opt/data/skills/`) so the agent can
  use it — this is what "install skill" almost always means.
- vs. **push/add a reference to that URL inside an unrelated GitHub repo** — a
  completely different action (editing README, adding a citation link).

These are easy to conflate when you're mid-session on GitHub repo work (e.g. pushing
tutorial repos) — a user saying "tolong masukkan <url>" right after a repo-push
task can get misread as "add this URL as a reference in the repo I'm pushing" instead
of "install these skills into Hermes." If ambiguous, ask; if the user explicitly
corrects you ("bukan di masukkan github", "maksud saya install ke hermes bukan di
push"), that confirms "install to Hermes" was the correct reading — don't guess wrong
twice in the same session.

## Procedure

1. **Inspect before cloning.** List the repo's top-level contents (GitHub API
   `contents` endpoint or a shallow clone) to see whether it's a *single skill*
   (one `SKILL.md` at root) or an *awesome-list* (many subdirectories, each its
   own skill). Awesome-lists are common and need a different strategy than a
   single-skill repo.

2. **Clone shallow to a scratch dir**, not directly into the skill library:
   `git clone --depth 1 <url> /tmp/<repo-name>`. Inspect before copying so a
   bad clone doesn't pollute `/opt/data/skills/`.

3. **Detect skill boundaries.** A directory is one installable skill iff it
   contains a `SKILL.md` directly inside it. Don't assume every top-level
   folder is a skill — some are just docs (`.github`, `CONTRIBUTING.md`) or
   nested collections (a folder containing many sub-folders that each have
   their own `SKILL.md`, e.g. `document-skills/{docx,pdf,pptx,xlsx}` or a
   giant `composio-skills/` tree with 800+ per-integration sub-skills).
   Walk one level deeper for any top-level dir that itself lacks a `SKILL.md`.

   Skills are often buried, not at repo root: `find <repo> -iname SKILL.md`
   across the whole clone rather than assuming a top-level `skills/` dir.
   Common real locations: `.claude/skills/*/SKILL.md`, `plugin/skills/*/`,
   `cli/assets/skills/*/`, `<product-name>/skills/*/`, or a `skills/` dir
   nested two or three levels down inside a larger app/CLI/plugin repo. If
   the same skill set appears in more than one location (e.g. both
   `.claude/skills/` and `cli/assets/skills/` in the same repo — one is
   usually the packaged/build copy of the other), install from ONE location
   only and skip the duplicate; check file counts/diff if unsure which is
   canonical (usually `.claude/skills/` or the top-level `skills/`).

   **Directory name suffixes vary.** Some collections name their skill
   folders with a `.skill` extension (e.g. `robotics-skills-suite` ships
   `skills/*.skill` — `iso12100-risk-assessment-builder.skill/`). The
   boundary test is still "contains SKILL.md inside", but a trailing
   `.skill` suffix survives copying: when you flatten/copy them into the
   library, decide up front whether to keep the suffix (so the directory
   name stays unique and greppable) or strip it. Keep it if the same skill
   name would collide with an existing library entry.

   **Verify frontmatter `name:` matches directory name.** After copying,
   run `grep -m1 "^name:" <dir>/SKILL.md` for each skill and compare with
   the directory name. Mismatch means Hermes will not resolve the skill
   correctly by name. Fix by editing `SKILL.md` frontmatter `name:` to
   exactly match the target directory name (or rename the directory to
   match). This caught real issues: generic names like `access` or
   `configure` appearing multiple times in a collection (discord, imessage,
   telegram all have `access` + `configure` sub-skills) — they must be
   namespaced (`discord-access`, `discord-configure`, etc.) to avoid
   collision in the flat skill namespace.

   **Not every repo is a skill collection at all.** Some GitHub links the
   user gives you are: (a) a bag of raw system prompts / docs with zero
   `SKILL.md` files (e.g. leaked-prompt archives), or (b) a full application
   or CLI tool (npm/pip package with hooks, a database, a server) that
   happens to ship a `skills/` subfolder as one small piece of a much larger
   system (e.g. a Claude Code memory-compression plugin). Detect this by
   counting `SKILL.md` hits: zero means "not a skill repo" — don't force-fit
   it as a skill; either install as a reference-only skill (bundle the raw
   docs under `assets/` with a new SKILL.md that indexes them, see step 3a)
   or ask the user what they want. When only a subfolder is skills and the
   rest is a running application/service, say clearly that you only
   installed the skill subfolder, not the underlying app/service, and that
   any skill inside it referencing the app's own database/state (e.g. "search
   the app's history") won't work until that app is separately installed and
   configured.

### 3a. When the repo has no SKILL.md at all (reference-only install)

   If the user still wants it "installed" despite zero `SKILL.md` files,
   don't invent skill boundaries that aren't there. Instead: copy the raw
   content into `assets/` under one new class-level skill, then write a
   SKILL.md that indexes what's in there and explains when to load it
   (e.g. "reference library for X, use `search_files`/`read_file` inside
   `assets/<subfolder>/`"). This keeps the material discoverable without
   pretending it's an executable workflow it isn't.

4. **Flag bulk/mega-collections to the user before installing them wholesale.**
   Some repos bundle hundreds of narrow, auto-generated sub-skills (e.g.
   per-API-integration automation skills that all require the same external
   MCP server like Composio/Rube to actually function). Surface the count and
   the runtime dependency and let the user decide whether they want all of it,
   a subset, or none — don't silently dump 800+ entries into the library.

5. **Copy into `/opt/data/skills/<source-repo-name>/`**, preserving each
   skill's own directory (SKILL.md + its scripts/references/templates
   subfolders intact). Hermes auto-registers any directory containing a
   `SKILL.md` — no manual registration step or restart is needed.

6. **Verify by count, not by eyeballing.** Call `skills_list()` before and
   after and diff the counts (or category) to confirm every expected skill
   registered. `skills_list()` output can be large (100K+ chars) for big
   imports — expect it to be paged to a file; read that file/filter by
   category rather than trying to print the whole thing.

7. **Note runtime dependencies explicitly.** A copied skill that requires an
   MCP server, API key, or CLI tool not yet configured will register fine but
   won't actually be usable until that dependency is set up. Say so — don't
   imply the skill is fully functional just because it's installed.

## Pitfall: copying a cloned repo into another repo → embedded git repo (gitlink)

When the destination is itself a git repo (e.g. backing the skill library up
into `hermes-skills-backup`), copying the clone *with its `.git/` directory
intact* turns the target into an embedded repository: `git add` records a
**gitlink** (mode `160000`) instead of the files, and the outer commit only
references the inner repo's HEAD. The outer clone does NOT contain the
contents — `git status` shows the subfolder as one opaque entry and the
files are missing for anyone who clones the backup.

Symptoms: `warning: adding embedded git repository: <path>` + `create mode
160000` lines in the commit output.

Fix (do this before committing):
```bash
git rm --cached robotics/robotics-agent-skills   # drop the gitlink from index
rm -rf robotics/robotics-agent-skills            # remove the embedded copy
cp -r /opt/data/skills/robotics-agent-skills robotics/  # copy WITHOUT .git
find robotics/ -name ".git" -type d -exec rm -rf {} +  # safety sweep
git add robotics/
```
General rule: **never `cp -r` a git clone into a git repo without stripping
its `.git` first** — strip via `rm -rf <copy>/.git`, `find ... -name .git
-exec rm -rf`, or use `git archive` / tar with exclusion. Check the commit
output for `160000` and for the embedded-repo warning; if either appears,
redo the copy.

## Pitfall: duplicate/overlapping skills

Bulk-importing a general-purpose collection (e.g. Anthropic's own
`document-skills` with `docx`/`pdf`/`pptx`/`xlsx`) can create near-duplicates
of skills already in the library under different names/paths. Installing
doesn't harm anything by itself, but flag the overlap to the user — don't
silently leave two skills competing for the same task without saying so.

## Pitfall: new-skill description length limit

`skill_manage(action='create')` enforces a hard 60-character cap on
`description` (one sentence, trigger first, ends with a period) — longer
values are rejected outright, not truncated. This only applies when you are
writing a *new* index/wrapper SKILL.md yourself (e.g. for the reference-only
case in 3a); imported skills that already have their own SKILL.md keep
whatever description they shipped with and are copied as-is, no rewrite
needed. When you do need to write one, draft short first and verify with a
character count before calling create — iterating against the API's
rejection message burns calls.

## Pitfall: npm/pip packages vs. their bundled skills subfolder

If the user asks to also install "the package itself" (not just the skills
folder) from a repo like this, that's a materially bigger ask — it usually
means an npm/pip install, its own hooks/database/MCP server, and often a
separate API key for background processing. Don't do this silently as a
follow-on to a skill-folder install; confirm with the user first (what it
installs, that it's separate from Hermes's own memory/skill system, and any
credential requirement) before running the package installer.
