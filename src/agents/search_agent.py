from sources import wikipedia_source, arxiv_source
from normalize import normalize
from dedupe import deduplicate

AI_ACRONYMS = {
    "cnn": "convolutional neural network",
    "rnn": "recurrent neural network",
    "gan": "generative adversarial network",
    "nlp": "natural language processing",
    "llm": "large language model",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "rl": "reinforcement learning",
    "svm": "support vector machine",
}

def expand_acronyms(text):
    words = text.split()
    expanded = []
    for word in words:
        clean = word.strip("?.,!").lower()
        if clean in AI_ACRONYMS:
            expanded.append(AI_ACRONYMS[clean])
        else:
            expanded.append(word)
    return " ".join(expanded)

def search_for_subtopic(subtopic, limit=3):
    expanded_query = expand_acronyms(subtopic)

    documents = []
    documents.extend(wikipedia_source.search(expanded_query, limit=limit))
    documents.extend(arxiv_source.search(expanded_query, limit=limit))
    documents = normalize(documents)
    documents = deduplicate(documents)
    return documents