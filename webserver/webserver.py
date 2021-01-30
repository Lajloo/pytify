import settings
from database.database import Database
from yt_handle.download_video import download_video_if_not_exist
from yt_handle.download_video import download_from_bookmarks
from bottle import *


@route('/favicon.ico', method='GET')
def get_favicon():
    """
    Browsers for no reason keep asking for favicon, so there you go.
    :return: favicon.ico
    """
    return static_file('favicon.ico',
                       root='staticfiles')


@route('/')
@view('index')
def index(bookmark_success=None):
    """
    Returns main page of the server.
    :return:
    """


    database = Database.get_database()
    return template('index.html',
                    title="What a PiTify!",
                    songs=database.list_all(),
                    bookmark_success=bookmark_success)


@route('/download/<yt_id>')
def download_song(yt_id):
    database = Database.get_database()
    song = database.get_song(yt_id)
    return static_file(os.path.basename(song['path']),
                       root=settings.save_audio_path,
                       mimetype="audio/mpeg",
                       download=song['title']+".mp3")
    # / download / {{song['yt_id']}}
    # database = Database.get_database()
    # song = database.get_song(yt_id)



@route('/style.css')
def send_style():
    """
    Sends style.css.
    :return: style.css
    """
    return static_file('style.css', root='staticfiles')


@post('/add')
@view('index')
def add_song():
    song_url = request.forms.song_url
    download_video_if_not_exist(song_url)
    return index()

@post('/bookmark_download')
@view('index')
def bookmark_download():
    status = download_from_bookmarks(request.forms.bookmark_path)
    return index(status)



def run_webserver(host='localhost', port=8080):
    os.chdir('./webserver')
    run(host=host, port=port)


if __name__ == "__main__":
    run(host='localhost', port=8080)
