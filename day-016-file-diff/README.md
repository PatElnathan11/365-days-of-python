# Day 016 - File Diff & Comparator CLI

Utilitas berbasis terminal untuk membandingkan dua file teks atau kode sumber, menampilkan perubahan baris demi baris, serta membuat laporan visual HTML.

## Fitur

- **Unified Diff dengan Warna Terminal:** Menampilkan baris yang ditambah (hijau), dihapus (merah), dan posisi perubahan (cyan).
- **Similarity Ratio:** Menghitung persentase kemiripan antara dua file menggunakan `SequenceMatcher`.
- **HTML Side-by-Side Export:** Menghasilkan laporan perbandingan visual berdampingan (`diff_report.html`) yang bisa dibuka di browser.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
