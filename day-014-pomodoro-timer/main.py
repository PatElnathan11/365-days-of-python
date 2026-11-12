import os
import json
import time
from datetime import datetime

LOG_FILE = "focus_log.json"

def load_logs() -> list:
    """Membaca riwayat sesi fokus dari file JSON."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_log(task_name: str, duration_seconds: int):
    """Menyimpan sesi fokus yang selesai ke file JSON."""
    logs = load_logs()
    entry = {
        "task": task_name,
        "duration_seconds": duration_seconds,
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

def run_timer(seconds: int, label: str):
    """Menjalankan countdown timer di satu baris terminal."""
    print(f"\n⏳ Memulai: {label} (Tekan Ctrl+C untuk membatalkan)\n")
    try:
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            timer_display = f"{mins:02d}:{secs:02d}"
            # Progress bar sederhana
            progress = int(((seconds - remaining) / seconds) * 20)
            bar = "█" * progress + "░" * (20 - progress)
            
            print(f"\r   [{bar}] ⏱️  {timer_display} tersisa...", end="", flush=True)
            time.sleep(1)

        print(f"\r   [{'█' * 20}] ✅ 00:00 - Selesai!{' ' * 15}\n")
        # Bunyi bell terminal standar (jika didukung OS)
        print("\a", end="")
        return True
    except KeyboardInterrupt:
        print("\n\n⚠️ Timer dibatalkan oleh pengguna.")
        return False

def show_stats():
    """Menampilkan ringkasan riwayat sesi fokus."""
    logs = load_logs()
    if not logs:
        print("\n📭 Belum ada riwayat sesi fokus yang tercatat.")
        return

    total_seconds = sum(item["duration_seconds"] for item in logs)
    total_mins = total_seconds // 60

    print("\n==================================================")
    print(" STATISTIK SESI FOKUS (Day 014) ")
    print("==================================================")
    print(f"Total Sesi Selesai : {len(logs)} sesi")
    print(f"Total Waktu Fokus  : {total_mins} menit ({total_seconds} detik)")
    print("--------------------------------------------------")
    for idx, item in enumerate(logs[-5:], 1):  # Tampilkan 5 sesi terakhir
        mins = item["duration_seconds"] // 60
        secs = item["duration_seconds"] % 60
        dur_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
        print(f" {idx}. [{item['completed_at']}] {item['task']} ({dur_str})")
    print("==================================================")

def main():
    while True:
        print("\n===========================================")
        print("  POMODORO FOCUS TIMER CLI (Day 014) ")
        print("===========================================")
        print(" [1] Fokus Standar (25 Menit)")
        print(" [2] Fokus Singkat (15 Menit)")
        print(" [3] Mode Tes Cepat (10 Detik)")
        print(" [4] Lihat Statistik Fokus")
        print(" [5] Keluar")

        choice = input("\nPilih menu (1-5): ").strip()

        if choice in ("1", "2", "3"):
            task = input("Apa target tugas untuk sesi ini? ").strip() or "Belajar Python"
            
            if choice == "1":
                duration = 25 * 60
            elif choice == "2":
                duration = 15 * 60
            else:
                duration = 10

            completed = run_timer(duration, f"Fokus: {task}")
            if completed:
                save_log(task, duration)
                print("Sesi berhasil dicatat ke focus_log.json!")

                take_break = input("Mulai istirahat singkat 5 menit? (y/N): ").strip().lower()
                if take_break == "y":
                    run_timer(5 * 60, "Istirahat Singkat")

        elif choice == "4":
            show_stats()
        elif choice == "5":
            print("Tetap produktif! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()