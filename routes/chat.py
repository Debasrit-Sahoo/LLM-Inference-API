from fastapi import APIRouter
from pydantic import BaseModel
from core.inference import run_inference

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = run_inference(req.message)
    return ChatResponse(response=reply)