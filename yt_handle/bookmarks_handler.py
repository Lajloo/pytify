import pytube
from moviepy.editor import *
import os
import chrome_bookmarks
import settings
import threading

def urls_in_folder(folder, url_list):
    for url in folder.urls:
        #print(url['url'], end=' ')
        #print(url['name'])
        url_list.append(url['url'])

    for child in folder.folders:
        urls_in_folder(child, url_list)

#returns list of urls from bookmarks
def get_list_of_urls(bookmark_name):
    url_list = []
    for folder in chrome_bookmarks.folders:
        if folder.name == bookmark_name:
            urls_in_folder(folder, url_list)
    return url_list

