
"""
main.py: FastAPI backend for RAG PDF demo. Handles retrieval and QA logic.
"""
from fastapi import FastAPI, Query
from pydantic import BaseModel
import openai
import faiss

DB_FAISS_PATH = "vectorstore/db_faiss"

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class RAGQA:
    def __init__(self, db_path=DB_FAISS_PATH):
        self.db_path = db_path

    def retrieve(self, query):
        """Stub: Retrieve relevant chunks from vectorstore."""
        return "[stubbed context]"

    def answer(self, query, context):
        """Stub: Run OpenAI completion for QA."""
        return f"[stubbed answer for: {query}]"

    def run(self, query):
        context = self.retrieve(query)
        return self.answer(query, context)

rag_qa = RAGQA()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query_api(request: QueryRequest):
    answer = rag_qa.run(request.question)
    return {"answer": answer}
