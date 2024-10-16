import queue
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import pyroomacoustics as pra

# audio device constants
deviceID = 20
Fs = 44100
channels = 8

# plotting animation constants
interval = 30

# array processing constants
num_source = 7
array_loc = [0, 0]
nfft = 1024
flow = 300
fhigh =1000
blocksize = 1200
block_number = 0
init_blocks = 10
eig_thresh = 100000
angle_jump_thresh = 15
smoothing_factor = 0.9
scale_factor = 1.7
n_sub = 5
sep_sub = 0.24
bf_plot_freq = 700

# initialise empty arrays and algorithms
ks = np.zeros(shape=(channels, init_blocks))
candidate_azs = np.linspace(0, 180, 181)

freq_range = [flow,fhigh]
freq_range = [int(np.round(f / Fs * nfft)) for f in freq_range] 
freq_bins = np.arange(freq_range[0], freq_range[1], dtype=np.int64)

mic_positions = np.array([[0.48,0.24,0.16,0.08,0,-0.08,-0.24,-0.48],[0]*channels])
subarray_positions = pra.linear_2D_array(center=array_loc, M=n_sub, phi=0, d=sep_sub)
beamformer = pra.Beamformer(subarray_positions, Fs, nfft)
music = pra.doa.normmusic.NormMUSIC(mic_positions, Fs, nfft,num_src=num_source,azimuth = candidate_azs*np.pi/180,mode='near')
music.freq_bins = freq_bins
q = queue.Queue()

grid_plotdata = np.zeros(len(candidate_azs))
az_plotdata = np.zeros(num_source,)
beam_plotdata = np.zeros([180,2])
previous_az = np.zeros(num_source)

# make fig and axis of matplotlib plt
fig, hiddenax = plt.subplots(figsize = (18,8))
hiddenax.axis('off')

gs = fig.add_gridspec(2,2,left=0.05,right=0.95,wspace=0.1,hspace=0.1,height_ratios=(2,1),)
ax1 = fig.add_subplot(gs[0,0],projection = 'polar')
ax2 = fig.add_subplot(gs[1,:])
ax3 = fig.add_subplot(gs[0,1],projection='polar')
ax = [ax1,ax2,ax3]

# plot formatting
ax[0].set_title("Estimated DOA")
ax[0].grid(True)
ax[0].set_ylim(0, 1)
ax[0].set_xlim(0, np.pi)
ax[0].xaxis.set_label_coords(0.9,1)
ax[0].set_yticks([])
ax[0].set_theta_direction(-1)
ax[0].set_theta_offset(np.pi)
ax[0].set_clip_on(False)

ax[1].set_title("Subspace spectrum")
ax[1].set_ylim(0,1)

ax[2].set_title('Array Beam Pattern')
ax[2].set_xlim(0, np.pi)
ax[2].set_ylim(0,1)
ax[2].set_theta_direction(-1)
ax[2].set_theta_offset(np.pi)
ax[2].set_yticks([])

lines = []
for i in range(num_source):
	lines.append(ax[0].plot(az_plotdata[i]))

lines.append(ax[1].plot(grid_plotdata))
for i in range(2):
    lines.append(ax[2].plot(np.arange(0,180,1)*np.pi/180,beam_plotdata[:,i]))

# use an audio call back function to process data
def audio_callback(indata,frames,time,status):
	data_array = np.array(indata.T)

	global block_number, ks, previous_az

	# normalize data
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

	# STFT and determine no. of sources
	X = pra.transform.stft.analysis(data_array.T, nfft, nfft//2).T
	C_hat = music._compute_correlation_matricesvec(X)
	Es,En,ws,wn = music._subspace_decomposition(C_hat[None,...])
	ws = np.squeeze(ws,axis=0)
	wn = np.squeeze(wn,axis=0)
	w = np.concatenate([wn,ws],axis=1)
	
	w_mean = np.mean(abs(w), axis=0)

	count_src = 0
	for i in range(len(w_mean)):
		if w_mean[i] > eig_thresh:
			count_src += 1
	music.num_src = count_src

	# matching game to assign azimuths closest to their last known value
	az_vector = np.zeros(num_source)
	grid_vector = np.zeros(candidate_azs.shape)
	response_data = np.zeros([180, 2])
	if music.num_src > 0:
		music.locate_sources(X,freq_bins=freq_bins)
		az = (music.azimuth_recon*180/np.pi - 90) * scale_factor + 90
		az.sort()
		
		distances = 360*np.ones((len(previous_az),len(az)))
		for i in range(len(az)):
			for j in range(len(previous_az)):
				distances[j,i] = abs(az[i] - previous_az[j])
		
		
		for i in range(len(az)):
			prev_i,curr_i = np.argmin(distances)//distances.shape[1],distances.argmin()%distances.shape[1]
			distances[:,curr_i] = 360*np.ones((len(previous_az)))
			distances[prev_i,:] = 360*np.ones((1,len(az)))
			
			if previous_az[prev_i] == 0:
				# don't filter if new source
				az_vector[prev_i] = az[curr_i]
			elif abs(previous_az[prev_i] - az[curr_i]) > angle_jump_thresh:
				# reject sudden large angle jumps
				az_vector[prev_i] = previous_az[prev_i]
			else:
				# filter for smoother plot
				az_vector[prev_i] = smoothing_factor*previous_az[prev_i] + (1 - smoothing_factor)*az[curr_i]
		
		grid_vector = music.grid.values
		
        # generate beam patterns for a given azimuth
		if count_src > 2:
			count_src = 2
		detected_azs = az_vector[:count_src]
		
		source_locs = np.zeros(shape=(2,len(detected_azs)))
		source_locs[0,:] = np.cos(detected_azs*np.pi/180)
		source_locs[1,:] = np.sin(detected_azs*np.pi/180)
		
		for i in range(len(detected_azs)):
			current_interf = source_locs
			current_interf = np.delete(current_interf, i, 1)
			interf = pra.soundsource.SoundSource([0,0])
			interf.images = current_interf
			source = pra.soundsource.SoundSource([0,0])
			source.images = np.array([source_locs[0, i], source_locs[1, i]])# beamformer pattern at first azimuth
			
			beamformer.frequencies = np.array([bf_plot_freq])
			beamformer.rake_max_sinr_weights(
				source = source,
				interferer = interf,
				R_n= 1e-6*np.identity(5)
				)
			response = beamformer.response(np.arange(0,180,1)*np.pi/180, bf_plot_freq)
			response_data[:,i] = np.abs(response[1])
			
	previous_az = az_vector
	return_data = [az_vector, grid_vector,response_data]
	q.put(return_data)
	
# take frame of audio samples from the queue and update plot
def update_plot(frame):
	global az_plotdata, grid_plotdata,beam_plotdata
	while True:
		try: 
			data = q.get_nowait()
		except queue.Empty:
			break
		az_plotdata = data[0]
		grid_plotdata = data[1]
		beam_plotdata = data[2]
	for i in range(len(az_plotdata)):
		lines[i][0].set_ydata([0, 1])
		lines[i][0].set_xdata([0, az_plotdata[i]*np.pi/180])

	lines[num_source][0].set_xdata(candidate_azs)
	lines[num_source][0].set_ydata(grid_plotdata)
	lines[num_source+1][0].set_ydata(np.abs(beam_plotdata[:,0])/np.max(np.abs(beam_plotdata[:,0])))
	lines[num_source+2][0].set_ydata(np.abs(beam_plotdata[:,1])/np.max(np.abs(beam_plotdata[:,1])))
	hiddenax.set_title(f'LIVE ARRAY PROCESSING \n Sources detected: {music.num_src}')
	return lines

# outer_axs[1].set_yticks([])
# outer_axs[1].set_xticks([])

# create input stream to record in real time
stream  = sd.InputStream(device = deviceID, channels = channels, samplerate = Fs, callback  = audio_callback, blocksize=blocksize)
ani  = FuncAnimation(fig,update_plot, interval=interval,blit=False)
with stream:
	plt.show()