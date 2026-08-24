# LAB-00X: [VULNERABILITY NAME]

**[One-sentence description of the vulnerability and learning objective]**

---

## 📚 Challenge Details

| Item | Value |
|------|-------|
| **Name** | LAB-00X: [Vulnerability Name] |
| **Type** | Hands-on Practical Lab |
| **Vulnerability** | [CWE-XXX: Name] |
| **Difficulty** | ⭐⭐ [Easy/Medium/Hard] |
| **Time to Solve** | [15-45 minutes] |
| **Objective** | [Extract X / Bypass Y / Execute Z] |
| **Framework** | Python Flask + [Docker] |

---

## 🚀 3-Minute Quick Start

```bash
# 1. Clone
git clone https://github.com/vanderstark/hacking-lab-lab00X-<type>.git
cd hacking-lab-lab00X-<type>

# 2. Deploy
docker-compose up -d

# 3. Access
# Browse: http://localhost:500X
```

**Expected:** Flask app running, interactive UI loads, challenge objective visible.

---

## 🎯 Objective

**What to do:**
1. [Specific exploitation task]
2. [Data extraction / code execution / auth bypass]
3. [Flag format: HACKING_LAB{...}]

**Why it matters:** [Real-world impact, e.g., data breaches, account takeover]

---

## 💡 Solution (3 Methods)

### Method 1: Basic [Payload Type]
**Difficulty:** ⭐ Beginner | **Time:** 5 min

[Simplest direct payload or technique]

```
[Exact payload]
```

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

### Method 2: [Intermediate Technique]
**Difficulty:** ⭐⭐ Intermediate | **Time:** 15 min

[More sophisticated approach, API interaction, etc.]

```
[Code/payload]
```

---

### Method 3: [Advanced Approach]
**Difficulty:** ⭐⭐⭐ Advanced | **Time:** 25 min

[Automated, obfuscated, multi-stage exploitation]

```
[Code/script]
```

---

## 📝 Vulnerable Code

### Problematic Code (app.py)
```python
# ⚠️ VULNERABLE - Input not escaped/validated
user_input = request.args.get('param')
query = f"SELECT * FROM users WHERE id = {user_input}"
cursor.execute(query)
```

**Problem:** User input directly interpolated into query/output without validation.

---

## 🛡️ How to FIX

### Secure Version
```python
# ✅ SECURE - Parameterized query
user_input = request.args.get('param')
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_input,))
```

### Key Changes:
1. Use parameterized queries (? or %s placeholders)
2. Validate/whitelist input
3. Escape output for rendering
4. Use framework built-in security (e.g., Jinja2 auto-escape)

---

## 🧠 Educational Context

### Real-World Impact
- **Ransomware attacks** typically exploit [this vuln type]
- **[Year breach]:** [Company] lost [X] records via [vulnerability]
- **Financial loss:** [Millions/Billions] in damages

### OWASP Reference
- **OWASP Top 10 #[X]:** [Vulnerability Class]
- **CWE-[XXX]:** [Name and link]

### Attack Chain
```
1. Attacker discovers [vulnerability]
2. Crafts [payload/exploit]
3. Bypasses [security measure]
4. Achieves [objective: data theft, code exec, etc.]
5. Exfiltrates [data] / Maintains [persistence]
```

---

## 🔧 Troubleshooting

### Container won't start
```bash
docker-compose logs lab-00X-<type>
# Check for syntax errors in app.py
```

### Payload not working
- Ensure quotes match (single/double)
- Check browser console for errors
- Verify endpoint URL

### Port conflict
```bash
# Change docker-compose.yml:
# ports: "5002:5002"  (instead of 5001)

# Update app.py:
# app.run(port=5002)
```

---

## ✅ Verification Checklist

- [ ] Container running: `docker-compose ps`
- [ ] Health check passes: `curl http://localhost:500X/health`
- [ ] Frontend loads: `curl http://localhost:500X/`
- [ ] Exploitation payload works (manual test)
- [ ] Flag extracted successfully
- [ ] Flag format matches: `HACKING_LAB{...}`

---

## 📚 Additional Resources

| Resource | Link |
|----------|------|
| OWASP Top 10 | https://owasp.org/www-project-top-ten/ |
| CWE Details | https://cwe.mitre.org/data/definitions/[XXX].html |
| Exploit Database | https://www.exploit-db.com/ |

---

## ⚠️ Legal Disclaimer

**This lab is for educational purposes only.**
- Do not use against systems you do not own
- Unauthorized access is illegal under [UU ITE / CFAA / etc.]
- Use only in authorized training/competition environment

---

**Generated:** [Date]  
**Version:** 1.0  
**Status:** Production-Ready
