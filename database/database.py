import os
import sqlite3
from datetime import datetime
import settings
from urllib.parse import urlparse, parse_qs


class Database:
    """
    Singleton-driven database management class.
    """

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
        """
        Add record to database.

        :param song_url: YouTube url.
        :param path: Path where song will be saved.
        :param title: Song title.
        """
        cursor = self.connection.cursor()
        date = Database.get_current_date()
        yt_id = self.get_yt_id(song_url)
        cursor.execute("INSERT INTO songs VALUES (?,?,?,?,?)", (song_url, yt_id, path, title, date))
        self.connection.commit()

    def add_record_thread_safe(self, song_url, path, title):
        """
        Add record to database safe for threads.

        :param song_url: YouTube url.
        :param path: Path where song will be saved.
        :param title: Song title.
        """
        connection = sqlite3.connect(os.path.join(settings.database_path, 'pityfy.db'))
        cursor = connection.cursor()
        date = Database.get_current_date()
        yt_id = self.get_yt_id(song_url)
        cursor.execute("INSERT INTO songs VALUES (?,?,?,?,?)", (song_url, yt_id, path, title, date))
        connection.commit()

    def list_all(self):
        """
        Select all records from database.

        :return: List of all songs.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM songs")
        results = cursor.fetchall()
        return results

    def get_song(self, yt_id):
        """
        Get song by id from database.

        :param yt_id: YouTube link id.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM songs WHERE yt_id = ?", (yt_id,))
        return cursor.fetchone()

    def check_if_exist(self, url):
        """
        Checking if song exists in database.

        :param url: YouTube link id.
        :return: Information if song exists in database.
        """
        yt_id = self.get_yt_id(url)
        connection = sqlite3.connect(os.path.join(settings.database_path, 'pityfy.db'))
        cursor = connection.cursor()
        return cursor.execute("SELECT * FROM songs WHERE yt_id = ?", (yt_id,)).fetchone()

    @staticmethod
    def dict_factory(cursor, row):
        """
        Creates resulting dictionary from cursors description.

        :param cursor: Iterates through database response.
        :param row: Provides index-based and case-insensitive name-based access to columns.
        :return: Dictionary
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def get_yt_id(url):
        """
        Analyze Youtube url.

        :param url: YouTube url.

        :return: YouTube video id.
        """
        u_pars = urlparse(url)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1]

    @staticmethod
    def get_database():
        """
        Database - Singleton getter.

        :return: Database object.
        """
        if Database.database:
            return Database.database
        else:
            Database.database = Database()
            return Database.database

    @staticmethod
    def get_current_date():
        """
        Selecting current date.

        :return: Current date.
        """
        return datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
