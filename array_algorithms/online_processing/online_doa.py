import sounddevice as sd
import numpy as np
from scipy.signal import correlate
import matplotlib.pyplot as plt
import pyroomacoustics as pra

deviceID = 20
Fs = 48000
channels = 8
duration = 10
array_loc = [0, 0]
sep = 0.3
R = pra.linear_2D_array(center=array_loc, M=channels, phi=0, d=sep)
nfft = 1024
flow =20
fhigh =20000
music = pra.doa.normmusic.NormMUSIC(R, Fs, nfft,num_src=1,azimuth = np.linspace(0, 180, 181)*np.pi/180,mode='near')
def callback(indata,frames,time,status):
    if status:
        print (status)

    data_array = np.array(indata)
    X = pra.transform.stft.analysis(data_array, nfft, nfft//2).T
    music.locate_sources(X,freq_range = [flow,fhigh])
    print(music.azimuth_recon*180/np.pi)
    volume = np.var(data_array)


    

audio_data = []
thetas = np.array([])
print('recording')
with sd.InputStream(samplerate=Fs,channels=channels, device=deviceID, callback=callback, blocksize=24000):
    sd.sleep(int(duration*1000))

plt.plot(180-thetas*180/np.pi)
plt.show()

# audio_array = np.concatenate(audio_data, axis=0)
# for i in range(channels):
#     sf.write('multichannel_recording_' + str(i) + '.wav', audio_array, Fs)
