import serial
import wave
import time
import numpy as np

# Pengaturan
port = 'COM9' 
baud_rate = 2000000
sample_rate = 16000
durasi_detik = 10
nama_file = "hasil_rekaman_jernih.wav"

try:
    ser = serial.Serial(port, baud_rate, timeout=1)
    print(f"Terhubung ke {port}. Menyiapkan rekaman...")
    time.sleep(2)
except Exception as e:
    print(f"Gagal: {e}")
    exit()

print(f"Mulai merekam selama {durasi_detik} detik...")

# Kita baca dalam chunk agar tidak membebani memori
bytes_per_sample = 4 # Karena kita kirim 32-bit dari Arduino
total_samples = sample_rate * durasi_detik
audio_data_16bit = []

start_time = time.time()
try:
    while len(audio_data_16bit) < total_samples:
        if ser.in_waiting >= bytes_per_sample:
            # Baca 4 byte data mentah
            raw_data = ser.read(bytes_per_sample)
            # Konversi ke integer 32-bit
            sample_32 = int.from_bytes(raw_data, byteorder='little', signed=True)
            
            # SPH0645 butuh bit-shift agar suaranya normal
            # Kita geser ke kanan dan batasi ke range 16-bit
            sample_16 = sample_32 >> 14
            
            # Pastikan nilai tetap di dalam batas int16
            if sample_16 > 32767: sample_16 = 32767
            elif sample_16 < -32768: sample_16 = -32768
            
            audio_data_16bit.append(int(sample_16))
            
            if len(audio_data_16bit) % 1600 == 0:
                print(f"Proses: {len(audio_data_16bit)} / {total_samples} samples", end='\r')
except KeyboardInterrupt:
    print("\nBerhenti.")

# Simpan ke file WAV
audio_np = np.array(audio_data_16bit, dtype=np.int16)
with wave.open(nama_file, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2) # 2 byte = 16-bit
    wf.setframerate(sample_rate)
    wf.writeframes(audio_np.tobytes())

print(f"\nSelesai! File disimpan sebagai: {nama_file}")
ser.close()