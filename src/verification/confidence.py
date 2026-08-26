from embeddings.embedder import embed_texts
from embeddings.similarity import cosine_similarity

def score_claim_against_sources(claim, source_texts):
    if not source_texts:
        return 0.0, -1

    claim_vec = embed_texts([claim])[0]
    source_vecs = embed_texts(source_texts)

    scores = [cosine_similarity(claim_vec, vec) for vec in source_vecs]
    best_score = max(scores)
    best_idx = scores.index(best_score)
    return float(best_score), best_idx

def classify_confidence(score):
    if score >= 0.6:
        return "High"
    elif score >= 0.4:
        return "Medium"
    else:
        return "Low"

