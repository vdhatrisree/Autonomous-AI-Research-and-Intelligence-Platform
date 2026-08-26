from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    question: str

class ChatRequest(BaseModel):
    session_id: int
    message: str

    