from dataset import load_dataset
from train import train_model
from evaluate import evaluate_model

if __name__ == "__main__":
    df = load_dataset()
    model, vectorizer, X_test, y_test = train_model(df)
    evaluate_model(model, vectorizer, X_test, y_test)
    print("\nModel and vectorizer saved to ../../models/")