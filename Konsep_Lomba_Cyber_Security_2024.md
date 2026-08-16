# KONSEP LOMBA CYBER SECURITY 2024
## National Cybersecurity Competition Framework

**Prepared by:** Hermes Agent (AI Assistant)  
**Date:** 16 Agustus 2026  
**For:** Polri Academy & Cybersecurity Lab Indonesia  

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Competition Overview](#competition-overview)
3. [Timeline & Schedule](#timeline--schedule)
4. [Competition Categories](#competition-categories)
5. [Problem Statements (Examples)](#problem-statements-examples)
6. [Scoring Rubric](#scoring-rubric)
7. [Judge Guidelines](#judge-guidelines)
8. [Prize Structure](#prize-structure)
9. [Technical Requirements](#technical-requirements)
10. [Rules & Regulations](#rules--regulations)

---

## EXECUTIVE SUMMARY

**Lomba Cyber Security 2024** adalah kompetisi tingkat nasional yang dirancang untuk mengidentifikasi, mengembangkan, dan memberikan penghargaan kepada profesional cybersecurity terbaik di Indonesia.

### QUICK FACTS

| Aspek | Detail |
|-------|--------|
| **Format** | On-site 24-jam intensif |
| **Tim** | 3-5 orang (professional/student) |
| **Kategori** | 3 tracks (Offensive, Defensive, Governance) |
| **Total Hadiah** | Rp 500 juta + internship opportunities |
| **Lokasi** | Jakarta, Cybersecurity Lab Polri |
| **Tanggal** | 15-17 November 2024 |
| **Peserta** | 50+ teams diperkirakan |

### TARGET OUTCOMES

✓ Mengidentifikasi 50+ top cybersecurity talents  
✓ Membangun networking ecosystem cybersecurity nasional  
✓ Positioning Indonesia di regional security competitions  
✓ Knowledge transfer & best practices sharing  
✓ Talent recruitment untuk Polri/BSSN/industry  

---

## COMPETITION OVERVIEW

### 2.1 Vision & Mission

**VISION:**  
Menjadi kompetisi cybersecurity terkemuka di Asia Tenggara yang mendorong inovasi dan excellence dalam protective of critical infrastructure Indonesia.

**MISSION:**
- Mengidentifikasi talent cybersecurity terbaik nasional
- Meningkatkan skill & awareness cybersecurity dalam organisasi
- Membangun komunitas cybersecurity profesional yang solid
- Mendorong innovation dalam defensive strategies
- Positioning Indonesia di international security landscape
- Memperkuat capacity building untuk critical infrastructure protection

### 2.2 Core Principles

| Prinsip | Penjelasan |
|---------|-----------|
| **AUTHORIZED ONLY** | Semua aktivitas dalam scope legal & authorized |
| **FRAMEWORKS-BASED** | MITRE ATT&CK, NIST CSF 2.0, ISO 27001, UU PDP |
| **PROFESSIONAL** | Standar industri international |
| **FAIR & TRANSPARENT** | Penilaian objektif, kriteria jelas, independent judges |
| **EDUCATIONAL** | Learning-focused, knowledge transfer priority |
| **INCLUSIVE** | Profesional & students welcome |

### 2.3 Framework Alignment

Kompetisi menggunakan framework internasional terkemuka:

**MITRE ATT&CK Framework**
- 14 tactics (Reconnaissance → Resource Dev → Execution → Persistence, dll)
- 600+ techniques mapping
- Used for Offensive & Defensive track problem design

**NIST Cybersecurity Framework 2.0**
- Govern, Identify, Protect, Detect, Respond, Recover
- Used for Governance track & control mapping

**ISO 27001 / 27002**
- Information Security Management System
- Used for compliance & control assessments

**UU PDP No. 27 Tahun 2022**
- Personal Data Protection Law (Indonesia context)
- Used for governance & legal alignment

---

## TIMELINE & SCHEDULE

### 3.1 Registration Phase

| Event | Date | Notes |
|-------|------|-------|
| Registration Opens | 1 September 2024 | Online via portal |
| Early Bird Close | 30 September 2024 | Rp 100K discount |
| Final Registration | 31 October 2024 | Last day to register |
| Team Briefing | 13 November 2024 | Mandatory attendance |
| Competition | 15-17 November 2024 | Main event |

### 3.2 Competition Schedule (24-hour Format)

**DAY 1 (15 Nov) - Opening & Track A**

| Time | Activity | Duration | Location |
|------|----------|----------|----------|
| 08:00 | Registration & Environment Setup | 2h | Main Hall |
| 10:00 | Opening Ceremony + Rules Briefing | 1h | Auditorium |
| 11:00 | **TRACK A START** (Offensive Security) | 4h | Lab 1-5 |
| 15:00 | Lunch Break | 1h | Cafeteria |
| 16:00 | **TRACK B START** (Defensive Security) | 4h | Lab 6-10 |
| 20:00 | Dinner & Rest | 2h | Cafeteria |
| 22:00 | **TRACK C** (Governance Challenge) | 2h | Meeting Rooms |

**DAY 2-3 (16-17 Nov) - Final Challenges & Judging**

| Time | Activity | Duration |
|------|----------|----------|
| 00:00-06:00 | Final Challenge (Multi-track Collaboration) | 6h |
| 06:00-09:00 | Rest & Breakfast | 3h |
| 09:00-16:00 | Submission & Judge Deliberation | 7h |
| 17:00 | Awards Ceremony | 2h |
| 19:00 | Closing & Celebration | 2h |

---

## COMPETITION CATEGORIES

### 4.1 Track A: OFFENSIVE SECURITY (Red Team)

**OBJECTIVE:** Identify vulnerabilities, execute exploits, demonstrate attack techniques using legal framework

**CHALLENGE STRUCTURE**

| Level | Scope | Difficulty | Time | Points |
|-------|-------|-----------|------|--------|
| **1** | Basic vuln scanning + SQL injection | Beginner | 1h | 100 |
| **2** | Web app exploitation + auth bypass | Intermediate | 1.5h | 100 |
| **3** | Custom multi-stage attack + privilege escalation | Advanced | 1h | 100 |
| **4** | APT simulation + lateral movement + persistence | Expert | 0.5h | 100 |
| | **TOTAL** | | **4h** | **400 pts** |

**FRAMEWORK MAPPING:**
- MITRE ATT&CK: Reconnaissance → Initial Access → Execution → Persistence → Privilege Escalation
- D3FEND: Defensive techniques to counter each attack

**TOOLS PROVIDED:**
- Burp Suite Professional
- Metasploit Framework
- Kali Linux (fully patched)
- DVWA vulnerable app
- Custom labs (HackTheBox instances)

**EVALUATION CRITERIA:**
- Technical correctness (40%): Valid exploitation, proper techniques
- Methodology (30%): Logical approach, documented steps
- Innovation (20%): Beyond-the-box techniques, advanced chains
- Efficiency (10%): Time management, resource optimization

**SAMPLE SCENARIO:**
> PT TechCorp Indonesia operates e-commerce platform with 500K daily users. Your task: identify 5 OWASP Top 10 vulnerabilities, exploit 3+ of them, extract sensitive data, document attack chain with MITRE ATT&CK mapping, provide remediation per OWASP guidelines.

---

### 4.2 Track B: DEFENSIVE SECURITY (Blue Team)

**OBJECTIVE:** Detect intrusions, respond to incidents, investigate forensics, harden defenses

**CHALLENGE STRUCTURE**

| Level | Scope | Focus | Time | Points |
|-------|-------|-------|------|--------|
| **1** | Log analysis + IDS alert triage | Detection | 1h | 100 |
| **2** | Incident response workflow + containment | Response | 1.5h | 100 |
| **3** | Forensics analysis + threat hunting | Investigation | 1h | 100 |
| **4** | Defense architecture design + remediation | Strategy | 0.5h | 100 |
| | **TOTAL** | | **4h** | **400 pts** |

**FRAMEWORK MAPPING:**
- NIST CSF: Identify → Protect → Detect → Respond → Recover
- ISO 27001: Control objectives & implementation

**TOOLS PROVIDED:**
- Splunk SIEM (sandbox environment)
- Suricata IDS
- ELK Stack (Elasticsearch/Kibana/Logstash)
- Wireshark for packet analysis
- Volatility for memory forensics

**EVALUATION CRITERIA:**
- Technical correctness (40%): Accurate log analysis, correct interpretation
- Methodology (30%): Proper incident response phases, documentation
- Innovation (20%): Advanced detection rules, threat hunting techniques
- Efficiency (10%): Time to detection, swift response

**SAMPLE SCENARIO:**
> Server 192.168.1.50 shows suspicious activity: failed login 14:23, successful login 14:25 different IP, file access /etc/shadow 14:30, data exfiltration 14:45. Analyze logs, identify attack phases (MITRE ATT&CK), provide containment plan, design recovery procedures, create detection rules.

---

### 4.3 Track C: GOVERNANCE & RISK (Purple Team)

**OBJECTIVE:** Map security controls, assess risks, align with compliance frameworks, design security strategy

**CHALLENGE STRUCTURE**

| Level | Scope | Format | Time | Points |
|-------|-------|--------|------|--------|
| **1** | NIST CSF control identification + ISO mapping | Analysis | 40min | 100 |
| **2** | Risk assessment + control prioritization | Assessment | 40min | 100 |
| **3** | Strategic planning + implementation roadmap | Strategy | 40min | 100 |
| | **TOTAL** | | **2h** | **300 pts** |

**FRAMEWORK MAPPING:**
- NIST CSF 2.0: Functions & Categories
- ISO 27001:2022: Control objectives
- UU PDP Indonesia: Compliance requirements
- IEC 31010: Risk assessment methodology

**CASE STUDY SCENARIO:**
> Startup fintech (50 employees) currently at 40% NIST CSF compliance. Target: 85% dalam 1 tahun. Your task: (1) Gap analysis current state, (2) Prioritize top 10 controls, (3) Map ke ISO 27001, (4) Create 12-month roadmap (3 phases), (5) Estimate budget & FTE requirements, (6) Design KPIs.

**DELIVERABLES:**
- Gap analysis report (2 pages)
- Control prioritization matrix (scoring & rationale)
- Implementation roadmap (phased, with milestones)
- Budget forecast (per phase)
- Presentation (10 min) + Q&A (5 min)

---

## SCORING RUBRIC

### 6.1 Evaluation Criteria (Universal)

| Criterion | Weight | Description | Excellent (90-100) | Good (70-89) | Adequate (60-69) |
|-----------|--------|-------------|-------------------|----------------|-----------------|
| **Technical Correctness** | 40% | Proper methodology, valid techniques, correct mapping | Complete, accurate, no errors | 1-2 minor errors | 3-4 minor errors |
| **Methodology** | 30% | Logical approach, step-by-step, documented | Clear flow, well documented, evidence | Generally logical, mostly documented | Basic logic, partial documentation |
| **Innovation & Depth** | 20% | Beyond-the-box, advanced techniques, comprehensive | Multiple innovations, deep analysis | 1-2 innovations, good depth | Standard approach, minimal depth |
| **Efficiency** | 10% | Time management, resource optimization | Well-optimized, fast execution | Adequate speed, minor delays | Slow execution, inefficient |
| **TOTAL** | **100%** | | **90+** | **70-89** | **60-69** |

### 6.2 Scoring Process

1. **Independent Scoring**: Setiap judge score independently (no collaboration)
2. **Score Entry**: Scores submitted within 30 min post-challenge
3. **Consensus Building**: Judges discuss scores (if variance > 15%)
4. **Final Score**: Average of 2-3 judges
5. **Appeal Resolution**: Team dapat appeal jika ada discrepancy

### 6.3 Minimum Passing Score

- **Per Challenge**: 60 points minimum
- **Track Average**: 70 points minimum (to rank in top 10)
- **Disqualification**: <50 points in any challenge

---

## JUDGE GUIDELINES

### 7.1 Judge Selection & Qualifications

**MINIMUM REQUIREMENTS:**
- ✓ 5+ years cybersecurity professional experience
- ✓ Certified (CEH, OSCP, CISSP, GIAC, or equivalent)
- ✓ No conflict of interest dengan peserta/organisasi
- ✓ Signed NDA & confidentiality agreement
- ✓ Attend 4-hour judge training session

**PREFERRED QUALIFICATIONS:**
- ✓ Published research dalam cybersecurity
- ✓ Prior competition judging experience
- ✓ Industry recognition (CISOs, architects, researchers)

### 7.2 Judge Responsibilities

**BEFORE COMPETITION:**
- [ ] Attend training session (framework, rubric, platform)
- [ ] Review problem statements & expected solutions
- [ ] Familiarize dengan scoring rubric & edge cases
- [ ] Conduct dry-run evaluation

**DURING COMPETITION:**
- [ ] Observe teams (note technical progress)
- [ ] Independently score challenges
- [ ] Provide immediate feedback if asked
- [ ] Document all scoring rationale
- [ ] Flag any technical issues to organizers

**AFTER COMPETITION:**
- [ ] Participate dalam consensus scoring
- [ ] Handle appeal requests (if any)
- [ ] Provide written feedback untuk winners
- [ ] Prepare award presentation comments

### 7.3 Judge Code of Conduct

✓ **Objectivity**: Score per rubric only (no bias)  
✓ **Confidentiality**: Keep scores confidential until announcement  
✓ **Impartiality**: Avoid communication dengan peserta during competition  
✓ **Professionalism**: Respectful, supportive tone dalam feedback  
✓ **Transparency**: Explain scoring rationale if asked  

---

## PRIZE STRUCTURE & RECOGNITION

### 8.1 Prize Money

| Rank | Prize Money | Trophy | Certificate | Recognition |
|------|-------------|--------|-------------|--------------|
| **1st Place** | Rp 200 juta | Gold | Official | Featured in media, internship offer |
| **2nd Place** | Rp 150 juta | Silver | Official | Media coverage, consulting project |
| **3rd Place** | Rp 100 juta | Bronze | Official | Training sponsorship, networking |
| **4-10th** | Rp 10-50 juta | — | Participation | Industry networking opportunities |

### 8.2 Special Recognitions

| Award | Criteria | Reward |
|-------|----------|--------|
| **Best Offensive** | Highest Track A score | Rp 25M + internship @ Polri |
| **Best Defensive** | Highest Track B score | Rp 25M + SIEM training |
| **Best Governance** | Highest Track C score | Rp 25M + consulting offer |
| **Innovation Award** | Most creative solution | Rp 25M + conference sponsorship |
| **Best Team Work** | Judge's discretion | Rp 10M + team bonding |

### 8.3 Opportunities Beyond Prizes

- **Internship Programs**: Winning teams offered 3-6 month internships at Polri/BSSN/major tech companies
- **Consulting Projects**: Top 10 teams eligible for security consulting projects (Rp 50-500M contracts)
- **Speaking Engagements**: Winners invited ke industry conferences & training programs
- **Publication**: Writeups dapat dipublikasikan di security journals/blogs (dengan approval)
- **Networking**: Access ke exclusive cybersecurity community & mentorship programs

---

## TECHNICAL REQUIREMENTS

### 9.1 Infrastructure Provided by Organizer

**HARDWARE:**
✓ Kali Linux workstations (16GB RAM, SSD, dual monitors)  
✓ Network lab (isolated, 10Mbps connections)  
✓ Backup laptops jika ada issues  

**SOFTWARE & SERVICES:**
✓ Kali Linux OS (fully patched, pre-configured)  
✓ Splunk SIEM (24-hour license per team)  
✓ Burp Suite Professional (license per team)  
✓ Metasploit Framework (free version)  
✓ DVWA vulnerable app (for Track A)  
✓ Vulnerable Linux boxes (for Track A/B)  
✓ Suricata IDS (pre-configured rules)  
✓ Forensic tools (Volatility, FTK, Autopsy)  

**NETWORK:**
✓ Dedicated lab network (isolated from internet)  
✓ Controlled internet access (filtered, monitored)  
✓ Backup connectivity (redundant ISP)  
✓ VPN untuk remote troubleshooting  

**SUPPORT:**
✓ 24/7 technical support team on-site  
✓ Network engineers untuk connectivity issues  
✓ Forensic experts untuk evidence handling  
✓ Competition coordinators untuk logistics  

### 9.2 Participant Requirements

**PREREQUISITE SKILLS:**
✓ Minimum 2 years cybersecurity professional experience (for professionals)  
✓ OR Advanced cybersecurity coursework (for students)  
✓ Basic Linux/Windows command line competency  
✓ Networking fundamentals (TCP/IP, DNS, HTTP)  
✓ Familiarity dengan security tools (Nessus, Burp, etc)  

**DOCUMENTATION:**
✓ Valid photo ID (KTP, passport, or employee ID)  
✓ Team registration form (signed by team lead)  
✓ Confirmation letter dari employer/university  
✓ Signed liability waiver  

**HEALTH & SAFETY:**
✓ COVID-19 vaccination proof (if required by government)  
✓ Medical certificate (if known health conditions)  
✓ Emergency contact information  

### 9.3 Restricted Items & Activities

**PROHIBITED:**
✗ External exploit tools/zero-days (only lab environment approved)  
✗ Communication dengan external parties selama kompetisi  
✗ Unauthorized access outside assigned lab scope  
✗ Data exfiltration/removal dari lab premises  
✗ Photography/video recording (except team documentation)  
✗ Sharing passwords/credentials dengan other teams  
✗ Accessing real-world systems (ONLY lab simulations)  

**COMPLIANCE:**
✓ All activities logged & monitored by technical team  
✓ Log retention: 90 days post-event  
✓ Legal review: All challenges pre-approved oleh legal counsel  
✓ Insurance: Organizer maintain cyber liability insurance  

---

## RULES & REGULATIONS

### 10.1 General Competition Rules

**ELIGIBILITY:**
✓ Indonesian citizens OR valid work permit  
✓ 18+ years old (or 13+ with parental consent)  
✓ No prior disqualification dari other competitions  
✓ Register sebagai team 3-5 orang (tidak ada duplicate across teams)  

**REGISTRATION:**
✓ Online registration via official portal  
✓ Rp 500K registration fee per team (waived for Polri/military)  
✓ Early bird discount: Rp 100K off (sebelum 30 Sept)  
✓ Confirmation: Teams akan menerima kit sebelum 13 Nov  

**CONDUCT STANDARDS:**
✓ Professional & respectful interaction dengan judges & other teams  
✓ Adhere to technical rules (no unauthorized access beyond scope)  
✓ Report security issues immediately (tidak exploit untuk advantage)  
✓ Zero tolerance untuk cheating, fraud, plagiarism  
✓ No harassment, discrimination, atau threatening behavior  

### 10.2 Disqualification Grounds

**AUTOMATIC DISQUALIFICATION:**
- ✗ Unauthorized access ke systems outside competition scope
- ✗ Evidence of cheating atau plagiarism dari public exploits
- ✗ Harassment, discrimination, atau threatening behavior terhadap judges/participants
- ✗ Non-compliance dengan technical rules (data exfiltration, external tools)
- ✗ Violation dari confidentiality/NDA
- ✗ Refusal untuk comply dengan judge instructions

**CONSEQUENCES:**
- Immediate removal dari competition
- Forfeiture dari prizes & recognition
- Potential legal action (jika unauthorized access actual)
- Public announcement (if deemed appropriate)
- Blacklist dari future competitions

### 10.3 Intellectual Property & Confidentiality

**TEAM OWNERSHIP:**
- All exploits, scripts, tools developed during competition = team property
- Teams retain IP rights untuk any original techniques/code created

**PUBLICATION RIGHTS:**
- Organizer may request anonymized writeups untuk security education purposes
- Publication hanya dengan explicit team permission
- Sensitive exploits/zero-days akan NOT be published
- Teams dapat opt-out dari publication

**CONFIDENTIALITY:**
- All competition problems, solutions, judge feedback = confidential
- Embargo period: 6 bulan post-competition before public disclosure
- NDAs signed by all participants, judges, organizers

---

## CLOSING STATEMENTS

This cybersecurity competition framework represents a commitment to:

✓ **Excellence in Security**: Identifying & recognizing top talent  
✓ **Legal Compliance**: Ensuring all activities remain authorized & ethical  
✓ **Knowledge Sharing**: Building a stronger cybersecurity community  
✓ **Professional Standards**: Meeting international best practices  
✓ **Innovation**: Encouraging next-generation security professionals  

---

## APPENDICES

### Appendix A: Problem Statement Bank (More Examples Available)

**A.1 - Offensive Track, Level 3**
Scenario: Government agency website vulnerable to advanced attacks. Conduct chain exploitation (SQL injection → file inclusion → RCE), establish persistence, document MITRE ATT&CK mapping.

**A.2 - Defensive Track, Level 4**
Scenario: Multi-day APT simulation. Analyze PCAP files, logs, memory dumps. Identify all attack phases, document forensic findings, design detection rules, create incident report.

**A.3 - Governance Track, Level 3**
Scenario: Enterprise digital transformation requires security alignment. Assess current controls, map ke ISO 27001, design 3-year roadmap covering NIST CSF 2.0 + UU PDP compliance.

---

## DOCUMENT INFORMATION

**Prepared By:** Hermes Agent (AI Cybersecurity Framework)  
**Date:** 16 Agustus 2026  
**Version:** 1.0 (Draft)  
**Classification:** For Internal Circulation  
**Contact:** kompetisi.cybersecurity@polri.go.id  

---

*This competition framework is designed to identify, develop, and recognize cybersecurity excellence while maintaining the highest standards of legal compliance, professional ethics, and educational value.*

**Selamat berkompetisi!** 🏆
