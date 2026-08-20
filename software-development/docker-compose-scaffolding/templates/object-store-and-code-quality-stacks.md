# Self-Hosted Object Store & Code Quality Docker Stacks

Two common self-hosted stack recipes produced with the one-repo-per-tool
pattern (`<tool>-docker-compose`). Both published cleanly with the
`github-token-deploy-workflow` push path.

## MinIO (S3-compatible object storage)

Single-service stack: server + web console + auto-init bucket sidecar.
Pin the version via the GitHub Releases API
(`https://api.github.com/repos/minio/minio/releases/latest`) rather than
guessing, then write `minio/minio:<TAG>`.

Key compose shape:
```yaml
services:
  minio:
    image: minio/minio:<TAG>
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
      MINIO_SERVER_URL: ${MINIO_SERVER_URL:-http://localhost:9000}
      MINIO_BROWSER_REDIRECT_URL: ${MINIO_BROWSER_REDIRECT_URL:-http://localhost:9001}
    ports: ["9000:9000", "9001:9001"]   # 9000 = S3 API, 9001 = console
    volumes: [minio_data:/data]
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
    restart: unless-stopped
  # auto-create bucket on first run (sidecar, exits after)
  minio-init:
    image: minio/mc:latest
    depends_on: { minio: { condition: service_healthy } }
    entrypoint: >
      /bin/sh -c "
      mc alias set local http://minio:9000 $${MINIO_ROOT_USER:-minioadmin} $${MINIO_ROOT_PASSWORD:-minioadmin};
      mc mb -p local/$${MINIO_BUCKET:-mybucket} || true;
      "
    restart: "no"
volumes:
  minio_data:
```

Notes / pitfalls:
- **`$${...}` not `${...}`** inside the container `entrypoint` string — the
  compose interpolates your `.env` on your host, `$$` escapes the literal
  `$` that reaches the container's shell so `MINIO_ROOT_*` resolves
  inside the container. Getting this wrong silently creates buckets with
  wrong creds.
- Healthcheck relies on `mc` being present in the `minio/minio` image
  (it is).
- Two ports: **9000** S3 API, **9001** console — clearly label both in
  README.

## SonarQube Community (code quality & security)

Server + Postgres 17 database. `sonarqube:lts-community` is the stable
image. Depends-on-healthy DB avoids the classic race where the app starts
before Postgres is ready.

```yaml
services:
  sonarqube:
    image: sonarqube:lts-community
    depends_on: { db: { condition: service_healthy } }
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonarqube
      SONAR_JDBC_USERNAME: ${SONAR_DATABASE:-sonar}
      SONAR_JDBC_PASSWORD: ${SONAR_DB_PASSWORD:-sonar}
    ports: ["9000:9000"]
    volumes: [sonarqube_data, sonarqube_extensions, sonarqube_logs]
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: ${SONAR_DATABASE:-sonar}
      POSTGRES_PASSWORD: ${SONAR_DB_PASSWORD:-sonar}
      POSTGRES_DB: sonarqube
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
```

### CRITICAL host requirement — ElasticSearch
SonarQube bundles Elasticsearch and **fails to start** unless the host has:
```
sudo sysctl -w vm.max_map_count=524288   # persist via /etc/sysctl.conf
```
Put this at the TOP of the README Troubleshooting so it's not buried —
it is the #1 "why won't it start" failure for SonarQube on Linux.

Other README must-haves:
- Default login `admin / admin` — flag to change on first login.
- Project-token flow + scanner examples (Maven / `sonar-scanner` /
  `npx sonar-scanner`).
- GitHub Actions `sonarqube-community/sonarqube-scan-action@v2` snippet.