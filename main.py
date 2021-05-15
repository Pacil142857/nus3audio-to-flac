import os
import subprocess
from configparser import ConfigParser
from mutagen import MutagenError
from mutagen.flac import FLAC, Picture
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
for file in (r'.\input\.gitkeep', r'.\output\.gitkeep'):
    if os.path.isfile(file):
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
config = ConfigParser()
config.read('config.ini')
settings = config['Settings']

# Set defaults
num_loops = 1.0
fade_duration = 10.0

# Get the data
num_loops = settings.get('Num_loops')
fade_duration = settings.get('Fade_duration')
cover_img = settings.get('Cover_image')
empty_input_dir = True if settings.get('Empty_input_folder') == 'True' else False

# Get song metadata
metadata = config['Song Metadata'].items()

# Convert lopus files to wav files
for file in lopus_files:
    # Get the filename and some other things
    filename = file.filename
    new_filepath = '.\\tmp\\' + file.rel_path + '.wav'
    path = file.path
    
    # Convert the lopus file to a wav file
    command = [r'.\tools\vgmstream\test.exe', '-l', num_loops, '-f', fade_duration, '-o', new_filepath, path]
    subprocess.run(command, stdout=subprocess.DEVNULL)
    
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
    subprocess.run([r'..\tools\sox\sox.exe', '.' + file.path, '.\\' + file.rel_path + '.flac'])
    
    # Open the audio file
    if cover_img or metadata:
        try:
            audio = FLAC(file.rel_path + '.flac')
        except (FileNotFoundError, MutagenError):
            print('Something went wrong, so the cover image and metadata won\'t be included.')
            cover_img = False
            metadata = False
            
    # Add the cover image
    if cover_img:
            
        # Create an image
        img = Picture()
        img.type = 3
        img.desc = 'front cover'
        
        # Open the image
        try:
            with open('..\\' + cover_img, 'rb') as f:
                img.data = f.read()
        except FileNotFoundError:
            print('Cover image not found, so a cover image won\'t be included.')
            cover_img = False
            img_found = False
            img.data = True # This is a little hacky, but it works fine.
        else:
            img_found = True
        
        # If the image exists, use it as the cover image.
        if img_found:
            audio.add_picture(img)
        elif not img.data:
            print('Cover image not found, so a cover image won\'t be included.')
            cover_img = False
    
    # Add the metadata
    for key, value in metadata:
        audio[key] = value
    
    # Save the audio
    if cover_img or metadata:
        audio.save()


# Delete the contents of the input folder
if empty_input_dir:
    rmtree(r'..\input')
    os.mkdir(r'..\input')

# Delete the tmp folder
rmtree(r'..\tmp')