# 📚 README.MD TEMPLATE FOR HACKING LABS

Copy this structure and fill in the brackets `[like this]` with your lab-specific details.

---

# [EMOJI] HACKING LABS - LAB-###: [Vulnerability Name] Challenge

**[One-sentence description of the lab and what it teaches]**

---

## 📋 **Tentang Challenge Ini**

| Detail | Info |
|--------|------|
| **Nama** | LAB-###: [Vulnerability Name] |
| **Tipe** | Hands-on Practical Lab |
| **Vulnerability** | [Vulnerability Name] (CWE-###) |
| **Framework** | Python Flask |
| **Deployment** | Docker + Docker Compose |
| **Difficulty** | ⭐⭐ [Easy-Medium / Medium-Hard] |
| **Time to Solve** | [15-30 / 30-45] menit |
| **Objective** | [What the participant needs to do] |

### 🎯 Learning Objectives
- ✅ [Learning objective 1]
- ✅ [Learning objective 2]
- ✅ [Learning objective 3]
- ✅ [Learning objective 4]
- ✅ [Learning objective 5]

---

## 🚀 **CARA DEPLOY (3 Menit)**

### Prerequisites
```bash
docker --version
docker-compose --version
```

### Step 1: Clone Repository
```bash
git clone https://github.com/vanderstark/hacking-lab-lab###-[slug].git
cd hacking-lab-lab###-[slug]
```

### Step 2: Deploy
```bash
docker-compose up -d
sleep 10  # Tunggu container start
```

### Step 3: Akses Challenge
```
🌐 http://localhost:PORT
```

**Status Check:**
```bash
docker-compose ps
# Expected: State should be "healthy"
```

---

## 🔐 **Demo Credentials / Info**

[If applicable, add credentials table or demo data]

| Item | Value |
|------|-------|
| Username | [demo username] |
| Password | [demo password] |
| Demo IP | [demo IP] |

---

## 💡 **CARA MENJAWAB / SOLUSI (Step-by-Step)**

### 🔍 **Langkah 1: Eksplorasi Aplikasi**

[Describe how to explore the app, what to look for. **Explain WHY the vulnerability exists, not just WHAT it is.**]

### 🔍 **Langkah 2: Identifikasi Kerentanan**

[Explain what vulnerability to look for and **WHY it's exploitable.**]

### 🔍 **Langkah 3: Craft Exploitation Payload**

[Show the payload structure and **WHY it works.**]

```
Payload: [example payload]
URL: http://localhost:PORT/endpoint
```

### 🔍 **Langkah 4: Execute Exploit**

[Step-by-step execution with explanation of what happens at each step.]

### 🔍 **Langkah 5: Get Flag**

**Expected Output:**
```
[expected output showing flag]
```

---

## 🌐 **Multiple Exploitation Methods**

### **Method 1: [Technique Name]**
```bash
[Technique 1 example - Python / curl / online tool]
```

### **Method 2: [Technique Name]**
```bash
[Technique 2 example]
```

### **Method 3: [Technique Name]**
```bash
[Technique 3 example]
```

### **Method 4: [Technique Name]**
```bash
[Technique 4 example]
```

---

## 🛡️ **Cara Memperbaiki Kerentanan**

### ❌ VULNERABLE CODE
```python
# Show vulnerable code
```

### ✅ SECURE CODE
```python
# Show secure code fix
```

---

## 🔧 **TROUBLESHOOTING**

### ❌ Issue 1: [Common Issue]
**Solution:** [Explicit fix]

### ❌ Issue 2: [Common Issue]
**Solution:** [Explicit fix]

### ❌ Issue 3: Port conflicts
```bash
# Port 5003 already in use?
lsof -i :5003
kill -9 <PID>
```

### ❌ Issue 4: Container won't start
```bash
docker-compose logs -f --tail=20
docker-compose down -v
docker-compose up -d
```

### ❌ Issue 5: Healthcheck fails
```bash
# Check if app is running
curl http://localhost:5003/health
# If timeout, check if Flask app crashes
docker-compose logs
```

### ❌ Issue 6: [Lab-specific issue]
**Solution:** [Explicit fix]

### ❌ Issue 7: [Lab-specific issue]
**Solution:** [Explicit fix]

---

## 📁 **STRUKTUR FILE**

```
lab-###-[vulnerability]/
├── Dockerfile              # Container image
├── app.py                  # Flask application
├── docker-compose.yml      # Container orchestration
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Interactive frontend
└── README.md               # This documentation
```

---

## 📊 **Soal & Flag**

**Tugas:**
1. [Task 1]
2. [Task 2]
3. [Task 3]

**Flag:** `HACKING_LAB{[flag_content]}`

---

## 🎯 **LAB SERIES STATUS**

| Lab | Vulnerability | Port | Status |
|-----|---------------|------|--------|
| 001 | SQL Injection | 5000 | ✅ Live |
| 002 | XSS Reflected | 5001 | ✅ Live |
| 003 | Command Injection | 5002 | ✅ Live |
| 004 | Path Traversal | 5003 | ✅ Live |
| 005 | JWT Bypass | 5004 | ✅ Live |
| **###** | **[Current Lab]** | **[Port]** | **✅ Live** |

---

## 📞 Support

Buka **Issues** di repository GitHub jika ada masalah teknis.

---

**Happy Hacking! 🔥**

*Generated: [Date] | Version: 1.0 | Status: Production Ready*

**⚠️ LEGAL DISCLAIMER**

Challenge ini **hanya untuk tujuan edukasi**! 
- Jangan pakai untuk serangan terhadap sistem orang lain
- Gunakan hanya di environment yang diotorisasi
- Patuhi UU ITE dan ethical hacking guidelines
