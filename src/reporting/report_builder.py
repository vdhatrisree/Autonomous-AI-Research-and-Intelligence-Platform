from datetime import datetime
from reporting.formatters import (
    format_sources_section, format_evidence_section,
    identify_limitations, identify_research_gaps
)

def build_full_report(question, subtopics, findings_text, documents, verified_claims, comparison_text=None):
    sections = []

    sections.append(f"# Research Report\n\n**Question:** {question}\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    sections.append(f"## Background\nThis report investigates: *{question}*. It was broken into {len(subtopics)} sub-questions: " + ", ".join(subtopics))
    sections.append("## Methodology\nSources were retrieved from Wikipedia and arXiv, ranked using hybrid semantic + keyword search, reranked with a cross-encoder, and synthesized using a local language model. Claims were verified against source evidence using embedding similarity.")
    sections.append(f"## Key Findings\n{findings_text}")
    sections.append(f"## Sources\n{format_sources_section(documents)}")
    sections.append(f"## Evidence\n{format_evidence_section(verified_claims)}")

    if comparison_text:
        sections.append(f"## Comparison with Past Research\n{comparison_text}")

    sections.append(f"## Limitations\n{identify_limitations(verified_claims, documents)}")
    sections.append(f"## Research Gaps\n{identify_research_gaps(subtopics, verified_claims)}")
    sections.append("## Conclusion\nThis research provides an evidence-backed overview of the topic based on available sources. Confidence levels and limitations above should be considered when using these findings.")
    sections.append(f"## References\n{format_sources_section(documents)}")

    return "\n\n".join(sections)

import os

def save_report_to_file(report_text, question):
    try:
        os.makedirs("../reports", exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c == " " else "_" for c in question)[:50].strip()
        filename = f"../reports/{safe_name}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        return filename
    except OSError as e:
        print(f"[report_builder] Failed to save report file: {e}")
        return None

