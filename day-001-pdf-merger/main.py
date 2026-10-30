import os
from pypdf import PdfWriter

def merge_pdfs(directory: str, output_filename: str):
    merger = PdfWriter()  # Menggunakan PdfWriter
    
    pdf_files = [
        f for f in os.listdir(directory) 
        if f.endswith('.pdf') and f != output_filename
    ]
    
    pdf_files.sort()
    
    if not pdf_files:
        print("file PDF tidak ditemukan")
        return

    print(f"Ditemukan {len(pdf_files)} file PDF untuk digabungkan:")
    for pdf in pdf_files:
        file_path = os.path.join(directory, pdf)
        print(f"   -> Menambahkan: {pdf}")
        merger.append(file_path)
    
    output_path = os.path.join(directory, output_filename)
    merger.write(output_path)
    merger.close()
    
    print(f"\nBerhasil! File gabungan disimpan sebagai: {output_filename}")

if __name__ == "__main__":
    current_directory = "."
    output_file = "merged_result.pdf"
    
    merge_pdfs(current_directory, output_file)