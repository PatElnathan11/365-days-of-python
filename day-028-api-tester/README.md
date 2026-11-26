# Day 028 - HTTP API Client & Endpoint Tester CLI

Utilitas berbasis terminal untuk menguji endpoint REST API, mengirim payload JSON, memeriksa header HTTP, dan mengukur waktu respon server.

## Fitur

- **Multi-Method HTTP Support:** Mendukung metode `GET`, `POST`, `PUT`, dan `DELETE`.
- **JSON Payload & Custom Headers:** Membaca body request dari file JSON lokal atau input langsung di terminal.
- **Response Inspector:** Menampilkan HTTP status code, durasi respon (ms), header penting, dan _formatted_ JSON body.
- **Request History Logger:** Menyimpan riwayat setiap pengujian API ke dalam file `api_history.json`.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
