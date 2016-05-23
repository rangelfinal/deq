import sqlite3

db= sqlite3.connect('DEQ.sqlite')
cursor = db.cursor()
cursor.execute('CREATE TABLE arduino(name text, value real, time integer)')
cursor.execute('CREATE TABLE interface(name text, value real)')
cursor.execute('CREATE TABLE python(name text, value real)')
db.commit()
