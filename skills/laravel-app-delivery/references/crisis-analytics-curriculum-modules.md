# Modul Krisis/Medsos, Analitik AI, Kurikulum (pola terbukti)

Sesi: implementasi sisa poin PDF Lab Kepemimpinan Digital POLRI (komunikasi
krisis + media sosial, dukungan analitik/AI, integrasi kurikulum
Sespimmen/Sespimti). Semua modul offline-first & rule-based (0 API eksternal).

## 1. Modul Komunikasi Krisis + Media Sosial

2 tabel: `media_sosial`, `komunikasi_krisis`.

```php
// Migration media_sosial
Schema::create('media_sosial', function (Blueprint $table) {
    $table->id();
    $table->foreignId('simulation_id')->nullable()->constrained('simulations')->nullOnDelete();
    $table->string('platform');          // X, Facebook, Instagram, TikTok, WA
    $table->string('jenis_konten');      // berita, rumor, hoax, seruan, info_resmi
    $table->string('judul');
    $table->text('konten');
    $table->string('sumber')->nullable();
    $table->string('sentimen')->default('netral'); // positif | netral | negatif
    $table->unsignedInteger('jangkauan')->default(0);
    $table->string('status')->default('aktif'); // aktif | ditangani | hoax_terkonfirmasi
    $table->json('analisis')->nullable();
    $table->timestamps();
});
```

Model WAJIB: `protected $table = 'media_sosial';` (lihat pitfall #20) dan
auto-analisis di booted() (pitfall #22):

```php
protected static function booted(): void
{
    static::creating(function (MediaSosial $model) {
        $analisis = self::analyzeRumor($model->konten);
        $model->analisis = $analisis;
        $model->sentimen = $analisis['sentiment'];
        if ($model->jenis_konten === 'hoax' || $analisis['is_hoax']) {
            $model->status = 'hoax_terkonfirmasi';
        }
    });
}
```

Deteksi hoax/rumor rule-based (offline): daftar keyword hoax
(`hoax, rektif, konspirasi, teori...`), rumor (`dengar, kabar, bocorkan,
viral, gempar`), sentimen negatif (`kematian, bencana, korban, darurat`).
Output array: `is_hoax, is_rumor, sentiment, urgency`.

`komunikasi_krisis` kolom: simulation_id, jenis (siaran_pers |
briefing_media | pernyataan_pimpinan | klarifikasi), judul, isi, audiens,
status (draf | terbit), data JSON. Simpan template siaran pers di model
sebagai konstanta `TEMPLATE` agar UI bisa isi otomatis.

## 2. Analitik AI (rule-based, tanpa API)

`AnalitikAIService` dengan 4 method reusable:

- `ringkasanSituasi(Simulation $sim)` → skor urgensi 0-100 dari: jumlah
  insiden (×5, cap 30), sentimen negatif (×4, cap 20), hoax (×5, cap 15),
  alert_level (merah 15 / kuning 10 / lainnya 5) + baseline 20. Map skor →
  KRITIS ≥70 / TINGGI ≥40 / SEDANG ≥20 / RENDAH. Output juga teks ringkasan
  siap tampil.
- `rekomendasi(Simulation $sim)` → array playbook [prioritas, tindakan,
  alasan]: skor ≥70 → eskalasi + siaran pers; insiden>0 → kerahkan unit;
  sentimen negatif ≥3 → tim krisis 24 jam; hoax>0 → klarifikasi resmi;
  0 unit aktif → siapkan cadangan; kosong → monitoring rutin.
- `prediksiKinerja(int $userId)` → butuh ≥2 assessment; delta skor_total
  pertama→terakhir: >5 Meningkat, <-5 Menurun, else Stabil.
- `dashboardAnalitik()` → agregat: total medsos, breakdown sentimen,
  hoax/rumor count, konten aktif, komunikasi terbit/draf, top platform
  (`groupBy('platform')->map->count()->sortDesc()->take(5)`).

## 3. Integrasi Kurikulum (Sespimmen/Sespimti)

3 tabel: `kurikulum_levels` (nama, tingkat: pertama|menengah|tinggi,
deskripsi, durasi_hari), `kurikulum_mappings` (level_id, tipe_skenario,
kode_skenario, nama_skenario, jam_pelatihan, objektif), `kurikulum_progress`
(user_id, level_id, mapping_id nullable, leadership_assessment_id nullable,
status: belum|berlangsung|selesai, skor, mulai, selesai, catatan).

- Seeder: 3 level (Sespim, Sespimmen, Sespimti) + ~10 mapping skenario
  per tingkat kesulitan (dasar: banjir/gempa; menengah: siber/disinformasi/
  tsunami/teror; tinggi: krisis kepercayaan/agenda nasional/konflik/multi-bencana).
  Gunakan `updateOrInsert` agar idempotent.
- Progress: `mulai` diisi saat status=berlangsung, `selesai` saat
  status=selesai — set di controller saat create/update.
- UI: card per level (jumlah mapping), form catat progress, tabel progress
  dengan filter level+status + update status inline.

### 4. Preset Geografis Indonesia (pustaka skenario per wilayah)

Seed data pulau/provinsi → tabel `presets` (kolom: code, nama, deskripsi,
lat, lon, zoom, population, area_km2, disaster_types array, param_overrides
array). Pola terbukti sesi 2026-08-11: 44 preset baru (34 provinsi + 7
nasional) + 3 lama = 47 total.

- 1 class `PresetIndonesiaSeeder` berisi array `$presets` besar; insert via
  `Preset::create($p)` dengan guard `!Preset::where('code',...)->exists()`
  → **idempotent**, aman dijalankan ulang.
- Kelompokkan per pulau di komentar (Sumatera/10, Jawa/6, Kalimantan/5,
  Sulawesi/6, Bali+NTB+NTT/3, Maluku+Papua/9, Nasional/7) biar gampang cari.
- `disaster_types` WAJIB pakai kode tipe valid dari tabel disaster_types
  (cek dulu: `DisasterType::all()->pluck('code')`) — typo kode → analisis
  diam-diam kosong.
- `param_overrides`: nilai khas wilayah (megathrust_risk 0.95, merapi
  status siaga, perbatasan_png true, karhutla_risk 0.92, dll) — boolean
  flag pakai `true` (JSON cast ke array).
- Daftarkan di `DatabaseSeeder::run()` via `$this->call([...])` setelah
  RoleAndPresetSeeder (3 preset awal) — urutan aman karena guard exists().
- Verifikasi: `Preset::count()` naik + tinker list kode/nama per wilayah.

```php
// Pattern idempotent seed
foreach ($presets as $p) {
    if (!Preset::where('code', $p['code'])->exists()) {
        Preset::create($p);
        $inserted++;
    }
}
```

## Verifikasi (urutkan)

1. `php -l` semua file baru → 0 error
2. `php artisan migrate --force` → tabel baru muncul
3. `php artisan db:seed --class=... --force` → data masuk
4. Tinker: create media sosial → cek `sentimen/status/analisis` terisi
   OTOMATIS (bukti booted() jalan), create progress kurikulum, panggil
   AnalitikAIService → ringkasan + rekomendasi non-kosong
5. `Route::has('krisis.index')` dll → OK; `php artisan route:list` jumlah
   route naik
6. Sync ke repo docker + monolith (`rm -rf app; cp -r app-core app`),
   commit, push pakai token (tulis ke /tmp/gh_token_file, chmod 600,
   hapus setelah push), INGATKAN revoke
