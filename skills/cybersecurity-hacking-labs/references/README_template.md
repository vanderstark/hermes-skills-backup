# LAB-XXX: [VULNERABILITY NAME]

**Hands-on CTF Challenge**

---

## 📚 Challenge Description

**Difficulty:** ⭐⭐ Easy-Medium  
**Time to Solve:** 15-30 minutes  
**Framework:** Python Flask + SQLite  
**Objective:** [What participants should accomplish]

---

## 🚀 Quick Start (3 Minutes)

```bash
git clone https://github.com/vanderstark/hacking-lab-<name>.git
cd hacking-lab-<name>
docker-compose up -d
# Open http://localhost:5000
```

---

## 🎯 Objective

[50-word description of what participants need to do]

---

## 🔧 Deployment Guide

### Prerequisites
```bash
docker --version
docker-compose --version
```

### Step 1: Clone
```bash
git clone ...
cd ...
```

### Step 2: Build & Run
```bash
docker-compose up -d
docker-compose ps
```

### Step 3: Verify
```bash
curl http://localhost:5000/health
```

### Step 4: Access
```
http://localhost:5000
```

---

## 💡 Solution Walkthrough

### Method 1: [Exploitation Technique]
```
Step 1: ...
Step 2: ...
Step 3: ...
Expected: Flag = HACKING_LAB{...}
```

### Method 2: [Alternative Technique]
```
Step 1: ...
```

### Method 3: Programmatic (Curl/API)
```bash
curl -X POST http://localhost:5000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"payload":"..."}'
```

---

## 🛡️ How to Fix (Secure Coding)

### ❌ Vulnerable Code
```python
# Problem: No input validation
```

### ✅ Secure Code
```python
# Solution: Parameterized queries
```

---

## 🧠 Educational Notes

- Why this vulnerability matters
- Real-world impact
- Prevention strategies
- OWASP/CWE references

---

## 🔧 Troubleshooting

### Container won't start
```bash
docker-compose logs lab-xxx
docker-compose down && docker-compose up -d
```

### Port 5000 in use
Edit docker-compose.yml: `"8080:5000"`

### Can't access http://localhost:5000
Wait 5-10 seconds for app startup, then retry.

---

## 📚 References

- OWASP Top 10
- CWE Details
- Docker Documentation
- Framework Security Guides

---

**Generated:** [DATE]  
**Status:** Production Ready
