from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from features import transform

def evaluate_model(model, vectorizer, X_test, y_test):
    X_test_vec = transform(vectorizer, X_test)
    predictions = model.predict(X_test_vec)

    print("Precision:", precision_score(y_test, predictions, zero_division=0))
    print("Recall:", recall_score(y_test, predictions, zero_division=0))
    print("F1 Score:", f1_score(y_test, predictions, zero_division=0))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))