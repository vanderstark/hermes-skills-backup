---
name: scanned-document-reading
description: "Use when a PDF is scan/photo-only with no extractable text."
metadata:
  version: "1.0.0"
---

# Reading Scanned / Image-Only Documents

When a user sends a PDF (or other document) that is actually just an
embedded photo or scan per page — common for phone-photographed
receipts, invoices, quotations, forms, ID cards saved as PDF — normal
text extraction (`pymupdf`'s `page.get_text()`, `pdftotext`, etc.)
returns empty or raw binary/stream garbage, not readable text.

## When to use this skill

Load this whenever a document-reading attempt via the `ocr-and-documents`
or `pdf` skills comes back empty, or when you can tell up front the file
is a scan (e.g. read_file on the raw PDF shows `/Filter /DCTDecode` /
`/Subtype /Image` XObject streams and no text operators).

## The fast path: render to PNG, hand to vision — skip OCR entirely

Don't reach for marker-pdf (~3-5GB install, OCR pipeline) or
pytesseract just to answer "what does this document say" for a single
document. Render the page(s) to an image with pymupdf and read them
directly with the vision tool — this is instant, needs no OCR model
download, and is more reliable on messy/rotated real-world photos than
OCR text extraction would be anyway:

```python
import fitz  # pymupdf; `pip install pymupdf` into a venv if not present
             # (the system Python is externally-managed — use
             # `python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install pymupdf`
             # rather than `pip install --system`)

doc = fitz.open("document.pdf")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)  # 150dpi is plenty for vision_analyze
    pix.save(f"/tmp/pdf_page_{i+1}.png")
```

Then call `vision_analyze(image_url="/tmp/pdf_page_1.png", question="<what
the user actually wants extracted>")`. Ask a specific question (e.g. "read
all text, specs, prices, and key fields" for a quotation/invoice) rather
than a generic "describe this image" — it produces a structured, complete
transcription instead of a surface-level visual description.

Reserve `ocr-and-documents`'s marker-pdf path for cases that actually need
machine-readable/searchable OCR output at scale (bulk archival, full-text
search indexing) — not one-off "tell me what this says" reads.

## Combining multiple scanned documents into one output

When a user has sent 2+ scanned documents (e.g. two vendor quotations) and
asks to put them "in 1 file" or "jadi 1 berkas", **that phrase is
ambiguous — clarify or infer from context which of these two they mean**:

1. **Literal concatenation** — just staple the pages together into one
   PDF, each document keeping its own layout/table. Quick:
   ```python
   import fitz
   merged = fitz.open()
   for f in files:
       d = fitz.open(f)
       merged.insert_pdf(d)
       d.close()
   merged.save("combined.pdf")
   ```
2. **Structured merge / comparison table** — extract the data fields from
   each document (via vision_analyze) and re-render them as ONE shared
   table/document, one row per spec, one column per source document. This
   is what a user usually means when they say "dalam 1 tabel" (in one
   table) after already seeing a literal-concatenation result and pushing
   back that it's still "2 different tables in different files." Don't
   assume option 1 satisfies a request that mentions "tabel" — build the
   real comparison table with `reportlab`:
   ```python
   from reportlab.lib import colors
   from reportlab.lib.pagesizes import A4
   from reportlab.lib.units import mm
   from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
   from reportlab.lib.styles import getSampleStyleSheet

   doc = SimpleDocTemplate("out.pdf", pagesize=A4)
   data = [["Spec", "Item A", "Item B"], ["Price", "Rp X", "Rp Y"], ...]
   table = Table(data, repeatRows=1)
   table.setStyle(TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f4e79')),
       ('TEXTCOLOR', (0,0), (-1,0), colors.white),
       ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
       ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f2f2f2')]),
   ]))
   doc.build([table])
   ```
   Install into the same throwaway venv: `/tmp/pdfenv/bin/pip install reportlab`.
   See `references/comparison-table-pdf.py` for a full runnable template
   (side-by-side product/quotation comparison with a highlighted price row) —
   copy it, fill in `data` with the extracted fields, adjust `OUTPUT_PATH`.
3. **Merged quotation/invoice, NOT a comparison** — when the source documents
   are themselves quotations/invoices (each with its own letterhead, "To/From"
   fields, one line-item table), "gabungkan jadi 1 file/tabel" often means
   "recreate ONE quotation letter with both items as two rows in the SAME
   line-item table" — not a spec-by-spec comparison grid (option 2) and not
   two stapled pages (option 1). Tell signal: user says "bukan perbandingan,
   tetapi penawaran" ("not a comparison, but an offer/quotation") after
   seeing option 2. Rebuild the original letterhead structure (company logo,
   To/From block, No. Surat, Tanggal) with a single item table that has one
   row per source document and a combined TOTAL row at the bottom — see
   `references/merged-quotation-pdf.py` for a full template with a real
   company logo pulled from the source PDF (see logo-extraction pitfall below).

## Reusing a company logo from a source PDF in a new document

Do NOT reconstruct a logo from `page.get_images()` + `doc.extract_image()`
+ manually recombining the base image with its `/SMask` — the extracted
soft-mask can come out inverted or with alpha=0 exactly where the logo/text
is, rendering as a solid black box when placed on a white page background,
even though the logo renders fine inside the original PDF. Instead, render
the logo's on-page bounding box directly from the live page (this respects
whatever masking already works correctly for on-page display):

```python
import fitz
doc = fitz.open("source.pdf")
page = doc[0]
# find the logo image's page bbox
for info in page.get_image_info(xrefs=True):
    print(info['xref'], info['bbox'], info['width'], info['height'])
# then crop-render just that rect at high resolution, alpha=False
# (renders it pre-composited onto white — safe to drop into a new white-page PDF)
rect = fitz.Rect(x0, y0, x1, y1)  # from the bbox printed above
pix = page.get_pixmap(matrix=fitz.Matrix(6, 6), clip=rect, alpha=False)
pix.save("logo_clean.png")
```
Use `logo_clean.png` directly in the new document's letterhead (e.g. via
reportlab's `Image(...)`) — no alpha-compositing step needed.

## Pitfalls

- The system Python (`/usr/bin/python3` in a PEP 668 / externally-managed
  environment) refuses `pip install --system`; create a throwaway venv
  first (see code above) rather than fighting the package manager.
- Don't ask vision a vague "describe this image" question for documents —
  it will return a photo-style visual description (colors, layout,
  people) instead of transcribing the actual text/numbers, which is
  usually what the user needs from a quotation, invoice, or form.
- `write_file` is sandboxed to `HERMES_WRITE_SAFE_ROOT` (typically the
  Hermes home, e.g. `/opt/data`) and will refuse paths like `/tmp/foo.py`.
  When generating a helper script to run with a venv interpreter, write it
  under the working dir (e.g. `/opt/data/cache/documents/`) via `write_file`,
  then execute it with the venv's python via `terminal` — `terminal` itself
  can still read/write `/tmp` freely, only the `write_file` tool is scoped.
- "Gabungkan jadi 1 file" (combine into 1 file) is ambiguous between literal
  page concatenation, a restructured comparison table, and a merged
  quotation/invoice with one shared line-item table — if the user clarifies
  after seeing a result that it's still not right, that's a signal to try
  the next interpretation up the ladder (concatenation → comparison table →
  merged quotation), not to just restyle the same interpretation. Ask which
  they mean up front if the request could plausibly be more than one, to
  avoid repeated round-trips.
