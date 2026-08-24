---
name: ci4-docker-app
description: "Build self-hosted internal CI4 apps via Docker."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [codeigniter, ci4, docker, mysql, adminer, php]
---

# CI4 Docker App — Internal Web App Scaffold

Build a production-ready, self-hosted internal web application with **CodeIgniter 4 + MySQL + Adminer**, containerized for a 3-minute deploy.

## When to use
- User wants an internal PHP/CI4 app (e.g. dashboards, LLM gateways, case trackers).
- Stack must be self-hosted, intranet, Docker-based, with a DB panel (Adminer) for ops.
- Requirements include: login/auth, role-based access (RBAC), audit trail, sensitive-data redaction, prompt/usage quota, seed data, and full docs.

## Architecture (1-DB/repo)
```
docker-compose.yml   # db (mysql) + adminer (8081) + app (8080)
Dockerfile           # php:8.3-apache + pdo_mysql/intl/mbstring + composer
app/                 # CodeIgniter 4 project (composer create-project)
├── app/Config/Routes.php
├── app/Controllers/  (Auth, <Feature>Controller, AdminController)
├── app/Models/       (UserModel, AuditModel, feature models)
├── app/Database/Migrations/*.php
├── app/Database/Seeds/PoliceSeeder.php
├── app/Views/        (login, dashboard, feature views — Bootstrap 5 CDN)
└── .env
```

## Steps
1. **Scaffold CI4**: `composer create-project codeigniter4/appstarter app`.
2. **Dockerfile** (php:8.3-apache): install `pdo_mysql intl mbstring gd`, `a2enmod rewrite`.
3. **docker-compose.yml**: `db` (mysql), `adminer` (8081), `app` (8080).
4. **Auth + RBAC**: Users table with `unit, role, quota`. Use Auth filter + session-based access.
5. **Audit log**: `audit_logs` table. `AuditModel` logs user_id, action, endpoint, details (JSON). Call `$this->auditModel->log(...)` in sensitive controllers.
6. **Auto-redact**: Redact helper (`preg_replace`) for NIK (16-digit), phone, email. Redact output BEFORE inserting into `prompt_usage_logs`.
7. **PDF export**: `composer require dompdf/dompdf`, use `Dompdf` to stream reports.
8. **Docs**: README with deploy (3 min) + usage + troubleshooting (Production-ready: README + INSTALL + USAGE + TROUBLESHOOTING + LICENSE).

## Pitfalls
- **php-fpm needs web server** — use `php:8.3-apache` base to expose port 80 directly.
- **CI4 rewrite**: `.htaccess` + `AllowOverride All` + `a2enmod rewrite` needed for routes.
- **writable/ permissions**: `chmod -R 777 writable` required for logs/cache.
- **Redact first**: if you log raw prompt/response, you defeat privacy. Redact before log.

## Verification
- `php -l` every PHP file before commit.
- `docker-compose up -d` → `php spark migrate` → `php spark db:seed PoliceSeeder`.
- Send prompt containing fake NIK → verify `[REDACTED_NIK]` in output.
