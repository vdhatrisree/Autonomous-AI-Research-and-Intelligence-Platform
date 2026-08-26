from embeddings.embedder import embed_texts
from embeddings.similarity import cosine_similarity

def answer_relevance(question, answer):
    vecs = embed_texts([question, answer])
    return float(cosine_similarity(vecs[0], vecs[1]))

def faithfulness_score(verified_claims):
    if not verified_claims:
        return 0.0
    scores = [c["score"] for c in verified_claims]
    return sum(scores) / len(scores)