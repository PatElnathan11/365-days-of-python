import os
import hmac
import hashlib
import secrets
from pathlib import Path
from getpass import getpass

MAGIC_HEADER = b"PYVAULT1"
SALT_SIZE = 16
MAC_SIZE = 32
ITERATIONS = 100_000


def derive_keys(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """Menurunkan kunci enkripsi dan kunci autentikasi (MAC) dari password."""
    master_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=64
    )
    enc_key = master_key[:32]
    mac_key = master_key[32:]
    return enc_key, mac_key


def xor_stream_transform(data: bytes, enc_key: bytes, salt: bytes) -> bytes:
    """Mengenkripsi atau mendekripsi bytes menggunakan keystream berbasis SHA-256."""
    output = bytearray(len(data))
    block_index = 0
    position = 0

    while position < len(data):
        counter_bytes = block_index.to_bytes(8, "big")
        keystream_block = hashlib.sha256(enc_key + salt + counter_bytes).digest()

        for byte_val in keystream_block:
            if position >= len(data):
                break
            output[position] = data[position] ^ byte_val
            position += 1

        block_index += 1

    return bytes(output)


def encrypt_file(input_path_str: str, password: str):
    """Mengenkripsi file dan menyimpan hasilnya dengan ekstensi .enc."""
    input_path = Path(input_path_str)
    if not input_path.exists() or not input_path.is_file():
        print(f" Error: File '{input_path_str}' tidak ditemukan!")
        return

    with open(input_path, "rb") as f:
        plaintext = f.read()

    salt = secrets.token_bytes(SALT_SIZE)
    enc_key, mac_key = derive_keys(password, salt)
    ciphertext = xor_stream_transform(plaintext, enc_key, salt)

    payload_without_mac = MAGIC_HEADER + salt + ciphertext
    mac_tag = hmac.new(mac_key, payload_without_mac, hashlib.sha256).digest()

    output_path = Path(f"{input_path}.enc")
    with open(output_path, "wb") as f:
        f.write(payload_without_mac + mac_tag)

    print("\n File berhasil dienkripsi!")
    print(f"  File Asli  : {input_path.name} ({len(plaintext)} bytes)")
    print(f"  File Vault : {output_path.name} ({output_path.stat().st_size} bytes)")


def decrypt_file(input_path_str: str, password: str):
    """Memverifikasi integritas file .enc dan mendekripsinya kembali."""
    input_path = Path(input_path_str)
    if not input_path.exists() or not input_path.is_file():
        print(f" Error: File '{input_path_str}' tidak ditemukan!")
        return

    with open(input_path, "rb") as f:
        raw_data = f.read()

    min_length = len(MAGIC_HEADER) + SALT_SIZE + MAC_SIZE
    if len(raw_data) < min_length or not raw_data.startswith(MAGIC_HEADER):
        print(" Error: Format file tidak valid atau bukan file hasil enkripsi PyVault!")
        return

    header_end = len(MAGIC_HEADER)
    salt_end = header_end + SALT_SIZE

    salt = raw_data[header_end:salt_end]
    ciphertext = raw_data[salt_end:-MAC_SIZE]
    stored_mac = raw_data[-MAC_SIZE:]

    enc_key, mac_key = derive_keys(password, salt)
    expected_mac = hmac.new(mac_key, raw_data[:-MAC_SIZE], hashlib.sha256).digest()

    if not hmac.compare_digest(stored_mac, expected_mac):
        print(" Gagal Dekripsi: Password salah atau file telah dimodifikasi!")
        return

    plaintext = xor_stream_transform(ciphertext, enc_key, salt)

    if input_path.suffix == ".enc":
        restored_name = f"decrypted_{input_path.stem}"
    else:
        restored_name = f"decrypted_{input_path.name}"

    output_path = input_path.parent / restored_name
    with open(output_path, "wb") as f:
        f.write(plaintext)

    print("\n File berhasil didekripsi dan integritas terverifikasi!")
    print(f"  Hasil Dekripsi : {output_path.name} ({len(plaintext)} bytes)")


def main():
    while True:
        print("\n=============================================")
        print("   FILE ENCRYPTOR & VAULT CLI (Day 024) ")
        print("=============================================")
        print(" [1] Enkripsi File")
        print(" [2] Dekripsi File (.enc)")
        print(" [3] Keluar")

        choice = input("\nPilih menu (1-3): ").strip()

        if choice == "1":
            target = input("Masukkan nama/path file (default: secret_notes.txt): ").strip() or "secret_notes.txt"
            pwd = getpass("Masukkan password enkripsi (input tersembunyi): ")
            if not pwd:
                print("⚠️ Password tidak boleh kosong!")
                continue
            confirm_pwd = getpass("Konfirmasi password: ")
            if pwd != confirm_pwd:
                print("Password tidak cocok!")
                continue
            encrypt_file(target, pwd)

        elif choice == "2":
            target = input("Masukkan nama/path file .enc (default: secret_notes.txt.enc): ").strip() or "secret_notes.txt.enc"
            pwd = getpass("Masukkan password dekripsi: ")
            if not pwd:
                print("Password tidak boleh kosong!")
                continue
            decrypt_file(target, pwd)

        elif choice == "3":
            print("Berhasil keluar")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()