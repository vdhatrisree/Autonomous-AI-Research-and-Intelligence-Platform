def recall_at_k(retrieved_titles, relevant_titles, k):
    retrieved_top_k = set(retrieved_titles[:k])
    relevant_set = set(relevant_titles)
    if not relevant_set:
        return 0.0
    hits = retrieved_top_k & relevant_set
    return len(hits) / len(relevant_set)

def precision_at_k(retrieved_titles, relevant_titles, k):
    retrieved_top_k = retrieved_titles[:k]
    if not retrieved_top_k:
        return 0.0
    relevant_set = set(relevant_titles)
    hits = sum(1 for title in retrieved_top_k if title in relevant_set)
    return hits / len(retrieved_top_k)

def mean_reciprocal_rank(retrieved_titles, relevant_titles):
    relevant_set = set(relevant_titles)
    for rank, title in enumerate(retrieved_titles, start=1):
        if title in relevant_set:
            return 1.0 / rank
    return 0.0

