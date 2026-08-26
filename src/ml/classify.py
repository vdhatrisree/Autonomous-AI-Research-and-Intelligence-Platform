import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "classifier.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.joblib")

def load_trained_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def predict_relevance(text, model, vectorizer):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return "AI-related" if prediction == 1 else "Not AI-related"