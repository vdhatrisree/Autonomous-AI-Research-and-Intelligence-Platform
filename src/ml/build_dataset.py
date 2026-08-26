import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sources"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from sources import wikipedia_source

AI_QUERIES = [
    "artificial intelligence", "machine learning", "deep learning",
    "neural network", "natural language processing", "computer vision",
    "reinforcement learning", "transformer deep learning", "large language model",
    "convolutional neural network",
]

NON_AI_QUERIES = [
    "cooking recipes", "football history", "gardening tips",
    "classical music composers", "ancient rome empire", "mountain hiking trails",
    "car engine maintenance", "yoga practice", "coffee brewing methods",
    "world war two history",
]

def fetch_labeled_documents(queries, label, limit_per_query=8):
    rows = []
    for query in queries:
        print(f"Fetching: {query}")
        docs = wikipedia_source.search(query, limit=limit_per_query)
        for doc in docs:
            if doc.summary and len(doc.summary.split()) >= 8:
                rows.append({"text": doc.summary, "label": label})
    return rows

if __name__ == "__main__":
    ai_rows = fetch_labeled_documents(AI_QUERIES, label=1)
    non_ai_rows = fetch_labeled_documents(NON_AI_QUERIES, label=0)

    df = pd.DataFrame(ai_rows + non_ai_rows)
    df = df.drop_duplicates(subset="text").reset_index(drop=True)

    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ml_training_data.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} labeled examples to {output_path}")
    print(f"AI-related: {(df['label'] == 1).sum()} | Not AI-related: {(df['label'] == 0).sum()}")

