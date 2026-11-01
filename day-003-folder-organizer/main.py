import os
import shutil
from pathlib import Path

# Pemetaan kategori folder berdasarkan ekstensi file
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".html", ".css", ".json", ".sh"],
}

def organize_folder(target_dir: str):
    target_path = Path(target_dir).resolve()

    if not target_path.exists() or not target_path.is_dir():
        print(f"Error: Folder '{target_dir}' tidak ditemukan!")
        return

    print(f"\nMemproses folder: {target_path}\n")

    moved_count = 0

    for item in target_path.iterdir():
        # Lewati jika berupa folder
        if item.is_dir():
            continue

        file_ext = item.suffix.lower()
        destination_folder = "Others"

        # Cari kategori yang cocok
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                destination_folder = category
                break

        # Buat folder kategori jika belum ada
        dest_dir = target_path / destination_folder
        dest_dir.mkdir(exist_ok=True)

        # Pindahkan file
        target_file_path = dest_dir / item.name
        
        # Hindari menimpa file bernama sama
        if target_file_path.exists():
            target_file_path = dest_dir / f"{item.stem}_copy{item.suffix}"

        shutil.move(str(item), str(target_file_path))
        print(f" ➔ [{destination_folder}] {item.name}")
        moved_count += 1

    print(f"\nSelesai! Berhasil merapikan {moved_count} file.")

if __name__ == "__main__":
    print("====================================")
    print("     AUTOMATIC FOLDER ORGANIZER     ")
    print("====================================")
    
    path_input = input("Masukkan path folder yang ingin dirapikan (Enter untuk folder saat ini): ").strip()
    
    # Jika dikosongkan, gunakan folder saat ini
    target = path_input if path_input else "."
    organize_folder(target)