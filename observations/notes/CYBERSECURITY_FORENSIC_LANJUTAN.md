# 🔒 Cybersecurity & Forensic Lanjutan: Malware Analysis & Digital Forensics

**Ditulis:** 24 Agustus 2026  
**Kategori:** Cybersecurity & Forensic (Lanjutan)  
**Target User:** Bos (Polri — Intelkam, Reskrim, polsek/academy AI/OSINT lab)  
**Bahasa:** Indonesian (Bahasa Indonesia)

---

## 🎯 Ringkasan

Setelah menguasai skill dasar (Docker CTF Labs), tahap lanjutan fokus pada **kemampuan forensik digital nyata** yang relevan untuk unit Reskrim & Intelkam Polri:
- Analisis malware (static & dynamic)
- Digital forensics (disk, memory, network)
- Incident response playbook
- Threat hunting & IOC (Indicator of Compromise) extraction

**Konteks operasional:** Polsek/academy AI/OSINT lab bisa menggunakan skill ini untuk **melatih penyidik siber** dan **membangun kapasitas forensik digital** untuk kasus cybercrime.

---

## 📚 Skill Roadmap: 3 Lapis Pembelajaran

### Tier 1: Dasar (Sudah Dikuasai)
- ✅ `hacking-labs-docker-ctf` — Build vulnerable Docker CTF labs untuk training

### Tier 2: Intermediate (Focus Sesi Ini)
- 🔷 `analyzing-memory-dumps-with-volatility` — RAM forensics (proses, network conn, registry cache)
- 🔷 `performing-malware-triage-with-yara` — Rapid malware classification via YARA rules
- 🔷 `analyzing-network-traffic-for-incidents` — PCAP analysis untuk deteksi C2, exfiltration
- 🔷 `extracting-iocs-from-malware-samples` — IOC extraction (hash, domain, IP) dari sample malware
- 🔷 `triaging-security-incident` — NIST-based initial incident triage
- 🔷 `building-incident-response-playbook` — Playbook untuk berbagai jenis insiden

### Tier 3: Advanced (Lanjutan)
- 🟦 `reverse-engineering-malware-with-ghidra` — Deep static analysis dengan Ghidra
- 🟦 `performing-disk-forensics-investigation` — Full disk imaging & recovery
- 🟦 `hunting-advanced-persistent-threats` — APT hunting berbasis MITRE ATT&CK
- 🟦 `analyzing-windows-event-logs-in-splunk` — Log correlation untuk investigasi

---

## 🔧 Core Workflow: Malware Analysis & Digital Forensics

### Fase 1: Triase Awal (First Response)
```
1. Isolasi sistem terinfeksi (network segmentation / air-gap)
2. Ambil volatile evidence (RAM dump) SEBELUM matikan sistem
3. Buat forensic image disk (bit-for-bit, write-blocker)
4. Catat chain of custody (siapa, kapan, bagaimana evidence diambil)
```

**Tools:** `acquiring-disk-image-with-dd-and-dcfldd`, `collecting-volatile-evidence-from-compromised-host`

### Fase 2: Static Analysis (Malware Sample)
```
1. Hash file (MD5, SHA-256) → cek reputasi via VirusTotal
2. Jalankan strings extraction (cari IP, domain, URL embedded)
3. PE header analysis (import table, section, compile time)
4. YARA rule matching untuk klasifikasi cepat
```

**Tools:** `performing-static-malware-analysis-with-pe-studio`, `performing-malware-triage-with-yara`, `performing-malware-hash-enrichment-with-virustotal`

### Fase 3: Dynamic Analysis (Sandbox)
```
1. Jalankan sample di sandbox terisolasi (Cuckoo/CAPE/ANY.RUN)
2. Monitor: file system changes, registry changes, network calls
3. Capture network traffic (PCAP) selama eksekusi
4. Identifikasi C2 server & komunikasi protokol
```

**Tools:** `performing-automated-malware-analysis-with-cape`, `performing-dynamic-analysis-with-any-run`, `analyzing-network-traffic-of-malware`

### Fase 4: Memory Forensics
```
1. Ambil memory dump dari sistem terinfeksi
2. Analisis proses aktif (Volatility: pslist, pstree)
3. Cari injected code / process hollowing
4. Extract credentials/artifacts dari memory
```

**Tools:** `analyzing-memory-dumps-with-volatility`, `detecting-process-injection-techniques`

### Fase 5: IOC Extraction & Threat Intel
```
1. Extract IOC: file hash, IP address, domain, registry key, mutex
2. Cross-reference ke threat intel feed (MISP, VirusTotal, AlienVault OTX)
3. Buat IOC report untuk sharing (STIX/TAXII format)
4. Update deteksi rules (Sigma, YARA) berdasarkan findings
```

**Tools:** `extracting-iocs-from-malware-samples`, `building-detection-rules-with-sigma`

### Fase 6: Incident Response & Reporting
```
1. Timeline reconstruction (kapan compromise terjadi, apa yang diakses)
2. Containment & eradication plan
3. Recovery verification (sistem bersih dari malware)
4. Lessons learned report + rekomendasi hardening
```

**Tools:** `building-incident-response-playbook`, `conducting-post-incident-lessons-learned`

---

## 📋 Template: Digital Forensics Investigation Report

```
LAPORAN INVESTIGASI FORENSIK DIGITAL
No. Laporan: [nomor kasus Polri]

1. RINGKASAN EKSEKUTIF
   - Jenis insiden (ransomware/data breach/APT/dll)
   - Sistem terdampak
   - Timeline singkat (kapan detect → kapan resolve)
   - Dampak (data loss, downtime, financial)

2. METODOLOGI
   - Standard yang digunakan (NIST SP 800-86, ISO 27037)
   - Chain of custody log
   - Tools yang digunakan (Volatility, Autopsy, Wireshark, dll)

3. TIMELINE KEJADIAN
   | Waktu | Event | Evidence Source |
   |-------|-------|-----------------|
   | T-0 | Initial compromise | Firewall log |
   | T+2h | Lateral movement | Windows Event Log |
   | T+5h | Data exfiltration | Network PCAP |

4. TEMUAN TEKNIS
   - Malware sample analysis (hash, family, behavior)
   - IOC list (IP, domain, file hash, registry key)
   - Attack vector (phishing, RDP brute-force, dll)
   - MITRE ATT&CK mapping (tactics, techniques used)

5. DAMPAK & KERUSAKAN
   - Sistem yang terinfeksi
   - Data yang terekspos/tercuri
   - Estimasi kerugian finansial

6. REKOMENDASI
   - Immediate: patch, isolasi, credential reset
   - Short-term: hardening, monitoring enhancement
   - Long-term: security awareness training, policy update

7. LAMPIRAN
   - Full IOC list
   - Screenshot evidence
   - Hash values semua file yang dianalisis
```

---

## 🎬 Use Cases (Real-World Polri Context)

### Skenario 1: Investigasi Ransomware di Instansi Pemerintah
Reskrim Polri menerima laporan ransomware attack di kantor dinas:
1. First response: isolasi jaringan, ambil RAM dump SEBELUM shutdown
2. Static analysis: identifikasi ransomware family (LockBit, Conti, dll)
3. Dynamic analysis: cek encryption method, C2 communication
4. IOC extraction: file hash ransom note, wallet address, C2 IP
5. Output: laporan forensik untuk barang bukti pengadilan + rekomendasi recovery

### Skenario 2: OSINT Lab Training untuk Penyidik Siber
Academy AI/OSINT lab ingin melatih penyidik baru:
1. Deploy Docker CTF lab dengan simulasi malware infection
2. Latih memory forensics: cari process injection di RAM dump
3. Latih network forensics: identifikasi C2 traffic di PCAP sample
4. Assessment: penyidik harus extract IOC lengkap dari skenario simulasi

### Skenario 3: Threat Intelligence untuk 170-Server DC
Bos ingin monitor apakah ada indikasi compromise di infrastruktur datacenter:
1. Setup YARA rules untuk scan file system secara berkala
2. Monitor network traffic untuk anomali (beaconing, unusual DNS query)
3. Cross-reference IOC dengan threat intel feed terbaru
4. Automated alert jika ditemukan match dengan known malware signature

---

## 💡 Key Insights & Pitfalls

### ✅ Best Practices

| Aspek | Best Practice |
|-------|---------------|
| **Order of Volatility** | Selalu ambil evidence dari yang paling volatile dulu: RAM → network state → disk → backup. |
| **Chain of Custody** | Dokumentasikan SETIAP langkah (siapa, kapan, hash sebelum/sesudah) — krusial untuk barang bukti pengadilan. |
| **Write-Blocker** | SELALU gunakan write-blocker saat imaging disk — jangan pernah analisis langsung di disk asli. |
| **Isolated Sandbox** | Jangan pernah jalankan malware sample di sistem produksi — selalu di sandbox terisolasi (air-gap/VM snapshot). |
| **Hash Verification** | Verify hash sebelum & sesudah setiap tahap analisis — pastikan integritas evidence tidak berubah. |

### ⚠️ Pitfalls (Hindari!)

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Matikan sistem sebelum ambil RAM dump | Kehilangan volatile evidence (proses aktif, network connections, encryption keys di memory) | SELALU ambil memory dump dulu sebelum shutdown/isolasi |
| Analisis malware di sistem yang terhubung internet | Malware bisa exfiltrate data atau menyebar ke sistem lain | Gunakan air-gapped sandbox, disable network kecuali untuk capture C2 traffic terkontrol |
| Skip chain of custody documentation | Evidence tidak bisa dipakai di pengadilan (dianggap tidak valid secara hukum) | Dokumentasikan setiap handling evidence dengan timestamp + signature |
| Terlalu fokus 1 tool | Miss detection karena setiap tool punya blind spot berbeda | Cross-validate findings dengan multiple tools (YARA + VirusTotal + sandbox behavior) |
| Tidak update YARA/Sigma rules | Miss deteksi varian malware baru | Update detection rules secara berkala berdasarkan threat intel terbaru |

---

## 🎓 Learning Path (6 Minggu)

### Minggu 1-2: Fundamentals & First Response
- [ ] Load skill: `collecting-volatile-evidence-from-compromised-host`
- [ ] Practice: simulasi first response (isolasi, RAM dump acquisition)
- [ ] Understand order of volatility & chain of custody
- [ ] **Deliverable:** SOP first response untuk lab OSINT academy

### Minggu 3: Static & Dynamic Malware Analysis
- [ ] Load skills: `performing-static-malware-analysis-with-pe-studio`, `performing-malware-triage-with-yara`
- [ ] Practice: analisis sample malware (gunakan sample dari lab, JANGAN internet malware asli tanpa isolasi ketat)
- [ ] Write custom YARA rule untuk deteksi keluarga malware tertentu
- [ ] **Deliverable:** 3 YARA rules custom + analisis report untuk 3 sample

### Minggu 4: Memory & Network Forensics
- [ ] Load skills: `analyzing-memory-dumps-with-volatility`, `analyzing-network-traffic-for-incidents`
- [ ] Practice: identifikasi process injection di memory dump
- [ ] Practice: identifikasi C2 beaconing di PCAP sample
- [ ] **Deliverable:** Memory forensics report + network IOC list

### Minggu 5: IOC & Threat Intelligence
- [ ] Load skill: `extracting-iocs-from-malware-samples`
- [ ] Build IOC database (hash, domain, IP) dari sample yang dianalisis
- [ ] Cross-reference dengan threat intel feed (MISP setup)
- [ ] **Deliverable:** IOC sharing report (STIX format)

### Minggu 6: Full Incident Response Simulation
- [ ] Load skill: `building-incident-response-playbook`
- [ ] Jalankan full tabletop exercise (simulasi ransomware attack end-to-end)
- [ ] Buat laporan investigasi forensik lengkap (sesuai template di atas)
- [ ] **Deliverable:** Full IR report + presentasi ke tim (dry run untuk kasus nyata)

---

## 📖 References & Learning Resources

### Official Standards
- NIST SP 800-86: Guide to Integrating Forensic Techniques into Incident Response
- ISO/IEC 27037: Guidelines for identification, collection, acquisition, preservation of digital evidence
- MITRE ATT&CK Framework: https://attack.mitre.org/

### Tools untuk Lab OSINT Academy
- **Volatility 3** — memory forensics framework (free/open-source)
- **YARA** — pattern matching untuk malware classification
- **Autopsy** — GUI disk forensics platform
- **Wireshark/tshark** — network traffic analysis
- **MISP** — threat intelligence platform (self-hosted, cocok untuk 170-server DC)

### Related Skills (Sudah Ada di Library)
- `security/reverse-skill/malware-analysis` — comprehensive static/dynamic/behavioral analysis
- `security/reverse-skill/digital-forensics` — memory dump, disk forensics, timeline reconstruction
- `security/reverse-skill/threat-hunting` — blue-team detection engineering
- `security/ctf-sandbox` — untuk training environment yang aman

---

## 🔐 Legal & Compliance Notes (Wajib untuk Polri)

**PENTING:** Semua aktivitas forensik/malware analysis di lab HARUS:
1. Mendapat otorisasi tertulis (untuk kasus real, bukan simulasi)
2. Mengikuti UU ITE dan KUHAP terkait barang bukti digital
3. Dokumentasi chain of custody sesuai standar pengadilan
4. Simulasi/training di lab HARUS terisolasi (air-gap, no internet) untuk malware sample asli
5. Jangan pernah eksekusi malware sample real di luar sandbox terisolasi

---

## ✨ Success Criteria

Bos/tim Reskrim dinyatakan **mastered** skill ini ketika bisa:
- [ ] Melakukan first response dengan benar (order of volatility, chain of custody)
- [ ] Analisis malware sample (static + dynamic) dalam 1 jam
- [ ] Extract IOC lengkap dari incident dan buat detection rule (YARA/Sigma)
- [ ] Buat laporan forensik yang bisa dipakai sebagai barang bukti pengadilan
- [ ] Jalankan tabletop exercise incident response secara mandiri

---

**Status:** Ready to Learn (Tier 2 - Intermediate)  
**Estimated Time to Mastery:** 6 minggu @ 5-8 jam/minggu  
**Next Milestone:** Tier 3 (Reverse Engineering dengan Ghidra + APT Hunting)
