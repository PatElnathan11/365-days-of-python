import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
    443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 8000, 8080, 8443
]

def get_service_name(port: int) -> str:
    """Mendapatkan nama layanan standar untuk nomor port tertentu."""
    try:
        return socket.getservbyport(port, "tcp").upper()
    except OSError:
        return "UNKNOWN"

def scan_port(ip: str, port: int, timeout: float = 0.8) -> tuple[int, bool, str]:
    """Mengecek apakah satu port TCP terbuka."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port, True, get_service_name(port)
        return port, False, ""

def run_scanner(target: str, ports: list[int]):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f" Error: Host '{target}' tidak dapat ditemukan/diresolve.")
        return

    print("\n==================================================")
    print("  MULTI-THREADED PORT SCANNER (Day 015) ")
    print("==================================================")
    print(f"Target Host : {target} ({target_ip})")
    print(f"Total Port  : {len(ports)} port")
    print(f"Mulai pada  : {datetime.now().strftime('%H:%M:%S')}")
    print("--------------------------------------------------")
    print("Memindai port...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports}
        for future in as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))

    open_ports.sort(key=lambda x: x[0])

    if open_ports:
        print(f"{'PORT':<10} | {'STATUS':<10} | {'SERVICE':<15}")
        print("-" * 40)
        for port, service in open_ports:
            print(f"{port:<10} | 🟢 OPEN    | {service:<15}")
    else:
        print("Tidak ditemukan port terbuka pada rentang yang dipindai.")

    print("\n--------------------------------------------------")
    print(f"Selesai! Ditemukan {len(open_ports)} port terbuka.")
    print("==================================================\n")

def main():
    print("=============================================")
    print(" NETWORK PORT SCANNER CLI  ")
    print("=============================================")

    target = input("Masukkan Host/IP target (default: 127.0.0.1): ").strip() or "127.0.0.1"

    print("\nPilih Mode Pemindaian:")
    print(" [1] Common Ports (22 port paling umum)")
    print(" [2] Rentang Port Kustom (misal: 1 sampai 1024)")

    choice = input("\nPilih menu (1/2, default 1): ").strip() or "1"

    if choice == "1":
        ports = COMMON_PORTS
    elif choice == "2":
        try:
            start_port = int(input("Port awal (1-65535): "))
            end_port = int(input("Port akhir (1-65535): "))
            if not (1 <= start_port <= end_port <= 65535):
                print("Rentang port tidak valid!")
                return
            ports = list(range(start_port, end_port + 1))
        except ValueError:
            print("Input harus berupa angka!")
            return
    else:
        print("Pilihan tidak valid!")
        return

    run_scanner(target, ports)

if __name__ == "__main__":
    main()