# =============================================================
# Azure OpenAI Client (openai_client.py)
# -------------------------------------------------------------
# This file configures the Azure OpenAI client for the backend.
# It loads credentials and endpoint info from environment variables
# and provides a function to send chat requests and handle function calls.
#
# Key Concepts for Beginners:
# - How to securely load API keys and endpoints
# - How to use the AzureOpenAI client (SDK >=1.0.0)
# - How to send chat requests with function definitions
# - How to parse and return function call results
# =============================================================

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Load Azure OpenAI environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# Create AzureOpenAI client (SDK >=1.0.0)
# For robust developer experience, handle API errors and rate limits gracefully.
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_BASE
)

def call_openai_api(payload):
    """
    Send a chat request to Azure OpenAI with optional function definitions.
    This function demonstrates how to:
    - Accept a payload containing a user message and a list of function schemas
    - Call the Azure OpenAI ChatCompletion API (SDK >=1.0.0)
    - Automatically trigger function calls if the LLM decides one is needed
    - Parse and return the function call details or the model's response
    - Handle errors gracefully for robust developer experience

    Args:
        payload (dict): {
            "message": str,  # The user's message to the LLM
            "functions": list # List of function definitions (OpenAI schema)
        }

    Returns:
        dict: {
            "function_call": dict or None, # Details if a function call is triggered
            "response": str or None        # LLM response if no function call
        }
    """
    message = payload.get("message", "")
    functions = payload.get("functions", [])
    try:
        # Send the chat request to Azure OpenAI
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": message}],
            functions=functions,           # Pass function definitions for LLM to choose from
            function_call="auto"          # Let LLM decide if/which function to call
        )
        choice = response.choices[0]
        # If the LLM triggers a function call, extract its name and arguments
        if hasattr(choice.message, "function_call") and choice.message.function_call:
            return {
                "function_call": {
                    "name": choice.message.function_call.name,
                    "arguments": choice.message.function_call.arguments
                },
                "response": None
            }
        # Otherwise, return the LLM's direct response
        return {"function_call": None, "response": choice.message.content}
    except Exception as e:
        # On error, return the error message for debugging or user feedback
        return {"function_call": None, "response": str(e)}
        return {"function_call": None, "response": choice.message.content}
    except Exception as e:
        return {"function_call": None, "response": str(e)}
