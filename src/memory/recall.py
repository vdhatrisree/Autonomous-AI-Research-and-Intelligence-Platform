from memory.db import get_connection

def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, created_at FROM research_sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "question": r[1], "created_at": r[2]} for r in rows]

def get_session_by_id(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, report FROM research_sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return {"question": row[0], "report": row[1]}

def find_similar_past_questions(question, limit=3):
    all_sessions = get_all_sessions()
    question_words = set(question.lower().split())

    scored = []
    for session in all_sessions:
        past_words = set(session["question"].lower().split())
        overlap = len(question_words & past_words)
        if overlap > 0:
            scored.append((overlap, session))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [session for _, session in scored[:limit]]

def get_sources_for_session(session_id):
    from memory.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, source FROM session_sources WHERE session_id = ?", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"title": r[0], "url": r[1], "source": r[2]} for r in rows]

def get_verified_claims(session_id):
    from memory.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT claim, source, score, confidence FROM verified_claims WHERE session_id = ?",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"claim": r[0], "source": r[1], "score": r[2], "confidence": r[3]} for r in rows]

