import pytube
from moviepy.editor import *
import os
import chrome_bookmarks

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
        return (url, mp3_file, name.strip('.mp4'))
    except:
        print('[-] Something went wrong...')


def download_from_bookmarks(bookmark_name):
    url_list = []
    tuple_list = []
    for folder in chrome_bookmarks.folders:
        if folder.name == bookmark_name:
            urls_in_folder(folder, url_list)

    for u in url_list:
        tuple_list.append(download_video_as_mp3(u))
    return tuple_list

