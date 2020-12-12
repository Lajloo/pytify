from bottle import route, run, template, view, static_file
import os
import re
import csv
import json
import settings
# from database import Database

class Database:
    def __init__(self):
        pass

    @staticmethod
    def list_all():
        return [{'timestamp': '2020-12-12 21:37:00',
                'artist': "metallica",
                'title': 'nuffin else mutters'},
                {'timestamp': '2020-12-12 21:37:00',
                 'artist': "metallica",
                 'title': 'hardwired to self-construct'}
                ]

    @staticmethod
    def get(index):
        return {'timestamp': '2020-12-12 21:37:00',
                'artist': "metallica",
                'title': 'nuffin else mutters'}


@route('/')
@view('report_template')
def index():
    """
    Returns main page of the server.
    :return:
    """
    return template('report_template',
                    title="What a PiTyfy!",
                    songs=Database.list_all())


