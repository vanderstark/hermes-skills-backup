# Ubuntu 24.04 Systemd + Venv Installer Pattern (Monolith)

Verified pattern from `crisis-command-center-monolith` — reusable when building
a bare-metal installer for a Python FastAPI/uvicorn app.

## Directory Layout

```
repo/
├── installer/
│   ├── install.sh
│   ├── uninstall.sh
│   └── <service-name>.service
├── backend/
├── frontend/
├── requirements.txt
└── README.md  (monolith-specific — NO Docker references)
```

## install.sh skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
APP_NAME="my-app"
APP_DIR="/opt/${APP_NAME}"
USER_RUN="${SUDO_USER:-$(logname 2>/dev/null || echo ubuntu)}"
SERVICE="${APP_NAME}.service"
[ "$(id -u)" -eq 0 ] || err "Run as root: sudo bash installer.sh"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip curl ca-certificates
mkdir -p "${APP_DIR}"
cp -r "$(dirname "$(readlink -f "$0")")/../" "${APP_DIR}/"   # careful — don't pull installer/.git
python3 -m venv "${APP_DIR}/venv"
"${APP_DIR}/venv/bin/pip" install --upgrade pip -q
"${APP_DIR}/venv/bin/pip" install -r "${APP_DIR}/requirements.txt" -q
chown -R "${USER_RUN}:${USER_RUN}" "${APP_DIR}"
cat > /etc/systemd/system/${SERVICE} << EOF
[Unit]
Description=${APP_NAME}
After=network.target
[Service]
Type=simple
User=${USER_RUN}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now ${SERVICE}
sleep 3
curl -sf http://127.0.0.1:8000/api/health >/dev/null && echo "✅"
```

## Pitfalls

- **`--host 0.0.0.0`** is mandatory for LAN access, not 127.0.0.1.
- Tiles are NOT committed — use `.gitkeep` + download script; installer doesn't fetch tiles.
- `SUDO_USER` vs `logname`: sudo context vs console-only installs.
