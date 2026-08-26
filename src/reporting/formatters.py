def format_sources_section(documents):
    if not documents:
        return "No sources were used."

    lines = []
    seen = set()
    for doc in documents:
        if doc.title in seen:
            continue
        seen.add(doc.title)
        lines.append(f"- {doc.title} ({doc.source}) — {doc.url}")
    return "\n".join(lines)

def format_evidence_section(verified_claims):
    if not verified_claims:
        return "No claims were verified."

    lines = []
    for v in verified_claims:
        lines.append(f"- **Claim:** {v['claim']}")
        lines.append(f"  **Source:** {v['source']} | **Confidence:** {v['confidence']} ({v['score']})")
    return "\n".join(lines)

def identify_limitations(verified_claims, documents):
    low_confidence = [v for v in verified_claims if v["confidence"] == "Low"]
    limitations = []

    if low_confidence:
        limitations.append(f"{len(low_confidence)} claim(s) had low confidence support from available sources.")
    if len(documents) < 5:
        limitations.append("A limited number of sources were retrieved for this research.")
    arxiv_count = sum(1 for d in documents if d.source == "arxiv")
    if arxiv_count == 0:
        limitations.append("No peer-reviewed papers (arXiv) were found; results rely on general reference sources.")

    if not limitations:
        limitations.append("No major limitations detected in this research pass.")

    return "\n".join(f"- {l}" for l in limitations)

def identify_research_gaps(subtopics, verified_claims):
    covered_topics = {v["source"] for v in verified_claims}
    gaps = []

    weak_subtopics = [v["claim"] for v in verified_claims if v["confidence"] in ("Low", "Medium")]
    if weak_subtopics:
        gaps.append("Some sub-questions were only weakly supported by available evidence and may need deeper investigation.")
    if len(covered_topics) < len(subtopics):
        gaps.append("Not all sub-questions had a uniquely matched source, suggesting overlapping or incomplete coverage.")

    if not gaps:
        gaps.append("No obvious research gaps identified in this pass.")

    return "\n".join(f"- {g}" for g in gaps)

