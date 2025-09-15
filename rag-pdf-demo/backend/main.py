
"""
main.py: FastAPI backend for RAG PDF demo.
Handles retrieval-augmented generation (RAG) flow:
    - Loads PDF chunks from ChromaDB vectorstore
    - Retrieves relevant chunks for a user query
    - Uses Azure OpenAI to generate answers based on retrieved context
"""

# FastAPI for API endpoints
from fastapi import FastAPI, Query
# Pydantic for request validation
from pydantic import BaseModel
# Azure OpenAI client
from openai import AzureOpenAI
# ChromaDB for vectorstore
import chromadb
import os
# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv("../../.env")


# Name of ChromaDB collection storing PDF chunks
CHROMA_COLLECTION_NAME = "pdf_chunks"


# Initialize FastAPI app
app = FastAPI()


# Request schema for /query endpoint
class QueryRequest(BaseModel):
    question: str



# RAGQA: Handles retrieval and QA using ChromaDB and Azure OpenAI
class RAGQA:
    def __init__(self, collection_name=CHROMA_COLLECTION_NAME):
        # Connect to ChromaDB
        self.client = chromadb.Client()
        # Try to get the collection, create if missing
        try:
            self.collection = self.client.get_collection(collection_name)
        except Exception:
            # If collection doesn't exist, create it
            self.collection = self.client.create_collection(name=collection_name)

        # Load Azure OpenAI config from environment
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        # Initialize Azure OpenAI client
        self.openai_client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base
        )

    def retrieve(self, query, k=3):
        """
        Retrieve top-k relevant chunks from ChromaDB for the input query.
        Returns concatenated context string.
        """
        results = self.collection.query(query_texts=[query], n_results=k)
        documents = results.get("documents", [[]])[0]
        context = "\n".join(documents)
        return context

    def answer(self, query, context):
        """
        Use Azure OpenAI to answer the user's question based on retrieved context.
        Sends a prompt to the chat completion endpoint.
        """
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
        """
        End-to-end RAG flow: retrieve context and answer question.
        """
        context = self.retrieve(query)
        return self.answer(query, context)


# Instantiate RAGQA (loads ChromaDB and Azure OpenAI)
rag_qa = RAGQA()


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Main query endpoint: receives user question, returns answer
@app.post("/query")
def query_api(request: QueryRequest):
    answer = rag_qa.run(request.question)
    return {"answer": answer}
