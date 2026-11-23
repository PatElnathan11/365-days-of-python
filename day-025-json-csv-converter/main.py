import csv
import json
from pathlib import Path


def parse_value(raw_value: str):
    """Mengonversi string dari CSV menjadi tipe data Python yang sesuai."""
    cleaned = raw_value.strip()
    if cleaned == "":
        return None

    lower_val = cleaned.lower()
    if lower_val == "true":
        return True
    if lower_val == "false":
        return False

    try:
        return int(cleaned)
    except ValueError:
        pass

    try:
        return float(cleaned)
    except ValueError:
        pass

    return cleaned


def preview_records(records: list[dict], limit: int = 5):
    """Menampilkan pratinjau data berbentuk tabel sederhana di terminal."""
    if not records:
        print(" Tidak ada data untuk ditampilkan.")
        return

    headers = []
    for row in records:
        for key in row.keys():
            if key not in headers:
                headers.append(key)

    header_line = " | ".join(f"{h:<16}" for h in headers)
    print("\n" + "-" * len(header_line))
    print(header_line)
    print("-" * len(header_line))

    for row in records[:limit]:
        cells = []
        for h in headers:
            val = row.get(h, "")
            val_str = "" if val is None else str(val)
            if len(val_str) > 16:
                val_str = val_str[:13] + "..."
            cells.append(f"{val_str:<16}")
        print(" | ".join(cells))

    print("-" * len(header_line))
    print(f" Menampilkan {min(len(records), limit)} dari total {len(records)} baris data.\n")


def json_to_csv(input_path_str: str, output_path_str: str):
    """Mengonversi file JSON (list of dicts) menjadi file CSV."""
    input_path = Path(input_path_str)
    if not input_path.exists() or not input_path.is_file():
        print(f" Error: File '{input_path_str}' tidak ditemukan!")
        return

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f" Error: Format JSON tidak valid ({e})")
        return

    if not isinstance(data, list) or len(data) == 0:
        print(" File JSON harus berisi daftar (array) objek yang tidak kosong!")
        return

    # Kumpulkan semua nama kolom unik secara berurutan
    fieldnames = []
    for item in data:
        if isinstance(item, dict):
            for key in item.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

    output_path = Path(output_path_str)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            if isinstance(item, dict):
                writer.writerow(item)

    print(f"\n Berhasil mengonversi '{input_path.name}' -> '{output_path.name}'!")
    preview_records(data)


def csv_to_json(input_path_str: str, output_path_str: str, infer_types: bool = True):
    """Mengonversi file CSV menjadi file JSON."""
    input_path = Path(input_path_str)
    if not input_path.exists() or not input_path.is_file():
        print(f" Error: File '{input_path_str}' tidak ditemukan!")
        return

    records = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {}
            for key, value in row.items():
                if key is None:
                    continue
                clean_key = key.strip()
                if infer_types and value is not None:
                    clean_row[clean_key] = parse_value(value)
                else:
                    clean_row[clean_key] = value.strip() if value is not None else None
            records.append(clean_row)

    output_path = Path(output_path_str)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

    print(f"\n Berhasil mengonversi '{input_path.name}' -> '{output_path.name}'!")
    preview_records(records)


def main():
    while True:
        print("=================================================")
        print("  JSON & CSV FORMAT CONVERTER CLI (Day 025) ")
        print("=================================================")
        print(" [1] Konversi JSON -> CSV")
        print(" [2] Konversi CSV  -> JSON")
        print(" [3] Keluar")

        choice = input("\nPilih menu (1-3): ").strip()

        if choice == "1":
            src = input("File JSON sumber (default: sample_users.json): ").strip() or "sample_users.json"
            dst = input("File CSV tujuan  (default: output_users.csv): ").strip() or "output_users.csv"
            json_to_csv(src, dst)

        elif choice == "2":
            src = input("File CSV sumber  (default: output_users.csv): ").strip() or "output_users.csv"
            dst = input("File JSON tujuan (default: converted_users.json): ").strip() or "converted_users.json"
            infer = input("Deteksi tipe data otomatis untuk angka/boolean? (Y/n): ").strip().lower()
            csv_to_json(src, dst, infer_types=(infer != "n"))

        elif choice == "3":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()