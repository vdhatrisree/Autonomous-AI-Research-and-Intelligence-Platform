def build_context(documents, indices, max_docs=3, max_chars=300):
    context_parts = []
    for rank, idx in enumerate(indices[:max_docs], start=1):
        doc = documents[idx]
        trimmed_summary = doc.summary[:max_chars]
        context_parts.append(f"[Source {rank}] {doc.title}\n{trimmed_summary}")
    return "\n\n".join(context_parts)