import spidev
from time import sleep
from time import time
import numpy as np

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device), for CE0

spi.max_speed_hz = 20000000
spi.mode = 0

def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

num_samples = 10000
signal = np.zeros(num_samples)

tb = time()
for i in range(0, num_samples):
    signal[i] = ReadChannel(0)
ta = time()

td = ta - tb
print("elapsed time: ", td)
print("approx sample rate (Hz): ", num_samples/td)