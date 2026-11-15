import sqlite3
from datetime import datetime

DB_FILE = "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Membuka koneksi ke database SQLite."""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Membuat tabel tasks jika belum ada."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        """)


def add_task():
    """Menambahkan tugas baru ke database."""
    title = input("Masukkan judul tugas: ").strip()
    if not title:
        print(" Judul tugas tidak boleh kosong!")
        return

    print("Pilih prioritas: [1] High  [2] Medium (default)  [3] Low")
    prio_choice = input("Pilihan (1-3): ").strip()
    priority_map = {"1": "High", "2": "Medium", "3": "Low"}
    priority = priority_map.get(prio_choice, "Medium")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (title, priority, status, created_at) VALUES (?, ?, 'Pending', ?)",
            (title, priority, created_at)
        )
    print(f" Tugas '{title}' [{priority}] berhasil ditambahkan!")


def list_tasks(keyword: str = ""):
    """Menampilkan daftar seluruh tugas atau hasil pencarian."""
    with get_connection() as conn:
        if keyword:
            cursor = conn.execute(
                "SELECT id, title, priority, status, created_at FROM tasks WHERE title LIKE ? ORDER BY id ASC",
                (f"%{keyword}%",)
            )
        else:
            cursor = conn.execute(
                "SELECT id, title, priority, status, created_at FROM tasks ORDER BY status DESC, id ASC"
            )
        rows = cursor.fetchall()

    if not rows:
        print("\n📭 Tidak ada tugas yang ditemukan.")
        return

    print("\n--------------------------------------------------------------------------------")
    print(f"{'ID':<4} | {'Status':<11} | {'Prioritas':<9} | {'Dibuat':<16} | {'Judul Tugas'}")
    print("--------------------------------------------------------------------------------")

    for task_id, title, priority, status, created_at in rows:
        status_icon = "✅ Done" if status == "Done" else "⏳ Pending"
        print(f"{task_id:<4} | {status_icon:<11} | {priority:<9} | {created_at:<16} | {title}")

    print("--------------------------------------------------------------------------------")


def complete_task():
    """Menandai tugas sebagai selesai berdasarkan ID."""
    list_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang sudah selesai: ").strip())
    except ValueError:
        print(" ID harus berupa angka!")
        return

    with get_connection() as conn:
        cursor = conn.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print(f" Tugas dengan ID {task_id} tidak ditemukan.")
        else:
            print(f" Tugas ID {task_id} ditandai selesai!")


def delete_task():
    """Menghapus tugas dari database berdasarkan ID."""
    list_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang ingin dihapus: ").strip())
    except ValueError:
        print("ID harus berupa angka!")
        return

    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print(f"Tugas dengan ID {task_id} tidak ditemukan.")
        else:
            print(f"Tugas ID {task_id} berhasil dihapus!")


def main():
    init_db()
    while True:
        print("\n===========================================")
        print(" SQLITE TASK MANAGER CLI  ")
        print("===========================================")
        print(" [1] Tambah Tugas Baru")
        print(" [2] Lihat Semua Tugas")
        print(" [3] Tandai Tugas Selesai")
        print(" [4] Cari Tugas")
        print(" [5] Hapus Tugas")
        print(" [6] Keluar")

        choice = input("\nPilih menu (1-6): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            kw = input("Masukkan kata kunci pencarian: ").strip()
            list_tasks(kw)
        elif choice == "5":
            delete_task()
        elif choice == "6":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()