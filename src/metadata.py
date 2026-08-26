def extract_basic_metadata(document):
    return {
        "title": document.title,
        "authors": document.authors,
        "source": document.source,
        "num_chunks": len(document.chunks),
        "has_pdf": bool(document.pdf_url),
    }