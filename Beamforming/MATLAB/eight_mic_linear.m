%% 8 Microphone Linear Beamforming Design
% Simulates beam patterns for the 8-mic array, based on a simple fixed,
% narrowband beamforming design
clear

% Constants
hhr = [20 20e3]; % human hearing range, hz
N_mics = 8; % number of selected microphones
v_sound = 343; % sound speed through air, m/s

% create basic cardioid microphone pattern for simulation
microphone = phased.CustomMicrophoneElement(FrequencyVector=hhr, ...
    PolarPatternFrequencies=[500 1000]);
microphone.PolarPattern = mag2db([...
    0.5+0.5*cosd(microphone.PolarPatternAngles);...
    0.6+0.4*cosd(microphone.PolarPatternAngles)]);

%% Vary Source Frequency and Microphone Separation

% create linear arrays of varying spacing
spacing = [0.1 0.2 0.3 0.4 0.5];

for i = 1:length(spacing)
    array = phased.ULA(N_mics, spacing(i), 'Element', microphone);

    % plot directivity over frequency range
    freq = linspace(hhr(1), hhr(2), 5); % simulation frequencies

    figure
    fig_title = ['Array Directivity for Varying Frequencies, Separation of ', num2str(spacing(i))];

    sgtitle(fig_title)
    for j = 1:length(freq)

        % subplot(2, 2, j)
        pattern(array,freq,[-180:180],0,'PropagationSpeed',v_sound,...
            'CoordinateSystem','rectangular','PlotStyle','waterfall','Type','directivity');
        legend(string(freq(j)))
    end
end

%% Vary Source Position

% azimuth angles to test
s = 0.25; % spacing from design
f = 1000; % test frequency (can change)
lambda = v_sound/f; % corresponding wavelength
azim = linspace(-60, 60, 4);

figure
sgtitle('Array Directivity for Varying Azimuth')
for i = 1:length(azim)
    array = phased.ULA(N_mics, s, 'Element', microphone);

    % plot directivity
    subplot(2, 2, i)
    w = steervec(getElementPosition(array)/lambda,[azim(i);0]);
    pattern(array,f,[-180:180],0,'PropagationSpeed',v_sound,...
        'CoordinateSystem','polar','Type','directivity', 'weights', w);
end