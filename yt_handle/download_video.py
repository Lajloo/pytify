import pytube
import queue
import settings
import threading
from browsers.chrome import bookmarks_handler
from database.database import Database
from moviepy.editor import *


class DownloadWorker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url = self.queue.get()
            try:
                download_video_if_not_exist(url)
            finally:
                self.queue.task_done()


#url = 'https://www.youtube.com/watch?v=Cpdw4mVSJdc'
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
    print(youtube.streams.filter(progressive=True).all())

    name = youtube.streams[0].default_filename
    cwd = os.getcwd()

    file_path_name = cwd + '/' + name
    mp3_file = file_path_name.strip('.mp4') + '.mp3'

    #video = youtube.streams.filter(only_audio=True).first()
    video = youtube.streams.filter(res='720p').first()

    try:
        video.download()
        print('[+] Downloaded!')
    except:
        print('[-] Something went wrong...')
    
def download_video_as_mp3(url):
    os.makedirs(settings.save_audio_path, exist_ok=True)
    youtube = pytube.YouTube(url)
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
    filename = os.path.splitext(default_filename)[0]
    #add database
    database = Database.get_database()
    database.add_record_thread_safe(url, audio_path, filename)


def download_from_bookmarks(bookmark_name, n_of_threads=1):
    urls = bookmarks_handler.get_list_of_urls(bookmark_name)
    # download_with_threads(urls, use_threads)
    que = queue.Queue()
    for x in range(n_of_threads):
        worker = DownloadWorker(que)
        worker.daemon = True
        worker.start()
    for u in urls:
        que.put(u)
    que.join()


def download_with_threads(video_links, use_threads=False):
    tuple_list = []
    if use_threads:
        que = queue.Queue()
        threads = []
        for video in video_links:
            t = threading.Thread(target=download_video_if_not_exist, args=(video, ))
            threads.append(t)
            t.start()
    else:
        for video in video_links:
            tuple_list.append(download_video_if_not_exist(video))

def download_video_if_not_exist(url):
    #check if url exists in database
    database = Database.get_database()
    if not database.check_if_exist(url):
        download_video_as_mp3(url)
    else:
        print('[*] Url already exists in database.')


# use __name__ == '__main__' to prevent unintended running
if __name__ == '__main__':
    download_from_bookmarks('muzaaaaa', 3)
