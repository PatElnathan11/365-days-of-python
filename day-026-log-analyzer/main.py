import re
import json
from pathlib import Path
from collections import Counter

LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"\[(?P<service>[^\]]+)\]:\s+"
    r"(?P<message>.+)$"
)


def parse_log_file(filepath_str: str) -> list[dict]:
    """Membaca dan mem-parsing seluruh baris pada file log."""
    filepath = Path(filepath_str)
    if not filepath.exists() or not filepath.is_file():
        print(f"❌ Error: File '{filepath_str}' tidak ditemukan!")
        return []

    parsed_entries = []

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line_num, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            if not line:
                continue

            match = LOG_PATTERN.match(line)
            if match:
                entry = {
                    "line": line_num,
                    "timestamp": match.group("timestamp"),
                    "level": match.group("level"),
                    "service": match.group("service"),
                    "message": match.group("message"),
                }
                parsed_entries.append(entry)

    return parsed_entries


def analyze_logs(entries: list[dict], source_name: str):
    """Menampilkan ringkasan statistik log dan error yang sering muncul."""
    if not entries:
        print("📭 Tidak ada entri log valid yang dapat dianalisis.")
        return

    level_counts = Counter()
    service_counts = Counter()
    error_messages = Counter()

    for entry in entries:
        level = entry["level"]
        service = entry["service"]
        message = entry["message"]

        level_counts[level] += 1
        service_counts[service] += 1

        if level in ("ERROR", "CRITICAL"):
            error_key = f"[{service}] {message}"
            error_messages[error_key] += 1

    total_logs = len(entries)

    print("\n=====================================================================")
    print(" 📋 SERVER LOG ANALYSIS REPORT (Day 026) ")
    print("=====================================================================")
    print(f" 📄 File Sumber   : {source_name}")
    print(f" 🔢 Total Baris   : {total_logs} entri valid")

    print("\n📊 Distribusi Level Log:")
    for level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        count = level_counts[level]
        pct = (count / total_logs) * 100
        bar = "█" * int((count / total_logs) * 25)
        print(f"   {level:<10} | {bar:<25} | {count:>3} ({pct:>5.1f}%)")

    print("\n🔥 Top Error & Critical Paling Sering Muncul:")
    if not error_messages:
        print("   ✅ Tidak ditemukan log ERROR atau CRITICAL.")
    else:
        for err_msg, count in error_messages.most_common(5):
            print(f"   - ({count}x) {err_msg}")

    print("\n⚙️  Aktivitas per Service:")
    for service, count in service_counts.most_common():
        print(f"   - {service:<18} : {count} log")

    print("=====================================================================\n")

    report_data = {
        "source_file": source_name,
        "total_entries": total_logs,
        "level_distribution": dict(level_counts),
        "service_activity": dict(service_counts),
        "top_errors": [
            {"error": msg, "count": cnt} for msg, cnt in error_messages.most_common(5)
        ],
    }

    with open("log_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print("💾 Laporan statistik disimpan ke: log_report.json\n")


def filter_logs(entries: list[dict]):
    """Memfilter dan menampilkan baris log berdasarkan level atau kata kunci."""
    if not entries:
        print("📭 Data log kosong.")
        return

    target_level = input("Filter berdasarkan level (INFO/WARNING/ERROR/CRITICAL, Enter untuk semua): ").strip().upper()
    keyword = input("Filter berdasarkan kata kunci (Enter untuk lewati): ").strip().lower()

    matched = []
    for entry in entries:
        if target_level and entry["level"] != target_level:
            continue
        if keyword:
            combined_text = f"{entry['service']} {entry['message']}".lower()
            if keyword not in combined_text:
                continue
        matched.append(entry)

    print(f"\n🔍 Ditemukan {len(matched)} log yang cocok:")
    print("-" * 75)
    for item in matched:
        print(f"[{item['timestamp']}] {item['level']:<8} [{item['service']}]: {item['message']}")
    print("-" * 75 + "\n")


def main():
    log_file = "server.log"
    entries = parse_log_file(log_file)

    while True:
        print("=============================================")
        print(" 🕵️  SERVER LOG ANALYZER CLI (Day 026) ")
        print("=============================================")
        print(f" File aktif: {log_file} ({len(entries)} entri)")
        print(" [1] Tampilkan Analisis & Export Laporan JSON")
        print(" [2] Filter & Cari Baris Log")
        print(" [3] Ganti File Log Target")
        print(" [4] Keluar")

        choice = input("\nPilih menu (1-4): ").strip()

        if choice == "1":
            analyze_logs(entries, log_file)
        elif choice == "2":
            filter_logs(entries)
        elif choice == "3":
            new_file = input("Masukkan path file log baru: ").strip()
            if new_file:
                log_file = new_file
                entries = parse_log_file(log_file)
        elif choice == "4":
            print("👋 Sampai jumpa di Day 027!")
            break
        else:
            print("⚠️ Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()