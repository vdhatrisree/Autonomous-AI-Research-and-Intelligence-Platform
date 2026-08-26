import torch
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

def evaluate_model(model, X_test, y_test):
    with torch.no_grad():
        outputs = model(X_test).squeeze()
        predictions = (outputs >= 0.5).float()

    print("Precision:", precision_score(y_test, predictions, zero_division=0))
    print("Recall:", recall_score(y_test, predictions, zero_division=0))
    print("F1 Score:", f1_score(y_test, predictions, zero_division=0))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))