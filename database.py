import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS candidates (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    cgpa REAL,
    aptitude INTEGER,
    technical INTEGER,
    interview INTEGER

)
''')

print("Table Created Successfully")

connection.commit()

connection.close()