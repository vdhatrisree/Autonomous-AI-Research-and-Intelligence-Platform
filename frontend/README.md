# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# Autonomous AI Research & Intelligence Platform

An end-to-end AI system that takes a research question, autonomously searches
Wikipedia and arXiv, retrieves and ranks evidence, verifies claims against
sources, and produces a cited, structured research report — accessible via
CLI, a chat interface, a REST API, and a web frontend.

## Architecture


## Entry Points

| File | Purpose |
|---|---|
| `src/main.py` | Core pipeline, no agents/memory. Good for testing individual components. |
| `src/main_agentic.py` | **Primary entry point.** Full agentic system with memory, verification, reports. |
| `src/chat_repl.py` | Terminal chat interface for past research sessions. |
| `src/api/app.py` | FastAPI backend (`uvicorn api.app:app --reload`). |
| `frontend/` | React UI (`npm run dev`). |

## Running the System

**Prerequisites:** Python 3.13, Node.js, Neo4j Desktop (local instance running), a `.env` file (see `.env.example`).

```powershell
pip install -r requirements.txt

# Core pipeline (no agents)
cd src
python main.py

# Full agentic system
python main_agentic.py

# Chat about a past session
python chat_repl.py

# API server
uvicorn api.app:app --reload

# Frontend (separate terminal)
cd ../frontend
npm run dev

# Evaluation suite
cd ../src/evaluation
python run_evaluation.py

# MLflow dashboard
cd ../..
mlflow ui --backend-store-uri sqlite:///mlflow.db

# Docker (containerized backend)
docker compose up --build
```

## Known Limitations

- **Local LLM (`flan-t5-large`)** occasionally repeats or echoes prompt fragments in generated answers; both entry points now fall back to a clear message when this happens instead of returning garbage.
- **Citation extraction (`CITES` graph relationship)** rarely triggers, since it relies on exact-format arXiv ID matches in abstract text rather than real reference-list parsing.
- **Planner Agent** frequently falls back to default sub-questions rather than generating novel ones, due to the small model's limited instruction-following.
- **Run-to-run variance** exists in evaluation metrics (beam search + live search results aren't fully deterministic) — compare multiple MLflow runs rather than trusting a single run's numbers.

## Tech Stack

Python, PyTorch, Hugging Face Transformers, sentence-transformers, FAISS, Neo4j,
FastAPI, React, SQLite, MLflow, Docker.
