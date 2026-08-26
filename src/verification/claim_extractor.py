import re

PLACEHOLDER_PHRASES = [
    "could not generate a full answer",
    "limited evidence available",
    "answer generation failed",
]

def extract_claims(report_text, min_words=6):
    clean_text = re.sub(r'^#{1,6}\s*.*$', '', report_text, flags=re.MULTILINE)
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)

    claims = []
    for s in sentences:
        s = s.strip()
        if len(s.split()) < min_words:
            continue
        if any(phrase in s.lower() for phrase in PLACEHOLDER_PHRASES):
            continue
        claims.append(s)
    return claims