# RACI Matrix Template for Incident Response Playbook

This template can be adapted for any incident type (phishing, ransomware, etc.)

| Activity                      | SOC L1 Analyst | SOC L2 Analyst | IR Team Lead | Legal Counsel | Communications | IT / SysAdmin | Management |
|-------------------------------|----------------|----------------|--------------|---------------|----------------|---------------|------------|
| **Initial Triage**            | R              | C              | I            |               |                | C             |            |
| **Alert Validation**          | R              | A              | I            |               |                | C             |            |
| **Evidence Collection**       | R              | A              | C            | C             |                | C             |            |
| **Containment Planning**      | C              | R              | A            | C             | I              | R             | I          |
| **Short-term Containment**    |                | R              | A            |               |                | R             |            |
| **Long-term Containment**     |                | C              | A            | I             |                | R             | I          |
| **Eradication Planning**      | C              | R              | A            | C             | I              | R             | I          |
| **Threat Removal**            |                | R              | A            |               |                | R             |            |
| **System Restoration**        |                | R              | A            |               |                | R             | I          |
| **Validation Testing**        | R              | A              | C            |               |                | C             |            |
| **User Notification**         |                | C              | A            | C             | R              | I             | I          |
| **Regulatory Reporting**      |                |                | C            | R             | A              | I             | I          |
| **Law Enforcement Coordination**|              |                | C            | R             | A              | I             | I          |
| **Lessons Learned Meeting**   | C              | C              | R            | C             | C              | C             | A          |
| **Playbook Update**           | I              | I              | R            | C             | C              | I             | A          |
| **Metrics Reporting**         | I              | I              | A            |               |                |               | R          |

Legend:
- R: Responsible (does the work)
- A: Accountable (owns the outcome, only one per activity)
- C: Consulted (two-way communication)
- I: Informed (one-way notification)

**Usage Instructions:**
1. Copy this table for your specific incident type
2. Replace role names with actual team titles in your organization
3. For each activity, assign exactly one 'A' (Accountable)
4. Ensure RACI coverage: every activity has at least one R
5. Review with all stakeholders before finalizing