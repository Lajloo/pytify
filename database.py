import os
import sqlite3
from datetime import datetime
import settings

class Database:

    def __init__(self):
        self.connection = sqlite3.connect(os.join.path(settings.database_path, 'pityfy.db'))
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        table = """CREATE TABLE IF NOT EXISTS
        songs(song_url TEXT, path TEXT, title TEXT, date TEXT)"""
        cursor.execute(table)

    def add_record(self, song_url, path, title):
        cursor = self.connection.cursor()
        date = datetime.now()
        cursor.execute("INSERT INTO songs VALUES (?,?,?,?)", (song_url, path, title, date))
        self.connection.commit()

    def list_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM songs")
        results = cursor.fetchall()
        print(results)

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
