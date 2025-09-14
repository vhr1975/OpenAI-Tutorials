
"""
main.py: FastAPI backend for RAG PDF demo. Handles retrieval and QA logic.
"""
from fastapi import FastAPI, Query
from pydantic import BaseModel
from openai import AzureOpenAI
import chromadb
import os
from dotenv import load_dotenv
load_dotenv("../../.env")

CHROMA_COLLECTION_NAME = "pdf_chunks"

app = FastAPI()

class QueryRequest(BaseModel):
    question: str


class RAGQA:
    def __init__(self, collection_name=CHROMA_COLLECTION_NAME):
        self.client = chromadb.Client()
        # Try to get the collection, create if missing
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
            azure_endpoint=self.api_base
        )

    def retrieve(self, query, k=3):
        """Retrieve top-k relevant chunks from ChromaDB."""
        results = self.collection.query(query_texts=[query], n_results=k)
        documents = results.get("documents", [[]])[0]
        context = "\n".join(documents)
        return context

    def answer(self, query, context):
        """Run Azure OpenAI completion for QA."""
        prompt = f"""
Use the following context to answer the user's question. If you don't know, say you don't know.
Context:
{context}
Question: {query}
Answer:
"""
        response = self.openai_client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

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
