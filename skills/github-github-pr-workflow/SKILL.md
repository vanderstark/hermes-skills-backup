---
name: github-github-pr-workflow
description: Use when managing GitHub pull request workflow.
---

# GitHub PR Workflow

## Kapan Digunakan
- User minta buat branch baru untuk fitur/fix
- User minta buka pull request
- User minta review/merge PR yang sudah ada
- Mengelola siklus development end-to-end di repo GitHub (termasuk repo privat Bos: vanderstark/*)

## Langkah Kerja

### 1. Branching
```bash
git checkout -b feature/nama-fitur
# atau
git checkout -b fix/nama-bug
```

### 2. Commit
```bash
git add <files>
git commit -m "type: deskripsi singkat

Detail perubahan jika perlu.
"
```
Konvensi commit: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

### 3. Push & Buka PR (via gh CLI)
```bash
git push -u origin feature/nama-fitur
gh pr create --title "Judul PR" --body "Deskripsi perubahan" --base main
```

### 4. Cek Status CI
```bash
gh pr checks <PR-number>
gh pr view <PR-number>
```

### 5. Merge
```bash
gh pr merge <PR-number> --squash --delete-branch
```

## Autentikasi Token (Headless/Agentic Environment)
Untuk push tanpa prompt interaktif di lingkungan Hermes:
```bash
git remote set-url origin https://<TOKEN>@github.com/<owner>/<repo>.git
git push
git remote set-url origin https://github.com/<owner>/<repo>.git  # revert setelah push
unset GITHUB_TOKEN
```

**PENTING (aturan keamanan Bos):**
- Jangan simpan token di `/tmp` sebagai file
- Selalu revert remote URL ke bentuk tanpa token setelah push selesai
- Ingatkan user untuk revoke token di github.com/settings/tokens setelah pekerjaan selesai
- Jangan pernah commit `.env` atau file secrets — pastikan `.gitignore` aktif

## Pitfalls
- Repo yang diverge (histori lokal vs remote beda) → `git pull --rebase origin main` sebelum push
- GitHub push protection akan menolak commit yang mengandung token/secret contoh di dokumentasi
- Selalu cek `git status` sebelum commit untuk hindari commit file yang tidak diinginkan
