---
name: markdown-to-pdf-conversion
category: productivity
description: Convert Markdown files to PDF with Unicode support.
---

## markdown-to-pdf-conversion

Use this skill when the user asks to convert Markdown (.md) files to PDF format.

### Method 1: Using Python (fpdf2)

1.  **Install Dependencies (in a virtual environment):**
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install markdown fpdf2
    ```
2.  **Run Conversion Script:**
    *   Use the Python script from `references/md_to_pdf.py` or write directly:
    ```python
    import sys
    from fpdf import FPDF

    def convert_md_to_pdf(md_path, pdf_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        lines = md_content.split('\n')
        pdf = FPDF()
        pdf.add_page()
        try:
            pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
            font_name = "DejaVu"
        except:
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
        convert_md_to_pdf(sys.argv[1], sys.argv[2])
    ```
3.  **Execute:**
    *   `python3 md_to_pdf.py <input.md> <output.pdf>`

### Method 2: Using Pandoc (if available)

```bash
pandoc <input.md> -o <output.pdf>
```

### Pitfalls:
*   **Unicode Characters:** Default `helvetica` font does not support Unicode (bullet points, special characters). Use `DejaVu` or another Unicode-capable font.
*   **File Permissions:** Ensure the script has read access to the input `.md` file and write access to the output directory.
*   **Line Length in Multi-Cell:** Use `w=190` for multi-line cells to avoid "Not enough horizontal space" errors with long lines.

### References:
*   Script: `references/md_to_pdf.py`

