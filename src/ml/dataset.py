import pandas as pd
import os

def load_dataset():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ml_training_data.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} real examples from {csv_path}")
        return df

    print("WARNING: No real training data found, falling back to tiny hardcoded dataset.")
    data = {
        "text": [
            "Neural networks learn patterns from data using backpropagation.",
            "This recipe uses flour, sugar, eggs, and butter.",
        ],
        "label": [1, 0],
    }
    return pd.DataFrame(data)