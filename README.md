# Capstone Audio Plugins

Stores all shared code for development of beamforming and DOA algorithms, and other plugin development.


## Usage

Clone the repository:

    git clone https://github.com/mwrogers-unimelb/Audio-Plugins-Capstone.git

Python dependencies:

    pyroomacoustics
    matplotlib
    numpy
    scipy
    playsound

MATLAB code should be able to run, as long as the phased array toolbox is installed.


### array_algorithms

Currently contains design simulations of a variety of scenarios, as well as physical tests of algorithms on real-world samples (not included in the repo). This includes:

#### design_sims

A variety of simulations to select array parameters (algorithm, geometry, location, etc.).

#### input_samples

input sound files for some code sections.

#### output_samples

processed output sound files for some code sections.

#### physical_tests

implementations of algorithms to be run on hardware.
