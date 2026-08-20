---
name: codeigniter4-app-delivery
description: Build CI4 app with MySQL/Docker/Adminer, auth & seeders.
---

# CodeIgniter 4 App Delivery — Docker + MySQL + Adminer + Seeder + GitHub

Workflow untuk membangun app CI4 production-ready dalam 1 sesi: scaffold,
auth berbasis DB, migration + seeder, controller/model/view per fitur,
docker-compose (app + MySQL + Adminer), export PDF, README Bahasa Indonesia,
push ke GitHub user.

Sibling dari `laravel-app-delivery` (framework berbeda, workflow & preferensi
user sama). Kalau user minta Laravel, pakai skill itu; kalau CI4, pakai ini.

## Trigger

- "Gunakan framework CI4" / "CodeIgniter 4" untuk app baru atau porting
- App butuh login DB + dashboard manajemen user (CRUD) + MySQL
- User minta docker-compose + panel DB (Adminer)
- Migrasi dari prototipe Flask/Python ke CI4

## Scaffold di Host Terbatas (tanpa root)

`php-intl` sering TIDAK terpasang dan `apt-get install php-intl` gagal
(exit 100, no sudo). JANGAN buang waktu di situ — CI4 tetap bisa di-scaffold:

```bash
composer create-project codeigniter4/appstarter <nama-proyek> \
  --prefer-dist --no-interaction --ignore-platform-reqs
cd <nama-proyek> && composer install --ignore-platform-reqs
cp env .env
```

Catatan:
- Nama paket yang benar `codeigniter4/appstarter` (bukan `app-starter`).
- `--ignore-platform-reqs` (jamak) adalah flag yang benar untuk
  `composer install`; `create-project` menerima keduanya.
- File template env di CI4 bernama `env` (tanpa titik) — harus di-copy ke
  `.env` sebelum konfigurasi DB dibaca.
- Package tambahan juga perlu flag yang sama:
  `composer require dompdf/dompdf --ignore-platform-reqs`

## Struktur App (terbukti)

- **Migrations** `app/Database/Migrations/` — penamaan
  `YYYY_MM_DD_NNNNNN_NamaMigration.php` (underscore, bukan tanda hubung;
  tanda hubung bikin spark tidak mengenali file). Class name harus sama
  dengan bagian setelah timestamp.
- **Models** `app/Models/` — `$table`, `$primaryKey`, `$returnType='array'`,
  `$allowedFields` LENGKAP, `$useTimestamps=false` kalau kolom `created_at`
  diisi manual. Tambahkan method domain (`getByUnit`, `getStatusSummary`,
  `search`, `push`) di model, bukan di controller.
- **Controllers** `app/Controllers/` — `use ResponseTrait;` untuk endpoint
  JSON (`respond`, `fail`, `failUnauthorized`, `failNotFound`). Guard
  session di awal setiap method: `if (! $this->session->get('logged_in'))`.
- **Views** `app/Views/<fitur>/<nama>.php` — buat subdirektori dulu
  (`mkdir -p app/Views/{location,kasus,report,sop}`), CI4 tidak membuatnya.
- **Seeder** `app/Database/Seeds/` — `namespace App\Database\Seeds;`,
  extends `CodeIgniter\Database\Seeder`, akses `$this->db->table(...)->insertBatch([...])`.

## Routes — SATU file saja

**Pitfall utama CI4:** file route tambahan di `app/Config/` (mis.
`AdminRoutes.php`) **TIDAK auto-loaded**. Semua route WAJIB dideklarasikan di
`app/Config/Routes.php`. Kalau sudah terlanjur buat file terpisah, konsolidasi
balik ke Routes.php, jangan biarkan (route diam-diam mati → 404 misterius).

Pola grup auth:
```php
$routes->get('/', 'Auth::login');
$routes->post('login', 'Auth::attemptLogin');
$routes->get('logout', 'Auth::logout');

$routes->group('', ['filter' => 'auth'], function($routes) {
    $routes->get('dashboard', 'PromptController::dashboard');
    // ... route lain
});
```
Route statis harus dideklarasikan SEBELUM route parametrik yang seprefix.

## Docker Stack (app + MySQL + Adminer)

- `docker-compose.yml` di root repo: service `db` (mysql:8.0 + volume
  `db_data`), `adminer` (port `8081:8080`, `ADMINER_DEFAULT_SERVER: db`),
  `app` (build dari Dockerfile, port `8080`).
- `Dockerfile` base `php:8.3-fpm` + `docker-php-ext-install pdo_mysql intl gd mbstring`
  (di container, intl TERSEDIA — masalah intl hanya di host sandbox).
- `.env` CI4: `database.default.hostname = db` (nama service, bukan localhost).

Perintah deploy:
```bash
docker-compose up -d
docker exec -it <app-container> php spark migrate
docker exec -it <app-container> php spark db:seed <NamaSeeder>
```

## Verifikasi Sebelum Commit (WAJIB)

Selalu jalankan syntax check batch atas semua file PHP yang disentuh:
```bash
php -l app/Config/Routes.php && \
php -l app/Controllers/XxxController.php && \
... && echo "ALL_SYNTAX_OK"
```
Atau loop: `for f in app/Controllers/*.php app/Models/*.php; do php -l "$f"; done`

Syntax check ≠ berjalan. Katakan JUJUR ke user: "syntax valid, belum diuji
runtime" — jangan klaim "semua berjalan dengan baik" sebelum migrate + login
+ klik menu di browser. User menghargai kejujuran ini.

## Support Files

- `references/menulis-file-besar.md` — strategi bergantian `write_file` ⇄
  `terminal` heredoc saat salah satu gagal; aturan newline asli di heredoc.
- `references/auto-redact-audit-log.md` — pola Audit Log (tabel + model
  `log()` helper) dan Auto-Redact PII Indonesia (NIK/telepon/email) untuk
  app instansi pemerintah.

## Pitfalls

1. **`write_file` gagal `missing required field 'path'` pada payload besar**
   — terjadi berulang untuk view HTML/PHP panjang. JANGAN retry call yang
   sama (tool loop warning). Ganti jalur: tulis via `terminal` heredoc.
   Sebaliknya, kalau heredoc kena guard, kembali ke `write_file` dengan
   konten dipecah. Detail: `references/menulis-file-besar.md`.
2. **Heredoc dengan `\n` literal di string perintah = syntax error bash** —
   `cat > f.php << \'EOF\'\n<?php\n...` GAGAL ("here-document delimited by
   end-of-file"). Perintah terminal harus berisi NEWLINE ASLI, bukan escape
   `\n`. Tulis command multi-baris apa adanya.
3. **Heredoc yang isinya mengandung `&`** ditolak guard sebagai
   "backgrounding" (false positive) → pakai `write_file` untuk file itu.
4. **`php-intl` hilang di host** — jangan `apt-get` (no sudo, exit 100).
   Pakai `--ignore-platform-reqs`; di container Docker intl terpasang normal.
5. **File env CI4 bernama `env`**, bukan `.env` — `cp env .env` dulu.
6. **Nama migration pakai tanda hubung** → spark tidak mengenali. Pakai
   underscore: `2024_01_03_000001_NamaMigration.php`.
7. **Tabrakan timestamp & nama class antar-migration saat generate batch.**
    Menulis banyak migration sekaligus gampang menghasilkan dua file dengan
    prefix timestamp SAMA (mis. dua-duanya `...-000008_`) atau dua file
    berbeda nama tapi isinya `class` yang identik → PHP fatal
    "Cannot declare class ... already in use" saat spark memuat semuanya.
    Cek sebelum commit, lalu rename/hapus yang kembar:
    ```bash
    cd app/Database/Migrations
    ls | sed 's/_.*//' | sort | uniq -d       # prefix timestamp duplikat
    grep -h '^class ' *.php | sort | uniq -d  # nama class duplikat
    ```
    Jangan campur dua konvensi penamaan (`YYYY_MM_DD_` vs `YYYY-MM-DD-`)
    dalam satu proyek — ikuti format file yang sudah ada.
8. **`write_file` TIDAK mem-validasi PHP** — outputnya berbunyi
    "No linter for .php files"; itu BUKAN tanda file valid. Migration hasil
    generate batch pernah lolos ke repo membawa error nyata seperti
    `'constraint' => 10 1` (spasi, bukan koma/string) dan `];` penutup method
    yang seharusnya `}`. Jalankan
    `for f in app/Database/Migrations/*.php; do php -l "$f"; done`
    sebelum `git add` — bukan cuma untuk controller/model.
9. **File route tambahan di app/Config tidak dimuat** — lihat bagian Routes.
8. **Klaim "tidak ada error, berjalan baik" tanpa runtime test** — user akan
   menanyakan ulang ("berarti aman ya?"). Jawab dengan tabel status:
   apa yang SUDAH diverifikasi (syntax, commit, push) vs apa yang MASIH
   butuh verifikasi di server (migrate, seed, login, klik tiap menu).
9. **Push GitHub**: token user dipakai ulang; INGATKAN revoke di
   github.com/settings/tokens setiap akhir push. Jangan simpan nilai token
   di chat/memory. Pola aman: `printf '%s' 'ghp_X' > /tmp/gh_token_file &&
   chmod 600 ...` → push → `rm -f`.
10. **README wajib berisi tutorial deploy + cara penggunaan per menu**
    (Bahasa Indonesia, langkah demi langkah, akun default, troubleshooting).
    User menilai dari kelengkapan, bukan singkatnya.
11. **User menolak penjelasan 'why' / proses panjang** — berikan HASIL +
    STATUS (✅/❌) + LANJUTKAN. Jangan narasikan proses. Frustrasi user:
    "Jangan bercanda", "Benar Bos, syntax PHP sudah valid". Pola: state the
    thing, the action, the reason, then next step.
12. **Tool error berulang (terminal/write_file)** → langsung berikan perintah
    manual untuk user copy-paste ke terminal fisik. Jangan retry tool yang
    gagal (tool loop warning). Workaround di references/menulis-file-besar.md.
13. **Token GitHub disampaikan user via chat** — jangan simpan di memory.
    Pattern: echo token > /tmp/gh_token_file (chmod 600) → git push → rm -f.
    Dokumentasikan di README bahwa token harus di-revoke setelah push.