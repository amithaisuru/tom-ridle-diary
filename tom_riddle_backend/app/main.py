from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])

