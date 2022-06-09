import sqlite3

connection = sqlite3.connect('database/database.db')

with open('create_tables.sql') as f:
    connection.executescript(f.read())

connection.close()
