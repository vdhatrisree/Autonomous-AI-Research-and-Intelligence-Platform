from fastapi import APIRouter
from api.schemas import ResearchRequest
from agents.orchestrator import run_research
from memory.db import init_db
from memory.store import save_session, save_verified_claims
from memory.recall import find_similar_past_questions
from verification.verifier import verify_report
from reporting.report_builder import build_full_report, save_report_to_file

router = APIRouter()
init_db()

@router.post("/research")
def do_research(request: ResearchRequest):
    question = request.question

    similar = find_similar_past_questions(question)
    report, used_documents, subtopics = run_research(question)
    verified = verify_report(report, used_documents)

    full_report = build_full_report(question, subtopics, report, used_documents, verified)
    save_report_to_file(full_report, question)

    session_id = save_session(question, report, used_documents)
    save_verified_claims(session_id, verified)

    return {
        "session_id": session_id,
        "question": question,
        "report": report,
        "verified_claims": verified,
        "related_sessions": similar,
    }