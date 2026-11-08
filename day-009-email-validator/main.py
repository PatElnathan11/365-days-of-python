import os
import re
import socket
import json

# Pattern Regex yang lebih ketat (mencegah titik berturut-turut di domain)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

def is_valid_syntax(email: str) -> bool:
    """Mengecek apakah format/sintaks email sesuai standar."""
    return bool(EMAIL_REGEX.match(email))

def is_domain_active(domain: str) -> bool:
    """Mengecek apakah domain memiliki DNS record aktif."""
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        # Menangkap socket.gaierror, UnicodeError, maupun error domain malformed lainnya
        return False

def validate_email(email: str) -> dict:
    """Proses evaluasi dua tahap: Sintaks & Domain."""
    email = email.strip()
    if not email:
        return None

    syntax_ok = is_valid_syntax(email)
    domain_ok = False
    status = "Invalid Syntax"

    if syntax_ok:
        domain = email.split('@')[1]
        domain_ok = is_domain_active(domain)
        status = "Valid" if domain_ok else "Domain Not Found"

    return {
        "email": email,
        "syntax_valid": syntax_ok,
        "domain_active": domain_ok,
        "status": status
    }

def main():
    print("==============================================")
    print(" BULK EMAIL VALIDATOR CLI (Day 009) ")
    print("==============================================")

    input_file = "emails.txt"

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' tidak ditemukan!")
        return

    print(f"Membaca daftar email dari '{input_file}'...\n")

    results = []
    valid_count = 0

    with open(input_file, "r", encoding="utf-8") as f:
        emails = f.readlines()

    print(f"{'Email':<42} | {'Status':<18}")
    print("-" * 64)

    for line in emails:
        res = validate_email(line)
        if res:
            results.append(res)
            icon = "✅" if res["status"] == "Valid" else "❌"
            print(f"{res['email']:<42} | {icon} {res['status']:<18}")
            if res["status"] == "Valid":
                valid_count += 1

    print("-" * 64)
    print(f"Ringkasan: {valid_count}/{len(results)} email valid.")

    # Export laporan ke JSON
    output_file = "validation_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Laporan lengkap disimpan di: {output_file}\n")

if __name__ == "__main__":
    main()