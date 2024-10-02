%% 16 Microphone Linear Beamforming Design
% Simulates beam patterns for the 16-mic array, based on a simple fixed,
% narrowband beamforming design
clear

% Constants
hhr = [20 20e3];
N_mics = 16; % number of selected microphones
v_sound = 343; % sound speed through air, m/s

% create basic omnidirectional microphone pattern for simulation
microphone = phased.OmnidirectionalMicrophoneElement('FrequencyRange', hhr, 'BackBaffled', true);

%% Microphone spacing design selection: 
% currently set so that beamformer performs best at middle frequency of human hearing range

hhr_vec = logspace(log10(hhr(1)), log10(hhr(2)), 3); % human hearing range, hz, with mid point
mid_freq = hhr_vec(2); % logarithmic middle of wideband frequency range
mid_lambda = v_sound/mid_freq;

opt_h = 0.5 * mid_lambda; % from tager paper, need: 0.25 < d/lambda < 0.5
opt_l = 0.25 * mid_lambda;

lin_mid = (opt_l + opt_h)/2 % based on this result, choose spacing 20cm

%% Vary Source Frequency

spacing = 0.2; % from above design step

array = phased.ULA(N_mics, spacing, 'Element', microphone);

% plot directivity over frequency range
freq = logspace(log10(hhr(1)), log10(hhr(2)), 20); % simulation frequencies

figure
fig_title = ['Array Directivity for Varying Frequencies, Separation of ', num2str(spacing)];

sgtitle(fig_title)
pattern(array,freq,[-180:180],0,'PropagationSpeed',v_sound,...
    'CoordinateSystem','rectangular','PlotStyle','waterfall','Type','directivity');
set(gca,'YScale','log')

%% Vary Source Position

f = mid_freq; % test frequency (set as optimal design freq - can change)
lambda = v_sound/f; % corresponding wavelength
azim = linspace(-60, 60, 4); % azimuth angles to test

figure
sgtitle('Array Directivity for Varying Azimuth')
for i = 1:length(azim)
    array = phased.ULA(N_mics, spacing, 'Element', microphone);

    % plot directivity
    subplot(2, 2, i)
    w = steervec(getElementPosition(array)/lambda,[azim(i);0]);
    pattern(array,f,[-180:180],0,'PropagationSpeed',v_sound,...
        'CoordinateSystem','polar','Type','directivity', 'weights', w);
end