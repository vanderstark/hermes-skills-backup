# 🔍 Hermes OSINT Toolkit Setup Guide

**Date:** August 16, 2026  
**Status:** ✅ INSTALLED & OPERATIONAL  
**Location:** `/opt/data/osint/`

---

## 📦 **Installed Tools**

| # | Tool | Type | Status | Command |
|---|------|------|--------|---------|
| 1 | **Sherlock** | Username Search | ✅ pip | `sherlock USERNAME` |
| 2 | **theHarvester** | Email/Subdomain | ✅ git | `python3 theHarvester/theHarvester.py` |
| 3 | **SpiderFoot** | Reconnaissance | ✅ git | `python3 spiderfoot/sf.py` |
| 4 | **Shodan CLI** | Internet Search | ✅ pip | `shodan search QUERY` |
| 5 | **Exiftool** | Metadata Extract | ✅ pip | `exiftool IMAGE.jpg` |
| 6 | **DNSPYTHON** | DNS Lookup | ✅ pip | `python3 -c "import dns.resolver"` |

---

## 🚀 **Quick Start Examples**

### **1. Sherlock — Find Username Across Internet**
```bash
cd /opt/data/osint
sherlock username123
# Output: Finds username on Twitter, Instagram, GitHub, etc.
```

### **2. theHarvester — Extract Emails & Subdomains**
```bash
cd /opt/data/osint/theHarvester
python3 theHarvester.py -d example.com -b google
# Output: emails, subdomains from domain
```

### **3. SpiderFoot — Automated Reconnaissance**
```bash
cd /opt/data/osint/spiderfoot
python3 sf.py -m sfp_dns,sfp_google -t example.com
# Output: Full reconnaissance report
```

### **4. Shodan CLI — Internet Device Search**
```bash
shodan init YOUR_API_KEY  # Get from shodan.io (free tier available)
shodan search "apache server"
# Output: Exposed devices on internet
```

### **5. Exiftool — Extract Image Metadata**
```bash
exiftool photo.jpg
# Output: GPS coordinates, camera model, timestamps
```

---

## 📊 **Directory Structure**

```
/opt/data/osint/
├── sherlock/              (pip installed)
├── theHarvester/          (git cloned)
│   ├── theHarvester.py
│   ├── requirements.txt
│   └── [modules]
├── spiderfoot/            (git cloned)
│   ├── sf.py
│   ├── requirements.txt
│   └── [modules]
└── [config files]
```

---

## ⚖️ **Legal & Ethical Guidelines**

### ✅ **AUTHORIZED USES:**
- Security research (with permission)
- Academic investigation
- Due diligence (job screening)
- Cybersecurity incident response
- Authorized penetration testing

### ❌ **PROHIBITED USES:**
- Doxxing / public harassment
- Stalking / surveillance (without consent)
- Identity theft
- Unauthorized data collection
- Violating GDPR / CCPA / Indonesia ITE Law

**⚠️ REMINDER:** Indonesia UU ITE Pasal 27-28 → unauthorized access = criminal penalty

---

## 🔧 **Configuration**

### **Sherlock Config** (optional)
```bash
sherlock --help  # View all options
sherlock -o results.txt username  # Save to file
sherlock -t 20 username  # Set timeout (seconds)
```

### **theHarvester Config**
```bash
python3 theHarvester.py -h  # View all options
# Common sources: google, bing, linkedin, twitter
```

### **SpiderFoot Config**
```bash
python3 sf.py -l  # List all modules
python3 sf.py -m MODULE1,MODULE2 -t TARGET
```

### **Shodan Config**
```bash
shodan init API_KEY
shodan info  # Show account info
shodan search --help  # Search options
```

---

## 📝 **Integration with Hermes Skills**

These OSINT tools can be wrapped as Hermes skills for automated profiling:

### **Skill 1: osint-username-search**
```python
# Usage: hermes run osint-username-search --username john_doe
# Returns: List of social profiles
```

### **Skill 2: osint-email-harvester**
```python
# Usage: hermes run osint-email-harvester --domain example.com
# Returns: Email list + subdomain report
```

### **Skill 3: osint-recon-full**
```python
# Usage: hermes run osint-recon-full --target example.com
# Returns: Full reconnaissance report
```

---

## 🛠️ **Troubleshooting**

| Issue | Solution |
|-------|----------|
| **Sherlock: Module not found** | `pip install --upgrade sherlock-project` |
| **theHarvester: API error** | Check internet connection, may need API key |
| **SpiderFoot: Requirements missing** | `pip install -r spiderfoot/requirements.txt` |
| **Shodan: No results** | Register free account at shodan.io for API key |
| **Exiftool: Command not found** | `pip install exiftool` or `apt install exiftool` |

---

## 📚 **References**

- Sherlock: https://github.com/sherlock-project/sherlock
- theHarvester: https://github.com/laramies/theHarvester
- SpiderFoot: https://github.com/smicallef/spiderfoot
- Shodan: https://www.shodan.io
- Exiftool: https://exiftool.org

---

## ✅ **Verification**

All tools installed and tested ✅:
- Sherlock ✅
- theHarvester ✅
- SpiderFoot ✅
- Shodan CLI ✅
- Exiftool ✅

**Ready for OSINT investigation work!**

---

**Repository:** /opt/data/osint/  
**Last Updated:** August 16, 2026  
**Status:** ✅ OPERATIONAL
