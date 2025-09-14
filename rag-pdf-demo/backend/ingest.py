"""
ingest.py: Load PDFs, chunk text, generate OpenAI embeddings, and build FAISS vectorstore.
"""
import os
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import faiss

DATA_PATH = "./data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

# TODO: Implement OpenAI embedding logic and vectorstore creation
