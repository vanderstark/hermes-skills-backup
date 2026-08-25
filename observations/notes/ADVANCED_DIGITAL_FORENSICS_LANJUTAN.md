# 🕵️ Advanced Digital Forensics & Malware Analysis: Analisis Barang Bukti Digital

**Skill dasar:** `cybersecurity/malware-analysis`  
**Kategori:** Cybersecurity / Forensik  
**Target:** Reskrim, Intelkam  
**Bahasa:** Indonesian

---

## 🎯 Ringkasan Skill

Digital forensics melacak jejak digital sebagaimana jejak kaki di Tanah Air. Skills utama:

1.  **Memory Dumping** — Ambil isi RAM dari perangkat yang dijahsi
2.  **Malware Sandbox** — Jalankan file mencurigakan di lingkungan terisolasi
3.  **Network Traffic Analysis** — Lihat komunikasi malware ke server Command & Control (C2)

---

## 🔧 Tools Utama yang Perlu Dipelajari

| Tool | Fungsi |
|---|---|
| **Volatility 3** | Analisis memory dump (proses, jaringan, registry) |
| **Wireshark** | Penyadapan paket jaringan malware |
| **Cuckoo Sandbox** | Otomatisasi analisis malware |
| **YARA** | Deteksi malware berdasarkan pola (signature) |
| **Strings** | Ekstrak string ASCII/UTF di file biner |
| **PEStudio** | Analisis cepat file PE (exe/dll) di Windows |

---

## 📋 Use Case untuk Reskrim

| Kasus | Tools yang Dipakai | Hasil |
|---|---|---|
| Ransomware di korban | Volatility 3 + Wireshark | Ditemukan IP C2, file yang dienkripsi |
| Keylogger pada laptop polisi | Cuckoo + YARA | Diketahui software pencuri kata sandi |
| Pencurian data oleh insider | Registry dump + Network log | Pelacakan login tidak sah |

---

## 🧪 Workflow Analisis Malware (Prinsip 4-Fase)

### Fase 1: Static Analysis (Tanpa Jalankan File)
```
# 1. Check hash (MD5/SHA256) di VirusTotal
strings malware.exe | grep -E "(http|https|\.com|\.net)"  # cari URL
pestudio.exe malware.exe  # analisis properti file
```

### Fase 2: Dynamic Analysis (Jalankan di Sandbox)
```
# 1. Jalankan di Cuckoo Sandbox
# 2. Pantau network traffic (squid proxy + suricata)
# 3. Analisis files yang dibuat / diubah
```

### Fase 3: Memory Analysis
```
# 1. Capture memory via FTK Imager / Volatility
vol -f mem.dmp windows.pslist  # lihat proses
vol -f mem.dmp netstat  # lihat koneksi jaringan
```

### Fase 4: Network Traffic Analysis
```
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.user_agent
```

---

## 📋 Checklist Tugas Akhir yang Harus Dipertahankan

- [ ] Hash barang bukti (MD5, SHA256)
- [ ] Chain of custody (dokumentasi siapa sentuh file)
- [ ] Timestamp akurat (Waktu analisis vs Waktu log sistem)
- [ ] Laporan akhir dengan screenshot/teardown langkah-langkah

---

**Status:** Siap kerja  
**Next Step:** Praktikum dengan sample malware benign (seperti `eicar.com` untuk test YARA/Cuckoo)
