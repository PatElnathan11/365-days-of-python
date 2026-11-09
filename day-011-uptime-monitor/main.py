import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

URLS_FILE = "urls.json"
LOG_FILE = "uptime_log.json"

def check_url(url: str, timeout: int = 5) -> dict:
    """Memeriksa status website dan mengukur latency."""
    start_time = time.time()
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            status_code = response.getcode()
            return {
                "url": url,
                "status": "ONLINE",
                "code": status_code,
                "latency_ms": latency
            }
    except urllib.error.HTTPError as e:
        latency = round((time.time() - start_time) * 1000, 2)
        return {
            "url": url,
            "status": f"HTTP {e.code}",
            "code": e.code,
            "latency_ms": latency
        }
    except (urllib.error.URLError, Exception):
        return {
            "url": url,
            "status": "OFFLINE",
            "code": None,
            "latency_ms": None
        }

def save_log(results: list):
    """Menyimpan riwayat monitoring ke file JSON."""
    history = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_checked": len(results),
        "results": results
    }

    history.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def main():
    print("==================================================")
    print(" WEBSITE UPTIME & LATENCY MONITOR (Day 011) ")
    print("==================================================")

    if not os.path.exists(URLS_FILE):
        print(f"❌ Error: File '{URLS_FILE}' tidak ditemukan!")
        return

    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    print(f"Memeriksa {len(urls)} URL target...\n")

    results = []
    online_count = 0

    print(f"{'URL':<42} | {'Status':<12} | {'Response Time':<12}")
    print("-" * 72)

    for url in urls:
        res = check_url(url)
        results.append(res)
        
        status_str = res['status']
        if status_str == "ONLINE":
            icon = "🟢"
            latency_str = f"{res['latency_ms']} ms"
            online_count += 1
        elif status_str.startswith("HTTP"):
            icon = "🟡"
            latency_str = f"{res['latency_ms']} ms"
        else:
            icon = "🔴"
            latency_str = "N/A"

        print(f"{res['url']:<42} | {icon} {status_str:<9} | {latency_str:<12}")

    print("-" * 72)
    print(f"Ringkasan: {online_count}/{len(urls)} server online.")

    save_log(results)
    print(f"Riwayat log disimpan di: {LOG_FILE}\n")

if __name__ == "__main__":
    main()