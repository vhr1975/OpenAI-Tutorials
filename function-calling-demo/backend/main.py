# FastAPI app entry point (stub)

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from functions import FUNCTIONS
from openai_client import call_openai_api
from utils import log_request, log_response, log_error

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    function_call: Optional[dict] = None
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Function Calling Demo Backend"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    log_request(request)
    try:
        # Call OpenAI API (stub)
        openai_result = call_openai_api({"message": request.message})
        # Simulate function call detection (stub)
        # In real use, parse openai_result for function call info
        function_call = openai_result.get("function_call") if openai_result else None
        response_text = openai_result.get("response") if openai_result else ""
        result = None
        if function_call:
            func_name = function_call.get("name")
            args = function_call.get("arguments", {})
            func = FUNCTIONS.get(func_name)
            if func:
                result = func(**args)
                response_text = f"Function '{func_name}' called. Result: {result}"
            else:
                response_text = f"Function '{func_name}' not found."
        chat_response = ChatResponse(response=response_text, function_call=function_call, error=None)
        log_response(chat_response)
        return chat_response
    except Exception as e:
        log_error(str(e))
        return ChatResponse(response="", function_call=None, error=str(e))
