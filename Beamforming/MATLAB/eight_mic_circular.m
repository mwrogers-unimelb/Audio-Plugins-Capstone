%% 8 Microphone Semicircular Beamforming Design
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

%% Vary radius of Semicircular microphone array

% create semicircular arrays of varying radius
rads = [0.3 0.4 0.5 0.6 0.7];
ang_range = 70; % range of angle, deg
azang = linspace(-ang_range, ang_range, N_mics);

for i = 1:length(rads)
    array = phased.ConformalArray(...
    'ElementPosition',[rads(i)*cosd(azang);rads(i)*sind(azang);zeros(1,N_mics)],...
    'ElementNormal',[azang;zeros(1,N_mics)],...
    'Element', microphone);

    % plot directivity over frequency range
    freq = [100 500 1000 5000]; % simulation frequencies

    figure
    fig_title = ['Array Directivity for Varying Frequencies, Radius of ', num2str(rads(i))];

    sgtitle(fig_title)
    for j = 1:length(freq)

        subplot(2, 2, j)
        pattern(array,freq(j),[-180:180],0,'PropagationSpeed',v_sound,...
            'CoordinateSystem','polar','Type','directivity');
        legend(string(freq(j)))
    end
end

%% Vary Source Position

% azimuth angles to test
r = 0.6; % radius selected from above
f = 1000; % test frequency (can change)
lambda = v_sound/f; % corresponding wavelength
azim = linspace(-30, 30, 4);

figure
sgtitle('Array Directivity for Varying Azimuth')
for i = 1:length(azim)
    array = phased.ConformalArray(...
    'ElementPosition',[r*cosd(azang);r*sind(azang);zeros(1,N_mics)],...
    'ElementNormal',[azang;zeros(1,N_mics)],...
    'Element', microphone);

    % plot directivity
    subplot(2, 2, i)
    w = steervec(getElementPosition(array)/lambda,[azim(i);0]);
    pattern(array,f,[-180:180],0,'PropagationSpeed',v_sound,...
        'CoordinateSystem','polar','Type','directivity', 'weights', w);
end