# Day 021 - Codebase Line Counter & Directory Tree CLI

Utilitas berbasis terminal untuk memvisualisasikan struktur direktori proyek dan menghitung statistik baris kode berdasarkan bahasa pemrograman.

## Fitur
- **Language Breakdown:** Mengelompokkan jumlah file, baris kode efektif, komentar, dan baris kosong berdasarkan ekstensi file (`.py`, `.js`, `.ts`, `.c`, `.html`, `.css`, `.md`, dll.).
- **Visual Directory Tree:** Menampilkan hierarki folder dan file dengan karakter pohon ASCII (`├──`, `└──`).
- **Smart Directory Filtering:** Otomatis mengabaikan direktori non-sumber seperti `.git`, `__pycache__`, `.venv`, dan `node_modules`.
- **JSON Summary Export:** Menyimpan hasil analisis codebase ke file `code_stats.json`.

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py