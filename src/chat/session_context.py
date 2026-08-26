from memory.recall import get_session_by_id, get_sources_for_session, get_verified_claims

def load_session_context(session_id):
    session = get_session_by_id(session_id)
    if session is None:
        return None

    sources = get_sources_for_session(session_id)
    claims = get_verified_claims(session_id)

    return {
        "question": session["question"],
        "report": session["report"],
        "sources": sources,
        "claims": claims,
    }