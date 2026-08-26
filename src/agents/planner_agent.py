from rag.llm_client import get_model

def plan_subtopics(question, max_subtopics=3):
    try:
        tokenizer, model = get_model()
        prompt = f"List {max_subtopics} factual sub-questions about this topic, one per line. Do not ask for opinions or 'best' options:\n\n{question}"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
        outputs = model.generate(**inputs, max_new_tokens=100, num_beams=4)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        subtopics = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        subtopics = [s for s in subtopics if len(s) > 10]
    except Exception as e:
        print(f"[planner_agent] Planning failed, using fallback subtopics: {e}")
        subtopics = []

    if len(subtopics) < 2:
        subtopics = [question, f"What are the key techniques in {question}?"]

    return subtopics[:max_subtopics]