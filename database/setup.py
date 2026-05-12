import sqlite3
import os

def init_db():
    # Ensure database directory exists
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the candidates table per user requirements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        academic_score REAL DEFAULT 0.0,
        skills_score REAL DEFAULT 0.0,
        experience_years INTEGER DEFAULT 0,
        test_score REAL DEFAULT 0.0,
        total_score REAL DEFAULT 0.0,
        rank INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
