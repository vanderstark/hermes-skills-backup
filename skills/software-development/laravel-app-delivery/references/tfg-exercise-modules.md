# TFG Exercise Modules — Implementasi Gap Tactical Floor Game

## Konteks
User upload dokumen TFG (DOCX: `Perancangan_TFG_Lengkap.docx`, `rencana_kebutuhan_tfg.docx`) lalu minta:
1. **Analisa** fitur/menu yang belum ada di CCC Laravel vs dokumen
2. **Implementasi** gap tersebut

Dokumen TFG menentukan **8 menu utama**: Latihan, Peta, Objek, Operasi, Situasi, EXCON, AAR, Sistem — dengan detail spec lengkap (state machine, fog of war, ORBAT, order board, replay, heatmap, video wall/kiosk, 7 satker Blue Cell).

---

## Pola Implementasi Gap TFG

### 1. Gap Analysis → Checklist Tabel
Sebelum kode, **selalu buat tabel gap** (✅/⚠️/❌) dibagikan ke user:
| Menu TFG | Status CCC | Catatan |
|----------|------------|---------|
| Latihan | ❌ | Belum ada session + T+ timer |
| Operasi | ❌ | Belum ada order board |
| EXCON | ❌ | Belum ada inject/fog |
| Replay | ⚠️ | Ada AAR dasar tapi tidak heatmap/replay engine |

User menilai dari tabel itu — **jangan klaim 100% kalau ada ❌**.

### 2. Migration Gabungan (1 file, 11 tabel)
```
2026_08_12_100001_create_tfg_core_tables.php
```

Tabel:
- `exercise_sessions` — state machine: `draft`→`briefing`→`running`→`paused`→`ended`
- `injects` — EXCON queue: kode, title, message, visible_to (satker), t_plus_sec, map_effect
- `fog_of_war` — per-satker layer visibility (enabled boolean)
- `orbat_units` — 7 satker Blue Cell (AI, Reserse, Brimob, Lantas, Sabhara, Binmas, Manajemen Konflik)
- `order_boards` — order/perintah dengan status (draft→dikirim→dibaca→dilaksanakan→selesai)
- `scenario_packages` — versioned package (manifest.json, orbat_*.json, injects.csv, scoring.json)
- `movement_logs` — untuk heatmap (entity_type, lat/lon, t_plus_sec)
- `decision_logs` — keputusan + PIC + waktu
- `roleplay_channels` + `roleplay_messages` — salur komando radio simulasi

### 3. Model Key Patterns

```php
// ExerciseSession - state machine + timer
public const STATUS = ['draft','briefing','running','paused','ended'];
public function canTransition(string $to): bool { ... }
public function tickTimer(): void { ... }

// FogOfWar - tabel non-standard plural
protected $table = 'fog_of_war';

// OrbatUnit - 7 satker hardcoded
public const SATKER = [
  'ai' => 'Analisis Informasi',
  'reserse' => 'Reserse',
  'brimob' => 'Brimob',
  'lantas' => 'Lantas',
  'sabhara' => 'Sabhara',
  'binmas' => 'Binmas',
  'manajemen_konflik' => 'Manajemen Konflik',
];
```

### 4. Controller Auto-Generate Pattern (store method)
```php
public function store(Request $request) {
  $session = ExerciseSession::create([...]);
  
  // Auto-generate 7 satker
  foreach (OrbatUnit::SATKER as $code => $nama) {
    OrbatUnit::create([...]);
  }
  
  // Auto-generate fog of war
  foreach (array_keys(OrbatUnit::SATKER) as $satker) {
    FogOfWar::create([...]);
  }
}
```

### 5. Timer Clamp (T+ display)
```javascript
const t = d.t_plus_detik;
[Math.floor(t/3600), Math.floor(t%3600/60), t%60]
  .map(n => String(n).padStart(2,'0')).join(':');
```

### 6. Views (11 Blade files)
| View | Fungsi |
|------|--------|
| `latihan/index` | Daftar sesi + search |
| `latihan/create` | Form buat sesi + objectives/ROE |
| `latihan/show` | Command center utama: status, timer, ORBAT, order, inject, decision log |
| `latihan/injects` | EXCON inject queue + deliver |
| `latihan/fog` | Fog of war toggle per satker |
| `latihan/decisions` | Log keputusan (form + tabel) |
| `operasi/index` | Order board CRUD |
| `operasi/orbat` | ORBAT board edit kekuatan/status |
| `videowall/show` | Kiosk COP read-only (Leaflet + polling) |
| `replay/show` | Replay player + timeline + heatmap |
| `replay/compare` | Side-by-side 2 sesi |

### 7. Routes (24 routes baru)
Prefix: `latihan/`, `operasi/`, `wall/`, `replay/` — semuanya di dalam grup `auth`.

### 8. Verification Checklist
```bash
# 1. PHP syntax
php -l app/Models/ExerciseSession.php  # all new files

# 2. Migration
php artisan migrate --force

# 3. Functional test via tinker
php artisan tinker --execute='... full scenario test ...'

# 4. Route check
php artisan route:list | grep -c "latihan\|operasi\|wall\|replay"
# harus ≥ 20

# 5. Blade compile
php artisan view:cache
# harus "Blade templates cached successfully" tanpa error
```

---

## Pitfall TFG-Spesifik

1. **Model `$table` fix** — `FogOfWar` (fog_of_war), `DecisionLog` (decision_logs), `OrderBoard` (order_boards) — semua non-standard. Selalu cek via tinker `App\Models\Xxx::count()` setelah migrate.

2. **Controller store() auto-generate** — satker & fog harus dibuat otomatis saat create sesi (user hanya klik "Buat Sesi").

3. **Timer T+** — `tickTimer()` dipanggil via polling AJAX (timer route) + saat show view. Clamp ke `durasi_menit * 60` biar tidak overflow.

4. **Route import** — 4 controller baru (`LatihanController`, `OperasiController`, `VideoWallController`, `ReplayController`) harus di-import di `web.php` sebelum dipakai.

5. **Sidebar nav** — tambahkan 3 dropdown: Latihan, Operasi, Replay (pada `layouts/app.blade.php`).

6. **Replay heatmap** — butuh `leaflet-heat.js` (CDN) + data dari `MovementLog`.

---

## Mapping dokumen TFG → Implementasi

| Dokumen TFG | File CCC |
|-------------|----------|
| 2.1 Latihan → `latihan.index`, `create`, `show` | Controllers + views |
| 2.2 Peta → `maps.blade.php` existing | Sudah ada (Leaflet) |
| 2.3 Objek → `orbat.blade.php`, `orbatUnits` | OperasiController |
| 2.4 Operasi → `operasi.index`, `orbat` | OperasiController |
| 2.5 Situasi → `latihan.show` (inject + decision) | LatihanController |
| 2.6 EXCON → `latihan.injects`, `fog` | LatihanController |
| 2.7 AAR → `replay.show`, `compare` | ReplayController |
| 2.8 Sistem → existing auth + RBAC | Sudah ada |
| 3.1 7 Satker → `OrbatUnit::SATKER` | Model + store auto-gen |
| 3.2 Fog of War → `FogOfWar` model + toggle | Fog view + controller |
| 3.3 Inject Engine → `Inject` model + deliver | Inject view |
| 3.4 Replay/Heatmap → `MovementLog` + Leaflet.heat | Replay view |
| 3.5 Video Wall → `VideoWallController` + polling | videowall/show |

---

## Perintah Deploy Terpadu (setelah implementasi)

```bash
# 1. Copy app-core ke dua repo
for r in ccc-laravel-docker ccc-laravel-monolith; do
  rm -rf $r/app && cp -r ccc-laravel/app-core $r/app
done

# 2. Commit & push docker
cd ccc-laravel-docker
git add -A && git commit -m "feat: TFG gap implementation" && git push

# 3. Commit & push monolith  
cd ccc-laravel-monolith
git add -A && git commit -m "feat: TFG gap implementation" && git push

# 4. Bersihkan token
rm -f /tmp/gh_token_file
```