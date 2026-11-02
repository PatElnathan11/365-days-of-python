import secrets
import string
import re

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True) -> str:
    """Membuat password acak berbasis modul secrets."""
    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def check_password_strength(password: str):
    """Mengecek kekuatan password berdasarkan kriteria tertentu."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("- Minimal panjang 8 karakter.")

    if len(password) >= 12:
        score += 1

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("- Tambahkan setidaknya satu huruf besar (A-Z).")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("- Tambahkan setidaknya satu huruf kecil (a-z).")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("- Tambahkan setidaknya satu angka (0-9).")

    if re.search(r'[\W_]', password):
        score += 1
    else:
        feedback.append("- Tambahkan setidaknya satu simbol khusus (!@#$%^&*).")

    # Evaluasi Tingkat Keamanan
    if score <= 2:
        rating = "🔴 Lemah"
    elif score <= 4:
        rating = "🟡 Sedang"
    else:
        rating = "🟢 Sangat Kuat"

    return rating, feedback

def main():
    print("===========================================")
    print("   PASSWORD GENERATOR & CHECKER (Day 004) ")
    print("===========================================")
    print("Pilih mode:")
    print(" [1] Generate Password Baru")
    print(" [2] Cek Keamanan Password")
    
    choice = input("\nMasukkan pilihan (1/2): ").strip()

    if choice == "1":
        try:
            length = int(input("Masukkan panjang password (default 12): ") or 12)
        except ValueError:
            length = 12
            
        upper = input("Sertakan huruf besar? (y/n, default y): ").lower() != 'n'
        digits = input("Sertakan angka? (y/n, default y): ").lower() != 'n'
        symbols = input("Sertakan simbol? (y/n, default y): ").lower() != 'n'

        pwd = generate_password(length, upper, digits, symbols)
        strength, _ = check_password_strength(pwd)

        print("\n-------------------------------------------")
        print(f"Password Terbuat : {pwd}")
        print(f"Tingkat Keamanan : {strength}")
        print("-------------------------------------------")

    elif choice == "2":
        pwd = input("\nMasukkan password yang ingin dicek: ").strip()
        strength, suggestions = check_password_strength(pwd)

        print("\n-------------------------------------------")
        print(f"Status Keamanan : {strength}")
        if suggestions:
            print("Saran perbaikan:")
            for s in suggestions:
                print(f"  {s}")
        print("-------------------------------------------")
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()