import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from features import create_vectorizer, fit_transform

def train_model(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
    )
    vectorizer = create_vectorizer()
    X_train_vec = fit_transform(vectorizer, X_train)

    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    joblib.dump(model, "../../models/classifier.joblib")
    joblib.dump(vectorizer, "../../models/vectorizer.joblib")

    return model, vectorizer, X_test, y_test