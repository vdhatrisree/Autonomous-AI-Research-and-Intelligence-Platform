import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "embeddings"))

from embedder import embed_texts
from faiss_index import build_index, search_index

documents = [
    "Neural networks learn patterns from data using backpropagation.",
    "This recipe uses flour, sugar, eggs, and butter.",
    "Reinforcement learning trains agents through rewards and penalties.",
    "The football match ended in a 2-1 victory.",
    "Large language models are trained on massive text corpora.",
]

doc_vectors = embed_texts(documents)
index = build_index(doc_vectors)

query = "How do AI models get trained?"
query_vector = embed_texts([query])[0]

indices, distances = search_index(index, query_vector, top_k=3)

print(f"Query: {query}\n")
for idx, dist in zip(indices, distances):
    print(f"(distance: {dist:.3f}) {documents[idx]}")

    