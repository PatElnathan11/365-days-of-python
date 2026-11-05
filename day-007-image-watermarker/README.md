# Day 007 - Image Resizer & Watermarker CLI

Script Python untuk memproses gambar secara massal: meresize dimensi gambar dan menambahkan watermark teks transparan di pojok gambar.

## Fitur
- Resize gambar massal berdasarkan persentase atau lebar maksimum (mempertahankan rasio aspek).
- Menambahkan watermark teks dengan transparansi/opacity khusus.
- Mendukung format `.jpg`, `.jpeg`, `.png`, dan `.webp`.
- Menyimpan hasil ke folder `output/` tanpa merusak file asli.

## Persyaratan
Install library `Pillow`:
```bash
pip install Pillow