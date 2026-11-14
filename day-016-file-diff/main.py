import os
import difflib

# Kode warna ANSI untuk terminal
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

def read_lines(filepath: str) -> list[str]:
    """Membaca seluruh baris dari file teks."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()

def calculate_similarity(lines1: list[str], lines2: list[str]) -> float:
    """Menghitung persentase kemiripan antara dua file."""
    text1 = "".join(lines1)
    text2 = "".join(lines2)
    ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return round(ratio * 100, 2)

def show_terminal_diff(file1: str, file2: str, lines1: list[str], lines2: list[str]):
    """Menampilkan unified diff berwarna di terminal."""
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=file1,
        tofile=file2,
        lineterm=""
    ))

    print("\n==================================================")
    print(" HASIL PERBANDINGAN FILE (UNIFIED DIFF) ")
    print("==================================================")

    if not diff:
        print("Kedua file identik! Tidak ada perbedaan.")
        return

    for line in diff:
        line_clean = line.rstrip("\n")
        if line_clean.startswith("+") and not line_clean.startswith("+++"):
            print(f"{GREEN}{line_clean}{RESET}")
        elif line_clean.startswith("-") and not line_clean.startswith("---"):
            print(f"{RED}{line_clean}{RESET}")
        elif line_clean.startswith("@@"):
            print(f"{CYAN}{line_clean}{RESET}")
        else:
            print(line_clean)

    print("==================================================")

def export_html_diff(file1: str, file2: str, lines1: list[str], lines2: list[str], output_file: str = "diff_report.html"):
    """Mengekspor perbandingan berdampingan (side-by-side) ke HTML."""
    html_diff = difflib.HtmlDiff(wrapcolumn=80)
    html_content = html_diff.make_file(
        lines1, lines2,
        fromdesc=f"File Lama: {file1}",
        todesc=f"File Baru: {file2}"
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Laporan visual HTML disimpan di: {output_file}")

def main():
    print("=============================================")
    print(" FILE DIFF & COMPARATOR CLI (Day 016) ")
    print("=============================================")

    file1 = input("Masukkan file pertama (default: config_v1.txt): ").strip() or "config_v1.txt"
    file2 = input("Masukkan file kedua   (default: config_v2.txt): ").strip() or "config_v2.txt"

    if not os.path.exists(file1) or not os.path.exists(file2):
        print("❌ Error: Salah satu atau kedua file tidak ditemukan!")
        return

    lines1 = read_lines(file1)
    lines2 = read_lines(file2)

    similarity = calculate_similarity(lines1, lines2)
    show_terminal_diff(file1, file2, lines1, lines2)
    print(f"Tingkat Kemiripan: {similarity}%\n")

    export = input("Ingin export laporan side-by-side ke HTML? (y/N): ").strip().lower()
    if export == "y":
        export_html_diff(file1, file2, lines1, lines2)

if __name__ == "__main__":
    main()