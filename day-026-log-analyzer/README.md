# Day 026 - Server Log Analyzer & Error Tracker CLI

Utilitas berbasis terminal untuk mem-parsing file log server, menghitung distribusi tingkat keparahan log, melacak error berulang, dan memfilter catatan aktivitas.

## Fitur

- **Log Pattern Parsing:** Mengekstrak timestamp, log level, nama layanan (_service_), dan pesan log menggunakan _Regular Expressions_.
- **Severity Breakdown:** Menghitung jumlah dan persentase kemunculan `INFO`, `WARNING`, `ERROR`, dan `CRITICAL`.
- **Top Recurring Errors:** Mengidentifikasi pesan error atau critical yang paling sering terjadi beserta layanan sumbernya.
- **Interactive Log Filter:** Memfilter baris log berdasarkan level tertentu atau kata kunci pencarian.
- **JSON Report Export:** Menyimpan ringkasan hasil audit log ke file `log_report.json`.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
