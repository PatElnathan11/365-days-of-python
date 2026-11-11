import os
import csv

def clean_csv_data(input_file: str, output_file: str, drop_missing: bool = False):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' tidak ditemukan!")
        return

    cleaned_rows = []
    seen_rows = set()
    total_original = 0
    duplicate_count = 0
    missing_count = 0

    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = [field.strip() for field in reader.fieldnames]

        for row in reader:
            total_original += 1
            # 1. Trim whitespace untuk setiap key dan value
            cleaned_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k is not None}

            # 2. Cek apakah ada missing values (sel kosong)
            has_missing = any(val == "" for val in cleaned_row.values())
            if has_missing:
                missing_count += 1
                if drop_missing:
                    continue  # Lewati baris ini jika user memilih hapus missing values

            # 3. Cek duplikasi baris
            row_tuple = tuple(cleaned_row.items())
            if row_tuple in seen_rows:
                duplicate_count += 1
                continue
            
            seen_rows.add(row_tuple)
            cleaned_rows.append(cleaned_row)

    # Tulis hasil pembersihan ke file baru
    with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("==============================================")
    print(" CSV DATA CLEANER REPORT (Day 013) ")
    print("==============================================")
    print(f"Total baris awal     : {total_original}")
    print(f"Baris duplikat dihapus: {duplicate_count}")
    print(f"Baris bersel kosong  : {missing_count} {'(Dihapus)' if drop_missing else '(Dipertahankan)'}")
    print(f"Total baris bersih   : {len(cleaned_rows)}")
    print("----------------------------------------------")
    print(f"Hasil disimpan ke    : {output_file}\n")

def main():
    print("==============================================")
    print(" CSV DATA FILTER & CLEANER CLI ")
    print("==============================================")

    input_file = "sample.csv"
    output_file = "cleaned_output.csv"

    print("Opsi Pembersihan:")
    print(" [1] Hapus duplikat & trim spasi saja")
    print(" [2] Hapus duplikat, trim spasi, DAN hapus baris yang ada kolom kosong")

    choice = input("\nPilih opsi (1/2, default 1): ").strip()
    drop_missing = choice == "2"

    clean_csv_data(input_file, output_file, drop_missing)

if __name__ == "__main__":
    main()