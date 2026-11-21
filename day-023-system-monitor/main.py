import os
import json
import shutil
import platform
import subprocess
from datetime import datetime


def bytes_to_gb(num_bytes: int) -> float:
    """Mengonversi ukuran byte menjadi gigabyte (GB)."""
    return round(num_bytes / (1024 ** 3), 2)


def get_system_info() -> dict:
    """Mengumpulkan informasi dasar sistem operasi dan CPU."""
    return {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "processor": platform.processor() or "Tidak terdeteksi",
        "cpu_cores": os.cpu_count() or 1,
        "python_version": platform.python_version()
    }


def get_disk_info(path: str = ".") -> dict:
    """Mengambil statistik penggunaan disk pada drive target."""
    abs_path = os.path.abspath(path)
    usage = shutil.disk_usage(abs_path)
    percent_used = round((usage.used / usage.total) * 100, 1)
    return {
        "path": abs_path,
        "total_gb": bytes_to_gb(usage.total),
        "used_gb": bytes_to_gb(usage.used),
        "free_gb": bytes_to_gb(usage.free),
        "percent_used": percent_used
    }


def get_top_processes(limit: int = 8) -> list:
    """Mengambil daftar proses aktif dengan penggunaan memori tertinggi."""
    processes = []
    current_os = platform.system()

    try:
        if current_os == "Windows":
            # Menggunakan tasklist format CSV tanpa header
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            for line in result.stdout.splitlines():
                parts = line.strip().strip('"').split('","')
                if len(parts) >= 5:
                    name = parts[0]
                    pid = parts[1]
                    # Contoh format memori: "124,560 K"
                    mem_str = parts[4].replace(" K", "").replace(",", "").replace(".", "").strip()
                    if mem_str.isdigit():
                        mem_mb = round(int(mem_str) / 1024, 1)
                        processes.append({"pid": pid, "name": name, "memory_mb": mem_mb})
        else:
            # Linux / macOS menggunakan ps
            result = subprocess.run(
                ["ps", "-eo", "pid,comm,rss"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            lines = result.stdout.splitlines()[1:]
            for line in lines:
                parts = line.split(None, 2)
                if len(parts) == 3 and parts[2].isdigit():
                    pid = parts[0]
                    name = os.path.basename(parts[1])
                    mem_mb = round(int(parts[2]) / 1024, 1)
                    processes.append({"pid": pid, "name": name, "memory_mb": mem_mb})
    except Exception as e:
        print(f" Gagal membaca daftar proses: {e}")

    # Urutkan dari penggunaan memori terbesar
    processes.sort(key=lambda item: item["memory_mb"], reverse=True)
    return processes[:limit]


def render_progress_bar(percent: float, width: int = 25) -> str:
    """Membuat progress bar ASCII berdasarkan persentase."""
    filled = int((percent / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def display_dashboard(sys_info: dict, disk_info: dict, top_procs: list):
    """Menampilkan laporan pemantauan sistem di terminal."""
    print("\n=====================================================================")
    print("   SYSTEM RESOURCE & PROCESS MONITOR (Day 023) ")
    print("=====================================================================")
    print(f"  Waktu Cek    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Hostname     : {sys_info['hostname']}")
    print(f"  Sistem OS    : {sys_info['os']} ({sys_info['architecture']})")
    print(f"  CPU Cores    : {sys_info['cpu_cores']} Logical Cores")
    print(f"  Python       : v{sys_info['python_version']}")

    print("\n---------------------------------------------------------------------")
    print("  KAPASITAS PENYIMPANAN (DISK USAGE)")
    print("---------------------------------------------------------------------")
    bar = render_progress_bar(disk_info["percent_used"])
    print(f" [{bar}] {disk_info['percent_used']}%")
    print(
        f" Terpakai: {disk_info['used_gb']} GB | "
        f"Tersedia: {disk_info['free_gb']} GB | "
        f"Total: {disk_info['total_gb']} GB"
    )

    print("\n---------------------------------------------------------------------")
    print("  TOP PROSES BERDASARKAN PENGGUNAAN MEMORI (RAM)")
    print("---------------------------------------------------------------------")
    if not top_procs:
        print(" Tidak ada data proses yang dapat ditampilkan.")
    else:
        print(f" {'PID':<8} | {'Nama Proses':<32} | {'Memori (MB)':>12}")
        print(" " + "-" * 58)
        for proc in top_procs:
            print(f" {proc['pid']:<8} | {proc['name']:<32} | {proc['memory_mb']:>10.1f} MB")

    print("=====================================================================\n")


def main():
    sys_info = get_system_info()
    disk_info = get_disk_info(".")
    top_procs = get_top_processes(limit=8)

    display_dashboard(sys_info, disk_info, top_procs)

    export = input("Simpan snapshot laporan sistem ke JSON? (y/N): ").strip().lower()
    if export == "y":
        snapshot = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system": sys_info,
            "disk": disk_info,
            "top_processes": top_procs
        }
        output_file = "system_snapshot.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)
        print(f" Snapshot berhasil disimpan ke: {output_file}")


if __name__ == "__main__":
    main()