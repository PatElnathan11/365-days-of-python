# Day 027 - SSL/TLS Certificate Expiry & Domain Checker CLI

Utilitas keamanan berbasis terminal untuk memeriksa masa berlaku sertifikat SSL/TLS, informasi penerbit (CA), dan status validitas domain HTTPS.

## Fitur
- **Live TLS Handshake Inspection:** Mengambil sertifikat X.509 langsung dari server port `443`.
- **Expiry Countdown:** Menghitung sisa hari sebelum sertifikat kedaluwarsa dan memberi peringatan jika kurang dari 30 hari.
- **Certificate Metadata:** Menampilkan nama penerbit (*Issuer*), subjek domain, dan rentang tanggal berlaku.
- **Batch Domain Audit:** Memeriksa daftar domain dari file `domains.txt` dan menyimpan laporan ke `ssl_report.json`.

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py