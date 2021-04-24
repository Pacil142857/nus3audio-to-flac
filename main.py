import os
import subprocess
from pydub import AudioSegment
from shutil import rmtree

# Find every file (recursively) in input
nus3audio_files = [os.path.join(path, file) for path, _, files in os.walk(r'.\input') for file in files]

# These lists get used later in the program
lopus_files = []
wav_files = []

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
    
    # Set default
    num_loops = '1'
    fade_duration = '10'
    
    # Get the number of loops and the fade duration
    for line in f:
        if 'NUM_LOOPS=' in line:
            num_loops = line[line.rfind('=') + 1:]
        elif 'FADE_DURATION=' in line:
            fade_duration = line[line.rfind('=') + 1:]


# Convert lopus files to wav files
for file in lopus_files:
    # Get the filename and the new file path
    filename = file[file.rfind('\\') + 1:-6]
    new_filepath = '.\\tmp\\' + filename + '.wav'
    
    # Convert the lopus file to a wav file
    command = [r'.\tools\vgmstream\test.exe', '-l', num_loops, '-f', fade_duration, '-o', new_filepath, file]
    subprocess.run(command)
    
    # Add the new file to wav_files
    wav_files.append(new_filepath)

# Convert wav files to flac files
for file in wav_files:
    # Get the filename
    filename = file[file.rfind('\\') + 1:-4]
    
    # Convert the file
    subprocess.run([r'.\tools\sox\sox.exe', file, '.\\output\\' + filename + '.flac'])

# Delete the tmp folder
rmtree('tmp')