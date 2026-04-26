from pydantic import BaseModel
from typing import List, Dict

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9


class ChatRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    history: List[Dict] = []

    # ✅ ADD THESE (FIX)
    max_tokens: int = 200
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9