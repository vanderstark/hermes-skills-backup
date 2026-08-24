# Learning Observation: Building Incident Response Playbook

**Skill:** `anthropic-cybersecurity-skills/skills/building-incident-response-playbook`
**Date:** 2026-08-24
**Learner:** Hermes Agent (for Bos - Polri)
**Status:** ACTIVE LEARNING

---

## 🔍 Skill Overview

This skill provides a methodology for designing **structured incident response (IR) playbooks** for cybersecurity teams. It aligns with:

- **NIST SP 800-61r3**: Computer Security Incident Handling Guide
- **SANS PICERL**: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned

The output is reusable procedure documentation that transforms ad-hoc investigations into institutional knowledge.

---

## 🧠 Conceptual Framework

### What is an IR Playbook?

A **playbook** is a documented, repeatable set of procedures for responding to a specific incident type.

It differs from a **runbook** (granular step-by-step technical tasks) and a **RACI Matrix** (who does what).

| Term | Definition |
|------|------------|
| **Playbook** | Documented procedures for a specific incident type |
| **Runbook** | Step-by-step technical instructions for a task within a playbook |
| **RACI Matrix** | Who is Responsible, Accountable, Consulted, Informed |
| **Decision Tree** | Logic flow with binary outcomes at each branch |
| **Escalation Criteria** | Conditions triggering higher-level notification |
| **SOAR Playbook** | Automated workflow in a SOAR platform executing playbook steps |

---

## 🗂️ Playbook Structure Template

Every playbook should follow this consistent structure:

```markdown
PLAYBOOK TEMPLATE
━━━━━━━━━━━━━━━━
1. Playbook Metadata
   - Name, version, owner, last review date
   - Trigger conditions
   - Severity criteria

2. RACI Matrix
   - Responsible / Accountable / Consulted / Informed per step

3. Detection & Triage
   - How detected
   - Initial triage checklist
   - Severity classification

4. Containment
   - Short-term actions
   - Long-term actions
   - Evidence preservation

5. Eradication
   - Root cause identification
   - Threat removal steps
   - Verification

6. Recovery
   - System restoration
   - Validation criteria
   - Post-recovery monitoring

7. Post-Incident
   - Lessons learned trigger
   - Report template
   - Detection improvement actions

8. Communication
   - Internal notification matrix
   - External notification requirements
   - Status update cadence

9. Appendices
   - Tool-specific procedures
   - Contact lists
   - Evidence collection checklists
```

---

## 🌲 Decision Tree Example (Phishing)

```
Detection Alert Received
├── Is the alert a true positive?
│   ├── YES → Classify severity
│   │   ├── P1 (Critical) → Page incident commander, begin containment immediately
│   │   ├── P2 (High) → Notify IR lead, begin investigation within 30 min
│   │   ├── P3 (Medium) → Queue for investigation within 4 hours
│   │   └── P4 (Low) → Document and investigate within 24 hours
│   └── NO → Document as false positive, tune detection rule
└── Cannot determine → Escalate to Tier 2 for deeper analysis
```

**Escalation Triggers:**
- Any P1 incident → Immediate escalation to IR lead and CISO
- Data exfiltration confirmed → Legal counsel + privacy officer notified
- Customer data involved → Customer notification process activated
- Third-party involvement → Vendor security contact engaged
- Law enforcement needed → General counsel authorizes before contact

---

## 🛠️ Tool-Specific Procedures (Concrete Examples)

### Containment – Endpoint Isolation via CrowdStrike
```bash
1. Open Falcon Console > Hosts > Search for affected hostname
2. Click on the host > Host Details
3. Click "Contain Host" button in upper right
4. Confirm isolation (host will only communicate with CrowdStrike cloud)
5. Document containment action in incident ticket with timestamp
6. Verify containment: Host should show "Contained" status badge
```

### Containment – Block C2 Domain at DNS
```bash
1. SSH to DNS server: ssh admin@dns-primary.corp.local
2. Add to block zone:
   echo "zone evil.com { type master; file /etc/bind/db.sinkhole; };" >> /etc/bind/named.conf.local
3. Reload DNS: rndc reload
4. Verify: dig @dns-primary evil.com (should resolve to sinkhole IP 10.0.0.99)
5. Document blocked domain in incident ticket
```

---

## 🤖 SOAR Integration

Convert manual playbook steps into automated workflows:

- Map each playbook step to a SOAR action (API call, script, human decision point)
- Define automation boundaries (what runs automatically vs. requires analyst approval)
- Build enrichment automations for triage phase
- Create containment automations with approval gates for high-impact actions
- Configure notification automations for stakeholder communication

**Tools:** Cortex XSOAR, Splunk SOAR, TheHive, Tines

---

## 🧪 Example: Phishing Response Playbook (Condensed)

```
Playbook Name:    Phishing Incident Response
Version:          2.1
Owner:            SOC Manager
Trigger:          Phishing email reported via abuse@corp.com or phish button

RACI MATRIX
Activity                    | SOC L1 | SOC L2 | IR Lead | Legal | Comms
Initial Triage              |   R    |   C    |   I     |       |
Email Analysis              |   R    |   A    |   I     |       |
Containment                 |        |   R    |   A     |   I   |
Credential Reset            |        |   R    |   A     |       |
User Notification           |        |   C    |   A     |       |   R
Regulatory Notification     |        |        |   C     |   R   |   A

PROCEDURE STEPS
1. Extract email headers, check sender reputation
2. Analyze URLs/attachments in sandbox
3. Quarantine email from all mailboxes
4. Block sender domain at mail gateway
5. Reset passwords if credentials entered
6. Notify affected users
7. Create case in TheHive with IOCs

DECISION TREE
[As above]

ESCALATION MATRIX
[Conditions and contacts]

METRICS
Target MTTA: 15 minutes
Target MTTC: 1 hour
Target MTTR: 4 hours
```

---

## 💡 Practical Takeaways for Polri Lab Context

- **Prioritas Playbook (bangun dulu):**
  1. Ransomware
  2. Phishing / credential compromise
  3. Business email compromise
  4. Data breach / exfiltration
  5. DDoS
  6. Insider threat
  7. Account takeover
  8. Web app compromise
  9. Cloud infra compromise

- **Pitfalls to Avoid:**
  - Terlalu generik tanpa referensi tool spesifik
  - Lupa komunikasi plan untuk user yang menerima phishing
  - Tidak definisi kriteria kapan laporan menjadi investigasi penuh
  - Tidak versioning / review cycle

- **Maintenance:**
  - Tabletop exercise dengan tim IR
  - Live-fire exercise di test environment
  - Review setelah setiap insiden nyata
  - Quarterly review untuk kontak list, prosedur, eskalasi

---

## 📌 Next Steps After Learning

✅ Identify top 3 incident types for Bos's infrastructure  
✅ Draft RACI matrix with actual team roles  
✅ Write tool-specific procedures for available security stack  
✅ Test playbook via tabletop exercise  

---

*Observation logged by Task Observer protocol.*
