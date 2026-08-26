import faiss
import numpy as np

def build_index(vectors):
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    vectors_np = np.array(vectors).astype("float32")
    index.add(vectors_np)
    return index

def search_index(index, query_vector, top_k=3):
    query_np = np.array([query_vector]).astype("float32")
    distances, indices = index.search(query_np, top_k)
    return indices[0], distances[0]

def save_index(index, path):
    faiss.write_index(index, path)

def load_index(path):
    return faiss.read_index(path)
