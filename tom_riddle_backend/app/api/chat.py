from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import generate_chat_reponse, generate_chat_reponse_with_google

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_model(request: ChatRequest):
    reply_text = await generate_chat_reponse_with_google(request.prompt, request.history)
    return ChatResponse(reply=reply_text)