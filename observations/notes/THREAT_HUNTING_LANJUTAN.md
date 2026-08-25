# Threat Hunting & Detection Engineering — Materi Lanjutan

> **Target Audience:** Tim Intelkam (Lantas, Sabhara), SIEM Team, Forensics Unit  
> **Level:** Intermediate → Advanced (Setelah Digital Forensics & Malware Analysis selesai)  
> **Estimasi Waktu:** 8–10 minggu (2 jam/hari, 5 hari/minggu)  
> **Prasyarat:** Sudah paham MITRE ATT&CK, YARA rules, dasar Linux/Windows forensics

---

## 🎯 Tujuan Pembelajaran

1. **Hypothesis-driven threat hunting**: pipa mentah → patokan → hasil
2. **Sigma/YARA rule engineering**: menulis deteksi yang bekerja di SIEM/EDR
3. **SIEM query design**: ELK, Splunk, Wazuh custom rules
4. **Endpoint telemetry**: osquery + osquery YARA extensions
5. **Atomic Red Team verification**: hanya di lab otoritas
6. **Detection pipeline**: dari log event hingga incident ticket

---

## 📚 Roadmap 10 Minggu

### Minggu 1–3: Fundamentals & Hypothesis

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **ATT&CK Mapping**: core techniques (T1055, T1003, T1021, T1082) | Navigasi `mitre-attack-navigator` visualisasi |
| 3–4 | **Data source inventory**: what logs do we have? (sysmon, eventid 4624, auth logs) | Export dari SIEM: elk/splunk query |
| 5–6 | **Threat hunting methodology**: hypothesis-first vs reactive | Workflow: hypothesis → query → validate → rule |
| 7–8 | **Baseline establishment**: normal admin behavior, business hours | PowerShell Script Block Log (BSL) — extract 30 hari terakhir |
| 9–10 | Lab: Deploy **Wazuh SIEM** lightweight (single-node) | `docker run -d -p 1514:1514 -p 5500:5500 wazuh/wazuh:4.7.0` |

**Deliverable Minggu 2:** `hunting-hypothesis.md` — 5 hipotesis threat ter-prioritaskan beserta data source

---

### Minggu 4–6: Sigma & YARA Rule Engineering

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Sigma rule anatomy**: title, id, status, tags, logsource, detection | Referensi `malware-analysis/yara-sigma-rules.md` |
| 3–4 | **Sigma to SIEM**: elk conversion, splunk conversion, wazuh conversion | `sigmac -t elk hunting-loop.yaml` |
| 5–6 | **YARA rules**: file + memory scanning, PE/ioc extraction | `yara -r -d rules.yar /opt/data/samples/` |
| 7–8 | **Performance tuning**: large dataset scanning, timeout handling | `timeout 300 yara rules.yar big_folder/` |
| 9–10 | Lab: **Generate 10 Sigma rules** untuk deteksi Living-off-the-Land di endpoint | 3 PowerShell, 2 cmd, 2 WMI, 2 Registry |

**Deliverable Minggu 6:** `sigma-rules-pack-indonesian-polri.yaml` — 10 Sigma rules dengan id unik

---

### Minggu 7–8: SIEM Query Design & Correlation

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **ELK query design**: painless scripting, index pattern, alert | `POST _search` query untuk T1055 process creation |
| 3–4 | **Splunk SPL**: correlation rules, timechart, eventstats | Detect lateral movement across hosts |
| 5–6 | **Wazuh rules**: decoded rule language, frequency threshold, firekam | Custom rule: failed SSH login > 5x per menit |
| 7–8 | **Cross-telemetry correlation**: Sysmon + Windows Security + DNS + Netflow | Build timeline of attack chain |
| 9–10 | Lab: **Sigma → Wazuh conversion** untuk 5 rules custom | Verify muncul di Wazuh dashboard + alerts |

**Deliverable Minggu 8:** `siem-queries-elk-splunk-wazuh.md` — 5 query + 5 Wazuh rule yang diuji

---

### Minggu 9–10: Atomic Red Team Verification & Detection Pipeline

| Hari | Topik | Praktik |
|------|-------|---------|
| 1–2 | **Atomic Red Team**: single-command tests per ATT&CK technique | `atc T1055` → test process injection via rundll32 |
| 3–4 | **Validation**: replay historical logs → detect? | `osquery` query → compare past 7 days |
| 5–6 | **Detection pipeline**: alert → ticket (ServiceNow/OTRS) → analyst | Custom Python bridge: `osquery → JSON → ServiceNow API` |
| 7–8 | **False positive tuning**: threshold adjustment, known-good tuning | `curve` analysis: precision/recall per rule |
| 9–10 | Final project: **Threat hunt exercise** — siapa attacker? | Dataset: 1-month attack sim (APT3/APT41 style), find IOCs |

**Deliverable Minggu 10:** `threat-hunt-exercise-report.pdf` — findings, IOCs, timeline, Sigma rules

---

## 🛠️ Toolchain Wajib Diinstall

```bash
# Wazuh SIEM (single-node)
docker pull wazuh/wazuh:4.7.0
docker run -d -p 1514:1514 -p 5500:5500 wazuh/wazuh:4.7.0

# Sigmac (Sigma → SIEM conversion)
pip install sigmac

# Osquery (endpoint telemetry)
osqueryi --disable_timestamp

# Atomic Red Team
git clone https://github.com/atomicredteam/atomicredteam && cd atomicredteam && chmod +x install.sh && ./install.sh

# Sigma YAML lint
pip install sigma-linter

# jq (JSON parsing)
apt-get install jq

# ELK Stack (opsional, untuk development)
docker pull elasticsearch:8.10.0
docker pull kibana:8.10.0
docker pull logstash:8.10.0
```

---

## 📂 File Referensi Penting (dari Skill Asli)

| File | Path | Kegunaan |
|------|------|----------|
| Hunting Loop | `security/reverse-skill/threat-hunting/references/hunting-loop.md` | Workflow hypothesis-driven |
| YARA-Sigma Rules | `malware-analysis/references/yara-sigma-rules.md` | Rule structure comparison |
| Sandbox Orchestration | `malware-analysis/references/sandbox-orchestration.md` | Automated analysis |
| Anti-Analysis Techniques | `malware-analysis/references/anti-analysis-techniques.md` | 94 tech detection |

---

## 🎯 Use Case Polri (Khusus)

| Unit | Skenario Threat Hunting | Prioritas |
|------|-------------------------|-----------|
| **Lantas** | Highway patrol CCTV → hijacking pattern, stolen truck network | 🔴 Critical |
| **Sabhara** | Drug trace API → suspicious transaction network | 🔴 Critical |
| **Intelkam** | OSINT darkweb forum → threat actor attribution | 🟠 High |
| **Binmas** | Community report → coordinated scam detection | 🟠 High |
| **Reskrim** | Cybercrime financial trail → money mule network | 🟠 High |

**Output Target:** Sigma rules + SIEM alerts + IOC list + incident timeline

---

## ✅ Checklist Kelulusan (Harus Semua ✅)

- [ ] Deploy **Wazuh SIEM** + 30-day log ingest (minimal 500MB)
- [ ] Tulis **10 Sigma rules** untuk deteksi PO (Living-off-the-Land) di endpoint Polri
- [ ] Convert Sigma → **ELK, Splunk, Wazuh** masing-masing 2 rules
- [ ] Uji **Atomic Red Team** untuk 5 ATT&CK techniques T1055/T1003/T1021
- [ ] Tulis **5 SIEM queries** ELK/Splunk untuk deteksi lateral movement
- [ ] Buat **dashboard** Wazuh: alerts per day, top 3 triggered rules, threat actor mapping
- [ ] Jalankan **threat hunt exercise** 1-month dataset → find attacker IOCs
- [ ] Presentasi hasil (30 menit) ke tim keamanan & direktur laboratorium

---

## 🚀 Next Steps Setelah Selesai

1. **Extended Detection & Response (XDR)**: integrasi endpoint + network + cloud
2. **Behavioral baselining**: machine learning anomaly detection (koneksi ke MLOps Advanced)
3. **Automated incident response playbook**: SOAR dengan n8n / Phantom
4. **Threat intelligence integration**: OpenCTI, MISP feed ke dalam Sigma
5. **Red vs Blue team exercises**: otorisasi bertahap, skenario terencana

---

## 📎 Referensi Eksternal

- MITRE ATT&CK: https://attack.mitre.org/
- Sigma: https://sigma-rules.com/
- Atomic Red Team: https://github.com/atomicredteam/atomicredteam
- Wazuh: https://wazuh.com/
- OSQuery: https://osquery.io/
- Elastic SIEM: https://www.elastic.com/en/security/siem
- Splunk: https://www.splunk.com/