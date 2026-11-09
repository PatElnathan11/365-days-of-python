# Day 011 - Website Uptime & Latency Monitor CLI

Script Python untuk melakukan pemeriksaan kesehatan (_health check_) website secara berkala, mengukur _response time_ (latency), dan mendeteksi ketersediaan server.

## Fitur

- Pengukuran waktu respon server dalam milidetik (ms).
- Identifikasi status server (`ONLINE`, `HTTP ERROR`, `OFFLINE/UNREACHABLE`).
- Membaca target dari file `urls.json`.
- Mencatat riwayat _monitoring log_ ke file `uptime_log.json`.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
