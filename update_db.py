import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''
ALTER TABLE candidates
ADD COLUMN final_score REAL
''')

connection.commit()

connection.close()

print("Final Score Column Added")