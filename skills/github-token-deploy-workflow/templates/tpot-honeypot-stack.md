# T-Pot Honeypot Platform Stack Template

T-Pot by Deutsche Telekom: 20+ honeypots in one Docker platform (Cowrie SSH/Telnet, Dionaea SMB/FTP/MySQL, Conpot ICS/SCADA, Heralding, Mailoney, etc). All data → Elasticsearch + Kibana + TheHive.

## Docker Compose

```yaml
services:
  tpot:
    image: ghcr.io/telekom-security/tpotce:latest
    container_name: tpot
    restart: unless-stopped
    ports:
      - "64297:64297"    # T-Pot Management UI
      - "2222:2222"      # Cowrie SSH
      - "8080:8080"      # Dionaea HTTP
      - "5900:5900"      # Dionaea VNC
      - "3306:3306"      # Dionaea MySQL
      - "4444:4444"      # Dionaea SMB
      - "8443:8443"      # Heralding fake HTTPS
      - "10000:10000"    # Attacker tracking
    environment:
      - TPOT_TOKEN=${TPOT_TOKEN:-changeme}
    volumes:
      - tpot-data:/opt/tpot
      - tpot-logs:/var/log/suricata
      - ./tpot.conf:/opt/tpot/etc/tpot.conf:ro
    networks:
      - tpot-net
      - ai-network
    cap_add:
      - NET_ADMIN
      - NET_RAW
    sysctls:
      - net.ipv4.ip_forward=1

  es-tpot:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    container_name: tpot-elasticsearch
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms2g -Xmx2g
      - cluster.name=tpot
    volumes:
      - tpot-es-data:/usr/share/elasticsearch/data

  kibana-tpot:
    image: docker.elastic.co/kibana/kibana:8.15.0
    container_name: tpot-kibana
    restart: unless-stopped
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://tpot-elasticsearch:9200
      - xpack.security.enabled=false
    depends_on:
      es-tpot:
        condition: service_healthy

  hive-tpot:
    image: thehiveproject/thehive4:latest
    container_name: tpot-thehive
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      - APP_SECRET=${THEHIVE_SECRET:-RandomSecretKey}
      - DATABASE_PROVIDER=local
      - DATABASE_LOCAL_DIRECTORY=/opt/thp/thehive/db
      - PLAY_HTTP_SECRET_KEY=${THEHIVE_SECRET:-RandomSecretKey}
    volumes:
      - tpot-hive-data:/opt/thp/thehive/db
    depends_on:
      es-tpot:
        condition: service_healthy

networks:
  tpot-net:
    driver: bridge
  ai-network:
    external: true
    name: ai-network

volumes:
  tpot-data:
  tpot-logs:
  tpot-es-data:
  tpot-hive-data:
```

## Honeypot Port Map

| Honeypot | Port | Target |
|----------|------|--------|
| Cowrie | 2222 | SSH, Telnet |
| Dionaea | 4444, 3306, 8080 | SMB, MySQL, HTTP |
| Conpot | 80/443 | ICS/SCADA |
| Heralding | 8443 | Fake login pages |
| Mailoney | 25 | SMTP |

## Deployment Notes

- **Do NOT run honeypot ports on same ports as production services** — port conflict
- **Do NOT expose honeypot directly to internet without firewall/DMZ** — use monitoring layer
- Kibana index pattern: `tpot-*`
- Elasticsearch data count check:
  ```bash
  curl -s "http://localhost:9200/tpot-*/_count" | python3 -c "import json,sys;print(json.load(sys.stdin)['count'])"
  ```
- Integrate with Wazuh: add rule to monitor honeypot logs as attack signals
- Data feeds CrowdSec for auto-ban of attacker IPs

## TheHive Incident Response

- TheHive = case management for IR — useful for police academy lab (simulate investigations)
- Default port 9000, secrets via `THEHIVE_SECRET` env
- Requires Elasticsearch healthy before start (depends_on condition)