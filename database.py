import sqlite3
from datetime import datetime



connection = sqlite3.connect('pityfy.db')

cursor = connection.cursor()

table = """CREATE TABLE IF NOT EXISTS
songs(song_url TEXT, path TEXT, title TEXT, date DATE)"""

cursor.execute(table)
now = datetime.now()
cursor.execute("INSERT INTO songs VALUES ('test1', 'test2')")
cursor.execute("INSERT INTO songs VALUES ('test4', 'test5')")

# cursor.execute("SELECT * FROM songs")
# results = cursor.fetchall()
# print(results)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

connection.row_factory = dict_factory
cur = connection.cursor()
cur.execute("SELECT * FROM songs")
print(cur.fetchall())