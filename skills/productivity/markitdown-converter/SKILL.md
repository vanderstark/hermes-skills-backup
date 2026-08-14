---
name: markitdown-converter
description: Convert documents (PDF, DOCX, XLSX, PPT, images) to clean Markdown using Microsoft's MarkItDown. Use when extracting text from office files, PDFs, or images for documentation, data extraction, or archival.
trigger: document extraction, pdf to markdown, docx to markdown, image to text, bulk document conversion
category: productivity
author: Hermes Agent
version: "1.0"
---

# MarkItDown Converter

Convert Office documents, PDFs, and images to **clean Markdown** format using Microsoft's MarkItDown library.

## When to Use

- Extract text from **PDF documents**
- Convert **Word (.docx)** files to Markdown
- Extract tables from **Excel (.xlsx)** to Markdown
- OCR **images (.jpg, .png)** to text
- Batch convert multiple documents
- Archive documents as searchable Markdown
- Extract structured data from scans

## Capabilities

- **PDF** → Markdown (with OCR for scanned PDFs)
- **Word (.docx)** → Markdown (preserves formatting)
- **Excel (.xlsx)** → Markdown tables
- **PowerPoint (.pptx)** → Markdown slides
- **Images** → OCR text extraction
- **Web URLs** → Markdown content
- **Zip archives** → Batch conversion

## Quick Start

```bash
# Install
pip install markitdown

# Convert single file
markitdown document.pdf > output.md
markitdown proposal.docx > proposal.md

# Convert image with OCR
markitdown scan.jpg > text.md

# Batch convert
for file in *.pdf; do markitdown "$file" > "${file%.pdf}.md"; done
```

## Python API

```python
from markitdown import markitdown

# Convert file
md_text = markitdown("document.pdf")
print(md_text)

# Save to file
with open("output.md", "w") as f:
    f.write(markitdown("input.docx"))
```

## Common Use Cases

### 1. Extract TFG Document
```bash
markitdown /opt/data/cache/documents/rencana_kebutuhan_tfg3.docx > tfg3.md
```

### 2. OCR Scanned Image
```bash
markitdown scan_page.jpg > extracted_text.md
```

### 3. Batch Convert Proposals
```bash
for doc in proposals/*.docx; do
  markitdown "$doc" > "md/${doc%.docx}.md"
done
```

### 4. Extract Table from Excel
```bash
markitdown data.xlsx > data_tables.md
```

## Output Quality

- ✅ Preserves formatting (headers, lists, emphasis)
- ✅ Extracts tables as Markdown tables
- ✅ Clean, readable Markdown
- ✅ OCR handles images & scans
- ✅ Removes unnecessary HTML/XML

## Pitfalls

- ⚠️ Large PDFs (1000+ pages) may take time
- ⚠️ Complex table layouts may need manual cleanup
- ⚠️ Requires Python 3.10+
- ⚠️ OCR quality depends on image resolution

## Files

See `/references/` for:
- `markitdown-examples.md` – example outputs
- `batch-conversion.sh` – ready-to-use script

---

**Workflow:**
1. Identify document type (PDF/DOCX/image)
2. Run markitdown conversion
3. Review output Markdown
4. Save to repo or archive

Ready to extract any document! 📄➡️📝
