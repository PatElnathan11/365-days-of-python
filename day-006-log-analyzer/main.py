import os
import re
from collections import Counter

LOG_FILE = "sample.log"

def analyze_log(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan!")
        return

    # Pattern Regex untuk ekstrak IP, Status Code, dan Log Level
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    status_pattern = re.compile(r'"\s+(\d{3})\s+')
    level_pattern = re.compile(r'\b(INFO|WARNING|ERROR|CRITICAL)\b')

    ip_counter = Counter()
    status_counter = Counter()
    level_counter = Counter()
    total_lines = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            total_lines += 1
            
            # Cari Alamat IP
            ip_match = ip_pattern.search(line)
            if ip_match:
                ip_counter[ip_match.group(0)] += 1

            # Cari Status Code HTTP
            status_match = status_pattern.search(line)
            if status_match:
                status_counter[status_match.group(1)] += 1

            # Cari Level Log
            level_match = level_pattern.search(line)
            if level_match:
                level_counter[level_match.group(0)] += 1

    # Tampilkan Hasil Analisis
    print("==================================================")
    print("   SERVER LOG ANALYZER REPORT (Day 006) ")
    print("==================================================")
    print(f"  Total Baris Diproses: {total_lines}")
    
    print("\nStatistik Log Level:")
    for level, count in level_counter.items():
        print(f"   - {level:<8}: {count}")

    print("\nTop Request Alamat IP:")
    for ip, count in ip_counter.most_common(3):
        print(f"   - {ip:<15}: {count} request(s)")

    print("\nDistribusi HTTP Status Code:")
    for status, count in status_counter.items():
        print(f"   - Status {status}  : {count}")
    print("==================================================")

if __name__ == "__main__":
    analyze_log(LOG_FILE)