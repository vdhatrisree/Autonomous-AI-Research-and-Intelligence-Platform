from rag.context_builder import build_context
from rag.answer_generator import generate_answer

def write_section(subtopic, evidence_docs):
    if not evidence_docs:
        return f"### {subtopic}\nNo relevant evidence found.\n", []

    context = build_context(evidence_docs, list(range(len(evidence_docs))))
    answer = generate_answer(subtopic, context)

    if len(answer.strip()) < 20:
        answer = f"(Limited evidence available.) {evidence_docs[0].summary[:300]}"

    return f"### {subtopic}\n{answer}\n", evidence_docs