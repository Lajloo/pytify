import os
import sqlite3
from datetime import datetime
import settings
from urllib.parse import urlparse, parse_qs


class Database:
    database = None

    def __init__(self):
        os.makedirs(settings.database_path, exist_ok=True)
        self.connection = sqlite3.connect(os.path.join(settings.database_path, 'pityfy.db'))
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        table = """CREATE TABLE IF NOT EXISTS
        songs(song_url TEXT, yt_id TEXT, path TEXT, title TEXT, date TEXT)"""
        cursor.execute(table)
        self.connection.commit()

    def add_record(self, song_url, path, title):
        cursor = self.connection.cursor()
        date = datetime.now()
        yt_id = self.get_yt_id(song_url)
        cursor.execute("INSERT INTO songs VALUES (?,?,?,?,?)", (song_url, yt_id, path, title, date))
        self.connection.commit()

    def list_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM songs")
        results = cursor.fetchall()
        return results

    def get_song(self, yt_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM songs WHERE yt_id = ?", (yt_id, ))
        return cursor.fetchone()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def get_yt_id(url):
        u_pars = urlparse(url)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1]

    @staticmethod
    def get_database():
        if Database.database:
            return Database.database
        else:
            Database.database = Database()
            return Database.database

Database.get_database().get_song("kurwa")