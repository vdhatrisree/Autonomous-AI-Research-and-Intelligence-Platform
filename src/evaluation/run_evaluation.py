import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from mlops.tracking import init_mlflow, log_question_run, log_summary
import mlflow
from evaluation.golden_set import GOLDEN_SET
from evaluation.retrieval_metrics import recall_at_k, precision_at_k, mean_reciprocal_rank
from evaluation.rag_metrics import answer_relevance, faithfulness_score
from evaluation.system_metrics import run_with_timing
from agents.orchestrator import run_research
from verification.verifier import verify_report

init_mlflow()
mlflow.start_run(run_name="evaluation_batch")

results = []

for item in GOLDEN_SET:
    question = item["question"]
    relevant_titles = item["relevant_titles"]

    print(f"\nEvaluating: {question}")
    outcome = run_with_timing(run_research, question)

    if not outcome["success"]:
        results.append({"question": question, "error": outcome["error"]})
        continue

    report, used_documents, subtopics = outcome["result"]
    retrieved_titles = [doc.title for doc in used_documents]
    verified = verify_report(report, used_documents)

    results.append({
        "question": question,
        "latency_seconds": outcome["latency_seconds"],
        "recall_at_5": round(recall_at_k(retrieved_titles, relevant_titles, 5), 3),
        "precision_at_5": round(precision_at_k(retrieved_titles, relevant_titles, 5), 3),
        "mrr": round(mean_reciprocal_rank(retrieved_titles, relevant_titles), 3),
        "answer_relevance": round(answer_relevance(question, report), 3),
        "faithfulness": round(faithfulness_score(verified), 3),
    })

    log_question_run(len(results), results[-1])

print("\n" + "=" * 50)
print("EVALUATION SUMMARY")
print("=" * 50)

successful = [r for r in results if "error" not in r]
for r in results:
    if "error" in r:
        print(f"\n[FAILED] {r['question']}: {r['error']}")
    else:
        print(f"\n{r['question']}")
        print(f"  Recall@5: {r['recall_at_5']} | Precision@5: {r['precision_at_5']} | MRR: {r['mrr']}")
        print(f"  Answer Relevance: {r['answer_relevance']} | Faithfulness: {r['faithfulness']}")
        print(f"  Latency: {r['latency_seconds']}s")

if successful:
    avg_recall = sum(r["recall_at_5"] for r in successful) / len(successful)
    avg_faithfulness = sum(r["faithfulness"] for r in successful) / len(successful)
    print(f"\nAverages — Recall@5: {round(avg_recall, 3)} | Faithfulness: {round(avg_faithfulness, 3)}")
    print(f"Success rate: {len(successful)}/{len(results)}")
    success_rate = len(successful) / len(results)

os.makedirs("../../evaluation_reports", exist_ok=True)
with open("../../evaluation_reports/latest_eval.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to evaluation_reports/latest_eval.json")

log_summary(avg_recall, avg_faithfulness, success_rate, "flan-t5-large", "../../evaluation_reports/latest_eval.json")
mlflow.end_run()
print("Logged to MLflow — run 'mlflow ui' from the research-ai root to view.")

