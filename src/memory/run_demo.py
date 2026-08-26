import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from memory.db import init_db
from memory.store import save_session
from memory.recall import get_all_sessions, find_similar_past_questions

class FakeDoc:
    def __init__(self, title, url, source):
        self.title = title
        self.url = url
        self.source = source

init_db()
docs = [FakeDoc("Convolutional neural network", "https://en.wikipedia.org/wiki/CNN", "wikipedia")]
save_session("What is a CNN?", "CNNs are a type of neural network...", docs)

print("All sessions:", get_all_sessions())
print("\nSimilar to 'What is CNN used for?':", find_similar_past_questions("What is CNN used for?"))
