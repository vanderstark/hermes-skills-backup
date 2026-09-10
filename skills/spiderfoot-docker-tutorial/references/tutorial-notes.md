# SpiderFoot Docker - Catatan Praktis

## A. Akses & Login

- **URL Antarmuka:** `http://localhost:5000`
- **Mencari Kredensial:** Setelah container pertama kali dijalankan, jalankan perintah berikut di terminal host untuk melihat email dan password yang otomatis dibuat:

  ```bash
  docker logs spiderfoot 2>&1 | grep -i -E "email|password|admin|user"
  ```

  *Catatan: Outputnya akan berupa baris seperti `Set admin account: admin@spiderfoot.net / sf_admin_password` atau sekelompok baris yang mirip. Gunakan kredensial tersebut untuk login.*

- **Login Awal:** Masukkan email dan password di halaman login SpiderFoot. Jika lupa, ulangi perintah `docker logs spiderfront` untuk meregenerasi informasi (atau `docker restart spiderfront` lalu lihat logs kembali).

## B. Menambah Target Pembersihan

1. Setelah login, di panel kiri pilih **`Add Target`** (atau ikon `+`).
2. Masukkan nilai di kolom **`Target`**:
   - **Domain:** contoh: `example.com`
   - **IP Address:** contoh: `8.8.8.8`
   - **Subdomain:** contoh: `login.example.com` (opsional)
3. Klik **`Add`** — SpiderFoot akan secara otomatis memulai pemindai menggunakan 400+ modul tersedia.
4. Status target akan berubah dari `Pending` ke `Scanning`, dan akhirnya ke `Completed` saat selesai.

## C. Mengaktifkan & Mengonfigurasi Modul

1. Dari panel utama, klik **`Management`** lalu pilih **`Modules`**.
2. Anda akan melihat daftar modul terbagi kategori:
   - **Network** — pemindaian port, nmap, service detection
   - **SSL/TLS** — analisis sertifikat, SSL/TLS handshake
   - **Email** — pemindaian phishing, enumerasi email
   - **Malware** — pencarian malware, VirusTotal integration
   - **Social** —Twitter, LinkedIn, crawling jejaring sosial
   - dll. (total >400 modul)
3. **Cara Mengaktifkan:**
   - Centang (check) kotak di setiap baris modul yang ingin aktif.
   - **Catatan:** Modul default sudah aktif sebagian. Anda bisa mengaktifkan semua dengan menekan tombol **`Select All`** di atas daftar, lalu **`Save`**.
4. Setelah memilih, scroll ke bawah dan klik **`Save`** untuk mengonfigurasi.
5. Modul yang diaktifkan akan langsung berjalan pada pemindaian target selanjutnya (atau pada target yang sedang scannings jika masih berjalan).

### Contoh: Aktifkan Modul Phishing & Port Scan

Cari baris:
- `SF phishing` (di bawah kategori Email)
- `SF portscan` (di bawah kategori Network)

Centang kedua kotak tersebut, lalu scroll ke bawah dan klik **Save**. Modul ini akan berjalan saat target diminda lagi atau saat di-refresh.

## D. Melihat & Mengekspor Hasil

1. Klik tab **`Results`** di panel utama.
2. Hasil akan muncul dalam format tree/structured kiri, dengan detail kanan.
3. **Filter:** Gunakan kotak pencarian bagian atas untuk menfilter berdasarkan modul, host, atau nilai.
4. **Eksportasi:**
   - Klik tombol **`Export`** di kanan atas.
   - Pilih format: `JSON`, `CSV`, atau `HTML`.
   - File akan diunduh ke komputer lokal.

### Tips Membaca Hasil

- **Domain/Subdomain:** Muncul di kolom `Host`. Anda bisa mengklik untuk melihat subdomain terkait.
- **IP Address:** Muncul di kolom `IP`. Berguna untuk menemukan host lain di jaringan sama.
- **CVE/Vuln:** Jika ditemukan, akan muncul di kolom `Vulnerabilities` dengan detail CVE ID dan deskripsi singkat.
- **Phishing:** Jika modul `SF phishing` diaktifkan, hasil akan berisi skor kepercayaan (`phishing score`) dan alasan mendukungnya.

## E. Backup & Maintenance

### 1. Backup Data SpiderFoot

Data pengetahuan (knowledge base) SpiderFoot disimpan di volume Docker bernama `spiderfoot_data`. Untuk backup:

```bash
# Dari host terminal
docker cp spiderfoot:/.sf_data /path/on/host/spiderfoot_backup_$(date +%Y%m%d).dump
```

Lalu simpan file `.dump` tersebut di lokasi yang aman. Untuk restore:

```bash
# Stop container terlebih dahulu
docker-compose down

# Pindahkan file backup ke volume
docker cp /path/on/host/spiderfoot_backup_*.dump spiderfoot:/.sf_data

# Start kembali
docker-compose up -d
```

### 2. Perbarui ke Versi Terbaru

```bash
# Stop dan ambil ulang citra terbaru
docker-compose down
docker-compose pull
docker-compose up -d --build
```

### 3. Lihat Log untuk Troubleshooting

```bash
# Log real-time
docker logs -f spiderfoot

# Log hanya 50 baris terakhir
docker logs spiderfoot | tail -50

# Cari error terkait modul
docker logs spiderfoot 2>&1 | grep -i "error\|fail\|timeout"
```

## FAQ & Troubleshooting

### Q: "Saya lupa password login-nya, bagaimana?"

A: Jalankan `docker logs spiderfoot` dan cari baris yang berisi "Set admin account" atau "email"/"password". Atau `docker restart spiderfoot` lalu lihat logs lagi.

### Q: "SpiderFoot tidak bisa menjalankan modul tertentu."

A: Pastikan:
- Docker memiliki cukup memori (minimal 512MB, disarankan 1GB+).
- Port `5000` tidak digunakan lain di host.
- Modul tertentu membutuhkan izin tambahan atau koneksi internet ke layanan eksternal (seperti VirusTotal). Nonaktifkan jika diblokir.

### Q: "Bagaimana cara mengganti email/password default?"

A: Edit file `docker-compose.yml` dan ubah nilai `SF_EMAIL` dan `SF_PASSWORD`. Lalu `docker-compose up -d --build` ulang.

### Q: "Bisa dijalankan di arsitektur ARM (Raspberry Pi)?"

A: Iya, gambar `smicallef/spiderfoot` mendukung arsitektur multi (amd64, arm64, dll.). Pastikan `docker-compose.yml` tidak men-specify arsitektur spesifik (ia akan otomatis sesuai hardware host).

---

**Catatan Penting:** SpiderFoot diprogettikan untuk OSINT bertanggung jawab. Selalu peroleh izin yang tepat sebelum meminda target yang bukan milik Anda. Penyesuaian hukum dan etika lokal adalah tanggung jawab pengguna.

---

**Versi:** 1.0.0  
**Dibuat:** tanggal sesi ini  
**Oleh:** Hermes Agent - Nous Research  
**Skill:** spiderfoot-docker-tutorial