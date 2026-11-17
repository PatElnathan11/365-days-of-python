import os
import json
import zipfile
from pathlib import Path
from datetime import datetime

BACKUP_DIR = Path("backups")
HISTORY_FILE = "backup_history.json"
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "backups"}


def load_history() -> list:
    """Membaca riwayat backup dari file JSON."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_history(entry: dict):
    """Menyimpan log backup baru ke file JSON."""
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def format_size(size_bytes: int) -> str:
    """Mengonversi ukuran byte menjadi format yang mudah dibaca (KB/MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes / (1024 ** 2):.2f} MB"


def create_backup(source_dir: str):
    """Membuat arsip ZIP dari folder target."""
    source_path = Path(source_dir).resolve()
    if not source_path.exists() or not source_path.is_dir():
        print(f"Error: Folder '{source_dir}' tidak ditemukan!")
        return

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{source_path.name}_{timestamp}.zip"
    archive_path = BACKUP_DIR / archive_name

    file_count = 0
    print(f"\nMemulai proses backup untuk: {source_path}")

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            # Filter folder yang dikecualikan agar tidak ikut di-scan
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                file_path = Path(root) / file
                # Hindari mengarsipkan file zip backup itu sendiri
                if file_path.resolve() == archive_path.resolve():
                    continue
                arcname = file_path.relative_to(source_path)
                zipf.write(file_path, arcname)
                file_count += 1

    archive_size = archive_path.stat().st_size
    entry = {
        "archive_name": archive_name,
        "source_path": str(source_path),
        "file_count": file_count,
        "size_bytes": archive_size,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_history(entry)

    print(" Backup berhasil dibuat!")
    print(f" Nama Arsip : {archive_path}")
    print(f" Total File : {file_count} file")
    print(f" Ukuran ZIP : {format_size(archive_size)}")


def list_backups() -> list[Path]:
    """Menampilkan daftar file backup yang tersedia."""
    if not BACKUP_DIR.exists():
        print("\n Belum ada folder atau file backup.")
        return []

    archives = sorted(BACKUP_DIR.glob("*.zip"), reverse=True)
    if not archives:
        print("\n Belum ada arsip backup (.zip) ditemukan.")
        return []

    print("\n-----------------------------------------------------------------------")
    print(f"{'No':<4} | {'Nama File Backup':<42} | {'Ukuran':<12}")
    print("-----------------------------------------------------------------------")
    for idx, arc in enumerate(archives, 1):
        size_str = format_size(arc.stat().st_size)
        print(f"{idx:<4} | {arc.name:<42} | {size_str:<12}")
    print("-----------------------------------------------------------------------")
    return archives


def restore_backup():
    """Mengekstrak arsip backup yang dipilih ke folder tujuan."""
    archives = list_backups()
    if not archives:
        return

    try:
        choice = int(input("\nPilih nomor arsip yang ingin di-restore: ").strip())
        if not (1 <= choice <= len(archives)):
            print("Nomor arsip tidak valid!")
            return
    except ValueError:
        print("Input harus berupa angka!")
        return

    selected_archive = archives[choice - 1]
    target_dir = input("Masukkan nama folder tujuan restore (default: restored_files): ").strip() or "restored_files"
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(selected_archive, "r") as zipf:
        zipf.extractall(target_path)

    print(f"\n Arsip '{selected_archive.name}' berhasil diekstrak ke folder '{target_path.resolve()}'!")


def main():
    while True:
        print("\n=============================================")
        print(" DIRECTORY BACKUP & RESTORE CLI (Day 019) ")
        print("=============================================")
        print(" [1] Buat Backup Folder Sekarang")
        print(" [2] Lihat Daftar Arsip Backup")
        print(" [3] Restore / Ekstrak Backup")
        print(" [4] Keluar")

        choice = input("\nPilih menu (1-4): ").strip()

        if choice == "1":
            src = input("Masukkan path folder yang ingin di-backup (Enter untuk folder saat ini): ").strip() or "."
            create_backup(src)
        elif choice == "2":
            list_backups()
        elif choice == "3":
            restore_backup()
        elif choice == "4":
            print("Sampai jumpa di Day 020!")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()