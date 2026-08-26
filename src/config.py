import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
HEADERS = {"User-Agent": "research-ai-learning-project/1.0 (contact: youremail@example.com)"}