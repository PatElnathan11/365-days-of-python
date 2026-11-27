# Day 029 - Password Generator & Strength Auditor CLI

Utilitas keamanan berbasis terminal untuk membangkitkan password maupun passphrase acak yang aman serta menganalisis tingkat kekuatan suatu password berdasarkan perhitungan entropi.

## Fitur

- **Cryptographic Password Generator:** Menghasilkan password acak dengan panjang kustom dan jaminan komposisi huruf besar, huruf kecil, angka, serta simbol.
- **Diceware-Style Passphrase Generator:** Membuat kombinasi kata acak yang mudah dihafal namun tetap sulit ditebak (misal: `Falcon-Orbit-742-Pixel`).
- **Entropy & Strength Auditor:** Menghitung nilai entropi (bits), estimasi waktu peretasan _brute-force_, dan mendeteksi pola lemah (urutan angka, karakter berulang, kata umum).
- **Batch Export Option:** Menyimpan daftar password yang baru dibuat ke file JSON jika diperlukan.

## Cara Penggunaan

Jalankan script dari terminal:

```bash
python main.py
```
