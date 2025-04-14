import network
import urequests
import time
import dht
from machine import Pin

# ======= KONFIGURASI WIFI =======
SSID = "OrangGantengPekanbaru"  # Ganti dengan nama WiFi
PASSWORD = "12345678"  # Ganti dengan password WiFi

# ======= ALAMAT SERVER =======
SERVER_URL = "http://192.168.170.240:5000/temperature"  # Ganti sesuai IP server Flask kamu

# ======= INISIALISASI SENSOR =======
sensor = dht.DHT11(Pin(4))  # Gunakan D4 (GPIO 4)

# ======= FUNGSI: KONEKSI WIFI =======
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("[INFO] Menghubungkan ke Wi-Fi...")
        wlan.connect(SSID, PASSWORD)

        timeout = 10  # detik
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                print("[ERROR] Gagal konek Wi-Fi!")
                return False
            time.sleep(1)
    print(f"[SUCCESS] Terhubung ke Wi-Fi! IP: {wlan.ifconfig()[0]}")
    return True

# ======= FUNGSI: BACA & KIRIM SUHU =======
def read_and_send_temperature():
    try:
        print("\n[INFO] Mengukur suhu...")
        sensor.measure()
        temp = sensor.temperature()
        print(f"[DATA] Temperature: {temp}°C")

        payload = {"temperature": temp}
        print(f"[INFO] Kirim data ke server: {SERVER_URL}")
        response = urequests.post(SERVER_URL, json=payload)
        print("[SUCCESS] Server response:", response.text)
        response.close()

    except Exception as e:
        print("[ERROR] Gagal kirim data:", e)

# ======= PROGRAM UTAMA =======
if connect_wifi():
    while True:
        read_and_send_temperature()
        time.sleep(10)  # setiap 10 detik
else:
    print("[FATAL] Tidak dapat menjalankan program karena Wi-Fi gagal.")


