# Disaster / Conflict Decision-Support Domain Model

Empirical formulas + resource ratios used in the Crisis Command Center web app
(repos: `vanderstark/crisis-command-center-docker` / `-monolith`). Reuse for the
app's Phase 2 (ML calibration), for answering "berapa pasukan/bantuan/tindakan"
questions, or for any future Indonesian emergency-management simulator.

---

## Impact estimation

### Earthquake — MMI via attenuation
```
MMI ≈ 3.5 + 0.65·M − 1.6·log10(d + 10) − 0.2·log10(Δ)
```
- M = magnitude (Mw), d = epicenter distance (km), Δ = depth (km)
- Clamp MMI to [2, 12]

Damage tiers (death_rate, injured_rate, damage_pct):

| MMI | death_rate | injured_rate | damage_pct |
|-----|-----------|--------------|-----------|
| ≥9  | 0.008     | 0.05         | 0.45      |
| ≥8  | 0.004     | 0.03         | 0.28      |
| ≥7  | 0.0015    | 0.015        | 0.14      |
| ≥6  | 0.0004    | 0.006        | 0.06      |
| <6  | 0.0001    | 0.002        | 0.02      |

Density modifier: `density_factor = infra_density * 1.2 + 0.4` multiplies both
rates. Affected ratio ≈ `min(1.0, 0.25 + MMI * 0.07)`; displaced = 55% of
affected. Buildings ≈ `(area_km2 / 0.02) * max(infra_density, 0.1)`;
destroyed = 35% of damaged. Economics (USD M) = `(destroyed*120k + damaged*45k)/1e6`.

### Flood — depth-damage curve
```
damage_pct     = min(0.85, 0.10 + 0.15*depth_m + 0.002*min(duration_h, 120))
affected_ratio = min(0.9, 0.2 + 0.1*depth_m + 0.05*min(duration_h//12, 10))
```
Death/injury by depth: <2m → 0.0003/0.004; 2-4m → 0.0015/0.012; ≥4m → 0.004/0.025.
Displaced = 65% affected; destroyed = 25% of damaged.

### Generic disaster (18+ types without unique physics)
All "severity_scale"-driven types (landslide, liquefaction, flash_flood,
drought, tornado, strong_wind, coastal_abrasion, extreme_wave, disease_outbreak,
building_fire, settlement_fire, transport_accident, tech_failure,
environmental_pollution, toxic_gas, construction_failure, social_conflict, riot,
terrorism, mass_violence, demonstration) share one helper:

```
s = clamp(severity_scale, 0, 1) * type_mult        # type_mult 0.6–1.3
affected  = pop * min(0.95, 0.1 + s * 0.6)
deaths    = pop * base_death_rate * (1 + 3s) * density     # base per type
injured   = affected * base_injured_rate * (1 + 2s)
displaced = affected * min(0.8, displaced_ratio + s * 0.3)
damaged   = buildings * min(0.7, 0.03 + s * 0.4) * damage_mult
destroyed = damaged * min(0.45, 0.1 + s * 0.25)
```
Per-type knobs (death_rate, injured_rate, damage_mult, displaced_ratio,
severity_mult): landslide 0.002/0.008/1.2/0.35/1.3 · tornado 0.0008/0.006/1.5/0.3/1.2 ·
liquefaction 0.003/0.012/1.5/0.5/1.3 · flash_flood 0.003/0.015/1.4/0.55/1.3 ·
terrorism 0.003/0.015/1.4/0.5/1.3 · toxic_gas 0.002/0.015/0.4/0.5/1.2 ·
pandemic 0.005/0.02/0.2/0.05/1.2 (+mortality_rate_pct = sev*1.2 or 2.5 when sev>0.7) ·
drought 0.0001/0.001/0.5/0.15/0.8 (+agricultural_loss_pct=sev*0.8) ·
tech_failure 0.0001/0.001/0.8/0.15/0.7 (+service_disruption_pct=sev*0.9) ·
demo 0.0001/0.002/0.4/0.1/0.6.

### Tsunami — wave-height severity
```
wave ≥15m → sev 0.95, death 0.03, inj 0.10, dmg 0.70
wave 10–15 → sev 0.80, death 0.015, inj 0.06, dmg 0.50
wave 5–10  → sev 0.55, death 0.005, inj 0.03, dmg 0.30
wave 2–5   → sev 0.30, death 0.001, inj 0.01, dmg 0.12
wave <2    → sev 0.10, ...
shore_factor = max(0.5, 1.0 − epicenter_dist_km / 500)   # closer → worse
deaths  = affected * death_rate                        # affected = pop*min(0.9, 0.15 + sev*shore*0.5)
displaced = affected * 0.70;  destroyed = damaged * 0.55
```

### Volcano — VEI lookup table (8 levels)
| VEI | lava_km | ash_km | death_rate | dmg | sev |
|-----|---------|--------|-----------|-----|-----|
| 0   | 0.01    | 1      | 0.0001     | 0.05| 0.05|
| 1   | 0.1     | 5      | 0.0003     | 0.08| 0.12|
| 2   | 1       | 20     | 0.001      | 0.15| 0.25|
| 3   | 5       | 100    | 0.003      | 0.28| 0.45|
| 4   | 15      | 300    | 0.008      | 0.40| 0.65|
| 5   | 50      | 1000   | 0.02       | 0.55| 0.80|
| 6   | 100     | 3000   | 0.04       | 0.70| 0.90|
| 7   | 300     | 10000  | 0.08       | 0.85| 0.95|
| 8   | 1000    | 30000  | 0.15       | 0.95| 1.00|

`dist_factor = max(0.2, 1/(1 + (dist_km/ash_km)²))` — inverse-square falloff;
`sev = vd.sev * dist_factor`; deaths = affected × vd.death_rate × dist_factor.

### Forest fire / karhutla — area × fuel × wind
```
fuel_mult: peat 1.6 | forest 1.2 | mineral 0.8 | urban 0.7     # gambut worst
area_sev  = min(1.0, log10(area_ha + 1) / 6)                  # log scale
wind_mult = 1.0 + wind_kmh / 100
sev = min(1.0, area_sev * fuel_mult * wind_mult)
smoke_radius_km = wind_kmh * sev * 2
deaths  = affected * (0.0005 + 0.002 * sev * fuel_mult)       # smoke/HAKI
injured = deaths * 8
economic = (area_ha*5000*fuel_mult + damaged*30k + destroyed*80k + displaced*50)/1e6
```

### Conflict (land) — escalation factor
```
escal = intensity * type_mult
type_mult: urban_warfare 1.8 | guerrilla 1.4 | insurgency 1.3 | riot 0.8
affected  = pop * min(0.95, 0.15 + escal*0.35)
displaced = affected * (0.4 + escal*0.3)
death_rate   = 0.0005 + 0.003*escal   (≈0.05%–1%)
injured_rate = 0.002  + 0.012*escal
damaged  = buildings * min(0.6, 0.05 + escal*0.35)
destroyed = damaged * (0.2 + escal*0.25)
```

### Combined / Tri-Matra (darat + laut + udara) — escalation factor
```
escal_land = threat_land * type_mult        (reuse Conflict formula)
escal_sea  = threat_sea * op_mult * cap_mult * (1 + enemy_ships / 10 * 0.5)
            op_mult:  zee_dispute 1.3 | alki_defense 1.5 | blockade 1.7 | amphibious 2.0
            cap_mult: patrol 0.8 | corvette 1.2 | frigate 1.5 | destroyer 1.8 | carrier_group 2.2
escal_air  = threat_air * op_mult * (1 + enemy_aircraft / 20 * 0.5)
            op_mult:  intrusion 1.4 | air_defense 1.6 | airstrike 2.2 | no_fly_zone 1.8
severity = max(escal_land, escal_sea, escal_air)
```
- Total affected = `pop * (1 - (1-escal_land/10)*(1-escal_sea/10)*(1-escal_air/10))`
  — three independent threat vectors each reduce population by their escalation ratio.
- Resource allocation: sum each sub-matra's military assets in parallel (KRI + fighter
  + marinir + radar + SAM), plus Kogabwilhan coordination layer.
- Decision engine emits cross-matra actions: Kogabwilhan activation, Satgas gabungan,
  operasi tri-matra (laut udara+ darat simultan), then pemulihan gabungan.

### Maritime — naval escalation model
```
op_mult:  zee_dispute 1.3 | alki_defense 1.5 | blockade 1.7 | amphibious 2.0 | piracy 1.0
cap_mult: patrol 0.8 | corvette 1.2 | frigate 1.5 | destroyer 1.8 | carrier_group 2.2
unit_factor = 1 + (enemy_units / 10) * 0.5
escal = threat * op_mult * cap_mult * unit_factor
```
- `threat` = `maritime_threat_level` [0–1]
- `enemy_units` = number of enemy naval vessels
- `shore_factor = max(0.3, 1.0 - dist_nm / 400)` — closer to shore = more damage
- coast_pop = 60% of total population
- affected = coast_pop × min(0.8, 0.15 + escal × 0.35)
- displaced = affected × min(0.9, 0.5 + escal × 0.3)
- death_rate = 0.0002 + 0.0015 × escal
- injured = civilians_at_sea + coast_pop × 0.01 × injured_rate
- ships_affected = max(1, enemy_units × 2 + civilians_at_sea / 100)
- ships_lost = ships_affected × min(0.4, escal × 0.25)
- port_facilities = max(1, area_km2 / 10)
- damaged = port_facilities × min(0.6, escal × 0.5)
- destroyed = damaged × 0.3
- economic = (damaged × 80k + destroyed × 200k + ships_lost × 5M) / 1e6

### Air — aerial escalation model
```
op_mult: intrusion 1.4 | air_defense 1.6 | airstrike 2.2 | no_fly_zone 1.8
unit_factor = 1 + (enemy_aircraft / 20) * 0.5
escal = threat * op_mult * unit_factor
```
- affected = pop × min(0.7, 0.1 + escal × 0.25)
- displaced = affected × (0.3 + escal × 0.2)
- buildings = (area_km2 / 0.05) × max(infra_density, 0.1)
- damaged = buildings × min(0.7, escal × 0.45)
- destroyed = damaged × 0.45
- death_rate = 0.0003 + 0.002 × escal
- air_assets_lost = 1 + enemy_aircraft × 0.2 + escal × 2
- economic = (damaged × 100k + destroyed × 250k + air_assets_lost × 5M) / 1e6

---

## Alert classification
```
deaths>500 or displaced>100k            → KRITIS / TANGGAP DARURAT
deaths>50 or displaced>10k or aff>100k  → TINGGI / SIAGA DARURAT
deaths>10 or displaced>1k               → SEDANG / SIAGA
else                                     → RINGAN / SIAGA AWAL
```

---

## Resource allocation ratios

### SIPIL (SPHERE / BNPB-style)
| Resource             | Ratio                                      |
|----------------------|--------------------------------------------|
| SAR teams            | 1 per 10,000 affected                      |
| Medical teams        | 1 per 10,000 (injured + 2% affected)      |
| Field hospitals      | 1 per 50,000 affected                     |
| Ambulances           | ≥2, 1 per 15,000 (injured + 1% displaced) |
| Command posts        | 1 per 75 km²                              |
| Comms units          | command_posts + 1 per 25,000 population   |
| Water                | 15 L/person/day (SPHERE) × displaced      |
| Food packs           | (displaced + affected) MSS per day        |
| Tents                | 4 persons/tent                            |
| Trucks (5t)          | 1 per 5,000 packs/day                     |
| Buses (50 pax)       | 1 per 250 displaced                       |
| Helicopters          | 1 per 50,000 affected                     |
| Boats (flood only)   | 1 per 2,500 affected                      |
| Field kitchens       | 1 per 5,000 displaced                     |
| Personnel total      | SAR×15 + med×8 + hosp×30 + amb×2 + cmd×12 + comm×2 + kitchen×6 + truck×2 |

### MILITER — Maritime (TNI AL)
| Asset | Ratio |
|-------|-------|
| KRI perang (fregat/korvet) | max(2, ceil(enemy_units × 1.2)) |
| Patroli laut (KAL/BKPK)    | max(3, ceil(enemy_units × 2) + 2) |
| Kapal selam                 | max(1, ceil(enemy_units / 4)) — only if enemy ≥ 4 |
| Batalyon marinir            | max(1, ceil(enemy_units / 2)) — only for amphibious |
| Pangkalan udara laut        | max(1, ceil(affected / 500k)) — only if enemy ≥ 2 |
| Personnel: marinir×600 + KRI×120 + patroli×15 added to civilian total |

### MILITER — Air (TNI AU)
| Asset | Ratio |
|-------|-------|
| Fighter jets (Su-30/F-16)   | max(2, ceil(enemy_aircraft × 1.5)) — 1.5:1 superiority |
| Surveillance aircraft (MPA)  | max(1, ceil(enemy_aircraft / 10)) |
| Attack helicopters           | max(1, ceil(enemy_aircraft / 15)) |
| Ground defense (SAM/AD)      | max(2, ceil(enemy_aircraft / 5)) — only if air_defense_required |
| Radar units                  | max(2, command_posts × 2) |
| Personnel: fighter×15 + surv×20 + radar×8 + AD×6 added to total |

---

## Decision engine — actions by scenario type

### DARAT (earthquake / flood / conflict)
- **resp_t0 (0–2 h)**: activate posko (BPBD/Pemda), mobilize SAR+medical (Basarnas), secure area TNI/Polri (quake/conflict), boat evacuation (flood), declare emergency status if alert ≥ SIAGA DARURAT.
- **resp_t1 (2–24 h)**: field hospital + triage (Kemenkes/PMI), open shelters, escalate to BNPB if casualties > 100.
- **stabilisasi (1–7 d)**: needs assessment & registration (BPBD/PUPR), WASH + outbreak prevention, humanitarian ceasefire if conflict.
- **pemulihan (3–4 wk)**: structural verification + prioritized rebuild (PUPR), psychosocial recovery (Kemensos).

### LAUT (maritime)
- **resp_t0 (0–2 h)**:
  - Siagakan armada TNI AL: KAL patroli, KRI jarak dekat — Siaga Operasi Kewilayahan Laut (Koarmada I/II)
  - Koordinasi Bakamla & Polisi Perairan — pantau & catat pergerakan kapal musuh
  - Siapkan KRI perang sesuai jumlah musuh untuk intersepsi & penghalauan
  - Evakuasi & amankan nelayan & kapal sipil dari zona operasi (Basarnas Laut / KKP)
- **resp_t1 (2–24 h)**: kapal rumah sakit (KRI dr. Wahidin) & helikopter SAR laut
- **stabilisasi (1–7 d)**: patroli laut intensif — jaga ZEE/ALKI dari serangan susulan
- **pemulihan (3–4 wk)**: rekonstruksi pelabuhan & dermaga

### UDARA (air)
- **resp_t0 (0–2 h)**: Aktifkan Radar (Satradar) & Siaga Hanudnas — siapkan fighter interceptor (Kohanudnas); koordinasi Bandara & ATC — tutup bandara sipil di area terdampak; misi fighter untuk intersepsi.
- **resp_t1 (2–24 h)**: pertahanan udara berlapis (SAM & gun AAA) di instalasi vital
- **stabilisasi (1–7 d)**: perbaikan bandara & instalasi radar yang rusak

### KEBAKARAN (forest_fire / building_fire / settlement_fire)
- **resp_t0**: water bombing (helikopter/Pesawat), pemadaman darat (Manggala Agni + Damkar), isolasi area (Karhutla: kanal sekat gambut).
- **resp_t1**: posko asap & layanan pernapasan (ISPA), evakuasi permukiman terdampak.
- **stabilisasi**: patroli titik panas (hotspot) via satelit/thermal drone, kulim (hujan buatan/weather modification) jika gambut.
- **pemulihan**: restorasi lahan gambut/forestri, rehabilitasi bangunan.

### WABAH/PANDEMI (disease_outbreak / pandemic)
- **resp_t0**: lockdown/sekat zona (pandemic), tracing + isolasi kasus (Dinkes), rujuk RS.
- **resp_t1**: RS darurat + oksigen + APD, rapid test massal, emergency room capacity surge.
- **stabilisasi**: vaksinasi massal, protokol kesehatan, data & surveillance epidemiologi.
- **pemulihan**: pemulihan ekonomi, trauma healing, evaluasi sistem kesehatan.

### SOSIAL (riot / terrorism / mass_violence / demonstration)
- **resp_t0**: pengamanan Polri (PHH/Har Kamtibmas), isolasi area & pengalihan arus, negosiasi/dialog (demo damai).
- **resp_t1**: penegakan hukum (Reskrim/Densus 88 untuk terorisme), BKO TNI bila eskalasi.
- **stabilisasi**: patroli rutin, intelijen, rekonsiliasi.
- **pemulihan**: perbaikan aset publik, trauma healing, penegakan hukum lanjutan.

---

## Preset Skenario Indonesia (for frontend UX)

| Preset | disaster_type | location | lat | lon | pop | area_km2 | infra_density | Key params |
|--------|--------------|----------|-----|-----|-----|----------|--------------|------------|
| **Natuna** | maritime | Laut Natuna Utara | 3.8876 | 108.3892 | 250k | 200 | 0.2 | threat=0.9, blockade, 5× frigate, 30nm, 2000 civilians |
| **Papua** | conflict | Kab. Puncak Jaya, Papua | -3.65 | 137.63 | 200k | 800 | 0.1 | intensity=0.8, insurgency |
| **Timor** | conflict | Perbatasan Timor-Timur | -9.3 | 124.9 | 150k | 300 | 0.3 | intensity=0.6, guerrilla |

---

## Calibration caveat
Estimates are planning-grade, not precise; calibrate with historical BNPB/BMKG data
+ expert input, and validate against real events (Cianjur 2022, Bekasi 2020, Natuna 2021)
before use in production ops.