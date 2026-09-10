#!/usr/bin/env python3
"""
Markdown to PDF Converter with Unicode Support

Converts a .md file to a simple PDF using fpdf2.
Handles headings and lists with basic styling.
Uses DejaVu font for Unicode character support.

Usage:
    python3 md_to_pdf.py <input.md> <output.pdf>

Example:
    python3 md_to_pdf.py Kajian_Advan_A10.md Kajian_Advan_A10.pdf
"""

import sys
from fpdf import FPDF


def convert_md_to_pdf(md_path: str, pdf_path: str) -> None:
    """
    Converts a Markdown file to a PDF.

    Args:
        md_path: Path to the input Markdown file.
        pdf_path: Path to save the output PDF file.
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    lines = md_content.split('\n')

    pdf = FPDF()
    pdf.add_page()

    # Try to use a Unicode font, fall back to helvetica if unavailable
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        pdf.add_font("DejaVu", "", font_path)
        font_name = "DejaVu"
    except Exception:
        font_name = "helvetica"

    pdf.set_font(font_name, size=12)

    for line in lines:
        if not line.strip():
            pdf.ln(5)
            continue

        if line.startswith('# '):
            pdf.set_font(font_name, size=16)
            pdf.multi_cell(w=190, h=10, text=line[2:], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font(font_name, size=12)
        elif line.startswith('## '):
            pdf.set_font(font_name, size=14)
            pdf.multi_cell(w=190, h=10, text=line[3:], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font(font_name, size=12)
        elif line.startswith('- ') or line.startswith('* '):
            pdf.multi_cell(w=190, h=8, text="  - " + line[2:].strip(), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.multi_cell(w=190, h=8, text=line.strip(), new_x="LMARGIN", new_y="NEXT")

    pdf.output(pdf_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 md_to_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    convert_md_to_pdf(sys.argv[1], sys.argv[2])
    print(f"✅ PDF saved to: {sys.argv[2]}")