from transformers import T5Tokenizer, T5ForConditionalGeneration

_tokenizer = None
_model = None

def get_model():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
        _model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
    return _tokenizer, _model