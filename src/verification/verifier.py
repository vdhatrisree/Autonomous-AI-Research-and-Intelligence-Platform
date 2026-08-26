from verification.claim_extractor import extract_claims
from verification.confidence import score_claim_against_sources, classify_confidence

def verify_report(report_text, evidence_docs):
    claims = extract_claims(report_text)
    source_texts = [doc.summary for doc in evidence_docs]
    source_titles = [doc.title for doc in evidence_docs]

    verified_claims = []
    for claim in claims:
        score, best_idx = score_claim_against_sources(claim, source_texts)
        confidence = classify_confidence(score)
        source_title = source_titles[best_idx] if best_idx >= 0 else "None"

        verified_claims.append({
            "claim": claim,
            "source": source_title,
            "score": round(score, 3),
            "confidence": confidence,
        })

    return verified_claims