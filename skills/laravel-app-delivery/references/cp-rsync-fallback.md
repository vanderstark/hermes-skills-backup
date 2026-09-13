# Rsync / cp Fallback for Copying Laravel Source Between Repos

**Konteks**: Saat menyiapkan 2 repo terpisah (monolith + docker) dari kode inti
yang sama (`app-core`), `rsync` sering **tidak terinstal** di sandbox/VPS.

## Solusi terbukti

```bash
# Jika rsync ada (optimal)
rsync -a --exclude=vendor --exclude=node_modules --exclude=.env \
  --exclude=database.sqlite --exclude=storage/logs \
  --exclude=storage/framework/cache --exclude=storage/framework/sessions \
  --exclude=storage/framework/views --exclude=bootstrap/cache \
  "$SRC/" "$DST/app/"

# Fallback universal (tanpa rsync) — WORKED 2026-08-12
cp -r "$SRC" "$DST/app"
# Lalu bersihkan yang tidak perlu
rm -rf "$DST/app/vendor" "$DST/app/node_modules" "$DST/app/.env" "$DST/app/database.sqlite"
rm -rf "$DST/app/storage/logs" "$DST/app/storage/framework/cache" \
       "$DST/app/storage/framework/sessions" "$DST/app/storage/framework/views"
rm -rf "$DST/app/bootstrap/cache"
```

## Kenapa bukan `rsync --exclude` terus

1. `rsync` tidak selalu terinstall (bukan default di minimal Ubuntu/Debian).
2. `cp -r` + `rm -rf` target-specific **lebih cepat di sandbox** (bukan network copy).
3. List exclude eksplisit di `rm` aman karena struktur `app-core` sudah fix.

## Catatan

- Folder `app/` di repo tujuan tidak boleh punya file `.git` (karena `cp -r` tidak
  menyalin `.git` — aman).
- Pastikan `database.sql` sudah di-copy terpisah (file root, bukan di `app/`).

Script lengkap ada di sesi deploy repo terpisah (CCC 2026-08-12).