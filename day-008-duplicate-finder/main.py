import os
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath: str, chunk_size: int = 8192) -> str:
    """Menghitung hash MD5 dari sebuah file secara bertahap (chunking)."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return ""

def find_duplicates(target_directory: str) -> dict:
    """Memindai direktori dan mengelompokkan file berdasarkan hash isi file."""
    hashes = defaultdict(list)
    total_files = 0

    print(f"🔍 Memindai direktori: {os.path.abspath(target_directory)} ...\n")

    for root, _, files in os.walk(target_directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            total_files += 1
            
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)

    # Filter hanya hash yang memiliki lebih dari 1 file (duplikat)
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    return duplicates, total_files

def main():
    print("=============================================")
    print(" DUPLICATE FILE FINDER CLI (Day 008) ")
    print("=============================================")

    target_dir = input("Masukkan path folder yang ingin dipindai (Enter untuk folder saat ini): ").strip()
    if not target_dir:
        target_dir = "."

    if not os.path.exists(target_dir):
        print(f"Error: Folder '{target_dir}' tidak ditemukan!")
        return

    duplicates, total_files = find_duplicates(target_dir)

    print("---------------------------------------------")
    print(f"Total file dipindai: {total_files}")
    print(f"Ditemukan {len(duplicates)} kelompok file duplikat.")
    print("---------------------------------------------\n")

    if not duplicates:
        print("Selamat! Tidak ada file duplikat yang ditemukan.")
        return

    to_delete = []

    for idx, (file_hash, paths) in enumerate(duplicates.items(), 1):
        print(f"Kelompok Duplikat #{idx} (Hash: {file_hash[:10]}...):")
        print(f"   [Asli]    : {paths[0]}")
        for copy_path in paths[1:]:
            print(f"   [Salinan] : {copy_path}")
            to_delete.append(copy_path)
        print()

    # Opsi Penanganan File Duplikat
    confirm = input(f"Apakah kamu ingin menghapus {len(to_delete)} file salinan di atas? (y/N): ").strip().lower()
    
    if confirm == 'y':
        deleted_count = 0
        for filepath in to_delete:
            try:
                os.remove(filepath)
                print(f" 🗑️ Dihapus: {filepath}")
                deleted_count += 1
            except Exception as e:
                print(f" Gagal menghapus {filepath}: {e}")
        print(f"\nBerhasil menghapus {deleted_count} file duplikat.")
    else:
        print("\nℹPengoperasian dibatalkan. Tidak ada file yang dihapus.")

if __name__ == "__main__":
    main()