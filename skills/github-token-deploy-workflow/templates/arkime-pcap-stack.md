# Arkime Full Packet Capture Stack Template

Arkime (formerly Moloch): full packet capture (PCAP) + metadata indexing to Elasticsearch. Use for forensic replay when incidents occur — Zeek/Suricata tell you WHAT happened, Arkime stores the RAW PROOF.

## Docker Compose

```yaml
services:
  arkime-master:
    image: arkime/arkime:latest
    container_name: arkime-master
    restart: unless-stopped
    network_mode: host
    environment:
      ARKIME_ELASTICSEARCH: http://localhost:9200
      ARKIME_INTERFACE: eth0
      ARKIME_ADMIN_PASSWORD: ${ARKIME_ADMIN_PASSWORD:-changeme}
      ARKIME_LOCALE: en_US.UTF-8
    volumes:
      - arkime-pcap:/opt/arkime/raw
      - arkime-logs:/opt/arkime/logs
    depends_on:
      es-arkime:
        condition: service_healthy
    sysctls:
      - net.core.rmem_max=26214400
      - net.core.wmem_max=26214400

  es-arkime:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    container_name: arkime-elasticsearch
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms4g -Xmx4g
      - cluster.name=arkime
      - bootstrap.memory_lock=true
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - arkime-es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  viewer:
    image: arkime/arkime:latest
    container_name: arkime-viewer
    restart: unless-stopped
    ports:
      - "8005:8005"
    environment:
      ARKIME_ELASTICSEARCH: http://localhost:9200
      ARKIME_VIEWER_PORT: 8005
      ARKIME_LOCALE: en_US.UTF-8
    depends_on:
      es-arkime:
        condition: service_healthy
    networks:
      - arkime-net

  filebeat-arkime:
    image: docker.elastic.co/beats/filebeat:8.15.0
    container_name: arkime-filebeat
    restart: unless-stopped
    volumes:
      - arkime-logs:/var/log/arkime:ro
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    depends_on:
      es-arkime:
        condition: service_healthy
    networks:
      - arkime-net

networks:
  arkime-net:
    driver: bridge

volumes:
  arkime-pcap:
  arkime-logs:
  arkime-es-data:
```

## CRITICAL: Storage Planning

Full packet capture eats disk FAST:

| Traffic | Storage/Day | 7-Day Retention |
|---------|-------------|-----------------|
| 100 Mbps | ~1 TB | ~7 TB |
| 1 Gbps | ~10 TB | ~70 TB |

**Recommendations:**
- Short retention (1-3 days) or selective capture (only critical interfaces/VLANs)
- Keep metadata (Elasticsearch) long-term, raw PCAP short-term
- Auto-rotation cron on host:
  ```bash
  0 2 * * * find /var/lib/docker/volumes/arkime_arkime-pcap/_data -name "*.pcap" -mtime +7 -delete
  ```

## Viewer Usage

- URL: `http://IP:8005`, login admin / password from .env
- Search by IP, port, protocol, time
- Click session → "View Packets" for raw payload replay
- Export to PCAP for Wireshark analysis

## Security & Compliance Notes

- PCAP contains RAW PAYLOAD — may include passwords, PII (GDPR/UU PDP compliance!)
- Restrict viewer access to trusted admins only
- PCAP stored locally, never sent off-box
- For police academy lab: valuable as forensic evidence training data