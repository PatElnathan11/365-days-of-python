import os
import json
from pathlib import Path
from collections import defaultdict

IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".vscode"}

LANGUAGE_MAP = {
    ".py": ("Python", "#"),
    ".js": ("JavaScript", "//"),
    ".ts": ("TypeScript", "//"),
    ".tsx": ("TypeScript React", "//"),
    ".jsx": ("JavaScript React", "//"),
    ".c": ("C", "//"),
    ".cpp": ("C++", "//"),
    ".h": ("C/C++ Header", "//"),
    ".java": ("Java", "//"),
    ".go": ("Go", "//"),
    ".rs": ("Rust", "//"),
    ".html": ("HTML", "<!--"),
    ".css": ("CSS", "/*"),
    ".sql": ("SQL", "--"),
    ".sh": ("Shell Script", "#"),
    ".md": ("Markdown", None),
    ".json": ("JSON", None),
}


def count_file_lines(file_path: Path, comment_prefix: str | None) -> tuple[int, int, int]:
    """Menghitung (baris_kode, baris_komentar, baris_kosong) dari sebuah file."""
    code_lines = 0
    comment_lines = 0
    blank_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif comment_prefix and stripped.startswith(comment_prefix):
                    comment_lines += 1
                else:
                    code_lines += 1
    except OSError:
        pass

    return code_lines, comment_lines, blank_lines


def print_directory_tree(dir_path: Path, prefix: str = "", max_depth: int = 2, current_depth: int = 0):
    """Mencetak struktur pohon direktori hingga kedalaman tertentu."""
    if current_depth >= max_depth:
        return

    entries = sorted(
        [e for e in dir_path.iterdir() if e.name not in IGNORED_DIRS],
        key=lambda x: (not x.is_dir(), x.name.lower())
    )

    for idx, entry in enumerate(entries):
        is_last = idx == len(entries) - 1
        connector = "└── " if is_last else "├── "
        icon = "📁 " if entry.is_dir() else "📄 "
        print(f"{prefix}{connector}{icon}{entry.name}")

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_directory_tree(entry, prefix + extension, max_depth, current_depth + 1)


def analyze_codebase(target_dir: str):
    """Menganalisis seluruh file kode di dalam direktori target."""
    root_path = Path(target_dir).resolve()
    if not root_path.exists() or not root_path.is_dir():
        print(f" Error: Folder '{target_dir}' tidak ditemukan!")
        return

    stats = defaultdict(lambda: {"files": 0, "code": 0, "comments": 0, "blanks": 0})

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for filename in files:
            file_path = Path(root) / filename
            ext = file_path.suffix.lower()
            if ext in LANGUAGE_MAP:
                lang_name, comment_prefix = LANGUAGE_MAP[ext]
                code, comments, blanks = count_file_lines(file_path, comment_prefix)
                stats[lang_name]["files"] += 1
                stats[lang_name]["code"] += code
                stats[lang_name]["comments"] += comments
                stats[lang_name]["blanks"] += blanks

    print("\n=====================================================================")
    print("  STRUKTUR DIREKTORI (Max Depth: 2) ")
    print("=====================================================================")
    print(f" {root_path.name}/")
    print_directory_tree(root_path, max_depth=2)

    print("\n=====================================================================")
    print("  STATISTIK BARIS KODE (Day 021) ")
    print("=====================================================================")

    if not stats:
        print(" Tidak ditemukan file kode sumber yang dikenali.")
        return

    print(f"{'Bahasa':<18} | {'Files':>6} | {'Code':>8} | {'Comments':>9} | {'Blanks':>8}")
    print("-" * 69)

    total_files = total_code = total_comments = total_blanks = 0

    sorted_stats = sorted(stats.items(), key=lambda x: x[1]["code"], reverse=True)
    for lang, data in sorted_stats:
        print(
            f"{lang:<18} | {data['files']:>6} | {data['code']:>8} | "
            f"{data['comments']:>9} | {data['blanks']:>8}"
        )
        total_files += data["files"]
        total_code += data["code"]
        total_comments += data["comments"]
        total_blanks += data["blanks"]

    print("-" * 69)
    print(
        f"{'TOTAL':<18} | {total_files:>6} | {total_code:>8} | "
        f"{total_comments:>9} | {total_blanks:>8}"
    )
    print("=====================================================================\n")

    report = {
        "project": root_path.name,
        "summary": {
            "total_files": total_files,
            "total_code_lines": total_code,
            "total_comment_lines": total_comments,
            "total_blank_lines": total_blanks,
        },
        "by_language": dict(sorted_stats)
    }

    with open("code_stats.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(" Laporan lengkap disimpan ke: code_stats.json")


def main():
    print("=============================================")
    print("  CODEBASE LINE COUNTER & TREE (Day 021) ")
    print("=============================================")

    target = input("Masukkan path folder proyek (default '..' untuk repo ini): ").strip() or ".."
    analyze_codebase(target)


if __name__ == "__main__":
    main()