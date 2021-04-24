import os
import subprocess
from pydub import AudioSegment
from shutil import rmtree

# Delete tmp directory
if os.path.exists(r'.\tmp') and os.path.isdir(r'.\tmp'):
    rmtree(r'.\tmp')

# Empty output directory
if os.path.exists(r'.\output') and os.path.isdir(r'.\output'):
    rmtree(r'.\output')
os.mkdir('output')

class File:
    '''Represents a file. Contains the path, filename, and file extension.'''
    def __init__(self, path):
        self.path = path
        
        # Get filename and extension
        self.filename = path[path.rfind('\\') + 1:]
        self.file_ext = self.filename[self.filename.rfind('.'):]
        self.filename = self.filename[:self.filename.rfind('.')]
        
        # Get the path, sans the first two directories (usually ".\input\" or ".\tmp\")
        # This also doesn't include the file extension, unlike self.path
        self.rel_path = '\\'.join(path.split('\\')[2:])
        self.rel_path = self.rel_path[:self.rel_path.rfind('.')]

# Find every file (recursively) in input
nus3audio_files = [File(os.path.join(path, file)) for path, _, files in os.walk(r'.\input') for file in files]

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
    
    # Get the filename, extension, and path
    filename = file.filename
    file_ext = file.file_ext
    path = file.path
    parents = file.rel_path[:-1 * len(filename)]
    
    # Skip file if file doesn't end in nus3audio
    if file_ext != '.nus3audio':
        print(f'Skipping {filename + file_ext} since it does not end in .nus3audio')
        continue
    
    # Convert the file and store it in the tmp directory
    command = [r'.\tools\nus3audio.exe', path, '-e', '.\\tmp\\' + parents]
    old_filename = subprocess.run(command, stdout=subprocess.PIPE).stdout
    old_filename = old_filename.decode('utf-8')[:-1]
    
    new_filepath = '.\\tmp\\' + file.rel_path + '.lopus'
    
    # Rename the lopus file to the filename of the nus3audio file
    try:
        os.rename('.\\tmp\\' + parents + old_filename, new_filepath)
    except FileExistsError:
        os.remove(new_filepath)
        os.rename('.\\tmp\\' + old_filename, new_filepath)
        
    lopus_files.append(File(new_filepath))

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
    # Get the filename and some other things
    filename = file.filename
    new_filepath = '.\\tmp\\' + file.rel_path + '.wav'
    path = file.path
    
    # Convert the lopus file to a wav file
    command = [r'.\tools\vgmstream\test.exe', '-l', num_loops, '-f', fade_duration, '-o', new_filepath, path]
    subprocess.run(command)
    
    # Add the new file to wav_files
    wav_files.append(File(new_filepath))

os.chdir(r'.\output')
# Convert wav files to flac files
for file in wav_files:
    # Create folders (if needed)
    folders = file.rel_path[:-1 * len(file.filename)]
    if folders:
        try:
            os.makedirs(folders)
        except FileExistsError:
            pass
    # Convert the file
    subprocess.run([r'..\tools\sox\sox.exe', '.' + file.path, '..\\output\\' + file.rel_path + '.flac'])

# Delete the tmp folder
rmtree('..\\tmp')