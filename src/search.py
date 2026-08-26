import requests
from config import WIKI_SEARCH_URL, HEADERS

def search_wikipedia(query, limit=5):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit,
    }
    response = requests.get(WIKI_SEARCH_URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return [item["title"] for item in data["query"]["search"]]