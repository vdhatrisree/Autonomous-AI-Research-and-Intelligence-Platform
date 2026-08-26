from memory.db import get_connection

def save_session(question, report, documents):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO research_sessions (question, report) VALUES (?, ?)",
            (question, report)
        )
        session_id = cursor.lastrowid

        for doc in documents:
            cursor.execute(
                "INSERT INTO session_sources (session_id, title, url, source) VALUES (?, ?, ?, ?)",
                (session_id, doc.title, doc.url, doc.source)
            )

        conn.commit()
        conn.close()
        return session_id
    except Exception as e:
        print(f"[memory.store] Failed to save session: {e}")
        return None

def save_verified_claims(session_id, verified_claims):
    from memory.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verified_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            claim TEXT,
            source TEXT,
            score REAL,
            confidence TEXT,
            FOREIGN KEY (session_id) REFERENCES research_sessions(id)
        )
    """)
    for v in verified_claims:
        cursor.execute(
            "INSERT INTO verified_claims (session_id, claim, source, score, confidence) VALUES (?, ?, ?, ?, ?)",
            (session_id, v["claim"], v["source"], v["score"], v["confidence"])
        )
    conn.commit()
    conn.close()

    