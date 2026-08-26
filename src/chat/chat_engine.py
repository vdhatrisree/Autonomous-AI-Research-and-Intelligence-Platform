from rag.llm_client import get_model

def answer_followup(user_question, context):
    try:
        tokenizer, model = get_model()
        report_snippet = context["report"][:600]
        prompt = f"""Research report:
{report_snippet}

Question: {user_question}

Answer based only on the report above:"""

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = model.generate(**inputs, max_new_tokens=150, num_beams=4)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"[chat_engine] Follow-up answer failed: {e}")
        return "Sorry, I couldn't generate an answer right now. Try asking about sources or evidence instead."
    
def handle_special_queries(user_question, context):
    q_lower = user_question.lower()

    if "source" in q_lower or "reference" in q_lower:
        if not context["sources"]:
            return "No sources are recorded for this session."
        lines = [f"- {s['title']} ({s['source']})" for s in context["sources"]]
        return "Sources used:\n" + "\n".join(lines)

    if "evidence" in q_lower or "confidence" in q_lower:
        if not context["claims"]:
            return "No verified claims are recorded for this session."
        lines = [f"- [{c['confidence']}] {c['claim'][:100]}" for c in context["claims"]]
        return "Verified claims:\n" + "\n".join(lines)

    return None

def chat_respond(user_question, context):
    special_answer = handle_special_queries(user_question, context)
    if special_answer:
        return special_answer
    return answer_followup(user_question, context)

