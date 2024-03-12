# Capstone Audio Plugins

Stores all shared code for plugin development.

## Usage

Clone the repository:

    git clone https://github.com/mwrogers-unimelb/Audio-Plugins-Capstone.git

In the Audio-Plugins-Capstone directory, run:

    cmake -S . -B build
    cmake --build build

This will take a while on the first run.

Currently, the gain plugin simply adjusts the volume of the track it is placed on. It does not save the state it was closed in so it will reset to a value of 0.5 upon opening.