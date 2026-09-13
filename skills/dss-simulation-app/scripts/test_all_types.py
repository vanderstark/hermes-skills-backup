#!/usr/bin/env python3
"""Regression loop SEMUA DisasterType terhadap API live DSS.
Jalankan sebelum push:  python3 scripts/test_all_types.py [BASE_URL]
Default BASE_URL=http://127.0.0.1:8131/api/v1/simulate
Exit code 1 jika ada tipe yang gagal (fallback diam-diam terdeteksi via tipe return).
"""
import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8131/api/v1/simulate"

# (disaster_type, extra_params) — nilai mewakili default wajar per tipe
TYPES = [
    ("earthquake", {"earthquake_magnitude": 6.5, "earthquake_depth_km": 20}),
    ("tsunami", {"tsunami_wave_height_m": 5, "tsunami_epicenter_distance_km": 50}),
    ("volcano", {"volcano_vei": 4, "volcano_eruption_distance_km": 10}),
    ("landslide", {"severity_scale": 0.6}),
    ("liquefaction", {"severity_scale": 0.6}),
    ("flood", {"flood_depth_m": 1.5, "flood_duration_hours": 24}),
    ("flash_flood", {"severity_scale": 0.6}),
    ("drought", {"severity_scale": 0.5}),
    ("tornado", {"severity_scale": 0.5}),
    ("strong_wind", {"severity_scale": 0.4}),
    ("coastal_abrasion", {"severity_scale": 0.4}),
    ("extreme_wave", {"severity_scale": 0.5}),
    ("disease_outbreak", {"severity_scale": 0.4}),
    ("pandemic", {"severity_scale": 0.6}),
    ("forest_fire", {"fire_area_ha": 2000, "fire_wind_speed_kmh": 25, "fire_fuel_type": "peat"}),
    ("building_fire", {"severity_scale": 0.4}),
    ("settlement_fire", {"severity_scale": 0.5}),
    ("transport_accident", {"severity_scale": 0.3}),
    ("tech_failure", {"severity_scale": 0.3}),
    ("environmental_pollution", {"severity_scale": 0.4}),
    ("toxic_gas", {"severity_scale": 0.5}),
    ("construction_failure", {"severity_scale": 0.4}),
    ("social_conflict", {"severity_scale": 0.5}),
    ("riot", {"severity_scale": 0.5}),
    ("terrorism", {"severity_scale": 0.6}),
    ("mass_violence", {"severity_scale": 0.5}),
    ("demonstration", {"severity_scale": 0.3}),
    ("conflict", {"conflict_intensity": 0.7, "conflict_type": "insurgency"}),
    ("maritime", {"maritime_threat_level": 0.8, "enemy_naval_units": 5}),
    ("air", {"air_threat_level": 0.7, "enemy_aircraft": 6}),
    ("combined", {"conflict_intensity": 0.6, "maritime_threat_level": 0.5, "air_threat_level": 0.4}),
]

# tipe yang KEBETULAN punya impact["type"] sama dengan tipe lain → skip cek kesamaan
AMBIGUOUS = {"flash_flood", "pandemic", "toxic_gas"}
# peta tipe → impact type yang diharapkan (subset — cukup utk menangkap fallback)
EXPECTED = {
    "earthquake": "gempa_bumi", "tsunami": "tsunami", "volcano": "letusan_gunung_api",
    "landslide": "tanah_longsor", "liquefaction": "likuifaksi", "flood": "flood",
    "flash_flood": "banjir_bandang", "drought": "kekeringan", "tornado": "angin_puting_beliung",
    "strong_wind": "angin_kencang", "coastal_abrasion": "abrasi_pantai",
    "extreme_wave": "gelombang_ekstrem", "disease_outbreak": "wabah_penyakit",
    "pandemic": "pandemi", "forest_fire": "kebakaran_hutan_lahan",
    "building_fire": "kebakaran_gedung", "settlement_fire": "kebakaran_permukiman",
    "transport_accident": "kecelakaan_transportasi", "tech_failure": "kegagalan_teknologi",
    "environmental_pollution": "pencemaran_lingkungan", "toxic_gas": "gas_beracun",
    "construction_failure": "kegagalan_konstruksi", "social_conflict": "konflik_sosial",
    "riot": "kerusuhan", "terrorism": "terorisme", "mass_violence": "aksi_kekerasan_massal",
    "demonstration": "demo", "conflict": "konflik", "maritime": "perang_laut",
    "air": "perang_udara", "combined": "operasi_gabungan",
}


def main():
    ok = fail = 0
    for t, extra in TYPES:
        payload = {
            "disaster_type": t, "location": "Kota Semarang",
            "population": 500000, "area_km2": 50, "area_type": "suburb",
            "infrastructure_density": 0.5, **extra,
        }
        req = urllib.request.Request(
            BASE, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode())
                itype = d.get("impact", {}).get("type", "?")
                # fallback diam-diam: tipe return tidak sesuai tipe yang diminta
                if t not in AMBIGUOUS and EXPECTED.get(t) and itype != EXPECTED[t]:
                    print(f"FAIL {t:22s} -> impact.type={itype!r} (expected {EXPECTED[t]!r}) — dispatch fallback!")
                    fail += 1
                    continue
                print(f"OK   {t:22s} -> {itype:24s} affected={d['affected_population']:>9,} "
                      f"deaths={d['estimated_deaths']:>6,} alert={d['alert_level']}")
                ok += 1
        except Exception as e:
            print(f"ERR  {t:22s} -> {e}")
            fail += 1

    print(f"\n=== TOTAL: {ok} OK, {fail} FAIL ===")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()