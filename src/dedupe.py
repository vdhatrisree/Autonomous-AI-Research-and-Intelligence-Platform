def deduplicate(documents):
    seen_titles = set()
    unique_docs = []
    for doc in documents:
        key = doc.title.lower().strip()
        if key not in seen_titles:
            seen_titles.add(key)
            unique_docs.append(doc)
    return unique_docs