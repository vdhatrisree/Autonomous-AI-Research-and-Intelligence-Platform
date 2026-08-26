import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graph.schema import create_constraints
from graph.ingest import add_document, add_authors
from graph.query_graph import get_papers_by_source, get_authors_of_paper

class FakeDoc:
    def __init__(self, title, summary, url, source, authors):
        self.title = title
        self.summary = summary
        self.url = url
        self.source = source
        self.authors = authors

create_constraints()

doc = FakeDoc(
    title="Attention Is All You Need",
    summary="Introduces the transformer architecture based on self-attention.",
    url="https://arxiv.org/abs/1706.03762",
    source="arxiv",
    authors=["Ashish Vaswani", "Noam Shazeer"]
)

add_document(doc)
add_authors(doc)

print("Papers from arxiv:", get_papers_by_source("arxiv"))
print("Authors of paper:", get_authors_of_paper("Attention Is All You Need"))
