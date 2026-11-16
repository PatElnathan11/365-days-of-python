# Day 018 - Local URL Shortener & Redirect Server

Aplikasi pemendek URL berbasis CLI dan server HTTP lokal menggunakan database SQLite untuk menyimpan tautan serta melacak statistik klik.

## Fitur

- **Generate Short Code:** Membuat kode pendek acak 6 karakter yang unik untuk setiap URL.
- **Custom Alias:** Mendukung pembuatan nama alias kustom (misal: `http://localhost:8000/github`).
- **Built-in Redirect Server:** Server HTTP lokal yang langsung mengarahkan browser (`302 Found`) ke URL tujuan.
- **Click Analytics:** Menghitung dan menampilkan jumlah klik untuk setiap tautan pendek.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
