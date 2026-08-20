---
name: ai-tool-system-prompts
description: Leaked system prompts from 30+ AI tools for prompt research.
license: See assets/LICENSE.md (source repo license)
metadata:
  version: "1.0.0"
  source: https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
---

# AI Tool System Prompts (Reference Library)

This skill is a **reference archive**, not an executable workflow. It bundles the raw system prompts, tool schemas, and internal docs collected/leaked from ~30 commercial and open-source AI coding/agent tools, mirrored from [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools).

## When to use this skill

Load it when the user wants to:
- Study how a specific AI tool (Cursor, Devin, Replit Agent, v0, Windsurf, Lovable, Manus, etc.) structures its system prompt or tool definitions
- Compare prompt-engineering approaches across tools (tone, tool-call format, safety rules, planning style)
- Borrow a proven pattern when designing a new agent, skill, or system prompt
- Research what real production agent prompts look like (not toy examples)

## What's inside (assets/)

Each top-level folder under `assets/` is one tool. Contents vary per tool: full system prompt text, tool-call JSON schemas, sub-agent prompts, or product docs.

```
Amp/                        Anthropic/                 Augment Code/
Cluely/                     CodeBuddy Prompts/          Comet Assistant/
Cursor Prompts/             Devin AI/                   Emergent/
Google/                     Junie/                       Kiro/
Leap.new/                   Lovable/                     Manus Agent Tools & Prompt/
NotionAi/                   Open Source prompts/         Orchids.app/
Perplexity/                 Poke/                         Qoder/
Replit/                     Same.dev/                     Trae/
Traycer AI/                 VSCode Agent/                 Warp.dev/
Windsurf/                   Xcode/                        Z.ai Code/
dia/                        v0 Prompts and Tools/
```

Notable files worth knowing by name:
- `assets/Cursor Prompts/Agent Prompt 2025-09-03.txt` — Cursor's latest known agent system prompt, plus `Agent Tools v1.0.json` for its tool schema.
- `assets/Devin AI/Prompt.txt` — Devin's core agent prompt; `DeepWiki Prompt.txt` for its docs-generation prompt.
- `assets/Manus Agent Tools & Prompt/` — Manus's full agent loop prompt and tool definitions, one of the most detailed in the collection.
- `assets/v0 Prompts and Tools/` — Vercel v0's UI-generation system prompt and tool schemas.
- `assets/Replit/`, `assets/Lovable/`, `assets/Windsurf/` — full-stack app builder agent prompts.
- `assets/Open Source prompts/` — prompts from open-source agent projects (not proprietary tools).

## How to use it

1. `search_files` inside `assets/<Tool Name>/` to find the right file (filenames often carry version/date).
2. `read_file` the prompt directly — most are plain `.txt`, some tool schemas are `.json`.
3. When comparing across tools, grep for a specific pattern (e.g. "never fabricate", "todo list", "parallel tool calls") across `assets/` with `search_files(target='content')` to see how different tools phrase the same constraint.
4. Cite the tool and file name when quoting a pattern back to the user — these are real, dated artifacts, not synthetic examples.

## Caveats

- Some of these prompts are **leaked**, not officially published by the vendor — treat them as historical/research artifacts, not guaranteed-current documentation. Tools update their prompts frequently; a file here may be stale.
- License: the source repo's own `assets/LICENSE.md` governs redistribution — check it before reproducing large verbatim chunks outside of research/reference use.
- This is a static mirror (no auto-update). Re-clone `https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools` and refresh `assets/` if the user wants the latest additions.
