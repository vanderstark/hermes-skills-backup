---
name: dss-simulation-app
description: DSS sim apps, scenario modules, GitHub deploy.
---

# Decision-Support Simulation App (DSS)

Workflow untuk membangun & mengembangkan aplikasi simulasi DSS: input parameter → estimasi dampak → alokasi sumber daya → rencana tindakan. Berbasis proyek **Crisis Command Center** (detail di `references/crisis-command-center.md`).

## Arsitektur pattern

- `backend/models/schemas.py` — Pydantic + `Enum` tipe skenario (English snake_case).
- `backend/models/<impact_model>.py` — satu method per skenario; **return tuple selalu**: `(impact_dict, affected, deaths, injured, displaced, damaged, destroyed, economic_m, severity)`.
- `backend/services/<resource_allocator>.py` — rasio/standar (SPHERE, BNPB, TNI) → dict sumber daya.
- `backend/services/<decision_engine>.py` — aksi per fase (resp_t0 → resp_t1 → stabilisasi → pemulihan), masing-masing dengan `priority`, `phase`, `timeframe`, `owner`, `rationale`.
- `backend/api/<router>.py` — endpoint POST /simulate + endpoint data statis (mis. daftar perang).
- `backend/data/*.json` — seed data dibaca saat runtime.
- `frontend/` — `index.html` (section param per skenario, disembunyikan `display:none`), `js/main.js` (payload builder + preset), `js/api.js` (fetch client), `js/ui.js` (render), `js/map.js` (Leaflet).
- Delivery: `Dockerfile`, `docker-compose.yml`, `.env.example` (placeholder saja), `.gitignore`, `README.md` tutorial Bahasa Indonesia.

## CHECKLIST: Menambah Skenario Baru (sumber bug!)

Setiap skenario baru wajib disinkron di **8 lapisan**, urut:

1. `schemas.py`: tambah nilai `DisasterType` enum + field opsional.
2. Impact model: metode baru + **nama variabel return harus persis sama dengan yang di-*unpack* router** (bug umum: rename `dist`→`dist_nm` tapi return masih lama; rename `affected`→`total_affected` tapi return `affected`).
3. Router `_impact_dispatch`: tambah key dispatch — kalau tidak → fallback diam-diam.
4. Resource allocator: branch `if disaster_type in ("x", "combined")` untuk aset militer/sipil.
5. Decision engine: conditional block + parameter baru (misal `combined=False`) — parameter harus ada di signature DAN dipanggil.
6. Schema respons: `_clean_resources()` harus punya SEMUA key yang dikirim, kalau tidak pydantic validation error.
7. Frontend: `<option>` dropdown + blok HTML param + `paramSections{}` + cabang payload builder.
8. `README`: daftar skenario + contoh curl + tabel output.

**Catatan terbukti (CCC 6→31 tipe):** skenario "tanpa formula khusus" cukup satu helper `_generic()` (severity 0–1) — lapisan 4–5 (allocator/decision engine) TIDAK wajib diubah jika file tsb punya branch fallback default; buktikan dengan live API test SEMUA tipe, jangan asumsi.

### Menambah BANYAK skenario sekaligus (pola 26+ tipe)

1. `schemas.py`: tambah **1 field generik** `severity_scale` (0–1) + `duration_hours` untuk semua tipe tanpa param khusus; field khusus (mis. `fire_area_ha`, `volcano_vei`) hanya untuk tipe yang punya formula sendiri.
2. Impact model: satu helper generik dengan koefisien per-tipe —
   `_generic(req, impact_type, severity, cat, base_death_rate, base_injured_rate, damage_mult, displaced_ratio, severity_mult)`
   → return tuple **persis sama** dengan method lain: `(impact_dict, affected, deaths, injured, displaced, damaged, destroyed, economic_m, severity)`. Tipe khusus (tsunami/volcano/forest_fire) tetap method sendiri dengan physics params.
3. Dispatch router: 1 baris per tipe (26+ baris), group dengan komentar kategori (geologis / hidrometeorologi / biologi / kebakaran / non-alam / sosial / militer).
4. Frontend: SEMUA tipe generik map ke **satu** param section `genericParams` (slider severity + durasi); payload builder cukup **satu branch** `['a','b',...].includes(type)` (bukan branch per tipe). Tipe khusus dapat section + branch sendiri.
5. README: tabel per kategori (geologis/hidrometeorologi/biologi/kebakaran/non-alam/sosial/militer) — struktur tabel sama di dua repo, tapi sesuaikan format (docker: tabel, monolith: list padat).

## Pitfall yang sudah terlanjur dihadapi

- **Rename variabel di method impact → return tuple** — penyebab `name 'X' is not defined`. Sinkronkan unpack di router.
- **Duplicate dict key** di return (misal `key` dua kali) — JSON diam-diam pakai yang terakhir.
- **Walrus `:=`** dalam rumus eskalasi — ganti variabel biasa.
- **Indentasi rusak** setelah patch multi-branch — tulis ulang blok penuh bila berubah banyak.
- `checkStatus()` harus hit endpoint nyata (`/api/health`).
- Saat API error: **curl respons mentah dulu** — pesan `detail:` langsung tunjuk akar masalah.
- **Mode gabungan**: bobot darat+laut+udara dihitung terpisah (`escal_land/sea/air`) lalu `max()`; severity & metode skenario tidak boleh sama dengan matra tunggal. Pastikan `combined` masuk ke `DisasterType`, dispatch router, branch allocator, branch decision engine (`combined=True` saat dipanggil), dan payload builder frontend.
- **Sync repo docker → monolith pakai `cp -r`**: ikut menyalin `frontend/assets/tiles/` (12rb+ file / ratusan MB) + `backend/__pycache__` — bersihkan sebelum commit (`rm -rf` tile + `__pycache__`), restore `frontend/assets/tiles/.gitkeep`, cek `du -sh frontend/assets/` (tanpa tile harus ≤ ~2MB).
- **Token PAT via file**, bukan env di command: `printf '%s' "$TOKEN" > /tmp/gh_token_file && chmod 600` → push dengan URL inline `https://x-access-token:${TOKEN}@github.com/<owner>/<repo>.git` → `rm -f /tmp/gh_token_file`. Sebelum push ulang cek dulu remote tidak menyisakan token (`git remote get-url origin`). Jangan simpan nilai token di memori/chat-file permanen.
- **Regression loop SEMUA tipe wajib** (`tests/test_all_types.py`, lihat scripts/): fallback diam-diam di dispatch (tipe tak dikenal → method gempa) hanya ketahuan lewat loop penuh enum, bukan sample 1-2 tipe.

## Offline-ready / contingency mode (jaringan mati)

Untuk lingkungan terbatas (posko, militer, bencana) aplikasi web harus tetap hidup tanpa internet. Pola:

1. **Self-host semua aset CDN**: unduh Leaflet CSS/JS + Font Awesome (css + webfonts .woff2/.ttf) ke `frontend/assets/`, ganti referensi CDN di `index.html` ke path relatif. Verifikasi: `curl -s <host>/assets/...` pulang 200 DAN `grep -c "unpkg\|cdnjs" index.html` = 0.
2. **Tile peta offline**: `download-tiles.py` dengan bounding box area prioritas → tile `{z}/{x}/{y}.png` di `frontend/assets/tiles/`. Loh koordinat tile: `x_min, y_min` dari titik BARAT-UTARA (`deg2num(max_lat, min_lon)`), `x_max, y_max` dari titik TIMUR-SELATAN (`deg2num(min_lat, max_lon)`). **Bug umum: pasangan lat/lon terbalik → range negatif & download nyaris 0.** Batasi total tile per zoom (mis. skip >6000) supaya tidak berjam-jam.
3. Auto-switch online/offline di `map.js`: cek `navigator.onLine` saat init → pilih URL tile lokal vs CDN; listener `window.addEventListener('online'/'offline')` → `tileLayer.setUrl()`; `errorTileUrl` fallback tile rusak.

## Verifikasi wajib sebelum push (baseline disimpan di references)

1. `python3 -m py_compile backend/**/*.py` + `node --check frontend/js/*.js`.
2. Live test `uvicorn backend.main:app --port 812x` background di venv, lalu `curl` health + **loop SEMUA tipe** via `tests/test_all_types.py` (di-repo — menjadi regression suite; commit bareng fitur) + cek JSON (alert, classification, resources, len(actions)).
3. Bandingkan angka baseline di references agar perilaku berubah terdeteksi lintas sesi.

## Deliver ke GitHub (akun vanderstark)

- PAT: export `GH_TOKEN` → remote URL bertoken → push → **segera** strip token dari remote + `unset GH_TOKEN`.
- Branch masih `master`: `git branch -m main` sebelum push pertama.
- Verifikasi: `GET /repos/<owner>/<repo>/git/trees/main?recursive=1`.
- README Bahasa Indonesia lengkap + `.env.example` berisi placeholder (`change_me_...`), tanpa secret asli.
- Satu repo per komponen deliverable; suffix `-docker-compose` untuk yang dual-stack.

## Referensi

| File | Isi |
|---|---|
| `references/crisis-command-center.md` | Layout CCC: endpoints, enums, wars.json, presets, payload test, baseline output |
| `scripts/test_all_types.py` | Regression loop semua DisasterType via API live (jalankan sebelum push; `python3 scripts/test_all_types.py [BASE_URL]`) |