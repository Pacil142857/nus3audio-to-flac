import os
import subprocess
from pydub import AudioSegment

# Find every file in input
nus3audio_files = [file.path for file in os.scandir(r'.\input')]
lopus_files = []

# Create tmp directory to store lopus files
try:
    os.mkdir('tmp')
except FileExistsError:
    pass

# Remove .gitkeep files if they exist
# TODO: Remove the "and False" part once the program is finished
for file in (r'.\input\.gitkeep', r'.\output\.gitkeep'):
    if os.path.isfile(file) and False:
        os.remove(file)

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
    old_filename = subprocess.run(command, stdout=subprocess.PIPE).stdout
    old_filename = old_filename.decode('utf-8')[:-1]
    
    new_filepath = '.\\tmp\\' + filename + '.lopus'
    
    # Rename the lopus file to the filename of the nus3audio file
    try:
        os.rename('.\\tmp\\' + old_filename, new_filepath)
    except FileExistsError:
        os.remove(new_filepath)
        os.rename('.\\tmp\\' + old_filename, new_filepath)
        
    lopus_files.append(new_filepath)

# Load settings
with open('config.txt') as f:
    settings = []
    
    for line in f:
        settings.append(line[line.rfind('=') + 1:])
        
    num_loops, fade_duration = settings

# Convert lopus files to wav files
for file in lopus_files:
    filename = file[file.rfind('\\') + 1:-6]
    new_filepath = '.\\output\\' + filename + '.wav'
    command = [r'.\tools\vgmstream\test.exe', '-l', str(num_loops), '-f', str(fade_duration), '-o', new_filepath, file]

# Convert wav files to flac files
# Example:
# song = AudioSegment.from_wav('foo.wav')
# song.export('bar.flac', format='flac')