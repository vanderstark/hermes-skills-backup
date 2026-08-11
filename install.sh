#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# install.sh — Restore SEMUA skill & plugin Hermes dalam 1 perintah
#
# Cara pakai:
#   bash install.sh                # restore dari repo (default: lokal)
#   bash install.sh --from-github  # clone langsung dari GitHub lalu restore
#   bash install.sh --skill-only   # hanya restore skills (tanpa plugins)
#   bash install.sh --dry-run      # simulasi, tidak menulis apa pun
#
# Sumber repo: https://github.com/vanderstark/hermes-skills-backup
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

REPO_URL="https://github.com/vanderstark/hermes-skills-backup.git"
REPO_NAME="hermes-skills-backup"
FROM_GITHUB=0
SKILL_ONLY=0
DRY_RUN=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR=""

# ── Parse argumen ──────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --from-github) FROM_GITHUB=1 ;;
    --skill-only)  SKILL_ONLY=1 ;;
    --dry-run)     DRY_RUN=1 ;;
    *) echo "❌ Argumen tidak dikenal: $arg" >&2; exit 1 ;;
  esac
done

# ── Tentukan HERMES_HOME ───────────────────────────────────────
if [ -n "${HERMES_HOME:-}" ]; then
  HERMES_HOME="${HERMES_HOME%/}"
else
  HERMES_HOME="$HOME"
fi
echo "📍 HERMES_HOME = $HERMES_HOME"

# ── Pastikan source repo ada ───────────────────────────────────
SRC="$SCRIPT_DIR"
if [ "$FROM_GITHUB" -eq 1 ]; then
  TMP_DIR="$(mktemp -d)"
  echo "⬇️  Clone dari GitHub: $REPO_URL"
  git clone --depth 1 "$REPO_URL" "$TMP_DIR/$REPO_NAME" >/dev/null 2>&1 || {
    echo "❌ Gagal clone. Cek koneksi internet / repo." >&2
    exit 1
  }
  SRC="$TMP_DIR/$REPO_NAME"
fi

trap 'rm -rf "$TMP_DIR"' EXIT

# ── Fungsi helper ──────────────────────────────────────────────
restore() {
  local target="$1" source="$2" label="$3"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "🔍 [DRY-RUN] Akan restore $label → $target"
    return 0
  fi
  mkdir -p "$(dirname "$target")"
  if [ -e "$target" ]; then
    echo "📦 Backup existing $label → ${target}.bak-$(date +%Y%m%d%H%M%S)"
    mv "$target" "${target}.bak-$(date +%Y%m%d%H%M%S)"
  fi
  cp -a "$source" "$target"
  echo "✅ $label → $target"
}

# ── Mulai restore ──────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════"
echo "  HERMES SKILL & PLUGIN RESTORE"
echo "══════════════════════════════════════════════════════════"

# 1. Skills (jika ada folder skills di source)
if [ -d "$SRC/skills" ]; then
  restore "$HERMES_HOME/skills" "$SRC/skills" "SKILLS"
else
  echo "ℹ️  Folder skills/ tidak ditemukan di source — dilewati"
fi

# 2. Plugins (kecuali --skill-only)
if [ "$SKILL_ONLY" -ne 1 ] && [ -d "$SRC/plugins" ]; then
  restore "$HERMES_HOME/plugins" "$SRC/plugins" "PLUGINS"
else
  echo "ℹ️  Plugins dilewati (--skill-only atau tidak ada)"
fi

# 3. AGENTS.md (project rules / aktivasi Task Observer)
if [ -f "$SRC/AGENTS.md" ]; then
  restore "$HERMES_HOME/AGENTS.md" "$SRC/AGENTS.md" "AGENTS.md"
fi

# 4. Persyaratan Python (requirements.txt) — opsional
if [ -f "$SRC/requirements.txt" ] && [ "$DRY_RUN" -ne 1 ]; then
  echo "ℹ️  requirements.txt ditemukan — lewati (dipasang manual sesuai kebutuhan)"
fi

# ── Verifikasi ─────────────────────────────────────────────────
if [ "$DRY_RUN" -ne 1 ]; then
  echo ""
  echo "══════════════════════════════════════════════════════════"
  echo "  VERIFIKASI"
  echo "══════════════════════════════════════════════════════════"
  echo "📊 Jumlah SKILL.md terpasang: $(find "$HERMES_HOME/skills" -name 'SKILL.md' 2>/dev/null | wc -l)"
  echo "📊 Jumlah file plugin:       $(find "$HERMES_HOME/plugins" -type f 2>/dev/null | wc -l)"
  echo ""
  echo "✅ RESTORE SELESAI! Restart sesi Hermes agar skill terbaca."
  echo "   Verifikasi: skills_list → semua skill muncul"
fi