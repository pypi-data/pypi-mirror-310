import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import keyboard as kb
import pyperclip as pc
import pandas as pd
import importlib
import subprocess
import platform
import requests
import PyPDF2
import base64
import time
import glob
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def is_package_installed(package_name):
    try:
        output = subprocess.check_output("dpkg -l | grep " + package_name, shell=True)
        return bool(output)
    except subprocess.CalledProcessError:
        return False

if platform.system() == "Linux":
    if not is_package_installed("libportaudio2"):
        subprocess.check_call(["sudo","apt-get", "update"])
        subprocess.check_call(["sudo","apt-get", "install", "libportaudio2"])
    else:
        pass

# try:
#     import PIL
# except ImportError:
#     subprocess.check_call(['pip', 'install', 'pillow'])
from PIL import Image

# Simple functions
def simple_bool(message, y='y', n ='n'):
    choose = input(message+" ("+y+"/"+n+"): ").lower()
    your_bool = choose in [y]
    return your_bool

# Function to check whether pyperclip works in the system
def check_copy_paste():
    try:
        pc.copy("test")
        test_text = pc.paste()
        if test_text == "test":
            return True
    except pc.PyperclipException:
        return False

def display_files_as_pd(path=os.getcwd(), ext='',  contains=''):
    file_pattern = os.path.join(path, "*." + ext) if ext else os.path.join(path, "*")
    files = glob.glob(file_pattern)
    files_name = []
    for file in files:
        file_name = os.path.basename(file)
        files_name.append(file_name)

    files_df = pd.Series(files_name)
    file = files_df[files_df.str.contains(contains)]
    return file


############## Install Requirements ###################

def check_and_install_requirements(requirements: list):
    missing_requirements = []
    for module in requirements:
        try:
            # Check if the module is already installed
            importlib.import_module(module)
        except ImportError:
            missing_requirements.append(module)
    if len(missing_requirements) == 0:
        pass
    else:
        x = simple_bool(str(missing_requirements)+" are missing.\nWould you like to install them all?")
        if x:
            for module in missing_requirements:
                subprocess.check_call(["pip", "install", module])
                print(f"{module}' was installed correctly.")
        else:
            print("Waring: missing modules")#exit()


def get_gitfile(url, flag='', dir=os.getcwd()):
    url = url.replace('blob','raw')
    response = requests.get(url)
    file_name = flag + url.rsplit('/',1)[1]
    file_path = os.path.join(dir, file_name)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully. Saved as {file_name}")
    else:
        print("Unable to download the file.")


def get_chat():
    handle = "https://github.com/johndef64/pychatgpt/blob/main/chats/"
    response = requests.get(handle)
    data = response.json()
    files = [item['name'] for item in data['payload']['tree']['items']]
    path = os.getcwd() + '/chats'
    if not os.path.exists(path):
        os.mkdir(path)

    file = files[int(input('select chat:\n'+str(pd.Series(files))))]
    url = handle + file
    get_gitfile(url, dir=os.getcwd()+'/chats')

### file manager ###

def load_file(file='', path=os.getcwd()):
    with open(os.path.join(path, file),'r', encoding='utf-8') as file:
        my_file = file.read()#ast.literal_eval(file.read())
        file.close()
    return my_file

def load_choosen_file(path=os.getcwd(), ext='', contains=''):
    files_df = display_files_as_pd(path, ext=ext, contains=contains)
    filename = str(files_df[int(input('Choose file:\n'+str(files_df)))])
    my_file = load_file(filename, path)
    return my_file

def load_multiple_files(file_list):
    loaded_files = {}
    for file_name in file_list:
        loaded_files[os.path.basename(file_name).split('.')[0]] = load_file(file=file_name)
    print('Loaded Files:', list(loaded_files.keys()))
    return loaded_files


def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

####### image functions #######

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def display_image(filename, jupyter = False, plotlib=True, dpi=200):
    if jupyter:
        image = Image.open(filename)
        display(image)
    elif plotlib:
        image = Image.open(filename)
        plt.figure(dpi=dpi)
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    else:
        image = Image.open(filename)
        image.show()


###### audio functions  #####
def play_audio(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit() # Close the file after music play ends

def audio_loop(audio_file="speech.mp3", repeat='alt' , exit='shift'):
    print('Press '+repeat+' to repeat aloud, '+exit+' to exit.')
    while True:
        if kb.is_pressed(repeat):
            play_audio(audio_file)
            #print('Press '+repeat+' to repeat aloud, '+exit+' to exit.')
        elif kb.is_pressed(exit):
            print('Chat Closed')
            break


def record_audio(duration=5, filename="recorded_audio.mp3"): # duration: in seconds
    print('start recording for',str(duration),'seconds')
    sample_rate = 44100
    channels = 2
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait() # wait until recording is finished
    print('recording ended')
    sf.write(filename, recording, sample_rate) #save audio file


def record_audio_press(filename='recorded_audio.wav',
                       channels=1,
                       rate=44100,
                       subtype='PCM_16',
                       stop= 'ctrl'):
    # start recording with the given sample rate and channels
    print("Recording... Press "+stop+" to stop")
    myrecording = sd.rec(int(rate * 10), samplerate=rate, channels=channels)
    while True:
        # If  'Key'  is pressed stop the recording and break the loop
        if kb.is_pressed(stop):
            print("Recording Stopped.")
            break

    sd.wait()  # wait until recording is finished
    sf.write(filename, myrecording, rate, subtype)


def loop_audio(start='alt', stop='ctrl',exit='shift', filename='recorded_audio.wav', printinfo=True):
    if printinfo: print("Press "+start+" to start recording, "+exit+" to exit")
    while True:
        # If 'Key' is pressed start the recording
        if kb.is_pressed(start):
            record_audio_press(filename, stop=stop)
            break
        elif kb.is_pressed(exit):
            break


def while_kb_press(start='alt',stop='ctrl'):
    while True:
        if kb.is_pressed(start):
            print("Press "+stop+" to stop")
            while True:
                if kb.is_pressed(stop):  # if key 'ctrl + c' is pressed
                    break  # finish the loop
                else:
                    print('while...')
                    time.sleep(2)
            print("Finished loop.")