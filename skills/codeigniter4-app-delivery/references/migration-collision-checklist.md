# Migration Collision Checklist

Sesuai pitfall #7 dan #8 di `codeigniter4-app-delivery`. Gunakan ini sebagai
checklist otomatis sebelum `git add app/Database/Migrations/`.

## 1. Cek prefix timestamp duplikat

```bash
cd app/Database/Migrations/
ls | sed 's/_.*//' | sort | uniq -d
```

Output kosong = aman. Output berisi prefix → ada migration dengan nomor
urut sama → rename file satu (atau hapus jika memang duplikat fungsional).

## 2. Cek nama class duplikat

```bash
grep -h '^class ' *.php | sort | uniq -d
```

Output kosong = aman. Output berisi → dua file berbeda tapi `class` namanya
sama → spark akan fatal saat memuat semua migration.

## 3. Cek syntax & struktur minimal class

```bash
for f in *.php; do php -l "$f"; done
grep -L 'up\|down' *.php               # file tanpa method up/down
grep -n "constraint' => *[0-9] *[0-9]" *.php   # typo 'constraint' => 10 1
```

## 4. Contoh kasus nyata (Polri LLM Gateway)

- `2026-08-19-000008_CreateAnomalyService.php` dan
  `2026-08-19-000008_CreateTokenUsage.php` — SAMA prefix, tapi class berbeda
  (CreateAnomalyService vs CreateTokenUsage). Di sini aman secara class,
  tapi `grep -h '^class ' *.php | sort | uniq -d` harus kosong.
- `CreateAnomalyService` sempat ada dua file dengan isi class SAMA
  (satu typo `'constraint' => 10 1`) → fatal. Harus hapus duplikat dan
  cek syntax sebelum push.

## 5. One-liner fix-and-verify

Jika ternyata ada duplikat timestamp, rename file kembar:

```bash
mv 2026-08-19-000008_CreateTokenUsage.php \
   2026-08-19-000011_CreateTokenUsage.php
```

Lalu re-run checklist di atas.