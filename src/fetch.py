import requests
from config import WIKI_SUMMARY_URL, HEADERS

def fetch_summary(title):
    url = WIKI_SUMMARY_URL + title.replace(" ", "_")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()