from dataclasses import dataclass, field

@dataclass
class Document:
    title: str
    summary: str
    url: str
    source: str
    authors: list = field(default_factory=list)
    pdf_url: str = ""
    chunks: list = field(default_factory=list)
    embedding: list = field(default_factory=list)
    arxiv_id: str = ""