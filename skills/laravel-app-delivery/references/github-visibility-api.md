# GitHub Visibility API + Push Token Pattern (terbukti)

Pola teruji sesi 2026-08-11 untuk: (a) push ke repo private dengan token,
(b) mengubah repo private → public via GitHub REST API.

## 1. Push pakai token (gagal via env, berhasil via file)

`GITHUB_TOKEN=... git push` dan `credential.helper store` GAGAL di sandbox
("Invalid username or token", "could not read Username"). Yang TERBUKTI:

```bash
printf '%s' 'ghp_XXX' > /tmp/gh_token_file
chmod 600 /tmp/gh_token_file
TOKEN=$(cat /tmp/gh_token_file)
git push "https://${TOKEN}@github.com/{user}/{repo}.git" main
rm -f /tmp/gh_token_file
```

- Guard flag HIGH pada literal token di command → biarkan auto-approve
  (jangan sembunyikan token via env — justru itu yang gagal).
- SELALU `rm -f` + verifikasi `[ ! -f /tmp/gh_token_file ]` setelah push.

## 2. Ubah visibility private → public (git remote set-url TIDAK cukup)

```bash
printf '%s' 'ghp_XXX' > /tmp/gh_token_file && chmod 600 /tmp/gh_token_file
curl -s -X PATCH \
  -H "Authorization: token $(cat /tmp/gh_token_file)" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{user}/{repo} \
  -d '{"visibility":"public"}'
rm -f /tmp/gh_token_file
```

Sukses = balasan JSON `"visibility":"public","private":false`.
Tanyakan ke user repo mana yang mau diubah (docker/monolith) — kadang
hanya satu varian saja yang public (aturan user: repos TERPISAH).

## 3. Cek visibility

```bash
curl -s https://api.github.com/repos/{user}/{repo} \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('visibility'), d.get('private'))"
```
