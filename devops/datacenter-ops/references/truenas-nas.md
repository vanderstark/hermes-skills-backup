# TrueNAS di Ubuntu 24.04 — Catatan Sesi

## 3 Metode Install

### A. TrueNAS SCALE sebagai VM di Proxmox VE (rekomendasi)
- ISO ~2 GB (`wget https://download.truenas.com/TrueNAS-SCALE-*.iso` → `/var/lib/vz/template/iso`)
- Buat VM: `q35` machine type, `OVMF (UEFI)` BIOS (wajib — SeaBIOS = boot loop), VIRTIO disk + NIC,
  ≥8 GB RAM, ≥50 GB system disk
- Konfigurasi WebUI: `http://IP` → pool → dataset (`/mnt/tank/share`) → SMB/NFS/iSCSI shares
- iSCSI untuk PBS: buat zvol → add target/extent → di Proxmox: Storage → Add → iSCSI

### B. Replicate di Ubuntu 24.04
- Stack: `zfsutils-linux` + `samba` + `nfs-kernel-server` + `cockpit` + `cockpit-storaged`
- Plugin ZFS: `github.com/optimans/cockpit-zfs` (install via wget+tar, restart cockpit)
- Pool: `sudo zpool create -o ashift=12 tank raidz2 /dev/sdX /dev/sdY /dev/sdZ /dev/sdW`
  (raidz2 = min 4 disk, 2 parity; raidz = min 3 disk)
- Dataset: `sudo zfs create tank/share`; access: `chown`, `chmod 755`
- SMB: add user to `sambashare`, `smbpasswd -a USER`, edit `/etc/samba/smb.conf` [share] block,
  `smbclient -L localhost -U USER` test
- NFS: `echo "/tank/share 192.168.1.0/24(rw,sync,no_subtree_check)" >> /etc/exports && exportfs -ra`
- Snapshot: `zfs snapshot tank/share@auto-$(date +%Y%m%d-%H%M)`, cron 0 2 * * *
- Snapshot cleanup: `zfs destroy tank/share@auto-YYYYMMDD-HHMM` (>retention_days)

### C. Standalone
- Flash ISO: Rufus (Windows, DD mode), `dd bs=4M status=progress` (Linux), balenaEtcher (Mac)
- Install: select SSD → erase → root password → reboot
- Post-install: set IP statis (Network → Global Configuration), Scrub Tasks, Periodic Snapshot Tasks
- NUT built-in: Services → UPS (NUT) → driver usbhid-ups, port auto

## Pitfalls
- UEFI requirement: Proxmox VM MUST use `OVMF (UEFI)` — not SeaBIOS. This is the #1 boot-loop cause.
- ZFS on root vs separate disk: never create a pool on the boot/root disk. Use dedicated data disks.
- `zpool import tank`: run if pool vanishes after reboot (`/etc/default/zfs` → `ZFS_INITRD_PRE_MOUNTROOT=yes`)
- Cockpit plugin: if `optimans/cockpit-zfs` install fails, manual: `/usr/share/cockpit/zfs/`
- Snapshot retention: no default auto-delete; must schedule cron or UI cleanup, else disk fills.

## Alternatives Comparison (for reference)
| Tool | Lisensi | Basis | Kekuatan | Cocok |
|---|---|---|---|---|
| TrueNAS SCALE | Free | Debian | ZFS+Apps+VM | DC / NAS server |
| TrueNAS CORE | Free | FreeBSD | ZFS stabil | NAS murni |
| Unraid | $59+ | Linux | UI ramah, mix disk, Docker+VM | Homelab |
| OpenMediaVault | Free | Debian | Ringan, plugin | UMKM / rumah |
| Proxmox VE | Free | Debian | VM+LXC+Ceph/ZFS | Virtualisasi |
| PBS | Free | Debian | Backup target | VM/CT backup |
| Cockpit+ZFS | Free | Linux | Ringan, modern | Metode B di atas |
