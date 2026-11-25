import os
import ssl
import json
import socket
from datetime import datetime, timezone


def extract_field(cert_tuples: tuple, key_name: str) -> str:
    """Mengambil nilai tertentu dari tuple bersarang subject/issuer sertifikat."""
    for group in cert_tuples:
        for key, value in group:
            if key == key_name:
                return value
    return "Unknown"


def check_ssl_certificate(domain: str, port: int = 443, timeout: float = 5.0) -> dict:
    """Mengambil dan menganalisis sertifikat SSL/TLS dari domain target."""
    clean_domain = domain.strip().replace("https://", "").replace("http://", "").split("/")[0]
    context = ssl.create_default_context()

    try:
        with socket.create_connection((clean_domain, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=clean_domain) as ssock:
                cert = ssock.getpeercert()

        not_after_str = cert.get("notAfter", "")
        not_before_str = cert.get("notBefore", "")

        expiry_date = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        issued_date = datetime.strptime(not_before_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)

        days_remaining = (expiry_date - now).days
        issuer_org = extract_field(cert.get("issuer", ()), "organizationName")
        common_name = extract_field(cert.get("subject", ()), "commonName")

        if days_remaining < 0:
            status = "EXPIRED"
        elif days_remaining <= 30:
            status = "EXPIRING SOON"
        else:
            status = "VALID"

        return {
            "domain": clean_domain,
            "status": status,
            "common_name": common_name,
            "issuer": issuer_org,
            "issued_on": issued_date.strftime("%Y-%m-%d"),
            "expires_on": expiry_date.strftime("%Y-%m-%d"),
            "days_remaining": days_remaining,
            "error": None
        }

    except ssl.SSLCertVerificationError as e:
        return {
            "domain": clean_domain,
            "status": "INVALID / UNTRUSTED",
            "common_name": "-",
            "issuer": "-",
            "issued_on": "-",
            "expires_on": "-",
            "days_remaining": None,
            "error": str(e.verify_message)
        }
    except Exception as e:
        return {
            "domain": clean_domain,
            "status": "CONNECTION ERROR",
            "common_name": "-",
            "issuer": "-",
            "issued_on": "-",
            "expires_on": "-",
            "days_remaining": None,
            "error": str(e)
        }


def display_single_result(res: dict):
    """Menampilkan detail sertifikat untuk satu domain."""
    print("\n============================================================")
    print(f" DETAIL SERTIFIKAT SSL: {res['domain']}")
    print("============================================================")
    print(f" Status          : {res['status']}")
    print(f" Common Name     : {res['common_name']}")
    print(f" Penerbit (CA)   : {res['issuer']}")
    print(f" Berlaku Mulai   : {res['issued_on']}")
    print(f" Kedaluwarsa     : {res['expires_on']}")
    if res["days_remaining"] is not None:
        print(f" Sisa Masa Aktif : {res['days_remaining']} hari")
    if res["error"]:
        print(f" Keterangan Error: {res['error']}")
    print("============================================================\n")


def run_batch_check(filepath: str = "domains.txt"):
    """Memeriksa seluruh domain dari file teks dan mengekspor laporan JSON."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' tidak ditemukan!")
        return

    domains = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                domains.append(stripped)

    if not domains:
        print("Daftar domain kosong.")
        return

    print(f"\nMemeriksa sertifikat SSL untuk {len(domains)} domain...\n")
    print(f"{'Domain':<26} | {'Status':<20} | {'Expires On':<12} | {'Sisa Hari':<10}")
    print("-" * 76)

    results = []
    for domain in domains:
        res = check_ssl_certificate(domain)
        results.append(res)

        if res["status"] == "VALID":
            icon = "🟢"
        elif res["status"] == "EXPIRING SOON":
            icon = "🟡"
        else:
            icon = "🔴"

        days_str = f"{res['days_remaining']} hari" if res["days_remaining"] is not None else "-"
        print(f"{res['domain']:<26} | {icon} {res['status']:<17} | {res['expires_on']:<12} | {days_str:<10}")

    print("-" * 76)

    output_file = "ssl_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Laporan audit SSL lengkap disimpan ke: {output_file}\n")


def main():
    while True:
        print("=============================================")
        print("  SSL/TLS CERTIFICATE CHECKER (Day 027) ")
        print("=============================================")
        print(" [1] Cek Satu Domain")
        print(" [2] Cek Massal dari 'domains.txt'")
        print(" [3] Keluar")

        choice = input("\nPilih menu (1-3): ").strip()

        if choice == "1":
            domain = input("Masukkan nama domain (contoh: github.com): ").strip()
            if not domain:
                print("Nama domain tidak boleh kosong!")
                continue
            print(f"Menghubungi {domain}:443...")
            result = check_ssl_certificate(domain)
            display_single_result(result)

        elif choice == "2":
            run_batch_check("domains.txt")

        elif choice == "3":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()