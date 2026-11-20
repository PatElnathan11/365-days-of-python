# Day 022 - RSS Feed Reader & News Aggregator CLI

Aplikasi pembaca berita dan artikel berbasis terminal yang mengambil data langsung dari sumber RSS/XML tanpa memerlukan API key.

## Fitur
- **XML Feed Parsing:** Mengambil dan mengurai elemen `<item>` atau `<entry>` dari berbagai sumber RSS feed.
- **HTML Sanitizer:** Membersihkan tag HTML mentah dari deskripsi artikel agar nyaman dibaca di terminal.
- **Feed Subscription Manager:** Menambah atau mengelola daftar URL RSS feed di file `feeds.json`.
- **Bookmark / Reading List:** Menyimpan artikel pilihan ke file `bookmarks.json` untuk dibaca nanti.

## Cara Penggunaan
Jalankan script dari terminal:
```bash
python main.py