# Database Tuning Parameters Reference

Values used across all monolith & Docker tuning scripts. Adjust based on user feedback or hardware.

---

## MySQL / MariaDB

| Parameter | Formula / Value | Notes |
|-----------|-----------------|-------|
| `innodb_buffer_pool_size` | 70% RAM | Core parameter; largest impact on read perf |
| `innodb_buffer_pool_instances` | CPU_CORES / 2 (min 1) | Reduce contention on high-core servers |
| `innodb_log_file_size` | 512MB | Fixed; balance between recovery time & write throughput |
| `max_connections` | CPU_CORES * 50 (min 200) | Connection overhead; test under load |
| `thread_cache_size` | 100 | Reuse threads; reduce creation overhead |
| `sort_buffer_size` | 4MB | Per-query buffer; tune if many sorts |
| `query_cache_size` | 256MB or 0 | MySQL 8.0 removed it; set 0 if not needed |
| `slow_query_log` | ON | threshold 2000ms (1 parameter not configured, just enabled) |
| `key_buffer_size` | 64MB | MyISAM only; use innodb_buffer_pool for InnoDB |

---

## PostgreSQL

| Parameter | Formula / Value | Notes |
|-----------|-----------------|-------|
| `shared_buffers` | 25% RAM | PostgreSQL shared cache; smaller than MySQL proportionally |
| `effective_cache_size` | 50% RAM | Optimizer hint; not actual allocation |
| `work_mem` | 8 + (CPU_CORES * 2) MB | Per-query sort/hash buffer; cumulative under high concurrency |
| `maintenance_work_mem` | 5% RAM | VACUUM, CREATE INDEX, ALTER TABLE |
| `max_connections` | CPU_CORES * 20 (capped 500) | Reserve 10 for superuser |
| `max_wal_size` | CPU_CORES * 16 MB | Checkpoint interval; higher = fewer checkpoints |
| `min_wal_size` | CPU_CORES * 4 MB | Don't shrink below this |
| `checkpoint_completion_target` | 0.9 | Spread checkpoint I/O over 90% of interval |
| `log_min_duration_statement` | 2000 ms | Log queries slower than 2 seconds |
| `autovacuum` | ON | Essential for long-running servers |

---

## MongoDB

| Parameter | Formula / Value | Notes |
|-----------|-----------------|-------|
| WiredTiger `cacheSizeGB` | 50% RAM (max 10GB) | In-memory storage engine cache |
| `maxIncomingConnections` | CPU_CORES * 100 (capped 65535) | TCP connections to mongod |
| `journal` / compression | snappy | Reduce disk I/O; ~50% compression ratio |
| `oplogSizeMB` | 4096 | Fixed; large enough for replication lag |
| `slowOpThresholdMs` | 2000 | Log operations slower than 2 seconds |
| `directoryForIndexes` | false | Keep index in default data dir (simpler) |
| `checkpointSizeMB` | 2000 | WiredTiger checkpoint size; balance memory vs I/O |

---

## Redis

| Parameter | Formula / Value | Notes |
|-----------|-----------------|-------|
| `maxmemory` | 70% RAM | Trigger eviction at this limit |
| `maxmemory-policy` | `allkeys-lru` | Evict least-recently-used key when full |
| `maxmemory-samples` | 5 | Sampling for LRU approximation (higher = more accurate, slower) |
| `maxclients` | 10000 | Max connected clients |
| `tcp-backlog` | 511 | TCP listen backlog (system limit often 65535) |
| `timeout` | 0 | No client timeout (keep connections alive) |
| `appendonly` | yes | Enable AOF (Append Only File) for persistence |
| `appendfsync` | `everysec` | Fsync every second (balance durability vs performance) |
| `slowlog-log-slower-than` | 2000 µs | Log commands slower than 2ms |
| `slowlog-max-len` | 128 | Keep last 128 slow commands |
| `hz` | 10 | Background tasks frequency (sampling, keyspace notifications) |

---

## Web Servers (Apache / Nginx)

### Apache

| Parameter | Value | Notes |
|-----------|-------|-------|
| `MaxRequestWorkers` | CPU_CORES * 2 to 4 | Concurrent requests; test under load |
| `KeepAlive` | On | Reuse TCP connections |
| `KeepAliveTimeout` | 5 seconds | Brief; TCP reuse without hanging |
| `MaxKeepAliveRequests` | 100 | Requests per connection |
| `ServerLimit` | CPU_CORES * 2 | Max processes; memory-gated |
| `StartServers` | CPU_CORES | Initial processes to spawn |

### Nginx

| Parameter | Value | Notes |
|-----------|-------|-------|
| `worker_processes` | CPU_CORES or `auto` | One per core; autodetect in nginx.conf |
| `worker_connections` | 8192 (or 4096 for low-mem) | Connections per worker |
| `keepalive_timeout` | 65 seconds | TCP reuse duration |
| `client_body_buffer_size` | 256KB | Upload buffer; tune if large POSTs |
| `gzip` | on | Compress responses (CPU trade-off) |
| `gzip_min_length` | 1KB | Only compress responses > 1KB |

---

## Kernel Parameters (All Databases / Web Servers)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `net.core.somaxconn` | 65535 | TCP listen backlog (global) |
| `net.ipv4.tcp_max_syn_backlog` | 8192 | SYN flood protection |
| `fs.file-max` | 2,097,152 (2M) | Process file descriptor limit |
| `fs.aio-max-nr` | 1,048,576 (1M) | Async I/O max threads |
| `net.ipv4.tcp_fin_timeout` | 15 | TIME_WAIT duration (reduce TIME_WAIT buildup) |
| `net.ipv4.tcp_tw_reuse` | 1 | Reuse TIME_WAIT sockets (safe with timestamps) |

---

## Ulimit / Security Limits

```bash
# All services get same baseline
<user> soft nofile  65535
<user> hard nofile  65535
<user> soft nproc   32768    # or higher for high-concurrency
<user> hard nproc   32768
```

---

## Notes for Future Tuning

- **Trade-offs:** Larger buffers = more memory, faster reads; fewer processes = lower CPU, less contention.
- **Test under load:** Tune values empirically, not by rule. Run benchmarks before & after.
- **Monitor:** Check logs for slow queries, evictions, connection saturation.
- **Reversion:** All scripts auto-backup; rollback by copying backup + restart.
