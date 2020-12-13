import pytube
from moviepy.editor import *
import os
import chrome_bookmarks
import settings

url = 'https://www.youtube.com/watch?v=Cpdw4mVSJdc'
#(song_url TEXT, path TEXT, title TEXT)

def urls_in_folder(folder, url_list):
    for url in folder.urls:
        #print(url['url'], end=' ')
        #print(url['name'])
        url_list.append(url['url'])

    for child in folder.folders:
        urls_in_folder(child, url_list)
    
def download_video(url):
    youtube = pytube.YouTube(url)

    name = youtube.streams[0].default_filename
    cwd = os.getcwd()

    file_path_name = cwd + '/' + name
    mp3_file = file_path_name.strip('.mp4') + '.mp3'

    video = youtube.streams.filter(only_audio=True).first()
    try:
        video.download()
        
        print('[+] Downloaded!')

    except:
        print('[-] Something went wrong...')
    
def download_video_as_mp3(url):
    os.makedirs(settings.save_audio_path, exist_ok=True)
    youtube = pytube.YouTube(url)
    try:
        video = youtube.streams.filter(only_audio=True).first()
        video.download(output_path=settings.save_audio_path)

        default_filename = video.default_filename
        video_path = os.path.join(settings.save_audio_path, default_filename)
        clip = AudioFileClip(video_path)

        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        clip.write_audiofile(audio_path)
        clip.close()
        os.remove(video_path)
        print('[+] Downloaded!')
        return (url, audio_path, default_filename)
    except:
        print(f'[-] Something went wrong while downloading {default_filename}')


def download_from_bookmarks(bookmark_name):
    url_list = []
    tuple_list = []
    for folder in chrome_bookmarks.folders:
        if folder.name == bookmark_name:
            urls_in_folder(folder, url_list)

    for u in url_list:
        tuple_list.append(download_video_as_mp3(u))
    return tuple_list

