import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

HISTORY_FILE = "api_history.json"


def load_history() -> list:
    """Membaca riwayat pengujian API dari file JSON."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_history(entry: dict):
    """Menyimpan log request baru ke file JSON."""
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def format_body(raw_bytes: bytes) -> str:
    """Memformat response body agar rapi jika berbentuk JSON."""
    text = raw_bytes.decode("utf-8", errors="replace").strip()
    if not text:
        return "(Empty Response Body)"

    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        return text


def send_http_request(method: str, url: str, headers: dict, body_bytes: bytes | None):
    """Mengirim HTTP request dan menampilkan hasil respon secara detail."""
    req = urllib.request.Request(
        url=url,
        data=body_bytes,
        headers=headers,
        method=method
    )

    start_time = time.time()
    status_code = None
    reason = ""
    resp_headers = {}
    resp_body = b""

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            status_code = response.getcode()
            reason = response.reason
            resp_headers = dict(response.headers.items())
            resp_body = response.read()

    except urllib.error.HTTPError as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        status_code = e.code
        reason = e.reason
        resp_headers = dict(e.headers.items()) if e.headers else {}
        resp_body = e.read()

    except Exception as e:
        print(f"\n Gagal terhubung ke server: {e}\n")
        return

    status_icon = "🟢" if 200 <= status_code < 300 else ("🟡" if 300 <= status_code < 500 else "🔴")

    print("\n=====================================================================")
    print("  HTTP RESPONSE RESULT (Day 028) ")
    print("=====================================================================")
    print(f" Request  : {method} {url}")
    print(f" Status   : {status_icon} {status_code} {reason}")
    print(f" Latency  : {latency_ms} ms")

    print("\n Response Headers (Utama):")
    important_headers = ["Content-Type", "Server", "Date", "Cache-Control"]
    for key in important_headers:
        for h_key, h_val in resp_headers.items():
            if h_key.lower() == key.lower():
                print(f"   {h_key}: {h_val}")

    print("\n Response Body:")
    print("-" * 69)
    formatted_output = format_body(resp_body)
    lines = formatted_output.splitlines()
    for line in lines[:35]:
        print(line)
    if len(lines) > 35:
        print(f"... ({len(lines) - 35} baris lainnya dipotong)")
    print("-" * 69)

    save_history({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "url": url,
        "status_code": status_code,
        "latency_ms": latency_ms
    })
    print(f"Riwayat request dicatat ke: {HISTORY_FILE}\n")


def show_history():
    """Menampilkan 10 riwayat pengujian endpoint terakhir."""
    history = load_history()
    if not history:
        print("\n📭 Belum ada riwayat pengujian API.\n")
        return

    print("\n--------------------------------------------------------------------------------")
    print(f"{'Waktu':<19} | {'Method':<6} | {'Status':<6} | {'Latency':<10} | {'URL'}")
    print("--------------------------------------------------------------------------------")
    for item in history[-10:]:
        lat_str = f"{item['latency_ms']} ms"
        print(
            f"{item['timestamp']:<19} | {item['method']:<6} | "
            f"{item['status_code']:<6} | {lat_str:<10} | {item['url']}"
        )
    print("--------------------------------------------------------------------------------\n")


def main():
    while True:
        print("=============================================")
        print("  HTTP API ENDPOINT TESTER CLI (Day 028) ")
        print("=============================================")
        print(" [1] Kirim HTTP Request (GET / POST / PUT / DELETE)")
        print(" [2] Lihat Riwayat Pengujian")
        print(" [3] Keluar")

        choice = input("\nPilih menu (1-3): ").strip()

        if choice == "1":
            method = input("Metode HTTP (GET/POST/PUT/DELETE, default GET): ").strip().upper() or "GET"
            if method not in ("GET", "POST", "PUT", "DELETE"):
                print("Metode HTTP tidak didukung!\n")
                continue

            default_url = (
                "https://jsonplaceholder.typicode.com/posts/1"
                if method == "GET"
                else "https://jsonplaceholder.typicode.com/posts"
            )
            url = input(f"Masukkan URL endpoint (default: {default_url}): ").strip() or default_url

            if not url.startswith(("http://", "https://")):
                print("URL harus diawali dengan http:// atau https://\n")
                continue

            headers = {
                "User-Agent": "Python-API-Tester-CLI/1.0",
                "Accept": "application/json"
            }

            body_bytes = None
            if method in ("POST", "PUT"):
                payload_file = input("Path file JSON payload (default: payload.json): ").strip() or "payload.json"
                if os.path.exists(payload_file):
                    try:
                        with open(payload_file, "r", encoding="utf-8") as f:
                            payload_obj = json.load(f)
                        body_bytes = json.dumps(payload_obj).encode("utf-8")
                        headers["Content-Type"] = "application/json; charset=utf-8"
                    except json.JSONDecodeError as e:
                        print(f"Format JSON pada '{payload_file}' tidak valid: {e}\n")
                        continue
                else:
                    print(f"File '{payload_file}' tidak ditemukan, mengirim request tanpa body.")

            print(f"\nMengirim {method} request ke {url}...")
            send_http_request(method, url, headers, body_bytes)

        elif choice == "2":
            show_history()

        elif choice == "3":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()