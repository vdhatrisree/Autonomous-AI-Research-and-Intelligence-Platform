from fastapi import APIRouter, HTTPException
from api.schemas import ChatRequest
from chat.session_context import load_session_context
from chat.chat_engine import chat_respond

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    context = load_session_context(request.session_id)
    if context is None:
        raise HTTPException(status_code=404, detail="Session not found")

    response = chat_respond(request.message, context)
    return {"response": response}