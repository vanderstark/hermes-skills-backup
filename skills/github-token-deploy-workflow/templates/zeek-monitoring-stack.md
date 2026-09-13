# Zeek Network Monitoring Stack Template

Use this as a starter for network behavior monitoring (NSM) deployments. Complements Suricata (signature-based) with protocol-level behavioral analysis.

## Docker Compose

```yaml
services:
  zeek:
    image: zeek/zeek:latest
    container_name: zeek
    restart: unless-stopped
    network_mode: host
    environment:
      ZEEK_MODE: live
      ZEEK_INTERFACE: eth0
      ZEEK_JSON: "yes"
    volumes:
      - zeek-logs:/opt/zeek/logs
      - zeek-scripts:/opt/zeek/share/zeek/site:ro
    command: >
      sh -c "cd /opt/zeek && ./bin/zeek -i $ZEEK_INTERFACE
             local.zeek Log::default_rotation_interval=1hr"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - zeek-net

  filebeat-zeek:
    image: docker.elastic.co/beats/filebeat:8.15.0
    container_name: zeek-filebeat
    restart: unless-stopped
    volumes:
      - zeek-logs:/var/log/zeek:ro
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    depends_on:
      - zeek
    networks:
      - zeek-net

networks:
  zeek-net:
    driver: bridge

volumes:
  zeek-logs:
  zeek-scripts:
```

## Filebeat Config (Optional ELK Shipping)

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/zeek/*.log
    json.keys_under_root: true
    json.add_error_key: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "zeek-%{[agent.version]}"
```

## Key Config Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ZEEK_MODE` | `live` | `live` = real traffic, `pcap` = offline file |
| `ZEEK_INTERFACE` | `eth0` | Interface to monitor — change per host |
| `ZEEK_JSON` | `yes` | JSON output for ELK pipeline |

## Deployment Notes

- Requires `network_mode: host` + root/privileged for interface access
- Best on SPAN/mirror port, not primary production interface
- Log rotation: 1 hour (configurable via `Log::default_rotation_interval`)
- Output logs: `conn.log`, `dns.log`, `http.log`, `ssl.log`, `ssh.log`, `notice.log`, `weird.log`
- Pair with Suricata: Suricata = signature alerts, Zeek = behavioral context

## Integration with Existing Stack

- Filebeat → Elasticsearch → Grafana/Kibana dashboards
- Zeek `notice.log` → Wazuh/CrowdSec for auto-blocking
- `conn.log` metadata → LibreNMS/Zabbix for network visibility