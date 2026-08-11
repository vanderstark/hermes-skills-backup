# reportlab (PDF) vs python-docx (DOCX) — dual generation cheat sheet

Condensed from generating a formal TOR (Term of Reference) document as both PDF and DOCX from
the same content plan. Use when a user asks for the same document "PDF dan Word" / "PDF and
DOCX" — write two scripts, not a converter.

## Setup

```bash
pip install reportlab python-docx
```

## Headings

```python
# reportlab
from reportlab.lib.styles import ParagraphStyle
h1_style = ParagraphStyle('h1', fontSize=12.5, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
E.append(Paragraph("I. LATAR BELAKANG", h1_style))

# python-docx
def add_heading(doc, text, size=12.5, bold=True, space_before=14, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
```

## Justified body paragraphs

```python
# reportlab
body_style = ParagraphStyle('body', fontSize=10, leading=15, alignment=TA_JUSTIFY)
E.append(Paragraph(text, body_style))

# python-docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
run = p.add_run(text)
run.font.size = Pt(10.5)
```

## Bullet lists

```python
# reportlab
from reportlab.platypus import ListFlowable, ListItem
E.append(ListFlowable([ListItem(Paragraph(t, bullet_style)) for t in items],
                       bulletType='bullet', start='-'))

# python-docx — use the built-in "List Bullet" style, no manual bullet chars needed
for it in items:
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(it)
    run.font.size = Pt(10.5)
```

## Tables with header shading + grid borders

```python
# reportlab
table = Table(data, colWidths=[...])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#888888')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f4f4')]),
]))

# python-docx — no high-level cell-shading API, needs raw OXML w:shd element
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

t = doc.add_table(rows=len(data), cols=3)
t.style = 'Table Grid'   # gives the grid borders for free
for j, val in enumerate(header_row):
    cell = t.rows[0].cells[j]
    cell.text = val
    r = cell.paragraphs[0].runs[0]
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), '1a1a1a')
    cell._tc.get_or_add_tcPr().append(shd)
```

## Borderless info/signature tables

```python
# reportlab — TableStyle simply omits GRID/BOX/LINE commands, borders default to none

# python-docx — a plain doc.add_table() DOES draw default borders; must explicitly strip them
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_border_none(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'nil')
        tcBorders.append(el)
    tcPr.append(tcBorders)
# call set_cell_border_none(cell) on every cell in the table
```

## Horizontal rule under a title

```python
# reportlab
from reportlab.platypus import HRFlowable
E.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#1a1a1a')))

# python-docx — paragraph bottom border via OXML, no direct "add a line" API
pPr = paragraph._p.get_or_add_pPr()
pBdr = OxmlElement('w:pBdr')
bottom = OxmlElement('w:bottom')
bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '12')
bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), '1a1a1a')
pBdr.append(bottom)
pPr.append(pBdr)
```

## Page breaks

```python
# reportlab
from reportlab.platypus import PageBreak
E.append(PageBreak())

# python-docx
doc.add_page_break()
```

## Margins

```python
# reportlab — set on SimpleDocTemplate(...)
doc = SimpleDocTemplate(path, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm,
                         leftMargin=22*mm, rightMargin=22*mm)

# python-docx — set on section
from docx.shared import Cm
section = doc.sections[0]
section.top_margin = Cm(2.0); section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.2); section.right_margin = Cm(2.2)
```

## Verification

- PDF: `fitz.open(path)[i].get_pixmap(dpi=120-150)` → save PNG → `vision_analyze`.
- DOCX: either trust python-docx output directly (it's generally WYSIWYG for these primitives)
  or convert with `libreoffice --headless --convert-to pdf <file>.docx` if a pixel-level check
  is needed — this is more reliable than the reverse direction (PDF→DOCX conversion tools tend
  to mangle table structure).
