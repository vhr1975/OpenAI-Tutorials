"""
ingest.py: Load PDFs, chunk text, generate OpenAI embeddings, and build FAISS vectorstore.
"""
import os
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import chromadb

DATA_PATH = "./data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

# TODO: Implement OpenAI embedding logic and vectorstore creation
# --- Stubs for ingestion pipeline ---

class PDFIngestor:
	def __init__(self, data_path=DATA_PATH):
		self.data_path = data_path

	def load_pdfs(self):
		"""Stub: Load PDFs from data directory."""
		pass

	def chunk_text(self, documents):
		"""Stub: Chunk documents into smaller pieces."""
		pass

	def generate_embeddings(self, chunks):
		"""Stub: Generate OpenAI embeddings for text chunks."""
		pass

	def build_vectorstore(self, embeddings):
		"""Stub: Build ChromaDB vectorstore from embeddings."""
		# Example stub for ChromaDB
		client = chromadb.Client()
		collection = client.create_collection(name="pdf_chunks")
		# collection.add(documents=chunks, embeddings=embeddings)
		pass

	def run(self):
		"""Stub: Run full ingestion pipeline."""
		pass

if __name__ == "__main__":
	ingestor = PDFIngestor()
	ingestor.run()
