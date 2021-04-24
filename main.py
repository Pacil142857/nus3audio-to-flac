import os
import subprocess
from pydub import AudioSegment

# Find every file in input
nus3audio_files = [file.path for file in os.scandir(r'.\input')]

# Create tmp directory to store lopus files
try:
    os.mkdir('tmp')
except FileExistsError:
    pass

# Extract lopus files from the nus3audio files in input
for file in nus3audio_files:
    
    # Get the filename and file extension
    filename = file[file.rfind('\\') + 1:]
    file_ext = file[file.rfind('.'):]
    filename = filename[:filename.rfind('.')]
    
    # Skip file if file doesn't end in nus3audio
    if file_ext != '.nus3audio':
        print(f'Skipping {filename + file_ext} since it does not end in .nus3audio')
        continue
    
    # Convert the file and store it in the tmp directory
    command = [r'.\tools\nus3audio.exe', file, '-e', r'.\tmp']
    new_filename = subprocess.run(command, stdout=subprocess.PIPE).stdout
    new_filename = new_filename.decode('utf-8')[:-1]
    
    # Rename the lopus file to the filename of the nus3audio file
    os.rename('.\\tmp\\' + new_filename, '.\\tmp\\' + filename + '.lopus')

# Convert lopus files to wav files

# Convert wav files to flac files
# Example:
# song = AudioSegment.from_wav('foo.wav')
# song.export('bar.flac', format='flac')