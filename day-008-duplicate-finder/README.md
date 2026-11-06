# Day 008 - Duplicate File Finder

Script Python untuk mendeteksi dan mengeliminasi file duplikat di dalam direktori menggunakan hashing MD5 secara sekuensial.

## Fitur
- Pemindaian file rekursif di seluruh sub-folder.
- Deteksi duplikat berbasis isi file (hashing MD5), bukan nama file.
- Pembacaan file bertahap (*chunk-based reading*) agar hemat penggunaan RAM saat memproses file berukuran besar.
- Menampilkan daftar file duplikat & opsi untuk menghapus file salinan secara aman.

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py