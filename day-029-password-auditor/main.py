import re
import math
import json
import secrets
import string
from getpass import getpass

WORD_LIST = [
    "atlas", "beacon", "cipher", "delta", "ember", "falcon", "glacier",
    "horizon", "ignite", "jasper", "krypton", "lantern", "meteor", "nebula",
    "orbit", "pixel", "quantum", "raven", "summit", "titan", "ultra",
    "vortex", "whisper", "xenon", "zenith", "cobalt", "matrix", "prism"
]

COMMON_PATTERNS = [
    r"12345", r"qwerty", r"password", r"admin", r"iloveyou",
    r"abcde", r"11111", r"00000", r"letmein", r"welcome"
]


def generate_secure_password(length: int = 16, use_symbols: bool = True) -> str:
    """Menghasilkan password acak yang memenuhi seluruh kategori karakter."""
    if length < 8:
        length = 8

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}<>?" if use_symbols else ""

    # Pastikan minimal 1 karakter dari setiap kategori terpilih
    required_chars = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
    ]
    if use_symbols:
        required_chars.append(secrets.choice(symbols))

    full_pool = lower + upper + digits + symbols
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(full_pool) for _ in range(remaining_length)]

    # Acak urutan karakter menggunakan SystemRandom
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def generate_passphrase(word_count: int = 4) -> str:
    """Menghasilkan passphrase acak dengan sisipan angka."""
    words = [secrets.choice(WORD_LIST).capitalize() for _ in range(word_count)]
    random_num = str(secrets.randbelow(900) + 100)
    insert_pos = secrets.randbelow(len(words))
    words.insert(insert_pos, random_num)
    return "-".join(words)


def estimate_crack_time(entropy_bits: float) -> str:
    """Memperkirakan waktu brute-force (asumsi 10 miliar tebakan/detik)."""
    guesses_per_sec = 10_000_000_000
    combinations = 2 ** entropy_bits
    seconds = combinations / guesses_per_sec

    if seconds < 1:
        return "Instan (< 1 detik)"
    elif seconds < 60:
        return f"{seconds:.1f} detik"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} menit"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} jam"
    elif seconds < 31_536_000:
        return f"{seconds / 86400:.1f} hari"
    elif seconds < 31_536_000 * 1000:
        return f"{seconds / 31_536_000:.1f} tahun"
    return "Ribuan hingga jutaan tahun"


def audit_password(password: str) -> dict:
    """Menganalisis kekuatan, entropi, dan kelemahan sebuah password."""
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_symbol:
        pool_size += 32

    entropy = round(length * math.log2(pool_size), 2) if pool_size > 0 else 0.0
    warnings = []

    if length < 12:
        warnings.append("Panjang password kurang dari 12 karakter.")
    if not has_upper or not has_lower:
        warnings.append("Gunakan kombinasi huruf besar dan huruf kecil.")
    if not has_digit:
        warnings.append("Tambahkan angka untuk memperbesar ruang kombinasi.")
    if not has_symbol:
        warnings.append("Tambahkan karakter simbol (!@#$...) untuk ketahanan ekstra.")

    lower_pwd = password.lower()
    for pattern in COMMON_PATTERNS:
        if re.search(pattern, lower_pwd):
            warnings.append(f"Mengandung pola umum yang mudah ditebak ('{pattern}').")
            entropy = max(0.0, round(entropy - 20.0, 2))

    if re.search(r"(.)\1{2,}", password):
        warnings.append("Terdapat karakter berulang berturut-turut (misal: 'aaa' atau '111').")

    if entropy < 40:
        rating = "🔴 SANGAT LEMAH"
    elif entropy < 60:
        rating = "🟠 LEMAH"
    elif entropy < 80:
        rating = "🟡 CUKUP KUAT"
    elif entropy < 100:
        rating = "🟢 KUAT"
    else:
        rating = "🛡️  SANGAT KUAT"

    return {
        "length": length,
        "pool_size": pool_size,
        "entropy_bits": entropy,
        "rating": rating,
        "crack_time": estimate_crack_time(entropy),
        "warnings": warnings
    }


def display_audit_result(report: dict):
    """Menampilkan hasil audit kekuatan password di terminal."""
    print("\n============================================================")
    print("  HASIL AUDIT KEKUATAN PASSWORD (Day 029) ")
    print("============================================================")
    print(f" Status Kekuatan : {report['rating']}")
    print(f" Panjang Karakter: {report['length']} karakter")
    print(f" Skor Entropi    : {report['entropy_bits']} bits")
    print(f" Estimasi Crack  : {report['crack_time']}")

    if report["warnings"]:
        print("\n Saran Perbaikan:")
        for warn in report["warnings"]:
            print(f"   - {warn}")
    else:
        print("\nTidak ditemukan kelemahan struktural yang umum!")
    print("============================================================\n")


def main():
    while True:
        print("=================================================")
        print(" PASSWORD GENERATOR & AUDITOR CLI  ")
        print("=================================================")
        print(" [1] Generate Password Acak Aman")
        print(" [2] Generate Passphrase (Mudah Diingat)")
        print(" [3] Audit Kekuatan Password")
        print(" [4] Keluar")

        choice = input("\nPilih menu (1-4): ").strip()

        if choice == "1":
            try:
                length_input = input("Panjang password (minimal 8, default 16): ").strip()
                length = int(length_input) if length_input else 16
            except ValueError:
                print("Input harus berupa angka!\n")
                continue

            sym_choice = input("Sertakan simbol khusus? (Y/n): ").strip().lower()
            use_symbols = sym_choice != "n"

            pwd = generate_secure_password(length, use_symbols)
            audit = audit_password(pwd)

            print(f"\nPassword Baru : {pwd}")
            print(f"Entropi       : {audit['entropy_bits']} bits ({audit['rating']})\n")

            save_opt = input("Simpan ke 'generated_passwords.json'? (y/N): ").strip().lower()
            if save_opt == "y":
                with open("generated_passwords.json", "w", encoding="utf-8") as f:
                    json.dump({"password": pwd, "audit": audit}, f, indent=4)
                print("Disimpan ke generated_passwords.json!\n")

        elif choice == "2":
            phrase = generate_passphrase(4)
            audit = audit_password(phrase)
            print(f"\n  Passphrase Baru : {phrase}")
            print(f"Entropi         : {audit['entropy_bits']} bits ({audit['rating']})\n")

        elif choice == "3":
            pwd_to_check = getpass("Masukkan password yang ingin diaudit (input tersembunyi): ")
            if not pwd_to_check:
                print("Password tidak boleh kosong!\n")
                continue
            report = audit_password(pwd_to_check)
            display_audit_result(report)

        elif choice == "4":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()