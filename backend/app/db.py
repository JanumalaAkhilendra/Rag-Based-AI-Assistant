import sqlite3
import os

def get_db_connection():
    db_path = os.getenv('DB_PATH', 'assistant.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS data_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                text TEXT,
                meta TEXT,
                role TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                role TEXT
            )
        ''')
    conn.close()
