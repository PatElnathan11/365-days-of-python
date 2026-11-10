import os
from pathlib import Path
from datetime import datetime

def get_files_in_directory(dir_path: str) -> list:
    """Mengambil seluruh file dalam direktori (mengabaikan folder)."""
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        return []
    return [f for f in path.iterdir() if f.is_file() and f.name != "main.py" and f.name != "README.md"]

def build_new_name(file_path: Path, mode: str, param1: str, param2: str, index: int) -> str:
    """Menghasilkan nama file baru berdasarkan opsi yang dipilih."""
    stem = file_path.stem      # Nama file tanpa ekstensi
    suffix = file_path.suffix  # Ekstensi (.jpg, .pdf, dll)

    if mode == "1":    # Prefix & Suffix
        new_stem = f"{param1}{stem}{param2}"
    elif mode == "2":  # Find & Replace
        new_stem = stem.replace(param1, param2)
    elif mode == "3":  # Sequential Numbering
        new_stem = f"{param1}_{index:03d}"
    elif mode == "4":  # Date Stamp
        mtime = os.path.getmtime(file_path)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y%m%d")
        new_stem = f"{date_str}_{stem}"
    else:
        new_stem = stem

    return f"{new_stem}{suffix}"

def process_rename(dir_path: str, mode: str, param1: str = "", param2: str = ""):
    files = get_files_in_directory(dir_path)

    if not files:
        print(" Tidak ada file yang ditemukan untuk diproses.")
        return

    files.sort()
    rename_plan = []

    print("\n PREVIEW PERUBAHAN NAMA (DRY RUN):")
    print("-" * 65)

    for idx, file_path in enumerate(files, 1):
        new_name = build_new_name(file_path, mode, param1, param2, idx)
        if new_name != file_path.name:
            rename_plan.append((file_path, file_path.parent / new_name))
            print(f"  {file_path.name}  ➔  {new_name}")

    print("-" * 65)

    if not rename_plan:
        print("ℹTidak ada nama file yang berubah.")
        return

    confirm = input(f"\n❓ Terapkan perubahan pada {len(rename_plan)} file? (y/N): ").strip().lower()

    if confirm == 'y':
        success_count = 0
        for old_path, new_path in rename_plan:
            try:
                old_path.rename(new_path)
                success_count += 1
            except Exception as e:
                print(f" Gagal rename {old_path.name}: {e}")
        print(f"\n Berhasil mengubah nama {success_count} file!")
    else:
        print("\nℹOperasi dibatalkan. File tidak diubah.")

def main():
    print("=============================================")
    print("     BULK FILE RENAMER CLI (Day 012) ")
    print("=============================================")

    target_dir = input("Masukkan path folder target (Enter untuk folder saat ini): ").strip() or "."

    if not os.path.exists(target_dir):
        print(f"Error: Folder '{target_dir}' tidak ditemukan!")
        return

    print("\nPilih Mode Rename:")
    print(" [1] Tambah Prefix & Suffix")
    print(" [2] Find & Replace Teks")
    print(" [3] Penomoran Urut (Sequential)")
    print(" [4] Tambah Stempel Tanggal Modifikasi")

    choice = input("\nMasukkan pilihan (1-4): ").strip()
    param1, param2 = "", ""

    if choice == "1":
        param1 = input("Masukkan Prefix (awal nama): ").strip()
        param2 = input("Masukkan Suffix (akhir nama): ").strip()
    elif choice == "2":
        param1 = input("Teks yang ingin diganti (Find): ").strip()
        param2 = input("Teks pengganti (Replace): ").strip()
    elif choice == "3":
        param1 = input("Nama dasar file (contoh: document): ").strip() or "file"
    elif choice != "4":
        print("Pilihan tidak valid!")
        return

    process_rename(target_dir, choice, param1, param2)

if __name__ == "__main__":
    main()