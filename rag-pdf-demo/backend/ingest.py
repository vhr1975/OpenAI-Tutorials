"""
ingest.py: Ingestion pipeline for RAG PDF demo.
Steps:
	- Load PDFs from data directory
	- Chunk text for semantic search
	- Generate embeddings using Azure OpenAI
	- Store chunks and embeddings in ChromaDB vectorstore
"""

# Standard library
import os
# LangChain for PDF loading and text splitting
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Azure OpenAI client
from openai import AzureOpenAI
# ChromaDB for vectorstore
import chromadb


# Path to PDF data
DATA_PATH = "./data/"
# (Unused) FAISS path stub
DB_FAISS_PATH = "vectorstore/db_faiss"


# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv("../../.env")  # Loads all .env variables from project root



# Load Azure OpenAI config from environment
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Create AzureOpenAI client for embedding generation
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_BASE
)


# PDFIngestor: Handles loading, chunking, embedding, and storing



class PDFIngestor:
	def __init__(self, data_path=DATA_PATH):
		self.data_path = data_path

	def load_pdfs(self):
		"""
		Load all PDF files from the data directory using LangChain.
		"""
		loader = DirectoryLoader(self.data_path, glob="*.pdf", loader_cls=PyPDFLoader)
		documents = loader.load()
		print(f"Loaded {len(documents)} documents from {self.data_path}")
		return documents

	def chunk_text(self, documents):
		"""
		Split loaded documents into smaller chunks for semantic search.
		"""
		text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
		chunks = text_splitter.split_documents(documents)
		print(f"Split documents into {len(chunks)} chunks")
		return chunks

	def generate_embeddings(self, chunks):
		"""
		Generate embeddings for each chunk using Azure OpenAI.
		Each chunk is sent to the embedding endpoint; results are collected.
		"""
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
		"""
		Store chunk texts and their embeddings in ChromaDB vectorstore.
		Each chunk is assigned a unique ID.
		"""
		client = chromadb.Client()
		collection = client.create_collection(name="pdf_chunks")
		ids = [str(i) for i in range(len(texts))]
		collection.add(documents=texts, embeddings=embeddings, ids=ids)
		print(f"Stored {len(texts)} chunks in ChromaDB")

	def run(self):
		"""
		End-to-end ingestion pipeline:
			1. Load PDFs
			2. Chunk text
			3. Generate embeddings
			4. Store in ChromaDB
		"""
		documents = self.load_pdfs()
		chunks = self.chunk_text(documents)
		texts, embeddings = self.generate_embeddings(chunks)
		self.build_vectorstore(texts, embeddings)
		print("Ingestion complete.")


# Run ingestion pipeline if script is executed directly
if __name__ == "__main__":
	ingestor = PDFIngestor()
	ingestor.run()
