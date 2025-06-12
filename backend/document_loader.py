import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Path hardening applied:
# Dynamically resolve base directory for SaaS-safe file system access
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

# ✅ Define client ID here for ingestion - you can easily modify this when onboarding new clients
client_id = "brassfax_internal"
client_vector_path = os.path.join(CHROMA_BASE_DIR, client_id)

# ✅ Where your ingestion docs live relative to deployment
docs_path = os.path.join(BASE_DIR, "static", "docs")

# ✅ Loader handles multiple file types — SaaS safe for most client document needs
loader = DirectoryLoader(
    docs_path,
    glob="**/*",
    loader_cls_mapping={
        ".pdf": UnstructuredPDFLoader,
        ".docx": UnstructuredWordDocumentLoader,
        ".txt": TextLoader
    }
)

# Load and embed documents
documents = loader.load()

# Generate embeddings + store into Chroma vector DB
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(documents, embeddings, persist_directory=client_vector_path)
vectordb.persist()

print("✅ Ingestion complete for client:", client_id)
