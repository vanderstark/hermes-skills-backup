# MinIO Object Storage — Docker Compose Pattern

Reusable stack for self-hosted **S3-compatible object storage** in the one-repo-per-tool
series (repo naming: `minio-docker-compose`). MinIO ships both a S3 API port and a
separate web-console port, plus a companion `mc` CLI image for healthchecking and
bucket bootstrap.

## Compose skeleton (verified shape)

```yaml
services:
  minio:
    image: minio/minio:RELEASE.2025-10-15T17-29-55Z   # pin a real release tag, not :latest
    container_name: minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
      MINIO_SERVER_URL: ${MINIO_SERVER_URL:-http://localhost:9000}
      MINIO_BROWSER_REDIRECT_URL: ${MINIO_BROWSER_REDIRECT_URL:-http://localhost:9001}
    ports:
      - "9000:9000"   # S3 API
      - "9001:9001"   # Web Console
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 20s
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # One-shot sidecar: waits for minio healthy, then ensures the default bucket exists.
  minio-init:
    image: minio/mc:latest
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
      mc alias set local http://minio:9000 $${MINIO_ROOT_USER:-minioadmin} $${MINIO_ROOT_PASSWORD:-minioadmin};
      mc mb -p local/$${MINIO_BUCKET:-mybucket} || true;
      exit 0;
      "
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
      MINIO_BUCKET: ${MINIO_BUCKET:-mybucket}
    restart: "no"

volumes:
  minio_data:
```

## Key facts / pitfalls

- **Two ports**: 9000 = S3 API (boto3 / AWS SDK / `mc`), 9001 = web console. The
  console is a *separate* `--console-address` server, not the same port.
- **Healthcheck** uses `mc ready local` (the `mc` binary ships in the server image)
  — not a TCP/wget probe. `depends_on.condition: service_healthy` on the init sidecar
  correctly gates bucket creation on server readiness.
- **Env vars**: `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` set root creds at first start
  (defaults `minioadmin`/`minioadmin` — must be changed in `.env` for prod). 
  `MINIO_SERVER_URL` / `MINIO_BROWSER_REDIRECT_URL` define the public URLs used by the
  console redirect when exposed behind a reverse proxy.
- **Auto-init bucket**: `mc mb -p` is idempotent; wrap in `|| true` so re-create on
  restart doesn't fail the sidecar.
- **Never git-add `.env`** with the real password. Ship `.env.example` with a strong
  placeholder + `.gitignore` excluding `.env` (standard `generate-env.sh` pattern applies).
- **Client example** for users: `boto3` with `endpoint_url=http://localhost:9000`
  (endpoint_url is the one mandatory non-default arg for S3-compatible MinIO).
- Verify the `minio/minio` image tag actually exists (GitHub release API
  `/repos/minio/minio/releases/latest` → tag name) before pinning, per the
  "verify every third-party image" rule.