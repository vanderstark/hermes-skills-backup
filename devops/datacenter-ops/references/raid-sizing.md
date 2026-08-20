# RAID Sizing — 8 TB per disk reference table

Formula: usable = (N − P) × disk_size ; efficiency = usable / (N × disk_size)

## RAID 6 (P=2, toleransi 2 disk) — 8 TB disks
| N | Bruto | Bersih | Efisiensi |
|---|---|---|---|
| 4 | 32 TB | 16 TB | 50% |
| 6 | 48 TB | 32 TB | 66.7% |
| 8 | 64 TB | 48 TB | 75% |
| 10 | 80 TB | 64 TB | 80% |
| 12 | 96 TB | 80 TB | 83.3% |

## Other configs for 3×8TB (asked in session)
- RAID6: **TIDAK BISA** — minimum 4 disk (2 data + 2 parity, matematis)
- RAID5: 16 TB, tahan 1 disk — opsi paling cocok untuk 3 disk
- RAID1 3-way: 8 TB, tahan 2 disk
- RAID0: 24 TB, tanpa redundancy — tidak untuk data penting
- JBOD: 24 TB gabungan, tanpa proteksi

## 4×8TB comparison (asked in session)
| Metrik | RAID 6 | RAID 5 |
|---|---|---|
| Bersih | 16 TB (50%) | 24 TB (75%) |
| Toleransi | 2 disk | 1 disk |
| Write penalty | lebih tinggi (2 parity) | lebih rendah |
| Risiko rebuild | sedang | TINGGI — disk ke-2 gagal saat rebuild = data hilang |

## Use-case recommendations
- Backup target (Proxmox Backup Server): ZFS RAID-Z2, 6–8 disk/vdev
- Primary storage VM/CT: RAID10 — IOPS tinggi, rebuild cepat (<2 jam)
- Cold archive: RAID6/RAID-Z2, 8+ disk

## Rebuild & drive advice (8TB+)
- Rebuild 8TB ≈ 12–24 jam tergantung controller/workload; array degraded saat rebuild
- URE konsumen ~1×10^14 bit → risiko gagal rebuild nyata → HDD enterprise/NAS
  (Seagate Exos/IronWolf Pro, WD Ultrastar/Red Pro), hot spare, monitoring SMART
- ZFS RAID-Z2 lebih aman dari RAID hardware: checksum end-to-end, self-healing,
  tanpa butuh battery-backed cache