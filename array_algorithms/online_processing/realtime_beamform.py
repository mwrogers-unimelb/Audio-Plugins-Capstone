import queue
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import pyroomacoustics as pra

length = 200000
deviceID = 20
channels = 8
Fs = 44100
interval = 10
blocksize = 20000


fig, ax = plt.subplots()
plotdata = np.zeros(length)
lines = []
line, = ax.plot(plotdata)
q = queue.Queue()
plt.ion()


def audio_callback(indata,frames,time,status):
    return_data = indata[:,0]
    q.put(return_data[::5])
    pass

def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata,-shift)
        plotdata[-shift:] = data[:]
    lines[0][0].set_ydata(plotdata)
    return line


stream  = sd.InputStream(device = deviceID, channels = channels, samplerate = Fs, callback  = audio_callback, blocksize=blocksize)
ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
with stream:
	plt.show()