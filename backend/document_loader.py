# brass-fax-ai/backend/document_loader.py

import os
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredHTMLLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# Load env vars from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Where the vector stores are persisted
CHROMA_BASE_DIR = "../data"

# Select appropriate loader based on file type
def select_loader(file_path: str):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return UnstructuredPDFLoader(file_path)
    elif ext == ".docx":
        return UnstructuredWordDocumentLoader(file_path)
    elif ext in [".html", ".htm"]:
        return UnstructuredHTMLLoader(file_path)
    elif ext == ".txt":
        return TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# Main ingestion function
def ingest_document(client_id: str, file_path: str):
    loader = select_loader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    client_vector_path = os.path.join(CHROMA_BASE_DIR, client_id)
    vectordb = Chroma(persist_directory=client_vector_path, embedding_function=embeddings)
    vectordb.add_documents(chunks)

    print(f"✅ Ingested {len(chunks)} chunks for client '{client_id}' from file '{file_path}'.")

# Batch ingestion for all files inside a client's folder
def ingest_folder(client_id: str):
    client_folder = os.path.join(CHROMA_BASE_DIR, client_id)
    files = os.listdir(client_folder)

    for filename in files:
        file_path = os.path.join(client_folder, filename)
        try:
            ingest_document(client_id, file_path)
        except Exception as e:
            print(f"⚠ Skipping {filename}: {str(e)}")

# CLI usage
if __name__ == "__main__":
    # Example run for internal Brass Fax docs
    client_id = "brassfax_internal"
    ingest_folder(client_id)
