import serial
import sounddevice as sd
import numpy as np

port = 'COM9' 
baud_rate = 2000000
sample_rate = 16000

ser = serial.Serial(port, baud_rate)

def callback(outdata, frames, time, status):
    # Baca 4 byte per sample (32-bit)
    raw_data = ser.read(frames * 4) 
    data = np.frombuffer(raw_data, dtype=np.int32)
    
    # Normalisasi data 32-bit ke float untuk speaker
    # SPH0645 seringkali perlu digeser karena datanya 24-bit di dalam wadah 32-bit
    float_data = data.astype(np.float32) / 2147483647.0
    outdata[:] = float_data.reshape(-1, 1)

print("Mulai mendengarkan... (Pastikan baud rate 2.000.000)")
with sd.OutputStream(channels=1, samplerate=sample_rate, dtype='float32', callback=callback):
    try:
        while True:
            pass
    except KeyboardInterrupt:
        ser.close()