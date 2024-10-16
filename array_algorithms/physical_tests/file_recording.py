import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import numpy as np

deviceID = 20
channels = 8
duration = 10
fs = 44100

stream  = sd.InputStream(device = deviceID, channels = channels, samplerate = Fs, callback  = audio_callback, blocksize=blocksize)

sd.rec(duration*fs,)

audio_array = np.concatenate(audio_data, axis=0)
for i in range(channels):
    sf.write('multichannel_recording_' + str(i) + '.wav', audio_array, Fs)