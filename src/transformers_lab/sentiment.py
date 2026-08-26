from transformers import pipeline

def analyze_sentiment(text):
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)[0]
    return result["label"], result["score"]