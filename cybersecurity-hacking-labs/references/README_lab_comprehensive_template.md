# Comprehensive README Template for Hacking Labs (058-068 pattern)

This is the standardized README template used for LAB-058 through LAB-068 and all future labs in this series.

---

## Required Sections (in order)

### 1. Header & Metadata Table
```markdown
# 🔄 HACKING LABS - LAB-XXX: [Vulnerability Name]

**Praktikum: [One-line description of vulnerability] (CWE-XXX)**

---

## 📋 **Tentang Challenge Ini**

| Detail | Info |
|--------|------|
| **Nama** | LAB-XXX: [Vulnerability Name] |
| **Vulnerability** | [Full name + CWE] |
| **OWASP** | [Category] |
| **Framework** | Python Flask |
| **Difficulty** | ⭐⭐ [Easy/Medium/Hard] |
| **Time to Solve** | XX menit |
| **Objective** | [What the player must achieve] |
```

### 2. Deploy Guide (3 Minutes)
```markdown
## 🚀 **CARA DEPLOY (3 Menit — Untuk Pemula!)**

```bash
git clone https://github.com/vanderstark/hacking-lab-labXXX-vulnname.git
cd hacking-lab-labXXX-vulnname
docker-compose up -d
sleep 10
```

**Akses:** `http://localhost:XXXX`

```markdown
### Step-by-step breakdown:
- **Langkah 1:** Clone repository
- **Langkah 2:** Masuk ke folder
- **Langkah 3:** Jalankan Docker Compose
- **Langkah 4:** Tunggu container ready
- **Langkah 5:** Cek status container
- **Langkah 6:** Akses challenge di browser
```

### 3. Tutorial 5-Step (Bahasa Indonesia, Beginner-Friendly)
```markdown
## 💡 **TUTORIAL STEP-BY-STEP (Untuk Pemula)**

### 🔍 **Langkah 1: Eksplorasi Awal**
[Open homepage, check /hint endpoint, understand the app]

### 🔍 **Langkah 2: Cek Versi Aman / Normal Flow**
[Test the secured/normal endpoint to show it's protected]

### 🔍 **Langkah 3: Coba Versi Rentan / Eksploitasi**
[The actual exploit - show vulnerable endpoint]

### 🔍 **Langkah 4: Verifikasi & Capture Flag**
[Get the flag from response]

### 🔍 **Langkah 5: Submit Flag**
**🚩 FLAG:** `HACKING_LAB{...}`
```

### 4. Real-World Impact
```markdown
## ⚡ **Real-World Impact (Contoh Nyata di Dunia)**

| Kasus | Tahun | Dampak |
|-------|-------|--------|
| [Company/Service] | 20XX | [What happened] |
```

### 5. Secure Code Comparison
```markdown
## 🛡️ **Cara Memperbaiki Oleh Developer (Best Practice)**

### ❌ **KODE VULNERABLE**
```python
# Vulnerable code with comments explaining WHY it's vulnerable
```

### ✅ **SECURE CODE**
```python
# Fixed code with comments explaining the fix
```

### ✅ **Best Practice Tambahan**
[Additional recommendations]
```

### 6. Troubleshooting
```markdown
## 🔧 **Troubleshooting / Troubleshooting**

```bash
# 1. Lihat log container
docker-compose logs -f

# 2. Restart container
docker-compose down && docker-compose up -d

# 3. Cek port sudah terpakai
docker ps | grep XXXX

# 4. Cek health endpoint
curl http://localhost:XXXX/health
```
```

### 7. File Structure
```markdown
## 📁 **Struktur File Lab**

```
hacking-lab-labXXX-vulnname/
├── app.py                 # Flask app
├── templates/
│   └── index.html         # UI web
├── requirements.txt       # Dependencies
├── Dockerfile            # Python image
├── docker-compose.yml    # Container config
└── README.md             # Dokumentasi
```
```

### 8. Flag & References
```markdown
## 🎯 **Hack The Flag**

**Submit:** `HACKING_LAB{...}`

---

## 📚 **Referensi Tambahan**

- [OWASP link]
- [CWE link]
- [Other resources]
```

---

## Key Principles Applied

1. **Indonesian language** throughout
2. **5-step format:** Eksplorasi → Exploit → Verifikasi → Capture Flag → Submit
3. **Explain WHY** exploits work, not just WHAT to do
4. **Code comparison:** ❌ Vulnerable vs ✅ Secure side-by-side
5. **Copy-paste ready** curl/python commands
6. **Beginner-friendly** tone with step-by-step breakdown
7. **Consistent flag format:** `HACKING_LAB{...}`
8. **Health endpoint** check included
9. **Docker troubleshooting** commands
10. **File structure** diagram

---

## Usage

When creating a new lab:
1. Copy this template
2. Fill in lab-specific details (vulnerability name, port, flag, commands)
3. Keep all section headers and structure identical
4. Ensure code blocks are correct and tested
5. Save as `README.md` in lab directory
6. **Immediately git commit + push** to GitHub