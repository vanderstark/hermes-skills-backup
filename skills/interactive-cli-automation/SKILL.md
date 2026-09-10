---
name: interactive-cli-automation
description: "Drive interactive CLI wizards headlessly via PTY + submit."
metadata:
  hermes:
    tags: [terminal, pty, background-process, cli, wizard, automation]
---

# Driving Interactive CLI Wizards Headlessly

Many setup flows are not flag-driven — they're interactive terminal wizards
(numbered menus, y/n confirmations, secret prompts) that block waiting for
stdin. Examples in this environment: `hermes gateway setup`, `hermes setup`,
`hermes model`, `hermes mcp add` (interactive mode), and most third-party
CLI installers. You cannot pipe answers into these via a single foreground
`terminal()` call — the process blocks on the first prompt and the call
times out or returns nothing useful. Use the background-process + PTY
pattern below instead.

## Procedure

1. **Launch in background with `pty=true`.** Interactive CLIs generally
   require a real terminal (isatty checks, cursor control, prompt_toolkit /
   inquirer-style menus) — without PTY the process may refuse to render
   prompts or hang differently than it does for a human.
   ```
   terminal(command="<interactive-cli-command>", background=true, pty=true, notify_on_complete=true)
   ```
   This returns a `session_id` immediately; the process keeps running.

2. **Poll to see the current prompt.** `process(action="poll", session_id=...)`
   shows an `output_preview` tail — enough to identify which menu/question
   is currently active. For the full transcript so far (needed when the
   preview truncates a long numbered menu), use `process(action="log", ...)`.

3. **Answer with `submit` (adds Enter) or `write` (no Enter).** Use `submit`
   for normal answers (menu number, y/n, free text, a token) — it appends
   the newline the CLI is waiting for. Use `write` only when you need to
   send raw keystrokes without triggering submission (rare).
   ```
   process(action="submit", session_id=..., data="24")   # e.g. picking menu item 24
   process(action="submit", session_id=..., data="")     # empty = accept the default
   ```

4. **Loop poll → read prompt → submit answer** until the process exits.
   Each `submit` advances the wizard by exactly one prompt — don't try to
   batch multiple answers into one `data` string separated by newlines;
   answer one prompt at a time and re-poll to see what appeared next before
   sending the following answer. Wizards commonly redraw the entire menu
   after each answer (full repaint, not just the new question) — read the
   *end* of the latest output, not just search for keywords, to find the
   current active prompt.

5. **Confirm completion.** After the process reports `status: exited`,
   verify the outcome with the tool's own status command (e.g.
   `hermes gateway status`) rather than trusting the wizard's last printed
   line alone — some wizards print a success message before an async step
   (like a service restart) actually finishes.

## Pitfalls

- **Empty-string submit for "leave blank / accept default"** — sending
  `data=""` to `submit` still writes a bare Enter, which is exactly what a
  human pressing Enter on an empty prompt does. Don't overthink it or try
  to skip the step some other way.
- **Don't assume the menu numbering is stable across CLI versions** —
  always poll and read the current numbered list before picking a number;
  don't hardcode "Telegram is always 24" from a past session.
- **A wizard field left blank for "sensitive/optional" reasons (allowlist,
  restricted-access ID, home-channel ID) is a legitimate call when the user
  explicitly defers it** — but say plainly in your response that access is
  currently open/unrestricted until that follow-up happens, so the user
  doesn't forget to close the gap.
- **`notify_on_complete=true` is worth setting even though you're actively
  polling** — if you get pulled into a long back-and-forth clarifying with
  the user between submits, the completion notification catches you up
  without needing a manual poll.
