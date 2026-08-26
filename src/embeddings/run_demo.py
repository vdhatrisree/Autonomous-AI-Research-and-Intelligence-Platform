from semantic_search import semantic_search

documents = [
    "Neural networks learn patterns from data using backpropagation.",
    "This recipe uses flour, sugar, eggs, and butter.",
    "Reinforcement learning trains agents through rewards and penalties.",
    "The football match ended in a 2-1 victory.",
    "Large language models are trained on massive text corpora.",
]

query = "How do AI models get trained?"
results = semantic_search(query, documents)

print(f"Query: {query}\n")
for doc, score in results:
    print(f"({score:.3f}) {doc}")