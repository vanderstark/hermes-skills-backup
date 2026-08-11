# NUT (Network UPS Tools) — Monolith + Docker notes

## Monolith repo: vanderstark/nut-ups-monolith (Ubuntu 24.04, no Docker)
Structure:
- `installer/install.sh` — connects to USB UPS, installs nut/nut-client/nut-server/nut-monitor,
  writes `/etc/nut/*`, udev rule, enables systemd; verifies with `upsc ups`
- `installer/uninstall.sh` — stops services, removes packages, backs up `/etc/nut` to `/etc/nut.backup.*`
- `installer/ups-check.service` — optional periodic check unit
- `scripts/check-ups.sh` — `--alarm` (exit 1 if power fails/battery<50%) / `--json` for Zabbix/Telegraf

Install: `sudo bash installer/install.sh` → edit `/etc/nut/upsd.users`
(change `change_this_password` & `change_this_admin_password`) → `sudo systemctl restart nut-server`

Config files written by installer:
- `/etc/nut/nut.conf` → MODE=standalone
- `/etc/nut/ups.conf` → [ups] driver usbhid-ups, port auto, vendorid/productid dari lsusb
- `/etc/nut/upsd.conf` → LISTEN 127.0.0.1 3493 + 0.0.0.0 3493
- `/etc/nut/upsd.users` → [monuser] upsmon master, [admin] upsmon admin
- `/etc/nut/upsmon.conf` → MONITOR ups@localhost 1 monuser <pw> master; SHUTDOWNCMD
  "/sbin/shutdown -h +0"

Status codes: `upsc ups` → ups.status: OL (on line PLN), OB (on battery), LB (low battery),
OL CHRG (charging). Other fields: battery.charge, battery.runtime, battery.voltage, ups.load.

## Docker option: instantlinux/nut-upsd
- Alpine base 16.7MB, multi-arch amd64/arm64/armv6/armv7, 1M+ pulls, updated recently, GPL-2.0
- Runs upsd server + USB drivers; exposes TCP 3493; env vars DRIVER/SERIAL/VENDORID/API_USER/API_PASSWORD
- **Requires `privileged: true`** for USB device access — host security risk
- Multi-UPS: one container per UPS, bind 3493 to separate ports
- Works APC/Tripp Lite/CyberPower (CyberPower needs MAXAGE > 25)
- Detection: `lsusb -D /dev/bus/usb/NNN/NNN` → idVendor/idProduct/iSerial
- udev rule on host for raw access, e.g.
  `SUBSYSTEM=="usb", ATTRS{idVendor}=="09ae", ... MODE="0660", GROUP="nut"`
- Verdict: container OK for monitoring/display; bare-metal NUT (systemd) more reliable
  for critical auto-shutdown in a DC

## Grafana integration paths
- Prometheus + `hon95/nut_exporter` (NUT_SERVER/NUT_PORT env) → scrape → Grafana
- Telegraf `inputs.exec` runs `check-ups.sh --json` → InfluxDB → Grafana
- Zabbix UserParameter → items → triggers → Grafana via Zabbix plugin

## Cron alarm example
```
*/5 * * * * /opt/nut-ups/scripts/check-ups.sh --alarm && echo "UPS OFF! $(date)" | mail -s "⚠️ UPS OFF" admin@dc.local
```