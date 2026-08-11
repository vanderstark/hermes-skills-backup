---
name: defuddle
description: Extract clean article Markdown from a URL via defuddle CLI.
license: MIT
metadata:
  version: "1.0.0"
  source: https://github.com/kepano/defuddle
  cli_version: "0.19.2"
---

# Defuddle

CLI/library that extracts the main content from web pages, stripping clutter (nav, ads, sidebars, comments, headers/footers) and returning clean HTML or Markdown. Built by the Obsidian team for their Web Clipper; works as a stronger alternative to Mozilla Readability with better footnote/math/code-block handling and richer metadata extraction (including schema.org data).

Installed globally via npm at `~/.npm-global/bin/defuddle` (added to PATH in `~/.bashrc`).

## When to use this skill

Load it when the user wants to:
- Extract the readable article content from a URL, stripping ads/navigation/clutter
- Convert a messy web page into clean Markdown for notes, summaries, or further processing
- Get structured metadata from a page (title, author, published date, site name, schema.org data)
- Do something that would otherwise require `web_extract` but needs more control (JSON output, footnote handling, math/code preservation)

## Usage

```bash
# Parse a URL, output clean Markdown to stdout
defuddle parse "https://example.com/article" --markdown

# Parse and output JSON (content + metadata: title, author, published date, site, etc.)
defuddle parse "https://example.com/article" --json

# Parse from a local HTML file
defuddle parse ./page.html --markdown

# Parse from stdin
curl -s "https://example.com/article" | defuddle parse --markdown

# Save output to a file
defuddle parse "https://example.com/article" --markdown > article.md
```

Run `defuddle parse --help` for the full flag list (there are options for image handling, removing specific elements, and controlling metadata extraction).

## How to use it in Hermes

1. Use `terminal(command="defuddle parse '<url>' --markdown")` to get clean Markdown for a page.
2. For metadata extraction (author, published date, site), use `--json` and parse the result with `execute_code`.
3. Prefer this over raw `web_extract`/`browser_navigate` scraping when the page is cluttered (news sites, blogs with heavy sidebars, sites with cookie banners/ads) and you need just the article body.
4. For pages behind JS rendering that a plain `curl`/fetch can't see, fetch the rendered HTML first (e.g. via `browser_snapshot(full=true)` or a headless fetch) and pipe it into `defuddle parse` via stdin or a temp file instead of fetching the URL directly (defuddle's own URL fetch does a plain HTTP GET, no JS execution).

## Environments supported (for reference, not directly usable from Hermes)

- Browser (`defuddle`, `defuddle/full`) — native DOM, used in browser extensions/web apps
- Node.js (`defuddle/node`) — accepts any DOM Document (linkedom, JSDOM, happy-dom)
- CLI (what Hermes uses) — via `npx defuddle` or the globally installed `defuddle` binary, backed by linkedom
- Cloudflare Worker — powers defuddle.md, the hosted API

## Notes

- Work in progress per upstream README — behavior on edge-case sites may change between versions.
- No network/API key required; runs fully local except for the actual URL fetch.
- If `defuddle` is ever not found, check `~/.npm-global/bin` is on PATH, or reinstall with `npm install -g defuddle` (prefix set via `npm config set prefix ~/.npm-global` since the default global path isn't writable in this environment).
