import pandas as pd

def load_dataset():
    data = {
        "text": [
            "Neural networks learn patterns from data using backpropagation.",
            "The transformer architecture uses self-attention for NLP tasks.",
            "This recipe uses flour, sugar, eggs, and butter.",
            "The football match ended in a 2-1 victory.",
            "Reinforcement learning trains agents through rewards and penalties.",
            "Deep learning models require large amounts of training data.",
            "The stock market fell sharply after the announcement.",
            "She planted tomatoes and basil in her garden this spring.",
            "Convolutional neural networks are widely used in image recognition.",
            "The concert was postponed due to heavy rainfall.",
            "Large language models are trained on massive text corpora.",
            "He went hiking in the mountains over the weekend.",
            "Gradient descent optimizes the weights of a neural network.",
            "The chef prepared a five course tasting menu.",
            "GANs generate realistic images by pitting two networks against each other.",
            "The marathon route passed through the old city center.",
            "Attention mechanisms allow models to focus on relevant tokens.",
            "The museum opened a new exhibit on ancient pottery.",
            "Transfer learning reuses a pretrained model on a new task.",
            "The airline canceled several flights due to the storm.",
        ],
        "label": [1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    }
    return pd.DataFrame(data)