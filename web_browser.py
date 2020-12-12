from bottle import route, run, template, view, static_file, request, post
import os
import re
import csv
import json
import settings
from database import Database

database = Database()
database.add_record("asdasdS", "asdasdagrgr", "ffgdgfds")

@route('/favicon.ico', method='GET')
def get_favicon():
    """
    Browsers for no reason keep asking for favicon, so there you go.
    :return: favicon
    """
    return static_file('favicon.ico', root='./static_files')


@route('/')
@view('templates/index')
def index():
    """
    Returns main page of the server.
    :return:
    """
    return template('templates/index.html', title="What a PiTyfy!",
                    songs=database.list_all())


if __name__ == "__main__":
    run(host='localhost', port=8080)