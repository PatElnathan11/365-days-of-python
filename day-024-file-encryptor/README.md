# Day 024 - File Encryptor & Integrity Vault CLI

Utilitas berbasis terminal untuk mengenkripsi dan mendekripsi file menggunakan password dengan verifikasi integritas data otomatis.

## Fitur

- **Password-Based Key Derivation:** Menggunakan `PBKDF2-HMAC-SHA256` dengan 100.000 iterasi dan _random salt_ 16-byte.
- **Authenticated Encryption (HMAC):** Menyertakan _signature_ HMAC-SHA256 untuk mendeteksi kesalahan password atau modifikasi file sebelum dekripsi.
- **Universal File Support:** Dapat mengenkripsi file teks (`.txt`, `.env`, `.json`) maupun file biner (`.pdf`, `.png`, `.zip`).
- **Safe Output:** Menghasilkan file baru berekstensi `.enc` tanpa menimpa file asli secara paksa.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
