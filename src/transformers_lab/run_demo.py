from tokenizer_demo import show_tokenization

text = "Transformers use self-attention to understand context in language."
tokens, ids = show_tokenization(text)

print("Original text:", text)
print("Tokens:", tokens)
print("Token IDs:", ids)

from zero_shot import classify_topic

topic_text = "Researchers proposed a new retrieval-augmented method for question answering."
labels = ["artificial intelligence", "sports", "cooking", "finance"]
scores = classify_topic(topic_text, labels)

print("\nZero-shot classification:")
for label, score in scores.items():
    print(f"  {label}: {score:.3f}")

