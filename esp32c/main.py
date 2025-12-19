import network
import socket
import time
from machine import I2S, Pin

# --- KONFIGURASI KAMU ---
WIFI_SSID = 'TROVERE1'
WIFI_PASS = '12345678OLU.'
LAPTOP_IP = '10.0.0.35' # Pastikan ini masih IP laptop kamu

# 1. Koneksi WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(1)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)

print("Menghubungkan ke WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi Ok!", wlan.ifconfig()[0])

# 2. Setup Mic SPH0645 (Pin D4, D5, D6)
# SCK=6, WS=7, SD=21
mic = I2S(0, sck=Pin(6), ws=Pin(7), sd=Pin(21),
          mode=I2S.RX, bits=16, format=I2S.MONO,
          rate=16000, ibuf=16000)

# 3. Hubungkan ke Server Node.js di Windows
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Mencoba menyambung ke server...")
try:
    client.connect((LAPTOP_IP, 5000))
    print("Terhubung ke Server!")
except:
    print("Gagal! Pastikan server.js sudah jalan dan port 5000 dibuka.")

# Kirim paket data ukuran 4096 byte agar suara lebih stabil
buf = bytearray(4096)
while True:
    try:
        mic.readinto(buf)
        client.send(buf)
    except Exception as e:
        print("Koneksi putus:", e)
        break
