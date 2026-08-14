#!/usr/bin/env bash
#
# batch_conversion.sh — Batch convert multiple documents to Markdown
# Usage: bash batch_conversion.sh /path/to/docs output_dir
#
set -euo pipefail

SOURCE_DIR="${1:-.}"
OUTPUT_DIR="${2:-./markdown_output}"

mkdir -p "$OUTPUT_DIR"
echo "==> Converting documents from $SOURCE_DIR → $OUTPUT_DIR"

# PDF files
for file in "$SOURCE_DIR"/*.pdf; do
  [[ -f "$file" ]] || continue
  basename="${file##*/}"
  outfile="$OUTPUT_DIR/${basename%.pdf}.md"
  echo "  Converting: $basename"
  markitdown "$file" > "$outfile"
done

# Word documents
for file in "$SOURCE_DIR"/*.docx; do
  [[ -f "$file" ]] || continue
  basename="${file##*/}"
  outfile="$OUTPUT_DIR/${basename%.docx}.md"
  echo "  Converting: $basename"
  markitdown "$file" > "$outfile"
done

# Excel spreadsheets
for file in "$SOURCE_DIR"/*.xlsx; do
  [[ -f "$file" ]] || continue
  basename="${file##*/}"
  outfile="$OUTPUT_DIR/${basename%.xlsx}.md"
  echo "  Converting: $basename"
  markitdown "$file" > "$outfile"
done

# Images (jpg, png)
for file in "$SOURCE_DIR"/{*.jpg,*.jpeg,*.png}; do
  [[ -f "$file" ]] || continue
  basename="${file##*/}"
  outfile="$OUTPUT_DIR/${basename%.*}.md"
  echo "  Converting: $basename (OCR)"
  markitdown "$file" > "$outfile"
done

echo "==> Done! Markdown files saved to $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR"
