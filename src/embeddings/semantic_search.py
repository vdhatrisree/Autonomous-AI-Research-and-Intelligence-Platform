from embedder import embed_texts
from similarity import cosine_similarity

def semantic_search(query, documents, top_k=3):
    query_vec = embed_texts([query])[0]
    doc_vecs = embed_texts(documents)

    scores = [cosine_similarity(query_vec, doc_vec) for doc_vec in doc_vecs]
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]