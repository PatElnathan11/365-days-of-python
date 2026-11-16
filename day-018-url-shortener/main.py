import sqlite3
import secrets
import string
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_FILE = "urls.db"
HOST = "127.0.0.1"
PORT = 8000


def init_db():
    """Membuat tabel urls di SQLite jika belum ada."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0
            )
        """)


def is_valid_url(url: str) -> bool:
    """Memvalidasi format URL (harus memiliki scheme http/https dan domain)."""
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def generate_code(length: int = 6) -> str:
    """Menghasilkan kode pendek acak alfanumerik."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def shorten_url():
    """Membuat URL pendek baru dan menyimpannya ke database."""
    original_url = input("Masukkan URL panjang (contoh: https://github.com): ").strip()
    if not is_valid_url(original_url):
        print("URL tidak valid! Pastikan diawali dengan http:// atau https://")
        return

    custom_code = input("Masukkan custom alias (kosongkan untuk acak): ").strip()
    short_code = custom_code if custom_code else generate_code()

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                (short_code, original_url)
            )
        print(f"\n✅ URL berhasil dipendekkan!")
        print(f"Short URL : http://{HOST}:{PORT}/{short_code}")
        print(f"Target    : {original_url}")
    except sqlite3.IntegrityError:
        print(f"Alias '{short_code}' sudah digunakan! Coba gunakan nama lain.")


def show_analytics():
    """Menampilkan daftar seluruh URL pendek beserta jumlah kliknya."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "SELECT short_code, original_url, clicks FROM urls ORDER BY clicks DESC, id DESC"
        )
        rows = cursor.fetchall()

    if not rows:
        print("\n📭 Belum ada URL yang tersimpan.")
        return

    print("\n--------------------------------------------------------------------------------")
    print(f"{'Short URL':<32} | {'Klik':<6} | {'URL Tujuan'}")
    print("--------------------------------------------------------------------------------")

    for code, orig_url, clicks in rows:
        short_link = f"http://{HOST}:{PORT}/{code}"
        print(f"{short_link:<32} | {clicks:<6} | {orig_url}")

    print("--------------------------------------------------------------------------------")


class RedirectHandler(BaseHTTPRequestHandler):
    """Handler HTTP untuk menangani redirect URL pendek."""

    def do_GET(self):
        code = self.path.lstrip("/")
        if not code:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h2>Local URL Shortener Server Aktif!</h2><p>Gunakan /&lt;short_code&gt; untuk redirect.</p>")
            return

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("SELECT original_url FROM urls WHERE short_code = ?", (code,))
            row = cursor.fetchone()

            if row:
                target_url = row[0]
                conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
                self.send_response(302)
                self.send_header("Location", target_url)
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h3>404 - Short code '{code}' tidak ditemukan.</h3>".encode("utf-8"))

    def log_message(self, format, *args):
        # Menampilkan log akses yang lebih ringkas di terminal
        print(f" [HTTP] {self.address_string()} -> {args[0]}")


def start_server():
    """Menjalankan server HTTP lokal untuk redirect."""
    server = HTTPServer((HOST, PORT), RedirectHandler)
    print(f"\nServer Redirect berjalan di http://{HOST}:{PORT}")
    print("Buka salah satu Short URL di browser untuk mengetes redirect & klik.")
    print("Tekan Ctrl+C untuk menghentikan server dan kembali ke menu.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()


def main():
    init_db()
    while True:
        print("\n===========================================")
        print(" LOCAL URL SHORTENER CLI (Day 018) ")
        print("===========================================")
        print(" [1] Pendekkan URL Baru")
        print(" [2] Lihat Daftar & Statistik Klik")
        print(" [3] Jalankan Server Redirect (Port 8000)")
        print(" [4] Keluar")

        choice = input("\nPilih menu (1-4): ").strip()

        if choice == "1":
            shorten_url()
        elif choice == "2":
            show_analytics()
        elif choice == "3":
            start_server()
        elif choice == "4":
            print("Berhasil Keluar")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()