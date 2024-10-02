import spidev
import numpy as np
import wave
from time import sleep
from time import time
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device), for CE0
spi.max_speed_hz = 7500000
spi.mode = 0

def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

num_samples = 100000
signal0 = np.zeros(num_samples)
signal1 = np.zeros(num_samples)
signal2 = np.zeros(num_samples)
signal3 = np.zeros(num_samples)

print("Recording...")
tb = time()
for i in range(0, num_samples):
    signal0[i] = ReadChannel(0)
    signal1[i] = ReadChannel(1)
    signal2[i] = ReadChannel(2)
    signal3[i] = ReadChannel(3)
ta = time()
print("Recording finished.")

td = ta - tb
sampling_rate = int(num_samples/td)
print("approx sample rate (Hz): ", sampling_rate)

plt.plot(signal0)
plt.savefig('channel0.png')

plt.plot(signal1)
plt.savefig('channel1.png')

plt.plot(signal2)
plt.savefig('channel2.png')

plt.plot(signal3)
plt.savefig('channel3.png')

signal0 = signal0.astype("<h")
with wave.open("channel0.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sampling_rate)
    f.writeframes(signal0.tobytes())

signal1 = signal1.astype("<h")
with wave.open("channel1.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sampling_rate)
    f.writeframes(signal1.tobytes())

signal2 = signal2.astype("<h")
with wave.open("channel2.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sampling_rate)
    f.writeframes(signal2.tobytes())

signal3 = signal3.astype("<h")
with wave.open("channel3.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sampling_rate)
    f.writeframes(signal3.tobytes())

# Close SPI connection
spi.close()