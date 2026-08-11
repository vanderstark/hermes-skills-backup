#!/usr/bin/env python3
"""
Template: merge N source quotations/invoices (each with its own letterhead
and one line-item) into a SINGLE quotation letter with ONE shared line-item
table (one row per source item, one combined TOTAL row).

Use when the user says "gabungkan jadi 1 file/tabel" about 2+ quotation PDFs
and clarifies "bukan perbandingan, tapi penawaran" (not a comparison, an
offer) — i.e. they want it to still read as ONE coherent quotation letter,
not a spec-by-spec comparison grid.

Steps:
1. Render each source PDF's logo via page.get_pixmap(clip=logo_bbox) — see
   the "Reusing a company logo" section in SKILL.md. Don't reconstruct from
   extract_image() + SMask, it can render as a solid black box.
2. Fill ITEMS below with one dict per source document's line item.
3. Adjust venv: /tmp/pdfenv/bin/pip install reportlab pymupdf (if not present)
   Run with: /tmp/pdfenv/bin/python3 this_script.py
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ---- CONFIGURE THESE ----
LOGO_PATH = "/tmp/logo_clean.png"          # from page.get_pixmap(clip=bbox) crop
LOGO_ASPECT = 201 / 621                     # height/width ratio of the crop
COMPANY_ADDR_HTML = (
    "Jl. Example No. 1, Jakarta<br/>Phone: +62-21-0000000"
)
TO_LINES = [("Kepada Yth.", "Pejabat Pembuat Komitmen"), ("Perusahaan", "Nama Instansi")]
FROM_LINES = [
    ("Dari", "Nama Sales (Account Executive)"),
    ("No. Surat", "PH/XXXX/YYYY/2026"),
    ("Tanggal", "01 Januari 2026"),
    ("Email", "sales@company.co.id"),
]
ITEMS = [
    # (no, description_multiline, qty, harga_satuan, total)
    ("1", "PRODUK A\nSpesifikasi singkat baris demi baris", "1", "Rp 0", "Rp 0"),
    ("2", "PRODUK B\nSpesifikasi singkat baris demi baris", "1", "Rp 0", "Rp 0"),
]
TOTAL_LABEL = "TOTAL (Include VAT 11%)"
TOTAL_VALUE = "Rp 0"
OUTPUT_PATH = "/tmp/merged_quotation.pdf"
# ---- END CONFIG ----

styles = getSampleStyleSheet()
addr_style = ParagraphStyle('addr', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#444444'), leading=11)
title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=14, alignment=TA_CENTER, spaceBefore=8, spaceAfter=14, textColor=colors.HexColor('#1f2f5c'))
label_style = ParagraphStyle('label', parent=styles['Normal'], fontSize=9.5, leading=14)

doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4, topMargin=15*mm, bottomMargin=15*mm, leftMargin=18*mm, rightMargin=18*mm)
elements = []

logo_img = Image(LOGO_PATH, width=55*mm, height=55*mm * LOGO_ASPECT)
addr_para = Paragraph(COMPANY_ADDR_HTML, addr_style)
header_table = Table([[logo_img, addr_para]], colWidths=[95*mm, 79*mm])
header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
elements.append(header_table)

line_table = Table([[""]], colWidths=[174*mm], rowHeights=[1.2])
line_table.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 1.2, colors.HexColor('#1f2f5c'))]))
elements += [Spacer(1, 3*mm), line_table, Spacer(1, 4*mm)]

elements.append(Paragraph("SURAT PENAWARAN HARGA (QUOTATION)", title_style))

info_rows = [[k, ":", v] for k, v in TO_LINES] + [["", "", ""]] + [[k, ":", v] for k, v in FROM_LINES]
info_table = Table(info_rows, colWidths=[32*mm, 5*mm, 137*mm])
info_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 9.5), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
]))
elements += [info_table, Spacer(1, 6*mm),
             Paragraph("Dengan hormat, bersama ini kami sampaikan penawaran harga sebagai berikut:", label_style),
             Spacer(1, 4*mm)]

data = [["No", "Deskripsi Barang", "Qty", "Harga Satuan", "Total"]] + [list(i) for i in ITEMS] + \
       [["", "", "", TOTAL_LABEL, TOTAL_VALUE]]
table = Table(data, colWidths=[10*mm, 84*mm, 12*mm, 34*mm, 34*mm], repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2f5c')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 9.5),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'), ('ALIGN', (0, 1), (0, -1), 'CENTER'), ('ALIGN', (2, 1), (2, -1), 'CENTER'),
    ('ALIGN', (3, 1), (4, -1), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('FONTSIZE', (0, 1), (-1, -1), 8.5),
    ('GRID', (0, 0), (-1, -2), 0.6, colors.HexColor('#999999')),
    ('LINEABOVE', (0, -1), (-1, -1), 1.2, colors.HexColor('#1f2f5c')), ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.HexColor('#1f2f5c')),
    ('SPAN', (0, -1), (2, -1)), ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'), ('FONTSIZE', (3, -1), (-1, -1), 10.5),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fdeeb3')),
    ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f4f6fa')]),
]))
elements.append(table)

doc.build(elements)
print(f"Saved {OUTPUT_PATH}")
