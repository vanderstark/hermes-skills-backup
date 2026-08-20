# NUT UPS — Docker Deployment Pattern (instantlinux/nut-upsd)

## Image: instantlinux/nut-upsd
- Base: Alpine Linux (16.7 MB)
- Ports: 3493 (NUT daemon), 8080 (optional HTTP status)
- Architectures: amd64, arm64, armv6, armv7
- Requires: `privileged: true` + USB device access (security caveat)

## docker-compose.yml pattern
```yaml
services:
  nut-upsd:
    image: instantlinux/nut-upsd:latest
    container_name: nut-upsd
    restart: unless-stopped
    privileged: true
    ports:
      - "3493:3493"
    environment:
      - UPS_NAME=ups
      - DRIVER=usbhid-ups
      - UPS_MODE=standalone
      - API_USER=admin
      - API_PASSWORD=<change_this_admin_password>
      - MONITOR=yes
    volumes:
      - nut-upsd-data:/var/state/nut
    healthcheck:
      test: ["CMD","/usr/local/bin/upsc","ups@localhost"]
      interval: 30s
      timeout: 5s
      retries: 3
volumes:
  nut-upsd-data:
```

## .env.example (non-secret, user fills in)
- `UPS_NAME=ups` — UPS device name
- `DRIVER=usbhid-ups` — NUT driver for UPS
- `VENDOR_ID=051d` — USB vendor ID (APC) — check via `lsusb`
- `API_PASSWORD=change_this_password` — user must replace
- `MONITOR=yes` — enable upsd monitoring daemon

## Key commands
```bash
docker compose up -d
docker compose exec nut-upsd upsc ups          # battery.charge, ups.status
docker compose exec nut-upsd upsc ups status   # summary
docker compose logs -f nut-upsd                # debug driver issues
```

## Pitfalls
- `privileged: true` = host access risk; if running alongside other containers on same host,
  prefer dedicated host NUT install for auto-shutdown; Docker NUT for display/monitoring only.
- UPS must be connected via USB BEFORE container starts — NUT driver probes USB on startup.
- `UPS_MODE=netclient` mode: remote client connects to another NUT server (multi-host monitoring).
- For auto-shutdown (upsmon → shutdown): use bare-metal NUT systemd service, not Docker container.
