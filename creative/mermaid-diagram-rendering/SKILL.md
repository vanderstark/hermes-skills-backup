---
name: mermaid-diagram-rendering
description: "Render crisp Mermaid diagrams as standalone HTML files."
version: 1.0.0
author: Hermes Agent (learned from e-HANJAR AKPOL session)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mermaid, diagrams, flowchart, topology, html, rendering, visualization]
    related_skills: [architecture-diagram, excalidraw]
---

# Mermaid Diagram Rendering — Crisp & Legible

Render Mermaid diagrams as standalone HTML files engineered for **crisp high-DPI output** (Telegram delivery, presentations, print). This skill encodes the hard-won fixes from the e-HANJAR AKPOL topology session.

## When to Use

- User asks for topology / flowchart / architecture / security diagrams
- User complains screenshots are **blurry** ("buram") and asks for **separate images** with better quality
- Diagrams must be embedded in documents, TORs, or presentations where legibility matters

## Key Principles

1. **One diagram per HTML file** — never one page with many stacked diagrams. The browser fragments/screenshots get blurry and hard to capture.
2. **Light theme by default** — white background (`#fff`) + dark text (`#111827`). Dark themes look cool but render muddy in Telegram compression and print badly.
3. **Large fonts** — set `fontSize: 22px` in `themeVariables` + `font-size:22px` CSS on `.mermaid`. Small fonts blur at screenshot scale.
4. **`useMaxWidth: false`** in `flowchart` config — prevents Mermaid from shrinking the SVG to container width (the #1 cause of blurry output).
5. **Viewport width hint** — `<meta name="viewport" content="width=2800">` tells the browser to lay out wide, so screenshots capture full resolution.

## Mermaid Syntax Pitfalls

These are the exact errors hit in the session — pre-empt them:

1. **Reserved words as node IDs** — `END` breaks Mermaid. Use `FIN`, `DONE`, `SELESAI` instead.
2. **Duplicate node IDs** — `subgraph DC[...]` + a node also named `DC` = collision. Prefix subgraph IDs (`DCX`) or rename nodes (`DCK` for Docker).
3. **Emoji directly in node labels** — risky with some CSP/securityLevel settings. Keep labels plain text.
4. **`-- TEXT -->` vs `-->|TEXT|`** — the pipe syntax `-->|BLOCK|` is the reliable one. The `-- TEXT -->` form can silently fail in some Mermaid versions; if a diagram won't render, switch all edges to pipe labels.
5. **Node IDs reused across subgraphs** — must be globally unique. Rename collisions (`R_ACT`, `R_OK`).
6. **Multi-line labels** — `securityLevel:'loose'` + `htmlLabels:true` needed for `<br/>` labels.

## Proven Template

A complete, verified working template lives at `templates/starter.html` (copy it, replace the diagram source, save as `NN-topic.html`). Use it instead of hand-writing the boilerplate.

## Files in This Skill

- `references/mermaid-pitfalls.md` — detailed error patterns and fixes
- `templates/starter.html` — base template for each diagram
- `scripts/split_diagrams.py` — batch splitter for multi-diagram source

## Recommended Base Template

```html
<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=2800, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  body{margin:0;padding:0;background:#ffffff;font-family:'Segoe UI',system-ui,sans-serif;}
  .mermaid { font-size:22px; text-align:center; }
</style></head><body>
<pre class="mermaid">
YOUR_DIAGRAM
</pre>
<script>
mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose',
  flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'basis', padding: 12 },
  themeVariables: {
    fontSize: '22px',
    fontFamily: 'Segoe UI, system-ui, sans-serif',
    primaryColor: '#e0e7ff',
    primaryTextColor: '#111827',
    primaryBorderColor: '#4f46e5',
    lineColor: '#374151',
    secondaryColor: '#dcfce7',
    tertiaryColor: '#fef3c7'
  }
});
</script>
</body></html>
```

## Rendering Verification Without Local Chromium

When mmdc/Puppeteer/Chromium are unavailable (no system chromium, npm scoped packages blocked):

1. Serve each diagram as its own minimal HTML file (template above).
2. `browser_navigate` to `file:///...` and wait — the snapshot shows only heading text until Mermaid finishes; wait 3–4s.
3. Verify via `browser_console`: check `el.querySelector('svg')` exists AND `textContent` does NOT include 'Syntax error'. A `viewBox` of `0 0 NNNN 512` with `max-width:512px` is the Mermaid error stub — that means failure.
4. Screenshot with `browser_vision` and have the vision model **verify node-by-node** against the checklist. Also check `svg.getBoundingClientRect()` — if `width:0` or `top:0` the element is off-viewport.
5. Telegram delivery: send `MEDIA:/path/to/screenshot.png` — but warn the user that **browser screenshots are compressed by Telegram**; local browser open = native resolution.