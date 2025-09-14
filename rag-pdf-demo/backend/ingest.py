"""
ingest.py: Load PDFs, chunk text, generate OpenAI embeddings, and build FAISS vectorstore.
"""
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
import chromadb

DATA_PATH = "./data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

import os
from dotenv import load_dotenv
load_dotenv("../../.env")  # Loads all .env variables from project root


# Load Azure OpenAI config from environment
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Create AzureOpenAI client
client = AzureOpenAI(
	api_key=AZURE_OPENAI_API_KEY,
	api_version=AZURE_OPENAI_API_VERSION,
	azure_endpoint=AZURE_OPENAI_API_BASE
)

# TODO: Implement OpenAI embedding logic and vectorstore creation
# --- Stubs for ingestion pipeline ---


class PDFIngestor:
	def __init__(self, data_path=DATA_PATH):
		self.data_path = data_path

	def load_pdfs(self):
		"""Load PDFs from data directory."""
		loader = DirectoryLoader(self.data_path, glob="*.pdf", loader_cls=PyPDFLoader)
		documents = loader.load()
		print(f"Loaded {len(documents)} documents from {self.data_path}")
		return documents

	def chunk_text(self, documents):
		"""Chunk documents into smaller pieces."""
		text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
		chunks = text_splitter.split_documents(documents)
		print(f"Split documents into {len(chunks)} chunks")
		return chunks

	def generate_embeddings(self, chunks):
		"""Generate Azure OpenAI embeddings for text chunks."""
		texts = [chunk.page_content for chunk in chunks]
		embeddings = []
		for text in texts:
			response = client.embeddings.create(
				input=[text],
				model=AZURE_OPENAI_DEPLOYMENT
			)
			embeddings.append(response.data[0].embedding)
		print(f"Generated {len(embeddings)} embeddings")
		return texts, embeddings

	def build_vectorstore(self, texts, embeddings):
		"""Build ChromaDB vectorstore from embeddings."""
		client = chromadb.Client()
		collection = client.create_collection(name="pdf_chunks")
		ids = [str(i) for i in range(len(texts))]
		collection.add(documents=texts, embeddings=embeddings, ids=ids)
		print(f"Stored {len(texts)} chunks in ChromaDB")

	def run(self):
		documents = self.load_pdfs()
		chunks = self.chunk_text(documents)
		texts, embeddings = self.generate_embeddings(chunks)
		self.build_vectorstore(texts, embeddings)
		print("Ingestion complete.")

if __name__ == "__main__":
	ingestor = PDFIngestor()
	ingestor.run()
