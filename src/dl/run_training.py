import torch
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from dataset import load_dataset
from model import SimpleClassifier
from train import train_model
from evaluate import evaluate_model

df = load_dataset()
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.3, random_state=42
)

vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train_text).toarray()
X_test_vec = vectorizer.transform(X_test_text).toarray()

X_train_tensor = torch.tensor(X_train_vec, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_vec, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

model = SimpleClassifier(input_dim=X_train_tensor.shape[1])
model = train_model(model, X_train_tensor, y_train_tensor)
evaluate_model(model, X_test_tensor, y_test_tensor)

import joblib

torch.save(model.state_dict(), "../../models/dl_classifier.pt")
joblib.dump(vectorizer, "../../models/dl_vectorizer.joblib")
print("\nModel and vectorizer saved to ../../models/")
