import queue
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import pyroomacoustics as pra

# constants
interval = 300
deviceID = 20
Fs = 44100
channels = 8
duration = 10
array_loc = [0, 0]
sep = 0.3
nfft = 1024
flow = 300
fhigh =1000
blocksize = 12000
length  = blocksize*10
block_number = 0
init_blocks = 10
ks = np.zeros(shape=(channels, init_blocks))

R = pra.linear_2D_array(center=array_loc, M=channels, phi=0, d=sep)
music = pra.doa.normmusic.NormMUSIC(R, Fs, nfft,num_src=1,azimuth = np.linspace(0, 180, 181)*np.pi/180,mode='near')
q = queue.Queue()

print(sd.query_devices(deviceID, 'input'))

audio_plotdata = np.zeros(shape=(length, channels))
az_plotdata = np.zeros(1)

# make fig and axis of matplotlib plt
fig = plt.figure(figsize = (18,8))
gs = fig.add_gridspec(1,2,wspace=0.1,hspace=0.1,)
ax1 = fig.add_subplot(gs[0,0],projection = 'polar')
gsinner = gs[0,1].subgridspec(8,1,wspace=0.1,hspace=0.1,)
# outer_axs = gs.subplots()
print(ax1)
ax = [ax1]
ax += list(gsinner.subplots())

# fig,ax = plt.subplots(9, figsize=(8,4))
ax[0].set_title("Estimated DOA")
ax[1].set_title("Channel Audio")

# R,G,B = 0,1,0.29 = green
colours = ['r', 'g', 'b', 'm', 'c', 'y', 'k', '0.8']
lines = []
lines.append(ax[0].plot(az_plotdata))
for i in range(channels):
	lines.append(ax[i+1].plot(audio_plotdata[:,i], colours[i]))
	

# use an audio call back function to process data
def audio_callback(indata,frames,time,status):
	data_array = np.array(indata.T)

	global block_number
	global ks
	if block_number < init_blocks:
		ks[:, block_number] = np.array(
			[
				1/np.sqrt(np.var(data_array[i, :]))
				for i in range(channels)
			]
		)
		block_number += 1
	elif block_number == init_blocks:
		ks = np.mean(ks, axis=1)
		block_number += 1
	else:
		data_array = np.array(
			[
				ks[i]*data_array[i,:]
				for i in range(channels)
			]
		)
    
    # data_array = np.array([np.divide(channel,np.sqrt(np.var(channel))) for channel in data_array])
	X = pra.transform.stft.analysis(data_array.T, nfft, nfft//2).T
	music.locate_sources(X,freq_range = [flow,fhigh])
	az = music.azimuth_recon*180/np.pi
	return_data = [az, data_array.T]
	q.put(return_data)

	
# take frame of audio samples from the queue and update plot
def update_plot(frame):
	global az_plotdata, audio_plotdata
	while True:
		try: 
			data = q.get_nowait()
		except queue.Empty:
			break
		audio_shift = len(data[1])
		az_shift = len(data[0])
		audio_plotdata = np.roll(audio_plotdata, -audio_shift,axis = 0)
		az_plotdata = np.roll(az_plotdata, -az_shift,axis = 0)
		# shift data back to make space for incoming data
		audio_plotdata[-audio_shift:] = data[1]
		az_plotdata[-az_shift:] = data[0]
	lines[0][0].set_ydata([0, 1])
	lines[0][0].set_xdata([0, az_plotdata[0]*np.pi/180])
	for column, line in enumerate(lines[1:]):
		line[0].set_ydata(audio_plotdata[:,column])
	return lines

# plot formatting
ax[0].grid(True)
ax[0].set_ylim(0, 1)
ax[0].set_xlim(0, np.pi)
ax[0].set_ylabel('Angle (Degrees)')
ax[0].set_yticks([])


for i in range(channels):
	ax[i+1].set_yticks([])
	ax[i+1].set_xticks([])
	ax[i+1].set_ylim(-20, 20)

# outer_axs[1].set_yticks([])
# outer_axs[1].set_xticks([])

# create input stream to record in real time
stream  = sd.InputStream(device = deviceID, channels = channels, samplerate = Fs, callback  = audio_callback, blocksize=blocksize)
ani  = FuncAnimation(fig,update_plot, interval=interval,blit=False)
with stream:
	plt.show()