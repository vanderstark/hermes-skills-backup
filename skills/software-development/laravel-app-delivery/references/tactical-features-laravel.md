# Fitur Taktis Laravel — Marker, Zone, Audit Trail, Export, Live Sync, Replay

Pola terbukti (sesi CCC 2026-08): menambah fitur "command center" pada app
Laravel yang sudah ada (simulasi bencana/militer) dengan cepat & tanpa bug.
Semua file di bawah ini di-generate, di-test HTTP 200, lalu di-push ke 2
repo (docker + monolith).

## 1. Migrations — 5 tabel baru (jalankan `php artisan migrate --force`)

```php
// 2026_08_11_100001_create_organizations_table.php
Schema::create('organizations', function (Blueprint $table) {
    $table->id();
    $table->string('code', 20)->unique();
    $table->string('nama', 150);
    $table->enum('jenis', ['polri', 'hankam', 'pemda', 'instansi']);
    $table->text('deskripsi')->nullable();
    $table->timestamps();
});

// 2026_08_11_100002_create_markers_table.php
Schema::create('markers', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
    $table->foreignId('simulation_id')->nullable()->constrained()->cascadeOnDelete();
    $table->enum('type', ['unit', 'incident', 'asset']);
    $table->string('nama', 120);
    $table->string('kategori', 80)->nullable();
    $table->decimal('lat', 10, 7);
    $table->decimal('lon', 10, 7);
    $table->enum('status', ['active', 'standby', 'on_mission'])->default('active');
    $table->json('extra')->nullable();
    $table->timestamps();
});

// 2026_08_11_100003_create_zones_table.php — zona/route/objective (geometry JSON)
Schema::create('zones', function (Blueprint $table) {
    $table->id();
    $table->foreignId('simulation_id')->nullable()->constrained()->cascadeOnDelete();
    $table->foreignId('organization_id')->nullable()->constrained()->nullOnDelete();
    $table->string('nama');
    $table->enum('jenis', ['zona', 'route', 'objective']);
    $table->string('warna')->default('#1f6feb');
    $table->json('geometry'); // array [lat,lon] atau polygon
    $table->text('keterangan')->nullable();
    $table->timestamps();
});

// 2026_08_11_100004_create_audit_logs_table.php
Schema::create('audit_logs', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
    $table->string('action', 100);          // create|update|delete|export|login
    $table->string('entity', 100)->nullable(); // simulation|marker|zone|user
    $table->unsignedBigInteger('entity_id')->nullable();
    $table->json('data')->nullable();
    $table->ipAddress('ip')->nullable();
    $table->string('user_agent')->nullable();
    $table->timestamps();
    $table->index(['entity', 'entity_id']);
});

// 2026_08_11_100005_add_organization_id_to_simulations.php — FK tambahan
Schema::table('simulations', function (Blueprint $table) {
    $table->foreignId('organization_id')->nullable()->after('preset_id')
        ->constrained()->nullOnDelete();
});
```

Catatan: `foreignId(...)->constrained()` perlu nama FK unik — pakai nama
tabel konsisten (organizations, markers, dst). `json` cast di model →
`protected $casts = ['geometry' => 'array', 'data' => 'array', 'extra' => 'array']`.

## 2. Audit Log — pola middleware alternatif (di controller)

Log di controller (bukan model observer — lebih eksplisit & gampang):

```php
\App\Models\AuditLog::create([
    'user_id' => auth()->id(),
    'action' => 'create',                       // create|update|delete
    'entity' => 'simulation',                   // simulation|marker|zone|user
    'entity_id' => $sim->id,
    'data' => ['location' => $sim->location],
    'ip' => request()->ip(),
]);
```

View audit: filter by entity/action/user via `when($request->...)` +
paginate(30). Badge warna per action: create=success, update=info,
delete=danger, export=warning, login=primary.

## 3. Export CSV + Briefing Markdown (ExportService)

```php
public function simulationCsv(iterable $simulations): StreamedResponse
{
    return response()->streamDownload(function () use ($simulations) {
        $out = fopen('php://output', 'w');
        fwrite($out, "\xEF\xBB\xBF"); // BOM UTF-8 agar Excel buka dengan benar
        fputcsv($out, ['ID', 'Tipe', ...]);
        foreach ($simulations as $s) { fputcsv($out, [...$s->field ?? 0]); }
        fclose($out);
    }, 'laporan-' . now()->format('Ymd-His') . '.csv', ['Content-Type' => 'text/csv; charset=UTF-8']);
}
```

- **WAJIB `iterable`** bukan `array` (Collection dari Eloquent).
- **WAJIB `?? 0`** sebelum `number_format()` (PHP 8.3 deprecation).
- Briefing: string Markdown dari model (dampak + alokasi + 4 fase aksi),
  response dengan `Content-Disposition: attachment`.

## 4. API Live Sync + Replay (TacticalApiController)

```php
// GET /api/v1/sync — polling 10 detik dari JS
public function sync() {
    $markers = Marker::where('status','active')->limit(100)->get()->map(fn($m) => [
        'id'=>$m->id,'type'=>$m->type,'nama'=>$m->nama,'lat'=>$m->lat,
        'lon'=>$m->lon,'status'=>$m->status,'updated_at'=>$m->updated_at?->toIso8601String(),
    ]);
    $zones = Zone::limit(50)->get()->map(fn($z) => [
        'id'=>$z->id,'nama'=>$z->nama,'jenis'=>$z->jenis,'warna'=>$z->warna,'geometry'=>$z->geometry,
    ]);
    return response()->json(['markers'=>$markers,'zones'=>$zones,'timestamp'=>now()->toIso8601String()]);
}
// GET /api/v1/replay?at=<ISO> — snapshot historis
// GET /api/v1/timeline — audit logs terurut untuk After Action Review
```

Routes API dalam grup `auth` + prefix `api/v1` (tanpa CSRF middleware —
GET saja, aman). Fallback route `Route::fallback()` HARUS diletakkan
SETELAH group API, bukan sebelum (kalau tidak, API kena redirect).

## 5. Maps view — Live Sync JS + layer toggle

```js
const unitMarkers = L.layerGroup(), incidentMarkers = L.layerGroup(),
      assetMarkers = L.layerGroup(), zonesGroup = L.layerGroup();
// toggle checkbox → map.addLayer/removeLayer per layer group

// Live sync polling
let syncInterval;
document.getElementById('liveSync').addEventListener('change', function() {
    if (this.checked) { fetchSync(); syncInterval = setInterval(fetchSync, 10000); }
    else { clearInterval(syncInterval); }
});
async function fetchSync() {
    const res = await fetch('/api/v1/sync');
    const data = await res.json();
    unitMarkers.clearLayers(); incidentMarkers.clearLayers();
    assetMarkers.clearLayers(); zonesGroup.clearLayers();
    data.markers.forEach(m => { /* L.marker([m.lat,m.lon]).addTo(grp sesuai type) */ });
    data.zones.forEach(z => {
        const latlngs = z.geometry.map(p => [parseFloat(p[0]), parseFloat(p[1])]);
        z.jenis==='route'
            ? L.polyline(latlngs,{color:z.warna,weight:3}).addTo(zonesGroup)
            : L.polygon(latlngs,{color:z.warna,fillOpacity:0.25}).addTo(zonesGroup);
    });
}
```

Indikator live: dot hijau beranimasi (CSS `@keyframes pulse`), text
"Terakhir: HH:MM:SS".

## 6. Menu navbar "Taktis" dropdown

Bootstrap 5: `dropdown-menu dropdown-menu-dark` + item route
(tactical.markers, tactical.zones, tactical.audit, tactical.organizations,
export.csv) + divider. Route name pattern: `tactical.*`.

## 7. Seeder Organisasi (POLRI/HANKAM/PEMDA/BNPB)

```php
// database/seeders/OrganizationSeeder.php — PASTIKAN namespace!
namespace Database\Seeders;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
class OrganizationSeeder extends Seeder {
    public function run(): void { /* DB::table('organizations')->insertOrIgnore([...]) */ }
}
// Jalankan: php artisan db:seed --class=OrganizationSeeder --force
```

## Verification Checklist (terbukti)

```bash
# 1. Syntax semua PHP
find app routes database -name "*.php" | while read f; do php -l "$f"; done
# 2. Route terdaftar
php artisan route:list | grep -E "taktis|export|api/"
# 3. View compile
php artisan view:clear && php artisan tinker --execute='Blade::compileString(file_get_contents("resources/views/tactical/markers.blade.php")); echo "OK";'
# 4. Controller test (jangan getStatusCode pada View)
php artisan tinker --execute='
Auth::login(App\Models\User::first());
$r = app(App\Http\Controllers\MarkerController::class)->index(new Illuminate\Http\Request());
echo $r->getData()["markers"]->count();'
# 5. HTTP penuh: login via curl (CSRF token dari HTML) lalu cek tiap halaman 200
# 6. API sync: curl -b cookies /api/v1/sync → JSON markers+zones
```

Catatan: test HTTP login butuh session cookie; pakai `-c`/`-b` jar curl +
ambil `_token` dari HTML login (`grep -oP 'name="_token" value="\K[^"]+'`).
Password default admin sandbox: `admin123` (Hash::check terbukti).
