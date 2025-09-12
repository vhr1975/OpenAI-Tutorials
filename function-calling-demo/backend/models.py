# Pydantic models for requests/responses
from pydantic import BaseModel
from typing import Optional, Dict

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class FunctionCall(BaseModel):
    name: str
    arguments: Dict

class ChatResponse(BaseModel):
    response: str
    function_call: Optional[FunctionCall] = None
    error: Optional[str] = None
