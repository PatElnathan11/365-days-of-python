# Day 015 - Multi-Threaded Port Scanner CLI

Utilitas jaringan berbasis terminal untuk mendeteksi port TCP yang terbuka pada suatu host atau IP address menggunakan _multi-threading_.

## Fitur

- **Fast Multi-Threaded Scanning:** Memanfaatkan `ThreadPoolExecutor` untuk memindai ratusan port dalam hitungan detik.
- **Service Identification:** Mendeteksi nama layanan standar (HTTP, HTTPS, SSH, MySQL, dll.) berdasarkan nomor port.
- **Preset & Custom Range:** Pilihan memindai port umum (_common ports_) atau rentang port kustom.
- **DNS Resolution:** Otomatis menerjemahkan nama domain ke alamat IPv4.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
