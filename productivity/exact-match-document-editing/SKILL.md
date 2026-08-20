---
name: exact-match-document-editing
description: "Edit/merge a PDF so it looks exactly like the original."
metadata:
  version: "1.0.0"
---

# Exact-Match Document Editing

When a user provides an existing document (PDF letterhead, quotation, invoice, official form)
and asks you to combine, merge, extend, or otherwise produce a new version that still looks
like "the same" document — do NOT redesign it from scratch with a generic template (fresh
reportlab layout, new color scheme, different fonts/header style). Users reject this
immediately with feedback like "jelek" (ugly/bad), "bukan ini yang saya minta", or an explicit
"buat sama persis seperti berkas" (make it exactly like the file), because a freshly-designed
template never matches the original's exact brand colors, spacing, plainness, or font choices —
even if the new design is objectively "nicer" by generic standards. A plain black-bordered
table with no header fill redesigned as a navy-header table with alternating row colors will
look foreign to the user even though it's more "polished."

## When to use this skill

- User sends 2+ documents/PDFs and asks to combine them into 1 (e.g. "gabungkan jadi 1 tabel/file")
- User says a document you produced doesn't look right / is "jelek" / "beda dari aslinya"
- User explicitly asks for an edited PDF to look "sama persis" / "exactly like" a source file
- Any request to extend, merge, or modify an existing formal document (quotation, invoice,
  certificate, letterhead) where format fidelity to the original matters more than aesthetics

## Correct approach — edit the original PDF in place with PyMuPDF (`fitz`)

Never rebuild from a template. Instead, treat the original PDF as a canvas and surgically
replace only the parts that need to change.

### 1. Probe the original's exact layout before touching anything

```python
import fitz
doc = fitz.open(source_path)
page = doc[0]

# Every text span with its exact position, font, size, color
d = page.get_text('dict')
for block in d['blocks']:
    if 'lines' not in block: continue
    for line in block['lines']:
        for span in line['spans']:
            print(span['bbox'], span['font'], span['size'], span['color'], repr(span['text']))

# Every line/rect drawn (table borders, dividers): position, fill vs stroke, color, width
for dr in page.get_drawings():
    print(dr['rect'], dr.get('fill'), dr.get('color'), dr.get('type'), dr.get('width'))
```

This tells you the REAL table grid coordinates, column boundaries, font family/size, and
border style to replicate. Never eyeball or guess layout for an "exact match" request — read
it out of the PDF's own content stream.

### 2. White-out only the region being replaced

```python
WHITE = (1, 1, 1)
wipe_rect = fitz.Rect(x0, y0, x1, y1)  # covers just the table/section to change
page.draw_rect(wipe_rect, color=WHITE, fill=WHITE)
```

This leaves the letterhead, logos, and every untouched section pixel-perfect — far more
reliable than trying to re-extract and recolor a logo (see pitfall below).

### 3. Redraw using the exact coordinates/fonts/sizes found in step 1

```python
BLACK = (0, 0, 0)
def hline(page, y, x0, x1, width=0.72):
    page.draw_line(fitz.Point(x0, y), fitz.Point(x1, y), color=BLACK, width=width)
def vline(page, x, y0, y1, width=0.72):
    page.draw_line(fitz.Point(x, y0), fitz.Point(x, y1), color=BLACK, width=width)

page.insert_text((x, y), "text", fontname="helv", fontsize=7.92, color=BLACK)
# or for wrapped/multi-line cell content:
page.insert_textbox(fitz.Rect(x0, y0, x1, y1), "text", fontname="helv", fontsize=7.92, color=BLACK)
```

Use PyMuPDF's builtin font aliases (`helv`, `hebo` for bold) unless the original uses a
specific embedded font you can match by name from the span probe in step 1.

If adding table rows (e.g. merging 2 source documents' line items into 1 table), compute row
heights from the original's row spacing (steps found in `get_drawings()`), not an arbitrary
guess — a too-short row height is the most common cause of overlapping text.

**Totals/merged-cell rows often have a DIFFERENT column-line set than item rows** — e.g. an
item row has 5 vertical borders (No | Description | Qty | Price | Total) but the "Total
Include VAT" row below it only draws 3, because Description+Qty+Price are visually merged into
one wide cell for that row. Don't assume every row in a table shares the same vertical-line
positions as the header/item rows. Check `get_drawings()` filtered to that row's specific
y-range (`if row_y0 <= d['rect'].y0 <= row_y1`) before drawing — copying the item-row's line
list onto the totals row is the most common way to get lines in the wrong place (e.g. a stray
line between Qty and Price where the original has none, and a missing line before the Total
column where the original has one).

### 4. Save to a NEW file — never overwrite the source the user sent

```python
doc.save(output_path)
```

### 5. Render and verify before delivering

```python
pix = doc[0].get_pixmap(dpi=150)
pix.save(preview_path)
```
Then check with `vision_analyze` — specifically ask it to confirm no overlapping/garbled text
and that the result visually matches the original's plainness/style rather than looking like a
redesign. Iterate on coordinates if spacing is off; this is fast (seconds per iteration) so
there's no excuse for delivering an unverified result.

**`vision_analyze` is unreliable for precise structural questions** ("is this vertical line
continuous from top to bottom", "how many vertical lines are in this crop") — it frequently
gives confident but contradictory answers across repeated calls on the same crop, or describes
lines/gaps that pixel inspection shows aren't there. Use it for the holistic check (does this
look like the original, is anything obviously garbled/overlapping) but verify precise line/
border positions programmatically instead:
```python
import fitz, numpy as np
pix = page.get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
scale = 300/72
y_px = int(y_pdf_mid * scale)  # a y coordinate through the middle of the row being checked
for x_pdf in candidate_column_boundaries:
    xp = int(x_pdf * scale)
    brightness = img[y_px, max(0,xp-3):xp+4].mean()
    print(x_pdf, "LINE" if brightness < 200 else "empty")
```
Run this same probe against the ORIGINAL pdf at the equivalent row to get the ground-truth
pattern of which boundaries should have lines, then diff against your rebuilt version.

## Pitfalls

- **Don't rebuild with reportlab/a generic template** when the ask is "exact match" — that's
  the #1 way to get "jelek" feedback. Template rebuilding is fine when the user wants a
  *comparison table* or a *new-style* document; it is wrong when they want the original's
  identity preserved.
- **Extracting a logo via `page.get_images()` + manually recombining with its `/SMask` alpha
  channel frequently produces a wrong/inverted alpha** — the logo renders as a solid black box
  instead of transparent. Don't hand-roll base+mask compositing with PIL. Instead render the
  logo region directly from the *page*:
  ```python
  pix = page.get_pixmap(matrix=fitz.Matrix(6,6), clip=logo_rect, alpha=False)
  pix.save(logo_out_path)
  ```
  This uses the PDF renderer's own compositing and comes out clean against white — also less
  code than manual mask handling.
- When a user pushes back with "jelek" / "not what I asked" / "buat sama persis" on a document
  you already delivered, that's the signal to switch approach entirely (redesign → in-place
  edit), not to just tweak colors on the same redesigned template.
- If the source PDF has no extractable text (scan/photo only), this in-place editing approach
  still works for adding new drawn/inserted content, but you can't read existing text via
  `get_text('dict')` — see the `scanned-document-reading` / `ocr-and-documents` skills for
  extracting scan content first.

## Generating the same formal document in both PDF and DOCX

When the user asks for a formal institutional document (TOR, quotation, letter) delivered in
"PDF dan Word" / "PDF and DOCX" — not an exact-match edit of an existing file, but a fresh
document that must look identical in both formats — write two parallel generator scripts
(`reportlab` for PDF, `python-docx` for DOCX) sharing the same content plan rather than trying
to convert one format to the other (LibreOffice/pandoc conversion of a reportlab PDF to DOCX
loses editability; converting a DOCX to PDF via headless LibreOffice is more reliable than the
reverse, but still drifts from a hand-tuned reportlab layout). Structure both scripts around
the same ordered list of sections/tables so a change to one is easy to mirror in the other:

- Match heading text, numbering (I./II./III.), and table columns exactly between the two scripts.
- In `python-docx`, `set_cell_border_none()` (custom XML helper, no built-in) is needed to get
  an information/signature table with invisible borders like reportlab's borderless `Table`.
- Reportlab table header shading = `TableStyle` with `BACKGROUND`; docx equivalent needs a raw
  `w:shd` OXML element inserted into `tcPr` — there's no high-level python-docx API for cell
  shading.
- Render both to preview images (`fitz` for the PDF; for DOCX either convert with
  `libreoffice --headless --convert-to pdf` first or just trust the docx render since python-docx
  output is generally WYSIWYG-safe) and check with `vision_analyze` before delivering, same
  verify-before-send discipline as single-format edits above.

See `references/pdf-docx-dual-generation.md` for a condensed side-by-side of the reportlab vs
python-docx primitives used for this pattern (headings, bullet lists, tables with borders/shading,
signature blocks).

## Related skills

`pdf` (general PDF create/merge/split — use for net-new documents where format fidelity to an
existing file isn't required), `ocr-and-documents` (text extraction, including from scans),
`nano-pdf` (natural-language single-field text edits — fine for simple swaps, but table
restructuring needs this skill's manual approach instead), `docx` (general DOCX creation — use
alongside this skill's dual-generation pattern when a PDF+DOCX pair is requested).
