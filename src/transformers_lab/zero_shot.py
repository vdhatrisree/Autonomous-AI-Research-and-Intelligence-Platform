from transformers import pipeline

_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")
    return _classifier

def classify_topic(text, labels):
    classifier = get_classifier()
    result = classifier(text, candidate_labels=labels)
    return dict(zip(result["labels"], result["scores"]))