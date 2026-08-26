from fastapi import FastAPI
from api.routes_research import router as research_router
from api.routes_memory import router as memory_router
from api.routes_chat import router as chat_router

app = FastAPI(title="Autonomous AI Research Platform")

app.include_router(research_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "running", "message": "Research API is live"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

