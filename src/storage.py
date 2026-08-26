import json
import os
from dataclasses import asdict
from config import DATA_DIR

def save_results(query, documents):
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, "last_results.json")
    data = {"query": query, "results": [asdict(doc) for doc in documents]}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filename