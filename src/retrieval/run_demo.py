from rank_bm25 import BM25Okapi
from keyword_search import build_bm25_index, keyword_search

class FakeDoc:
    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

documents = [
    FakeDoc("Neural Networks", "Neural networks learn patterns from data."),
    FakeDoc("Cooking", "This recipe uses flour, sugar, and eggs."),
    FakeDoc("Reinforcement Learning", "Reinforcement learning trains agents through rewards."),
]

bm25 = build_bm25_index(documents)
indices, scores = keyword_search(bm25, "learning agents", top_k=2)

for idx, score in zip(indices, scores):
    print(f"({score:.3f}) {documents[idx].title}")