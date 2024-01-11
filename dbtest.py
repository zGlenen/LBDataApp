import sqlite3

conn = sqlite3.connect('database/FilmDataDB.db')
cursor = conn.cursor()

cursor.execute("INSERT INTO film VALUES (1,'zackmovie',2019,'zackglenen')")
conn.commit()
conn.close()