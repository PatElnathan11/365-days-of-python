import os
import re
import json
import html
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

FEEDS_FILE = "feeds.json"
BOOKMARKS_FILE = "bookmarks.json"

DEFAULT_FEEDS = [
    {"name": "Python Insider", "url": "https://blog.python.org/feeds/posts/default?alt=rss"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage"},
    {"name": "Real Python", "url": "https://realpython.com/atom.xml"},
]


def load_json(filepath: str, default_data: list) -> list:
    """Membaca data dari file JSON atau membuat file default jika belum ada."""
    if not os.path.exists(filepath):
        save_json(filepath, default_data)
        return default_data

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default_data


def save_json(filepath: str, data: list):
    """Menyimpan data list ke dalam file JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def clean_html(raw_text: str) -> str:
    """Menghapus tag HTML dan merapikan spasi berlebih."""
    if not raw_text:
        return "Tidak ada deskripsi."
    unescaped = html.unescape(raw_text)
    no_tags = re.sub(r"<[^>]+>", " ", unescaped)
    cleaned = re.sub(r"\s+", " ", no_tags).strip()
    return cleaned


def fetch_feed_articles(feed_url: str, limit: int = 8) -> list:
    """Mengunduh dan mem-parsing artikel dari URL RSS/Atom feed."""
    req = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "Mozilla/5.0 (Python RSS Reader CLI)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
    except (urllib.error.URLError, Exception) as e:
        print(f" Gagal mengambil feed dari {feed_url}: {e}")
        return []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"❌ Gagal mem-parsing XML: {e}")
        return []

    articles = []

    # Cek format RSS 2.0 (<item>)
    items = root.findall(".//item")
    if items:
        for item in items[:limit]:
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            date_el = item.find("pubDate")

            title = title_el.text.strip() if title_el is not None and title_el.text else "Tanpa Judul"
            link = link_el.text.strip() if link_el is not None and link_el.text else "-"
            summary = clean_html(desc_el.text if desc_el is not None else "")
            pub_date = date_el.text.strip() if date_el is not None and date_el.text else "-"

            articles.append({
                "title": title,
                "link": link,
                "summary": summary[:180] + ("..." if len(summary) > 180 else ""),
                "published": pub_date
            })
        return articles

    # Cek format Atom (<entry>) jika bukan RSS 2.0
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall(".//atom:entry", ns)
    for entry in entries[:limit]:
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link", ns)
        summary_el = entry.find("atom:summary", ns) or entry.find("atom:content", ns)
        date_el = entry.find("atom:updated", ns)

        title = title_el.text.strip() if title_el is not None and title_el.text else "Tanpa Judul"
        link = link_el.attrib.get("href", "-") if link_el is not None else "-"
        summary = clean_html(summary_el.text if summary_el is not None else "")
        pub_date = date_el.text.strip() if date_el is not None and date_el.text else "-"

        articles.append({
            "title": title,
            "link": link,
            "summary": summary[:180] + ("..." if len(summary) > 180 else ""),
            "published": pub_date
        })

    return articles


def read_feed_menu():
    """Menampilkan daftar sumber RSS dan membaca artikelnya."""
    feeds = load_json(FEEDS_FILE, DEFAULT_FEEDS)
    if not feeds:
        print("\n Daftar RSS feed kosong.")
        return

    print("\n Pilih Sumber RSS Feed:")
    for idx, feed in enumerate(feeds, 1):
        print(f" [{idx}] {feed['name']} ({feed['url']})")

    try:
        choice = int(input("\nMasukkan nomor feed: ").strip())
        if not (1 <= choice <= len(feeds)):
            print(" Nomor feed tidak valid!")
            return
    except ValueError:
        print(" Input harus berupa angka!")
        return

    selected_feed = feeds[choice - 1]
    print(f"\n Mengambil berita terbaru dari {selected_feed['name']}...")
    articles = fetch_feed_articles(selected_feed["url"])

    if not articles:
        print(" Tidak ada artikel yang dapat ditampilkan.")
        return

    print("\n======================================================================")
    print(f"   ARTIKEL TERBARU: {selected_feed['name'].upper()} ")
    print("======================================================================")

    for idx, art in enumerate(articles, 1):
        print(f"\n[{idx}] {art['title']}")
        print(f"     Tanggal : {art['published']}")
        print(f"     Link    : {art['link']}")
        print(f"     Ringkas : {art['summary']}")

    print("\n======================================================================")

    bookmark_input = input("Masukkan nomor artikel untuk di-bookmark (Enter untuk lewati): ").strip()
    if bookmark_input.isdigit():
        art_idx = int(bookmark_input)
        if 1 <= art_idx <= len(articles):
            bookmarks = load_json(BOOKMARKS_FILE, [])
            bookmarks.append(articles[art_idx - 1])
            save_json(BOOKMARKS_FILE, bookmarks)
            print(f" Artikel '{articles[art_idx - 1]['title']}' disimpan ke {BOOKMARKS_FILE}!")


def add_new_feed():
    """Menambahkan sumber RSS feed baru ke feeds.json."""
    name = input("Masukkan nama sumber (contoh: TechCrunch): ").strip()
    url = input("Masukkan URL RSS feed: ").strip()

    if not name or not url.startswith(("http://", "https://")):
        print(" Nama tidak boleh kosong dan URL harus diawali http:// atau https://")
        return

    feeds = load_json(FEEDS_FILE, DEFAULT_FEEDS)
    feeds.append({"name": name, "url": url})
    save_json(FEEDS_FILE, feeds)
    print(f" Feed '{name}' berhasil ditambahkan!")


def show_bookmarks():
    """Menampilkan daftar artikel yang sudah di-bookmark."""
    bookmarks = load_json(BOOKMARKS_FILE, [])
    if not bookmarks:
        print("\n Belum ada artikel yang disimpan di bookmark.")
        return

    print("\n======================================================================")
    print("  DAFTAR BACAAN TERSIMPAN (BOOKMARKS) ")
    print("======================================================================")
    for idx, item in enumerate(bookmarks, 1):
        print(f" {idx}. {item['title']}")
        print(f"     {item['link']}")
    print("======================================================================")


def main():
    while True:
        print("\n===========================================")
        print(" 📡 RSS FEED READER CLI (Day 022) ")
        print("===========================================")
        print(" [1] Baca Berita dari RSS Feed")
        print(" [2] Tambah Sumber RSS Feed Baru")
        print(" [3] Lihat Daftar Bookmark")
        print(" [4] Keluar")

        choice = input("\nPilih menu (1-4): ").strip()

        if choice == "1":
            read_feed_menu()
        elif choice == "2":
            add_new_feed()
        elif choice == "3":
            show_bookmarks()
        elif choice == "4":
            print("Berhasil Keluar")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()