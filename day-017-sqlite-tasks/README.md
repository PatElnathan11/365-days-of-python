# Day 017 - SQLite Task Manager CLI

Aplikasi manajemen tugas berbasis terminal menggunakan database relasional SQLite untuk penyimpanan data lokal yang cepat dan persisten.

## Fitur

- **Operasi CRUD Lengkap:** Tambah tugas baru, lihat daftar tugas, tandai selesai, cari berdasarkan kata kunci, dan hapus tugas.
- **Tingkat Prioritas:** Pengelompokan tugas berdasarkan prioritas (`High`, `Medium`, `Low`).
- **Database Lokal Otomatis:** Membuat file database `tasks.db` dan tabel secara otomatis saat pertama kali dijalankan.
- **Keamanan Kueri:** Menggunakan _parameterized queries_ (`?`) untuk mencegah _SQL Injection_.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
