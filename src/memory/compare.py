from memory.recall import get_session_by_id, get_sources_for_session
from rag.llm_client import get_model

def compare_with_past(current_question, current_report, past_session_id):
    past_session = get_session_by_id(past_session_id)
    if past_session is None:
        return "No matching past session found."

    past_words = set(past_session["report"].lower().split())
    current_words = set(current_report.lower().split())
    overlap = past_words & current_words

    overlap_ratio = len(overlap) / max(len(current_words), 1)

    if overlap_ratio > 0.4:
        return f"This research overlaps significantly with session {past_session_id} ('{past_session['question']}') — likely covering similar ground."
    elif overlap_ratio > 0.15:
        return f"This research is somewhat related to session {past_session_id} ('{past_session['question']}') but covers some new material."
    else:
        return f"This research appears mostly distinct from session {past_session_id} ('{past_session['question']}')."
    

def compare_sources(current_documents, past_session_id):
    past_sources = get_sources_for_session(past_session_id)
    past_titles = {s["title"] for s in past_sources}
    current_titles = {doc.title for doc in current_documents}

    return {
        "shared_sources": list(past_titles & current_titles),
        "new_sources": list(current_titles - past_titles),
        "past_only_sources": list(past_titles - current_titles),
    }

