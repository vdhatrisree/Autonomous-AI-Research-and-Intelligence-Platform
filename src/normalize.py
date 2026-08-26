def normalize(documents):
    for doc in documents:
        doc.title = " ".join(doc.title.split())
        doc.summary = " ".join(doc.summary.split())
    return documents