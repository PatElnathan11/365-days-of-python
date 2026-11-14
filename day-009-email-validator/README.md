# Day 009 - Bulk Email Validator CLI

Script Python untuk memvalidasi alamat email secara massal berdasarkan sintaks format dan keberadaan domain/server mail.

## Fitur
- **Syntax Validation:** Memeriksa struktur email (karakter valid, simbol `@`, dan ekstensi domain) menggunakan Regex.
- **Domain Verification:** Memeriksa keberadaan DNS domain server menggunakan modul `socket`.
- **Bulk Processing:** Membaca daftar email dari file `.txt` atau `.csv`.
- **Export Result:** Menyimpan laporan hasil validasi ke file JSON.

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py