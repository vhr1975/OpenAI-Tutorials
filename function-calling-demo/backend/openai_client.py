


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
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_BASE
)

def call_openai_api(payload):
    # Call Azure OpenAI ChatCompletion with function definitions (SDK >=1.0.0)
    message = payload.get("message", "")
    functions = payload.get("functions", [])
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": message}],
            functions=functions,
            function_call="auto"
        )
        choice = response.choices[0]
        # If function_call is present, return it
        if hasattr(choice.message, "function_call") and choice.message.function_call:
            return {
                "function_call": {
                    "name": choice.message.function_call.name,
                    "arguments": choice.message.function_call.arguments
                },
                "response": None
            }
        return {"function_call": None, "response": choice.message.content}
    except Exception as e:
        return {"function_call": None, "response": str(e)}
        return {"function_call": None, "response": choice.message.content}
    except Exception as e:
        return {"function_call": None, "response": str(e)}
