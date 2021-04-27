# nus3audio-to-flac

This is a simple batch converter that converts nus3audio files to flac files. It only works on Windows.

**Anything in /tmp and /output will be deleted once the program ends. Do not store any files there.**

## Usage

First, edit the settings in config.ini to your liking.

* `Num_loops` is the number of loops the song will do through (decimals are valid)
* `Fade_duration` is the amount of time in seconds that it will fade out near the end.
  * If the song loops, this time will be added onto the song.
* `Cover_img` will set the cover image of the songs to the image file it's set to (e.g. `Cover_img=logo.png` will set the image to `logo.png`)
  * Make sure that the cover image file is in the same folder as the program.
  * If left empty, then there won't be a cover image.
* `Empty_input_folder`, if set to "True" (capitalization matters!), will **delete all files in /input after the program has finished**.
  * If it's set to anything else, such as "False", then all the files in /input won't be deleted.
* `Artist` will set the artist of the song to whatever it's equal to.
  * If left empty, there will be no artist for the song.

After that, simply run the program using a version of Python greater than or equal to 3.6 and the files will be converted.
