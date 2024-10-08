import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import correlate
import matplotlib.pyplot as plt

deviceID = 8
Fs = 48000
channels = 8
duration = 10

def callback(indata,frames,time,status):
    if status:
        print (status)

    data_array = np.array(indata)

    z = correlate(data_array[:,3],data_array[:,4])
    packagesize = data_array.shape[0]
    d = 0.3
    
    zvalid = z[packagesize-40:packagesize+40]
    taurange = 1/Fs*np.arange(-packagesize+1,packagesize)
    tauvalid = taurange[packagesize-40:packagesize+40]
    thetavalid = np.arccos(343*tauvalid/d)
    theta = thetavalid[np.argmax(zvalid)]
    np.append(thetas, theta)
    print(180-theta*180/np.pi)
    audio_data.append(indata.copy())

audio_data = []
thetas = np.array([])
print('recording')
with sd.InputStream(samplerate=Fs,channels=channels, device=deviceID, callback=callback):
    sd.sleep(int(duration*1000))

plt.plot(180-thetas*180/np.pi)
plt.show()

audio_array = np.concatenate(audio_data, axis=0)

for i in range(channels):
    sf.write('multichannel_recording_' + str(i) + '.wav', audio_array, Fs)
