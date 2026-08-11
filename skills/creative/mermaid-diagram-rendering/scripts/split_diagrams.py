#!/usr/bin/env python3
"""Split a multi-diagram HTML source into one minimal HTML per diagram.

Verifikasi: dipakai sukses pada session e-HANJAR AKPOL (2026-08) untuk
memisahkan 5 diagram Mermaid menjadi file terpisah berkualitas tinggi.

Usage:
    python3 split_diagrams.py <source.html> [output_dir]

Sumber: file HTML yang berisi beberapa blok <pre class="mermaid"> ... </pre>
dan heading <h2> ... </h2> sebagai judul tiap diagram.
"""
import re
import os
import sys

# Template minimal — light theme, lebar viewport 2800 untuk screenshot tajam
TMPL = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=2800, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  body{{margin:0;padding:0;background:#ffffff;font-family:'Segoe UI',system-ui,sans-serif;}}
  .mermaid {{ font-size:22px; text-align:center; }}
</style></head>
<body>
<pre class="mermaid">
{body}
</pre>
<script>
mermaid.initialize({{
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose',
  flowchart: {{ useMaxWidth: false, htmlLabels: true, curve: 'basis', padding: 12 }},
  themeVariables: {{
    fontSize: '22px',
    fontFamily: 'Segoe UI, system-ui, sans-serif',
    primaryColor: '#e0e7ff',
    primaryTextColor: '#111827',
    primaryBorderColor: '#4f46e5',
    lineColor: '#374151',
    secondaryColor: '#dcfce7',
    tertiaryColor: '#fef3c7'
  }}
}});
</script>
</body></html>"""


def slugify(title: str) -> str:
    """'3. Algoritma Keamanan — 3 Layer' -> '03-algoritma-keamanan-3-layer'"""
    slug = title.strip().split('.')[0].strip().lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug


def main():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(src)
    os.makedirs(out, exist_ok=True)

    data = open(src, encoding="utf-8").read()
    blocks = re.findall(r'<pre class="mermaid">\n(.*?)</pre>', data, re.S)
    titles = re.findall(r'<h2>(.*?)</h2>', data, re.S)
    print(f"Found {len(blocks)} diagrams, {len(titles)} titles")

    for i, (title, body) in enumerate(zip(titles, blocks), 1):
        if i > len(blocks):
            break
        slug = f"{i:02d}-{slugify(title)}.html" if i <= len(titles) else f"{i:02d}-diagram.html"
        path = os.path.join(out, slug)
        with open(path, "w", encoding="utf-8") as f:
            f.write(TMPL.format(body=body.strip()))
        print(f"[{i}] {slug}")


if __name__ == "__main__":
    main()