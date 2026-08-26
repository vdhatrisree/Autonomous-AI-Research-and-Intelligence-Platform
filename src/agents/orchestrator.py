from agents.planner_agent import plan_subtopics
from agents.search_agent import search_for_subtopic
from agents.evidence_agent import find_evidence
from agents.report_agent import write_section

def run_research(question):
    subtopics = plan_subtopics(question)
    print(f"\n[Planner Agent] Subtopics: {subtopics}")

    report_sections = []
    all_documents = []

    for subtopic in subtopics:
        print(f"\n[Search Agent] Searching: {subtopic}")
        documents = search_for_subtopic(subtopic)

        print(f"[Evidence Agent] Ranking {len(documents)} documents")
        evidence = find_evidence(subtopic, documents)
        all_documents.extend(evidence)

        print(f"[Report Agent] Writing section")
        section, section_evidence = write_section(subtopic, evidence)
        report_sections.append(section)

    report = "\n".join(report_sections)
    return report, all_documents, subtopics