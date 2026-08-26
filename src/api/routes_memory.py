from fastapi import APIRouter, HTTPException
from memory.recall import get_all_sessions, get_session_by_id, get_sources_for_session, get_verified_claims

router = APIRouter()

@router.get("/sessions")
def list_sessions():
    return get_all_sessions()

@router.get("/sessions/{session_id}")
def get_session(session_id: int):
    session = get_session_by_id(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session["sources"] = get_sources_for_session(session_id)
    session["claims"] = get_verified_claims(session_id)
    return session