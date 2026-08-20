# Mermaid Rendering — Pitfall Patterns & Diagnostics

Session-proven error patterns from e-HANJAR AKPOL topology work (2026-08).

## How to Diagnose a Failed Render

1. Navigate to the diagram HTML via `browser_navigate` (file://).
2. Wait 3–4s for Mermaid to finish (snapshot shows only text until then).
3. Run in `browser_console`:
   ```javascript
   const el = document.querySelector('.mermaid');
   const svg = el?.querySelector('svg');
   JSON.stringify({
     hasSvg: !!svg,
     hasError: el?.textContent.includes('Syntax error'),
     viewBox: svg?.getAttribute('viewBox'),
     style: svg?.getAttribute('style'),
     rect: svg ? (() => { const r = svg.getBoundingClientRect(); return {w:r.width,h:r.height,top:r.top,left:r.left}; })() : null
   })
   ```
   - `hasSvg: true` + `hasError: false` → render OK.
   - `hasSvg: true` but tiny `viewBox` like `0 0 2412 512` + `max-width:512px` → **error stub** — the diagram FAILED and Mermaid drew the error box.
   - `hasSvg: false` → Mermaid never ran (script not loaded, or page refreshed before render).

## Pitfall Cheat-Sheet

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 1 | `END` as node ID | Parse error line: `END[...]` | Rename: `FIN`, `DONE`, `SELESAI` |
| 2 | Subgraph ID == node ID (`DC` both) | Only one renders, other missing | Prefix subgraph: `DCX`, or node: `DCK` |
| 3 | Same node ID reused across subgraphs | Nodes merge / wrong edges | Globally unique IDs (`R_ACT`, `R_OK`) |
| 4 | Emoji/symbols in node label | Renderer chokes | Keep labels plain; symbols in `-->|SYM|` edge labels |
| 5 | `-- TEXT -->` edge label syntax | Silent fail — SVG missing or error box | Use `-->|TEXT|` pipe syntax exclusively |
| 6 | `securityLevel` strict (e.g. `strict`) | `<br/>` / HTML labels broken | `securityLevel:'loose'` + `htmlLabels:true` |
| 7 | Blurry output | SVG scaled to container width | `flowchart: { useMaxWidth:false }` + viewport width=2800 |

## Real Session Fix Sequence (hard data)

Diagram 2 & 3 of the e-HANJAR AKPOL set failed on first render:

- **Diagram 2** (`flowchart-keamanan`): node named `END` → renamed `FIN` → render OK.
- **Diagram 3** (`algoritma-3layer`): node IDs `A1`/`A2` used twice and also as class targets → renamed to `R_ACT`/`R_OK` → render OK.
- **Diagram 1** (`topologi-fisik`): subgraph `DC` colliding with node `DC` → renamed subgraph `DCX` → render OK.

## Verification Checklist (before delivery)

- [ ] All nodes from the spec appear in the vision-model readback
- [ ] No 'Syntax error' text in node content
- [ ] `useMaxWidth:false` + viewport 2800 → high-res screenshot
- [ ] Light theme white bg — print/Telegram safe
- [ ] Telegram delivery: MEDIA:/path + warn about compression