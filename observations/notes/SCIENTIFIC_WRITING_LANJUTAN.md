# ✍️ Scientific Writing: Materi Lanjutan untuk Bos

**Skill dasar:** `research-paper-writing` (Research Paper Writing Pipeline, MIT license)
**Kategori:** Research & Scientific Communication
**Target:** Penulisan naskah teknis/buku (Academy Polri) & paper ilmiah

---

## 🎯 Ringkasan Skill

Pipeline end-to-end untuk menulis paper riset ML/AI yang siap publikasi (target: NeurIPS, ICML, ICLR, ACL, AAAI, COLM) — tapi strukturnya sama persis dipakai untuk buku teknis/akademik Polri. Ini **bukan pipeline linear** — iteratif: hasil eksperimen memicu eksperimen baru, review memicu revisi.

**Dependencies:** semanticscholar, arxiv, habanero, requests, scipy, numpy, matplotlib, SciencePlots

---

## 📚 Alur Kerja (Design → Submit)

### Tahap 1: Desain & Perencanaan
- Rumuskan pertanyaan riset yang jelas & spesifik
- Cari 3-5 paper fondasi (pakai skill `arxiv` untuk searching)
- Identifikasi gap yang belum ditangani literatur

### Tahap 2: Eksperimen & Analisis
- Desain eksperimen terukur
- Jalankan & monitor eksperimen (data collection terstruktur)
- Analisis statistik (scipy/numpy) — jangan asal klaim tanpa uji signifikansi

### Tahap 3: Penulisan Naskah
Struktur standar (dipakai untuk buku Bos juga):
```
1. Judul — spesifik, cerminkan kontribusi
2. Abstrak (150-300 kata): masalah → metodologi → temuan → implikasi
3. Pendahuluan: latar belakang, rumusan masalah, kontribusi
4. Tinjauan Pustaka: 3-5 paper utama, gap analysis
5. Metodologi: desain, data, tools yang dipakai
6. Hasil & Diskusi: data + interpretasi + kaitan literatur
7. Kesimpulan & Saran: ringkasan, batasan, future work
8. Daftar Pustaka (format IEEE/APA/ACM — konsisten!)
```

### Tahap 4: Review & Revisi (Loop Iteratif)
- Self-review pakai checklist (lihat bawah)
- Simulasikan review reviewer (skeptis, cari kelemahan metodologi)
- Revisi berdasarkan feedback — ini bisa berulang beberapa kali

### Tahap 5: Submit
- Cek format sesuai target (jurnal/konferensi/portal academy)
- Sitasi & referensi lengkap dan konsisten
- LaTeX untuk publikasi formal (kalau target jurnal internasional)

---

## ✅ Checklist Final Sebelum Submit

- [ ] Judul mencerminkan kontribusi utama
- [ ] Abstrak mencakup 4 elemen: why, how, what, so what
- [ ] Setiap gambar/tabel punya caption & nomor jelas
- [ ] Referensi konsisten formatnya (jangan campur APA+IEEE)
- [ ] Tidak ada jargon berlebihan tanpa penjelasan
- [ ] Ada bagian "Limitations" & "Future Work" — jujur soal batasan
- [ ] Klaim statistik didukung uji signifikansi, bukan asumsi

---

## 💡 Penerapan untuk Bos (Buku & Dokumen Academy Polri)

1. **Gunakan struktur yang sama** untuk buku teknis — cuma ganti "paper" jadi "bab", target audiens jadi peserta didik Academy.
2. **Pakai skill `arxiv`** untuk riset literatur pendukung (state-of-the-art AI/OSINT untuk konteks keamanan siber).
3. **Loop iteratif penting** — jangan tulis linear dari Bab 1 sampai selesai; tulis outline dulu, isi tiap bagian secara paralel, lalu revisi menyeluruh.
4. **Related skills:** `arxiv` (cari referensi), `subagent-driven-development` (delegasi riset paralel), `plan` (breakdown penulisan jadi tahapan terkelola).

---

**Status:** Siap dipakai untuk draft buku/paper Bos
**Next Step:** Mulai dari outline 1 halaman → breakdown per bab → drafting paralel
