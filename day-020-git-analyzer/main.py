import os
import json
import subprocess
from collections import Counter
from datetime import datetime

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def run_git_command(args: list[str], repo_path: str) -> str:
    """Menjalankan perintah git pada direktori target dan mengembalikan stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Gagal menjalankan perintah git.")
    return result.stdout.strip()


def is_git_repo(repo_path: str) -> bool:
    """Memeriksa apakah path merupakan repository Git yang valid."""
    if not os.path.isdir(repo_path):
        return False
    try:
        output = run_git_command(["rev-parse", "--is-inside-work-tree"], repo_path)
        return output == "true"
    except RuntimeError:
        return False


def analyze_repository(repo_path: str):
    """Menganalisis riwayat commit dari repository Git."""
    abs_path = os.path.abspath(repo_path)
    if not is_git_repo(abs_path):
        print(f"Error: '{abs_path}' bukan merupakan repository Git yang valid!")
        return

    # Format: hash|author_name|iso_date|subject
    raw_logs = run_git_command(
        ["log", "--pretty=format:%h|%an|%ad|%s", "--date=iso"],
        abs_path
    )

    if not raw_logs:
        print("📭 Repository ini belum memiliki commit.")
        return

    lines = raw_logs.splitlines()
    total_commits = len(lines)
    authors = Counter()
    days_of_week = Counter()
    recent_commits = []

    for idx, line in enumerate(lines):
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        commit_hash, author, date_str, subject = parts
        authors[author] += 1

        # Ekstrak tanggal YYYY-MM-DD untuk menentukan hari
        date_only = date_str.split()[0]
        try:
            dt = datetime.strptime(date_only, "%Y-%m-%d")
            days_of_week[DAY_NAMES[dt.weekday()]] += 1
        except ValueError:
            pass

        if idx < 5:
            recent_commits.append({
                "hash": commit_hash,
                "author": author,
                "date": date_only,
                "message": subject
            })

    branch_name = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], abs_path)

    print("\n============================================================")
    print("  GIT REPOSITORY ACTIVITY REPORT  ")
    print("============================================================")
    print(f" Repository   : {os.path.basename(abs_path)}")
    print(f" Branch Aktif : {branch_name}")
    print(f" Total Commit : {total_commits}")

    print("\n Top Kontributor:")
    for author, count in authors.most_common(5):
        pct = (count / total_commits) * 100
        print(f"   - {author:<22} : {count:>3} commit ({pct:.1f}%)")

    print("\n Aktivitas Berdasarkan Hari:")
    max_day_count = max(days_of_week.values()) if days_of_week else 1
    for day in DAY_NAMES:
        count = days_of_week[day]
        bar_len = int((count / max_day_count) * 20)
        bar = "█" * bar_len
        print(f"   {day:<10} | {bar:<20} ({count})")

    print("\n🕒 5 Commit Terakhir:")
    for item in recent_commits:
        print(f"   [{item['hash']}] {item['date']} - {item['message']} ({item['author']})")

    print("============================================================\n")

    # Simpan ringkasan ke JSON
    report_data = {
        "repository": os.path.basename(abs_path),
        "branch": branch_name,
        "total_commits": total_commits,
        "contributors": dict(authors),
        "commits_by_day": {day: days_of_week[day] for day in DAY_NAMES},
        "recent_commits": recent_commits,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("git_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print("Laporan lengkap disimpan ke: git_report.json")


def main():
    print("=============================================")
    print(" GIT COMMIT & ACTIVITY ANALYZER  ")
    print("=============================================")

    target = input("Masukkan path repo Git (default '..' untuk repo ini): ").strip() or ".."
    analyze_repository(target)


if __name__ == "__main__":
    main()