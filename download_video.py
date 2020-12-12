import pytube
from moviepy.editor import *
import os

url = 'https://www.youtube.com/watch?v=Cpdw4mVSJdc'

def download_video(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams.filter(only_audio=True).first()
    try:
        video.download()
        print('[+] Downloaded!')
    except:
        print('[-] Something went wrong...')
