# Delivering a Downloadable HTML Diagram via Chat (Telegram/Discord)

When the user asks for a **topology/diagram you rendered as HTML** and wants to
*download* it (rather than just look at it in a browser), and Playwright is NOT
installed in the environment, don't get stuck trying to `pip install playwright`
(big chromium download, often times out in restricted containers).

## Working method

1. Write the self-contained `.html` (inline CSS, no external deps beyond an
   optional Google Fonts link) under the Hermes write-safe root, e.g.
   `/opt/data/build/<name>.html`.
2. Render/verify it with Hermes' **built-in browser** tool:
   - `browser_navigate(url="file:///opt/data/build/<name>.html")` — loads it.
   - `browser_vision(annotate=false)` — confirm layout renders correctly and
     optionally dump a screenshot.
3. **Deliver the file** by including the path in your response:
   ```
   MEDIA:/opt/data/build/<name>.html
   ```
   The platform delivers it as a native file attachment the user can download
   and open in their browser. This is the canonical way to hand off an HTML
   artifact on messaging platforms.

## Notes

- The **HTML file itself is the primary deliverable** — do not generate a PNG
  unless the user explicitly asks for an image. HTML is interactive, scalable,
  and matches "downloadable" exactly.
- Try `pip install playwright` / `chromium` browser install only if the user
  asks for an actual rendered PNG/screenshot; otherwise it's wasted time.
- This pattern generalizes to any HTML artifact (topology, diagrams, doc
  dashboards), not just docker-compose deliverables.