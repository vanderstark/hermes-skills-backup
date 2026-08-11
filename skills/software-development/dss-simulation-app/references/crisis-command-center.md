# Crisis Command Center (CCC) — Reference

Proyek DSS bencana + perang, lokasi: `/opt/data/deliverables/crisis-command-center`

## Struktur file

```
backend/main.py
backend/api/simulation.py      ← POST /simulate, GET /wars, GET /wars/{id}
backend/models/schemas.py       ← DisasterType enum: earthquake/flood/conflict/maritime/air/combined
backend/models/impact_model.py  ← method per skenario; return (impact_dict, affected, deaths, ...)
backend/services/resource_allocator.py  ← rasio SPHERE/BNPB/TNI + aset militer
backend/services/decision_engine.py     ← aksi per fase, owner, rationale
backend/data/wars.json          ← 45 perang sejarah Indonesia (id, nama, tahun, wilayah, matra, lat/lon, pop, deskripsi)
frontend/index.html, js/, css/
frontend/assets/                ← aset self-host (offline): leaflet/, fontawesome/, tiles/
download-tiles.py               ← unduh tile peta offline per bounding box
Dockerfile, docker-compose.yml, requirements.txt, .env.example, .gitignore, README.md
```

## Offline assets (sudah di-push)

- **Self-host**: Leaflet 1.9.4 (css+js+images) + Font Awesome 6.5.1 (css + webfonts) di `frontend/assets/` — **0 referensi CDN** di index.html.
- **Tile cache**: `frontend/assets/tiles/` — ~12.661 tile (57MB): Indonesia zoom 3–9, Natuna zoom 3–12, Papua zoom 3–10, Jawa & Timor sebagian. Area baru: edit bbox di `download-tiles.py` lalu jalankan.
- Auto-switch online/offline di `js/map.js` (`navigator.onLine` + event listener + `setUrl`).

## DisasterType enum

```
# 26 bencana Indonesia + 5 operasi militer (total 31)
geologis:  earthquake tsunami volcano landslide liquefaction
hidromet:  flood flash_flood drought tornado strong_wind coastal_abrasion extreme_wave
biologi:   disease_outbreak pandemic
kebakaran: forest_fire building_fire settlement_fire
non-alam:  transport_accident tech_failure environmental_pollution toxic_gas construction_failure
sosial:    social_conflict riot terrorism mass_violence demonstration
militer:   conflict maritime air combined
```

Aturan penamaan katalog: 26 jenis bencana nasional (BNPB taxonomy) + 5 operasi.
Tipe generik pakai `severity_scale`; tipe khusus pakai field sendiri
(`earthquake_magnitude`, `tsunami_wave_height_m`, `volcano_vei`,
`fire_area_ha/fire_wind_speed_kmh/fire_fuel_type`).

## Impact model — koefisien helper generik `_generic()`

Return tuple sama persis dengan semua method lain:
`(impact_dict, affected, deaths, injured, displaced, damaged, destroyed, economic_m, severity)`

Koefisien per kategori (death rate, damage_mult, displaced):
- tanah longsor/likuifaksi/gas beracun/terorisme → **high fatality** (0.002–0.003)
- angin kencang/kekeringan/abrasi/demo → **low fatality** (0.0001–0.0003)
- kebakaran permukiman/kerusuhan/konflik sosial → moderate + displaced besar
- pandemi: tambah `mortality_rate_pct` + `healthcare_capacity_stress` ke dict
- forest_fire: severity = `log10(area_ha)/6 × fuel_mult(gambut 1.6 > hutan 1.2) × (1+wind/100)`; smoke radius & korban pernapasan
- tsunami: severity dari tinggi gelombang (≥15m→0.95, 10m→0.80, 5m→0.55, 2m→0.30) × `shore_factor` dari jarak episenter
- volcano: lookup VEI 0–8 (`lava_km, ash_km, death_r, dmg, sev`) × `dist_factor` inverse-square

Catatan jujur untuk user: angka adalah **estimasi rule-based untuk perencanaan** (decision support), bukan klaim presisi; untuk operasi riil kalibrasi dengan data BNPB/BMKG + pakar.

## API Endpoints

| Endpoint | Method | Isi |
|---|---|---|
| `/api/health` | GET | `{"status":"ok"}` |
| `/api/v1/simulate` | POST | SimulateRequest → SimulationResult |
| `/api/v1/wars` | GET | 45 perang sejarah |
| `/api/v1/wars/{id}` | GET | Detail satu perang |

## Presets

| Key | Lokasi | Matra |
|---|---|---|
| `natuna` | 3.8876N, 108.3892E | maritime |
| `papua` | -3.65, 137.63 | conflict |
| `timor` | -9.3, 124.9 | conflict |

## Payload test (sudah terverifikasi)

**Gempa Cianjur M5.6:**
`{"disaster_type":"earthquake","location":"Cianjur","lat":-6.82,"lon":107.14,"population":750000,"area_km2":120,"infrastructure_density":0.7,"earthquake_magnitude":5.6,"earthquake_depth_km":10,"epicenter_distance_km":5}`
→ affected=455250, deaths=93, personel=1666, aksi=6

**Natuna blockade (maritime):**
`{"disaster_type":"maritime","location":"Laut Natuna Utara","lat":3.8876,"lon":108.3892,"population":250000,"area_km2":200,"infrastructure_density":0.2,"maritime_threat_level":0.9,"maritime_operation":"blockade","enemy_naval_units":5,"enemy_capability":"frigate","sea_distance_nm":30,"civilians_at_sea":2000}`
→ affected=120000, KRI=6, patroli=12, selam=2, aksi=11

**Air airstrike:**
`{"disaster_type":"air","location":"Riau","lat":3.59,"lon":98.67,"population":500000,"area_km2":200,"air_threat_level":0.6,"air_operation":"airstrike","enemy_aircraft":10}`
→ affected=256250, fighter=15, SAM=2, radar=6, aksi=10

**Combined Papua Barat:**
`{"disaster_type":"combined","location":"Papua Barat","lat":-1.5,"lon":132,"population":500000,"area_km2":500,"infrastructure_density":0.3,"conflict_intensity":0.7,"conflict_type":"guerrilla","maritime_threat_level":0.6,"maritime_operation":"amphibious","enemy_naval_units":6,"enemy_capability":"frigate","air_threat_level":0.5,"air_operation":"airstrike","enemy_aircraft":8}`
→ alert=TANGGAP DARURAT, affected=449249, deaths=3077, personel=5125, KRI=8, patroli=14, fighter=12, radar=14, SAM=2, aksi=20

## GitHub

CCC final state = **dua repo terpisah** (user rule: satu repo per metode instalasi):

- `vanderstark/crisis-command-center-docker` — Docker Compose. Commit `c485e86` = README ditulis ulang jadi tutorial **100% Docker** (15 bagian, tanpa bab monolith, link silang ke repo monolith hanya di akhir).
- `vanderstark/crisis-command-center-monolith` — Ubuntu 24.04 bare metal: `installer/install.sh` (apt + venv + systemd, bind `0.0.0.0:8000`, user diambil dari `SUDO_USER`), `installer/uninstall.sh`, `installer/crisis-command-center.service`. 40 file, tile cache TIDAK di-push (`.gitignore` `frontend/assets/tiles/*` + `.gitkeep`).
- Repo lama `vanderstark/crisis-command-center` **telah dihapus** (DELETE 204 → re-GET 404) setelah kedua pengganti live & diverifikasi — ikuti urutan ketat ini.

**Akses LAN multi-device**: `docker-compose.yml` (docker) dan `ExecStart` (monolith) bind `0.0.0.0` — bukan `127.0.0.1` — supaya device lain di jaringan posko bisa buka `http://<IP-server>:8000`. Verifikasi dengan `curl` ke IP LAN (`hostname`/`hostname -I`) bukan hanya localhost.

Verifikasi tree: `GET /repos/vanderstark/crisis-command-center-{docker|monolith}/git/trees/main?recursive=1`.
