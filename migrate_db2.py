import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

def migrate_admins():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Admins table created successfully!")

if __name__ == '__main__':
    migrate_admins()
