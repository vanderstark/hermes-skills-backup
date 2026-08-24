# Menulis File Besar di CI4 Project (write_file vs terminal heredoc)

Session ini berulang kali gagal menulis file view PHP/HTML panjang (>~3K
karakter) lewat `write_file` dengan error:

```
{"error": "write_file: missing required field 'path'. Re-emit the tool call with both 'path' and 'content' set."}
```

Ini BUKAN karena parameter kosong — ini **truncation di sisi model saat
streaming payload besar**: field `content` kepotong di tengah, sehingga JSON
yang sampai ke runtime kehilangan `path` (atau `content` ikut terpotong).
Bila teks di dalamnya mengandung karakter yang memicu parser, hasilnya
malah jadi duplicate-output kosong.

## Strategi bergantian (terbukti di session)

1. **Coba `write_file` dulu** untuk file kecil–sedang (< 3K char). Cepat & aman.
2. **Kalau `write_file` gagal berulang (≥2x) untuk file besar**, BERHENTI
   retry dan beralih ke `terminal` heredoc:
   ```bash
   cat > app/Views/prompt/dashboard.php << 'ENDOFFILE'
   <!DOCTYPE html>
   ...isi lengkap...
   ENDOFFILE
   php -l app/Views/prompt/dashboard.php
   ```
3. **Sebaliknya**, kalau heredoc di-guard (false positive "backgrounding"
   karena isi mengandung `&`, atau error "here-document delimited by
   end-of-file" karena ada `\n` literal di string perintah), kembali ke
   `write_file` dan **pecah jadi beberapa write kecil** (tulis per
   `<section>` / per fungsi, lalu sambung manual).

## Aturan NEWLINE di heredoc (kritis)

Perintah terminal `cat > f <<'EOF'\n<?php\n...` dengan `\n` **escape** GAGAL:
```
warning: here-document at line 3 delimited by end-of-file (wanted 'EOF')
syntax error near unexpected token `('
```
Perintah harus berisi **newline asli** (bukan `\n`). Tulis multiline command
apa adanya di tool call, jangan inject `\n`.

## Deteksi awal sebelum menulis

- File HTML view dengan banyak inline JS + CDN → rawan gagal `write_file`
  besar. Langsung pakai heredoc.
- File PHP controller/model → biasanya < 3K, `write_file` cukup, lalu
  `php -l` verify.
- Selalu `php -l` setelah tulis, baik lewat write_file maupun heredoc.
