# CSRF-Free Testing via Laravel Tinker

**Konteks**: Testing endpoint POST (register, simulasi store, login) di Laravel
tanpa CSRF token (development/smoke-test) — **hanya untuk verifikasi cepat, bukan
produksi**.

## Pola yang terbukti

```bash
# Test register (guest route)
php artisan tinker --execute='
$svc = app(App\Services\SimulationService::class);
$input = ["disaster_type" => "earthquake", "location" => "Kota Semarang",
  "lat" => -6.99, "lon" => 110.42, "population" => 500000,
  "area_km2" => 50, "area_type" => "suburb", "infrastructure_density" => 0.5,
  "severity_scale" => 0.6, "earthquake_magnitude" => 6.8];
$sim = $svc->run($input);
echo "ID: {$sim->id} Alert: {$sim->alert_level} Affected: {$sim->affected_population}\n";
'
```

## Kenapa tinker bukan curl?

- **CSRF middleware** (`VerifyCsrfToken`) melindungi semua POST route non-API.
  Token token sulit diambil via script (perlu session + cookies).
- **Service layer** sudah terisolasi — test langsung service method (`run()`)
  tanpa perlu HTTP layer.
- **Migrasi + seeder** sudah jalan di SQLite; data akun/role sudah terisi.
- **Deterministik & cepat** (tidak perlu server artisan serve jalan).

## Pitfall — PHP `+` operator bukan string concat

Di `routes/web.php`, baris logout: `Auth::logout() + request()->session()->invalidate()`
→ **ERROR** (`+` adalah arithmetic di PHP, bukan `.` concat). Harus pisah statement
atau pakai fungsi/closure terpisah.

```php
// SALAH
Route::post('/logout', fn () => Auth::logout() + request()->session()->invalidate() + redirect('/'))

// BENAR
Route::post('/logout', function (Request $request) {
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect('/');
})
```

Catatan ini ditambah karena sesi 2026-08-12 kena error ini & diselesaikan.