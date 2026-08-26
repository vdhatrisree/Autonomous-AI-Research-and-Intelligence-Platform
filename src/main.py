
"""
Core Pipeline (non-agentic)
----------------------------
Runs the base search -> extract -> embed -> retrieve -> verify -> RAG flow
in one fixed sequence. Useful for testing individual components (ML classifier,
FAISS, hybrid retrieval, knowledge graph) in isolation, without the overhead
of the full agent framework.

Does NOT include: memory/sessions, multi-agent planning, structured reports,
or the chat interface. For the full-featured system, use main_agentic.py instead.
"""
from sources import wikipedia_source, arxiv_source
from normalize import normalize
from dedupe import deduplicate
from storage import save_results
from display import display_results
from pdf_processor import download_and_extract_text
from chunking import chunk_text
from ml.classify import load_trained_model, predict_relevance
from transformers_lab.zero_shot import classify_topic
from embeddings.embedder import embed_texts
from vectorstore.faiss_index import build_index, search_index
from rag.context_builder import build_context
from rag.answer_generator import generate_answer
from retrieval.keyword_search import build_bm25_index, keyword_search
from retrieval.hybrid import hybrid_merge
from retrieval.reranker import rerank
from graph.schema import create_constraints
from graph.ingest import add_document, add_authors
from graph.extraction import extract_datasets, extract_arxiv_citations
from graph.ingest import add_dataset_usage, add_citations

def run(query):
    documents = []
    documents.extend(wikipedia_source.search(query))
    documents.extend(arxiv_source.search(query))

    documents = normalize(documents)
    documents = deduplicate(documents)

    create_constraints()
    for doc in documents:
        add_document(doc)
        add_authors(doc)

        full_text = " ".join(doc.chunks) if doc.chunks else doc.summary
        datasets = extract_datasets(full_text)
        if datasets:
            add_dataset_usage(doc, datasets)

        citations = extract_arxiv_citations(full_text)
        if citations:
            add_citations(doc, citations)

    print(f"\nAdded {len(documents)} documents to the knowledge graph.")

    for doc in documents:
        if doc.source == "arxiv" and doc.pdf_url:
            full_text = download_and_extract_text(doc.pdf_url)
            doc.chunks = chunk_text(full_text)

    try:
        ml_model, ml_vectorizer = load_trained_model()
        for doc in documents:
            relevance = predict_relevance(doc.summary, ml_model, ml_vectorizer)
            print(f"[ML Check] {doc.title[:50]}... -> {relevance}")
    except FileNotFoundError:
        print("\nNo trained model found yet. Run src/ml/run_training.py first.")

    ai_labels = ["artificial intelligence", "not related to artificial intelligence"]
    for doc in documents[:3]:
        scores = classify_topic(doc.summary, ai_labels)
        top_label = max(scores, key=scores.get)
        print(f"[Transformer Check] {doc.title[:50]}... -> {top_label} ({scores[top_label]:.2f})")

    summaries = [doc.summary for doc in documents]
    vectors = embed_texts(summaries)
    for doc, vec in zip(documents, vectors):
        doc.embedding = vec.tolist()
    print(f"\nGenerated embeddings for {len(documents)} documents.")

    index = build_index([doc.embedding for doc in documents])
    query_vector = embed_texts([query])[0]
    semantic_indices, _ = search_index(index, query_vector, top_k=8)

    bm25_index = build_bm25_index(documents)
    keyword_indices, _ = keyword_search(bm25_index, query, top_k=8)

    hybrid_indices = hybrid_merge(list(semantic_indices), keyword_indices, top_k=8)

    top_indices, rerank_scores = rerank(query, documents, hybrid_indices, top_k=5)

    print(f"\nTop {len(top_indices)} most relevant documents (after hybrid retrieval + reranking):")
    for rank, (idx, score) in enumerate(zip(top_indices, rerank_scores), start=1):
        print(f"  {rank}. (score: {score:.3f}) {documents[idx].title}")

    context = build_context(documents, top_indices)
    answer = generate_answer(query, context)
    print(f"\n=== RAG Answer ===\n{answer}\n")

    display_results([doc.__dict__ for doc in documents])
    saved_path = save_results(query, documents)
    print(f"\nSaved results to: {saved_path}")

if __name__ == "__main__":
    question = input("Enter your research question: ")
    run(question)