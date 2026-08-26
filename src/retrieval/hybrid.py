def hybrid_merge(semantic_indices, keyword_indices, top_k=5):
    scores = {}
    for rank, idx in enumerate(semantic_indices):
        scores[idx] = scores.get(idx, 0) + (1.0 / (rank + 1))
    for rank, idx in enumerate(keyword_indices):
        scores[idx] = scores.get(idx, 0) + (1.0 / (rank + 1))

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [idx for idx, score in ranked[:top_k]]