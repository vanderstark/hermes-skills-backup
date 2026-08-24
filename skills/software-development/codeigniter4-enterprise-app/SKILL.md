---
name: codeigniter4-enterprise-app
description: "Build secure CI4 apps with Audit, Redact, and Cron."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# CodeIgniter 4 Enterprise / Secure Internal App

Builds production-ready CodeIgniter 4 + MySQL apps with Docker, focused on the recurring Polri internal-app domain: RBAC per unit, full audit logging, auto-redaction of sensitive PII, and autonomous maintenance (backup / cleanup / quota reset).

## When to use
- Building or extending a CI4 internal tool for Polri units (Intelkam, Reskrim, Binmas, Sabhara, Lantas) or similar secure intranet apps.
- Need: user CRUD + daily prompt/action quota, OSINT tool integration, PDF export, auto-redact, audit trail, scheduled maintenance.
- Target: self-hosted intranet, 3-minute Docker deploy.

## Core patterns

### 1. RBAC via session
Store `user_id`, `unit`, `role`, `logged_in` in session after login. Gate controllers: `if (! $this->session->get('logged_in')) return redirect()->to('/login');`. Keep a permission matrix (Admin / Analis / Operator / Pimpinan) — hide actions in UI by role, not just controller checks.

### 2. Audit log (capture every action)
Create `audit_logs` table (id, user_id, action, endpoint, details, ip_address, user_agent, created_at). `AuditModel` inserts on every mutating action. See `references/ci4-recipes.md` for the model + a `log()` helper. Wire into PromptController::send, KasusController CRUD, login.

### 3. Auto-redact sensitive PII
Before storing LLM/OSINT output, run `redactSensitiveInfo()` with regex for: NIK (16-digit), Indonesian phone (+62 / 08xx), email. Replace with `[REDACTED_NIK]` etc. Critical for data-security compliance — never persist raw NIK / phone / email.

### 4. Migration + Seeder
One migration per schema change. Seeder (`PoliceSeeder`) inserts 6 units, SOP docs, sample cases, prompt templates. Make migrations idempotent (guard `addColumn` with `fieldExists`).

### 5. Maintenance as a Spark command + Docker cron
Create `app/Commands/Maintenance.php` (`php spark app:maintenance`) that: deletes audit logs > 90 days, `mysqldump` to `writable/backups/`, rotates to 14 files, resets `usage_count` on day 1. Mount a crontab into the Docker image and run `cron -f` as the container command. See recipes.

### 6. Docker Compose
Services: `db` (mysql:8.0 + healthcheck), `app` (php:8.3-fpm build), `adminer` (8081), `cron` (same build, `cron -f`). Expose 8080 (app), 8081 (adminer), 3306 (db).

## Pitfalls
- **Autonomous delivery, not chat dumps.** User expects files written to disk and pushed to GitHub, not code blocks pasted in chat for manual copy. After building, run `git add -A && git commit -m "..." && git push origin main`. Present a short summary + RAPI markdown table, not the source.
- **write_file needs both `path` and `content`.** A call missing `path` is rejected. Always supply both.
- **Audit log `created_at` must be set manually** if `$useTimestamps = false` (CI4 AuditModel pattern). Use `date('Y-m-d H:i:s')`.
- **mysqldump in container** needs the mysql client installed in the image (add `default-mysql-client` to Dockerfile `apt-get install`). Otherwise the backup step fails silently.
- **Crontab file needs a trailing newline** or cron ignores it.
- **Revoke GitHub PAT** after every push (token in /tmp/gh_token_file, chmod 600).

## Verification
- `find app -name "*.php" -exec php -l {} \;` → all "No syntax errors detected".
- `docker-compose exec app php spark migrate` runs clean.
- `docker-compose exec app php spark app:maintenance` prints 4 steps OK.

See `references/ci4-recipes.md` for copy-ready code.
