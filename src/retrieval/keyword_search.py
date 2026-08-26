from rank_bm25 import BM25Okapi

def build_bm25_index(documents):
    tokenized = [doc.summary.lower().split() for doc in documents]
    return BM25Okapi(tokenized)

def keyword_search(bm25_index, query, top_k=5):
    tokenized_query = query.lower().split()
    scores = bm25_index.get_scores(tokenized_query)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return ranked_indices[:top_k], [scores[i] for i in ranked_indices[:top_k]]