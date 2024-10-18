# Capstone Audio Plugins

Stores all code for the project: Designing Audio Effect Plugins, which investigated the application of acoustic phased arrays to live performance settings.


## Usage

Clone the repository:

    git clone https://github.com/mwrogers-unimelb/Audio-Plugins-Capstone.git

Python dependencies:

    pyroomacoustics
    matplotlib
    numpy
    scipy
    playsound
    jupyter

MATLAB code should be able to run, as long as the phased array toolbox is installed.


## Description

Each sub-directory contains code to perform the functions as described below.

### array_algorithms

Parent python code foler. Currently contains design simulations of a variety of scenarios, as well as physical tests of algorithms on real-world samples (not included in the repo), and online processing.

#### basic_algorithms

A basic introduction and application of beamforming and DOA algorithms used in the project.

#### design_sims

A variety of simulations to select array parameters (algorithm, geometry, location, etc.).

#### input_samples

input sound files for array simulations (vocal sounds).

#### output_samples

processed output sound files from simulation and hardware tests.

#### array_samples

recordings from the hardware array, for offline processing.

#### physical_tests

implementations of algorithms to be run on hardware, offline.

#### online_processing

algorithms designed to process audio online (in real-time) for the built hardware array.
