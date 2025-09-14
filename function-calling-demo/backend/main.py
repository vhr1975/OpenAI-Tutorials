# =============================================================
# Function Calling Demo Backend (main.py)
# -------------------------------------------------------------
# This file is the entry point for the backend API.
# It demonstrates how to use Azure OpenAI to call Python functions
# from natural language using FastAPI.
#
# Key Concepts for Beginners:
# - How user messages are received and processed
# - How OpenAI/Azure suggests function calls
# - How Python functions are dynamically invoked
# - How to extend the backend with new functions
# - How to use environment variables for secure API access
#
# Try sending a POST request to /chat with a message like:
#   {"message": "What's the weather in Paris?", "user_id": "user123"}
# and see how the backend responds!
# =============================================================

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from functions import FUNCTIONS
from openai_client import call_openai_api
from utils import log_request, log_response, log_error
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()

# Enable CORS for frontend integration
# This allows the React frontend to communicate with the backend during development.
# In production, update allow_origins to match your deployed frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This model defines what a chat request looks like
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

# This model defines what a chat response looks like
class ChatResponse(BaseModel):
    response: str
    function_call: Optional[dict] = None
    error: Optional[str] = None

# This function tells OpenAI what backend functions are available to call
def get_function_definitions():
    # Each function has a name, description, and parameters
    return [
        {
            "name": "get_weather",
            "description": "Get weather forecast for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Location name"}
                },
                "required": ["location"]
            }
        },
        {
            "name": "get_events",
            "description": "Get calendar events for a date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                },
                "required": ["date"]
            }
        },
        {
            "name": "translate",
            "description": "Translate text to a target language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "target_lang": {"type": "string", "description": "Target language code"}
                },
                "required": ["text", "target_lang"]
            }
        }
    ]

# Simple health check endpoint
@app.get("/")
def read_root():
    return {"message": "Function Calling Demo Backend"}

# This is the main endpoint for chat and function calling
from fastapi import Body
from fastapi import APIRouter

# Add an OpenAPI example for the /chat endpoint to help developers in Swagger UI
@app.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a chat message and trigger function calling",
    response_description="Chat response with optional function call details",
    tags=["Chat"],
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "message": "What's the weather in Paris?",
                        "user_id": "user123"
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": {
                            "response": "Function 'get_weather' called. Result: Sunny in Paris.",
                            "function_call": {
                                "name": "get_weather",
                                "arguments": {"location": "Paris"}
                            },
                            "error": None
                        }
                    }
                }
            }
        }
    }
)
async def chat_endpoint(request: ChatRequest = Body(..., example={"message": "What's the weather in Paris?", "user_id": "user123"})):
    # Log the incoming request for debugging and monitoring
    log_request(request)
    try:
        # 1. Send the user's message and available functions to OpenAI
        openai_result = call_openai_api({
            "message": request.message,
            "functions": get_function_definitions()
        })
        # 2. See if OpenAI wants to call a function
        function_call = openai_result.get("function_call") if openai_result else None
        response_text = openai_result.get("response") if openai_result else ""
        result = None
        if function_call:
            # 3. If a function call is requested, get the function name and arguments
            func_name = function_call.get("name")
            args = function_call.get("arguments", {})
            # Arguments may be a JSON string, so parse if needed
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            # 4. Look up the Python function in our registry
            # To add new functions, simply define them in the functions/ directory
            # and register them in FUNCTIONS (see functions/__init__.py)
            func = FUNCTIONS.get(func_name)
            if func:
                # 5. Call the function with the provided arguments
                result = func(**args)
                response_text = f"Function '{func_name}' called. Result: {result}"
            else:
                response_text = f"Function '{func_name}' not found."
        # 6. Build the response object
        chat_response = ChatResponse(response=response_text, function_call=function_call, error=None)
        # Log the response for debugging
        log_response(chat_response)
        return chat_response
    except Exception as e:
        # If anything goes wrong, log the error and return it
        log_error(str(e))
        return ChatResponse(response="", function_call=None, error=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
