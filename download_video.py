import pytube
from moviepy.editor import *
import os

url = 'https://www.youtube.com/watch?v=Cpdw4mVSJdc'

def download_video(url):
    youtube = pytube.YouTube(url)
    name = youtube.streams[0].default_filename
    cwd = os.getcwd()
    file_path_name = cwd + '/' + name
    print(file_path_name)
    video = youtube.streams.filter(only_audio=True).first()
    print(name)
    try:
        video.download()
        
        print('[+] Downloaded!')

    except:
        print('[-] Something went wrong...')
    
def download_video_as_mp3(url):
    youtube = pytube.YouTube(url)

    name = youtube.streams[0].default_filename
    cwd = os.getcwd()

    file_path_name = cwd + '/' + name
    mp3_file = file_path_name.strip('.mp4') + '.mp3'

    video = youtube.streams.filter(only_audio=True).first()
    try:
        video.download()
        clip = AudioFileClip(name)
        clip.write_audiofile(mp3_file)
        clip.close()
        os.remove(file_path_name)
        print('[+] Downloaded!')
    except:
        print('[-] Something went wrong...')

