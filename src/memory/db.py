import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "memory.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            report TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            title TEXT,
            url TEXT,
            source TEXT,
            FOREIGN KEY (session_id) REFERENCES research_sessions(id)
        )
    """)
    conn.commit()
    conn.close()