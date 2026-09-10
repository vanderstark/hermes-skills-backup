# Modul Penilaian (Scoring) & Workflow Multi-Tahap (AAR) di Laravel

Pola terbukti dari implementasi requirement PDF "Rapat Pendirian Lab
Kepemimpinan Digital Polri" ke CCC (app Laravel existing dengan simulation
engine). Dipicu: user upload dokumen requirement (PDF/doc) + minta
"pelajari & implementasikan sesuai dokumen".

## Alur Kerja Requirement → Implementasi (terbukti)

1. **Ekstrak dokumen** (PDF):
   - pymupdf: `python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install pymupdf`
     (sandbox TIDAK punya fitz/pdftotext — jangan coba; install venv dulu).
   - `fitz.open(path)` → loop `page.get_text()`; print `[NO TEXT LAYER]` kalau
     image-only (perlu render + vision_analyze).
2. **Gap analysis**: petakan tiap poin dokumen → status di app (✅ ada /
   ⚠️ partial / ❌ belum). Tampilkan tabel ke user SEBELUM implementasi.
   User menilai kesesuaian dari tabel ini; jangan langsung kode.
3. **Implementasi bertahap per item** (todo list), test tiap item sebelum
   lanjut. Item di sini: 4 skenario baru, scoring service, dashboard, workflow.

## Pola Modul Penilaian (Weighted Scoring)

```php
// app/Services/LeadershipAssessmentService.php
class LeadershipAssessmentService {
    public const BOBOT = ['keputusan'=>25,'kecepatan'=>20,'kolaborasi'=>15,
                          'komunikasi'=>15,'integritas'=>10,'risiko'=>15];
    // hitungDariSimulasi(Simulation $sim, User $user): skor per dimensi
    //   dari karakteristik sim (alert_level, duration_minutes, estimated_deaths,
    //   organization_id) + nilaiManual() untuk assessor.
    // skor_total = rata-rata 6 dimensi; grade: >=90 A, >=80 B, >=70 C, >=60 D, else E
}
```

- Model: `protected $casts = ['detail_penilaian' => 'array']` — WAJIB.
  Tanpa cast, create() dengan array JSON memunculkan warning PHP
  "Array to string conversion in Connection.php" (nilai tersimpan 'Array').
- Tambahkan `$casts` juga di model lain yang punya kolom JSON (`'data' => 'array'`).
- Dashboard KPI: `avg('skor_total') ?? 0` (hindari null), ranking via
  `selectRaw('user_id, COUNT(*) as total, ROUND(AVG(skor_total),1) as rata')
  ->groupBy('user_id')->orderByDesc('rata')`.
- API JSON endpoint: method tambahan di TacticalApiController (pola yang
  sama: query → map ke array ringan → response()->json()).

## Pola Workflow Multi-Tahap (AAR / pipeline)

```php
// app/Models/AarSession.php — 1 tabel generic, kolom 'tahap' enum:
// briefing | simulation | decision | aar | feedback
// create(['user_id'=>auth()->id(), 'simulation_id'=>..., 'tahap'=>$t,
//         'judul'=>..., 'konten'=>..., 'data'=>['ip'=>$request->ip()]])
```

- 1 tabel + kolom tahap (bukan 5 tabel) — cukup untuk timeline + filter.
- Report: controller return `response($md, 200, ['Content-Type'=>'text/markdown'])
  ->header('Content-Disposition','attachment; filename="AAR-Report-...md"')`.
  Testable via tinker: `$resp->getContent()`.
- Route conflict: `/aar/laporan` vs `/aar/laporan/simulasi/{simulation}` —
  urutan deklarasi penting; `{simulation}` route HARUS setelah route statis.
- Navbar dropdown: menu baru di `layouts/app.blade.php` (dropdown terpisah,
  bukan submenu dalam — navbar tak berbenturan).

## Test Cepat (tinker)

```bash
php artisan tinker --execute='
$svc = app(App\Services\LeadershipAssessmentService::class);
$ass = $svc->hitungDariSimulasi(App\Models\Simulation::first(), App\Models\User::first());
echo "total={$ass->skor_total} grade={$ass->grade}\n";
// Controller test: app()->instance("request", $req); $view = $ctrl->dashboard($req);
// baca $view->getData()["kpi"]["total"] — JANGAN getStatusCode() (View tak punya).
'
```

## Pitfall Khusus

1. **PDF tanpa text layer** → bukan bug; render page ke PNG + vision_analyze
   (lihat references/csrf-tinker-testing.md untuk pola venv pymupdf).
2. **JSON cast warning** — lihat atas; gejala `Array to string conversion`.
3. **User kirim token baru via chat** — guard security flag HIGH; tulis ke
   `/tmp/gh_token_file` chmod 600, push, `rm -f`, ingatkan revoke. JANGAN
   simpan nilai token di memory/chat. Jika push kedua setelah token dihapus,
   minta user kirim ulang (jangan tebak/curi dari history).
4. **Dua repo (docker+monolith)**: setelah implementasi di app-core, sync via
   `rm -rf $repo/app && cp -r app-core $repo/app`, commit BERSIH, push
   terpisah. Verifikasi file baru dengan `find`/`ls` path BENAR (struktur
   double-app `repo/app/app/...` vs `repo/app/database/...` membingungkan —
   cek path aktual sebelum klaim "file hilang").
5. **Seeder baru**: tambahkan `namespace Database\Seeders;` — tanpa namespace
   class global bentrok autoload classmap (`Cannot declare class ... already
   in use`); lalu `composer dump-autoload`. `$this->command?->info()` aman
   (nullable).
