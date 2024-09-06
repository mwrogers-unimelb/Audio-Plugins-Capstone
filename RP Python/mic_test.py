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

spi.max_speed_hz = 4000000
spi.mode = 0

def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

num_samples = 1000000
signal = np.zeros(num_samples)

tb = time()
for i in range(0, num_samples):
    signal[i] = ReadChannel(0)
ta = time()

td = ta - tb
sampling_rate = int(num_samples/td)
print("approx sample rate (Hz): ", sampling_rate)

plt.plot(signal)
plt.savefig('audio.png')

signal = signal.astype("<h")
with wave.open("gpiozero_audio.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sampling_rate)
    f.writeframes(signal.tobytes())

# Close SPI connection
spi.close()