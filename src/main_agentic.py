"""
Full Agentic Research Platform (primary entry point)
------------------------------------------------------
Runs the complete system: Planner -> Search -> Evidence -> Report agents,
research memory (SQLite sessions), evidence verification, structured
multi-section reports, and comparison against past research.

This is the main entry point for real use. See main.py for a simpler,
non-agentic version useful for isolated component testing.
"""

from agents.orchestrator import run_research
from memory.db import init_db
from memory.store import save_session
from memory.recall import find_similar_past_questions
from memory.compare import compare_with_past, compare_sources
from verification.verifier import verify_report
from reporting.report_builder import build_full_report, save_report_to_file
from memory.store import save_verified_claims

if __name__ == "__main__":
    init_db()
    question = input("Enter your research question: ")

    similar = find_similar_past_questions(question)
    if similar:
        print("\n[Memory] Found related past research:")
        for s in similar:
            print(f"  - {s['question']} (session {s['id']})")

    report, used_documents, subtopics = run_research(question)
    print("\n=== FINAL REPORT ===\n")
    print(report)

    verified = verify_report(report, used_documents)
    print("\n=== EVIDENCE VERIFICATION ===\n")
    for v in verified:
        print(f"[{v['confidence']}] ({v['score']}) {v['claim']}")
        print(f"   -> Source: {v['source']}\n")

    comparison_text = None
    if similar:
        past_id = similar[0]["id"]
        comparison_text = compare_with_past(question, report, past_id)
        source_diff = compare_sources(used_documents, past_id)
        print(f"\n=== COMPARISON WITH SESSION {past_id} ===\n{comparison_text}")
        print(f"Shared sources: {source_diff['shared_sources']}")
        print(f"New sources: {source_diff['new_sources']}")

    full_report = build_full_report(question, subtopics, report, used_documents, verified, comparison_text)
    saved_path = save_report_to_file(full_report, question)
    print(f"\n[Report] Full structured report saved to: {saved_path}")

    session_id = save_session(question, report, used_documents)
    if session_id:
        save_verified_claims(session_id, verified)
        print(f"\n[Memory] Saved as session {session_id}")
    else:
        print("\n[Memory] Could not save this session, but your report is still complete above.")