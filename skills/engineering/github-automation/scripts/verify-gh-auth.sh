#!/usr/bin/env bash
# Verify gh auth status before running GitHub operations
set -euo pipefail

echo "🔍 Checking GitHub Authentication Status..."

# Check if gh is authenticated
STATUS=$(gh auth status 2>/dev/null || echo "NOT_AUTHD")

if echo "$STATUS" | grep -q "keyring"; then
    echo "✅ Authenticated: $(echo "$STATUS" | grep -o 'Logged in as [^(]*' | head -1)"
    echo "   Protocol: $(echo "$STATUS" | grep -o 'protocol: [^ ]*' | head -1 | cut -d' ' -f2)"
    echo "   Token: Active (keyring-backed)"
    exit 0
else
    echo "❌ Not authenticated or token invalid"
    echo "   Full status output:"
    gh auth status 2>&1 || true
    echo ""
    echo "💡 Run: gh auth login to re-authenticate"
    exit 1
fi