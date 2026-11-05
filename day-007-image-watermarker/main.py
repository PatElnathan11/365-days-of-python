import os
from PIL import Image, ImageDraw, ImageFont

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

def add_watermark_and_resize(
    input_dir: str,
    output_dir: str,
    watermark_text: str,
    max_width: int = 1080
):
    """Meresize gambar dan menambahkan watermark teks."""
    if not os.path.exists(input_dir):
        print(f"Folder '{input_dir}' tidak ditemukan!")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(SUPPORTED_EXTENSIONS)]

    if not files:
        print(f"Tidak ada file gambar ditemukan di folder '{input_dir}'!")
        return

    print(f"\nDitemukan {len(files)} gambar. Memproses...\n")

    for file_name in files:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, f"wm_{file_name}")

        try:
            with Image.open(input_path).convert("RGBA") as base_img:
                # 1. Resize Gambar (Maintain Aspect Ratio)
                orig_w, orig_h = base_img.size
                if orig_w > max_width:
                    ratio = max_width / float(orig_w)
                    new_h = int(float(orig_h) * ratio)
                    base_img = base_img.resize((max_width, new_h), Image.Resampling.LANCZOS)

                # 2. Buat Lapisan Watermark (Transparent Overlay)
                txt_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt_layer)

                # Ukuran font proporsional dengan lebar gambar
                font_size = max(16, int(base_img.width * 0.035))
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()

                # Tentukan Posisi Teks (Pojok Kanan Bawah)
                margin = 20
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                
                x = base_img.width - text_w - margin
                y = base_img.height - text_h - margin

                # Menggambar teks watermark dengan transparansi (R, G, B, Opacity)
                draw.text((x, y), watermark_text, fill=(255, 255, 255, 160), font=font)

                # Combine gambar asli dengan watermark
                watermarked = Image.alpha_composite(base_img, txt_layer)

                # Simpan gambar (Konversi balik ke RGB jika file JPEG)
                if file_name.lower().endswith(('.jpg', '.jpeg')):
                    watermarked = watermarked.convert("RGB")
                    watermarked.save(output_path, "JPEG", quality=90)
                else:
                    watermarked.save(output_path)

                print(f" Berhasil: {file_name} -> output/wm_{file_name}")

        except Exception as e:
            print(f" Gagal memproses {file_name}: {e}")

    print(f"\nSelesai! Seluruh gambar tersimpan di folder: {output_dir}")

def main():
    print("============================================")
    print("    IMAGE RESIZER & WATERMARKER (Day 007) ")
    print("============================================")
    
    text = input("Masukkan Teks Watermark (default: © 365DaysOfPython): ").strip()
    if not text:
        text = "© 365DaysOfPython"

    try:
        width = int(input("Masukkan Lebar Maksimum Gambar (px, default 1080): ") or 1080)
    except ValueError:
        width = 1080

    input_dir = "."
    output_dir = "output"

    add_watermark_and_resize(input_dir, output_dir, text, width)

if __name__ == "__main__":
    main()