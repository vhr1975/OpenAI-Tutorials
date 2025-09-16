import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import AzureOpenAI
import chromadb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Local folder for storing uploaded PDFs
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory PDF tracker (demo only)
pdf_store = {}

# Chroma collection
CHROMA_COLLECTION_NAME = "pdf_chunks"

# Initialize FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG PDF Demo API")

# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class RAGQA:
    def __init__(self, collection_name=CHROMA_COLLECTION_NAME):
        # Connect to Chroma (PersistentClient if you want disk persistence)
        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection(collection_name)
        except Exception:
            self.collection = self.client.create_collection(name=collection_name)

        # Azure OpenAI config
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        self.openai_client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base,
        )

    def retrieve(self, query: str, k: int = 3) -> str:
        results = self.collection.query(query_texts=[query], n_results=k)
        documents = results.get("documents", [[]])[0]
        return "\n".join(documents)

    def answer(self, query: str, context: str) -> str:
        prompt = f"""
Use the following context to answer the user's question.
If you don't know, say you don't know.

Context:
{context}

Question: {query}
Answer:
"""
        response = self.openai_client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def run(self, query: str) -> str:
        context = self.retrieve(query)
        return self.answer(query, context)


# Instantiate the RAG pipeline
rag_qa = RAGQA()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Save uploaded PDF into the local data/ folder."""
    try:
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        pdf_store[file.filename] = {
            "path": file_path,
            "ingested": False,  # ingestion happens offline
        }

        return {"file_id": file.filename, "status": "uploaded"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/query")
def query_api(request: QueryRequest):
    """Query against already ingested Chroma collection."""
    try:
        answer = rag_qa.run(request.question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
