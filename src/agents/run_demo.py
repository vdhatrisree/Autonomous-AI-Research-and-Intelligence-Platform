import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agents.orchestrator import run_research

question = "How do neural networks compare to traditional machine learning?"
report, used_documents = run_research(question)

print("\n=== FINAL REPORT ===\n")
print(report)