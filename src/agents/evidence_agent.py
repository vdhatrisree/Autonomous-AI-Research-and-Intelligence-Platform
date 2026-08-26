from embeddings.embedder import embed_texts
from vectorstore.faiss_index import build_index, search_index
from retrieval.reranker import rerank

def find_evidence(subtopic, documents, top_k=3):
    if not documents:
        return []

    vectors = embed_texts([doc.summary for doc in documents])
    for doc, vec in zip(documents, vectors):
        doc.embedding = vec.tolist()

    index = build_index([doc.embedding for doc in documents])
    query_vector = embed_texts([subtopic])[0]
    candidate_count = min(top_k * 2, len(documents))
    semantic_indices, _ = search_index(index, query_vector, top_k=candidate_count)

    top_indices, _ = rerank(subtopic, documents, list(semantic_indices), top_k=min(top_k, len(documents)))
    return [documents[i] for i in top_indices]