# Preset Geografis Indonesia — Seeder 44 Wilayah (pola terbukti)

Sesi 2026-08-11: menambah preset seluruh pulau Indonesia ke CCC Laravel
(tabel `presets`). 44 preset baru + 3 lama (natuna/papua/timor) = 47 total,
terbagi: Sumatera/10, Jawa/6, Kalimantan/5, Sulawesi/6, Bali+NTB+NTT/3,
Maluku+Papua/9, Nasional/7.

## Struktur Kolom Tabel `presets`

`id, code, nama, deskripsi, lat, lon, zoom, population, area_km2,
disaster_types (json array), param_overrides (json array), timestamps`

## Pola Seeder (idempotent)

```php
namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Preset;

class PresetIndonesiaSeeder extends Seeder
{
    public function run(): void
    {
        $presets = [
            // ═══ PULAU SUMATERA (10) ═══
            ['code' => 'aceh', 'nama' => 'Aceh', 'deskripsi' => '...',
             'lat' => 4.6951, 'lon' => 96.7494, 'zoom' => 7,
             'population' => 5274871, 'area_km2' => 57956.0,
             'disaster_types' => ['tsunami', 'earthquake', 'flood', 'conflict'],
             'param_overrides' => ['tsunami_risk' => 0.95, 'seismic_zone' => 'tinggi']],
            // ... dst 43
        ];

        $inserted = 0;
        foreach ($presets as $p) {
            if (!Preset::where('code', $p['code'])->exists()) {
                Preset::create($p);
                $inserted++;
            }
        }
        echo "Preset baru: {$inserted}, total: " . Preset::count() . "\n";
    }
}
```

## Pitfall & Aturan

1. **Kode `disaster_types` WAJIB valid** — cek dulu
   `DisasterType::all()->pluck('code')` (35 kode: earthquake, tsunami,
   volcano, landslide, liquefaction, flood, flash_flood, drought, tornado,
   strong_wind, coastal_abrasion, extreme_wave, disease_outbreak, pandemic,
   forest_fire, building_fire, settlement_fire, transport_accident,
   tech_failure, environmental_pollution, toxic_gas, construction_failure,
   social_conflict, riot, terrorism, mass_violence, demonstration, conflict,
   maritime, air, combined, cyber_attack, disinformation,
   public_trust_crisis, national_security). Kode typo → silent kosong di
   analisis, TIDAK ada error.
2. **`param_overrides`** pakai nilai khas wilayah: megathrust_risk 0.95
   (Sumbar), merapi_status 'siaga' (Jateng/Yogyakarta), palu_koro_fault 0.92
   (Sulteng), karhutla_risk 0.92-0.95 (Riau/Kalbar), perbatasan_png true
   (Papua), ikn_area true (Kaltim), pandemic_scale 'nasional' (Nasional).
   Boolean flag = `true` (bukan string "true") — JSON cast ke array.
3. **Deskripsi kontekstual** — sertakan rujukan bencana sejarah (tsunami
   2004 Aceh, tsunami Selat Sunda 2018, gempa Palu 2018) agar briefing
   kaya konteks.
4. **Koordinat ibu kota provinsi** + zoom 7-11 (kota besar zoom 11, provinsi
   zoom 7, nasional zoom 5).
5. Daftarkan di `DatabaseSeeder::run()` via `$this->call([...])` — urutan
   setelah RoleAndPresetSeeder aman karena guard `exists()`.

## Verifikasi

```bash
php artisan db:seed --class=PresetIndonesiaSeeder --force
php artisan tinker --execute='
foreach (App\Models\Preset::orderBy("code")->get() as $p) {
    echo "{$p->code} | {$p->nama}\n";
}
echo "TOTAL: " . App\Models\Preset::count() . "\n";'
```

Sync ke repo: `rm -rf repo/app; cp -r app-core repo/app` (kedua varian),
commit + push (lihat pitfall #24 pola token), INGATKAN revoke token.
