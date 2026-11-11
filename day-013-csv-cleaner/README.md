# Day 013 - CSV Data Filter & Cleaner CLI

Script Python untuk melakukan *data cleaning* awal pada file CSV tanpa memerlukan library pihak ketiga seperti Pandas.

## Fitur
- **Trim Whitespace:** Menghapus spasi berlebih di awal dan akhir teks pada setiap sel data.
- **Deduplikasi:** Menghapus baris yang identik/duplikat.
- **Handling Missing Values:** Opsi untuk mengabaikan atau mengedit baris dengan nilai kosong.
- **Export Data:** Menyimpan hasil pembersihan ke file CSV baru (`cleaned_output.csv`).

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py