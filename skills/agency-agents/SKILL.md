---
name: agency-agents
description: Reference library of 300+ AI agent personas and roles.
category: reference-library
tags: [reference, agent-personas, ai-agents, roles, disciplines]
---

# Agency Agents - AI Agent Persona Library

**Deskripsi:** Koleksi lengkap 300+ persona agen AI agent untuk berbagai disiplin profesional, bidang riset, dan peran kriptografus.

## Cara Menggunakan

Repository ini berisi file Markdown (`.md`) untuk setiap persona. Setiap file mewakili seorang agen AI dengan:
- Background profesional
- Kompetensi kunci
- Pendekatan kerja
- Statistik keberhasilan (jika ada)

**Untuk menggunakan:**
1.  Baca file yang relevan dengan `read_file(path: "/opt/data/skills/agency-agents/<category>/<agent-name>.md")`
2.  Sebagai referensi saat merancang prompt agen
3.  Untuk riset atau analisis disiplin tertentu

## Kategori Tersedia

### Disiplin Utama
- **academic/** - Akademisi (5 agent): anthropologist, geographer, historian, narratologist, psychologist, statistician
- **design/** - Desainer (10 agent): brand-guardian, image-prompt-engineer, inclusive-visuals-specialist, persona-walkthrough, ui-designer, ui-finish-gate-reviewer, ux-architect, ux-researcher, visual-storyteller, whimsy-injector
- **engineering/** - Injeneer (70+ agent): AI, backend, frontend, DevOps, database, frontend, mobile, cloud, security, data, dan banyak lagi
- **finance/** - Keuangan
- **game-development/** - Pengembangan Game
- **gis/** - GIS
- **healthcare/** - Kesehatan
- **integrations/** - Integrasi AI (hermes, claude-code, cursor, github-copilot, opencode, vibe, dll.)

### Kategori Lainnya
- **marketing/**
- **paid-media/**
- **product/**
- **project-management/**
- **research/**
- **security/**
- **specialized/**
- **strategy/**
- **support/**
- **testing/**

## Contoh Penggunaan

```python
# Baca persona engineer
content = read_file(path="/opt/data/skills/agency-agents/engineering/engineering-ai-engineer.md")
# Gunakan sebagai reference untuk merancang prompt
```

## Catatan Penting

-   Ini **bukan skill executable** - hanya koleksi referensi
-   Gunakan `search_files()` untuk mencari agent spesifik
-   File `.md` dapat langsung dibaca oleh model untuk konteks

## License

Lihat LICENSE di repository sumber: https://github.com/msitarzewski/agency-agents