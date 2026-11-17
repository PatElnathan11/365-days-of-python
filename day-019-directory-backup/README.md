# Day 019 - Automated Directory Backup & Restore CLI

Utilitas berbasis terminal untuk mencadangkan direktori kerja ke dalam arsip ZIP terkompresi dan memulihkannya kembali dengan mudah.

## Fitur

- **Smart Exclusion:** Otomatis melewati folder `.git`, `__pycache__`, `.venv`, dan `node_modules` agar ukuran backup tetap ringkas.
- **Timestamped Archives:** Penamaan file cadangan otomatis berdasarkan tanggal dan waktu pembuatan (`backup_YYYYMMDD_HHMMSS.zip`).
- **Backup History Log:** Mencatat seluruh riwayat backup (ukuran file, jumlah file, dan lokasi sumber) ke `backup_history.json`.
- **Built-in Restore:** Memungkinkan pemilihan dan ekstraksi file backup langsung dari menu CLI.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
