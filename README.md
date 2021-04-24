# nus3audio-to-flac

This is a simple batch converter that converts nus3audio files to flac files. It only works on Windows.

**Anything in /tmp and /output will be deleted once the program ends. Do not store any files there.**

## Usage

First, edit the settings in config.txt to your liking. NUM_LOOPS is the number of loops the song will do through (decimals are valid), and FADE_DURATION is the amount of time in seconds that it will fade out near the end. If the song loops, this time will be added onto the song.

After that, simply run the program using a version of Python greater than or equal to 3.6 and the files will be converted.
