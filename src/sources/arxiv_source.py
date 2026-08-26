import requests
import feedparser
from config import ARXIV_API_URL, HEADERS
from models import Document

def search(query, limit=5):
    params = {"search_query": f"all:{query}", "start": 0, "max_results": limit}
    try:
        response = requests.get(ARXIV_API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[arxiv_source] Search failed, skipping arXiv for this query: {e}")
        return []

    feed = feedparser.parse(response.text)

    documents = []
    for entry in feed.entries:
        pdf_link = next((l.href for l in entry.links if l.type == "application/pdf"), "")
        arxiv_id = entry.id.split("/abs/")[-1].split("v")[0]
        documents.append(Document(
            title=entry.title.strip(),
            summary=entry.summary.strip(),
            url=entry.link,
            source="arxiv",
            authors=[a.name for a in entry.authors],
            pdf_url=pdf_link,
            arxiv_id=arxiv_id,
        ))
    return documents