from sklearn.feature_extraction.text import TfidfVectorizer

def create_vectorizer():
    return TfidfVectorizer(max_features=2000, stop_words="english", ngram_range=(1, 2))

def fit_transform(vectorizer, texts):
    return vectorizer.fit_transform(texts)

def transform(vectorizer, texts):
    return vectorizer.transform(texts)