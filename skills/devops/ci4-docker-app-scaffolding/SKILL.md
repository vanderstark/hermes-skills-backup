---
name: ci4-docker-app-scaffolding
category: devops
description: Setup CodeIgniter 4 apps with Docker, MySQL, Adminer.
---

## ci4-docker-app-scaffolding

Use this skill when the user asks to build a CodeIgniter 4 application and deploy it with Docker Compose, including MySQL and Adminer.

### Workflow:

1.  **Create GitHub Repository:**
    *   `gh repo create <owner>/<repo_name> --public --description "<description>"`
2.  **Clone Repository:**
    *   `git clone https://github.com/<owner>/<repo_name>.git`
    *   `cd <repo_name>`
3.  **Scaffold CodeIgniter 4 Application:**
    *   Download `composer.phar` temporarily: `curl -sS https://getcomposer.org/installer | php`
    *   Create CI4 project in a temporary directory: `php composer.phar create-project codeigniter4/appstarter ci4_temp --no-install`
    *   Move files to root and clean up:
        ```bash
        shopt -s dotglob
        mv ci4_temp/* .
        mv ci4_temp/.env .
        rm -rf ci4_temp
        rm composer.phar
        ```
    *   Configure Git user: `git config --global user.email "hermes@nousresearch.com"` (or user's email), `git config --global user.name "Hermes Agent"` (or user's name).
    *   Commit initial scaffolding: `git add . && git commit -m "chore: scaffold CI4 appstarter"`
    *   Push to GitHub: `git push origin main`
4.  **Create Docker Compose, Dockerfile, and Nginx Config:**
    *   `docker-compose.yml`: Defines services for `app` (PHP-FPM), `nginx`, `db` (MySQL), and `adminer`.
    *   `Dockerfile`: Builds PHP-FPM image, installs necessary extensions (e.g., `intl`, `gd`, `pdo_mysql`).
    *   `nginx.conf`: Configures Nginx to serve the CI4 application.
5.  **Install Composer Dependencies (within Docker context):**
    *   When the Docker containers are built (`docker-compose up --build`), ensure `composer install` runs inside the PHP-FPM container to resolve dependencies (the `Dockerfile` should include `RUN composer install` after copying `composer.json`).
6.  **Create Database Migrations (CodeIgniter Spark):**
    *   After dependencies are installed (e.g., within the running Docker container or after a local `composer install`), generate migration files using `php spark make:migration <MigrationName>`.
7.  **Run Database Migrations:**
    *   `php spark migrate` (inside the Docker container or local CI4 environment).
8.  **Commit and Push:**
    *   `git add .`
    *   `git commit -m "feat: setup docker and database migrations"`
    *   `git push origin main`

### Pitfalls:
*   **`composer create-project` in non-empty directory:** Avoid running `create-project` directly in a cloned (non-empty) git repository. Scaffold into a temporary directory and then move files.
*   **Missing `ext-intl`:** CodeIgniter 4 requires `php-intl` extension. Ensure it's installed in the Dockerfile or local PHP environment.
*   **Git Authentication Issues:** Always run `gh auth setup-git` if `git push` fails due to credential issues with `gh CLI`.

