from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Path resolution fully hardened for SaaS deployment:
# Dynamically resolve the absolute path to /data directory regardless of Docker or Railway working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for cross-origin browser requests (necessary for embedding)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (your frontend widget assets)
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/query")
async def query(request: Request):
    # Core multi-client logic unchanged
    body = await request.json()
    client_id = body["client_id"]
    question = body["question"]

    # Fully hardened path resolution for correct vector store access
    client_vector_path = os.path.join(CHROMA_BASE_DIR, client_id)

    # Load embeddings + ChromaDB from correct path
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma(persist_directory=client_vector_path, embedding_function=embeddings)
    retriever = vectordb.as_retriever()

    # Build RetrievalQA chain
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o", temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    # Run query
    answer = qa.invoke(question)

    # Fix applied: RetrievalQA returns full dict, extract only 'result'
    return {"answer": answer['result']}
