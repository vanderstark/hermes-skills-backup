---
name: spiderfoot-docker-tutorial
description: SpiderFoot Docker OSINT.
category: devops
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# SpiderFoot Docker Tutorial Skill

**Trigger:** Use when user wants SpiderFoot Docker setup.

**Purpose:** Provide a complete, ready-to-use Docker setup for SpiderFoot with all configuration, deployment steps, and usage guidelines.

## Prerequisites

- Docker and Docker Compose installed
- Internet access for source data collection
- Approximately 512MB RAM minimum

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/vanderstark/spiderfoot-docker-tutorial.git
cd spiderfoot-docker-tutorial

# 2. Start the container
docker-compose up -d --build

# 3. Access the web interface
# Open your browser to: http://localhost:5000
```

## Docker Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  spiderfoot:
    image: smicallef/spiderfoot
    container_name: spiderfoot
    restart: unless-stopped
    environment:
      - SF_EMAIL=admin@yourdomain.com
      - SF_PASSWORD=***
      - SF_CONSOLE_PORT=5000
    ports:
      - "5000:5000"
    volumes:
      - spiderfoot_data:/data

volumes:
  spiderfoot_data:
```

### Environment Variables (.env)

Copy `.env` example and customize:

```env
SF_EMAIL=your_email@example.com
SF_PASSWORD=YourStrongPassword123!
```

## Web Interface Usage

### Access

- **URL:** `http://localhost:5000`
- **Default Credentials:** Check `docker logs spiderfoot` for email/password

### Adding Targets

1. Navigate to **Add Target** section
2. Enter domain, IP, or subdomain
3. SpiderFoot will automatically start scanning using its 400+ modules

### Configuring Modules

Go to **Management → Modules** to enable/disable specific scanning modules:

| Category | Example Modules |
|----------|----------------|
| Network | `SF portscan`, `SF nmap` |
| SSL/TLS | `SF ssl`, `SF certificate` |
| Email | `SF phishing`, `SF email` |
| Malware | `SF malw`, `SF virustotal` |
| Social | `SF twitter`, `SF linkedin` |

### Viewing & Exporting Results

- Results appear in real-time under the **Results** tab
- Export to JSON, CSV, or HTML format
- View detailed findings per module
- Correlate data across different scanning sources

## Use Cases

### Corporate Security Assessment

```bash
# Add target: company-domain.com
# Enable modules: SF phishing, SF malw, SF ssl
# Export findings for risk assessment
```

### Incident Response

```bash
# Investigate suspicious IP/domain
# Correlate with existing threat intelligence
# Generate IOC (Indicators of Compromise) reports
```

### Asset Discovery

```bash
# Map entire subnet or organization's digital footprint
# Discover forgotten subdomains and services
# Identify exposed credentials and certificates
```

## Security Best Practices

1. Never expose SpiderFoot to public internet without proper authentication
2. Use strong, unique passwords for the web console
3. Regularly update the Docker image for security patches
4. Firewall access - restrict port 5000 to trusted IPs only
5. Audit logs - review console activity periodically
6. Data privacy - be aware of local regulations regarding OSINT collection

## Updates & Maintenance

### Update to Latest Version

```bash
docker-compose down
docker-compose pull
docker-compose up -d --build
```

### Backup Strategy

```bash
# Daily/weekly backup of SpiderFoot data
docker cp spiderfoot:/.sf_data /path/on/host/sf_backup_$(date +%Y%m%d).dump
```

### Log Management

```bash
# View real-time logs
docker logs -f spiderfoot

# Log to file for analysis
docker logs spiderfoot > spiderfoot.log 2>&1
```

## License

SpiderFoot is open-source software developed by [smicallef](https://github.com/smicallef) and distributed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

This skill is provided for educational and operational purposes.

## Integration with Hermes Agent

When using Hermes Agent for OSINT tasks:

1. Always check Docker availability before starting SpiderFoot
2. Use `docker-compose` commands for setup and management
3. Integrate scan results into Hermes workflows for threat intelligence
4. Export findings to shared knowledge bases or team repositories

---

**Last Updated:** current session date

**Author:** Hermes Agent - Nous Research

**Related Skills:** github-workflow-preferences, hermes-agent, devops related skills