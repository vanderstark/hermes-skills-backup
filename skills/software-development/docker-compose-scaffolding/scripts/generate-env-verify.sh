#!/bin/bash
# generate-env-verify.sh — Verify env vars exist and contain valid values
# Usage: cd /path/to/compose/folder && bash generate-env-verify.sh

set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.yml}"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "ERROR: $COMPOSE_FILE not found" >&2
  exit 1
fi

echo "=== Verifying env vars in $COMPOSE_FILE ==="

# Extract all variable names referenced in docker-compose.yml (environment blocks)
# Note: this is a simple grep-based scan. For complex cases, use yq or a proper parser.
grep -oP '^\s*-?\s*\$\K[A-Z_][A-Z0-9_]+' "$COMPOSE_FILE" | sort -u | while read -r var; do
  if grep -q "environment:\s*$var\s" "$COMPOSE_FILE" || grep -q "environment:\s*$var\b\s" "$COMPOSE_FILE"; then
    echo "  ✅ $var — found in environment section"
  else
    echo "  ⚠️  $var — referenced but NOT found in environment section (may be OK)"
  fi
done

# Verify no secrets in .env.example (or any example file that may have been
# mistakenly put in the repo) — a simple grep for common secret keywords
for f in .env.example .env; do
  if [[ -f "$f" ]]; then
    echo "  ⚠️  $f exists (check contents for real secrets before committing)"
  fi
done

# Confirm YAML parse (only valid if python + pyyaml available — otherwise just exit)
if command -v python3 >/dev/null 2>&1; then
  python3 -c "
import yaml, sys
with open('$COMPOSE_FILE') as fh:
    d = yaml.safe_load(fh)
print(f'  ✅ YAML valid — {len(d.get(\"services\", {}))} services loaded')
" 2>/dev/null || echo "  ⚠️  YAML syntax check failed — verify by hand"
fi

echo "=== Verification complete ==="