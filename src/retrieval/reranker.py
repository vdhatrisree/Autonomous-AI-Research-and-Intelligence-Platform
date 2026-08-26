from sentence_transformers import CrossEncoder

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _reranker

def rerank(query, documents, candidate_indices, top_k=5):
    reranker = get_reranker()
    pairs = [[query, documents[idx].summary] for idx in candidate_indices]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(candidate_indices, scores), key=lambda x: x[1], reverse=True)
    return [idx for idx, score in ranked[:top_k]], [score for idx, score in ranked[:top_k]]

