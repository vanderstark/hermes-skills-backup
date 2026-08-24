# OSINT Tools Catalog — Open Source & Paid

Reference for OSINT tool selection. Updated from session 2026-08-21.

---

## 🟢 Open Source (Free) — GitHub Repositories

| Tool | Purpose | GitHub | Install |
|------|---------|--------|---------|
| **SpiderFoot** | Automated recon, 200+ modules | https://github.com/smicallef/spiderfoot | `git clone --depth=1 ... && pip install -r requirements.txt` |
| **theHarvester** | Email, subdomain, host enum | https://github.com/laramies/theHarvester | `git clone --depth=1 ... && pip install -r requirements.txt` |
| **Sherlock** | Username search 400+ sites | https://github.com/sherlock-project/sherlock | `pip install sherlock-project` |
| **Maltego CE** | Visual link analysis (CE) | https://github.com/paterva/maltego-ce | Download from site |
| **Recon-ng** | Modular recon framework | https://github.com/lanmaster53/recon-ng | `git clone ... && pip install -r requirements.txt` |
| **Photon** | Fast web crawler | https://github.com/s0md3v/Photon | `git clone ... && pip install -r requirements.txt` |
| **ExifTool** | Metadata extraction | https://github.com/exiftool/exiftool | `pip install exiftool` (Perl) |
| **Amass** | Subdomain enum & attack surface | https://github.com/owasp-amass/amass | `go install -v github.com/owasp-amass/amass/v4/...@master` |
| **Holehe** | Email registration check | https://github.com/megadose/holehe | `pip install holehe` |
| **PhoneInfoga** | Phone number intel | https://github.com/PhoneInfoga/PhoneInfoga | `go install ...` or Docker |
| **Sublist3r** | Subdomain enum via search engines | https://github.com/aboul3la/Sublist3r | `git clone ... && pip install -r requirements.txt` |
| **GHunt** | Google account investigation | https://github.com/mxrch/GHunt | `pip install ghunt` |
| **Osintgram** | Instagram recon | https://github.com/Datalux/Osintgram | `git clone ... && pip install -r requirements.txt` |
| **Metagoofil** | Metadata from public docs | https://github.com/laramies/metagoofil | `git clone ... && pip install -r requirements.txt` |

---

## 🔴 Paid / Enterprise Tools

| Tool | Purpose | Pricing (est.) |
|------|---------|----------------|
| **Maltego Pro** | Advanced link analysis | ~$999/yr |
| **Shodan** | Internet-connected device search | $59 lifetime – $899/mo |
| **Censys** | Asset mapping & SSL certs | $99+/mo |
| **Hunter.io** | Email finder & verifier | $49+/mo |
| **Babel X** | Multi-lang deep/dark web search | Enterprise |
| **Skopenow** | Automated investigation & risk | Enterprise |
| **Social Links** | Maltego transforms (500+ sources) | Enterprise |
| **Intelligence X** | Archive & darknet search | €99+/mo |
| **SpyCloud** | Credential leak detection (ATO) | Enterprise |
| **Cobwebs** | Web intelligence for LE | Enterprise |

---

## ⚖️ Legal Boundaries (Indonesia Context)

**Authorized Use Only:**
- Written permission + security research
- Institution-approved academic
- Law enforcement with warrant
- Bug bounty (within scope)
- Public source collection

**Prohibited:**
- UU ITE Pasal 30 violations (unauthorized access)
- UU PDP violations (personal data protection)
- Doxxing, stalking, harassment
- Dark web sources without authorization
- Credential misuse

---

## 🐳 Quick Docker Deployment Pattern

```yaml
# docker-compose.yml for OSINT stack
version: '3.8'
services:
  spiderfoot:
    image: smicallef/spiderfoot:latest
    ports: ["5001:5001"]
    volumes: ["./data:/home/spiderfoot/data"]
  redis:
    image: redis:7-alpine
    volumes: ["redis-data:/data"]
volumes:
  redis-data:
```

Run: `docker compose up -d` → SpiderFoot at `http://localhost:5001`

---

## 📝 Session Notes (2026-08-21)

- Created `osint-toolkit` repo with README, Dockerfile, docker-compose.yml
- Pushed to `vanderstark/osint-toolkit` (public)
- User prefers: autonomous git push, Indonesian language, RAPI tables, 3x 🙏
- GitHub PAT embedded in remote URL for headless push: `https://$TOKEN@github.com/...`