# Autonomous AI Research & Intelligence Platform

An end-to-end AI system that takes a research question, autonomously searches Wikipedia and arXiv, retrieves and ranks evidence, verifies claims against sources, and produces a cited, structured research report — accessible via CLI, a chat interface, a REST API, and a web frontend.

Built as a progressive learning project covering the full modern AI engineering stack: data engineering, classical ML, deep learning, transformers, embeddings, vector search, knowledge graphs, RAG, agentic AI, evaluation, and MLOps.

---

## Table of Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Evaluation & MLOps](#evaluation--mlops)
- [Known Limitations](#known-limitations)
- [What I Learned](#what-i-learned)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Most "AI research assistants" either hallucinate confidently or just dump search results with no synthesis. This project tries to do better by treating every generated claim as something that must be traced back to a real source and scored for how well that source actually supports it — before it's shown to the user.

The system is built in layers, each one independently testable, so retrieval quality, generation quality, and reasoning quality can all be debugged and evaluated separately instead of as one opaque black box.

---

## Screenshots

<img width="1757" height="952" alt="Screenshot 2026-08-26 090608" src="https://github.com/user-attachments/assets/1b2b3901-b2a0-4179-8d18-f1cd498d9372" />

<img width="1770" height="928" alt="Screenshot 2026-08-26 090618" src="https://github.com/user-attachments/assets/7fa89f5e-9d6a-42f7-bca4-97dbff77dd9f" />

<img width="1757" height="928" alt="Screenshot 2026-08-26 091433" src="https://github.com/user-attachments/assets/1a951bf6-c7c9-4092-8be2-6608dd55d702" />



### Research Desk — Main Interface
*The catalog-style UI showing a submitted research question and generated report.*

![Research Desk UI](./docs/screenshots/research-desk.png)

### Evidence Verification — Confidence Stamps
*Every claim shown with a High / Medium / Low confidence stamp and its matched source.*

![Evidence Verification](./docs/screenshots/evidence-verification.png)

### Knowledge Graph — Neo4j Browser
*Papers, authors, sources, and datasets connected as a graph.*

![Knowledge Graph](./docs/screenshots/knowledge-graph.png)

### FastAPI Interactive Docs
*The `/api/research`, `/api/sessions`, and `/api/chat` endpoints, testable directly in the browser.*

![API Docs](./docs/screenshots/api-docs.png)

### MLflow Experiment Tracking
*Evaluation runs logged with Recall@K, Precision@K, MRR, faithfulness, and latency, comparable over time.*

![MLflow Dashboard](./docs/screenshots/mlflow-dashboard.png)

### Chat Interface
*Following up on a past research session — sources and evidence answered instantly from stored data, open-ended questions answered by the LLM.*

![Chat Interface](./docs/screenshots/chat-interface.png)

---

## Features

- **Multi-source retrieval** — searches Wikipedia and arXiv, extracts and chunks full PDF text for papers
- **Hybrid search** — combines semantic (FAISS + sentence-transformers) and keyword (BM25) retrieval, merged via reciprocal rank fusion
- **Reranking** — a cross-encoder re-scores the combined candidate pool for the most accurate final ranking
- **Knowledge graph** — Neo4j stores Papers, Authors, Sources, and Datasets as connected entities, queryable independently of the vector store
- **Multi-agent pipeline** — a Planner breaks a question into sub-questions; Search, Evidence, and Report agents handle each one; an orchestrator combines the results
- **Evidence verification** — every claim in a generated report is checked via embedding similarity against its source and labeled High / Medium / Low confidence
- **Research memory** — past sessions, sources, and reports are stored in SQLite, with keyword-based recall of related past research and a rule-based comparison between sessions
- **Structured reports** — 11-section Markdown reports (background, methodology, findings, evidence, limitations, gaps, conclusion, references) saved to disk
- **Chat interface** — ask follow-up questions about any past session; structured questions (sources, evidence) are answered directly from stored data, open-ended questions fall back to the LLM
- **Full-stack app** — FastAPI backend + React frontend with a custom "research archive" visual design
- **Containerized backend** — Docker + Docker Compose, connecting to a local Neo4j instance via `host.docker.internal`
- **Evaluation harness** — a hand-labeled golden set scored on Recall@K, Precision@K, MRR, answer relevance, and faithfulness, with per-run latency and success tracking
- **Experiment tracking** — every evaluation run logged to MLflow for comparison over time
- **Resilience** — network calls (Wikipedia, arXiv, Neo4j) and LLM generation calls are all wrapped with error handling and graceful fallbacks, so a single failure doesn't crash the whole pipeline

---

## Architecture

```
                Research Question
                       |
                       v
              ┌─────────────────┐
              │  Planner Agent   │  breaks question into sub-questions
              └────────┬─────────┘
                       |
          ┌────────────┴────────────┐
          v                         v
  ┌───────────────┐         ┌───────────────┐
  │  Search Agent  │  ...    │  Search Agent  │   (one per sub-question)
  └───────┬────────┘         └───────┬────────┘
          |                          |
Wikipedia + arXiv search    Wikipedia + arXiv search
PDF extraction + chunking   PDF extraction + chunking
          |                          |
          v                          v
  ┌────────────────────────────────────────┐
  │              Evidence Agent              │
  │  Embeddings -> FAISS -> BM25 -> Hybrid   │
  │  Merge -> Cross-Encoder Rerank           │
  └───────────────────┬──────────────────────┘
                       v
              ┌─────────────────┐
              │  Report Agent    │  RAG generation per sub-question
              └────────┬─────────┘
                       v
              ┌─────────────────┐
              │Evidence Verifier │  claim -> source -> confidence
              └────────┬─────────┘
                       v
          ┌────────────┴────────────┐
          v                         v
┌──────────────────┐      ┌──────────────────┐
│  Knowledge Graph   │      │  Research Memory  │
│  (Neo4j)            │      │  (SQLite)          │
└──────────────────┘      └──────────────────┘
                       |
                       v
             Structured Research Report
                (Markdown, 11 sections)
                       |
                       v
          FastAPI Backend  <->  React Frontend
                       |
                 Chat Interface
          (follow-ups on past sessions)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13, JavaScript (React) |
| ML / DL | scikit-learn, PyTorch |
| NLP / LLM | Hugging Face Transformers, sentence-transformers, `flan-t5-large` |
| Retrieval | FAISS, rank_bm25, cross-encoder reranking |
| Graph DB | Neo4j |
| Relational / Memory | SQLite |
| Backend | FastAPI, Uvicorn |
| Frontend | React (Vite), Axios |
| Containerization | Docker, Docker Compose |
| Experiment Tracking | MLflow |
| Data Sources | Wikipedia API, arXiv API |

---

## Project Structure

```
research-ai/
├── src/
│ ├── main.py # core pipeline (no agents/memory)
│ ├── main_agentic.py # PRIMARY entry point — full agentic system
│ ├── chat_repl.py # terminal chat interface
│ ├── sources/ # Wikipedia + arXiv search
│ ├── ml/ # classical ML relevance classifier
│ ├── dl/ # PyTorch neural network experiments
│ ├── transformers_lab/ # tokenization, zero-shot, sentiment demos
│ ├── embeddings/ # sentence-transformers + semantic search
│ ├── vectorstore/ # FAISS indexing
│ ├── retrieval/ # BM25, hybrid fusion, reranking
│ ├── graph/ # Neo4j client, schema, ingestion, queries
│ ├── rag/ # context building + LLM answer generation
│ ├── agents/ # Planner, Search, Evidence, Report, Orchestrator
│ ├── memory/ # SQLite sessions, recall, comparison
│ ├── verification/ # claim extraction + confidence scoring
│ ├── reporting/ # structured report assembly
│ ├── chat/ # chat context + response engine
│ ├── api/ # FastAPI app, routes, schemas
│ ├── evaluation/ # golden set + retrieval/RAG/system metrics
│ └── mlops/ # MLflow tracking
├── frontend/ # React app
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js (for the frontend)
- [Neo4j Desktop](https://neo4j.com/download/) with a running local instance
- (Optional) [Docker Desktop](https://www.docker.com/products/docker-desktop/) for containerized deployment

### Installation

```powershell
git clone https://github.com/vdhatrisree/Autonomous-AI-Research-and-Intelligence-Platform.git
cd Autonomous-AI-Research-and-Intelligence-Platform

pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local Neo4j URI, username, and password
```

### Frontend setup

```powershell
cd frontend
npm install
```

---

## Usage

### Full agentic system (recommended)

```powershell
cd src
python main_agentic.py
```

Runs the complete pipeline: planning, multi-source search, hybrid retrieval, reranking, RAG generation, evidence verification, memory, and structured report saving.

### Core pipeline (component testing)

```powershell
cd src
python main.py
```

A simpler, single-pass pipeline without agents or memory — useful for testing retrieval, the knowledge graph, or the ML classifier in isolation.

### Chat about past research

```powershell
cd src
python chat_repl.py
```

### Full web app

```powershell
# Terminal 1 — backend
cd src
uvicorn api.app:app --reload

# Terminal 2 — frontend
cd frontend
npm run dev
```

Then open `http://localhost:5173`.

### Docker (backend only)

```powershell
docker compose up --build
```

Serves the API at `http://localhost:8000`. Connects to your local Neo4j instance via `host.docker.internal`.

---

## API Reference

Interactive docs available at `http://localhost:8000/docs` once the backend is running.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/research` | Runs the full research pipeline for a question |
| `GET` | `/api/sessions` | Lists all past research sessions |
| `GET` | `/api/sessions/{id}` | Retrieves one session with its sources and verified claims |
| `POST` | `/api/chat` | Answers a follow-up question about a past session |
| `GET` | `/health` | Health check |

---

## Evaluation & MLOps

A hand-labeled golden set of research questions (with known-relevant document titles) is used to score the system on:

- **Retrieval:** Recall@5, Precision@5, Mean Reciprocal Rank
- **Generation:** Answer relevance (embedding similarity to question), Faithfulness (average confidence of verified claims)
- **System:** Per-question latency, success/failure rate

```powershell
cd src/evaluation
python run_evaluation.py
```

Every run is logged to MLflow for comparison over time:

```powershell
cd ../..
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open `http://127.0.0.1:5000` to browse experiment history.

---

## Known Limitations

- **Local LLM (`flan-t5-large`)** occasionally repeats or echoes prompt fragments instead of generating a real answer, particularly on vaguely-phrased or open-ended questions. Both entry points fall back to a clear message when this happens rather than showing garbled output.
- **Citation extraction (`CITES` graph relationship)** rarely triggers in practice, since it relies on exact-format arXiv ID matches (`arXiv:XXXX.XXXXX`) inside abstract text, rather than real reference-list parsing (which would need a dedicated tool like GROBID).
- **Planner Agent** frequently falls back to default sub-questions instead of generating genuinely novel ones, due to the small model's limited instruction-following ability.
- **Run-to-run variance** exists in evaluation metrics — beam search generation and live search results aren't fully deterministic, so compare multiple MLflow runs rather than trusting a single run's numbers.
- **Backend only is containerized** — the frontend and Neo4j run outside Docker for now, by design, to avoid unnecessary complexity at this stage.

---

## What I Learned

This project was built incrementally as a learning exercise, phase by phase, rather than all at once. Some of the most useful lessons along the way:

- Small local models (`flan-t5-base/large`) are reliable for single-document extraction but consistently fail at cross-document synthesis (comparison, multi-source reasoning) — the right fix is often a **simple rule-based fallback**, not more prompt engineering.
- Retrieval quality and generation quality are separate failure modes and need to be evaluated separately — a perfect retrieval result can still produce a bad answer, and vice versa.
- Real external APIs (Wikipedia, arXiv) fail in production in ordinary ways (timeouts, rate limits) that need explicit handling, not just a happy-path implementation.
- Evaluation metrics without repeated runs can be misleading — this system shows genuine run-to-run variance that a single evaluation pass would hide.

---

## Roadmap

- [ ] Fine-tune `flan-t5` on real research Q&A data collected from usage
- [ ] Proper citation parsing (GROBID or similar) to fix the `CITES` graph relationship
- [ ] Automated test suite
- [ ] CI/CD pipeline

---

## License

MIT
