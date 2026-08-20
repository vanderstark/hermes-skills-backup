---
name: datacenter-ops
description: Use for RAID sizing, UPS/NUT, or DC monitoring.
---

# Datacenter Ops — RAID/Storage, UPS/NUT, Monitoring Stacks

Class-level guide for Eko ("Bos"): 170-server datacenter + police academy AI/OSINT lab.
Reply in **Bahasa Indonesia**, hormat tone, address as "Bos", exactly 3x 🙏🙏🙏 per message.

## When to use
- Storage math: "HDD X TB x N RAID 6 menjadi berapa?" (recurring — asked 4x in one session)
- UPS / kelistrikan: NUT setup, docker vs monolith, PDU/UPS monitoring
- "Tools untuk super admin data center": monitoring, DCIM, network, physical security stack

## RAID / storage sizing — quick reference
- Formula: usable = (N − P) × disk size. RAID5 → P=1, RAID6 → P=2, RAID10 → 50% usable.
- RAID6 minimum 4 disks (hard constraint: 2 data + 2 parity). 3 disks CANNOT do RAID6 —
  offer RAID5 (16 TB @ 3×8TB), 3-way RAID1 (8 TB), or JBOD. Never claim it works.
- Efficiency improves with N: 4×8TB RAID6=16TB (50%), 6×8TB=32TB (66.7%), 8×8TB=48TB (75%).
- 8TB+ disks: rebuild 12–24h+, degraded-array URE risk → recommend enterprise/NAS drives
  (Exos / IronWolf Pro / Ultrastar), hot spare, SMART monitoring.
- Use case: backup/PBS → ZFS RAID-Z2 (6–8 disk vdev); VM primary → RAID10; cold archive → RAID6.
- Full tables & comparisons: `references/raid-sizing.md`

## UPS / NUT (Network UPS Tools)
- **Monolith repo**: `vanderstark/nut-ups-monolith` — Ubuntu 24.04 installer,
  `sudo bash installer/install.sh` auto-detects USB UPS (lsusb vendorid/productid), writes `/etc/nut/*`,
  enables systemd `nut-server nut-monitor nut-client`, listener port 3493.
  Placeholder passwords `change_this_password` / `change_this_admin_password` in upsd.users.
- **Docker repo**: `vanderstark/nut-ups-docker` — `instantlinux/nut-upsd` (Alpine 16.7MB, multi-arch,
  1M+ pulls) via docker-compose, port 3493, `privileged: true` + USB devices for access (security caveat).
  Includes `.env.example` (UPS_NAME/DRIVER/VENDOR_ID/API_PASSWORD placeholders), `install.sh`
  (setup .env + secrets/nut-password.txt + compose up), `config/ups.conf` template. Per rule, docker &
  monolith are SEPARATE repos.
- Fine for monitoring/display, but auto-shutdown kritis lebih andal di bare-metal NUT (systemd).
- Verify: `upsc ups` → `ups.status: OL` (PLN normal), OB (baterai), LB (kritis).
- Config map + troubleshooting: `references/nut-ups-monolith.md`; Docker compose pattern: `references/nut-ups-docker.md`

## TrueNAS / NAS storage (asked 2026-08)
- **TrueNAS SCALE is a standalone OS (Debian-based), NOT a package installable on top of Ubuntu** —
  tell users this upfront (jujur). Three valid routes: (a) VM di Proxmox (paling disarankan),
  (b) replicate fungsi di Ubuntu murni, (c) boot langsung standalone di dedicated hardware.
- Replicate stack ~90% TrueNAS: `zfsutils-linux` + Samba + `nfs-kernel-server` + Cockpit
  (`cockpit-storaged`, `:9090`) + plugin `optimans/cockpit-zfs`; lacks TrueNAS Apps/VM.
- Pool: `sudo zpool create -o ashift=12 tank raidz2 /dev/sdX ...` (RAID-Z2 min 4 disk;
  raidz=3, raidz3=5). Dataset per use case (`tank/share`, `tank/backup`), snapshot cron dengan retensi
  (`zfs snapshot tank/share@auto-$(date +%Y%m%d-%H%M)`, destroy >14 hari), `zpool scrub` terjadwal.
- TrueNAS VM di Proxmox: WAJIB `q35` + `OVMF (UEFI)` — SeaBIOS = boot loop; disk/network VirtIO,
  RAM ≥8 GB, ISO di `/var/lib/vz/template/iso`.
- Repos (split per metode, per user rule): `truenas-proxmox-vm`, `truenas-on-ubuntu`
  (README + `scripts/setup-nas-ubuntu.sh` + `create-pool.sh` + `snapshot-zfs.sh`),
  `truenas-standalone`. Detailed notes: `references/truenas-nas.md`

## Monitoring / DCIM stack (recommended for 170-server DC)
- Power: NUT + kWh meter Modbus (Eastron SDM630) + PDU SNMP → Telegraf → InfluxDB → Grafana.
- Backbone: Zabbix (SNMP/IPMI/BMC), Netdata (per-host realtime), Pulse (Proxmox/PBS AI patrol),
  Prometheus + Grafana.
- **Centralized Logging**: Loki + Promtail (pull) — 2 repo split:
  - `vanderstark/loki-logging-docker` — Docker Compose (Loki + Promtail + Grafana), script `setup-loki.sh`, bulk agent deploy via `deploy-bulk.sh servers.txt`.
  - `vanderstark/loki-logging-monolith` — Native binary (no Docker), systemd units, same agent deploy pattern.
  - Agent pattern: Promtail agent installed via SSH on each target server (170 servers), ships logs to central Loki. Both repos include `servers.txt.example` template.
- DCIM/IPAM: **NetBox** (rack U, cable map, IP/VLAN, power per PDU — push this one), alt:
  RackTables / OpenDCIM / phpIPAM.
- Network: LibreNMS / Observium, The Dude, OpenNMS. Automation: Ansible + Terraform + ipmitool.
- Physical: Modbus temp/humidity sensors, Frigate CCTV (AI), ZKTeco access control.
- NAS alternatives to recommend: OpenMediaVault (Debian, ringan), Unraid (bayar, mix disk), Proxmox VE
  (virtualisasi + storage), PBS (backup target VM/CT), MinIO (S3 object), Cockpit+ZFS (replicate = metode B).
- TrueNAS clones/alternatives comparison table lives in `references/truenas-nas.md`.

## Agent deployment patterns (for all monitoring stacks)
- **Prometheus (pull)**: Node Exporter agent on each target → scrape config via `file_sd_configs` or static targets. Scripts: `deploy-agent.sh` + `install-agent.sh` + `servers.txt.example`.
- **Uptime Kuma (push)**: Pushbeat agent (curl loop) on each target → HTTP heartbeat to Uptime Kuma Push API. Each server needs unique Push URL (1 monitor per server). Scripts: `install-agent.sh` + `deploy-bulk.sh`.
- **Loki (push)**: Promtail agent on each target → HTTP push to Loki `/loki/api/v1/push`. Scripts: `deploy-bulk.sh` + `install-agent.sh` (Docker or native binary).
- All stacks: `servers.txt.example` template, bulk deploy scripts, SSH root key-based auth required.

## Pitfalls
- RAID6 with 3 disks: state the constraint upfront, give valid alternatives immediately.
- NUT in Docker: privileged mode = host security risk; for shutdown automation prefer host install.
- After any repo push: strip token from remote, remind user to revoke PAT & change placeholders.