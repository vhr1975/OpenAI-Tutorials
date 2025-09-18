
"""
main.py: FastAPI backend stub for RAG Vision Demo

This file implements the API for Retrieval-Augmented Generation (RAG) with GPT-4o Vision.

Features to implement:
- Image upload endpoint: saves images to local storage
- Vision Q&A endpoint: answers questions about uploaded images using GPT-4o Vision
- Health endpoint: basic service status
"""



import os
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import AzureOpenAI


# Load environment variables
load_dotenv()

# Azure OpenAI config
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Azure OpenAI client
openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_BASE,
)

app = FastAPI(title="RAG Vision Demo API")

# Directory for storing uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory image tracker (demo only)
image_store = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Save uploaded image into the local uploads/ folder.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        image_store[file.filename] = {
            "path": file_path,
            "uploaded": True,
        }
        return {"file_id": file.filename, "status": "uploaded"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/query")
async def query_vision(file_id: str = Body(...), question: str = Body(...)):
    """
    Answer a question about an uploaded image using Azure OpenAI GPT-4o Vision.
    """
    image_info = image_store.get(file_id)
    if not image_info:
        return JSONResponse(status_code=404, content={"error": "Image not found. Please upload first."})
    image_path = image_info["path"]
    # Stub: Call Azure OpenAI GPT-4o Vision API (pseudo-code)
    try:
        # with open(image_path, "rb") as img_file:
        #     response = openai_client.chat.completions.create(
        #         model=AZURE_OPENAI_DEPLOYMENT,
        #         messages=[
        #             {"role": "system", "content": "You are a helpful vision assistant."},
        #             {"role": "user", "content": [
        #                 {"type": "text", "text": question},
        #                 {"type": "image", "image": img_file.read()}
        #             ]}
        #         ],
        #         max_tokens=256
        #     )
        #     answer = response.choices[0].message.content
        answer = f"[Stub] Would call GPT-4o Vision for '{question}' on '{file_id}'."
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
