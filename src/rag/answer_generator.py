from rag.llm_client import get_model

def generate_answer(question, context):
    try:
        tokenizer, model = get_model()
        prompt = f"""Answer the question using only the sources below. Mention which source(s) you used, like [Source 1].

Sources:
{context}

Question: {question}

Answer:"""

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = model.generate(**inputs, max_new_tokens=150, num_beams=4)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if len(answer.strip()) < 20:
            return "(The model could not generate a full answer. Please review the sources above directly.)"
        return answer
    except Exception as e:
        print(f"[answer_generator] LLM generation failed: {e}")
        return "(Answer generation failed. Please see the sources above for relevant information.)"