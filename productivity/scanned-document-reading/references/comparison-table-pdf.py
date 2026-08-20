#!/usr/bin/env python3
"""Worked example: build a single side-by-side comparison PDF from data
extracted (via vision_analyze) out of N scanned documents.

Usage pattern in a session:
  1. Render each source PDF's page(s) to PNG with pymupdf.
  2. vision_analyze() each PNG, asking for full text/spec/price extraction.
  3. Manually map the extracted fields into the `data` matrix below
     (one row per spec, one column per source document).
  4. Run this script with the venv python:
     /tmp/pdfenv/bin/python3 references/comparison-table-pdf.py

Requires: pymupdf + reportlab in a throwaway venv (system python is
externally managed):
  python3 -m venv /tmp/pdfenv
  /tmp/pdfenv/bin/pip install pymupdf reportlab
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=16, alignment=TA_CENTER, spaceAfter=6)
sub_style = ParagraphStyle('sub', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=14)
note_style = ParagraphStyle('note', parent=styles['Normal'], fontSize=8, textColor=colors.grey)

OUTPUT_PATH = "/opt/data/cache/documents/Comparison_Output.pdf"  # write_file-safe root

doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    topMargin=20*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm,
)

elements = [
    Paragraph("Comparison Title Here", title_style),
    Paragraph("Subtitle / context line here", sub_style),
]

# First row = header. First column = spec label. Remaining columns = one per source doc.
data = [
    ["Spesifikasi", "Item A", "Item B"],
    ["Contoh field", "nilai A", "nilai B"],
    ["Harga", "Rp 0", "Rp 0"],  # highlighted row below assumes price is near the end
]

price_row_index = len(data) - 1  # 0-indexed into `data`, adjust to taste

n_cols = len(data[0])
col_width = (170*mm) / n_cols  # fits A4 with the margins above
table = Table(data, colWidths=[col_width]*n_cols, repeatRows=1)

table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#888888')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    # Highlight the price row so it's easy to spot at a glance.
    ('BACKGROUND', (0, price_row_index + 1), (-1, price_row_index + 1), colors.HexColor('#fff2cc')),
    ('FONTNAME', (0, price_row_index + 1), (-1, price_row_index + 1), 'Helvetica-Bold'),
]))

elements.append(table)
elements.append(Spacer(1, 14*mm))
elements.append(Paragraph("Optional footnote / data-source disclaimer here.", note_style))

doc.build(elements)
print(f"PDF built at {OUTPUT_PATH}")
