%% Delay and sum beamformer algorithm implementation
% uses MATLAB's built-in beamformer for now
clear

% Constants
hhr = [20 20e3];
N_mics = 8; % number of selected microphones
v_sound = 343; % sound speed through air, m/s

% create basic cardioid microphone pattern for simulation
microphone = phased.CustomMicrophoneElement(FrequencyVector=hhr, ...
    PolarPatternFrequencies=[500 1000]);
microphone.PolarPattern = mag2db([...
    0.5+0.5*cosd(microphone.PolarPatternAngles);...
    0.6+0.4*cosd(microphone.PolarPatternAngles)]);

%% Read input audio from file
% taken from pyroomacoustics room simulation

input = [];

for i = 1:N_mics
    [x, fs] = audioread("../pyroomacoustics/output_samples/singing_8000_mic_" + int2str(i-1) + ".wav");
    input = [input x];
end

%% Build beamformer and process signal

% Design parameters
spacing = 0.2;

array = phased.ULA(N_mics, spacing, 'Element', microphone);

az = 0;
el = 0;
direction = [az; el]; % DOA info - hard coded for now

beamformer = phased.SubbandPhaseShiftBeamformer('SensorArray',array,...
    'SampleRate',fs,'PropagationSpeed',v_sound,...
    'NumSubbands',64,'OperatingFrequency',4001,...
    'Direction',direction,'DirectionSource','Property',...
    'WeightsOutputPort',true,'SubbandsOutputPort',true);
[output, weights, subbands] = step(beamformer, input); % process signal

%% Save signal to file
% stored in subdirectory "processed_samples"

audiowrite('processed_samples/singing_8000_processed.wav', output, fs);