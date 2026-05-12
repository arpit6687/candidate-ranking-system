import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE candidates ADD COLUMN ml_score REAL DEFAULT 0.0")
        print("Successfully added ml_score column!")
    except sqlite3.OperationalError as e:
        print("Column may already exist or error:", e)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
