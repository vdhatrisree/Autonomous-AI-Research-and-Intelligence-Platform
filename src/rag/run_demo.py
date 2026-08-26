import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from rag.context_builder import build_context
from rag.answer_generator import generate_answer

class FakeDoc:
    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

documents = [
    FakeDoc("Artificial intelligence", "AI is the capability of computer systems to perform tasks requiring human-like intelligence."),
    FakeDoc("AI agent", "An AI agent pursues goals and takes actions autonomously using tools."),
]

context = build_context(documents, [0, 1])
answer = generate_answer("What is AI?", context)
print(answer)