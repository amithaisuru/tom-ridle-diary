from pydantic import BaseModel, Field
from typing import List, Literal


class Message(BaseModel):
    role: Literal["user", "model"]
    content: str

class ChatRequest(BaseModel):
    prompt: str
    history: List[Message] = Field(default_factory=list)

class ChatResponse(BaseModel):
    reply: str