import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses() -> list:
    """Membaca data pengeluaran dari file JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses: list):
    """Menyimpan data pengeluaran ke file JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses: list):
    """Menambahkan item pengeluaran baru."""
    description = input("Masukkan deskripsi pengeluaran: ").strip()
    if not description:
        print("Deskripsi tidak boleh kosong!")
        return

    try:
        amount = float(input("Masukkan jumlah (Rp): "))
    except ValueError:
        print("Jumlah harus berupa angka!")
        return

    category = input("Masukkan kategori (Makanan/Transport/Hiburan/Lainnya): ").strip() or "Lainnya"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    expense = {
        "description": description,
        "amount": amount,
        "category": category,
        "date": date_str
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Pengeluaran berhasil dicatat!")

def show_expenses(expenses: list):
    """Menampilkan riwayat dan total pengeluaran."""
    if not expenses:
        print("\n  Belum ada catatan pengeluaran.")
        return

    print("\n----------------------------------------------------------------------")
    print(f"{'No':<4} | {'Tanggal':<16} | {'Kategori':<12} | {'Deskripsi':<18} | {'Jumlah (Rp)':<10}")
    print("----------------------------------------------------------------------")

    total = 0
    for idx, item in enumerate(expenses, 1):
        print(f"{idx:<4} | {item['date']:<16} | {item['category']:<12} | {item['description']:<18} | Rp{item['amount']:,.0f}")
        total += item['amount']

    print("----------------------------------------------------------------------")
    print(f"  Total Pengeluaran: Rp{total:,.0f}")
    print("----------------------------------------------------------------------")

def main():
    expenses = load_expenses()
    while True:
        print("\n===================================")
        print("   EXPENSE TRACKER CLI (Day 005) ")
        print("===================================")
        print(" [1] Tambah Pengeluaran")
        print(" [2] Lihat Semua Pengeluaran")
        print(" [3] Keluar")

        choice = input("\nPilih menu (1-3): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            print("Sampai jumpa! Tetap hemat!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()