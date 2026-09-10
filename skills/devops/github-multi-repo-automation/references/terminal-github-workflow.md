# Terminal + GitHub Push Workflow untuk Polri LLM Project

## 🎯 Konteks
Ses ini membangun sistem AI (Polri LLM Gateway Laravel + AI V4 Clone) dan menghadapi tantangan:
- Tools `shell` tidak berfungsi di environment Hermes
- Hanya `terminal` tool yang bisa dipakai
- Token GitHub sering diganti dan perlu aman
- Butuh push otomatis tanpa campur tangan manual

## ✅ Workflow yang Berhasil (Session: 2026-08-20)

### 1. Setup Token Aman
```bash
echo "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" > /tmp/gh_token_file
chmod 600 /tmp/gh_token_file
```

### 2. Buat Repo Baru via GitHub API (jika belum ada)
```bash
TOKEN=$(cat /tmp/gh_token_file)
curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"polri-llm-v4-clone","description":"AI Setara DeepSeek V4","private":true,"auto_init":false}'
```

### 3. Push dari Folder Lokal
```bash
cd /opt/data/polri-llm-v4-clone
git branch -m main
git remote set-url origin "https://$TOKEN@github.com/vanderstark/polri-llm-v4-clone.git" 2>/dev/null || \
git remote add origin "https://$TOKEN@github.com/vanderstark/polri-llm-v4-clone.git"
git add . && git commit -m "Initial commit" --allow-empty
git push -u origin main --force
```

### 4. Cleanup Token
```bash
rm -f /tmp/gh_token_file
```

## 🚨 Lessons Learned

| Masalah | Solusi |
|---------|--------|
| `shell` tool tidak jalan | Pakai `terminal` dengan perintah eksplisit per baris |
| `execute_code` gagal | Gunakan `terminal` langsung |
| Repo not found | Selalu buat repo dulu via API sebelum push |
| Branch mismatch | Pakai `git branch -m main` sebelum push |
| Token exposed | Hapus otomatis di akhir script |

## 🔄 Template Script Reusable

```bash
#!/bin/bash
# push-polri-repo.sh - Push otomatis untuk repo Polri LLM
set -euo pipefail

REPO_NAME="$1"
REPO_DESC="$2"
LOCAL_PATH="$3"
GITHUB_USER="vanderstark"

if [[ -z "$REPO_NAME" || -z "$LOCAL_PATH" ]]; then
  echo "Usage: $0 <repo-name> <description> <local-path>"
  exit 1
fi

TOKEN=$(cat /tmp/gh_token_file)
echo "📦 Creating repo $REPO_NAME..."
curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"$REPO_DESC\",\"private\":true,\"auto_init\":false}" >/dev/null

echo "🚀 Pushing from $LOCAL_PATH..."
cd "$LOCAL_PATH"
git branch -m main
git remote set-url origin "https://$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || \
git remote add origin "https://$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
git add . && git commit -m "feat: $REPO_NAME template" --allow-empty
git push -u origin main --force

rm -f /tmp/gh_token_file
echo "✅ Done: https://github.com/$GITHUB_USER/$REPO_NAME"
```