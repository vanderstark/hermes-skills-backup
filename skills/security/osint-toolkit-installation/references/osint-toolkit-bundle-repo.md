# OSINT Toolkit Bundle Repository Pattern

Documented from session 2026-08-21: user asked to create a new GitHub repo containing
all open-source OSINT tools as a curated bundle with Docker deployment, tutorials,
and usage guides — then push it.

## Repository Created

**Repo:** `vanderstark/osint-toolkit`
**URL:** https://github.com/vanderstark/osint-toolkit

## Files in Bundle

| File | Purpose |
|------|---------|
| `README.md` | Full tutorial: tools list, legal notice, Docker & local install, usage examples per tool, backup instructions, license |
| `Dockerfile` | SpiderFoot web UI container (port 5001) |
| `docker-compose.yml` | One-command deploy: `docker-compose up -d` |

## Tools Covered (14)

| Tool | GitHub | Purpose |
|------|--------|---------|
| SpiderFoot | https://github.com/smicallef/spiderfoot | 200+ recon modules, web UI |
| theHarvester | https://github.com/laramies/theHarvester | Email/subdomain enumeration |
| Sherlock | https://github.com/sherlock-project/sherlock | Username tracking 400+ sites |
| Maltego CE | https://github.com/paterva/maltego-ce | Visual link analysis |
| Recon-ng | https://github.com/lanmaster53/recon-ng | Modular recon framework |
| Photon | https://github.com/s0md3v/Photon | Fast web crawler |
| ExifTool | https://github.com/exiftool/exiftool | Metadata extraction |
| Amass | https://github.com/owasp-amass/amass | Attack surface mapping |
| Holehe | https://github.com/megadose/holehe | Email registration check |
| PhoneInfoga | https://github.com/PhoneInfoga/PhoneInfoga | Phone number intelligence |
| Sublist3r | https://github.com/aboul3la/Sublist3r | Subdomain enumeration |
| GHunt | https://github.com/mxrch/GHunt | Google account investigation |
| Osintgram | https://github.com/Datalux/Osintgram | Instagram recon |
| Metagoofil | https://github.com/laramies/metagoofil | Document metadata extraction |

## Deployment Pattern (Validated)

```bash
# User clone + deploy in 3 minutes
git clone https://github.com/vanderstark/osint-toolkit.git
cd osint-toolkit
docker-compose up -d
# SpiderFoot web UI → http://localhost:5001
```

Other tools run via `docker exec -it osint-toolkit /bin/bash` then CLI inside container.

## Push Workflow (using github-token-deploy-workflow skill)

1. Create repo via API with PAT
2. `git init --initial-branch=main` locally
3. Add all files, commit, push with token in remote URL
4. **Immediately** strip token from remote URL (`git remote set-url origin https://...`)
5. Verify via Contents API
6. Clean temp files and unset token

## Legal Boundary Reminder (user context: Indonesia Polri)

All tools for **authorized use only** — UU ITE Pasal 30, UU PDP, GDPR. User requires
3x 🙏 per message, Indonesian language, "Bos" address, RAPI markdown tables.
This bundle repo follows same conventions.

## When to Reuse This Pattern

- User asks for "tools bundle repo" with Docker + tutorials
- Need to curate a set of tools into a deployable package
- OSINT/red-team/blue-tool collections for police/academy labs