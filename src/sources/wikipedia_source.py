import requests
from config import WIKI_SEARCH_URL, WIKI_SUMMARY_URL, HEADERS
from models import Document

def search(query, limit=5):
    params = {
        "action": "query", "list": "search",
        "srsearch": query, "format": "json", "srlimit": limit,
    }
    try:
        response = requests.get(WIKI_SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        titles = [item["title"] for item in response.json()["query"]["search"]]
    except requests.exceptions.RequestException as e:
        print(f"[wikipedia_source] Search failed, skipping Wikipedia for this query: {e}")
        return []

    documents = []
    for title in titles:
        url = WIKI_SUMMARY_URL + title.replace(" ", "_")
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue
            data = r.json()
        except requests.exceptions.RequestException:
            continue

        documents.append(Document(
            title=data.get("title", ""),
            summary=data.get("extract", ""),
            url=data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            source="wikipedia",
        ))
    return documents