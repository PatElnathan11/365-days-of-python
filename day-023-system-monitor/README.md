# Day 023 - System Resource & Process Monitor CLI

Utilitas pemantau spesifikasi sistem, penggunaan ruang penyimpanan, dan daftar proses aktif berbasis terminal tanpa dependensi eksternal.

## Fitur

- **System & Hardware Overview:** Menampilkan informasi sistem operasi, arsitektur prosesor, hostname, dan jumlah logical CPU core.
- **Disk Usage Visualizer:** Menghitung total, terpakai, dan sisa kapasitas disk lengkap dengan grafik batang ASCII.
- **Top Memory Processes:** Mengambil daftar proses aktif dan mengurutkannya berdasarkan penggunaan memori (RAM) tertinggi.
- **Snapshot Report Export:** Menyimpan hasil pemantauan sistem ke dalam file `system_snapshot.json`.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
