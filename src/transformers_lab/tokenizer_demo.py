from transformers import AutoTokenizer

def show_tokenization(text, model_name="distilbert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    ids = tokenizer.convert_tokens_to_ids(tokens)
    return tokens, ids

from sentiment import analyze_sentiment

review_text = "This paper presents a groundbreaking and elegant solution."
label, score = analyze_sentiment(review_text)
print(f"\nSentiment: {label} (confidence: {score:.3f})")

