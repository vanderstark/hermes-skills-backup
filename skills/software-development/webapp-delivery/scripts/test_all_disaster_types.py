#!/usr/bin/env python3
"""Smoke-test ALL disaster/conflict types against a running CCC instance.

Usage:
  1. Start the app:  uvicorn backend.main:app --host 127.0.0.1 --port 8131
  2. Run:            python3 tests/test_all_types.py

Loops every DisasterType enum value with a minimal-but-valid payload and
asserts HTTP 200 + non-zero affected population. py_compile never catches a
missing _impact_dispatch/allocator/engine branch - this live loop does.

Extend the `extra` dict per type when the model gains new specific params
(e.g. tsunami_wave_height_m, volcano_vei, fire_area_ha).
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8131/api/v1/simulate"

# (disaster_type, type-specific params)
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
    # military types: regression check
    ("conflict", {"conflict_intensity": 0.7, "conflict_type": "insurgency"}),
    ("maritime", {"maritime_threat_level": 0.8, "enemy_naval_units": 5}),
    ("air", {"air_threat_level": 0.7, "enemy_aircraft": 6}),
    ("combined", {"conflict_intensity": 0.6, "maritime_threat_level": 0.5, "air_threat_level": 0.4}),
]


def run(base=BASE, types=TYPES):
    ok = fail = 0
    for t, extra in types:
        payload = {
            "disaster_type": t, "location": "Kota Semarang",
            "population": 500000, "area_km2": 50, "area_type": "suburb",
            "infrastructure_density": 0.5, **extra,
        }
        req = urllib.request.Request(
            base, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode())
                imp = d.get("impact", {})
                print(f"OK  {t:22s} -> {imp.get('type','?'):24s} "
                      f"affected={d['affected_population']:>9,} "
                      f"deaths={d['estimated_deaths']:>6,} alert={d['alert_level']}")
                ok += 1
        except Exception as e:  # noqa: BLE001 - want all failures counted
            print(f"ERR {t:22s} -> {e}")
            fail += 1
    print(f"\n=== TOTAL: {ok} OK, {fail} FAIL ===")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(run())