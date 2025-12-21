import asyncio
import pyaudio
import numpy as np
from bleak import BleakClient, BleakScanner

# Konfigurasi BLE
DEVICE_NAME = "Stezio-Streaming"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
SAMPLE_RATE = 8000
CHUNKS = 400 # Ukuran buffer suara

# Penampung data mentah
raw_buffer = bytearray()

def notification_handler(sender, data):
    global raw_buffer
    raw_buffer.extend(data)

async def start_streaming():
    global raw_buffer
    print(f"Mencari {DEVICE_NAME}...")
    device = await BleakScanner.find_device_by_name(DEVICE_NAME)
    
    if not device:
        print("Perangkat tidak ketemu, cok!")
        return

    # Inisialisasi PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True,
                    frames_per_buffer=CHUNKS)

    try:
        async with BleakClient(device) as client:
            print(f"Terhubung ke {device.address}. Pakai earphone biar jernih!")
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            
            print("Streaming detak jantung berjalan... Tekan Ctrl+C buat berhenti.")
            while True:
                # Jika buffer sudah terkumpul cukup banyak, mainkan
                if len(raw_buffer) >= CHUNKS * 2:
                    data_to_play = raw_buffer[:CHUNKS * 2]
                    raw_buffer = raw_buffer[CHUNKS * 2:]
                    
                    # Tulis langsung ke soundcard laptop
                    stream.write(bytes(data_to_play))
                
                # Jeda tipis biar CPU tidak kerja rodi
                await asyncio.sleep(0.005)
                
    except Exception as e:
        print(f"\nAda masalah: {e}")
    finally:
        print("\nMematikan streaming...")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    asyncio.run(start_streaming())