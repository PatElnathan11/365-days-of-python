# Day 025 - JSON & CSV Format Converter CLI

Utilitas berbasis terminal untuk mengonversi data dua arah antara format JSON dan CSV secara otomatis dengan deteksi header dan tipe data.

## Fitur

- **JSON to CSV:** Mengubah daftar objek JSON menjadi tabel CSV dengan deteksi seluruh kunci (_keys_) secara menyeluruh.
- **CSV to JSON with Type Inference:** Mengonversi baris CSV menjadi JSON terstruktur sekaligus mengembalikan tipe data angka (`int`/`float`) dan boolean (`true`/`false`).
- **Terminal Table Preview:** Menampilkan cuplikan isi data dalam bentuk tabel rapi sebelum atau sesudah konversi.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
